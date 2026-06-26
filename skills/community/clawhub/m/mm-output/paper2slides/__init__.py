"""
Paper2Slides module for PosterGenParserUnit.
Generates poster/slides images from markdown content using Gemini image generation.

Usage:
    from paper2slides import generate_poster_image, generate_slides_images, generate_xhs_slides

    results = generate_poster_image(parser_results, output_dir)
    results = generate_slides_images(parser_results, output_dir)
    results = generate_xhs_slides(parser_results, output_dir)
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from .models import ContentPlan, GeneratedImage
from .content_planner import ContentPlanner
from .image_generator import GeminiImageGenerator, save_images_as_pdf
from .xhs_generator import generate_xhs_copy, build_xhs_html

logger = logging.getLogger(__name__)


def generate_poster_image(
    parser_results: Dict,
    output_dir: str,
    style: str = "academic",
    density: str = "medium",
    text_model: str = None,
    image_gen_api_key: str = None,
    language: str = "auto",
) -> Dict[str, Any]:
    """
    Generate a poster image from parser results.

    Args:
        parser_results: Output from PosterGenParserUnit.parse() or parse_markdown()
        output_dir: Directory to save generated images
        style: Style name (academic, doraemon, minimal)
        density: Content density (sparse, medium, dense)
        text_model: VLM model for content planning (uses env TEXT_MODEL if None)
        image_gen_api_key: Gemini API key (uses env IMAGE_GEN_API_KEY if None)
        language: Language for output (auto, zh, en)

    Returns:
        Dict with status, output paths, and metadata
    """
    return _generate(
        parser_results=parser_results,
        output_dir=output_dir,
        output_type="poster",
        style=style,
        density=density,
        text_model=text_model,
        image_gen_api_key=image_gen_api_key,
        language=language,
    )


def generate_slides_images(
    parser_results: Dict,
    output_dir: str,
    style: str = "academic",
    slides_length: str = "medium",
    text_model: str = None,
    image_gen_api_key: str = None,
    language: str = "auto",
) -> Dict[str, Any]:
    """
    Generate slides images from parser results.

    Args:
        parser_results: Output from PosterGenParserUnit.parse() or parse_markdown()
        output_dir: Directory to save generated images
        style: Style name (academic, doraemon, minimal)
        slides_length: Number of slides (short=5-8, medium=8-12, long=12-15)
        text_model: VLM model for content planning (uses env TEXT_MODEL if None)
        image_gen_api_key: Gemini API key (uses env IMAGE_GEN_API_KEY if None)
        language: Language for output (auto, zh, en)

    Returns:
        Dict with status, output paths, and metadata
    """
    return _generate(
        parser_results=parser_results,
        output_dir=output_dir,
        output_type="slides",
        style=style,
        slides_length=slides_length,
        text_model=text_model,
        image_gen_api_key=image_gen_api_key,
        language=language,
    )


def _generate(
    parser_results: Dict,
    output_dir: str,
    output_type: str,
    style: str = "academic",
    density: str = "medium",
    slides_length: str = "medium",
    text_model: str = None,
    image_gen_api_key: str = None,
    language: str = "auto",
) -> Dict[str, Any]:
    """Internal: run content planning then image generation."""
    out_path = Path(output_dir)
    img_dir = out_path / f"{output_type}_images"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Content Planning
    logger.info("[Paper2Slides] Step 1: Content planning (%s)...", output_type)
    print(f"[Paper2Slides] Planning {output_type} content...")
    planner = ContentPlanner(model=text_model)
    plan = planner.plan_from_parser_results(
        parser_results,
        output_type=output_type,
        density=density,
        slides_length=slides_length,
        language=language,
    )
    logger.info("[Paper2Slides] Planned %d sections", len(plan.sections))
    print(f"[Paper2Slides] Planned {len(plan.sections)} sections")

    plan_path = img_dir / "content_plan.json"
    plan_path.write_text(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    # Step 2: Image Generation
    logger.info("[Paper2Slides] Step 2: Generating %s images...", output_type)
    print(f"[Paper2Slides] Generating {output_type} images via Gemini...")
    generator = GeminiImageGenerator(api_key=image_gen_api_key)

    figure_base_path = ""
    figures_path = parser_results.get("figures_path", "")
    if figures_path:
        figure_base_path = str(Path(figures_path).parent)

    images = generator.generate(plan, style=style, figure_base_path=figure_base_path, language=language)
    logger.info("[Paper2Slides] Generated %d images", len(images))
    print(f"[Paper2Slides] Generated {len(images)} images")

    # Step 3: Save outputs
    ext_map = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
    output_files = []

    for img in images:
        ext = ext_map.get(img.mime_type, ".png")
        filepath = img_dir / f"{img.section_id}{ext}"
        filepath.write_bytes(img.image_data)
        output_files.append(str(filepath))
        logger.info("[Paper2Slides] Saved: %s", filepath.name)
        print(f"[Paper2Slides] Saved: {filepath.name}")

    # For slides, also generate a combined PDF
    pdf_path = None
    if output_type == "slides" and len(images) > 1:
        try:
            pdf_path = str(img_dir / "slides.pdf")
            save_images_as_pdf(images, pdf_path)
            output_files.append(pdf_path)
            logger.info("[Paper2Slides] Saved: slides.pdf")
            print("[Paper2Slides] Saved: slides.pdf")
        except ImportError:
            logger.warning("Pillow not installed, skipping PDF generation")
            print("[Paper2Slides] Warning: Pillow not installed, skipping PDF generation")

    return {
        "status": "success",
        "output_type": output_type,
        "output_dir": str(img_dir),
        "images": output_files,
        "pdf_path": pdf_path,
        "num_sections": len(plan.sections),
        "num_images": len(images),
        "plan_path": str(plan_path),
    }


def generate_xhs_slides(
    parser_results: Dict,
    output_dir: str,
    style: str = "academic",
    slides_length: str = "short",
    text_model: str = None,
    image_gen_api_key: str = None,
    language: str = "zh",
) -> Dict[str, Any]:
    """
    Generate vertical slides images + XHS HTML page with copywriting.

    Pipeline:
      1. Content plan (slides)
      2. Vertical (9:16) image generation via Gemini
      3. XHS copywriting via LLM
      4. XHS HTML with carousel + copy

    Returns:
        Dict with status, image paths, html path, and xhs copy.
    """
    out_path = Path(output_dir)
    img_dir = out_path / "xhs_slides"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Content Planning
    print("[XHS-Slides] Step 1: Planning slides content...")
    planner = ContentPlanner(model=text_model)
    plan = planner.plan_from_parser_results(
        parser_results,
        output_type="slides",
        slides_length=slides_length,
        language=language,
    )
    print(f"[XHS-Slides] Planned {len(plan.sections)} sections")

    plan_path = img_dir / "content_plan.json"
    plan_path.write_text(
        json.dumps(plan.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Step 2: Generate vertical (9:16) slide images
    print("[XHS-Slides] Step 2: Generating vertical slide images via Gemini...")
    generator = GeminiImageGenerator(api_key=image_gen_api_key)

    figure_base_path = ""
    figures_path = parser_results.get("figures_path", "")
    if figures_path:
        figure_base_path = str(Path(figures_path).parent)

    images = generator.generate(
        plan, style=style, figure_base_path=figure_base_path,
        language=language, orientation="portrait",
    )
    print(f"[XHS-Slides] Generated {len(images)} vertical slides")

    # Save images
    ext_map = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
    image_files = []
    for img in images:
        ext = ext_map.get(img.mime_type, ".png")
        fpath = img_dir / f"{img.section_id}{ext}"
        fpath.write_bytes(img.image_data)
        image_files.append(str(fpath))
        print(f"[XHS-Slides] Saved: {fpath.name}")

    # Step 3: Generate XHS copywriting
    print("[XHS-Slides] Step 3: Generating 小红书 copywriting...")
    md_path = parser_results.get("raw_text_path", "")
    md_text = Path(md_path).read_text(encoding="utf-8") if md_path else ""
    xhs_copy = generate_xhs_copy(md_text, model=text_model)

    copy_path = img_dir / "xhs_copy.json"
    copy_path.write_text(
        json.dumps(xhs_copy, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Step 4: Build XHS HTML
    print("[XHS-Slides] Step 4: Building XHS HTML page...")
    html_path = build_xhs_html(
        image_paths=image_files,
        xhs_copy=xhs_copy,
        output_dir=str(img_dir),
    )

    # Optional: slides PDF
    pdf_path = None
    if len(images) > 1:
        try:
            pdf_path = str(img_dir / "slides.pdf")
            save_images_as_pdf(images, pdf_path)
            print("[XHS-Slides] Saved: slides.pdf")
        except ImportError:
            print("[XHS-Slides] Warning: Pillow not installed, skipping PDF")

    return {
        "status": "success",
        "output_type": "xhs_slides",
        "output_dir": str(img_dir),
        "images": image_files,
        "html_path": html_path,
        "pdf_path": pdf_path,
        "xhs_copy": xhs_copy,
        "num_sections": len(plan.sections),
        "num_images": len(images),
        "plan_path": str(plan_path),
    }
