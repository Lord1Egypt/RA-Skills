#!/usr/bin/env python3
"""
Index PDFs into the knowledge base.
Extracts text from PDF files (including image-based PDFs via OCR) and creates 
temporary markdown files for indexing.

Phase 2.1: ChromaDB Integration
Phase 2.2: OCR-Parallelization (ThreadPoolExecutor)
"""

import sys
import uuid
import json
import tempfile
import hashlib
import re
import os
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# Import the indexer
sys.path.insert(0, str(Path(__file__).parent.parent))
from indexer import BiblioIndexer, MarkdownIndexer

try:
    import pypdf
except ImportError:
    print("ERROR: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


class TesseractOCR:
    """
    Tesseract OCR - Alternative to EasyOCR.
    
    Advantages:
    - Faster than EasyOCR
    - No GPU needed
    - Better accuracy on clean documents
    
    Requires:
    - tesseract installed (apt install tesseract-ocr)
    - German/English language files (deu-eng.traineddata)
    """
    
    _available = None
    _version = None
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if Tesseract is installed."""
        if cls._available is None:
            try:
                result = subprocess.run(
                    ['tesseract', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                cls._available = result.returncode == 0
                if cls._available:
                    # Extract version number
                    import re
                    match = re.search(r'tesseract\s+(\d+\.\d+)', result.stdout)
                    cls._version = match.group(1) if match else 'unknown'
            except (subprocess.SubprocessError, FileNotFoundError):
                cls._available = False
                cls._version = None
        return cls._available
    
    @classmethod
    def get_version(cls) -> str:
        """Return Tesseract version."""
        cls.is_available()  # Ensure _version is set
        return cls._version or 'not installed'
    
    @classmethod
    def ocr_image(cls, image_path: str) -> str:
        """
        Run Tesseract OCR on an image file.
        
        Args:
            image_path: Path to image
            
        Returns:
            Extracted text
        """
        if not cls.is_available():
            raise RuntimeError("Tesseract is not installed")
        
        try:
            result = subprocess.run(
                ['tesseract', image_path, 'stdout', '-l', 'deu+eng', '--psm', '6'],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                print(f"  ⚠️  Tesseract error: {result.stderr}")
                return ""
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Tesseract timeout for {image_path}")
            return ""
        except Exception as e:
            print(f"  ⚠️  Tesseract exception: {e}")
            return ""
    
    @classmethod
    def _ocr_page_worker(cls, args: tuple) -> tuple:
        """Worker function for parallel Tesseract OCR."""
        page_num, img_bytes, tmpdir = args
        img_path = Path(tmpdir) / f"page_{page_num}.png"
        with open(str(img_path), 'wb') as f:
            f.write(img_bytes)
        txt = cls.ocr_image(str(img_path))
        return page_num, txt
    
    @classmethod
    def pdf_pages_to_text(cls, pdf_path: Path, parallel: bool = True, max_workers: int = 4) -> str:
        """
        Convert PDF pages to images and run Tesseract OCR.
        
        Args:
            pdf_path: Path to PDF file
            parallel: Use ThreadPoolExecutor (default: True)
            max_workers: Number of parallel workers (default: 4)
        """
        if not cls.is_available():
            raise RuntimeError("Tesseract is not installed")
        
        try:
            import fitz  # PyMuPDF
            with tempfile.TemporaryDirectory() as tmpdir:
                doc = fitz.open(str(pdf_path))
                
                # Pre-render all pages to images
                zoom = 200 / 72  # 200 DPI for good OCR quality
                mat = fitz.Matrix(zoom, zoom)
                
                page_images = []
                for page_num, page in enumerate(doc):
                    pix = page.get_pixmap(matrix=mat)
                    img_bytes = pix.tobytes("png")
                    page_images.append((page_num, img_bytes, tmpdir))
                
                text_parts = []
                
                if parallel and len(page_images) > 1:
                    # Parallel OCR processing
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = {executor.submit(cls._ocr_page_worker, args): args[0] 
                                   for args in page_images}
                        
                        for future in as_completed(futures):
                            page_num, txt = future.result()
                            if txt.strip():
                                text_parts.append((page_num, f"## Page {page_num+1}\n\n{txt}"))
                else:
                    # Sequential processing
                    for page_num, img_bytes, _img_tmpdir in page_images:
                        _, txt = cls._ocr_page_worker((page_num, img_bytes, tmpdir))
                        if txt.strip():
                            text_parts.append((page_num, f"## Page {page_num+1}\n\n{txt}"))
                
                # Sort by page number and join
                text_parts.sort(key=lambda x: x[0])
                return "\n\n".join([t for _, t in text_parts])
        except Exception as e:
            print(f"  ⚠️  Tesseract OCR error: {e}")
            return ""


class OCRProcessor:
    """
    OCR processing with support for both EasyOCR and Tesseract.
    
    Preference order:
    1. Tesseract (if available - faster, more accurate)
    2. EasyOCR (Fallback)
    
    Usage:
        OCRProcessor.pdf_pages_to_text(pdf_path)  # Automatic selection
        OCRProcessor.use_tesseract = True  # Force Tesseract
    """
    
    _reader = None
    _gpu_available = None
    use_tesseract = False  # Class variable to force Tesseract
    
    @classmethod
    def _check_gpu(cls) -> bool:
        """Check if GPU is available."""
        if cls._gpu_available is None:
            try:
                import torch
                cls._gpu_available = torch.cuda.is_available()
            except ImportError:
                cls._gpu_available = False
        return cls._gpu_available
    
    @classmethod
    def get_reader(cls):
        """Lazy-load EasyOCR reader."""
        if cls._reader is None:
            import easyocr
            gpu = cls._check_gpu()
            cls._reader = easyocr.Reader(['de', 'en'], gpu=gpu, verbose=False)
            print(f"  🖥️  EasyOCR initialized (GPU: {gpu})")
        return cls._reader
    
    @classmethod
    def ocr_image(cls, image_path: str, detail: int = 0) -> str:
        """
        Run OCR on an image file.
        
        Automatic OCR engine selection:
        - Tesseract if available (preferred)
        - EasyOCR as fallback
        
        detail: 0 = list of strings, 1 = list of tuples (bbox, text, conf)
        """
        # Try Tesseract first if available or forced
        if cls.use_tesseract or TesseractOCR.is_available():
            if TesseractOCR.is_available():
                return TesseractOCR.ocr_image(image_path)
            elif cls.use_tesseract:
                print("  ⚠️  Tesseract requested but not available, falling back to EasyOCR")
        
        # Fallback to EasyOCR
        reader = cls.get_reader()
        results = reader.readtext(image_path, detail=detail)
        
        if detail == 0:
            if isinstance(results, list):
                return '\n'.join([r.strip() for r in results if r.strip() and len(r.strip()) > 1])
            return str(results) if results else ""
        else:
            if isinstance(results, list):
                return '\n'.join([r[1].strip() for r in results if r[1].strip()])
            return str(results)
    
    @classmethod
    def _ocr_page_worker(cls, args: tuple) -> tuple:
        """Worker function for parallel OCR processing."""
        page_num, img_bytes, tmpdir = args
        img_path = Path(tmpdir) / f"page_{page_num}.png"
        with open(str(img_path), 'wb') as f:
            f.write(img_bytes)
        txt = cls.ocr_image(str(img_path), detail=0)
        return page_num, txt
    
    @classmethod
    def pdf_pages_to_text(cls, pdf_path: Path, parallel: bool = True, max_workers: int = 4) -> str:
        """
        Convert PDF pages to images and run OCR.
        
        Automatic engine selection:
        - Tesseract (if available): Faster, better for documents
        - EasyOCR (Fallback): For images and complex layouts
        """
        # Determine which OCR engine to use
        if cls.use_tesseract or TesseractOCR.is_available():
            if TesseractOCR.is_available():
                print(f"  📷 Using Tesseract OCR v{TesseractOCR.get_version()}")
                return TesseractOCR.pdf_pages_to_text(pdf_path, parallel, max_workers)
            elif cls.use_tesseract:
                print("  ⚠️  Tesseract requested but not available, falling back to EasyOCR")
        
        # Fallback to EasyOCR
        print(f"  📷 Using EasyOCR")
        return cls._pdf_pages_to_text_easyocr(pdf_path, parallel, max_workers)
    
    @classmethod
    def _pdf_pages_to_text_easyocr(cls, pdf_path: Path, parallel: bool = True, max_workers: int = 4) -> str:
        """EasyOCR implementation for backwards compatibility."""
        try:
            import fitz  # PyMuPDF
            with tempfile.TemporaryDirectory() as tmpdir:
                doc = fitz.open(str(pdf_path))
                
                # Pre-render all pages to images
                zoom = 200 / 72  # 200 DPI for good OCR quality
                mat = fitz.Matrix(zoom, zoom)
                
                page_images = []
                for page_num, page in enumerate(doc):
                    pix = page.get_pixmap(matrix=mat)
                    img_bytes = pix.tobytes("png")
                    page_images.append((page_num, img_bytes, tmpdir))
                
                text_parts = []
                
                if parallel and len(page_images) > 1:
                    # Parallel OCR processing
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = {executor.submit(cls._ocr_page_worker, args): args[0] 
                                   for args in page_images}
                        
                        for future in as_completed(futures):
                            page_num, txt = future.result()
                            if txt.strip():
                                text_parts.append((page_num, f"## Page {page_num+1}\n\n{txt}"))
                else:
                    # Sequential processing
                    for page_num, img_bytes, _img_tmpdir in page_images:
                        _, txt = cls._ocr_page_worker((page_num, img_bytes, tmpdir))
                        if txt.strip():
                            text_parts.append((page_num, f"## Page {page_num+1}\n\n{txt}"))
                
                # Sort by page number and join
                text_parts.sort(key=lambda x: x[0])
                return "\n\n".join([t for _, t in text_parts])
        except Exception as e:
            print(f"  ⚠️  OCR fallback error: {e}")
            return ""


class PDFIndexer:
    """Extract text from PDFs and index into knowledge base."""

    # Path to ChromaDB integration — resolved lazily via KBConfig
    CHROMA_INTEGRATION_PATH: Optional[str] = None

    @classmethod
    def _get_chroma_path(cls) -> str:
        if cls.CHROMA_INTEGRATION_PATH is not None:
            return cls.CHROMA_INTEGRATION_PATH
        try:
            from kb.base.config import KBConfig
            cls.CHROMA_INTEGRATION_PATH = str(KBConfig.get_instance().knowledge_base_path)
        except Exception:
            from kb.framework.paths import get_default_base_path
            cls.CHROMA_INTEGRATION_PATH = str(get_default_base_path() / "framework")
        return cls.CHROMA_INTEGRATION_PATH
    
    STOPWORDS = {
        'der', 'die', 'das', 'und', 'oder', 'mit', 'fuer', 'von', 'auf', 'in', 'zu',
        'ist', 'sind', 'war', 'wurden', 'wird', 'werden', 'kann', 'koennen',
        'eine', 'einer', 'einem', 'einen', 'als', 'an', 'auch', 'bei', 'bis',
        'durch', 'fuer', 'hat', 'nach', 'nicht', 'nur', 'ob', 'oder', 'sich',
        'sie', 'sind', 'so', 'sowie', 'um', 'unter', 'von', 'vor', 'wenn',
        'wie', 'wird', 'noch', 'schon', 'sehr', 'wurde', 'wurden', 'sein'
    }
    
    def __init__(self, kb_indexer: BiblioIndexer):
        self.kb_indexer = kb_indexer
        self._chroma = None
    
    def _get_chroma(self):
        """Lazy-load ChromaDB integration (singleton)."""
        if self._chroma is None:
            sys.path.insert(0, self.CHROMA_INTEGRATION_PATH)
            from chroma_integration import get_chroma
            self._chroma = get_chroma()
        return self._chroma
    
    def _embed_sections_for_file(self, file_path: str, file_id: str) -> int:
        """
        Generate and store embeddings for all sections of a file in ChromaDB.
        
        Phase 2.1: PDF -> ChromaDB Integration
        """
        try:
            chroma = self._get_chroma()
            collection = chroma.sections_collection
            
            # Load sections from DB
            cursor = self.kb_indexer.conn.execute(
                """SELECT id, section_header, content_preview, keywords 
                   FROM file_sections WHERE file_path = ?""",
                (file_path,)
            )
            sections = cursor.fetchall()
            
            if not sections:
                return 0
            
            # Build texts for embedding
            ids = []
            embeddings = []
            metadatas = []
            documents = []
            
            for section_id, header, preview, keywords in sections:
                text = f"{header} | {preview[:500] if preview else ''} | Keywords: {keywords[:100] if keywords else ''}"
                emb = chroma.embed_text(text)
                
                ids.append(section_id)
                embeddings.append(emb)
                metadatas.append({
                    "file_id": file_id,
                    "file_path": file_path,
                    "section_header": header,
                    "keywords": keywords
                })
                documents.append(text)
            
            # Upsert to ChromaDB
            collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
            return len(sections)
        except Exception as e:
            print(f"  ⚠️  ChromaDB embedding error: {e}")
            return 0
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract full text from PDF file. Falls back to OCR for image-based PDFs."""
        try:
            reader = pypdf.PdfReader(pdf_path)
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"## Page {i+1}\n\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            
            # Count meaningful words (4+ letters)
            word_count = len(re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', full_text))
            
            # If fewer than 5 words extracted, try OCR (likely image-based PDF)
            if word_count < 5:
                print(f"  🔍 Only {word_count} words extracted — attempting OCR...")
                full_text = OCRProcessor.pdf_pages_to_text(pdf_path)
            
            return full_text
        except Exception as e:
            print(f"  ⚠️  Error reading {pdf_path.name}: {e}")
            return ""
    
    def _extract_keywords(self, text: str, top_n: int = 15) -> list:
        """Extract keywords from text."""
        words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', text.lower())
        keywords = [w for w in words if w not in self.STOPWORDS]
        return [k for k, _ in Counter(keywords).most_common(top_n)]
    
    def _categorize_pdf(self, path: Path) -> str:
        """Categorize PDF based on path."""
        path_str = str(path).lower()
        if 'medizin_studien' in path_str or 'medizin-studien' in path_str:
            return 'medizin_studien'
        elif 'gesundheit' in path_str:
            return 'gesundheit'
        elif 'buecher' in path_str or 'bucher' in path_str:
            return 'buecher'
        elif 'aluminium' in path_str:
            return 'aluminium'
        return 'dokumentation'
    
    def _hash_file(self, file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        return hashlib.md5(file_path.read_bytes()).hexdigest()
    
    def index_pdf(self, pdf_path: Path) -> int:
        """
        Index a PDF file into the knowledge base.
        
        Extracts text, creates sections, and inserts into DB.
        Returns number of sections indexed.
        """
        if not pdf_path.exists():
            print(f"  ⚠️  File not found: {pdf_path}")
            return 0
        
        # Extract text from PDF
        print(f"  📄 Extracting text from {pdf_path.name}...")
        full_text = self.extract_text_from_pdf(pdf_path)
        
        if not full_text.strip():
            print(f"  ⚠️  No text extracted from {pdf_path.name} (including OCR)")
            return 0
        
        # Prepare data
        file_id = str(uuid.uuid4())
        category = self._categorize_pdf(pdf_path)
        current_hash = self._hash_file(pdf_path)
        
        # Check if already indexed (by hash)
        existing = self.kb_indexer.conn.execute(
            "SELECT file_hash FROM files WHERE file_path = ?",
            (str(pdf_path),)
        ).fetchone()
        
        if existing and existing['file_hash'] == current_hash:
            print(f"  ⏭️  Unchanged: {pdf_path.name}")
            return 0
        
        # Delete old entries
        self.kb_indexer.conn.execute(
            "DELETE FROM file_sections WHERE file_path = ?",
            (str(pdf_path),)
        )
        self.kb_indexer.conn.execute(
            "DELETE FROM files WHERE file_path = ?",
            (str(pdf_path),)
        )
        
        # Insert file record
        self.kb_indexer.conn.execute("""
            INSERT INTO files 
            (id, file_path, file_name, file_category, file_type, 
             file_size, line_count, file_hash, last_modified, index_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'indexed')
        """, (
            file_id,
            str(pdf_path),
            pdf_path.name,
            category,
            'pdf',
            pdf_path.stat().st_size,
            len(full_text.splitlines()),
            current_hash,
            datetime.fromtimestamp(pdf_path.stat().st_mtime)
        ))
        
        # Create sections from PDF text
        # Split by page markers
        pages = re.split(r'## Page \d+', full_text)
        pages = [p.strip() for p in pages if p.strip()]
        
        section_count = 0
        section_ids = []  # Track section IDs for ChromaDB
        for i, page_content in enumerate(pages):
            if not page_content.strip():
                continue
            
            section_id = str(uuid.uuid4())
            section_ids.append(section_id)
            keywords = self._extract_keywords(page_content)
            
            # Create section header from first meaningful line
            first_lines = page_content.split('\n')[:5]
            header_candidate = ' '.join(first_lines)[:100]
            header = f"Page {i+1}: {header_candidate}" if i > 0 else header_candidate[:100]
            
            # Phase 5.2: Better encoding handling
            try:
                content_preview = (page_content[:200] + '...' if len(page_content) > 200 else page_content).encode('utf-8', 'strict').decode('utf-8')
                content_full = page_content.encode('utf-8', 'strict').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                content_preview = (page_content[:200] + '...' if len(page_content) > 200 else page_content).encode('utf-8', 'replace').decode('utf-8')
                content_full = page_content.encode('utf-8', 'replace').decode('utf-8')
            
            self.kb_indexer.conn.execute("""
                INSERT INTO file_sections 
                (id, file_path, section_level, section_header, parent_section_id,
                 content_preview, content_full, line_start, line_end, 
                 keywords, word_count, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                section_id,
                str(pdf_path),
                1,
                header,
                None,
                content_preview,
                content_full,
                i * 100 + 1,
                (i + 1) * 100,
                json.dumps(keywords),
                len(page_content.split()),
                current_hash
            ))
            
            # Index keywords
            for keyword in keywords:
                keyword_id = self.kb_indexer._get_or_create_keyword(keyword)
                if keyword_id:
                    self.kb_indexer.conn.execute("""
                        INSERT OR IGNORE INTO section_keywords 
                        (section_id, keyword_id, weight)
                        VALUES (?, ?, 1.0)
                    """, (section_id, keyword_id))
            
            section_count += 1
        
        self.kb_indexer.conn.commit()
        
        # Phase 2.1: ChromaDB embedding after SQLite commit
        if section_count > 0:
            embedded = self._embed_sections_for_file(str(pdf_path), file_id)
            print(f"  📊 ChromaDB: {embedded} sections embedded")
        
        print(f"  ✅ {pdf_path.name}: {section_count} sections indexed")
        return section_count


class ImageIndexer:
    """Index image files (JPG, PNG, etc.) using OCR."""
    
    STOPWORDS = PDFIndexer.STOPWORDS
    
    def __init__(self, kb_indexer: BiblioIndexer):
        self.kb_indexer = kb_indexer
    
    def _extract_keywords(self, text: str, top_n: int = 15) -> list:
        words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', text.lower())
        keywords = [w for w in words if w not in self.STOPWORDS]
        return [k for k, _ in Counter(keywords).most_common(top_n)]
    
    def _categorize_image(self, path: Path) -> str:
        path_str = str(path).lower()
        if 'medizin_studien' in path_str or 'medizin-studien' in path_str:
            return 'medizin_studien'
        elif 'gesundheit' in path_str:
            return 'gesundheit'
        elif 'bild' in path_str or 'foto' in path_str or 'photo' in path_str:
            return 'bilder'
        return 'dokumentation'
    
    def _hash_file(self, file_path: Path) -> str:
        return hashlib.md5(file_path.read_bytes()).hexdigest()
    
    def index_image(self, image_path: Path) -> int:
        """Index an image file using OCR."""
        if not image_path.exists():
            print(f"  ⚠️  File not found: {image_path}")
            return 0
        
        ext = image_path.suffix.lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
            print(f"  ⚠️  Unsupported image type: {ext}")
            return 0
        
        print(f"  🖼️  Running OCR on {image_path.name}...")
        try:
            text = OCRProcessor.ocr_image(str(image_path), detail=0)
        except Exception as e:
            print(f"  ⚠️  OCR failed for {image_path.name}: {e}")
            return 0
        
        if not text.strip():
            print(f"  ⚠️  No text extracted from {image_path.name}")
            return 0
        
        file_id = str(uuid.uuid4())
        category = self._categorize_image(image_path)
        current_hash = self._hash_file(image_path)
        
        # Delete old entries
        self.kb_indexer.conn.execute(
            "DELETE FROM file_sections WHERE file_path = ?",
            (str(image_path),)
        )
        self.kb_indexer.conn.execute(
            "DELETE FROM files WHERE file_path = ?",
            (str(image_path),)
        )
        
        # Insert file record
        self.kb_indexer.conn.execute("""
            INSERT INTO files 
            (id, file_path, file_name, file_category, file_type, 
             file_size, line_count, file_hash, last_modified, index_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'indexed')
        """, (
            file_id,
            str(image_path),
            image_path.name,
            category,
            f'image{ext}',
            image_path.stat().st_size,
            len(text.splitlines()),
            current_hash,
            datetime.fromtimestamp(image_path.stat().st_mtime)
        ))
        
        # Split text into sections (by line groups)
        lines = text.split('\n')
        sections = []
        current_section = []
        
        for line in lines:
            if line.strip():
                current_section.append(line)
            else:
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
        if current_section:
            sections.append('\n'.join(current_section))
        
        section_count = 0
        for i, section_content in enumerate(sections):
            if not section_content.strip():
                continue
            
            section_id = str(uuid.uuid4())
            keywords = self._extract_keywords(section_content)
            
            self.kb_indexer.conn.execute("""
                INSERT INTO file_sections 
                (id, file_path, section_level, section_header, parent_section_id,
                 content_preview, content_full, line_start, line_end, 
                 keywords, word_count, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                section_id,
                str(image_path),
                1,
                f"OCR Section {i+1}",
                None,
                (section_content[:200] + '...' if len(section_content) > 200 else section_content).encode('utf-8', 'replace').decode('utf-8'),
                section_content.encode('utf-8', 'replace').decode('utf-8'),
                i * 100 + 1,
                (i + 1) * 100,
                json.dumps(keywords),
                len(section_content.split()),
                current_hash
            ))
            
            for keyword in keywords:
                keyword_id = self.kb_indexer._get_or_create_keyword(keyword)
                if keyword_id:
                    self.kb_indexer.conn.execute("""
                        INSERT OR IGNORE INTO section_keywords 
                        (section_id, keyword_id, weight)
                        VALUES (?, ?, 1.0)
                    """, (section_id, keyword_id))
            
            section_count += 1
        
        self.kb_indexer.conn.commit()
        print(f"  ✅ {image_path.name}: {section_count} OCR sections indexed")
        return section_count


def main():
    if len(sys.argv) < 2:
        print("Usage: python index_pdfs.py <file1> [file2] ...")
        print("  Supports: .pdf (with OCR fallback), .jpg, .png, .gif, .bmp, .webp, .tiff")
        sys.exit(1)
    
    try:
        from kb.base.config import KBConfig
        db_path = KBConfig.get_instance().db_path
    except (ImportError, AttributeError):
        from kb.framework.paths import get_default_db_path
        db_path = get_default_db_path()
    
    with BiblioIndexer(str(db_path)) as indexer:
        pdf_indexer = PDFIndexer(indexer)
        image_indexer = ImageIndexer(indexer)
        
        total_sections = 0
        for path_str in sys.argv[1:]:
            path = Path(path_str).expanduser()
            ext = path.suffix.lower()
            if ext == '.pdf':
                print(f"\n📚 Indexing: {path.name}")
                sections = pdf_indexer.index_pdf(path)
                total_sections += sections
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
                print(f"\n🖼️  Indexing image: {path.name}")
                sections = image_indexer.index_image(path)
                total_sections += sections
            else:
                print(f"  ⚠️  Unsupported file type: {ext}")
    
    print(f"\n✅ Done! Total sections indexed: {total_sections}")


if __name__ == "__main__":
    main()
