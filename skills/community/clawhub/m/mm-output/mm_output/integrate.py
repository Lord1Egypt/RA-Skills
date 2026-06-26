"""
Integration helper for adding MMOutput to PosterGen run.py workflow.

This module provides helper functions to easily integrate multi-modal output
into the existing PosterGen pipeline.

Usage in run.py:
    
    from mm_output.integrate import add_mm_output_args, generate_mm_outputs
    
    # Add arguments to parser
    add_mm_output_args(parser)
    
    # ... after HTML rendering ...
    if html_path:
        generate_mm_outputs(html_path, args.output_dir, args)
"""

import argparse
from pathlib import Path
from typing import Union, Optional


def add_mm_output_args(parser: argparse.ArgumentParser):
    """
    Add multi-modal output arguments to an ArgumentParser.
    
    Args:
        parser: The ArgumentParser instance to add arguments to
    """
    mm_group = parser.add_argument_group("Multi-modal Output Options")
    
    mm_group.add_argument(
        "--output-pdf",
        action="store_true",
        help="Generate PDF output from HTML"
    )
    
    mm_group.add_argument(
        "--output-png",
        action="store_true",
        help="Generate PNG image output from HTML"
    )
    
    mm_group.add_argument(
        "--output-docx",
        action="store_true",
        help="Generate DOCX (Word) output from HTML"
    )

    mm_group.add_argument(
        "--output-pptx",
        action="store_true",
        help="Generate PPTX (PowerPoint) output from HTML"
    )
    
    mm_group.add_argument(
        "--output-all",
        action="store_true",
        help="Generate all supported output formats (PDF, PNG, DOCX, PPTX)"
    )
    
    mm_group.add_argument(
        "--mm-output-dir",
        type=str,
        default=None,
        help="Directory for multi-modal outputs (default: <output_dir>/mm_outputs)"
    )
    
    mm_group.add_argument(
        "--chrome-path",
        type=str,
        default=None,
        help="Path to Chrome/Chromium executable for PDF/PNG generation"
    )
    
    # PDF specific options
    mm_group.add_argument(
        "--pdf-page-size",
        type=str,
        default="A4",
        choices=["A4", "Letter", "Legal", "A3", "A5"],
        help="PDF page size (default: A4)"
    )
    
    mm_group.add_argument(
        "--pdf-landscape",
        action="store_true",
        help="Use landscape orientation for PDF"
    )
    
    # PNG specific options
    mm_group.add_argument(
        "--png-full-page",
        action="store_true",
        default=True,
        help="Capture full page for PNG (default: True)"
    )
    
    mm_group.add_argument(
        "--png-viewport-width",
        type=int,
        default=1200,
        help="Viewport width for PNG capture (default: 1200)"
    )
    
    mm_group.add_argument(
        "--png-viewport-height",
        type=int,
        default=1600,
        help="Viewport height for PNG capture (default: 1600)"
    )


def generate_mm_outputs(
    html_path: Union[str, Path],
    output_dir: Union[str, Path],
    args,
    verbose: bool = True
) -> Optional[dict]:
    """
    Generate multi-modal outputs based on command line arguments.
    
    Args:
        html_path: Path to the input HTML file
        output_dir: Base output directory
        args: Parsed command line arguments
        verbose: Whether to print progress messages
        
    Returns:
        Dictionary mapping format names to output paths, or None if no outputs generated
    """
    # Check if any MM output is requested
    if not (args.output_pdf or args.output_png or args.output_docx or getattr(args, "output_pptx", False) or args.output_all):
        return None
    
    # Determine output directory
    if args.mm_output_dir:
        mm_output_dir = Path(args.mm_output_dir)
    else:
        mm_output_dir = Path(output_dir) / "mm_outputs"
    
    mm_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine formats to generate
    formats = []
    if args.output_all:
        formats = ["pdf", "png", "docx", "pptx"]
    else:
        if args.output_pdf:
            formats.append("pdf")
        if args.output_png:
            formats.append("png")
        if args.output_docx:
            formats.append("docx")
        if getattr(args, "output_pptx", False):
            formats.append("pptx")
    
    if not formats:
        return None
    
    try:
        from .converter import MMOutputGenerator
    except ImportError as e:
        if verbose:
            print(f"[MMOutput] Warning: Cannot import MMOutput module: {e}")
            print("[MMOutput] Please install dependencies: pip install playwright python-docx beautifulsoup4")
        return None
    
    if verbose:
        print(f"\n[MMOutput] Generating multi-modal outputs: {', '.join(formats).upper()}")
        print(f"[MMOutput] Output directory: {mm_output_dir}")
    
    # Prepare format-specific options
    pdf_options = {}
    if hasattr(args, 'pdf_page_size'):
        pdf_options['page_size'] = args.pdf_page_size
    if hasattr(args, 'pdf_landscape'):
        pdf_options['landscape'] = args.pdf_landscape
    
    png_options = {}
    if hasattr(args, 'png_full_page'):
        png_options['full_page'] = args.png_full_page
    if hasattr(args, 'png_viewport_width') and hasattr(args, 'png_viewport_height'):
        png_options['viewport_size'] = (args.png_viewport_width, args.png_viewport_height)
    
    docx_options = {}
    
    # Generate outputs
    results = {}
    
    try:
        with MMOutputGenerator(chrome_path=getattr(args, 'chrome_path', None)) as gen:
            base_name = Path(html_path).stem
            
            for fmt in formats:
                output_path = mm_output_dir / f"{base_name}.{fmt}"
                
                try:
                    if fmt == 'pdf':
                        result = gen.html_to_pdf(html_path, output_path, **pdf_options)
                        results['pdf'] = result
                    elif fmt == 'png':
                        result = gen.html_to_png(html_path, output_path, **png_options)
                        results['png'] = result
                    elif fmt == 'docx':
                        result = gen.html_to_docx(html_path, output_path, **docx_options)
                        results['docx'] = result
                    elif fmt == 'pptx':
                        result = gen.html_to_pptx(html_path, output_path)
                        results['pptx'] = result
                except Exception as e:
                    if verbose:
                        print(f"[MMOutput] Error generating {fmt.upper()}: {e}")
        
        if verbose and results:
            print(f"\n[MMOutput] Generated outputs:")
            for fmt, path in results.items():
                print(f"  - {fmt.upper()}: {path}")
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"[MMOutput] Error during generation: {e}")
        return None


def patch_run_py(run_py_path: Union[str, Path] = None) -> str:
    """
    Generate the code snippet needed to integrate MMOutput into run.py
    
    Args:
        run_py_path: Optional path to run.py for reference
        
    Returns:
        Python code snippet to add to run.py
    """
    code = '''
# === MMOutput Integration ===
# Add these imports at the top of run.py:
from mm_output.integrate import add_mm_output_args, generate_mm_outputs

# Add this after creating the argument parser:
add_mm_output_args(parser)

# Add this after HTML rendering (before the final print):
if html_path:
    generate_mm_outputs(html_path, args.output_dir, args)
# === End MMOutput Integration ===
'''
    return code


def create_example_usage():
    """Create an example script showing how to use the integration."""
    example = '''#!/usr/bin/env python3
"""
Example: Using MMOutput with PosterGen

This example shows how to integrate multi-modal output generation
into your PosterGen workflow.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mm_output import MMOutputGenerator


def example_standalone():
    """Example: Standalone usage after HTML generation"""
    
    # Assuming you have generated HTML files
    html_files = [
        "output/poster_llm.html",
        "output/poster_preview.html"
    ]
    
    output_dir = "output/mm_outputs"
    
    with MMOutputGenerator() as gen:
        for html_path in html_files:
            if Path(html_path).exists():
                print(f"\\nProcessing: {html_path}")
                
                # Convert to all formats
                results = gen.convert_all(
                    html_path,
                    output_dir,
                    base_name=Path(html_path).stem
                )
                
                print("Generated:")
                for fmt, path in results.items():
                    print(f"  - {fmt}: {path}")


def example_specific_format():
    """Example: Generate only specific formats"""
    
    html_path = "output/poster_llm.html"
    output_dir = "output/mm_outputs"
    
    with MMOutputGenerator() as gen:
        # Only PDF and PNG
        results = gen.convert_all(
            html_path,
            output_dir,
            formats=["pdf", "png"]
        )


def example_custom_options():
    """Example: Custom options for each format"""
    
    html_path = "output/poster_llm.html"
    output_dir = "output/mm_outputs"
    
    with MMOutputGenerator() as gen:
        # PDF with landscape orientation
        gen.html_to_pdf(
            html_path,
            f"{output_dir}/poster_landscape.pdf",
            page_size="A4",
            landscape=True
        )
        
        # PNG with custom viewport
        gen.html_to_png(
            html_path,
            f"{output_dir}/poster_screenshot.png",
            viewport_size=(1920, 1080),
            full_page=False
        )
        
        # DOCX without images
        gen.html_to_docx(
            html_path,
            f"{output_dir}/poster_text_only.docx",
            include_images=False
        )


if __name__ == "__main__":
    print("MMOutput Examples")
    print("=================")
    print("\\n1. Standalone usage")
    print("   Run: python examples/mm_output_example.py")
    print("\\n2. Command line")
    print("   Run: python -m mm_output.cli input.html --format all")
    print("\\n3. Integration with run.py")
    print("   See mm_output/integrate.py for integration helper")
'''
    return example


if __name__ == "__main__":
    # Print integration instructions when run directly
    print("MMOutput Integration Helper")
    print("=" * 60)
    print("\nTo integrate MMOutput into run.py, add the following code:\n")
    print(patch_run_py())
    print("\n" + "=" * 60)
    print("\nExample usage script:\n")
    print(create_example_usage())
