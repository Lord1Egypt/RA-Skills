#!/usr/bin/env python3
"""火一五流程图 — 一站式 CLI。

最常见用法
==========

    # 从 YAML 规格生成 PNG（默认 modern 风格）
    python3 scripts/create-flow-chart.py -i examples/architecture.yaml -o /tmp/arch.png

    # 泳道图（真·PlantUML）
    python3 scripts/create-flow-chart.py -i examples/swimlane.yaml -o /tmp/lane.svg

    # 泳道图（Mermaid subgraph 风格，不需要 Java）
    python3 scripts/create-flow-chart.py -i examples/swimlane_mermaid.yaml -o /tmp/lane.svg

    # 直接渲染 Mermaid 源码
    python3 scripts/create-flow-chart.py -i flow.mmd -o /tmp/flow.pdf --style dark

    # 同时导出多种格式
    python3 scripts/create-flow-chart.py -i spec.yaml -o /tmp/arch.png \
        --export-formats svg,pdf,mmd --style xiaohongshu

    # 导出 draw.io 源文件（可本地编辑）
    python3 scripts/create-flow-chart.py -i spec.yaml -o /tmp/arch.drawio \
        --export-formats png,svg,pdf

    # draw.io 精美主题
    python3 scripts/create-flow-chart.py -i spec.yaml -o /tmp/arch.png \
        --theme modern --font "Microsoft YaHei" --shadow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flowchart_core import parse, to_mermaid, to_plantuml, to_dot, to_drawio, FlowChart  # noqa: E402
from flowchart_render import render  # noqa: E402
from styles import get_style, list_styles, to_mermaid_init_directive, to_plantuml_skinparam  # noqa: E402


def _pick_engine(fc: FlowChart, explicit: str = "auto") -> str:
    if explicit != "auto":
        return explicit
    if fc.diagram_type in ("swimlane", "plantuml_raw"):
        return "plantuml"
    if fc.diagram_type == "dot_raw":
        return "dot"
    return "mermaid"


def _generate_source(fc: FlowChart, engine: str, style, theme: str = "modern",
                     font_family: str = None, shadow: bool = True) -> str:
    if engine == "mermaid":
        return to_mermaid(
            fc,
            to_mermaid_init_directive(style, diagram_type=fc.diagram_type),
            style=style,
        )
    if engine == "plantuml":
        return to_plantuml(fc, to_plantuml_skinparam(style))
    if engine == "dot":
        return to_dot(fc, style=style)
    if engine == "drawio":
        return to_drawio(fc, style=style, theme=theme, font_family=font_family,
                         shadow=shadow)
    raise ValueError(f"未知 engine {engine}")


def _hex_to_rgb_tuple(hex_color: str):
    h = (hex_color or "#000000").lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _ansi_bg(hex_color: str) -> str:
    r, g, b = _hex_to_rgb_tuple(hex_color)
    return f"\033[48;2;{r};{g};{b}m"


def _ansi_fg(hex_color: str) -> str:
    r, g, b = _hex_to_rgb_tuple(hex_color)
    return f"\033[38;2;{r};{g};{b}m"


def _ansi_reset() -> str:
    return "\033[0m"


def _print_style_gallery() -> None:
    """终端打印所有风格的色卡（Truecolor ANSI）。"""
    import os
    no_color = os.environ.get("NO_COLOR") or not sys.stdout.isatty()
    all_styles = list_styles()
    print("huo15-flow-chart · 风格清单")
    print("=" * 68)
    for key, style in all_styles.items():
        # 风格名 + key
        name_line = f"  {style.name}  ({key})"
        print(name_line)
        # 色卡：fill / border / text / accent + palette
        swatches = [
            ("fill   ", style.primary_color),
            ("border ", style.primary_border_color),
            ("text   ", style.primary_text_color),
            ("accent ", style.accent_color),
            ("line   ", style.line_color),
            ("bg     ", style.background),
        ]
        for label, col in swatches:
            if no_color:
                print(f"    {label} {col}")
            else:
                # 用 fill 色做背景，text 色做前景，显示 3 个空格色块 + hex
                block = f"{_ansi_bg(col)}    {_ansi_reset()}"
                print(f"    {label} {block} {col}")
        if style.palette:
            if no_color:
                print(f"    palette  {'  '.join(style.palette)}")
            else:
                row = "    palette  "
                for col in style.palette:
                    row += f"{_ansi_bg(col)}   {_ansi_reset()} "
                row += "  " + "  ".join(style.palette)
                print(row)
        print()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="火一五流程图 / 架构图 / 泳道图 / 时序图等生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="支持的 type：flowchart / swimlane / swimlane_mermaid / sequence / state /\n"
               "           gantt / er / class / journey / pie /\n"
               "           architecture / c4_context / c4_container / mindmap",
    )
    ap.add_argument("--input", "-i", help="输入路径（yaml/json/mmd/puml/dot/drawio）"
                                          "；仅 --list-styles 时可省略")
    ap.add_argument("--input-format", default="auto",
                    choices=["auto", "yaml", "json", "mermaid", "plantuml", "dot"])
    ap.add_argument("--output", "-o",
                    help="输出路径（.svg/.png/.pdf/.mmd/.puml/.dot/.drawio）"
                         "；仅 --list-styles 时可省略")
    ap.add_argument("--export-formats", "--also", dest="export_formats", default="",
                    help="附加输出格式，逗号分隔。如 'svg,pdf,mmd,drawio'（旧名 --also 仍可用）")
    ap.add_argument("--export-dir", default="",
                    help="源文件输出目录，默认与主输出同目录")
    ap.add_argument("--style", default="modern",
                    help=f"风格：{','.join(list_styles().keys())}（或中文别名）")
    ap.add_argument("--theme", default="modern",
                    help="draw.io 主题：modern / dark / xiaohongshu / ocean 等（与 --style 对应）")
    ap.add_argument("--font", default="PingFang SC",
                    help="字体名称，默认 PingFang SC（Mac）/ Microsoft YaHei（Win）")
    ap.add_argument("--shadow", action="store_true",
                    help="为 draw.io 节点添加投影效果")
    ap.add_argument("--engine", default="auto",
                    choices=["auto", "mermaid", "plantuml", "dot", "drawio"])
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--background", help="背景色，默认用 style 的 background")
    ap.add_argument("--dump-source", action="store_true",
                    help="只打印生成的源码到 stdout，不调用渲染器")
    ap.add_argument("--no-pdf-fit", dest="pdf_fit", action="store_false",
                    default=True,
                    help="导出 PDF 时不自适应画布（默认自适应，整图一体不分页）")
    ap.add_argument("--scale", type=float, default=3.0,
                    help="高清倍率（PNG 默认 3.0 = 印刷级 ≈288DPI；视网膜屏 2.0；普屏 1.0）")
    ap.add_argument("--gallery", action="store_true",
                    help="把同一张输入用全部 10 种风格渲染成一张对比大图")
    ap.add_argument("--gallery-styles", default="",
                    help="限制 gallery 中展示的风格（逗号分隔）")
    ap.add_argument("--gallery-cols", type=int, default=3,
                    help="gallery 列数（默认 3）")
    ap.add_argument("--list-styles", action="store_true",
                    help="打印所有可用风格 + palette 色卡，然后退出")
    args = ap.parse_args()

    # 列出风格（无需输入输出）
    if args.list_styles:
        _print_style_gallery()
        return 0

    # 必填校验（非 list-styles 模式）
    if not args.input or not args.output:
        ap.error("需要提供 --input 和 --output（除非使用 --list-styles）")

    # 画廊模式
    if args.gallery:
        from gallery import build_gallery
        styles = [s for s in args.gallery_styles.split(",") if s.strip()] \
            if args.gallery_styles else None
        try:
            path = build_gallery(args.input, args.output, styles=styles,
                                 cols=args.gallery_cols)
            print(f"✓ {path}")
            return 0
        except Exception as e:
            print(f"[错误] gallery 渲染失败：{e}", file=sys.stderr)
            return 1

    try:
        fc = parse(args.input, hint=args.input_format)
    except Exception as e:
        print(f"[错误] 解析输入失败：{e}", file=sys.stderr)
        return 1

    try:
        style = get_style(args.style)
    except Exception as e:
        print(f"[错误] 风格无效：{e}", file=sys.stderr)
        return 1

    # 判断 engine
    engine = args.engine
    if engine == "auto":
        out_ext = Path(args.output).suffix.lower()
        if out_ext == ".drawio":
            engine = "drawio"
        else:
            engine = _pick_engine(fc, "auto")

    font_family = args.font
    shadow = args.shadow or True  # 默认开启软阴影（现代化质感）
    if args.dump_source and engine == "drawio":
        print(_generate_source(fc, engine, style, theme=args.theme,
                               font_family=font_family, shadow=shadow))
        return 0

    try:
        source = _generate_source(fc, engine, style, theme=args.theme,
                                  font_family=font_family, shadow=shadow)
    except Exception as e:
        print(f"[错误] 生成 {engine} 源码失败：{e}", file=sys.stderr)
        return 1

    background = args.background or style.background

    # 解析导出格式
    export_exts = []
    if args.export_formats:
        for e in args.export_formats.split(","):
            e = e.strip().lstrip(".")
            if e:
                export_exts.append(e)

    # 主输出 + 附加输出
    outputs = [args.output]
    for ext in export_exts:
        if ext == "drawio":
            ext = "drawio"
        base = Path(args.output)
        out_dir = Path(args.export_dir) if args.export_dir else base.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        outputs.append(str(out_dir / f"{base.stem}.{ext}"))

    successes, failures = [], []
    for path in outputs:
        try:
            final = render(source, path, engine=engine,
                           width=args.width, height=args.height,
                           background=background,
                           pdf_fit=args.pdf_fit,
                           scale=args.scale)
            successes.append(final)
        except Exception as e:
            failures.append((path, str(e)))

    for f in successes:
        print(f"✓ {f}")
    for path, msg in failures:
        print(f"✗ {path}: {msg}", file=sys.stderr)

    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
