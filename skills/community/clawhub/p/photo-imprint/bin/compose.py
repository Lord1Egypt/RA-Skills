#!/usr/bin/env python3
"""Deterministically compose normalized subject plates into final carousel pages.

This is deliberately a small, closed renderer for the configuration vocabulary
currently shipped by the skill.  It never invents fonts, assets, captions, or
module behavior: unsupported enabled settings stop the build.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFont

from renderer_receipt import load as load_renderer_receipt, validate as validate_renderer_receipt

SUPPORTED_MODULES = {"caption", "route", "watermark"}
KNOWN_MODULES = SUPPORTED_MODULES | {"disclosure", "numbering"}
SUPPORTED_CAPTION_FIELDS = {"location", "subject", "date"}


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def color(value: object, label: str, alpha: int = 255) -> tuple[int, int, int, int]:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a color string")
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise ValueError(f"invalid {label}: {value!r}") from exc
    if len(rgb) != 3:
        raise ValueError(f"{label} must resolve to RGB")
    return rgb[0], rgb[1], rgb[2], alpha


def integer(value: object, label: str, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def ratio(value: object, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= float(value) <= 1:
        raise ValueError(f"{label} must be a number from 0 to 1")
    return float(value)


def enabled(module: object) -> bool:
    return isinstance(module, dict) and module.get("enabled") is True


def validate_and_get(config: dict[str, Any], plan: dict[str, Any], font_path: Path | None) -> dict[str, Any]:
    if config.get("resolved") is not True:
        raise ValueError("config is not a resolved configuration")
    profiles = config.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("config.profiles must be an object")
    composition = profiles.get("composition")
    unification = profiles.get("unification")
    if not isinstance(composition, dict) or not isinstance(unification, dict):
        raise ValueError("resolved config requires composition and unification profiles")
    canvas = composition.get("canvas")
    if not isinstance(canvas, dict):
        raise ValueError("composition.canvas must be an object")
    width = integer(canvas.get("width"), "composition.canvas.width")
    height = integer(canvas.get("height"), "composition.canvas.height")
    subject = composition.get("subject")
    if not isinstance(subject, dict):
        raise ValueError("composition.subject must be an object")
    low = ratio(subject.get("height_ratio_min"), "subject.height_ratio_min")
    high = ratio(subject.get("height_ratio_max"), "subject.height_ratio_max")
    if not 0 < low <= high < 1:
        raise ValueError("subject height ratios must satisfy 0 < min <= max < 1")
    ratio(subject.get("center_y_ratio"), "subject.center_y_ratio")
    whitespace = composition.get("whitespace")
    if not isinstance(whitespace, dict):
        raise ValueError("composition.whitespace must be an object")
    ratio(whitespace.get("edge_margin_ratio"), "whitespace.edge_margin_ratio")
    if composition.get("cross_slide", {}).get("assembly") not in {None, "single-long-canvas-then-crop"}:
        raise ValueError("unsupported composition.cross_slide.assembly")

    paper = unification.get("paper")
    if not isinstance(paper, dict):
        raise ValueError("unification.paper must be an object")
    color(paper.get("color"), "unification.paper.color")
    if paper.get("finish") not in {None, "matte"}:
        raise ValueError("unsupported paper finish")
    if paper.get("texture_scale") not in {None, "shared-master"}:
        raise ValueError("unsupported paper texture scale")

    modules = config.get("modules", {})
    if not isinstance(modules, dict):
        raise ValueError("config.modules must be an object")
    unknown = set(modules) - KNOWN_MODULES
    if unknown:
        raise ValueError("unsupported modules: " + ", ".join(sorted(unknown)))
    unsupported_enabled = sorted(name for name in ("disclosure", "numbering") if enabled(modules.get(name)))
    if unsupported_enabled:
        raise ValueError("unsupported enabled modules: " + ", ".join(unsupported_enabled))

    needs_font = enabled(modules.get("caption")) or enabled(modules.get("watermark"))
    if needs_font:
        if font_path is None or not font_path.is_file():
            raise ValueError(f"configured typography requires an explicit readable font asset: {font_path}")
        try:
            ImageFont.truetype(str(font_path), 12)
        except OSError as exc:
            raise ValueError(f"font asset is unreadable: {font_path}: {exc}") from exc

    caption = modules.get("caption", {})
    if enabled(caption):
        lines = caption.get("lines")
        if not isinstance(lines, list) or not lines or not all(isinstance(v, str) for v in lines):
            raise ValueError("caption.lines must be a non-empty string array")
        unknown_lines = set(lines) - SUPPORTED_CAPTION_FIELDS
        if unknown_lines:
            raise ValueError("unsupported caption fields: " + ", ".join(sorted(unknown_lines)))
        zone = composition.get("caption_zone")
        if not isinstance(zone, dict) or zone.get("position") != "below-subject" or zone.get("alignment") != "center":
            raise ValueError("unsupported caption zone; expected centered below-subject")
        maximum = integer(zone.get("maximum_lines"), "caption_zone.maximum_lines")
        if len(lines) > maximum:
            raise ValueError("caption lines exceed caption_zone.maximum_lines")
        integer(caption.get("font_size_at_1080px"), "caption.font_size_at_1080px")
        color(caption.get("color"), "caption.color")

    watermark = modules.get("watermark", {})
    if enabled(watermark):
        if not isinstance(watermark.get("text"), str) or not watermark["text"].strip():
            raise ValueError("watermark.text must be non-empty")
        if watermark.get("position") != "top-right":
            raise ValueError("unsupported watermark position")

    route = modules.get("route", {})
    if enabled(route):
        color(route.get("color"), "route.color")
        opacity = ratio(route.get("opacity"), "route.opacity")
        if opacity <= 0:
            raise ValueError("route.opacity must be greater than zero")
        integer(route.get("width_at_1080px"), "route.width_at_1080px")
        for key in ("hand_drawn", "anti_alias", "avoid_subjects"):
            if not isinstance(route.get(key), bool):
                raise ValueError(f"route.{key} must be boolean")
        markers = route.get("markers", {})
        if not isinstance(markers, dict):
            raise ValueError("route.markers must be an object")
        for key in ("enabled", "start", "end"):
            if key in markers and not isinstance(markers[key], bool):
                raise ValueError(f"route.markers.{key} must be boolean")

    pages = plan.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("render plan requires a non-empty pages array")
    seen: set[int] = set()
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("render plan pages must be objects")
        number = page.get("page")
        if not isinstance(number, int) or number < 1 or number in seen:
            raise ValueError("every page requires a unique positive integer page number")
        seen.add(number)
        placement = page.get("placement", "center")
        if placement not in {"left", "center", "right"}:
            raise ValueError(f"page {number}: unsupported placement {placement!r}")
        if enabled(caption):
            data = page.get("caption_data")
            if not isinstance(data, dict):
                raise ValueError(f"page {number}: caption_data is required")
            for field in caption["lines"]:
                if not isinstance(data.get(field), str) or not data[field].strip():
                    raise ValueError(f"page {number}: caption field {field!r} is missing")
    return {
        "composition": composition,
        "paper": paper,
        "modules": modules,
        "pages": pages,
        "width": width,
        "height": height,
    }


def find_plate(directory: Path, page: int) -> Path:
    matches: list[Path] = []
    for stem in (f"{page:02d}", str(page)):
        for suffix in (".png", ".webp"):
            candidate = directory / (stem + suffix)
            if candidate.is_file() and candidate not in matches:
                matches.append(candidate)
    if len(matches) != 1:
        raise ValueError(f"page {page}: expected exactly one plate named {page:02d}.png/.webp or {page}.png/.webp")
    return matches[0]


def prepared_subject(path: Path, composition: dict[str, Any], placement: str, canvas: tuple[int, int]) -> tuple[Image.Image, tuple[int, int]]:
    try:
        with Image.open(path) as source:
            if "A" not in source.getbands():
                raise ValueError(f"plate lacks alpha channel: {path}")
            plate = source.convert("RGBA")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"unreadable plate {path}: {exc}") from exc
    bbox = plate.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"plate is fully transparent: {path}")
    plate = plate.crop(bbox)
    width, height = canvas
    subject = composition["subject"]
    target_height = round(height * (float(subject["height_ratio_min"]) + float(subject["height_ratio_max"])) / 2)
    margin = round(width * float(composition["whitespace"]["edge_margin_ratio"]))
    max_width = width - 2 * margin
    scale = min(target_height / plate.height, max_width / plate.width)
    new_size = (max(1, round(plate.width * scale)), max(1, round(plate.height * scale)))
    plate = plate.resize(new_size, Image.Resampling.LANCZOS)
    x_centers = {"left": 0.28, "center": 0.5, "right": 0.72}
    x = round(width * x_centers[placement] - plate.width / 2)
    x = min(max(margin, x), width - margin - plate.width)
    y = round(height * float(subject["center_y_ratio"]) - plate.height / 2)
    y = min(max(0, y), height - plate.height)
    return plate, (x, y)


def global_page_numbers(plan: dict[str, Any], pages: list[dict[str, Any]]) -> list[int]:
    numbers = {page["page"] for page in pages}
    gate = plan.get("review_gate", {})
    if isinstance(gate, dict):
        for key in ("permitted_before_approval", "blocked_before_approval"):
            values = gate.get(key, [])
            if isinstance(values, list):
                numbers.update(value for value in values if isinstance(value, int) and value > 0)
    ordered = sorted(numbers)
    if ordered != list(range(1, max(ordered) + 1)):
        raise ValueError(f"route requires globally contiguous page numbers from 1, got {ordered}")
    return ordered


def route_layer(width: int, height: int, count: int, route: dict[str, Any]) -> list[Image.Image]:
    scale = 4 if route.get("anti_alias") else 1
    long_width, long_height = width * count * scale, height * scale
    layer = Image.new("RGBA", (long_width, long_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    base = color(route["color"], "route.color", round(float(route["opacity"]) * 255))
    line_width = max(1, round(int(route["width_at_1080px"]) * width / 1080 * scale))
    start_x, end_x = round(width * 0.07 * scale), round((width * count - width * 0.07) * scale)
    center_y = height * 0.34 * scale
    amplitude = height * 0.018 * scale if route.get("hand_drawn") else 0
    samples = max(12, count * 24)
    points = []
    for index in range(samples + 1):
        fraction = index / samples
        x = start_x + (end_x - start_x) * fraction
        y = center_y + amplitude * math.sin(fraction * math.pi * (count + 1))
        points.append((round(x), round(y)))
    draw.line(points, fill=base, width=line_width, joint="curve")
    markers = route.get("markers", {})
    if markers.get("enabled"):
        radius = max(3 * scale, line_width * 2)
        if markers.get("start"):
            x, y = points[0]
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=base)
        if markers.get("end"):
            x, y = points[-1]
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=base)
    if scale != 1:
        layer = layer.resize((width * count, height), Image.Resampling.LANCZOS)
    return [layer.crop((index * width, 0, (index + 1) * width, height)) for index in range(count)]


def draw_text_modules(
    image: Image.Image,
    page: dict[str, Any],
    modules: dict[str, Any],
    composition: dict[str, Any],
    font_path: Path | None,
) -> None:
    width, height = image.size
    draw = ImageDraw.Draw(image)
    caption = modules.get("caption", {})
    if enabled(caption):
        font_size = max(1, round(int(caption["font_size_at_1080px"]) * width / 1080))
        font = ImageFont.truetype(str(font_path), font_size)
        lines = [page["caption_data"][field] for field in caption["lines"]]
        spacing = max(1, round(font_size * 0.25))
        boxes = [draw.textbbox((0, 0), text, font=font) for text in lines]
        heights = [box[3] - box[1] for box in boxes]
        total = sum(heights) + spacing * (len(lines) - 1)
        subject = composition["subject"]
        subject_bottom = height * (float(subject["center_y_ratio"]) + float(subject["height_ratio_max"]) / 2)
        clearance = height * float(composition["caption_zone"].get("minimum_subject_clearance_ratio", 0))
        y = round(subject_bottom + clearance)
        if y + total > height:
            raise ValueError(f"page {page['page']}: caption does not fit below subject")
        fill = color(caption["color"], "caption.color")
        for text, box, line_height in zip(lines, boxes, heights):
            text_width = box[2] - box[0]
            draw.text(((width - text_width) // 2, y), text, font=font, fill=fill)
            y += line_height + spacing
    watermark = modules.get("watermark", {})
    if enabled(watermark):
        size = max(1, round(18 * width / 1080))
        font = ImageFont.truetype(str(font_path), size)
        text = watermark["text"]
        box = draw.textbbox((0, 0), text, font=font)
        margin = max(4, round(width * 0.035))
        draw.text((width - margin - (box[2] - box[0]), margin), text, font=font, fill=(59, 56, 50, 180))


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministically compose plates, paper, route, captions, and watermark")
    parser.add_argument("--config", required=True, type=Path, help="Resolved config JSON")
    parser.add_argument("--render-plan", required=True, type=Path)
    parser.add_argument("--plates", required=True, type=Path, help="Directory containing numbered normalized plates")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--font", type=Path, help="Explicit font file required by enabled typography")
    parser.add_argument("--renderer-receipt", required=True, type=Path,
                        help="Valid receipt whose rendered-output hashes include every input plate")
    args = parser.parse_args()
    try:
        config = load_object(args.config, "resolved config")
        plan = load_object(args.render_plan, "render plan")
        context = validate_and_get(config, plan, args.font)
        if not args.plates.is_dir():
            raise ValueError(f"plates directory is missing: {args.plates}")
        receipt = load_renderer_receipt(args.renderer_receipt)
        receipt_errors = validate_renderer_receipt(receipt, check_files=True, require_rendered_output=True)
        if receipt_errors:
            raise ValueError("invalid renderer receipt: " + "; ".join(receipt_errors))
        registered_outputs = {
            (Path(entry["path"]).resolve(), entry["sha256"])
            for entry in receipt["rendered_outputs"]
        }
        registered_sources = {
            (str(Path(entry["path"]).resolve()), entry["sha256"])
            for entry in receipt["sources"]
        }
        expected_sources = {
            (str(Path(str(page.get("source_path", ""))).resolve()), page.get("source_sha256"))
            for page in context["pages"]
        }
        if registered_sources != expected_sources:
            raise ValueError("renderer receipt sources do not exactly match render-plan sources")
        registered_references = {
            (str(Path(entry["path"]).resolve()), entry["sha256"])
            for entry in receipt["references"]
        }
        expected_references = {
            (str(Path(str(entry.get("image_path", ""))).resolve()), entry.get("image_sha256"))
            for entry in plan.get("style_reference_locks", [])
        }
        if registered_references != expected_references:
            raise ValueError("renderer receipt references do not exactly match render-plan references")
        plate_paths = {page["page"]: find_plate(args.plates, page["page"]) for page in context["pages"]}
        import hashlib
        expected_outputs = {
            (plate_path.resolve(), hashlib.sha256(plate_path.read_bytes()).hexdigest())
            for plate_path in plate_paths.values()
        }
        if registered_outputs != expected_outputs:
            raise ValueError("renderer receipt outputs must exactly match the normalized plate set")
        output = args.output
        output.mkdir(parents=True, exist_ok=True)
        width, height = context["width"], context["height"]
        paper_rgba = color(context["paper"]["color"], "paper color")
        global_numbers = global_page_numbers(plan, context["pages"])
        if enabled(context["modules"].get("route")):
            all_routes = route_layer(width, height, len(global_numbers), context["modules"]["route"])
            routes = {number: all_routes[number - 1] for number in global_numbers}
        else:
            routes = {number: None for number in global_numbers}
        plate_evidence = [
            {"page": number, "path": str(path.resolve()),
             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for number, path in sorted(plate_paths.items())
        ]
        outputs: list[dict[str, Any]] = []
        for page in context["pages"]:
            plate_path = plate_paths[page["page"]]
            subject, position = prepared_subject(
                plate_path, context["composition"], page.get("placement", "center"), (width, height)
            )
            final = Image.new("RGBA", (width, height), paper_rgba)
            subject_layer = Image.new("RGBA", final.size, (0, 0, 0, 0))
            subject_layer.alpha_composite(subject, position)
            final = Image.alpha_composite(final, subject_layer)
            route_segment = routes[page["page"]]
            if route_segment is not None:
                final = Image.alpha_composite(final, route_segment)
            draw_text_modules(final, page, context["modules"], context["composition"], args.font)
            target = output / f"{page['page']:02d}.png"
            final.save(target, format="PNG", compress_level=9, optimize=False)
            with Image.open(target) as check:
                forbidden = [key for key in check.info if any(term in key.lower() for term in ("exif", "xmp", "gps"))]
                if forbidden or check.getexif():
                    target.unlink(missing_ok=True)
                    raise ValueError(f"metadata stripping failed for page {page['page']}: {forbidden}")
            outputs.append({
                "page": page["page"], "path": str(target.resolve()),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            })
        manifest_path = output / "composition-manifest.json"
        font_evidence = None
        if args.font is not None:
            font_evidence = {"path": str(args.font.resolve()),
                             "sha256": hashlib.sha256(args.font.read_bytes()).hexdigest()}
        manifest_path.write_text(json.dumps({
            "schema_version": "1.1.0", "deterministic": True,
            "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
            "render_plan_sha256": hashlib.sha256(args.render_plan.read_bytes()).hexdigest(),
            "renderer_receipt": {"path": str(args.renderer_receipt.resolve()),
                                 "sha256": hashlib.sha256(args.renderer_receipt.read_bytes()).hexdigest()},
            "font": font_evidence,
            "plates": plate_evidence,
            "metadata_policy": {"exif_gps_xmp": "forbidden", "verified": True},
            "outputs": outputs,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Composed {len(outputs)} deterministic page(s) in {output}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Composition blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
