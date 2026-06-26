#!/usr/bin/env python3
"""
Perceptron Vision CLI — powered by the Perceptron Python SDK.

A unified CLI for all Perceptron SDK capabilities: detection, OCR, captioning,
visual Q&A, DSL composition, batch processing, streaming, and more.

Requires: pip install perceptron
API key:  export PERCEPTRON_API_KEY=ak_...
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import perceptron
    from perceptron import (
        configure,
        config,
        detect,
        caption,
        ocr,
        ocr_html,
        ocr_markdown,
        question,
        perceive,

        annotate_image,
        scale_points_to_pixels,
        extract_points,
        parse_text,
        strip_tags,
        inspect_task,
        image,
        text,
        system,
        box,
        point,
        polygon,
        collection,
        agent,
    )
except ImportError:
    print("Error: perceptron SDK not installed. Run: pip install perceptron", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup(args):
    """Apply global config from CLI args."""
    kwargs = {}
    if getattr(args, "api_key", None):
        kwargs["api_key"] = args.api_key
    if getattr(args, "provider", None):
        kwargs["provider"] = args.provider
    if getattr(args, "model", None):
        kwargs["model"] = args.model
    if kwargs:
        configure(**kwargs)


def _gen_kwargs(args):
    """Extract generation kwargs from parsed args."""
    kw = {}
    if getattr(args, "model", None):
        kw["model"] = args.model
    if getattr(args, "temperature", None) is not None:
        kw["temperature"] = args.temperature
    if getattr(args, "max_tokens", None) is not None:
        kw["max_tokens"] = args.max_tokens
    return kw


def _print_result(result, args):
    """Print a PerceiveResult in the requested format."""
    fmt = getattr(args, "format", "text")
    if fmt == "json":
        out = {"text": result.text}
        if result.points:
            out["points"] = _serialize_annotations(result.points)
        if hasattr(result, "usage") and result.usage:
            out["usage"] = result.usage
        print(json.dumps(out, indent=2))
    else:
        if result.text:
            print(result.text)
        if result.points:
            print()
            for ann in result.points:
                _print_annotation(ann)


def _serialize_annotations(points):
    """Convert annotation objects to JSON-serializable dicts."""
    out = []
    for ann in points:
        cls_name = type(ann).__name__
        d = {"type": cls_name.lower(), "mention": ann.mention}
        if cls_name == "SinglePoint":
            d["x"] = ann.x
            d["y"] = ann.y
        elif cls_name == "BoundingBox":
            d["top_left"] = {"x": ann.top_left.x, "y": ann.top_left.y}
            d["bottom_right"] = {"x": ann.bottom_right.x, "y": ann.bottom_right.y}
        elif cls_name == "Polygon":
            d["hull"] = [{"x": p.x, "y": p.y} for p in ann.hull]
        elif cls_name == "Collection":
            d["items"] = _serialize_annotations(getattr(ann, "items", []))
        if ann.t is not None:
            d["confidence"] = ann.t
        out.append(d)
    return out


def _print_annotation(ann):
    """Pretty-print a single annotation."""
    cls_name = type(ann).__name__
    label = ann.mention or "?"
    if cls_name == "SinglePoint":
        print(f"  [{label}] point ({ann.x}, {ann.y})")
    elif cls_name == "BoundingBox":
        print(f"  [{label}] box ({ann.top_left.x},{ann.top_left.y}) → ({ann.bottom_right.x},{ann.bottom_right.y})")
    elif cls_name == "Polygon":
        coords = " ".join(f"({p.x},{p.y})" for p in ann.hull)
        print(f"  [{label}] polygon {coords}")
    elif cls_name == "Collection":
        print(f"  [{label}] collection:")
        for item in getattr(ann, "items", []):
            print("    ", end="")
            _print_annotation(item)


def _handle_stream(stream_iter):
    """Consume a streaming iterator, printing text deltas and collecting result."""
    result = None
    for event in stream_iter:
        etype = event.get("type", "")
        if etype == "text.delta":
            print(event.get("chunk", ""), end="", flush=True)
        elif etype in ("points.delta", "points.snapshot"):
            pts = event.get("points", [])
            if pts:
                for p in pts:
                    _print_annotation(p)
        elif etype == "final":
            result = event.get("result")
    print()
    return result


def _resolve_images(path_str):
    """Resolve a path to a list of image files (supports directories)."""
    p = Path(path_str)
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
    if p.is_dir():
        return sorted(f for f in p.iterdir() if f.suffix.lower() in exts)
    return [p]


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_detect(args):
    """Run object detection."""
    _setup(args)
    classes = args.classes.split(",") if args.classes else None
    gkw = _gen_kwargs(args)

    for img_path in _resolve_images(args.image):
        if len(_resolve_images(args.image)) > 1:
            print(f"\n--- {img_path.name} ---")

        result = detect(
            str(img_path),
            classes=classes,
            stream=args.stream,
            **gkw,
        )

        if args.stream:
            _handle_stream(result)
        else:
            _print_result(result, args)

            # Pixel conversion
            if args.pixels and result.points:
                from PIL import Image as PILImage
                img = PILImage.open(str(img_path))
                w, h = img.size
                img.close()
                pixel_pts = scale_points_to_pixels(result.points, width=w, height=h)
                print(f"\n  Pixel coordinates ({w}x{h}):")
                if pixel_pts:
                    for ann in pixel_pts:
                        print("   ", end="")
                        _print_annotation(ann)


def cmd_caption(args):
    """Generate image captions."""
    _setup(args)
    gkw = _gen_kwargs(args)

    for img_path in _resolve_images(args.image):
        if len(_resolve_images(args.image)) > 1:
            print(f"\n--- {img_path.name} ---")

        result = caption(
            str(img_path),
            style=args.style,
            expects=args.expects,
            stream=args.stream,
            **gkw,
        )

        if args.stream:
            _handle_stream(result)
        else:
            _print_result(result, args)


def cmd_ocr(args):
    """Extract text from images."""
    _setup(args)
    gkw = _gen_kwargs(args)

    ocr_fn = ocr
    if args.output == "html":
        ocr_fn = ocr_html
    elif args.output == "markdown":
        ocr_fn = ocr_markdown

    for img_path in _resolve_images(args.image):
        if len(_resolve_images(args.image)) > 1:
            print(f"\n--- {img_path.name} ---")

        result = ocr_fn(
            str(img_path),
            prompt=args.prompt,
            stream=args.stream,
            **gkw,
        )

        if args.stream:
            _handle_stream(result)
        else:
            _print_result(result, args)


def cmd_question(args):
    """Visual Q&A."""
    _setup(args)
    gkw = _gen_kwargs(args)

    result = question(
        args.image,
        args.question,
        expects=args.expects,
        stream=args.stream,
        **gkw,
    )

    if args.stream:
        _handle_stream(result)
    else:
        _print_result(result, args)


def cmd_perceive_cmd(args):
    """Compose a custom perception task with DSL nodes."""
    _setup(args)

    nodes = []
    if args.system_prompt:
        nodes.append(system(args.system_prompt))
    nodes.append(image(args.image))
    nodes.append(text(args.prompt))

    gkw = _gen_kwargs(args)
    result = perceive(
        *nodes,
        expects=args.expects,
        stream=args.stream,
        **gkw,
    )

    if args.stream:
        _handle_stream(result)
    else:
        _print_result(result, args)



def cmd_batch(args):
    """Process multiple images with the same task."""
    _setup(args)
    gkw = _gen_kwargs(args)

    images = []
    if args.images:
        for img_arg in args.images:
            images.extend(_resolve_images(img_arg))
    if args.from_file:
        with open(args.from_file) as f:
            images.extend(Path(line.strip()) for line in f if line.strip())

    if not images:
        print("Error: no images provided", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, img_path in enumerate(images):
        print(f"\n--- [{i+1}/{len(images)}] {img_path} ---")

        nodes = []
        if args.system_prompt:
            nodes.append(system(args.system_prompt))
        nodes.append(image(str(img_path)))
        nodes.append(text(args.prompt))

        result = perceive(
            *nodes,
            expects=args.expects,
            stream=False,
            **gkw,
        )

        _print_result(result, args)
        results.append({"image": str(img_path), "text": result.text,
                         "points": _serialize_annotations(result.points) if result.points else []})

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved {len(results)} results to {args.output}")


def cmd_parse(args):
    """Parse raw model output to extract annotations."""
    raw = args.text
    if args.text == "-":
        raw = sys.stdin.read()

    if args.mode == "points":
        points = extract_points(raw, expected=args.type)
        for p in points:
            _print_annotation(p)
    elif args.mode == "segments":
        segments = parse_text(raw)
        print(json.dumps(segments, indent=2))
    elif args.mode == "strip":
        print(strip_tags(raw))


def cmd_annotate(args):
    """Create annotated image examples for in-context learning."""
    _setup(args)

    # Parse annotations from JSON string
    annotations = json.loads(args.annotations)
    example = annotate_image(args.image, annotations)
    print(json.dumps(example, indent=2, default=str))


def cmd_models(args):
    """List available models."""
    _setup(args)
    try:
        import httpx
        from perceptron import settings
        s = settings()
        base = (s.base_url or "https://api.perceptron.inc").rstrip("/")
        api_key = s.api_key or os.environ.get("PERCEPTRON_API_KEY", "")
        resp = httpx.get(f"{base}/v1/models", headers={"Authorization": f"Bearer {api_key}"}, timeout=15)
        resp.raise_for_status()
        for m in resp.json().get("data", []):
            owned = m.get("owned_by", "")
            print(f"  {m['id']:<40} {owned}")
    except Exception as e:
        print(f"Error listing models: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_config_show(args):
    """Show current configuration."""
    _setup(args)
    from perceptron import settings
    s = settings()
    print(f"Provider:  {s.provider or '(default)'}")
    print(f"Model:     {s.model or '(default)'}")
    print(f"API Key:   {'***' + s.api_key[-8:] if s.api_key and len(s.api_key) > 8 else '(set)' if s.api_key else '(not set)'}")
    print(f"Base URL:  {s.base_url or '(default)'}")
    print(f"Timeout:   {s.timeout}s")
    print(f"\nSDK version: {perceptron.__version__}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Perceptron Vision CLI — powered by the Python SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s detect photo.jpg --classes person,car
  %(prog)s detect ./frames/ --classes forklift --pixels --format json
  %(prog)s caption scene.png --style detailed --stream
  %(prog)s ocr document.png --prompt "Extract the table"
  %(prog)s ocr receipt.jpg --output markdown
  %(prog)s question scene.jpg "How many people?" --expects point
  %(prog)s perceive frame.png --prompt "Find safety violations" --expects box
  %(prog)s batch --images img1.jpg img2.jpg --prompt "Count objects" --output results.json
  %(prog)s parse --mode points "<point_box mention=\\"car\\">(100,200) (300,400)</point_box>"
  %(prog)s models
  %(prog)s config
""",
    )

    # Global options
    parser.add_argument("--api-key", default=None, help="Perceptron API key")
    parser.add_argument("--provider", default=None, help="Provider (perceptron, fal, ...)")
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--temperature", type=float, default=None, help="Sampling temperature")
    parser.add_argument("--max-tokens", type=int, default=None, help="Max output tokens")

    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    # --- detect ---
    p = sub.add_parser("detect", help="Object detection with bounding boxes/points/polygons")
    p.add_argument("image", help="Image path/URL or directory")
    p.add_argument("--classes", default=None, help="Comma-separated classes to detect")
    p.add_argument("--expects", default="box", choices=["box", "point", "polygon"],
                   help="Output geometry type (default: box)")
    p.add_argument("--pixels", action="store_true", help="Also show pixel coordinates")
    p.add_argument("--stream", action="store_true", help="Stream output")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- caption ---
    p = sub.add_parser("caption", help="Image captioning")
    p.add_argument("image", help="Image path/URL or directory")
    p.add_argument("--style", default="concise", choices=["concise", "detailed"])
    p.add_argument("--expects", default="text", choices=["text", "box", "point", "polygon"],
                   help="Grounding type (default: text)")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- ocr ---
    p = sub.add_parser("ocr", help="Text extraction (OCR)")
    p.add_argument("image", help="Image path/URL or directory")
    p.add_argument("--prompt", default=None, help="Custom extraction prompt")
    p.add_argument("--output", default="text", choices=["text", "html", "markdown"],
                   help="Output format (default: text)")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- question ---
    p = sub.add_parser("question", help="Visual Q&A")
    p.add_argument("image", help="Image path/URL")
    p.add_argument("question", help="Question to ask")
    p.add_argument("--expects", default="text", choices=["text", "box", "point", "polygon"],
                   help="Output type (default: text)")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- perceive ---
    p = sub.add_parser("perceive", help="Custom perception task with DSL")
    p.add_argument("image", help="Image path/URL")
    p.add_argument("--prompt", required=True, help="Task prompt")
    p.add_argument("--system-prompt", default=None, help="System prompt")
    p.add_argument("--expects", default="text", choices=["text", "box", "point", "polygon"])
    p.add_argument("--stream", action="store_true")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- batch ---
    p = sub.add_parser("batch", help="Batch process images with same prompt")
    p.add_argument("--images", nargs="+", help="Image paths/URLs or directories")
    p.add_argument("--from-file", default=None, help="File with one image path per line")
    p.add_argument("--prompt", required=True, help="Prompt to apply")
    p.add_argument("--system-prompt", default=None, help="System prompt")
    p.add_argument("--expects", default="text", choices=["text", "box", "point", "polygon"])
    p.add_argument("--output", "-o", default=None, help="Save results JSON to file")
    p.add_argument("--format", "-f", default="text", choices=["text", "json"])

    # --- parse ---
    p = sub.add_parser("parse", help="Parse raw model output for annotations")
    p.add_argument("text", nargs="?", default="-", help="Raw text (or '-' for stdin)")
    p.add_argument("--mode", default="points", choices=["points", "segments", "strip"],
                   help="Parse mode: extract points, full segments, or strip tags")
    p.add_argument("--type", default=None, choices=["point", "box", "polygon"],
                   help="Filter to specific annotation type")

    # --- models ---
    sub.add_parser("models", help="List available models")

    # --- config ---
    sub.add_parser("config", help="Show current SDK configuration")

    args = parser.parse_args()

    cmds = {
        "detect": cmd_detect,
        "caption": cmd_caption,
        "ocr": cmd_ocr,
        "question": cmd_question,
        "perceive": cmd_perceive_cmd,
        "batch": cmd_batch,
        "parse": cmd_parse,
        "models": cmd_models,
        "config": cmd_config_show,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
