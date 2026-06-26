#!/usr/bin/env python3
"""
LaTeX Code Generator
Generates LaTeX source code from structured content and templates
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from template_manager import Template


@dataclass
class DocumentStructure:
    """Document structure definition"""
    title: str = ""
    subtitle: str = ""
    authors: List[Dict[str, str]] = field(default_factory=list)
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    sections: List[Dict] = field(default_factory=list)
    bibliography: List[Dict] = field(default_factory=list)
    acknowledgments: str = ""
    appendices: List[Dict] = field(default_factory=list)


class LaTeXGenerator:
    """Generate LaTeX code from document structure"""
    
    # LaTeX special characters that need escaping
    LATEX_SPECIAL_CHARS = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    
    def __init__(self, template: Template):
        self.template = template
        self.preamble = PreambleBuilder(template)
        self.body = BodyBuilder(template)
    
    def escape_latex(self, text: str) -> str:
        """Escape LaTeX special characters"""
        result = text
        for char, replacement in self.LATEX_SPECIAL_CHARS.items():
            result = result.replace(char, replacement)
        return result
    
    def generate(self, document: DocumentStructure) -> str:
        """Generate complete LaTeX document"""
        # Build preamble
        preamble = self.preamble.build()
        
        # Build body
        body = self.body.build(document)
        
        # Build bibliography if present
        bibliography = self.build_bibliography(document)
        
        # Assemble complete document
        latex_code = f"""{preamble}

\\begin{{document}}

{body}

{bibliography}

\\end{{document}}
"""
        
        return latex_code
    
    def build_bibliography(self, document: DocumentStructure) -> str:
        """Build bibliography section"""
        if not document.bibliography:
            return ""
        
        if self.template.category in ["ieee", "acm"]:
            # Use .bib file with \bibliography
            return r"""
\bibliographystyle{plain}
\bibliography{references}
"""
        else:
            # Manual bibliography with thebibliography
            entries = []
            for i, bib in enumerate(document.bibliography, 1):
                entry = bib.get("entry", "")
                entries.append(f"\\bibitem{{{i}}} {entry}")
            
            return f"""\\begin{{thebibliography}}{{9}}
{chr(10).join(entries)}
\\end{{thebibliography}}
"""


class PreambleBuilder:
    """Build LaTeX preamble"""
    
    def __init__(self, template: Template):
        self.template = template
    
    def build(self) -> str:
        """Generate complete preamble"""
        components = []
        
        # 1. Document class
        components.append(self.build_documentclass())
        
        # 2. Encoding and language
        components.append(self.build_encoding())
        
        # 3. Geometry and layout
        components.append(self.build_geometry())
        
        # 4. Math support
        components.append(self.build_math_packages())
        
        # 5. Graphics and tables
        components.append(self.build_graphics_packages())
        
        # 6. Colors and links
        components.append(self.build_color_packages())
        
        # 7. Bibliography
        components.append(self.build_bibliography_packages())
        
        # 8. Template-specific configurations
        components.append(self.build_template_specific())
        
        # 9. Custom commands
        components.append(self.build_custom_commands())
        
        return "\n".join(components)
    
    def build_documentclass(self) -> str:
        """Build document class line"""
        doc_class = self.template.document_class
        
        # Default options based on style
        if self.template.style == "chinese_academic":
            options = ["UTF8", "a4paper", "12pt"]
        elif self.template.style == "academic":
            options = ["conference", "letterpaper", "10pt"]
        elif self.template.style == "resume":
            options = ["11pt", "a4paper", "sans"]
        else:
            options = ["a4paper", "12pt"]
        
        return f"\\documentclass[{','.join(options)}]{{{doc_class}}}"
    
    def build_encoding(self) -> str:
        """Build encoding and language packages"""
        packages = []
        
        if self.template.style == "chinese_academic":
            # CTeX handles everything for Chinese
            packages.append("% Chinese support (CTeX)")
            packages.append("\\usepackage{ctex}")
        else:
            # Standard UTF-8 encoding
            packages.append("% Encoding")
            packages.append("\\usepackage[utf8]{inputenc}")
            
            # Language
            if "english" in self.template.features:
                packages.append("\\usepackage[english]{babel}")
            
            # Font encoding
            packages.append("\\usepackage[T1]{fontenc}")
        
        return "\n".join(packages)
    
    def build_geometry(self) -> str:
        """Build page geometry"""
        lines = ["% Page geometry"]
        
        if self.template.category in ["ieee", "acm"]:
            # These templates handle geometry themselves
            pass
        else:
            lines.append("\\usepackage{geometry}")
            lines.append("\\geometry{")
            lines.append("    a4paper,")
            lines.append("    margin=2.5cm,")
            lines.append("    top=2.5cm,")
            lines.append("    bottom=2.5cm")
            lines.append("}")
        
        return "\n".join(lines)
    
    def build_math_packages(self) -> str:
        """Build math support packages"""
        packages = [
            "% Math packages",
            "\\usepackage{amsmath}",
            "\\usepackage{amssymb}",
            "\\usepackage{amsthm}",
        ]
        
        # Additional math packages
        packages.append("\\usepackage{mathtools}")
        
        # Theorem environments for academic papers
        if self.template.style == "academic":
            packages.extend([
                "\\theoremstyle{definition}",
                "\\newtheorem{definition}{Definition}[section]",
                "\\newtheorem{theorem}{Theorem}[section]",
                "\\newtheorem{lemma}{Lemma}[section]",
                "\\newtheorem{corollary}{Corollary}[section]",
            ])
        
        return "\n".join(packages)
    
    def build_graphics_packages(self) -> str:
        """Build graphics and table packages"""
        packages = [
            "% Graphics and tables",
            "\\usepackage{graphicx}",
            "\\usepackage{booktabs}",
            "\\usepackage{array}",
            "\\usepackage{multirow}",
            "\\usepackage{tabularx}",
        ]
        
        # Float control
        packages.extend([
            "\\usepackage{float}",
            "\\usepackage{caption}",
            "\\usepackage{subcaption}",
        ])
        
        # Code listings for technical papers
        if "code" in self.template.features:
            packages.extend([
                "\\usepackage{listings}",
                "\\usepackage{xcolor}",
                "\\lstset{",
                "    basicstyle=\\small\\ttfamily,",
                "    breaklines=true,",
                "    frame=single",
                "}",
            ])
        
        return "\n".join(packages)
    
    def build_color_packages(self) -> str:
        """Build color and hyperlink packages"""
        packages = [
            "% Colors and links",
            "\\usepackage{xcolor}",
            "\\usepackage{hyperref}",
        ]
        
        # Hyperref setup
        packages.append("\\hypersetup{")
        
        if self.template.style == "academic":
            # Academic papers: colored links
            packages.extend([
                "    colorlinks=true,",
                "    linkcolor=blue,",
                "    filecolor=magenta,", 
                "    urlcolor=cyan,",
                "    citecolor=blue,",
            ])
        else:
            # Other docs: black links for printing
            packages.extend([
                "    colorlinks=false,",
                "    linkcolor=black,",
                "    citecolor=black,",
                "    urlcolor=black,",
            ])
        
        packages.append("}")
        
        return "\n".join(packages)
    
    def build_bibliography_packages(self) -> str:
        """Build bibliography packages"""
        if self.template.category in ["ieee", "acm"]:
            # These templates handle bibliography themselves
            return "% Bibliography handled by template"
        
        packages = [
            "% Bibliography",
        ]
        
        # Use natbib for author-year citations
        packages.extend([
            "\\usepackage[numbers]{natbib}",
            "\\bibliographystyle{plainnat}",
        ])
        
        return "\n".join(packages)
    
    def build_template_specific(self) -> str:
        """Build template-specific configurations"""
        lines = ["% Template-specific configurations"]
        
        if self.template.category == "ieee":
            lines.extend([
                "% IEEE-specific settings",
                "\\IEEEoverridecommandlockouts",
            ])
        elif self.template.category == "acm":
            lines.extend([
                "% ACM-specific settings",
                "\\setcopyright{acmcopyright}",
                "\\acmConference[Conference'25]{Conference Name}{Month Day, Year}{City, Country}",
            ])
        elif self.template.category == "moderncv":
            lines.extend([
                "% ModernCV settings",
                "\\moderncvstyle{banking}",
                "\\moderncvcolor{blue}",
            ])
        
        return "\n".join(lines)
    
    def build_custom_commands(self) -> str:
        """Build custom LaTeX commands"""
        commands = [
            "% Custom commands",
            "% Math shortcuts",
            "\\newcommand{\\vect}[1]{\\boldsymbol{#1}}",
            "\\newcommand{\\mat}[1]{\\mathbf{#1}}",
            "\\newcommand{\\norm}[1]{\\left\\|#1\\right\\|}",
            "\\newcommand{\\E}{\\mathbb{E}}",
            "\\newcommand{\\R}{\\mathbb{R}}",
            "",
            "% Utility commands",
            "\\newcommand{\\todo}[1]{\\textcolor{red}{\\textbf{TODO:} #1}}",
            "\\newcommand{\\note}[1]{\\textcolor{blue}{\\textbf{Note:} #1}}",
        ]
        
        return "\n".join(commands)


# Utility functions

def escape_latex(text: str) -> str:
    """Escape LaTeX special characters"""
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    
    # Sort by length (descending) to avoid partial replacements
    for char in sorted(special_chars.keys(), key=len, reverse=True):
        text = text.replace(char, special_chars[char])
    
    return text


if __name__ == "__main__":
    # Test code
    from template_manager import TemplateManager
    
    manager = TemplateManager()
    template = manager.get_template("ieee-trans")
    
    if template:
        generator = LaTeXGenerator(template)
        preamble = generator.preamble.build()
        print("=== Preamble ===")
        print(preamble[:1000])
        print("...")
    else:
        print("Template not found")