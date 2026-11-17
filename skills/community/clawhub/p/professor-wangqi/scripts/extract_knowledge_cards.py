"""
PDF解析与知识卡提取脚本

功能：
1. 解析PDF文件，提取文本内容
2. 识别论文结构（标题、摘要、章节等）
3. 按照knowledge-card-schema.md生成知识卡JSON
4. 支持批量处理

依赖：
- PyMuPDF (fitz) 或 pdfplumber: PDF解析（优先fitz，fallback到pdfplumber）
- jieba: 中文分词
- openai: 调用GPT进行信息抽取（可选）

使用：
    python extract_knowledge_cards.py --input data/raw/ --output data/cards/
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from card_cleaner import clean_authors, clean_card, clean_title
from runtime_paths import DEFAULT_OUTPUT_DIR, load_runtime_env


# ============================================================================
# Confidence Scoring System
# ============================================================================

class ConfidenceLevel(Enum):
    """Confidence levels for extracted field values."""
    HIGH = "high"      # 0.85-1.0: LLM extraction or high-confidence rule
    MEDIUM = "medium"  # 0.50-0.84: Rule-based extraction with validation
    LOW = "low"        # 0.25-0.49: Heuristic extraction
    NONE = "none"      # 0.0-0.24: Fallback or missing


@dataclass
class FieldConfidence:
    """
    Confidence information for a single field value.
    
    Attributes:
        value: The extracted value (single value, not a list of candidates)
        confidence: Confidence score (0.0-1.0)
        source: Extraction source ("llm", "metadata", "regex", "heuristic", "fallback", "manual")
        level: Confidence level ("high", "medium", "low", "none") - computed from confidence
        reasoning: Optional explanation of the confidence assessment
        candidates: Top 3 alternative candidates for short fields (title, authors, etc.)
    """
    value: Any
    confidence: float = 0.0
    source: str = "unknown"
    reasoning: str = ""
    candidates: List[Dict[str, Any]] = field(default_factory=list)
    
    # Thresholds for level calculation (same as ConfidenceCalculator)
    HIGH_THRESHOLD = 0.75
    MEDIUM_THRESHOLD = 0.50
    LOW_THRESHOLD = 0.25
    
    def get_level(self) -> str:
        """Convert confidence to level string."""
        if self.confidence >= self.HIGH_THRESHOLD:
            return "high"
        elif self.confidence >= self.MEDIUM_THRESHOLD:
            return "medium"
        elif self.confidence >= self.LOW_THRESHOLD:
            return "low"
        return "none"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "confidence": round(self.confidence, 2),
            "source": self.source,
            "level": self.get_level()
        }
        if self.value is not None:
            result["value"] = self.value
        if self.reasoning:
            result["reasoning"] = self.reasoning
        if self.candidates:
            result["candidates"] = self.candidates
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FieldConfidence":
        """Create from dictionary."""
        return cls(
            value=data.get("value"),
            confidence=data.get("confidence", 0.0),
            source=data.get("source", "unknown"),
            reasoning=data.get("reasoning", ""),
            candidates=data.get("candidates", [])
        )


class ConfidenceCalculator:
    """
    Calculate confidence scores for extracted field values.
    
    Design decisions:
    - Short fields (title, authors, journal, year, doi, keywords): Keep Top 3 candidates
    - Long fields (abstract, conclusions): NO candidates
    - LLM confidence: Fixed 0.85
    - Rule-based confidence: Based on validation heuristics
    """
    
    # Fixed confidence for LLM extraction
    LLM_CONFIDENCE = 0.85
    
    # Confidence thresholds
    HIGH_THRESHOLD = 0.75
    MEDIUM_THRESHOLD = 0.50
    LOW_THRESHOLD = 0.25
    
    # Fields that support candidates (short fields)
    SHORT_FIELDS = {"title", "authors", "journal", "year", "doi", "keywords"}
    
    # Fields that don't support candidates (long fields)
    LONG_FIELDS = {"abstract", "conclusions"}
    
    def __init__(self):
        self.field_data: Dict[str, FieldConfidence] = {}
    
    def calculate_title_confidence(
        self,
        title: str,
        source: str,
        metadata_title: str = "",
        filename: str = ""
    ) -> FieldConfidence:
        """
        Calculate confidence for title extraction.
        
        Sources (in order of preference):
        1. metadata: PDF metadata title
        2. text: Extracted from text
        3. filename: Derived from filename
        4. fallback: Last resort
        """
        candidates = []
        confidence = 0.0
        
        if not title:
            return FieldConfidence(value="", confidence=0.0, source="none")
        
        # Build candidates list
        if metadata_title and metadata_title != title:
            candidates.append({
                "value": metadata_title,
                "confidence": 0.70,
                "source": "metadata"
            })
        
        if filename:
            # Derive title from filename
            file_title = self._derive_title_from_filename(filename)
            if file_title and file_title != title:
                candidates.append({
                    "value": file_title,
                    "confidence": 0.50,
                    "source": "filename"
                })
        
        # Calculate confidence based on source
        if source == "metadata":
            confidence = 0.75
        elif source == "text":
            # Higher confidence if title looks valid
            confidence = self._validate_title(title)
        elif source == "filename":
            confidence = 0.50
        elif source == "fallback":
            confidence = 0.30
        else:
            confidence = 0.40
        
        # Keep only top 3 candidates
        candidates = candidates[:3]
        
        return FieldConfidence(
            value=title,
            confidence=confidence,
            source=source,
            candidates=candidates
        )
    
    def calculate_authors_confidence(
        self,
        authors: List[str],
        source: str,
        metadata_authors: str = ""
    ) -> FieldConfidence:
        """Calculate confidence for authors extraction."""
        candidates = []
        confidence = 0.0
        
        if not authors:
            return FieldConfidence(value=[], confidence=0.0, source="none")
        
        # Build candidates from metadata if available
        if metadata_authors:
            meta_authors = self._parse_authors_string(metadata_authors)
            if meta_authors and meta_authors != authors:
                candidates.append({
                    "value": meta_authors,
                    "confidence": 0.65,
                    "source": "metadata"
                })
        
        # Calculate confidence based on source and validation
        if source == "metadata":
            confidence = 0.70
        elif source == "text":
            confidence = self._validate_authors(authors)
        elif source == "heuristic":
            confidence = 0.45
        else:
            confidence = 0.35
        
        candidates = candidates[:3]
        
        return FieldConfidence(
            value=authors,
            confidence=confidence,
            source=source,
            candidates=candidates
        )
    
    def calculate_year_confidence(
        self,
        year: Optional[int],
        source: str
    ) -> FieldConfidence:
        """Calculate confidence for year extraction."""
        if year is None:
            return FieldConfidence(value=None, confidence=0.0, source="none")
        
        # Validate year range
        if not (1900 <= year <= 2100):
            return FieldConfidence(value=year, confidence=0.20, source=source)
        
        # Confidence based on source
        if source == "metadata":
            confidence = 0.80
        elif source == "text":
            confidence = 0.65
        else:
            confidence = 0.40
        
        return FieldConfidence(value=year, confidence=confidence, source=source)
    
    def calculate_journal_confidence(
        self,
        journal: str,
        source: str
    ) -> FieldConfidence:
        """Calculate confidence for journal extraction."""
        if not journal:
            return FieldConfidence(value="", confidence=0.0, source="none")
        
        # Confidence based on source and validation
        if source == "metadata":
            confidence = 0.70
        elif source == "text":
            # Higher confidence if looks like a journal name
            confidence = self._validate_journal(journal)
        else:
            confidence = 0.40
        
        return FieldConfidence(value=journal, confidence=confidence, source=source)
    
    def calculate_doi_confidence(
        self,
        doi: Optional[str],
        source: str
    ) -> FieldConfidence:
        """Calculate confidence for DOI extraction."""
        if not doi:
            return FieldConfidence(value=None, confidence=0.0, source="none")
        
        # DOI validation
        if not doi.startswith("10."):
            return FieldConfidence(value=doi, confidence=0.30, source=source)
        
        # High confidence for valid DOI
        confidence = 0.90 if source == "text" else 0.75
        
        return FieldConfidence(value=doi, confidence=confidence, source=source)
    
    def calculate_keywords_confidence(
        self,
        keywords: List[str],
        source: str
    ) -> FieldConfidence:
        """Calculate confidence for keywords extraction."""
        if not keywords:
            return FieldConfidence(value=[], confidence=0.0, source="none")
        
        # Confidence based on source and count
        if source == "metadata":
            confidence = 0.75
        elif source == "text":
            # More keywords = higher confidence
            confidence = min(0.70, 0.40 + len(keywords) * 0.05)
        else:
            confidence = 0.35
        
        return FieldConfidence(value=keywords, confidence=confidence, source=source)
    
    def calculate_abstract_confidence(
        self,
        abstract: str,
        source: str,
        is_llm: bool = False
    ) -> FieldConfidence:
        """
        Calculate confidence for abstract extraction.
        Note: Long field, no candidates.
        """
        if not abstract:
            return FieldConfidence(value="", confidence=0.0, source="none")
        
        # LLM extraction gets fixed confidence
        if is_llm:
            confidence = self.LLM_CONFIDENCE
        elif source == "text":
            # Validate abstract quality
            confidence = self._validate_abstract(abstract)
        else:
            confidence = 0.40
        
        return FieldConfidence(value=abstract, confidence=confidence, source=source)
    
    def calculate_conclusions_confidence(
        self,
        conclusions: str,
        source: str,
        is_llm: bool = False
    ) -> FieldConfidence:
        """
        Calculate confidence for conclusions extraction.
        Note: Long field, no candidates.
        """
        if not conclusions:
            return FieldConfidence(value="", confidence=0.0, source="none")
        
        if is_llm:
            confidence = self.LLM_CONFIDENCE
        elif source == "text":
            confidence = self._validate_conclusions(conclusions)
        else:
            confidence = 0.35
        
        return FieldConfidence(value=conclusions, confidence=confidence, source=source)
    
    def get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Convert numeric confidence to ConfidenceLevel."""
        if confidence >= self.HIGH_THRESHOLD:
            return ConfidenceLevel.HIGH
        elif confidence >= self.MEDIUM_THRESHOLD:
            return ConfidenceLevel.MEDIUM
        elif confidence >= self.LOW_THRESHOLD:
            return ConfidenceLevel.LOW
        return ConfidenceLevel.NONE
    
    # ========================================================================
    # Validation helpers
    # ========================================================================
    
    def _validate_title(self, title: str) -> float:
        """Validate title quality and return confidence."""
        if not title:
            return 0.0
        
        confidence = 0.50
        
        # Length check
        if 10 <= len(title) <= 200:
            confidence += 0.10
        
        # Contains meaningful words
        if re.search(r'[a-zA-Z]{3,}', title) or re.search(r'[\u4e00-\u9fff]{2,}', title):
            confidence += 0.10
        
        # Not all caps (usually not a real title)
        if not title.isupper():
            confidence += 0.05
        
        # Contains common title words
        title_words = ["study", "analysis", "research", "review", "treatment", 
                       "研究", "分析", "治疗", "经验", "关系"]
        if any(word in title.lower() for word in title_words):
            confidence += 0.10
        
        return min(confidence, 0.85)
    
    def _validate_authors(self, authors: List[str]) -> float:
        """Validate authors list quality."""
        if not authors:
            return 0.0
        
        confidence = 0.50
        
        # Reasonable count
        if 1 <= len(authors) <= 20:
            confidence += 0.10
        
        # Check for valid name patterns
        valid_names = 0
        for author in authors:
            # Chinese name: 2-4 characters
            if re.fullmatch(r'[\u4e00-\u9fff]{2,4}', author):
                valid_names += 1
            # English name: First Last pattern
            elif re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', author):
                valid_names += 1
        
        if valid_names == len(authors):
            confidence += 0.15
        
        return min(confidence, 0.80)
    
    def _validate_journal(self, journal: str) -> float:
        """Validate journal name quality."""
        if not journal:
            return 0.0
        
        confidence = 0.50
        
        # Contains journal-related words
        journal_words = ["journal", "medicine", "science", "research", "clinical",
                        "杂志", "学报", "期刊"]
        if any(word in journal.lower() for word in journal_words):
            confidence += 0.20
        
        # Reasonable length
        if 5 <= len(journal) <= 100:
            confidence += 0.10
        
        return min(confidence, 0.80)
    
    def _validate_abstract(self, abstract: str) -> float:
        """Validate abstract quality."""
        if not abstract:
            return 0.0
        
        confidence = 0.50
        
        # Length check (abstracts should be substantial)
        if len(abstract) >= 100:
            confidence += 0.10
        if len(abstract) >= 200:
            confidence += 0.10
        
        # Contains structured abstract markers
        markers = ["background", "objective", "methods", "results", "conclusion",
                   "目的", "方法", "结果", "结论"]
        if any(marker in abstract.lower() for marker in markers):
            confidence += 0.15
        
        return min(confidence, 0.85)
    
    def _validate_conclusions(self, conclusions: str) -> float:
        """Validate conclusions quality."""
        if not conclusions:
            return 0.0
        
        confidence = 0.50
        
        # Length check
        if len(conclusions) >= 50:
            confidence += 0.10
        if len(conclusions) >= 100:
            confidence += 0.10
        
        # Contains conclusion markers
        markers = ["suggest", "indicate", "show", "demonstrate", "conclude",
                   "提示", "表明", "说明", "结论"]
        if any(marker in conclusions.lower() for marker in markers):
            confidence += 0.15
        
        return min(confidence, 0.80)
    
    def _derive_title_from_filename(self, filename: str) -> str:
        """Derive a title from filename."""
        if not filename:
            return ""
        
        # Remove extension
        title = filename
        for ext in ['.pdf', '.PDF', '.Pdf']:
            if title.endswith(ext):
                title = title[:-len(ext)]
                break
        
        # Clean up
        title = re.sub(r'^[\d_\-\.]+', '', title)
        title = re.sub(r'[\d_\-\.]+$', '', title)
        title = re.sub(r'_[^_]+$', '', title)
        title = title.replace('_', ' ').replace('-', ' ')
        title = ' '.join(title.split())
        
        return title.strip() if len(title) >= 5 else ""
    
    def _parse_authors_string(self, author_str: str) -> List[str]:
        """Parse author string into list."""
        if not author_str:
            return []
        
        separators = [",", ";", "、", "，"]
        authors = [author_str]
        
        for sep in separators:
            new_authors = []
            for a in authors:
                new_authors.extend(a.split(sep))
            authors = new_authors
        
        return [a.strip() for a in authors if a.strip()]


def generate_review_structure(field_meta: Dict, thresholds: Dict = None) -> Dict:
    """
    Generate _review structure based on field confidence metadata.
    
    Args:
        field_meta: The _field_meta dict with confidence info for each field
        thresholds: Optional custom thresholds per field (default: use standard thresholds)
    
    Returns:
        _review structure matching schema definition
    """
    # Default thresholds by field importance
    DEFAULT_THRESHOLDS = {
        "doi": 0.95,        # critical_identity
        "title": 0.85,      # critical_operational
        "year": 0.85,       # critical_operational
        "authors": 0.80,    # standard
        "journal": 0.80,    # standard
        "keywords": 0.80,   # standard
        "abstract": 0.70,   # descriptive
        "conclusions": 0.70 # descriptive
    }
    
    thresholds = thresholds or DEFAULT_THRESHOLDS
    
    # Find fields needing review
    fields_needing_review = []
    min_confidence = 1.0
    thresholds_used = {}
    
    for field, threshold in thresholds.items():
        # Skip thresholds for fields not present in field_meta
        # This prevents clinical_experience cards from being flagged for paper-specific fields
        if field not in field_meta:
            continue
            
        field_data = field_meta.get(field, {})
        confidence = field_data.get("confidence", 0.0)
        
        # Track minimum confidence
        if confidence > 0:  # Only count non-missing fields
            min_confidence = min(min_confidence, confidence)
        
        # Check if below threshold
        if confidence < threshold:
            fields_needing_review.append(field)
            thresholds_used[field] = threshold
    
    # Determine status
    if not fields_needing_review:
        status = "auto_accepted"
    else:
        status = "needs_review"
    
    # Determine priority
    if min_confidence < 0.50:
        priority = 0  # P0: urgent
    elif min_confidence < 0.80:
        priority = 1  # P1: high
    else:
        priority = 2  # P2: normal
    
    return {
        "status": status,
        "priority": priority,
        "fields": fields_needing_review,
        "thresholds_used": thresholds_used,
        "auto_reviewed_at": datetime.now().isoformat(),
        "manual_reviewed_at": None,
        "reviewer_notes": ""
    }


# 加载.env配置
load_runtime_env()

# 尝试导入PDF解析库（优先PyMuPDF，fallback到pdfplumber）
HAS_PYMUPDF = False
HAS_PDFPLUMBER = False

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    pass

if not HAS_PYMUPDF:
    try:
        import pdfplumber
        HAS_PDFPLUMBER = True
    except ImportError:
        pass

if not HAS_PYMUPDF and not HAS_PDFPLUMBER:
    print("ERROR: Neither PyMuPDF nor pdfplumber is installed.")
    print("Please install one of them:")
    print("  pip install pymupdf")
    print("  pip install pdfplumber")

# 尝试导入中文分词
try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False


def clean_text(text: str) -> str:
    """
    清洗PDF提取的文本
    
    处理：
    - 移除PDF特有的噪声字符
    - 合并被换行打断的句子
    - 规范化空白字符
    """
    if not text:
        return ""
    
    # 移除PDF特有的噪声字符（如  等）
    text = re.sub(r'[\ue000-\uf8ff\U0001f000-\U0001ffff]', '', text)
    
    # 移除控制字符（保留换行和制表符）
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # 合并被单个换行打断的中文字符（常见于PDF）
    text = re.sub(r'([\u4e00-\u9fff])\n([\u4e00-\u9fff])', r'\1\2', text)
    
    # 规范化多个连续空白为单个空格
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 规范化多个连续换行为两个换行（段落分隔）
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 移除行首行尾空白
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()


class PDFParser:
    """PDF文件解析器（支持PyMuPDF和pdfplumber）"""
    
    def __init__(self):
        if not HAS_PYMUPDF and not HAS_PDFPLUMBER:
            raise RuntimeError("Either PyMuPDF or pdfplumber is required for PDF parsing")
        
        self.use_pymupdf = HAS_PYMUPDF
        print(f"PDFParser initialized with {'PyMuPDF' if self.use_pymupdf else 'pdfplumber'}")
    
    def extract_text(self, pdf_path: str) -> Dict:
        """
        提取PDF文本内容
        
        Returns:
            {
                "full_text": "完整文本",
                "pages": [{"page_num": 1, "text": "..."}],
                "metadata": {...}
            }
        """
        if self.use_pymupdf:
            return self._extract_with_pymupdf(pdf_path)
        else:
            return self._extract_with_pdfplumber(pdf_path)
    
    def _extract_with_pymupdf(self, pdf_path: str) -> Dict:
        """使用PyMuPDF提取文本"""
        doc = fitz.open(pdf_path)
        
        pages = []
        full_text = []
        
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            text = clean_text(text)
            pages.append({
                "page_num": page_num,
                "text": text
            })
            full_text.append(text)
        
        metadata = doc.metadata
        
        doc.close()
        
        full_text_str = "\n".join(full_text)
        
        # Check if text is garbled (high ratio of non-printable chars)
        printable_chars = sum(1 for c in full_text_str if c.isprintable() or c.isspace())
        if len(full_text_str) > 100 and printable_chars / len(full_text_str) < 0.7:
            print(f"  Warning: PDF text appears garbled, using metadata for title")
            # Don't try pdfplumber - just use metadata
            # Return the garbled text but keep the metadata (which has the title)
        
        return {
            "full_text": full_text_str,
            "pages": pages,
            "metadata": metadata
        }
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> Dict:
        """使用pdfplumber提取文本"""
        pages = []
        full_text = []
        metadata = {}
        
        with pdfplumber.open(pdf_path) as pdf:
            # 尝试获取元数据
            if pdf.metadata:
                metadata = pdf.metadata
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                text = clean_text(text)
                pages.append({
                    "page_num": page_num,
                    "text": text
                })
                full_text.append(text)
        
        return {
            "full_text": "\n".join(full_text),
            "pages": pages,
            "metadata": metadata
        }
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        识别并提取论文各章节，并过滤参考文献和尾注
        
        改进：
        1. 更准确的章节识别
        2. 处理无明确摘要标题的论文（摘要在标题后第一段）
        3. 过滤参考文献段（避免关键词污染）
        4. 过滤图注、表注
        """
        sections = {}
        
        # 章节标题模式（中英文）
        section_patterns = {
            "abstract": ["Abstract", "ABSTRACT", "摘要", "SUMMARY"],
            "introduction": ["Introduction", "INTRODUCTION", "引言", "前言"],
            "methods": ["Methods", "METHODS", "Materials and Methods", "方法"],
            "results": ["Results", "RESULTS", "结果"],
            "discussion": ["Discussion", "DISCUSSION", "讨论"],
            "conclusion": ["Conclusion", "CONCLUSIONS", "结论", "Concluding remarks"],
        }
        
        # 参考文献开始标记（需要过滤的内容）
        reference_markers = [
            "References", "REFERENCES", "参考文献",
            "Bibliography", "BIBLIOGRAPHY",
            "Supplementary", "SUPPLEMENTARY", "补充材料",
            "Acknowledgements", "ACKNOWLEDGEMENTS", "致谢",
            "Author contributions", "Funding", "Conflicts of interest",
            "Appendix", "APPENDIX", "附录"
        ]
        
        lines = text.split("\n")
        current_section = "other"
        current_content = []
        in_references = False
        found_abstract = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 检查是否进入参考文献区域
            if not in_references:
                for marker in reference_markers:
                    if marker in line_stripped and len(line_stripped) < 50:
                        in_references = True
                        if current_content:
                            sections[current_section] = "\n".join(current_content)
                        break
                
                if in_references:
                    continue
            
            # 检查是否是章节标题
            found_section = None
            for section_key, patterns in section_patterns.items():
                if any(pattern in line_stripped for pattern in patterns):
                    if len(line_stripped) < 60:
                        found_section = section_key
                        if section_key == "abstract":
                            found_abstract = True
                        break
            
            if found_section:
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = found_section
                current_content = []
                in_references = False
            else:
                if not self._is_figure_table_caption(line_stripped):
                    current_content.append(line)
        
        if current_content:
            sections[current_section] = "\n".join(current_content)
        
        # 如果没有找到摘要，尝试从开头提取（处理无明确摘要标题的情况）
        if not found_abstract and "abstract" not in sections:
            # 摘要通常在标题后的第一段，特征是：较长、包含研究目的/方法/结论
            first_paragraphs = []
            for line in lines[:30]:  # 只看前30行
                line = line.strip()
                if line and len(line) > 100:  # 摘要通常较长
                    first_paragraphs.append(line)
                if len(first_paragraphs) >= 1 and len(" ".join(first_paragraphs)) > 500:
                    break
            
            if first_paragraphs:
                potential_abstract = " ".join(first_paragraphs)
                # 检查是否像摘要（包含关键词）
                abstract_keywords = ["aim", "objective", "purpose", "study", "review", "investigate", 
                                   "目的", "方法", "研究", "分析", "评估", "this review", "this study"]
                if any(kw in potential_abstract.lower() for kw in abstract_keywords):
                    sections["abstract"] = potential_abstract
        
        return sections
    
    def _is_figure_table_caption(self, line: str) -> bool:
        """判断是否是图注或表注"""
        caption_patterns = [
            r'^Fig\.?\s*\d+', r'^Figure\.?\s*\d+',
            r'^Table\.?\s*\d+', r'^表\.?\s*\d+',
            r'^图\.?\s*\d+', r'^Tab\.?\s*\d+',
        ]
        for pattern in caption_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        return False


class KnowledgeCardExtractor:
    """知识卡提取器"""
    
    def __init__(self, use_llm: bool = False, api_key: Optional[str] = None,
                 base_url: Optional[str] = None, model_name: Optional[str] = None):
        """
        Args:
            use_llm: 是否使用LLM辅助抽取
            api_key: OpenAI API密钥（如果使用LLM）
            base_url: API基础URL（OpenAI兼容）
            model_name: 模型名称
        """
        self.use_llm = use_llm
        self.api_key = api_key or os.getenv("API_KEY", "")
        self.base_url = base_url or os.getenv("BASE_URL", "http://100.68.117.93:1234/v1")
        self.model_name = model_name or os.getenv("MODEL_NAME", "qwen/qwen3.6-35b-a3b")
        self.client = None
        self.llm_timeout = 30  # 30秒超时
        
        if use_llm and self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
                print(f"LLM client initialized: {self.base_url} with model {self.model_name}")
            except Exception as e:
                print(f"Warning: Failed to initialize LLM client: {e}")
                self.client = None
    
    def _safe_metadata_str(self, value) -> str:
        """Safely extract string from metadata value (could be str, dict, or None)"""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            # Some PDFs have nested metadata
            return value.get("value", "")
        return str(value)

    def _normalize_inline_text(self, text: str) -> str:
        """Normalize inline text for regex extraction."""
        if not text:
            return ""
        text = text.replace("\u00a0", " ").replace("\u200b", "")
        text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\s*\n\s*", "\n", text)
        return text.strip()

    def _get_title_page_text(self, pdf_content: Optional[Dict], max_pages: int = 2) -> str:
        """Return concatenated text from the first few pages."""
        if not pdf_content:
            return ""
        pages = pdf_content.get("pages", []) or []
        selected = [page.get("text", "") for page in pages[:max_pages] if page.get("text")]
        return "\n".join(selected).strip()

    def _split_author_line(self, line: str) -> List[str]:
        """Split a likely author line into candidate author tokens."""
        if not line:
            return []

        normalized = self._normalize_inline_text(line)
        normalized = normalized.replace("†", " ").replace("‡", " ").replace("✉", " ")
        normalized = re.sub(r"\s*&\s*", ", ", normalized)
        if re.search(r"[,，;；、&]|\d", normalized):
            normalized = re.sub(r"\s+and\s+", ", ", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\([^)]*\)", "", normalized)

        parts = re.split(r"[;,，、；]+", normalized)
        cleaned_parts = []
        for part in parts:
            candidate = re.sub(r"[\d\*＊†‡§¶✉]+", "", part).strip()
            candidate = re.sub(r"\b[a-z](?:\s*,\s*[a-z])*$", "", candidate).strip()
            candidate = re.sub(r"\s+", " ", candidate).strip(" .,:;")
            if candidate:
                if re.fullmatch(r"[A-Za-z]", candidate):
                    continue
                cleaned_parts.append(candidate)
        return cleaned_parts

    def _looks_like_name_token(self, token: str) -> bool:
        """Check whether a token looks like a person name."""
        if not token:
            return False

        candidate = re.sub(r"[\d\*＊†‡§¶✉]+", "", token).strip()
        if not candidate:
            return False

        if re.fullmatch(r"[\u4e00-\u9fff]{2,8}", candidate):
            return True

        parts = [part for part in re.split(r"\s+", candidate.replace("-", " ")) if part]
        if not parts or len(parts) > 4:
            return False

        valid_parts = 0
        for part in parts:
            if re.fullmatch(r"[A-Za-z][A-Za-z'.-]{0,30}", part):
                if not (part[0].isupper() or part.isupper()):
                    return False
                valid_parts += 1

        return valid_parts == len(parts) and valid_parts >= 1

    def _is_affiliation_like_line(self, line: str) -> bool:
        """Check whether a line looks like affiliation/contact metadata."""
        if not line:
            return False

        lower = line.lower().strip()
        affiliation_hints = [
            "university", "college", "hospital", "department", "school", "institute",
            "laboratory", "centre", "center", "faculty", "academy", "beijing", "china",
            "email", "e-mail", "correspondence", "received", "accepted", "available online",
            "published online", "copyright", "license", "funded by", "supported by",
            "website", "quick response code", "doi:", "vol.", "www.", "http://", "https://",
            "no. ", "p.r. china",
        ]
        if any(hint in lower for hint in affiliation_hints):
            return True

        if re.search(r"\b\d{5,6}\b", line):
            return True

        if re.search(
            r"^[a-z]\s+(university|college|hospital|school|department|institute|center|centre|faculty|laboratory|division)\b",
            lower,
        ):
            return True

        return False

    def _is_author_like_line(self, line: str) -> bool:
        """Check whether a line is likely to contain author names."""
        if not line or len(line) > 260 or self._is_affiliation_like_line(line):
            return False

        lower = line.lower()
        if line.isupper() and len(line) < 60:
            return False

        if any(marker in lower for marker in ["from cas & cae members", "cas & cae members", "review article", "research article"]):
            return False

        if re.search(r"\b(abstract|摘要|keywords?|key words?|introduction|citation)\b", line, re.IGNORECASE):
            return False

        if not re.search(r"[,，;；、&]", line):
            return False

        tokens = self._split_author_line(line)
        name_like_count = sum(1 for token in tokens if self._looks_like_name_token(token))
        return name_like_count >= 2

    def _normalize_doi(self, doi: str) -> Optional[str]:
        """Normalize DOI string to canonical form."""
        if not doi:
            return None

        cleaned = self._normalize_inline_text(doi)
        cleaned = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^doi\s*[:：]\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.split(
            r"(?i)(published\s*online|available\s*online|received|accepted|copyright|open access)",
            cleaned,
        )[0]
        cleaned = cleaned.strip(" \n\r\t.;,)]}>")
        cleaned = cleaned.replace(" ", "")
        return cleaned if cleaned.lower().startswith("10.") else None

    def _extract_doi(self, metadata: Dict, text: str) -> Optional[str]:
        """Extract DOI from metadata or text."""
        metadata_candidates = [
            self._safe_metadata_str(metadata.get("subject", "")),
            self._safe_metadata_str(metadata.get("keywords", "")),
            self._safe_metadata_str(metadata.get("title", "")),
        ]
        doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)

        for candidate in metadata_candidates:
            if not candidate:
                continue
            normalized = self._normalize_inline_text(candidate)
            match = doi_pattern.search(normalized)
            if match:
                doi = self._normalize_doi(match.group(0))
                if doi:
                    return doi

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for i, line in enumerate(lines[:160]):
            normalized = self._normalize_inline_text(line)
            match = doi_pattern.search(normalized)
            if not match and i + 1 < len(lines) and ("doi" in normalized.lower() or normalized.lower().startswith("10.")):
                joined = normalized + self._normalize_inline_text(lines[i + 1])
                match = doi_pattern.search(joined.replace(" ", ""))
            if match:
                doi = self._normalize_doi(match.group(0))
                if doi:
                    return doi
        return None

    def _split_keywords(self, text: str) -> List[str]:
        """Split keyword text into a normalized keyword list."""
        if not text:
            return []

        normalized = self._normalize_inline_text(text)
        normalized = re.sub(r"^(keywords?|key words?|关键词|关键字)\s*[:：]?\s*", "", normalized, flags=re.IGNORECASE)
        normalized = normalized.replace("•", ";").replace("·", ";")
        parts = re.split(r"[;,；，、]\s*", normalized)

        keywords = []
        seen = set()
        for part in parts:
            candidate = part.strip(" .:;，；、")
            if not candidate:
                continue
            if len(candidate) > 80:
                continue
            key = candidate.lower()
            if key not in seen:
                seen.add(key)
                keywords.append(candidate)
        return keywords

    def _extract_keywords(self, metadata: Dict, text: str) -> List[str]:
        """Extract keywords from metadata or title page."""
        meta_keywords = self._safe_metadata_str(metadata.get("keywords", ""))
        if meta_keywords:
            parsed = self._split_keywords(meta_keywords)
            if parsed:
                return parsed

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for i, line in enumerate(lines[:120]):
            if re.match(r"^(keywords?|key words?|关键词|关键字)\s*[:：]?", line, re.IGNORECASE):
                inline = self._split_keywords(line)
                if inline:
                    return inline
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not re.search(r"\b(abstract|摘要|introduction|citation|doi)\b", next_line, re.IGNORECASE):
                        parsed = self._split_keywords(next_line)
                        if parsed:
                            return parsed

        for i, line in enumerate(lines[:120]):
            if line.count(",") >= 2 and len(line) < 220:
                if any(marker in line.lower() for marker in ["citation", "received", "accepted", "published", "copyright"]):
                    continue
                prev_line = lines[i - 1].lower() if i > 0 else ""
                next_line = lines[i + 1].lower() if i + 1 < len(lines) else ""
                if "abstract" in prev_line or "摘要" in prev_line or "citation" in next_line:
                    parsed = self._split_keywords(line)
                    if len(parsed) >= 3:
                        return parsed

        return []

    def _clean_journal_candidate(self, candidate: str) -> str:
        """Normalize a journal candidate and remove DOI/year noise."""
        if not candidate:
            return ""

        journal = self._normalize_inline_text(candidate)
        journal = re.sub(r"https?://(?:dx\.)?doi\.org/\S+", "", journal, flags=re.IGNORECASE)
        journal = re.sub(r"doi\s*[:：]\s*\S+", "", journal, flags=re.IGNORECASE)
        journal = re.sub(r"^[A-Z][a-z]+\s+et\s+al\.\s+", "", journal, flags=re.IGNORECASE)
        journal = re.sub(r"^\d+\s*", "", journal)
        journal = re.sub(r"\s*\(\d{4}\).*?$", "", journal)
        journal = re.sub(r"\s+\d{4}[;,:].*$", "", journal)
        journal = re.sub(r",\s*Vol\..*$", "", journal, flags=re.IGNORECASE)
        journal = re.sub(r"\s+\d+\(\d+\).*$", "", journal)
        journal = re.sub(r"\s+\d+:\d+.*$", "", journal)
        journal = journal.strip(" .;,:")

        if not journal:
            return ""

        lower = journal.lower()
        words = [word for word in re.split(r"\s+", journal) if word]
        invalid_markers = [
            "background:", "objective:", "methods:", "results:", "conclusion:",
            "received", "accepted", "published", "copyright", "open access",
            "research article", "short communication", "original paper",
            "section of the journal", "permission from the journal", "changed in any way",
        ]
        if any(marker in lower for marker in invalid_markers):
            return ""
        if re.search(r"\([A-Z][A-Za-z-]+,\s*\d{4}\)", journal):
            return ""
        if len(words) > 6:
            return ""

        return journal

    def _extract_journal(self, metadata: Dict, text: str) -> str:
        """Extract journal name from metadata subject or title page."""
        subject = self._safe_metadata_str(metadata.get("subject", ""))
        if subject and not re.search(r"\b(background|objective|methods|results)\s*:", subject, re.IGNORECASE):
            candidate = self._clean_journal_candidate(subject)
            if candidate:
                return candidate

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:80]:
            if "|" in line and "www." in line.lower():
                left = line.split("|", 1)[0].strip()
                candidate = self._clean_journal_candidate(left)
                if candidate:
                    return candidate
            if self._is_affiliation_like_line(line):
                continue
            candidate = ""
            if re.search(r"\(\d{4}\)", line) or re.search(r"\b\d{4};\d", line):
                candidate = self._clean_journal_candidate(line)
            elif len(line) <= 80 and re.search(r"\b(journal|medicine|biochem|discovery|life sci|targeted therapy)\b", line, re.IGNORECASE):
                candidate = self._clean_journal_candidate(line)
            elif line.startswith("The American Journal of"):
                candidate = self._clean_journal_candidate(line)

            if candidate:
                return candidate

        for line in lines[:120]:
            if re.search(r"(doi|https?://doi\.org|\(\d{4}\)|\b\d{4};\d)", line, re.IGNORECASE):
                matches = re.findall(
                    r"([A-Z][A-Za-z.&]*(?:\s+[A-Z][A-Za-z.&]*){0,5}\s(?:Journal|Medicine|Biochem|Discovery|Life Sci|Therapy))",
                    line,
                )
                if matches:
                    candidate = self._clean_journal_candidate(matches[-1])
                    if candidate:
                        return candidate

        doi = self._extract_doi(metadata, text)
        if doi:
            doi_lower = doi.lower()
            doi_journal_map = {
                "j.scib": "Science Bulletin",
            }
            for key, journal in doi_journal_map.items():
                if key in doi_lower:
                    return journal

        return ""

    def _extract_year_from_text(self, text: str) -> Optional[int]:
        """Extract a plausible publication year from the PDF text."""
        if not text:
            return None

        search_window = self._normalize_inline_text(text[:12000])
        date_expr = r"(?:[A-Za-z]+\s+\d{1,2},?\s+|\d{1,2}\s+[A-Za-z]+\s+)"
        patterns = [
            rf"published(?:\s+online)?(?:\s+on)?\s+{date_expr}((?:19|20)\d{{2}})",
            rf"available\s+online\s+{date_expr}((?:19|20)\d{{2}})",
            rf"received\s+{date_expr}((?:19|20)\d{{2}})",
            rf"accepted\s+{date_expr}((?:19|20)\d{{2}})",
            r"©\s*((?:19|20)\d{2})",
            r"\(((?:19|20)\d{2})\)",
            r"\b((?:19|20)\d{2})\s+Science China Press\b",
            r"\b((?:19|20)\d{2})\s+The Chinese Medical Association\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, search_window, re.IGNORECASE)
            if match:
                year = int(match.group(1))
                if 1990 <= year <= 2030:
                    return year

        all_years = [int(year) for year in re.findall(r"\b((?:19|20)\d{2})\b", search_window)]
        plausible = [year for year in all_years if 1990 <= year <= 2030]
        return max(plausible) if plausible else None

    def _extract_block_after_heading(self, text: str, headings: List[str], stop_patterns: List[str], max_lines: int = 30) -> str:
        """Extract a text block after a heading until a stop marker."""
        lines = [line.strip() for line in text.split("\n")]
        for i, line in enumerate(lines):
            normalized = line.strip()
            if not normalized:
                continue
            if normalized.lower() in {heading.lower() for heading in headings}:
                block = []
                for next_line in lines[i + 1:i + 1 + max_lines]:
                    stripped = next_line.strip()
                    if not stripped:
                        if block:
                            block.append("")
                        continue
                    if any(re.match(pattern, stripped, re.IGNORECASE) for pattern in stop_patterns):
                        break
                    block.append(stripped)
                candidate = clean_text("\n".join(block)).strip()
                if len(candidate) >= 80:
                    return candidate
        return ""

    def _extract_abstract(self, sections: Dict[str, str], text: str) -> str:
        """Extract abstract with multiple fallbacks."""
        if sections.get("abstract"):
            abstract = clean_text(sections["abstract"]).strip()
            if len(abstract) >= 80:
                return abstract

        explicit_abstract = self._extract_block_after_heading(
            text,
            headings=["Abstract", "ABSTRACT", "摘要"],
            stop_patterns=[
                r"^(keywords?|key words?|关键词|关键字)\b",
                r"^citation\b",
                r"^(introduction|引言|前言)\b",
                r"^\d+[\.\s]+",
            ],
            max_lines=40,
        )
        if explicit_abstract:
            return explicit_abstract

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for i, line in enumerate(lines[:120]):
            if re.match(r"^(Background|Objective|Aim|Purpose|Methods|Results|Conclusions?)\s*[:：]", line, re.IGNORECASE):
                block = []
                for next_line in lines[i:i + 40]:
                    if re.match(r"^(Citation|Introduction|Keywords?|Key Words?)\b", next_line, re.IGNORECASE):
                        break
                    block.append(next_line)
                candidate = clean_text("\n".join(block)).strip()
                if len(candidate) >= 120:
                    return candidate

        structured_match = re.search(
            r"((?:Background|Objective|Aim|Purpose|Methods|Results|Conclusions?)\s*:[\s\S]{120,2000}?)(?=\n(?:Citation|Introduction|Keywords?|Key Words?)\b|$)",
            text,
            re.IGNORECASE,
        )
        if structured_match:
            return clean_text(structured_match.group(1)).strip()

        stop_markers = {"introduction", "citation", "keywords", "key words", "摘要", "引言"}
        stop_idx = None
        for i, line in enumerate(lines[:150]):
            lower = line.lower()
            if lower in stop_markers or lower.startswith("introduction") or lower.startswith("citation"):
                stop_idx = i
                break

        if stop_idx is not None:
            lead_block = []
            passed_header = False
            for line in lines[:stop_idx]:
                lower = line.lower()
                if re.search(r'https?://|doi[:：]', line, re.IGNORECASE):
                    if lead_block:
                        break
                    continue
                if self._is_author_like_line(line) or self._is_affiliation_like_line(line):
                    passed_header = True
                    if lead_block:
                        break
                    continue
                if re.search(r"(received|accepted|published|available online)", lower):
                    passed_header = True
                    if lead_block:
                        break
                    continue
                if lower.startswith(("signal transduction", "cell discovery", "chinese medicine", "cell phys", "the american journal")):
                    if lead_block:
                        break
                    continue
                if not passed_header:
                    continue
                if len(line) >= 50:
                    lead_block.append(line)
                elif lead_block:
                    break
            if lead_block:
                candidate = clean_text("\n".join(lead_block)).strip()
                if len(candidate) >= 120:
                    return candidate

            block = []
            for line in reversed(lines[:stop_idx]):
                lower = line.lower()
                if self._is_author_like_line(line) or self._is_affiliation_like_line(line):
                    if block:
                        break
                    continue
                if len(line) < 35:
                    if block:
                        break
                    continue
                if lower.startswith(("signal transduction", "cell discovery", "chinese medicine", "cell physiol", "the american journal")):
                    if block:
                        break
                    continue
                block.append(line)
                if len(block) >= 12:
                    break
            if block:
                candidate = clean_text("\n".join(reversed(block))).strip()
                if len(candidate) >= 120:
                    return candidate

        return ""

    def _extract_conclusions(self, sections: Dict[str, str], text: str, abstract: str) -> str:
        """Extract conclusions from section headings or abstract tail."""
        if sections.get("conclusion"):
            conclusions = clean_text(sections["conclusion"]).strip()
            if len(conclusions) >= 40:
                return conclusions

        conclusion_block = self._extract_block_after_heading(
            text,
            headings=["Conclusion", "Conclusions", "结论"],
            stop_patterns=[
                r"^(references|参考文献|acknowledg|funding|supplementary|author contributions)\b",
                r"^\d+[\.\s]+",
            ],
            max_lines=20,
        )
        if conclusion_block:
            return conclusion_block

        structured_match = re.search(r"(Conclusions?\s*:[\s\S]{40,1000})$", abstract, re.IGNORECASE)
        if structured_match:
            return clean_text(structured_match.group(1)).strip()

        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[。！？.!?])\s+", abstract)
            if sentence.strip()
        ]
        for sentence in reversed(sentences):
            if len(sentence) < 40:
                continue
            if re.search(r"\b(suggest\w*|indicat\w*|show\w*|demonstrat\w*|conclud\w*|propos\w*|highlight\w*)\b", sentence, re.IGNORECASE):
                return sentence
            if any(token in sentence for token in ["提示", "表明", "说明", "发现", "提出"]):
                return sentence

        return ""
    
    def extract_from_paper(self, 
                          pdf_content: Dict,
                          source_file: str,
                          card_id: str) -> Dict:
        """
        从SCI论文提取知识卡
        
        Args:
            pdf_content: PDF解析结果
            source_file: 原始文件名
            card_id: 知识卡ID
        
        Returns:
            知识卡JSON
        """
        text = pdf_content["full_text"]
        sections = pdf_content.get("sections", {})
        metadata = pdf_content.get("metadata", {})
        title_page_text = self._get_title_page_text(pdf_content)
        
        # Initialize confidence calculator
        confidence_calc = ConfidenceCalculator()
        
        # Extract fields with source tracking
        extracted_title, title_source = self._extract_title_robust_with_source(text, source_file, metadata)
        extracted_authors, authors_source = self._extract_authors_robust_with_source(text, metadata, extracted_title, source_file)
        extracted_year, year_source = self._extract_year_with_source(metadata, text)
        extracted_journal, journal_source = self._extract_journal_with_source(metadata, title_page_text or text)
        extracted_abstract, abstract_source = self._extract_abstract_with_source(sections, title_page_text or text)
        extracted_conclusions, conclusions_source = self._extract_conclusions_with_source(sections, text, extracted_abstract)
        extracted_keywords, keywords_source = self._extract_keywords_with_source(metadata, title_page_text or text)
        extracted_doi, doi_source = self._extract_doi_with_source(metadata, title_page_text or text)
        
        # Calculate confidence for each field
        title_confidence = confidence_calc.calculate_title_confidence(
            extracted_title, title_source, 
            metadata.get("title", ""), source_file
        )
        authors_confidence = confidence_calc.calculate_authors_confidence(
            extracted_authors, authors_source,
            metadata.get("author", "")
        )
        year_confidence = confidence_calc.calculate_year_confidence(extracted_year, year_source)
        journal_confidence = confidence_calc.calculate_journal_confidence(extracted_journal, journal_source)
        abstract_confidence = confidence_calc.calculate_abstract_confidence(
            extracted_abstract, abstract_source, is_llm=self.use_llm
        )
        conclusions_confidence = confidence_calc.calculate_conclusions_confidence(
            extracted_conclusions, conclusions_source, is_llm=self.use_llm
        )
        keywords_confidence = confidence_calc.calculate_keywords_confidence(extracted_keywords, keywords_source)
        doi_confidence = confidence_calc.calculate_doi_confidence(extracted_doi, doi_source)
        
        # 基础知识卡结构
        card = {
            "card_id": card_id,
            "source_type": "paper",
            "source_file": source_file,
            "title": extracted_title,
            "authors": extracted_authors,
            "year": extracted_year,
            "journal": extracted_journal,
            "language": self._detect_language(text),
            "abstract": extracted_abstract,
            "keywords": extracted_keywords,
            "doi": extracted_doi,
            "research_focus": {
                "constitution_type": [],
                "disease": [],
                "topic": []
            },
            "methods": {},
            "results": {},
            "conclusions": extracted_conclusions,
            "knowledge_points": [],
            "related_constitutions": [],
            "related_diseases": [],
            "evidence_sentences": [],
            "page_info": {
                "total_pages": 0,
                "sections": {}
            },
            "created_at": datetime.now().isoformat(),
            # Confidence tracking
            "_field_meta": {
                "title": title_confidence.to_dict(),
                "authors": authors_confidence.to_dict(),
                "year": year_confidence.to_dict(),
                "journal": journal_confidence.to_dict(),
                "abstract": abstract_confidence.to_dict(),
                "conclusions": conclusions_confidence.to_dict(),
                "keywords": keywords_confidence.to_dict(),
                "doi": doi_confidence.to_dict()
            },
            # Review structure (auto-generated based on confidence)
            "_review": generate_review_structure({
                "title": title_confidence.to_dict(),
                "authors": authors_confidence.to_dict(),
                "year": year_confidence.to_dict(),
                "journal": journal_confidence.to_dict(),
                "abstract": abstract_confidence.to_dict(),
                "conclusions": conclusions_confidence.to_dict(),
                "keywords": keywords_confidence.to_dict(),
                "doi": doi_confidence.to_dict()
            })
        }
        
        # 提取页面信息
        card["page_info"] = self._extract_page_info(pdf_content, sections)
        
        # 如果使用LLM，进行智能抽取
        if self.use_llm:
            card = self._llm_extract(card, text)
        else:
            # 基于规则的抽取
            card = self._rule_based_extract(card, text, pdf_content)

        card, _ = clean_card(card)
        return card
    
    def extract_from_experience(self,
                                pdf_content: Dict,
                                source_file: str,
                                card_id: str) -> Dict:
        """
        从诊疗经验文章提取知识卡
        """
        text = pdf_content["full_text"]
        metadata = pdf_content.get("metadata", {})
        sections = pdf_content.get("sections", {})
        
        # Initialize confidence calculator
        confidence_calc = ConfidenceCalculator()
        
        # Extract fields with source tracking
        extracted_title, title_source = self._extract_title_robust_with_source(text, source_file, metadata)
        extracted_authors, authors_source = self._extract_authors_robust_with_source(
            text, metadata, extracted_title, source_file
        )
        extracted_year, year_source = self._extract_year_with_source(metadata, text)
        
        # Calculate confidence for each field
        title_confidence = confidence_calc.calculate_title_confidence(
            extracted_title, title_source,
            metadata.get("title", ""), source_file
        )
        authors_confidence = confidence_calc.calculate_authors_confidence(
            extracted_authors, authors_source,
            metadata.get("author", "")
        )
        year_confidence = confidence_calc.calculate_year_confidence(extracted_year, year_source)
        
        card = {
            "card_id": card_id,
            "source_type": "clinical_experience",
            "source_file": source_file,
            "title": extracted_title,
            "authors": extracted_authors,
            "year": extracted_year,
            "language": "zh",
            "experience_type": "treatment_method",
            "clinical_focus": {
                "disease": "",
                "syndrome": "",
                "constitution": []
            },
            "diagnostic_approach": {},
            "treatment_approach": {},
            "case_studies": [],
            "clinical_insights": "",
            "knowledge_points": [],
            "related_constitutions": [],
            "related_diseases": [],
            "evidence_sentences": [],
            "research_focus": {  # 添加research_focus字段
                "constitution_type": [],
                "disease": [],
                "topic": []
            },
            "page_info": {
                "total_pages": 0,
                "sections": {}
            },
            "created_at": datetime.now().isoformat(),
            # Confidence tracking
            "_field_meta": {
                "title": title_confidence.to_dict(),
                "authors": authors_confidence.to_dict(),
                "year": year_confidence.to_dict()
            },
            # Review structure (auto-generated based on confidence)
            "_review": generate_review_structure({
                "title": title_confidence.to_dict(),
                "authors": authors_confidence.to_dict(),
                "year": year_confidence.to_dict()
            })
        }
        
        # 提取页面信息
        card["page_info"] = self._extract_page_info(pdf_content, sections)
        
        if self.use_llm:
            card = self._llm_extract_experience(card, text)
        else:
            card = self._rule_based_extract_experience(card, text, pdf_content)

        card, _ = clean_card(card)
        return card
    
    def _parse_authors(self, author_str: str) -> List[str]:
        """解析作者字符串"""
        if not author_str:
            return []
        
        # 常见分隔符
        separators = [",", ";", "、", "，"]
        authors = [author_str]
        
        for sep in separators:
            new_authors = []
            for a in authors:
                new_authors.extend(a.split(sep))
            authors = new_authors
        
        return [a.strip() for a in authors if a.strip()]
    
    def _extract_authors_robust(
        self,
        text: str,
        metadata: Dict,
        title: str = "",
        source_file: str = "",
    ) -> List[str]:
        """
        从文本中提取作者，当元数据不可靠时回退到文本提取
        
        Args:
            text: 文档全文
            metadata: PDF元数据
        
        Returns:
            作者列表
        """
        # 第一步：检查元数据是否有效
        author_str = metadata.get("author", "")
        if author_str:
            parsed_authors = self._parse_authors(author_str)
            # 过滤无效的元数据作者（扩展黑名单）
            invalid_authors = [
                "CNKI", "Unknown", "unknown", "PDF", "Adobe", "",
                "Administrator", "administrator", "admin", "Admin",
                "Author", "author", "USER", "user", "Guest", "guest",
                "System", "system", "Test", "test"
            ]
            valid_authors = [a for a in parsed_authors if a and a not in invalid_authors and len(a) > 1]
            if valid_authors:
                cleaned = clean_authors(valid_authors, title=title, source_file=source_file)
                if cleaned:
                    return cleaned
        
        # 第二步：从文本中提取作者
        return clean_authors(self._extract_authors_from_text(text), title=title, source_file=source_file)
    
    def _extract_authors_from_text(self, text: str) -> List[str]:
        """
        从文本中提取作者
        
        策略：
        1. 查找明确的作者标记
        2. 在标题后、摘要前的区域查找中文名
        3. 过滤误识别的词汇
        """
        # 要过滤的假阳性词汇
        false_positives = {
            "摘要", "关键词", "Abstract", "Keywords", "引言", "Introduction",
            "方法", "Methods", "结果", "Results", "结论", "Conclusion",
            "讨论", "Discussion", "参考文献", "References", "目的", "Objective",
            "研究", "Study", "分析", "Analysis", "评估", "Evaluation",
            "临床", "Clinical", "体质", "Constitution", "中医", "Chinese",
            "王琦教授", "指导", "通信作者", "基金项目", "作者简介",
            "收稿日期", "修回日期", "DOI", "中图分类号", "文献标识码",
        }
        
        # 机构/地址相关词汇（不应被识别为作者）
        institution_words = {
            "University", "College", "Institute", "Hospital", "School",
            "Department", "Center", "Laboratory", "Faculty", "Division",
            "Beijing", "Shanghai", "Guangzhou", "Nanjing", "Chengdu",
            "China", "Chinese", "America", "American", "Europe", "European",
            "National", "Provincial", "Municipal", "Medical", "Health",
            "Science", "Technology", "Medicine", "Pharmacy", "Life",
            "Computer", "Software", "Engineering", "Research", "Development",
            "Access", "article", "online", "this", "Quick", "Response",
            "Code", "Website", "Correspondence", "activation", "exerts",
            "cardioprotection", "through", "transcriptional", "upregulation",
            "heart", "failure", "School", "South",
            # 新增：期刊元数据
            "www", "org", "com", "net", "edu",
            "cmj", "doi", "email", "mail",
        }
        
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        
        # 策略1：查找明确的作者标记
        author_patterns = [
            r'作者[：:]\s*([^\n]+)',
            r'编者[：:]\s*([^\n]+)',
            r'[Aa]uthors?[：:]\s*([^\n]+)',
            r'执笔[：:]\s*([^\n]+)',
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, text[:5000])  # 只搜索前5000字符
            if match:
                authors_str = match.group(1).strip()
                authors = self._parse_authors(authors_str)
                # 清理作者名中的数字和标点（如上标数字表示单位）
                cleaned = []
                for a in authors:
                    # 移除数字和特殊字符
                    a_clean = re.sub(r'[\d\*＊†‡§¶]', '', a).strip()
                    if a_clean and a_clean not in false_positives:
                        cleaned.append(a_clean)
                if cleaned:
                    return cleaned[:15]  # 限制最多15个作者
        
        # 策略2：识别标题后的作者块（更适合英文论文首页）
        for i, line in enumerate(lines[:30]):
            if not self._is_author_like_line(line):
                continue

            author_block = [line]
            for next_line in lines[i + 1:i + 4]:
                if self._is_affiliation_like_line(next_line):
                    break
                if re.search(r"\b(abstract|摘要|keywords?|key words?|citation|introduction|received|accepted)\b", next_line, re.IGNORECASE):
                    break
                if len(next_line) <= 120 and not next_line.endswith("."):
                    author_block.append(next_line)
                else:
                    break

            merged = " ".join(author_block)
            authors = self._split_author_line(merged)
            if authors:
                return authors[:20]

        # 策略3：在标题后、摘要前的区域查找中文姓名
        # 通常作者在标题之后、摘要之前的前20行
        search_lines = lines[:min(20, len(lines))]
        
        # 跳过标题行（通常是第一行或前几行中的长行）
        potential_authors = []
        for i, line in enumerate(search_lines):
            line = line.strip()
            
            # 跳过空行、太长或太短的行
            if not line or len(line) > 100 or len(line) < 3:
                continue
            
            # 跳过包含特定关键词的行
            skip_keywords = ["摘要", "Abstract", "关键词", "Keywords", "DOI", "基金项目", "作者简介",
                           "Website", "Code", "Quick Response", "Correspondence", "E-Mail", "Email",
                           "www.", "http", "Access this article", "Copyright", "©"]
            if any(kw in line for kw in skip_keywords):
                continue
            
            # 跳过纯英文大写行（可能是期刊名等）
            if line.isupper() and line.isalpha():
                continue
            
            # 尝试解析为作者行
            # 中文姓名格式：2-4个汉字，可能用逗号、顿号、空格分隔
            # 也可能带数字上标（单位编号）
            
            # 先移除数字和标点
            line_clean = re.sub(r'[\d\*＊†‡§¶,，、;；\s]+', ' ', line).strip()
            
            # 检查是否是潜在的作者行
            # 中文名字通常由2-4个汉字组成
            # 一行可能包含多个作者，用空格分隔
            
            parts = line_clean.split()
            if parts:
                # 检查每个部分是否像中文姓名
                valid_parts = []
                for part in parts:
                    # 中文名：2-4个汉字
                    if len(part) >= 2 and len(part) <= 4:
                        if all('\u4e00' <= c <= '\u9fff' for c in part):
                            # 过滤常见假阳性
                            if part not in false_positives:
                                valid_parts.append(part)
                if valid_parts and len(valid_parts) >= 1:
                    # 如果找到多个可能的作者名，检查是否在合理位置
                    # 通常作者在标题后几行
                    if i >= 1:  # 不是第一行（标题通常在第一行）
                        potential_authors.extend(valid_parts)
        
        # 去重并限制数量
        seen = set()
        unique_authors = []
        for author in potential_authors:
            author_lower = author.lower()
            if author_lower not in seen:
                seen.add(author_lower)
                unique_authors.append(author)
        
        # 如果找到的作者太多，可能识别错误，只返回前15个
        return unique_authors[:15] if unique_authors else []
    
    def _extract_year(self, metadata: Dict, text: str = "") -> Optional[int]:
        """提取年份"""
        # 尝试从不同字段提取
        for key in ["creationDate", "modDate", "date"]:
            if key in metadata:
                date_str = self._safe_metadata_str(metadata[key])
                if date_str:
                    try:
                        # PDF日期格式: D:YYYYMMDD...
                        if date_str.startswith("D:"):
                            year = int(date_str[2:6])
                            if 1990 <= year <= 2030:
                                return year
                        # 其他格式
                        year_match = re.search(r"\d{4}", date_str)
                        if year_match:
                            year = int(year_match.group())
                            if 1990 <= year <= 2030:
                                return year
                    except:
                        pass

        return self._extract_year_from_text(text)
    
    # ========================================================================
    # Source-tracking extraction methods (for confidence calculation)
    # ========================================================================
    
    def _extract_title_robust_with_source(self, text: str, filename: str, metadata: Dict) -> tuple:
        """Extract title with source tracking. Returns (title, source)."""
        # Check metadata first
        meta_title = self._safe_metadata_str(metadata.get("title", ""))
        is_garbled = self._is_text_garbled(text)
        
        if is_garbled:
            if meta_title and len(meta_title) >= 10:
                return (meta_title, "metadata")
            title = self._extract_title_from_filename(filename)
            if title and len(title) >= 5:
                return (title, "filename")
            return (meta_title if meta_title else "", "fallback")
        
        # Try text extraction
        title = self._extract_title_from_text(text)
        if title and len(title) >= 5:
            if not self._is_text_garbled(title):
                return (clean_title(title, filename), "text")
        
        # Try filename
        title = self._extract_title_from_filename(filename)
        if title and len(title) >= 5:
            return (clean_title(title, filename), "filename")
        
        # Try metadata
        if meta_title and len(meta_title) >= 5:
            return (clean_title(meta_title, filename), "metadata")
        
        # Last resort
        title = self._extract_title(text)
        if title and len(title) >= 5:
            return (clean_title(title, filename), "fallback")
        
        return ("", "none")
    
    def _extract_authors_robust_with_source(self, text: str, metadata: Dict, title: str = "", source_file: str = "") -> tuple:
        """Extract authors with source tracking. Returns (authors, source)."""
        # Check metadata first
        author_str = metadata.get("author", "")
        if author_str:
            parsed_authors = self._parse_authors(author_str)
            invalid_authors = [
                "CNKI", "Unknown", "unknown", "PDF", "Adobe", "",
                "Administrator", "administrator", "admin", "Admin",
                "Author", "author", "USER", "user", "Guest", "guest",
                "System", "system", "Test", "test"
            ]
            valid_authors = [a for a in parsed_authors if a and a not in invalid_authors and len(a) > 1]
            if valid_authors:
                cleaned = clean_authors(valid_authors, title=title, source_file=source_file)
                if cleaned:
                    return (cleaned, "metadata")
        
        # Extract from text
        authors = clean_authors(self._extract_authors_from_text(text), title=title, source_file=source_file)
        if authors:
            return (authors, "text")
        
        return ([], "none")
    
    def _extract_year_with_source(self, metadata: Dict, text: str = "") -> tuple:
        """Extract year with source tracking. Returns (year, source)."""
        # Try metadata
        for key in ["creationDate", "modDate", "date"]:
            if key in metadata:
                date_str = self._safe_metadata_str(metadata[key])
                if date_str:
                    try:
                        if date_str.startswith("D:"):
                            year = int(date_str[2:6])
                            if 1990 <= year <= 2030:
                                return (year, "metadata")
                        year_match = re.search(r"\d{4}", date_str)
                        if year_match:
                            year = int(year_match.group())
                            if 1990 <= year <= 2030:
                                return (year, "metadata")
                    except:
                        pass
        
        # Try text
        year = self._extract_year_from_text(text)
        if year:
            return (year, "text")
        
        return (None, "none")
    
    def _extract_journal_with_source(self, metadata: Dict, text: str) -> tuple:
        """Extract journal with source tracking. Returns (journal, source)."""
        subject = self._safe_metadata_str(metadata.get("subject", ""))
        if subject and not re.search(r"\b(background|objective|methods|results)\s*:", subject, re.IGNORECASE):
            candidate = self._clean_journal_candidate(subject)
            if candidate:
                return (candidate, "metadata")
        
        # Try text extraction
        journal = self._extract_journal({"subject": ""}, text)
        if journal:
            return (journal, "text")
        
        return ("", "none")
    
    def _extract_abstract_with_source(self, sections: Dict[str, str], text: str) -> tuple:
        """Extract abstract with source tracking. Returns (abstract, source)."""
        if sections.get("abstract"):
            abstract = clean_text(sections["abstract"]).strip()
            if len(abstract) >= 80:
                return (abstract, "text")
        
        # Try other methods
        abstract = self._extract_abstract(sections, text)
        if abstract:
            return (abstract, "text")
        
        return ("", "none")
    
    def _extract_conclusions_with_source(self, sections: Dict[str, str], text: str, abstract: str) -> tuple:
        """Extract conclusions with source tracking. Returns (conclusions, source)."""
        if sections.get("conclusion"):
            conclusions = clean_text(sections["conclusion"]).strip()
            if len(conclusions) >= 40:
                return (conclusions, "text")
        
        # Try other methods
        conclusions = self._extract_conclusions(sections, text, abstract)
        if conclusions:
            return (conclusions, "text")
        
        return ("", "none")
    
    def _extract_keywords_with_source(self, metadata: Dict, text: str) -> tuple:
        """Extract keywords with source tracking. Returns (keywords, source)."""
        meta_keywords = self._safe_metadata_str(metadata.get("keywords", ""))
        if meta_keywords:
            parsed = self._split_keywords(meta_keywords)
            if parsed:
                return (parsed, "metadata")
        
        # Try text extraction
        keywords = self._extract_keywords(metadata, text)
        if keywords:
            return (keywords, "text")
        
        return ([], "none")
    
    def _extract_doi_with_source(self, metadata: Dict, text: str) -> tuple:
        """Extract DOI with source tracking. Returns (doi, source)."""
        # Check metadata first
        metadata_candidates = [
            self._safe_metadata_str(metadata.get("subject", "")),
            self._safe_metadata_str(metadata.get("keywords", "")),
            self._safe_metadata_str(metadata.get("title", "")),
        ]
        doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)
        
        for candidate in metadata_candidates:
            if not candidate:
                continue
            normalized = self._normalize_inline_text(candidate)
            match = doi_pattern.search(normalized)
            if match:
                doi = self._normalize_doi(match.group(0))
                if doi:
                    return (doi, "metadata")
        
        # Try text
        doi = self._extract_doi(metadata, text)
        if doi:
            return (doi, "text")
        
        return (None, "none")
    
    def _detect_language(self, text: str) -> str:
        """检测语言"""
        # 简单的中英文检测
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        total_chars = len(text)
        
        if chinese_chars / total_chars > 0.3:
            return "zh"
        return "en"
    
    def _extract_title(self, text: str) -> str:
        """从文本开头提取标题"""
        lines = text.strip().split("\n")
        for line in lines[:5]:  # 检查前5行
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                return line
        return ""
    
    def _extract_page_info(self, pdf_content: Dict, sections: Dict[str, str] = None) -> Dict:
        """
        提取页面信息
        
        Args:
            pdf_content: PDF解析结果，包含pages数组
            sections: 章节内容字典（可选）
        
        Returns:
            {
                "total_pages": int,
                "sections": {section_name: {"start": page_num, "end": page_num}}
            }
        """
        pages = pdf_content.get("pages", [])
        total_pages = len(pages)
        
        page_info = {
            "total_pages": total_pages,
            "sections": {}
        }
        
        if not sections or not pages:
            return page_info
        
        # 章节标题模式（用于匹配页面）
        section_markers = {
            "abstract": ["Abstract", "ABSTRACT", "摘要", "SUMMARY"],
            "introduction": ["Introduction", "INTRODUCTION", "引言", "前言"],
            "methods": ["Methods", "METHODS", "Materials and Methods", "方法"],
            "results": ["Results", "RESULTS", "结果"],
            "discussion": ["Discussion", "DISCUSSION", "讨论"],
            "conclusion": ["Conclusion", "CONCLUSIONS", "结论", "Concluding remarks"],
        }
        
        # 为每个章节查找页码范围
        for section_key, markers in section_markers.items():
            if section_key not in sections or not sections[section_key]:
                continue
            
            section_text = sections[section_key]
            # 取章节文本的前100个字符作为特征
            section_start_text = section_text[:100].strip() if len(section_text) > 100 else section_text.strip()
            
            start_page = None
            end_page = None
            
            for page_data in pages:
                page_num = page_data.get("page_num", 0)
                page_text = page_data.get("text", "")
                
                # 检查章节标题是否在当前页
                for marker in markers:
                    if marker in page_text:
                        if start_page is None:
                            start_page = page_num
                        end_page = page_num
                        break
                
                # 也检查章节内容是否在当前页
                if section_start_text and section_start_text[:50] in page_text:
                    if start_page is None:
                        start_page = page_num
                    if end_page is None or page_num > end_page:
                        end_page = page_num
            
            if start_page is not None:
                page_info["sections"][section_key] = {
                    "start": start_page,
                    "end": end_page if end_page else start_page
                }
        
        return page_info
    
    def _find_page_for_sentence(self, sentence: str, pages: List[Dict]) -> Optional[int]:
        """
        查找句子所在的页码
        
        Args:
            sentence: 要查找的句子
            pages: 页面列表，每项包含page_num和text
        
        Returns:
            页码（1-based），未找到返回None
        """
        if not sentence or not pages:
            return None
        
        # 取句子的前50个字符作为特征（避免换行符问题）
        search_text = sentence[:50].strip() if len(sentence) > 50 else sentence.strip()
        
        for page_data in pages:
            page_text = page_data.get("text", "")
            if search_text in page_text:
                return page_data.get("page_num")
        
        return None
    
    def _extract_title_from_text(self, text: str) -> str:
        """
        从文本中提取标题（改进版）
        
        策略：
        1. 查找前15行中长度适中的非空行
        2. 过滤掉常见的非标题行（如摘要、关键词、期刊元数据等）
        3. 支持多行标题拼接
        """
        if not text:
            return ""
        
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        
        # 非标题行的关键词
        non_title_keywords = [
            "摘要", "abstract", "关键词", "keywords", 
            "引言", "introduction", "前言", "preface",
            "作者", "author", "通讯作者", "corresponding",
            "基金项目", "fund", "收稿日期", "received",
            "中图分类号", "DOI", "doi", "http", "www",
            "版权", "copyright", "©",
            # 新增：期刊元数据关键词
            "website:", "quick response code:", "code:",
            "correspondence", "e-mail", "email",
            "access this article", "scan qr code",
            "published online",
            "commercial purposes",
            "written permission",
            "licensed under",
            "published by",
        ]
        
        # 文章类型标签黑名单（这些不是标题）
        article_type_blacklist = [
            "review article", "original article", "research article",
            "short communication", "case report", "editorial",
            "letter to editor", "commentary", "perspective",
            "access this article online", "quick response code",
            "original research", "brief communication",
            # 新增：页眉/期刊标签
            "from cas & cae members", "cas & cae members",
            "selected by", "recommended by",
            "this article", "download from",
            "journal of", "vol.", "no.", "pp.",
            # 新增：文章类型
            "research paper", "full paper", "extended abstract",
            "position paper", "white paper", "technical report",
            # 新增：期刊元数据
            "quick response code", "website",
        ]
        
        def is_title_candidate(line: str) -> bool:
            line_lower = line.lower()
            if len(line) < 5 or len(line) > 200:
                return False
            if any(kw in line_lower for kw in non_title_keywords):
                return False
            if any(bl in line_lower for bl in article_type_blacklist):
                return False
            if line.isupper() and len(line) < 50:
                return False
            if line.isdigit():
                return False
            if re.match(r'^\[\d+\]', line):
                return False
            if re.search(r'https?://|doi[:：]', line, re.IGNORECASE):
                return False
            if self._is_author_like_line(line) or self._is_affiliation_like_line(line):
                return False
            return True

        def is_noise_line(line: str) -> bool:
            line_lower = line.lower()
            if len(line) < 5 or len(line) > 200:
                return True
            if any(kw in line_lower for kw in non_title_keywords):
                return True
            if any(bl in line_lower for bl in article_type_blacklist):
                return True
            if "et al." in line_lower:
                return True
            if line.isupper() and len(line) < 50:
                return True
            if line.isdigit():
                return True
            if re.match(r'^\[\d+\]', line):
                return True
            if re.search(r'https?://|doi[:：]', line, re.IGNORECASE):
                return True
            if re.search(r"\b\d{4};\d", line) or re.search(r"vol\.\s*\d+", line, re.IGNORECASE):
                return True
            if self._is_affiliation_like_line(line):
                return True
            return False

        title_lines = []
        for i, line in enumerate(lines[:25]):  # 检查前25行
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            if not title_lines and is_noise_line(line):
                continue
            if not title_lines and len(line.split()) < 3 and not re.search(r"[\u4e00-\u9fff]", line):
                continue

            if title_lines:
                if is_noise_line(line):
                    break
                if self._is_author_like_line(line):
                    break
                if len(" ".join(title_lines + [line])) > 260:
                    break
                title_lines.append(line)
                continue

            # 第一个标题行不能是明显的作者行
            if self._is_author_like_line(line) and ("," in line or "&" in line or " and " in line.lower()):
                continue
            title_lines = [line]

            for next_line in lines[i + 1:i + 6]:
                next_line = next_line.strip()
                if not next_line:
                    break
                if is_noise_line(next_line):
                    break
                if self._is_author_like_line(next_line):
                    break
                if len(title_lines) >= 2 and next_line.count(",") >= 1:
                    break
                if re.search(r"\d", next_line) and next_line.count(",") >= 1:
                    break
                if len(" ".join(title_lines + [next_line])) > 260:
                    break
                title_lines.append(next_line)

            return " ".join(title_lines)
        
        return ""
    
    def _extract_title_from_filename(self, filename: str) -> str:
        """
        从文件名中提取标题
        
        示例：
        - "王琦教授治疗肥胖经验.pdf" → "王琦教授治疗肥胖经验"
        - "Wang_Qi_Obesity_Treatment.pdf" → "Wang Qi Obesity Treatment"
        - "痰湿质与代谢综合征研究.pdf" → "痰湿质与代谢综合征研究"
        - "基于数据挖掘分析王琦院士治疗荨麻疹的用药规律_严云.pdf" → "基于数据挖掘分析王琦院士治疗荨麻疹的用药规律"
        """
        if not filename:
            return ""
        
        # 移除扩展名
        title = filename
        for ext in ['.pdf', '.PDF', '.Pdf']:
            if title.endswith(ext):
                title = title[:-len(ext)]
                break
        
        # 清理常见的文件名噪声
        # 移除开头的数字和下划线（如 "01_", "1-" 等）
        title = re.sub(r'^[\d_\-\.]+', '', title)
        
        # 移除结尾的数字和下划线
        title = re.sub(r'[\d_\-\.]+$', '', title)
        
        # 移除作者后缀（如 "_严云", "_李英帅" 等）
        title = re.sub(r'_[^_]+$', '', title)
        
        # 将下划线和连字符替换为空格（英文标题）
        title = title.replace('_', ' ').replace('-', ' ')
        
        # 清理多余空格
        title = ' '.join(title.split())
        
        # 跳过太短的结果
        if len(title) < 5:
            return ""
        
        return title.strip()
    
    def _is_text_garbled(self, text: str) -> bool:
        """Check if text appears to be garbled/encoded incorrectly"""
        if not text or len(text) < 10:
            return False
        
        # Check for garbled characters (black squares, replacement chars, etc.)
        garbled_chars = ['■', '□', '▪', '▫', '�', '\ufffd']
        garbled_count = sum(1 for c in text if c in garbled_chars)
        if garbled_count / len(text) > 0.3:
            return True
        
        # Check for meaningful content
        # Count alphanumeric characters (letters and numbers)
        alnum_count = sum(1 for c in text if c.isalnum())
        
        # If very few alphanumeric chars, likely garbled
        if alnum_count / len(text) < 0.3:
            return True
        
        # Check for excessive special characters
        special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if special_count / len(text) > 0.5:
            return True
        
        # Check for repeated patterns (e.g., all same character)
        unique_chars = len(set(text[:200]))
        if unique_chars < 10 and len(text) > 200:
            return True
        
        return False
    
    def _extract_title_robust(self, text: str, filename: str, metadata: Dict) -> str:
        """
        鲁棒的标题提取方法（带回退链）
        
        回退链：
        1. 检查文本是否为乱码，优先使用元数据
        2. 从文本中提取
        3. 从文件名解析
        4. 从元数据获取
        
        Args:
            text: PDF文本内容
            filename: PDF文件名
            metadata: PDF元数据
        
        Returns:
            提取的标题，如果都失败则返回空字符串
        """
        # 先检查元数据标题（最可靠）
        meta_title = self._safe_metadata_str(metadata.get("title", ""))
        
        # 检查文本是否为乱码
        is_garbled = self._is_text_garbled(text)
        
        if is_garbled:
            # 文本乱码，优先使用元数据
            if meta_title and len(meta_title) >= 10:
                return meta_title
            # 元数据也没有，尝试文件名
            title = self._extract_title_from_filename(filename)
            if title and len(title) >= 5:
                return title
            return meta_title if meta_title else ""
        
        # 1. 尝试从文本提取
        title = self._extract_title_from_text(text)
        if title and len(title) >= 5:
            # 验证标题不是乱码
            if not self._is_text_garbled(title):
                return clean_title(title, filename)
        
        # 2. 尝试从文件名解析
        title = self._extract_title_from_filename(filename)
        if title and len(title) >= 5:
            return clean_title(title, filename)
        
        # 3. 尝试从元数据获取
        if meta_title and len(meta_title) >= 5:
            return clean_title(meta_title, filename)
        
        # 4. 最后尝试原始的文本提取方法
        title = self._extract_title(text)
        if title and len(title) >= 5:
            return clean_title(title, filename)
        
        # 所有方法都失败，返回空字符串
        return ""
    
    def _rule_based_extract(self, card: Dict, text: str, pdf_content: Dict = None) -> Dict:
        """
        基于规则的信息抽取
        
        改进：填充更多字段，确保知识卡有足够内容用于检索
        """
        pages = pdf_content.get("pages", []) if pdf_content else []
        # ===== 1. 体质关键词提取 =====
        constitution_keywords = {
            "平和质": ["平和质", "正常质"],
            "气虚质": ["气虚质", "气虚型", "Qi-deficiency"],
            "阳虚质": ["阳虚质", "阳虚型", "Yang-deficiency"],
            "阴虚质": ["阴虚质", "阴虚型", "Yin-deficiency"],
            "痰湿质": ["痰湿质", "痰湿型", "Phlegm-dampness"],
            "湿热质": ["湿热质", "湿热型", "Damp-heat"],
            "血瘀质": ["血瘀质", "血瘀型", "Blood-stasis"],
            "气郁质": ["气郁质", "气郁型", "Qi-stagnation"],
            "特禀质": ["特禀质", "特禀型", "过敏质", "Special-diathesis"],
        }
        
        for constitution, keywords in constitution_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    if constitution not in card["related_constitutions"]:
                        card["related_constitutions"].append(constitution)
                        # 添加到research_focus
                        if constitution not in card["research_focus"]["constitution_type"]:
                            card["research_focus"]["constitution_type"].append(constitution)
                    break
        
        # ===== 2. 疾病关键词提取（改进：只在正文部分搜索）=====
        # 使用摘要+结论+方法+结果作为正文，排除参考文献污染
        main_text_parts = []
        for section in ["abstract", "introduction", "methods", "results", "discussion", "conclusion"]:
            if card.get(section):
                main_text_parts.append(card[section])
        main_text = "\n".join(main_text_parts)
        
        # 如果正文为空，使用全文（但这是fallback）
        if not main_text:
            main_text = text
        
        disease_keywords = [
            ("肥胖", "obesity"),
            ("过敏性鼻炎", "allergic rhinitis"),
            ("代谢综合征", "metabolic syndrome"),
            ("高血压", "hypertension"),
            ("糖尿病", "diabetes"),
            ("失眠", "insomnia"),
            ("抑郁症", "depression"),
            ("哮喘", "asthma"),
        ]
        
        for disease_cn, disease_en in disease_keywords:
            # 只在正文部分搜索
            if disease_cn in main_text or disease_en.lower() in main_text.lower():
                if disease_cn not in card["related_diseases"]:
                    card["related_diseases"].append(disease_cn)
                    if disease_cn not in card["research_focus"]["disease"]:
                        card["research_focus"]["disease"].append(disease_cn)
        
        # ===== 3. 自动生成知识点 =====
        knowledge_points = []
        
        # 3.1 体质相关知识点
        for constitution in card["related_constitutions"]:
            knowledge_points.append({
                "category": "theory",
                "content": f"本文涉及{constitution}相关研究",
                "importance": "high",
                "evidence_level": "B"
            })
        
        # 3.2 疾病相关知识点
        for disease in card["related_diseases"]:
            knowledge_points.append({
                "category": "diagnosis",
                "content": f"本文研究{disease}与体质的关系",
                "importance": "high",
                "evidence_level": "B"
            })
        
        # 3.3 从结论中提取核心观点
        if card.get("conclusions"):
            # 简单分句
            sentences = re.split(r'[。！？\.\!\?]', card["conclusions"])
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and len(sentence) < 200:
                    # 检查是否包含关键词
                    if any(kw in sentence for kw in ["体质", "表明", "发现", "认为", "建议", "证明"]):
                        knowledge_points.append({
                            "category": "finding",
                            "content": sentence,
                            "importance": "high",
                            "evidence_level": "A"
                        })
                        # 同时添加到证据句
                        page_num = self._find_page_for_sentence(sentence, pages)
                        card["evidence_sentences"].append({
                            "sentence": sentence,
                            "section": "conclusions",
                            "claim_type": "finding",
                            "page_num": page_num
                        })
        
        card["knowledge_points"] = knowledge_points
        
        # ===== 4. 提取方法学信息 =====
        methods = {}
        
        # 样本量
        sample_match = re.search(r'(\d+)\s*(例|名|位|subjects?|participants?|patients?)', text, re.IGNORECASE)
        if sample_match:
            methods["sample_size"] = int(sample_match.group(1))
        
        # 研究设计
        design_keywords = {
            "RCT": ["randomized controlled trial", "随机对照试验", "RCT"],
            "队列研究": ["cohort study", "队列研究"],
            "横断面研究": ["cross-sectional", "横断面", "调查"],
            "Meta分析": ["meta-analysis", "荟萃分析", "Meta分析"],
        }
        for design, keywords in design_keywords.items():
            if any(kw in text for kw in keywords):
                methods["study_design"] = design
                break
        
        card["methods"] = methods
        
        # ===== 5. 提取结果信息 =====
        if card.get("abstract") or card.get("conclusions"):
            # 尝试从摘要/结论中提取主要发现
            source_text = card.get("abstract", "") + " " + card.get("conclusions", "")
            
            # 寻找包含显著性的句子
            sig_match = re.search(r'(P\s*[<>=]\s*0\.\d+|显著|significantly)', source_text, re.IGNORECASE)
            if sig_match:
                card["results"]["has_significance"] = True
        
        # ===== 6. 证据句提取（强制填充）=====
        card["evidence_sentences"] = self._extract_evidence_sentences(card, main_text, pages)
        
        return card
    
    def _extract_evidence_sentences(self, card: Dict, text: str, pages: List[Dict] = None) -> List[Dict]:
        """
        从论文中提取证据句（强制填充）
        
        策略：
        1. 从结论中提取核心发现句
        2. 从摘要中提取目的/方法/结果句
        3. 从结果中提取数据支撑句
        """
        evidence_sentences = []
        
        # 1. 从结论中提取（最重要）
        if card.get("conclusions"):
            conclusion_sentences = self._extract_key_sentences(
                card["conclusions"], 
                keywords=["体质", "表明", "发现", "认为", "证明", "显示", "suggest", "found", "showed", "concluded"],
                section="conclusions",
                max_count=3,
                pages=pages
            )
            evidence_sentences.extend(conclusion_sentences)
        
        # 2. 从摘要中提取
        if card.get("abstract"):
            abstract_sentences = self._extract_key_sentences(
                card["abstract"],
                keywords=["objective", "aim", "method", "result", "conclusion", "目的", "方法", "结果", "结论"],
                section="abstract",
                max_count=2,
                pages=pages
            )
            evidence_sentences.extend(abstract_sentences)
        
        # 3. 从结果中提取数据句
        if card.get("results"):
            # results可能是dict或字符串，确保是字符串
            results_text = card["results"]
            if isinstance(results_text, dict):
                # 如果是dict，尝试提取文本或跳过
                results_text = results_text.get("text", "")
            if results_text and isinstance(results_text, str):
                result_sentences = self._extract_key_sentences(
                    results_text,
                    keywords=["P <", "P<", "显著", "significant", "higher", "lower", "increased", "decreased"],
                    section="results",
                    max_count=2,
                    pages=pages
                )
                evidence_sentences.extend(result_sentences)
        
        # 4. 如果仍然为空，从全文中段提取（跳过标题和参考文献）
        if not evidence_sentences:
            # 使用main_text的中段，避免标题区域和参考文献
            text_mid = text[len(text)//4:len(text)//4*3] if len(text) > 4000 else text[500:2000]
            fallback_sentences = self._extract_key_sentences(
                text_mid,  # 使用中段文本
                keywords=["体质", "constitution", "痰湿", "气虚", "阳虚", "阴虚", "found", "showed", "results"],
                section="main_text",
                max_count=3,
                pages=pages
            )
            evidence_sentences.extend(fallback_sentences)
        
        return evidence_sentences
    
    def _extract_key_sentences(self, text: str, keywords: List[str], section: str, max_count: int = 3, pages: List[Dict] = None) -> List[Dict]:
        """从文本中提取包含关键词的关键句"""
        sentences = []
        
        # 过滤机构/地址/基金相关的内容
        exclude_patterns = [
            r'University|College|Institute|Hospital|School|Department',  # 机构
            r'Beijing|Shanghai|China|Chinese',  # 地址
            r'Grant\s*No|supported\s*by|funded\s*by|No\.\s*\d{4,}',  # 基金
            r'\d{5,6}(,\s*\w+)*$',  # 邮编格式
            r'@|\.edu|\.org|\.com',  # 邮箱/网址
            r'Correspondence|Corresponding\s*author',  # 通讯作者
            r'©|Copyright',  # 版权
        ]
        
        # 分句（中英文）- 不单独按\n分割
        raw_sentences = re.split(r'[。！？\.\!\?]+', text)
        
        for sentence in raw_sentences:
            sentence = sentence.strip()
            
            # 过滤太短或太长的句子
            if len(sentence) < 20 or len(sentence) > 300:
                continue
            
            # 过滤机构/地址/基金句子
            if any(re.search(p, sentence, re.IGNORECASE) for p in exclude_patterns):
                continue
            
            # 过滤纯数字或数字过多的句子
            digit_ratio = sum(c.isdigit() for c in sentence) / len(sentence)
            if digit_ratio > 0.3:
                continue
            
            # 检查是否包含关键词
            for keyword in keywords:
                if keyword.lower() in sentence.lower():
                    # 查找页码
                    page_num = self._find_page_for_sentence(sentence, pages) if pages else None
                    
                    sentences.append({
                        "sentence": sentence,
                        "section": section,
                        "claim_type": "finding" if section in ["conclusions", "results"] else "statement",
                        "page_num": page_num
                    })
                    break
            
            if len(sentences) >= max_count:
                break
        
        return sentences
    
    def _rule_based_extract_experience(self, card: Dict, text: str, pdf_content: Dict = None) -> Dict:
        """
        基于规则的诊疗经验抽取
        
        改进：填充诊疗经验特有字段
        """
        # 复用论文抽取的基础逻辑
        card = self._rule_based_extract(card, text, pdf_content)
        
        # ===== 1. 诊疗经验特有字段 =====
        
        # 1.1 方剂识别
        formula_keywords = [
            "玉屏风散", "六味地黄丸", "金匮肾气丸",
            "二陈汤", "逍遥散", "血府逐瘀汤",
            "过敏煎", "龙胆泻肝汤", "四君子汤",
            "参苓白术散", "归脾汤", "柴胡疏肝散"
        ]
        
        formulas_found = []
        for formula in formula_keywords:
            if formula in text:
                formulas_found.append(formula)
        
        # 1.2 治则治法识别
        principle_keywords = [
            ("益气固表", "气虚质"),
            ("温阳散寒", "阳虚质"),
            ("滋阴清热", "阴虚质"),
            ("健脾化痰", "痰湿质"),
            ("清热利湿", "湿热质"),
            ("活血化瘀", "血瘀质"),
            ("疏肝解郁", "气郁质"),
        ]
        
        principles_found = []
        for principle, constitution in principle_keywords:
            if principle in text:
                principles_found.append(principle)
        
        # 1.3 填充treatment_approach
        card["treatment_approach"] = {
            "main_formula": formulas_found[0] if formulas_found else "",
            "related_formulas": formulas_found,
            "principle": "、".join(principles_found) if principles_found else "",
        }
        
        # 1.4 药物识别
        herb_keywords = [
            "黄芪", "白术", "防风", "人参", "当归",
            "柴胡", "茯苓", "甘草", "陈皮", "半夏",
            "熟地", "山药", "山茱萸", "泽泻", "丹皮"
        ]
        
        herbs_found = [herb for herb in herb_keywords if herb in text]
        if herbs_found:
            card["treatment_approach"]["herbs"] = herbs_found
        
        # ===== 2. 辨证要点提取 =====
        # 寻找包含"辨证"、"证属"等的句子
        pattern = r'[辨证证属].{0,50}[。]'
        matches = re.findall(pattern, text)
        if matches:
            card["diagnostic_approach"] = {
                "key_points": matches[0] if matches else ""
            }
        
        # ===== 3. 临床见解提取 =====
        # 寻找包含"体会"、"经验"、"认为"的段落
        insight_patterns = [
            r'[体会经验认为].{20,200}[。]',
            r'王琦.{0,5}(教授|老师).{0,30}[。]'
        ]
        
        insights = []
        for pattern in insight_patterns:
            matches = re.findall(pattern, text)
            insights.extend(matches)
        
        if insights:
            card["clinical_insights"] = "\n".join(insights[:3])  # 取前3条
        
        # ===== 4. 生成知识点 =====
        knowledge_points = card.get("knowledge_points", [])
        
        # 方剂知识点
        for formula in formulas_found:
            knowledge_points.append({
                "category": "formula",
                "content": f"本文涉及{formula}的应用",
                "importance": "high",
                "evidence_level": "C"
            })
        
        # 治法知识点
        for principle in principles_found:
            knowledge_points.append({
                "category": "treatment",
                "content": f"治法：{principle}",
                "importance": "high",
                "evidence_level": "C"
            })
        
        card["knowledge_points"] = knowledge_points
        
        return card
    
    def _llm_extract_knowledge_points(self, card: Dict, text: str) -> List[Dict]:
        """
        使用LLM提取知识点
        
        从结论和摘要中提取具体的研究发现，而非泛泛描述。
        
        Args:
            card: 当前知识卡（包含abstract, conclusions等字段）
            text: 完整文本
        
        Returns:
            知识点列表 [{"category": "finding", "content": "...", "importance": "high", "evidence_level": "A"}]
        """
        if not self.client:
            return []
        
        # 构建输入文本：优先使用结论和摘要
        input_parts = []
        if card.get("conclusions"):
            input_parts.append(f"【结论】\n{card['conclusions']}")
        if card.get("abstract"):
            input_parts.append(f"【摘要】\n{card['abstract']}")
        
        if not input_parts:
            return []
        
        input_text = "\n\n".join(input_parts)
        
        # 限制输入长度，避免超出上下文限制
        if len(input_text) > 3000:
            input_text = input_text[:3000]
        
        prompt = f"""从以下学术文本中提取3-5个核心知识点。

要求：
1. 每个知识点必须是具体的研究发现或临床经验，而非泛泛描述（如"本文涉及XX相关研究"是不合格的）
2. 包含具体数据、结论或方法学要点
3. 标注类别：
   - finding: 研究发现（包含数据、显著性等）
   - method: 方法学要点（研究设计、样本量等）
   - implication: 临床意义或应用建议
4. importance: high/medium/low
5. evidence_level: A（强证据）/B（中等证据）/C（弱证据/专家意见）

文本：
{input_text}

输出JSON格式（只输出JSON，不要其他文字）：
{{"knowledge_points": [{{"category": "finding", "content": "具体的发现内容", "importance": "high", "evidence_level": "A"}}]}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
                timeout=self.llm_timeout
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # 尝试提取JSON（处理可能的markdown代码块）
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                knowledge_points = result.get("knowledge_points", [])
                
                # 验证并清理知识点
                valid_points = []
                for kp in knowledge_points:
                    if not isinstance(kp, dict):
                        continue
                    content = kp.get("content", "")
                    # 过滤泛泛描述
                    if len(content) < 15:
                        continue
                    if any(generic in content for generic in ["本文涉及", "本文研究", "本文探讨"]):
                        continue
                    valid_points.append({
                        "category": kp.get("category", "finding"),
                        "content": content,
                        "importance": kp.get("importance", "medium"),
                        "evidence_level": kp.get("evidence_level", "B")
                    })
                
                return valid_points
            
        except json.JSONDecodeError as e:
            print(f"  [LLM] JSON parsing error: {e}")
        except Exception as e:
            print(f"  [LLM] Error extracting knowledge points: {e}")
        
        return []
    
    def _llm_extract_experience_points(self, card: Dict, text: str) -> List[Dict]:
        """
        使用LLM提取诊疗经验知识点
        
        从临床经验文章中提取具体的诊疗要点、用药经验、辨证思路等。
        
        Args:
            card: 当前知识卡
            text: 完整文本
        
        Returns:
            知识点列表
        """
        if not self.client:
            return []
        
        # 构建输入文本
        input_text = text[:3000] if len(text) > 3000 else text
        
        prompt = f"""从以下中医诊疗经验文章中提取3-5个核心知识点。

要求：
1. 每个知识点必须是具体的诊疗经验，而非泛泛描述
2. 包含具体的辨证要点、用药经验、治疗思路等
3. 标注类别：
   - diagnosis: 辨证要点、诊断经验
   - treatment: 治疗方法、方药应用
   - insight: 临床心得、经验总结
4. importance: high/medium/low
5. evidence_level: C（专家经验）

文本：
{input_text}

输出JSON格式（只输出JSON，不要其他文字）：
{{"knowledge_points": [{{"category": "treatment", "content": "具体的治疗经验", "importance": "high", "evidence_level": "C"}}]}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
                timeout=self.llm_timeout
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # 尝试提取JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
                knowledge_points = result.get("knowledge_points", [])
                
                # 验证并清理知识点
                valid_points = []
                for kp in knowledge_points:
                    if not isinstance(kp, dict):
                        continue
                    content = kp.get("content", "")
                    if len(content) < 15:
                        continue
                    if any(generic in content for generic in ["本文涉及", "本文介绍"]):
                        continue
                    valid_points.append({
                        "category": kp.get("category", "insight"),
                        "content": content,
                        "importance": kp.get("importance", "medium"),
                        "evidence_level": "C"  # 临床经验默认为C级
                    })
                
                return valid_points
            
        except json.JSONDecodeError as e:
            print(f"  [LLM] JSON parsing error: {e}")
        except Exception as e:
            print(f"  [LLM] Error extracting experience points: {e}")
        
        return []
    
    def _llm_extract(self, card: Dict, text: str) -> Dict:
        """
        使用LLM进行智能抽取（论文类型）
        
        流程：
        1. 先执行规则抽取填充基础字段
        2. 使用LLM提取知识点
        3. 如果LLM失败，保留规则抽取结果
        """
        # 先执行规则抽取
        card = self._rule_based_extract(card, text)
        
        # 如果没有LLM客户端，直接返回
        if not self.client:
            print("  [LLM] No client available, using rule-based extraction")
            return card
        
        print("  [LLM] Extracting knowledge points...")
        
        # 使用LLM提取知识点
        llm_points = self._llm_extract_knowledge_points(card, text)
        
        if llm_points:
            # 替换知识点（LLM结果更具体）
            card["knowledge_points"] = llm_points
            print(f"  [LLM] Extracted {len(llm_points)} knowledge points")
        else:
            # LLM失败，保留规则抽取结果
            print(f"  [LLM] Failed, keeping {len(card.get('knowledge_points', []))} rule-based points")
        
        return card
    
    def _llm_extract_experience(self, card: Dict, text: str) -> Dict:
        """
        使用LLM抽取诊疗经验
        
        流程：
        1. 先执行规则抽取填充基础字段
        2. 使用LLM提取知识点
        3. 如果LLM失败，保留规则抽取结果
        """
        # 先执行规则抽取
        card = self._rule_based_extract_experience(card, text)
        
        # 如果没有LLM客户端，直接返回
        if not self.client:
            print("  [LLM] No client available, using rule-based extraction")
            return card
        
        print("  [LLM] Extracting experience knowledge points...")
        
        # 使用LLM提取知识点
        llm_points = self._llm_extract_experience_points(card, text)
        
        if llm_points:
            # 替换知识点
            card["knowledge_points"] = llm_points
            print(f"  [LLM] Extracted {len(llm_points)} knowledge points")
        else:
            print(f"  [LLM] Failed, keeping {len(card.get('knowledge_points', []))} rule-based points")
        
        return card


def process_pdfs(input_dir: str, 
                output_dir: str,
                source_type: str = "paper",
                use_llm: bool = False,
                api_key: Optional[str] = None):
    """
    批量处理PDF文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        source_type: "paper" 或 "experience"
        use_llm: 是否使用LLM
        api_key: API密钥
    
    Returns:
        dict: {"success": int, "failed": int, "errors": list}
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    parser = PDFParser()
    extractor = KnowledgeCardExtractor(use_llm=use_llm, api_key=api_key)
    
    pdf_files = list(input_path.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    # 跟踪成功和失败
    success_count = 0
    failed_count = 0
    errors = []
    success_files = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"Processing [{i}/{len(pdf_files)}]: {pdf_file.name}")
        
        try:
            # 解析PDF
            pdf_content = parser.extract_text(str(pdf_file))
            pdf_content["sections"] = parser.extract_sections(pdf_content["full_text"])
            
            # 生成知识卡ID
            card_id = f"WQ-{'SCI' if source_type == 'paper' else 'EXP'}-{i:03d}"
            
            # 提取知识卡
            if source_type == "paper":
                card = extractor.extract_from_paper(
                    pdf_content, pdf_file.name, card_id
                )
            else:
                card = extractor.extract_from_experience(
                    pdf_content, pdf_file.name, card_id
                )
            
            # 保存知识卡
            output_file = output_path / f"{card_id}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(card, f, ensure_ascii=False, indent=2)
            
            print(f"  -> Saved: {output_file}")
            success_count += 1
            success_files.append(pdf_file.name)
            
        except Exception as e:
            error_msg = f"{pdf_file.name}: {type(e).__name__}: {e}"
            print(f"  -> Error: {error_msg}")
            import traceback
            traceback.print_exc()
            errors.append(error_msg)
            failed_count += 1
    
    # 打印汇总
    print("\n" + "="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")
    
    if errors:
        print("\nFailed files:")
        for err in errors:
            print(f"  - {err}")
    
    if len(pdf_files) != success_count:
        print(f"\nWARNING: {failed_count} PDF(s) failed to process!")
    
    print("="*50)
    
    return {
        "success": success_count,
        "failed": failed_count,
        "errors": errors,
        "success_files": success_files
    }


def main():
    parser = argparse.ArgumentParser(description="Extract knowledge cards from PDFs")
    parser.add_argument("--input", required=True, help="Input directory")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--type", choices=["paper", "experience"], 
                       default="paper", help="Source type")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM for extraction")
    parser.add_argument("--api-key", help="OpenAI API key")
    
    args = parser.parse_args()
    
    result = process_pdfs(
        input_dir=args.input,
        output_dir=args.output,
        source_type=args.type,
        use_llm=args.use_llm,
        api_key=args.api_key
    )
    
    # Return non-zero exit code if any failures
    if result["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
