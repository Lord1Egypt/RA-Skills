#!/usr/bin/env python3
"""
Content Parser - Parse user input to structured content
"""

import json
import re
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


class ContentParser:
    """Parse various content formats to structured document"""
    
    @staticmethod
    def parse_markdown(md_text: str) -> Dict[str, Any]:
        """
        Parse Markdown text to document structure
        
        Args:
            md_text: Markdown content
        
        Returns:
            Document structure dict
        """
        document = {
            "title": "",
            "sections": [],
            "abstract": "",
            "keywords": []
        }
        
        lines = md_text.split('\n')
        current_section = None
        in_abstract = False
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Title (# Title)
            if line.startswith('# ') and not document["title"]:
                document["title"] = line[2:].strip()
                i += 1
                continue
            
            # Abstract section
            if line.lower() in ["## abstract", "## 摘要"]:
                in_abstract = True
                i += 1
                continue
            
            if in_abstract:
                if line.startswith('## ') or line.startswith('# '):
                    in_abstract = False
                else:
                    document["abstract"] += line + " "
                    i += 1
                    continue
            
            # Keywords
            if line.lower().startswith('keywords:') or line.startswith('关键词：'):
                keywords_text = line.split(':', 1)[1] if ':' in line else line[4:]
                document["keywords"] = [k.strip() for k in keywords_text.split(',')]
                i += 1
                continue
            
            # Section headers
            if line.startswith('## '):
                section_title = line[3:].strip()
                current_section = {
                    "title": section_title,
                    "content": "",
                    "level": 1,
                    "subsections": []
                }
                document["sections"].append(current_section)
                i += 1
                continue
            
            # Subsection headers
            if line.startswith('### '):
                subsection_title = line[4:].strip()
                if current_section:
                    subsection = {
                        "title": subsection_title,
                        "content": "",
                        "level": 2,
                        "subsections": []
                    }
                    current_section["subsections"].append(subsection)
                i += 1
                continue
            
            # Content lines
            if line and current_section:
                current_section["content"] += line + "\n"
            
            i += 1
        
        # Clean up abstract
        document["abstract"] = document["abstract"].strip()
        
        return document
    
    @staticmethod
    def parse_json(json_text: str) -> Dict[str, Any]:
        """Parse JSON content"""
        return json.loads(json_text)
    
    @staticmethod
    def extract_from_text(text: str) -> Dict[str, Any]:
        """
        Extract document structure from plain text
        Uses simple heuristics to identify structure
        """
        document = {
            "title": "",
            "sections": [],
            "abstract": "",
            "keywords": []
        }
        
        lines = text.split('\n')
        
        # Try to find title (first non-empty line or line with specific formatting)
        for line in lines:
            stripped = line.strip()
            if stripped:
                # Check if it looks like a title
                if len(stripped) < 200 and not stripped.endswith('.'):
                    document["title"] = stripped
                    break
        
        # Look for sections (numbered or titled paragraphs)
        current_section = None
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for section headers (e.g., "1. Introduction" or "Introduction")
            if re.match(r'^(\d+\.\s+|Section\s+\d+\s*:|\*{3}|={3,})$', stripped, re.IGNORECASE):
                if current_section:
                    document["sections"].append(current_section)
                
                current_section = {
                    "title": stripped,
                    "content": "",
                    "level": 1,
                    "subsections": []
                }
            elif current_section is not None:
                current_section["content"] += stripped + "\n"
        
        # Add last section
        if current_section:
            document["sections"].append(current_section)
        
        return document


def parse_user_input(user_input: str, input_format: str = "auto") -> Dict[str, Any]:
    """
    Main entry point for parsing user input
    
    Args:
        user_input: Raw user input text
        input_format: Format hint (auto, markdown, json, text)
    
    Returns:
        Parsed document structure
    """
    parser = ContentParser()
    
    if input_format == "markdown" or user_input.strip().startswith('#'):
        return parser.parse_markdown(user_input)
    
    elif input_format == "json" or user_input.strip().startswith('{'):
        return parser.parse_json(user_input)
    
    else:
        # Auto-detect or use plain text extraction
        return parser.extract_from_text(user_input)


if __name__ == "__main__":
    # Test code
    test_md = """
# Test Document

## Abstract
This is a test abstract for the document.

Keywords: test, latex, python

## Introduction
This is the introduction section.

## Methods
We used Python for this test.

### Subsection
More details here.

## Results
The results were positive.

## Conclusion
In conclusion, this works.
"""
    
    parser = ContentParser()
    result = parser.parse_markdown(test_md)
    
    print("Parsed document structure:")
    print(json.dumps(result, indent=2, ensure_ascii=False))