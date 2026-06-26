from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 确保可以找到本地模块（纯Skill执行，使用绝对路径）
sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_drawio import export_drawio
from export_excalidraw import export_excalidraw
from export_html import export_html_viewer
from export_integrity import ExportIntegrityError
from export_mermaid import export_mermaid
from export_svg import export_svg, export_svg_auto, export_product_tree_svg, export_matrix_svg, export_capability_map_svg, export_swimlane_flow_svg
from generate import write_plan_output
from model import load_json, write_json
from prompt_generator import generate_prompt_file
from projection import build_narrative_projection, default_projection_path
from validate import validate_blueprint
from viewer import write_viewer_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="business-blueprint")
    parser.add_argument("--plan", help="Generate only the canonical blueprint JSON.")
    parser.add_argument("--project", help="Generate canonical projection JSON for downstream skills.")
    parser.add_argument(
        "--generate",
        help="Path to blueprint JSON. Generates free-flow HTML viewer.",
    )
    parser.add_argument("--edit", help="Refresh the static viewer for an existing blueprint.")
    parser.add_argument("--export", help="Export diagram artifacts. Default: free-flow SVG + HTML viewer.")
    parser.add_argument("--export-auto", help="Alias for --export (free-flow SVG + HTML viewer).")
    parser.add_argument("--html", help="Generate self-contained HTML viewer with inline SVG.")
    parser.add_argument("--validate", help="Validate a blueprint and print JSON results.")
    parser.add_argument(
        "--refine",
        help="Refine an existing blueprint with user feedback. "
             "Supply --feedback and --output. AI generates a structured diff which is "
             "applied to produce a new blueprint. Falls back to interactive stdin "
             "for the LLM call when no API is configured.",
    )
    parser.add_argument(
        "--feedback",
        help="Natural-language feedback for --refine.",
    )
    parser.add_argument(
        "--no-apply",
        action="store_true",
        help="With --refine: write the diff but do not apply it to the blueprint.",
    )
    parser.add_argument("--from", dest="from_path", help="Source text or file path.")
    parser.add_argument("--output", help="Optional output path for projection generation.")
    parser.add_argument("--format", dest="export_format", default="svg",
                        help="Export format: svg (default: SVG + HTML viewer), drawio, excalidraw, mermaid.")
    _INDUSTRIES = ["common", "finance", "manufacturing", "retail", "cross-border-ecommerce"]
    parser.add_argument("--industry", default="common", choices=_INDUSTRIES,
                        help=f"Template pack name ({', '.join(_INDUSTRIES)}).")
    parser.add_argument("--theme", default="dark", choices=["light", "dark"],
                        help="Color theme for HTML output (default: dark).")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.plan:
        source_text = _read_source_text(args.from_path)
        # 如果 --from 未提供且存在 stdin 数据，则从 stdin 读取
        if not source_text and not args.from_path and not sys.stdin.isatty():
            source_text = sys.stdin.read()
        if not source_text.strip():
            print("Error: --plan requires source text. Provide it via --from <text> or pipe from stdin.", file=sys.stderr)
            print("Example: business-blueprint --plan output.json --from \"My requirements here\"", file=sys.stderr)
            return 1
        write_plan_output(Path(args.plan), source_text, args.industry, Path.cwd())
        return 0

    if args.project:
        blueprint_path = Path(args.project)
        projection = build_narrative_projection(
            load_json(blueprint_path),
            blueprint_path=blueprint_path,
        )
        output_path = Path(args.output) if args.output else default_projection_path(blueprint_path)
        write_json(output_path, projection)
        return 0

    if args.generate:
        blueprint_path = Path(args.from_path or "solution.blueprint.json")
        viewer_path = Path(args.generate)
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=viewer_path.with_name("solution.handoff.json"),
            patch_path=viewer_path.with_name("solution.patch.jsonl"),
        )
        # Also generate self-contained HTML viewer with inline SVG
        html_path = viewer_path.with_name("solution.viewer.html")
        export_html_viewer(load_json(blueprint_path), html_path, theme=args.theme)
        return 0

    if args.edit:
        blueprint_path = Path(args.edit)
        viewer_path = blueprint_path.with_suffix(".viewer.html")
        write_viewer_package(
            blueprint_path=blueprint_path,
            viewer_path=viewer_path,
            handoff_path=blueprint_path.with_name("solution.handoff.json"),
            patch_path=blueprint_path.with_name("solution.patch.jsonl"),
        )
        return 0

    if args.export:
        blueprint_path = Path(args.export)
        blueprint = load_json(blueprint_path)
        export_dir = blueprint_path.with_name("solution.exports")
        export_dir.mkdir(parents=True, exist_ok=True)
        html_path = blueprint_path.parent / f"{blueprint_path.stem}.html"
        fmt = args.export_format or "svg"
        try:
            generate_prompt_file(blueprint, export_dir, theme=args.theme, fmt=fmt)
            if fmt == "svg":
                export_svg_auto(blueprint, export_dir / "solution.svg", theme=args.theme)
                export_html_viewer(blueprint, html_path, theme=args.theme)
            elif fmt == "drawio":
                export_drawio(blueprint, export_dir / "solution.drawio")
            elif fmt == "excalidraw":
                export_excalidraw(blueprint, export_dir / "solution.excalidraw")
            elif fmt == "mermaid":
                export_mermaid(blueprint, export_dir / "solution.mermaid.md")
            else:
                print(f"Unknown format: {fmt}. Supported: svg (default), drawio, excalidraw, mermaid", file=sys.stderr)
                return 1
        except ExportIntegrityError as exc:
            print(json.dumps(exc.to_payload(), ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        return 0

    if args.export_auto:
        blueprint_path = Path(args.export_auto)
        blueprint = load_json(blueprint_path)
        stem = blueprint_path.stem
        export_dir = blueprint_path.parent / f"{stem}.exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        html_path = blueprint_path.parent / f"{stem}.html"
        export_svg(blueprint, export_dir / "solution.auto.svg", theme=args.theme)
        export_html_viewer(blueprint, html_path, theme=args.theme)
        generate_prompt_file(blueprint, export_dir, theme=args.theme, fmt="auto-svg")
        return 0

    if args.html:
        blueprint_path = Path(args.from_path or "solution.blueprint.json")
        blueprint = load_json(blueprint_path)
        html_path = Path(args.html)
        html_path.parent.mkdir(parents=True, exist_ok=True)
        export_html_viewer(blueprint, html_path, theme=args.theme)
        generate_prompt_file(blueprint, html_path.parent, theme=args.theme, fmt="html")
        return 0

    if args.validate:
        payload = load_json(Path(args.validate))
        print(json.dumps(validate_blueprint(payload), ensure_ascii=False, indent=2))
        return 0

    if args.refine:
        from refine import refine_blueprint, stdout_llm_caller
        if not args.feedback:
            print("Error: --refine requires --feedback <text>.", file=sys.stderr)
            return 1
        if not args.output:
            print("Error: --refine requires --output <path>.", file=sys.stderr)
            return 1
        diff = refine_blueprint(
            blueprint_path=Path(args.refine),
            feedback=args.feedback,
            output_path=Path(args.output),
            llm_call=stdout_llm_caller,
            auto_apply=not args.no_apply,
        )
        ops = diff.get("operations", [])
        rationale = diff.get("rationale", "")
        print(f"Diff generated: {len(ops)} operations")
        if rationale:
            print(f"Rationale: {rationale}")
        return 0

    return 0


def _read_source_text(value: str | None) -> str:
    if not value:
        return ""
    # 内联文本通常较长且包含中文等非 ASCII 字符，不应当作文件路径处理。
    # Linux 文件名上限 255 字节，超过此值传给 stat() 会报 OSError: File name too long。
    # 策略：超过 255 字节直接当内联文本；短字符串才检查是否为文件路径。
    if len(value.encode("utf-8")) > 255:
        return value
    path = Path(value)
    if not path.exists():
        return value
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


if __name__ == "__main__":
    raise SystemExit(main())
