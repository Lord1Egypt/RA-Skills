"""
MMOutput - Multi-modal Output Module for PosterGen

Provides conversion from HTML output to various formats:
- PDF: via headless Chrome (print-to-PDF)
- PNG: via headless Chrome (screenshot)
- DOCX: via python-docx

Usage:
    from mm_output import MMOutputGenerator
    
    generator = MMOutputGenerator()
    
    # Convert HTML to PDF
    generator.html_to_pdf("input.html", "output.pdf")
    
    # Convert HTML to PNG
    generator.html_to_png("input.html", "output.png", full_page=True)
    
    # Convert HTML to DOCX
    generator.html_to_docx("input.html", "output.docx")
    
    # Batch convert
    generator.convert_all("input.html", "output_dir/")
"""

from .converter import MMOutputGenerator

__all__ = ["MMOutputGenerator"]
__version__ = "1.0.0"
