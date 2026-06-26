#!/usr/bin/env python3
"""
Body Builder - Constructs the document body content
"""

from typing import List, Optional
from latex_generator import DocumentStructure, escape_latex
from template_manager import Template


class BodyBuilder:
    """Build LaTeX document body"""
    
    def __init__(self, template: Template):
        self.template = template
    
    def build(self, document: DocumentStructure) -> str:
        """Generate document body"""
        sections = []
        
        # Title and authors
        sections.append(self.build_title(document))
        
        # Abstract
        if document.abstract:
            sections.append(self.build_abstract(document))
        
        # Main content
        if document.sections:
            for section in document.sections:
                sections.append(self.build_section(section))
        
        # Appendices
        if document.appendices:
            sections.append("\\appendix")
            for appendix in document.appendices:
                sections.append(self.build_section(appendix, is_appendix=True))
        
        # Acknowledgments
        if document.acknowledgments:
            sections.append(self.build_acknowledgments(document))
        
        return "\n\n".join(sections)
    
    def build_title(self, document: DocumentStructure) -> str:
        """Build title section"""
        if self.template.category == "ieee":
            return self._build_ieee_title(document)
        elif self.template.category == "acm":
            return self._build_acm_title(document)
        elif self.template.category == "moderncv":
            return self._build_moderncv_title(document)
        else:
            return self._build_standard_title(document)
    
    def _build_ieee_title(self, document: DocumentStructure) -> str:
        """Build IEEE title format"""
        lines = ["\\IEEEpeerreviewmaketitle"]
        
        # Title
        lines.append(f"\\title{{{escape_latex(document.title)}}}")
        
        # Authors
        if document.authors:
            author_lines = []
            for author in document.authors:
                name = escape_latex(author.get("name", ""))
                affiliation = escape_latex(author.get("affiliation", ""))
                email = escape_latex(author.get("email", ""))
                
                author_lines.append(
                    f"\\IEEEauthorblockN{{{name}}}\\nl"
                    f"\\IEEEauthorblockA{{{affiliation} \\\\n                    {email}}}"
                )
            
            lines.append("\\author{" + "\\and ".join(author_lines) + "}")
        
        return "\n".join(lines)
    
    def _build_acm_title(self, document: DocumentStructure) -> str:
        """Build ACM title format"""
        lines = []
        
        # Title
        lines.append(f"\\title{{{escape_latex(document.title)}}}")
        
        # Subtitle if present
        if document.subtitle:
            lines.append(f"\\subtitle{{{escape_latex(document.subtitle)}}}")
        
        # Authors with ORCID support
        if document.authors:
            for i, author in enumerate(document.authors):
                name = escape_latex(author.get("name", ""))
                affiliation = escape_latex(author.get("affiliation", ""))
                email = escape_latex(author.get("email", ""))
                orcid = author.get("orcid", "")
                
                lines.append(f"\\author{{{name}}}")
                lines.append(f"\\affiliation{{\\institution{{{affiliation}}}}}")
                lines.append(f"\\email{{{email}}}")
                
                if orcid:
                    lines.append(f"\\orcid{{{orcid}}}")
        
        return "\n".join(lines)
    
    def _build_moderncv_title(self, document: DocumentStructure) -> str:
        """Build ModernCV title (personal info header)"""
        lines = []
        
        # Name
        if document.authors:
            name = document.authors[0].get("name", "")
            lines.append(f"\\name{{{name}}}{{}}{{}}{{")
        
        # Title/position
        if document.subtitle:
            lines.append(f"\\title{{{escape_latex(document.subtitle)}}}")
        
        # Contact info
        if document.authors:
            author = document.authors[0]
            
            phone = author.get("phone", "")
            email = author.get("email", "")
            address = author.get("address", "")
            
            if phone:
                lines.append(f"\\phone[mobile]{{{phone}}}")
            if email:
                lines.append(f"\\email{{{email}}}")
            if address:
                lines.append(f"\\address{{{escape_latex(address)}}}")
            
            # Social links
            linkedin = author.get("linkedin", "")
            github = author.get("github", "")
            
            if linkedin:
                lines.append(f"\\social[linkedin]{{{linkedin}}}")
            if github:
                lines.append(f"\\social[github]{{{github}}}")
        
        # Photo (optional)
        # lines.append("\\photo[64pt][0.4pt]{photo.jpg}")
        
        lines.append("\\makecvtitle")
        
        return "\n".join(lines)
    
    def _build_standard_title(self, document: DocumentStructure) -> str:
        """Build standard title page"""
        lines = []
        
        # Title
        lines.append(f"\\title{{{escape_latex(document.title)}}}")
        
        # Authors
        if document.authors:
            author_names = [escape_latex(a.get("name", "")) for a in document.authors]
            lines.append(f"\\author{{{', '.join(author_names)}}}")
        
        # Date
        lines.append(f"\\date{{{datetime.now().strftime('%Y-%m-%d')}}}")
        
        # Make title
        lines.append("\\maketitle")
        
        return "\n".join(lines)
    
    def build_abstract(self, document: DocumentStructure) -> str:
        """Build abstract section"""
        if not document.abstract:
            return ""
        
        abstract_text = escape_latex(document.abstract)
        
        if self.template.category == "ieee":
            # IEEE format with keywords
            keywords = ", ".join(document.keywords) if document.keywords else ""
            return f"""\\begin{{abstract}}
{abstract_text}
\\end{{abstract}}

\\begin{{IEEEkeywords}}
{keywords}
\\end{{IEEEkeywords}}"""
        
        elif self.template.category == "acm":
            # ACM format
            return f"""\\begin{{abstract}}
{abstract_text}
\\end{{abstract}}"""
        
        else:
            # Standard format
            return f"""\\begin{{abstract}}
{abstract_text}
\\end{{abstract}}"""
    
    def build_section(self, section: Dict, is_appendix: bool = False) -> str:
        """Build a document section"""
        title = escape_latex(section.get("title", ""))
        content = section.get("content", "")
        level = section.get("level", 1)
        subsections = section.get("subsections", [])
        
        lines = []
        
        # Section command based on level
        if is_appendix:
            section_cmd = f"\\section{{{title}}}"
        else:
            if level == 1:
                section_cmd = f"\\section{{{title}}}"
            elif level == 2:
                section_cmd = f"\\subsection{{{title}}}"
            elif level == 3:
                section_cmd = f"\\subsubsection{{{title}}}"
            else:
                section_cmd = f"\\paragraph{{{title}}}"
        
        lines.append(section_cmd)
        
        # Add content
        if content:
            escaped_content = escape_latex(content)
            lines.append(escaped_content)
        
        # Add subsections
        for subsection in subsections:
            subsection["level"] = level + 1
            lines.append(self.build_section(subsection))
        
        return "\n\n".join(lines)
    
    def build_acknowledgments(self, document: DocumentStructure) -> str:
        """Build acknowledgments section"""
        if not document.acknowledgments:
            return ""
        
        text = escape_latex(document.acknowledgments)
        
        if self.template.category in ["ieee", "acm"]:
            return f"""\\section*{{Acknowledgments}}
{text}"""
        else:
            return f"""\\section*{{致谢}}
{text}"""


if __name__ == "__main__":
    # Test code
    from template_manager import TemplateManager
    
    manager = TemplateManager()
    template = manager.get_template("ctex-article")
    
    if template:
        # Create sample document
        doc = DocumentStructure(
            title="测试文档",
            authors=[{"name": "张三", "affiliation": "测试大学"}],
            abstract="这是一个测试摘要。",
            keywords=["测试", "LaTeX"],
            sections=[
                {
                    "title": "引言",
                    "content": "这是引言部分的内容。",
                    "level": 1
                }
            ]
        )
        
        generator = LaTeXGenerator(template)
        latex_code = generator.generate(doc)
        
        print("=== Generated LaTeX ===")
        print(latex_code[:2000])
        print("...")
    else:
        print("Template not found")