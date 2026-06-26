#!/usr/bin/env python3
"""
Metadata extractor - Extract metadata from documents.
"""

import datetime
import zipfile
from pathlib import Path
from typing import Dict, Optional


def extract_docx_metadata(docx_path: str) -> Dict:
    """Extract metadata from DOCX file."""
    metadata = {
        'file': Path(docx_path).name,
        'size': Path(docx_path).stat().st_size,
    }
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            if 'docProps/core.xml' in z.namelist():
                import xml.etree.ElementTree as ET
                content = z.read('docProps/core.xml')
                root = ET.fromstring(content)
                
                ns = {'dc': 'http://purl.org/dc/elements/1.1/',
                      'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
                
                fields = {
                    '{dc}title': 'title',
                    '{dc}creator': 'author',
                    '{dc}subject': 'subject',
                    '{dc}description': 'description',
                    '{cp}lastModifiedBy': 'last_modified_by',
                    '{cp}revision': 'revision',
                }
                
                for xml_tag, meta_key in fields.items():
                    elem = root.find(xml_tag, ns)
                    if elem is not None and elem.text:
                        metadata[meta_key] = elem.text
                
                for xml_tag in ['{dc}created', '{cp}modified']:
                    elem = root.find(xml_tag, ns)
                    if elem is not None and elem.text:
                        try:
                            dt = datetime.fromisoformat(elem.text.replace('Z', '+00:00'))
                            metadata['created' if 'created' in xml_tag else 'modified'] = dt.isoformat()
                        except Exception:
                            pass
            
            metadata['pages'] = sum(1 for n in z.namelist() if n.startswith('word/page'))
            metadata['images'] = sum(1 for n in z.namelist() if n.startswith('word/media/'))
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata


def extract_pdf_metadata(pdf_path: str) -> Dict:
    """Extract metadata from PDF file."""
    metadata = {
        'file': Path(pdf_path).name,
        'size': Path(pdf_path).stat().st_size,
    }
    
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            if reader.metadata:
                metadata['title'] = reader.metadata.get('/Title', '')
                metadata['author'] = reader.metadata.get('/Author', '')
                metadata['subject'] = reader.metadata.get('/Subject', '')
                metadata['creator'] = reader.metadata.get('/Creator', '')
                metadata['producer'] = reader.metadata.get('/Producer', '')
            
            metadata['pages'] = len(reader.pages)
            metadata['encrypted'] = reader.is_encrypted
    except ImportError:
        metadata['error'] = 'PyPDF2 not installed'
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata


def extract_xlsx_metadata(xlsx_path: str) -> Dict:
    """Extract metadata from XLSX file."""
    metadata = {
        'file': Path(xlsx_path).name,
        'size': Path(xlsx_path).stat().st_size,
    }
    
    try:
        with zipfile.ZipFile(xlsx_path, 'r') as z:
            if 'docProps/core.xml' in z.namelist():
                import xml.etree.ElementTree as ET
                content = z.read('docProps/core.xml')
                root = ET.fromstring(content)
                
                ns = {'dc': 'http://purl.org/dc/elements/1.1/',
                      'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
                
                fields = ['{dc}title', '{dc}creator', '{dc}description']
                for tag in fields:
                    elem = root.find(tag, ns)
                    if elem is not None and elem.text:
                        metadata[tag.split('}')[1]] = elem.text
            
            metadata['sheets'] = sum(1 for n in z.namelist() if n.startswith('xl/worksheets/'))
            metadata['images'] = sum(1 for n in z.namelist() if n.startswith('xl/media/'))
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata


def extract_metadata(file_path: str) -> Dict:
    """Extract metadata from any supported document."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext in ['.docx']:
        return extract_docx_metadata(file_path)
    elif ext in ['.pdf']:
        return extract_pdf_metadata(file_path)
    elif ext in ['.xlsx', '.xls']:
        return extract_xlsx_metadata(file_path)
    else:
        return {'file': path.name, 'size': path.stat().st_size, 'type': 'unsupported'}


if __name__ == "__main__":
    import argparse, json
    
    parser = argparse.ArgumentParser(description="Extract document metadata")
    parser.add_argument("file", help="Document file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    metadata = extract_metadata(args.file)
    
    if args.json:
        print(json.dumps(metadata, indent=2))
    else:
        for k, v in metadata.items():
            print(f"{k}: {v}")