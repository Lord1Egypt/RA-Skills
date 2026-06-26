#!/usr/bin/env python3
"""
Template Manager for LaTeX Writer
Manages LaTeX templates for various document types
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Template:
    """LaTeX Template Definition"""
    id: str
    name: str
    description: str
    document_class: str
    style: str  # academic, cv, chinese, etc.
    category: str  # ieee, acm, ctex, moderncv, etc.
    fonts: List[str]
    features: List[str]
    template_path: Path
    sample_tex: Optional[str] = None
    
    def get_cls_path(self) -> Optional[Path]:
        """Get path to .cls file if exists"""
        cls_file = self.template_path / f"{self.document_class}.cls"
        if cls_file.exists():
            return cls_file
        return None


class TemplateManager:
    """Manages LaTeX templates library"""
    
    # Built-in templates configuration
    BUILTIN_TEMPLATES = {
        # Academic templates
        "ieee-trans": {
            "name": "IEEE Transactions",
            "description": "IEEE Transactions journal template",
            "document_class": "IEEEtran",
            "style": "academic",
            "category": "ieee",
            "fonts": ["Times New Roman"],
            "features": ["two_column", "abstract", "keywords", "bibliography", "biography"],
        },
        "ieee-conf": {
            "name": "IEEE Conference",
            "description": "IEEE Conference proceedings template",
            "document_class": "IEEEtran",
            "style": "academic",
            "category": "ieee",
            "fonts": ["Times New Roman"],
            "features": ["two_column", "abstract", "keywords", "bibliography"],
        },
        "acm-sigconf": {
            "name": "ACM SIG Conference",
            "description": "ACM SIG conference proceedings",
            "document_class": "acmart",
            "style": "academic",
            "category": "acm",
            "fonts": ["Linux Libertine", "Linux Biolinum"],
            "features": ["ccs", "keywords", "acm_reference_format", "authors", "orcid"],
        },
        
        # Chinese templates
        "ctex-article": {
            "name": "CTeX Article",
            "description": "Chinese article with CTeX",
            "document_class": "ctexart",
            "style": "chinese_academic",
            "category": "ctex",
            "fonts": ["Source Han Serif CN", "Source Han Sans CN"],
            "features": ["abstract_cn", "keywords_cn", "thanks", "funding"],
        },
        "ctex-report": {
            "name": "CTeX Report",
            "description": "Chinese thesis/report with CTeX",
            "document_class": "ctexrep",
            "style": "chinese_academic",
            "category": "ctex",
            "fonts": ["Source Han Serif CN", "Source Han Sans CN"],
            "features": ["chapter", "abstract_cn", "toc", "bibliography_cn"],
        },
        
        # CV/Resume templates
        "moderncv-classic": {
            "name": "ModernCV Classic",
            "description": "Classic style curriculum vitae",
            "document_class": "moderncv",
            "style": "resume",
            "category": "moderncv",
            "fonts": ["Latin Modern Roman", "Latin Modern Sans"],
            "features": ["photo", "social_links", "cventry", "cvlanguage"],
        },
        "moderncv-banking": {
            "name": "ModernCV Banking",
            "description": "Banking style CV with timeline",
            "document_class": "moderncv",
            "style": "resume",
            "category": "moderncv",
            "fonts": ["Latin Modern Roman"],
            "features": ["timeline", "skillbars", "social_links"],
        },
    }
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize Template Manager"""
        if templates_dir is None:
            # Default to skill's templates directory
            self.templates_dir = Path(__file__).parent.parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)
        
        self._templates_cache: Dict[str, Template] = {}
        self._load_builtin_templates()
    
    def _load_builtin_templates(self):
        """Load built-in template definitions"""
        for template_id, config in self.BUILTIN_TEMPLATES.items():
            template_path = self.templates_dir / config["category"]
            
            template = Template(
                id=template_id,
                name=config["name"],
                description=config["description"],
                document_class=config["document_class"],
                style=config["style"],
                category=config["category"],
                fonts=config["fonts"],
                features=config["features"],
                template_path=template_path,
            )
            
            self._templates_cache[template_id] = template
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """Get template by ID"""
        return self._templates_cache.get(template_id)
    
    def list_templates(
        self,
        style: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Template]:
        """List templates with optional filtering"""
        templates = list(self._templates_cache.values())
        
        if style:
            templates = [t for t in templates if t.style == style]
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        return templates
    
    def match_template(
        self,
        user_input: str,
        document_type: Optional[str] = None
    ) -> List[Tuple[Template, float]]:
        """Match templates based on user input with confidence scores"""
        scores = []
        
        # Keywords mapping for matching
        keyword_map = {
            "ieee": ["ieee", "transactions", "journal"],
            "acm": ["acm", "sigchi", "conference"],
            "ctex": ["中文", "论文", "毕业论文", "ctex"],
            "moderncv": ["简历", "cv", "curriculum", "vitae"],
        }
        
        user_lower = user_input.lower()
        
        for template_id, template in self._templates_cache.items():
            score = 0.0
            
            # 1. 关键词匹配
            keywords = keyword_map.get(template.category, [])
            for keyword in keywords:
                if keyword in user_lower:
                    score += 0.3
            
            # 2. 风格匹配
            if document_type and template.style == document_type:
                score += 0.4
            
            # 3. 名称匹配
            if template.name.lower() in user_lower:
                score += 0.5
            
            if score > 0:
                scores.append((template, score))
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


# Convenience function
def get_template_manager() -> TemplateManager:
    """Get default template manager instance"""
    return TemplateManager()