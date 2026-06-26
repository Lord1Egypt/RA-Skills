#!/usr/bin/env python3
"""
LaTeX Writer - Main entry point
Intelligent LaTeX document generator with template management
"""

import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Import modules
from template_manager import TemplateManager, Template
from latex_generator import LaTeXGenerator, DocumentStructure
from pdf_builder import PDFBuilder, BuildResult


class LaTeXWriter:
    """Main LaTeX Writer class"""
    
    def __init__(self):
        self.template_manager = TemplateManager()
        self.pdf_builder: Optional[PDFBuilder] = None
    
    def select_template(
        self,
        user_input: str,
        document_type: Optional[str] = None
    ) -> Optional[Template]:
        """Select best matching template based on user input"""
        matches = self.template_manager.match_template(
            user_input,
            document_type
        )
        
        if matches:
            best_match, confidence = matches[0]
            print(f"Selected template: {best_match.name} (confidence: {confidence:.2f})")
            return best_match
        
        return None
    
    def generate_latex(
        self,
        template: Template,
        document: DocumentStructure
    ) -> str:
        """Generate LaTeX source code"""
        generator = LaTeXGenerator(template)
        return generator.generate(document)
    
    def build_pdf(
        self,
        latex_code: str,
        output_name: str = "document"
    ) -> BuildResult:
        """Compile LaTeX to PDF"""
        if self.pdf_builder is None:
            self.pdf_builder = PDFBuilder()
        
        import asyncio
        return asyncio.run(
            self.pdf_builder.build(latex_code, output_name)
        )
    
    def create_document(
        self,
        user_input: str,
        content: Dict[str, Any],
        document_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """End-to-end document creation pipeline"""
        result = {
            "success": False,
            "latex_code": None,
            "pdf_bytes": None,
            "pdf_path": None,
            "template": None,
            "error_message": ""
        }
        
        try:
            # 1. Select template
            template = self.select_template(user_input, document_type)
            if not template:
                result["error_message"] = "No suitable template found"
                return result
            
            result["template"] = template.id
            
            # 2. Build document structure
            document = self._build_document_structure(content)
            
            # 3. Generate LaTeX
            latex_code = self.generate_latex(template, document)
            result["latex_code"] = latex_code
            
            # 4. Build PDF
            build_result = self.build_pdf(latex_code, "document")
            
            if build_result.success:
                result["success"] = True
                result["pdf_bytes"] = build_result.pdf_bytes
                result["pdf_path"] = str(build_result.pdf_path) if build_result.pdf_path else None
            else:
                result["error_message"] = build_result.error_message
        
        except Exception as e:
            result["error_message"] = f"Error: {str(e)}"
        
        return result
    
    def _build_document_structure(self, content: Dict) -> DocumentStructure:
        """Build DocumentStructure from content dict"""
        return DocumentStructure(
            title=content.get("title", ""),
            subtitle=content.get("subtitle", ""),
            authors=content.get("authors", []),
            abstract=content.get("abstract", ""),
            keywords=content.get("keywords", []),
            sections=content.get("sections", []),
            bibliography=content.get("bibliography", []),
            acknowledgments=content.get("acknowledgments", ""),
            appendices=content.get("appendices", [])
        )


def main():
    """Command-line interface for LaTeX Writer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LaTeX Writer - Generate documents")
    parser.add_argument("--template", "-t", help="Template ID")
    parser.add_argument("--output", "-o", default="document.pdf", help="Output PDF path")
    parser.add_argument("--content", "-c", help="Content JSON file")
    
    args = parser.parse_args()
    
    writer = LaTeXWriter()
    
    if args.content:
        # Load content from JSON
        with open(args.content, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # Create document
        result = writer.create_document(
            user_input=content.get("description", ""),
            content=content,
            document_type=content.get("type")
        )
        
        if result["success"]:
            # Save PDF
            with open(args.output, 'wb') as f:
                f.write(result["pdf_bytes"])
            print(f"✓ PDF generated: {args.output}")
            
            # Save LaTeX source
            tex_path = args.output.replace('.pdf', '.tex')
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(result["latex_code"])
            print(f"✓ LaTeX source: {tex_path}")
        else:
            print(f"✗ Error: {result['error_message']}")
    else:
        # Interactive mode or list templates
        print("LaTeX Writer - Available templates:")
        for template in writer.template_manager.list_templates():
            print(f"  - {template.id}: {template.name}")


if __name__ == "__main__":
    main()