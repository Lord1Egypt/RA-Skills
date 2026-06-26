#!/usr/bin/env python3
"""
generate_ppt.py — Generate a .pptx from a validated slide plan JSON.

Two modes:
  --mode from-scratch   PptxGenJS — builds a fresh styled presentation
  --mode from-template  template_builder.py — fills content into an uploaded .pptx template
                        (replaces the old "print instructions" stub)

v4 improvements:
  - from-template mode now actually works via template_builder.py
  - visual_hint rendered as real charts / image placeholders via chart_builder.py
  - chart layout: when visual_hint is present, bullet list shifts left and chart fills right
  - all prior v3 fixes retained

Slide plan JSON schema:
{
  "title": "Presentation Title",
  "palette": { "primary": "1E2761", "secondary": "CADCFC", "accent": "FFFFFF" },
  "font_heading": "Calibri",
  "font_body": "Calibri",
  "slides": [
    {
      "index": 1,
      "layout": "title",
      "title": "Main Title",
      "subtitle": "Subtitle or tagline",
      "body": [],
      "notes": "Speaker notes",
      "visual_hint": ""
    },
    {
      "index": 5,
      "layout": "content",
      "title": "Sales Performance",
      "body": ["Revenue up 23%", "NPS score: 87"],
      "visual_hint": "chart:bar:Q1=120,Q2=145,Q3=98,Q4=200 title=Quarterly Revenue"
    }
  ]
}

visual_hint formats:
  chart:bar:<label>=<val>,...          — bar chart
  chart:line:<label>=<val>,...         — line chart
  chart:pie:<label>=<val>,...          — pie chart
  chart:doughnut:<label>=<val>,...     — doughnut chart
  icon:<name>                          — colored accent icon placeholder
  image:<label>                        — gray image placeholder box
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path

# Import chart_builder from same directory
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from chart_builder import chart_to_js, visual_hint_to_js
    _HAS_CHART_BUILDER = True
except ImportError:
    _HAS_CHART_BUILDER = False

try:
    from style_renderers import get_renderer
    _HAS_STYLE_RENDERERS = True
except ImportError:
    _HAS_STYLE_RENDERERS = False


# ── Validation step ───────────────────────────────────────────────────────────

def run_validator(plan_path: str) -> tuple[str, list]:
    validator = os.path.join(_SCRIPT_DIR, "validator.py")
    if not os.path.exists(validator):
        print(json.dumps({"status": "warning", "message": "validator.py not found — skipping"}),
              file=sys.stderr)
        return plan_path, []

    validated_path = plan_path + ".validated.json"
    result = subprocess.run(
        [sys.executable, validator, "--plan", plan_path, "--out", validated_path],
        capture_output=True, text=True
    )

    corrections = []
    if result.stderr:
        try:
            report = json.loads(result.stderr)
            corrections = report.get("corrections", [])
            if corrections:
                print(json.dumps({
                    "status": "validation",
                    "corrections_count": len(corrections),
                    "corrections": corrections,
                }, ensure_ascii=False), file=sys.stderr)
        except json.JSONDecodeError:
            pass

    if result.returncode == 1:
        raise RuntimeError(f"Validation failed: {result.stderr}")

    if os.path.exists(validated_path):
        return validated_path, corrections
    return plan_path, corrections


# ── PptxGenJS script builder ──────────────────────────────────────────────────

def _title_bar(lines, title, subtitle, primary, secondary, accent, font_h, font_b):
    """Emit standard dark title bar for light slides."""
    lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 0, w: 10, h: 0.9, fill: {{ color: PRIMARY }}, line: {{ color: PRIMARY, width: 0 }} }});")
    lines.append(f"  slide.addText({json.dumps(title)}, {{")
    lines.append(f"    x: 0.4, y: 0, w: 9.2, h: 0.9, fontSize: 24, fontFace: FONT_H,")
    lines.append(f"    color: ACCENT, bold: true, valign: 'middle', margin: 0")
    lines.append(f"  }});")
    if subtitle:
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0.4, y: 0.95, w: 1.2, h: 0.05, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({json.dumps(subtitle)}, {{")
        lines.append(f"    x: 0.4, y: 1.0, w: 9.2, h: 0.45, fontSize: 14, fontFace: FONT_B,")
        lines.append(f"    color: '555555', italic: true")
        lines.append(f"  }});")


def _render_slide_legacy(lines, slide_data, primary, secondary, accent, font_h, font_b, has_visual, visual_lines):
    """Fallback renderer — original v4.2 corporate layout. Used when style_renderers.py is unavailable."""
    layout   = slide_data.get("layout", "content")
    title    = slide_data.get("title", "")
    subtitle = slide_data.get("subtitle", "")
    body     = slide_data.get("body", [])
    notes    = slide_data.get("notes", "")

    lines.append("{")
    lines.append("  const slide = pres.addSlide();")

    if layout == "title":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 4.8, w: 10, h: 0.825, fill: {{ color: ACCENT, transparency: 85 }}, line: {{ color: ACCENT, width: 0 }} }});")
        lines.append(f"  slide.addText({json.dumps(title)}, {{ x: 0.7, y: 1.6, w: 8.6, h: 1.6, fontSize: 44, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
        if subtitle:
            lines.append(f"  slide.addText({json.dumps(subtitle)}, {{ x: 0.7, y: 3.3, w: 8.6, h: 0.8, fontSize: 20, fontFace: FONT_B, color: SECONDARY, align: 'left' }});")
    elif layout == "section":
        lines.append(f"  slide.background = {{ color: PRIMARY }};")
        lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0.6, y: 2.4, w: 0.08, h: 1.0, fill: {{ color: SECONDARY }}, line: {{ color: SECONDARY, width: 0 }} }});")
        lines.append(f"  slide.addText({json.dumps(title)}, {{ x: 0.9, y: 2.2, w: 8.5, h: 1.3, fontSize: 36, fontFace: FONT_H, color: ACCENT, bold: true, align: 'left', valign: 'middle' }});")
    elif layout == "quote":
        lines.append(f"  slide.background = {{ color: SECONDARY }};")
        qt = body[0] if body else title
        lines.append(f"  slide.addText('\u201c', {{ x: 0.5, y: 0.2, w: 2, h: 1.5, fontSize: 96, fontFace: FONT_H, color: PRIMARY, bold: true }});")
        lines.append(f"  slide.addText({json.dumps(qt)}, {{ x: 1.0, y: 1.2, w: 8.0, h: 2.8, fontSize: 26, fontFace: FONT_H, color: PRIMARY, italic: true, align: 'center', valign: 'middle' }});")
    else:
        lines.append(f"  slide.background = {{ color: 'FFFFFF' }};")
        _title_bar(lines, title, subtitle, primary, secondary, accent, font_h, font_b)
        body_y = 1.55 if subtitle else 1.05
        body_h = round(5.425 - body_y - 0.2, 3)
        if body and has_visual:
            runs = [{"text": b, "options": {"bullet": True, "breakLine": True}} for b in body[:-1]]
            runs.append({"text": body[-1], "options": {"bullet": True}})
            lines.append(f"  slide.addText({json.dumps(runs)}, {{ x: 0.4, y: {body_y}, w: 4.4, h: {body_h}, fontSize: 15, fontFace: FONT_B, color: '2D2D2D', valign: 'top', paraSpaceAfter: 6 }});")
        elif body:
            runs = [{"text": b, "options": {"bullet": True, "breakLine": True}} for b in body[:-1]]
            runs.append({"text": body[-1], "options": {"bullet": True}})
            lines.append(f"  slide.addText({json.dumps(runs)}, {{ x: 0.5, y: {body_y}, w: 9.0, h: {body_h}, fontSize: 16, fontFace: FONT_B, color: '2D2D2D', valign: 'top', paraSpaceAfter: 6 }});")
        if visual_lines and layout not in ("title", "section", "quote"):
            lines.extend(visual_lines)
        if layout not in ("title", "section"):
            lines.append(f"  slide.addShape(pres.shapes.RECTANGLE, {{ x: 0, y: 5.425, w: 10, h: 0.2, fill: {{ color: PRIMARY, transparency: 70 }}, line: {{ color: PRIMARY, width: 0 }} }});")

    if notes:
        lines.append(f"  slide.addNotes({json.dumps(notes)});")
    lines.append("}")
    lines.append("")


def generate_pptxgenjs_script(plan: dict, output_path: str) -> str:
    palette    = plan.get("palette", {})
    primary    = palette.get("primary",   "1E2761")
    secondary  = palette.get("secondary", "CADCFC")
    accent     = palette.get("accent",    "FFFFFF")
    font_h     = plan.get("font_heading", "Calibri")
    font_b     = plan.get("font_body",    "Calibri")
    pres_title = plan.get("title",        "Presentation")
    slides     = plan.get("slides",       [])

    lines = []
    lines.append("const pptxgen = require('pptxgenjs');")
    lines.append("const pres = new pptxgen();")
    lines.append("pres.layout = 'LAYOUT_16x9';")
    lines.append(f"pres.title = {json.dumps(pres_title)};")
    lines.append(f"const PRIMARY   = '{primary}';")
    lines.append(f"const SECONDARY = '{secondary}';")
    lines.append(f"const ACCENT    = '{accent}';")
    lines.append(f"const FONT_H    = {json.dumps(font_h)};")
    lines.append(f"const FONT_B    = {json.dumps(font_b)};")
    lines.append("const makeShadow = () => ({ type: 'outer', blur: 8, offset: 3, angle: 135, color: '000000', opacity: 0.12 });")
    lines.append("")

    for slide_data in slides:
        layout      = slide_data.get("layout", "content")
        body        = slide_data.get("body", [])
        chart       = slide_data.get("chart")
        visual_hint = slide_data.get("visual_hint", "")

        # ── Resolve visual lines ──────────────────────────────────────────────
        visual_lines = []
        if _HAS_CHART_BUILDER:
            if chart:
                if body:
                    visual_lines = chart_to_js(
                        chart, "slide", x=5.1, y=1.05, w=4.7, h=4.3,
                        primary=primary, secondary=secondary)
                else:
                    visual_lines = chart_to_js(
                        chart, "slide", x=0.5, y=1.05, w=9.0, h=4.3,
                        primary=primary, secondary=secondary)
            elif visual_hint:
                if body:
                    visual_lines = visual_hint_to_js(
                        visual_hint, "slide", x=5.1, y=1.05, w=4.7, h=4.3,
                        primary=primary, secondary=secondary)
                else:
                    visual_lines = visual_hint_to_js(
                        visual_hint, "slide", x=0.5, y=1.05, w=9.0, h=4.3,
                        primary=primary, secondary=secondary)

        has_visual = bool(visual_lines)

        # ── Render slide via style renderer ───────────────────────────────────
        if _HAS_STYLE_RENDERERS:
            style_category = plan.get("style_category", "")
            renderer = get_renderer(style_category)
            pal_dict = {"primary": primary, "secondary": secondary, "accent": accent}
            font_dict = {"heading": font_h, "body": font_b}
            renderer(lines, slide_data, pal_dict, font_dict, has_visual, visual_lines)
        else:
            # Fallback: original inline corporate layout (backward compatible)
            _render_slide_legacy(lines, slide_data, primary, secondary, accent,
                                font_h, font_b, has_visual, visual_lines)

    lines.append(f"pres.writeFile({{ fileName: {json.dumps(output_path)} }})")
    lines.append(f"  .then(() => {{")
    lines.append(f"    console.log(JSON.stringify({{ status: 'ok', output: {json.dumps(output_path)}, slides: {len(slides)} }}));")
    lines.append(f"  }})")
    lines.append(f"  .catch(err => {{")
    lines.append(f"    process.stderr.write(JSON.stringify({{ status: 'error', message: err.message }}) + '\\n');")
    lines.append(f"    process.exit(1);")
    lines.append(f"  }});")

    return "\n".join(lines)


def run_pptxgenjs(script_content: str) -> dict:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(script_content)
            tmp_path = f.name

        result = subprocess.run(["node", tmp_path], capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        pass
            return {"status": "ok", "stdout": result.stdout.strip()}
        else:
            err_msg = result.stderr.strip() or result.stdout.strip()
            for line in err_msg.split("\n"):
                if line.strip().startswith("{"):
                    try:
                        return json.loads(line.strip())
                    except json.JSONDecodeError:
                        pass
            return {"status": "error", "message": err_msg[:500]}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def run_template_builder(template_path: str, plan_path: str, output_path: str) -> dict:
    """Delegate to template_builder.py for template-based generation."""
    builder = os.path.join(_SCRIPT_DIR, "template_builder.py")
    if not os.path.exists(builder):
        return {
            "status": "error",
            "message": "template_builder.py not found in scripts/. Cannot use from-template mode."
        }

    result = subprocess.run(
        [sys.executable, builder,
         "--template", template_path,
         "--plan", plan_path,
         "--output", output_path],
        capture_output=True, text=True, timeout=120
    )

    output_lines = result.stdout.strip().split("\n")
    for line in output_lines:
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass

    if result.returncode != 0:
        return {"status": "error", "message": result.stderr[:500] or result.stdout[:500]}

    return {"status": "ok", "output": output_path}


# ── Patch helper ─────────────────────────────────────────────────────────────

def apply_patch(plan_path: str, patch_json: str) -> str:
    """
    Apply a partial slide patch to an existing plan.
    Patch format: {"slides": [{"index": 3, "title": "New", "body": [...]}]}
    Slides in the patch replace matching index in the plan. Non-matching slides
    are left untouched. Returns path to the patched plan (temp file).
    """
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    patch = json.loads(patch_json)
    patch_slides = {s["index"]: s for s in patch.get("slides", []) if "index" in s}

    if not patch_slides:
        return plan_path

    for i, slide in enumerate(plan.get("slides", [])):
        idx = slide.get("index")
        if idx in patch_slides:
            # Merge: patch fields overwrite, unpatched fields preserved
            for key, val in patch_slides[idx].items():
                slide[key] = val
            plan["slides"][i] = slide

    patched_path = plan_path + ".patched.json"
    with open(patched_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "status": "patched",
        "slides_updated": list(patch_slides.keys()),
        "output": patched_path,
    }, ensure_ascii=False), file=sys.stderr)

    return patched_path


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate PPTX from a slide plan JSON")
    parser.add_argument("--plan",     required=True, help="Path to slide plan JSON (raw or pre-validated)")
    parser.add_argument("--output",   required=True, help="Output .pptx path")
    parser.add_argument("--mode",     choices=["from-scratch", "from-template"], default="from-scratch")
    parser.add_argument("--template", help="Path to .pptx template (required for from-template mode)")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--patch",    help='JSON string to patch specific slides, e.g. \'{"slides":[{"index":3,"title":"New Title"}]}\'')
    args = parser.parse_args()

    plan_path   = args.plan
    output      = os.path.abspath(args.output)
    validated_tmp = None
    patched_tmp   = None

    try:
        # Apply patch if provided
        if args.patch:
            plan_path = apply_patch(plan_path, args.patch)
            if plan_path != args.plan:
                patched_tmp = plan_path

        # Validate
        if not args.skip_validation:
            plan_path, corrections = run_validator(plan_path)
            if plan_path != args.plan and plan_path != patched_tmp:
                validated_tmp = plan_path

        if args.mode == "from-scratch":
            with open(plan_path, "r", encoding="utf-8") as f:
                plan = json.load(f)
            script = generate_pptxgenjs_script(plan, output)
            result = run_pptxgenjs(script)
            print(json.dumps(result, ensure_ascii=False))

        elif args.mode == "from-template":
            if not args.template:
                print(json.dumps({
                    "status": "error",
                    "message": "from-template mode requires --template <path-to-template.pptx>"
                }))
                sys.exit(1)
            result = run_template_builder(
                template_path=os.path.abspath(args.template),
                plan_path=plan_path,
                output_path=output,
            )
            print(json.dumps(result, ensure_ascii=False))

    finally:
        if validated_tmp and os.path.exists(validated_tmp):
            os.unlink(validated_tmp)
        if patched_tmp and os.path.exists(patched_tmp):
            os.unlink(patched_tmp)


if __name__ == "__main__":
    main()
