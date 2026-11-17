#!/usr/bin/env python3
"""
Visual verification: PPTX → PDF → JPEG for slide-by-slide quality review.

Usage:
    python visual_verify.py <input.pptx> [--output-dir <dir>] [--dpi 150]

Requires: LibreOffice (soffice), poppler-utils (pdftoppm)
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def pptx_to_images(pptx_path: str, output_dir: str = None, dpi: int = 150) -> list:
    """Convert PPTX to individual JPEG images via PDF intermediate.
    
    Returns list of generated image paths.
    """
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        print(f"Error: {pptx_path} not found", file=sys.stderr)
        sys.exit(1)

    if output_dir is None:
        output_dir = pptx_path.parent / "visual_review"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: PPTX → PDF via LibreOffice
    pdf_path = output_dir / f"{pptx_path.stem}.pdf"
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "soffice", "--headless", "--convert-to", "pdf",
            "--outdir", tmpdir, str(pptx_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"LibreOffice conversion failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        
        tmp_pdf = Path(tmpdir) / f"{pptx_path.stem}.pdf"
        if tmp_pdf.exists():
            import shutil
            shutil.move(str(tmp_pdf), str(pdf_path))
        else:
            print(f"PDF not generated in {tmpdir}", file=sys.stderr)
            sys.exit(1)

    # Step 2: PDF → JPEG via pdftoppm
    prefix = output_dir / "slide"
    cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf_path), str(prefix)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"pdftoppm failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Collect generated images
    images = sorted(output_dir.glob("slide-*.jpg"))
    print(f"Generated {len(images)} slide images in {output_dir}")
    for img in images:
        print(f"  {img.name}")
    
    # Clean up intermediate PDF
    pdf_path.unlink(missing_ok=True)
    
    return [str(p) for p in images]


def main():
    parser = argparse.ArgumentParser(description="Visual verification for PPTX")
    parser.add_argument("pptx", help="Input PPTX file")
    parser.add_argument("--output-dir", "-o", help="Output directory for images")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (default: 150)")
    args = parser.parse_args()

    images = pptx_to_images(args.pptx, args.output_dir, args.dpi)
    if not images:
        print("Warning: No images generated", file=sys.stderr)
        sys.exit(1)
    print(f"\n✅ Visual verification images ready. Review each slide for:")
    print("   - Text cutoff / overflow")
    print("   - Element overlap or misalignment")
    print("   - Color contrast issues")
    print("   - Visual hierarchy correctness")


if __name__ == "__main__":
    main()
