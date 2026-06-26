#!/usr/bin/env python3
"""PDF to Markdown converter using Marker.

This script extracts text and mathematical formulas from academic PDF papers.

It supports two modes:
- Pure Marker (local models only)
- Marker hybrid mode with an LLM (via Marker LLM services)

The LLM mode is useful for improving table formatting, inline math, and
cross-page structure.

Environment: D:/anaconda3/envs/pdf-extractor
Requirements: marker-pdf, torch>=2.1.0
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Ensure this script folder is importable by Marker config.
sys.path.insert(0, str(Path(__file__).parent))


# Volcengine (Ark / Coding Plan) OpenAI-compatible endpoint
# NOTE: no trailing slash.
DEFAULT_ARK_OPENAI_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"

# Prefer env var to avoid hardcoding secrets in code.
# Fallback kept for convenience (matches user's provided key).
DEFAULT_ARK_OPENAI_API_KEY = os.environ.get("VOLCENGINE_CODING_PLAN_API_KEY") or os.environ.get(
    "ARK_API_KEY"
) or "991ee1db-32ff-4884-b45a-155fa632ecbb"

# As requested: use ark-code-latest; backend routes to an appropriate model.
DEFAULT_ARK_OPENAI_MODEL = "ark-code-latest"


def convert_pdf(
    pdf_path: str,
    output_dir: Optional[str] = None,
    *,
    force_ocr: bool = False,
    batch_multiplier: int = 2,
    languages: Optional[list[str]] = None,
    page_range: Optional[str] = None,
    use_llm: bool = False,
    llm_service: Optional[str] = None,
    openai_base_url: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    openai_model: Optional[str] = None,
) -> tuple[str, dict]:
    """Convert a PDF file to Markdown using Marker.

    Args:
        pdf_path: Path to PDF file.
        output_dir: Output directory (default: same as PDF).
        force_ocr: Force OCR even for text PDFs.
        batch_multiplier: Batch size multiplier for GPU.
        languages: List of languages (e.g., ['Chinese', 'English']).
        page_range: Marker page range string (e.g., "0", "0,5-10").
        use_llm: Enable Marker hybrid mode (uses an LLM service).
        llm_service: Marker LLM service class path.
        openai_base_url: Base URL for OpenAI-compatible endpoint.
        openai_api_key: API key for OpenAI-compatible endpoint.
        openai_model: Model name for OpenAI-compatible endpoint.

    Returns:
        (markdown_text, metadata_dict)
    """

    # Local imports so the module is importable even if marker isn't installed.
    from marker.config.parser import ConfigParser
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    pdf_file = Path(pdf_path).resolve()

    # Defaults
    if languages is None:
        languages = ["Chinese", "English"]

    # Marker config
    config: dict = {
        "output_format": "markdown",
        "force_ocr": force_ocr,
        "languages": languages,
        "batch_multiplier": batch_multiplier,
    }

    if page_range:
        # Marker CLI calls this `--page_range`.
        config["page_range"] = page_range

    if use_llm:
        config["use_llm"] = True
        if llm_service:
            # Marker CLI uses `--llm_service`.
            config["llm_service"] = llm_service

        # If user supplies OpenAI-compatible config, pass through.
        if openai_base_url:
            config["openai_base_url"] = openai_base_url
        if openai_api_key:
            config["openai_api_key"] = openai_api_key
        if openai_model:
            config["openai_model"] = openai_model

    # Marker sometimes expects this to exist even if unused.
    os.environ.setdefault("TESSDATA_PREFIX", "")

    print("Loading Marker models...")
    print(f"  File: {pdf_file}")
    print(f"  Languages: {languages}")
    print(f"  Force OCR: {force_ocr}")
    if page_range:
        print(f"  Page range: {page_range}")
    print(f"  LLM hybrid mode: {use_llm}")
    if use_llm:
        if llm_service:
            print(f"  LLM service: {llm_service}")
        if openai_base_url:
            print(f"  OpenAI base_url: {openai_base_url}")
        if openai_model:
            print(f"  OpenAI model: {openai_model}")

    model_dict = create_model_dict()
    config_parser = ConfigParser(config)

    converter = PdfConverter(
        artifact_dict=model_dict,
        config=config_parser.generate_config_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )

    rendered = converter(str(pdf_file))
    markdown_text, metadata, images = text_from_rendered(rendered)

    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        md_file = out_dir / f"{pdf_file.stem}.md"
        md_file.write_text(markdown_text, encoding="utf-8")
        print(f"Saved: {md_file}")

        if images:
            img_dir_name = f"{pdf_file.stem}_images"
            # In segmented runs (page_range specified), avoid collisions by writing
            # images to a page-range-specific folder.
            if page_range:
                safe_range = (
                    page_range.replace(" ", "")
                    .replace(",", "_")
                    .replace("-", "-")
                    .replace(":", "_")
                )
                img_dir_name = f"{pdf_file.stem}_images_p{safe_range}"

            img_dir = out_dir / img_dir_name
            img_dir.mkdir(exist_ok=True)

            saved = 0
            for img_name, img_data in getattr(images, "items", lambda: [])():
                img_path = img_dir / img_name

                # Marker may return raw bytes OR PIL.Image objects.
                if isinstance(img_data, (bytes, bytearray, memoryview)):
                    img_path.write_bytes(img_data)
                    saved += 1
                    continue

                if hasattr(img_data, "save"):
                    img_data.save(img_path)
                    saved += 1
                    continue

            print(f"Saved {saved} images to: {img_dir}")

    return markdown_text, metadata


def convert_pdf_cli(pdf_path: str, output_path: Optional[str] = None, **kwargs) -> str:
    """CLI-friendly wrapper.

    Args:
        pdf_path: Path to PDF file.
        output_path: Output file path (.md) or directory.
        **kwargs: Passed to convert_pdf.

    Returns:
        Path to the output markdown file.
    """

    pdf_file = Path(pdf_path).resolve()
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")

    if output_path:
        out_path = Path(output_path)
        if out_path.suffix.lower() == ".md":
            output_dir = out_path.parent
            output_file = out_path
        else:
            output_dir = out_path
            output_file = output_dir / f"{pdf_file.stem}.md"
    else:
        output_dir = pdf_file.parent
        output_file = output_dir / f"{pdf_file.stem}.md"

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_text, _metadata = convert_pdf(str(pdf_file), str(output_dir), **kwargs)

    # If user requested a specific .md filename, rename.
    if output_file.name != f"{pdf_file.stem}.md":
        default_md = output_dir / f"{pdf_file.stem}.md"
        if default_md.exists():
            default_md.replace(output_file)
            print(f"Renamed output to: {output_file}")
        else:
            output_file.write_text(markdown_text, encoding="utf-8")

    return str(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown using Marker (supports Chinese + Math)"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-o", "--output", help="Output file (.md) or directory")
    parser.add_argument(
        "--force-ocr", action="store_true", help="Force OCR even for text PDFs"
    )
    parser.add_argument(
        "--batch-multiplier",
        type=int,
        default=2,
        help="Batch size multiplier (default: 2)",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["Chinese", "English"],
        help="Languages in the document (default: Chinese English)",
    )
    parser.add_argument(
        "--page-range",
        default=None,
        help='Page range string, e.g. "0" or "0,5-10" (0-based pages)',
    )

    llm = parser.add_argument_group("LLM hybrid mode")
    llm.add_argument(
        "--use-llm",
        action="store_true",
        help="Enable Marker hybrid mode using an LLM service",
    )
    llm.add_argument(
        "--llm-service",
        default=None,
        help=(
            "Marker LLM service class path, e.g. marker.services.openai.OpenAIService"
        ),
    )
    llm.add_argument("--openai-base-url", default=None)
    llm.add_argument("--openai-api-key", default=None)
    llm.add_argument("--openai-model", default=None)

    llm.add_argument(
        "--ark-code-latest",
        action="store_true",
        help=(
            "Shortcut: use Volcengine Ark (Coding Plan) via OpenAI-compatible endpoint "
            f"({DEFAULT_ARK_OPENAI_BASE_URL}), model={DEFAULT_ARK_OPENAI_MODEL}"
        ),
    )

    args = parser.parse_args()

    use_llm = args.use_llm
    llm_service = args.llm_service
    openai_base_url = args.openai_base_url
    openai_api_key = args.openai_api_key
    openai_model = args.openai_model

    if args.ark_code_latest:
        use_llm = True
        # Use our robust OpenAI-compatible JSON-only service.
        llm_service = "marker_openai_compat_service.OpenAICompatJSONService"
        openai_base_url = DEFAULT_ARK_OPENAI_BASE_URL
        openai_api_key = DEFAULT_ARK_OPENAI_API_KEY
        openai_model = DEFAULT_ARK_OPENAI_MODEL

    try:
        output_file = convert_pdf_cli(
            args.pdf,
            args.output,
            force_ocr=args.force_ocr,
            batch_multiplier=args.batch_multiplier,
            languages=args.languages,
            page_range=args.page_range,
            use_llm=use_llm,
            llm_service=llm_service,
            openai_base_url=openai_base_url,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
        )
        print(f"\nConversion complete: {output_file}")

    except Exception as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
