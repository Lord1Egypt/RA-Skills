#!/usr/bin/env python3
"""
PDF to LaTeX/Markdown Converter using Nougat OCR

This script extracts text and mathematical formulas from academic PDF papers
and converts them to LaTeX-compatible Markdown format.

Environment: D:\anaconda3\envs\pdf-extractor
"""

import argparse
import torch
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import sys
from tqdm import tqdm


def load_model(model_tag="0.1.0-base", device=None):
    """Load Nougat model with GPU support if available."""
    from nougat import NougatModel
    from nougat.utils.checkpoint import get_checkpoint

    print(f"Loading Nougat model ({model_tag})...")
    checkpoint = get_checkpoint(model_tag=model_tag)
    model = NougatModel.from_pretrained(checkpoint)

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    if device == "cuda":
        model = model.to("cuda")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Using CPU")

    model.eval()
    return model, device


def render_page(page, dpi=300):
    """Render a PDF page to PIL Image."""
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return Image.open(io.BytesIO(img_data)).convert("RGB")


def process_pdf(pdf_path, model, device, pages=None, dpi=300):
    """
    Process a PDF file and extract text/formulas.

    Args:
        pdf_path: Path to PDF file
        model: Loaded Nougat model
        device: 'cuda' or 'cpu'
        pages: List of page numbers (0-indexed) or None for all pages
        dpi: Resolution for rendering (default 300)

    Returns:
        List of (page_num, text) tuples
    """
    from nougat.utils.device import move_to_device

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    if pages is None:
        pages = list(range(total_pages))
    else:
        pages = [p for p in pages if 0 <= p < total_pages]

    print(f"Processing {len(pages)} pages from {pdf_path}")

    results = []
    for page_num in tqdm(pages, desc="Converting"):
        page = doc[page_num]
        img = render_page(page, dpi)

        # Prepare for model
        img_tensor = model.encoder.prepare_input(img, random_padding=False)
        img_tensor = move_to_device(img_tensor.unsqueeze(0), device)

        # Inference
        with torch.no_grad():
            output = model.inference(image_tensors=img_tensor)

        text = output["predictions"][0]
        results.append((page_num + 1, text))  # 1-indexed for output

    doc.close()
    return results


def save_results(results, output_path, format="mmd"):
    """Save extraction results to file."""
    if format == "mmd":
        # Single markdown file
        content = "\n\n".join([text for _, text in results])
        Path(output_path).write_text(content, encoding="utf-8")
    elif format == "pages":
        # Separate file per page
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        for page_num, text in results:
            page_file = output_dir / f"page_{page_num:03d}.mmd"
            page_file.write_text(text, encoding="utf-8")

    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to LaTeX/Markdown using Nougat OCR"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("-p", "--pages", help='Page range (e.g., "0-5" or "1,3,5")')
    parser.add_argument("-m", "--model", default="0.1.0-base", help="Model tag")
    parser.add_argument("--dpi", type=int, default=300, help="Render DPI")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode")
    parser.add_argument(
        "--per-page", action="store_true", help="Save each page separately"
    )

    args = parser.parse_args()

    # Parse page range
    pages = None
    if args.pages:
        pages = []
        for part in args.pages.split(","):
            if "-" in part:
                start, end = part.split("-")
                pages.extend(range(int(start), int(end) + 1))
            else:
                pages.append(int(part))

    # Default output
    pdf_path = Path(args.pdf)
    if args.output:
        output_path = args.output
    else:
        if args.per_page:
            output_path = pdf_path.parent / f"{pdf_path.stem}_pages"
        else:
            output_path = pdf_path.with_suffix(".mmd")

    # Load model
    device = "cpu" if args.cpu else None
    model, device = load_model(args.model, device)

    # Process
    results = process_pdf(args.pdf, model, device, pages, args.dpi)

    # Save
    format = "pages" if args.per_page else "mmd"
    save_results(results, output_path, format)

    # Print summary
    total_chars = sum(len(text) for _, text in results)
    print(f"\nSummary:")
    print(f"  Pages processed: {len(results)}")
    print(f"  Total characters: {total_chars}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
