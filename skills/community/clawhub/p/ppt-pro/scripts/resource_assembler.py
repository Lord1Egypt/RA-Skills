#!/usr/bin/env python3
"""资源组装工具 -- 从 planning JSON 自动提取并组装 [RESOURCES] 文本块

彻底消除 LLM 在 HTML 生成阶段"偷懒不读资源"的问题。
脚本机械化地读取 planning JSON 声明的所有资源文件，
拼装为 prompt-4-design.md 要求的 {{RESOURCES}} 文本块，
LLM 只需 view_file 即可获得完整上下文。

planning JSON 格式（两层资源绑定）:
  - 页面级: required_resources（layout / page_template / principles[]）
  - 卡片级: cards[].resource_ref（block / chart / principle）

用法:
  # 单页模式（输出到 stdout）
  python resource_assembler.py planning4.json --refs ./references/

  # 单页模式（输出到文件）
  python resource_assembler.py planning4.json --refs ./references/ -o resources-4.txt

  # 批量模式（为每个 planning JSON 生成对应 resources 文件）
  python resource_assembler.py planning/ --refs ./references/ -o resources/

SKILL.md Step 5c 集成方式:
  每页 HTML 生成前执行:
  python3 SKILL_DIR/scripts/resource_assembler.py \\
    OUTPUT_DIR/planning/planning{n}.json \\
    --refs SKILL_DIR/references \\
    -o OUTPUT_DIR/resources/resources-{n}.txt
  然后 view_file OUTPUT_DIR/resources/resources-{n}.txt 获取完整 [RESOURCES] 块。
"""

import argparse
import json
import sys
from pathlib import Path


def read_resource(refs_dir: Path, rel_path: str) -> str | None:
    """读取 references/ 下的资源文件，返回内容或 None。"""
    if not rel_path:
        return None
    clean = rel_path.removeprefix("references/")
    full = refs_dir / clean
    if full.is_file():
        return full.read_text(encoding="utf-8")
    alt = Path(rel_path)
    if alt.is_file():
        return alt.read_text(encoding="utf-8")
    return None


# 每页必须注入的全局资源（无论 planning JSON 是否声明）
GLOBAL_RESOURCES = [
    "blocks/card-styles.md",
    "layout-patterns.md",
]


def assemble_resources(planning_path: Path, refs_dir: Path) -> str:
    """读取 planning JSON 并组装 [RESOURCES] 文本块（两层格式 + 去重 + 全局注入）。"""
    planning = json.loads(planning_path.read_text(encoding="utf-8"))
    page_num = planning.get("page_number", "?")
    page_type = planning.get("page_type", "?")
    title = planning.get("title", "?")
    warnings = 0
    resource_count = 0  # 精确计数
    seen_paths: set[str] = set()  # 去重：记录已加载的资源路径

    def _load_unique(rel_path: str) -> str | None:
        """加载资源并去重。已加载过的返回 None。"""
        nonlocal resource_count
        clean = rel_path.removeprefix("references/")
        if clean in seen_paths:
            return None  # 已加载过，跳过
        seen_paths.add(clean)
        content = read_resource(refs_dir, rel_path)
        if content:
            resource_count += 1
        return content

    sections = []
    rr_raw = planning.get("required_resources", {})

    # 类型防御：required_resources 必须是 dict，不能是 list 或其他类型
    if not isinstance(rr_raw, dict):
        error_msg = (
            f"[ERROR] required_resources 类型错误: 必须是 JSON 对象 {{...}}，"
            f"不能是 {type(rr_raw).__name__}。"
            f"请修正后重新运行 planning_validator.py，再执行本脚本。"
        )
        print(error_msg, file=sys.stderr)
        sys.exit(2)

    rr = rr_raw

    # ── GLOBAL（每页必须注入的全局资源）─────────────────────────────────
    global_parts = []
    for gpath in GLOBAL_RESOURCES:
        content = _load_unique(gpath)
        if content:
            global_parts.append(f"--- {gpath} ---\n{content}")
    if global_parts:
        sections.append("=== GLOBAL_RESOURCES ===\n" + "\n\n".join(global_parts))

    # ── LAYOUT ──────────────────────────────────────────────────────────
    layout_path = rr.get("layout")
    if layout_path:
        content = _load_unique(layout_path)
        if content:
            sections.append(f"=== LAYOUT ({layout_path}) ===\n{content}")
        elif layout_path.removeprefix("references/") not in seen_paths:
            sections.append(f"=== LAYOUT ===\n[WARNING] 文件未找到: {layout_path}")
            warnings += 1
        # else: 已去重，静默跳过

    # ── PAGE_TEMPLATE ───────────────────────────────────────────────────
    pt_path = rr.get("page_template")
    if pt_path:
        content = _load_unique(pt_path)
        if content:
            sections.append(f"=== PAGE_TEMPLATE ({pt_path}) ===\n{content}")
        elif pt_path.removeprefix("references/") not in seen_paths:
            sections.append(f"=== PAGE_TEMPLATE ===\n[WARNING] 文件未找到: {pt_path}")
            warnings += 1

    # ── PAGE_PRINCIPLES ─────────────────────────────────────────────────
    principles = rr.get("principles", [])
    if principles:
        parts = []
        for p in principles:
            if not p:
                continue
            content = _load_unique(p)
            if content:
                parts.append(f"--- {p} ---\n{content}")
            elif p.removeprefix("references/") not in seen_paths:
                parts.append(f"--- {p} ---\n[WARNING] 文件未找到")
                warnings += 1
        if parts:
            sections.append("=== PAGE_PRINCIPLES ===\n" + "\n\n".join(parts))

    # ── CARD_RESOURCES ──────────────────────────────────────────────────
    cards = planning.get("cards", [])
    card_parts = []
    for idx, card in enumerate(cards):
        card_type = card.get("card_type", "unknown")
        chart_type = card.get("chart_type", "")
        card_style = card.get("card_style", "")

        card_header = (
            f"--- card[{idx}]: {card_type}"
            + (f" (chart_type={chart_type})" if chart_type else "")
            + (f" [{card_style}]" if card_style else "")
            + " ---"
        )

        ref = card.get("resource_ref", {})
        if not ref or not isinstance(ref, dict) or all(
            v is None or v == "" for v in ref.values()
        ):
            card_parts.append(card_header + "\n（无卡片级资源）")
            continue

        res_lines = []

        for key in ("block", "chart", "principle"):
            path = ref.get(key)
            if not path:
                continue
            content = _load_unique(path)
            if content:
                res_lines.append(f"[{key}] {path}\n{content}")
            elif path.removeprefix("references/") not in seen_paths:
                res_lines.append(f"[{key}] {path}\n[WARNING] 文件未找到")
                warnings += 1
            else:
                res_lines.append(f"[{key}] {path}\n（已在上方加载，此处去重跳过）")

        if res_lines:
            card_parts.append(card_header + "\n" + "\n\n".join(res_lines))
        else:
            card_parts.append(card_header + "\n（无卡片级资源）")

    if card_parts:
        sections.append("=== CARD_RESOURCES ===\n" + "\n\n".join(card_parts))

    # ── 组装最终输出 ────────────────────────────────────────────────────
    body = "\n\n".join(sections)

    header = (
        f"# [RESOURCES] 第 {page_num} 页: {title} ({page_type})\n"
        f"# 自动生成 -- resource_assembler.py\n"
        f"# ─────────────────────────────────────────────────\n"
    )
    stats = (
        f"\n# ─────────────────────────────────────────────────\n"
        f"# 资源文件: {resource_count} 个（去重后）"
    )
    if warnings > 0:
        stats += f", {warnings} 个文件未找到 (!!)"

    return header + "\n" + body + stats


def process_single(planning_path: Path, refs_dir: Path, output: str | None):
    """处理单个 planning JSON。"""
    result = assemble_resources(planning_path, refs_dir)
    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"OK: {planning_path.name} -> {out_path}", file=sys.stderr)
    else:
        print(result)


def process_batch(planning_dir: Path, refs_dir: Path, output_dir: str):
    """批量处理目录下所有 planning JSON。"""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(planning_dir.glob("planning*.json"))
    if not files:
        print(f"Error: No planning*.json files in {planning_dir}", file=sys.stderr)
        sys.exit(1)

    for f in files:
        num = f.stem.replace("planning", "")
        out_file = out_dir / f"resources-{num}.txt"
        result = assemble_resources(f, refs_dir)
        out_file.write_text(result, encoding="utf-8")
        print(f"OK: {f.name} -> {out_file}", file=sys.stderr)

    print(f"\nDone: {len(files)} files -> {out_dir}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Resource Assembler -- "
                    "从 planning JSON 自动组装 [RESOURCES] 文本块",
    )
    parser.add_argument(
        "path",
        help="单个 planning JSON 文件，或包含 planning*.json 的目录",
    )
    parser.add_argument(
        "--refs", required=True,
        help="references 目录路径（SKILL_DIR/references/）",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="输出路径（单页: 文件路径，批量: 目录路径）",
    )
    args = parser.parse_args()

    input_path = Path(args.path)
    refs_dir = Path(args.refs)

    if not refs_dir.is_dir():
        print(f"Error: references 目录不存在: {refs_dir}", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        process_single(input_path, refs_dir, args.output)
    elif input_path.is_dir():
        if not args.output:
            print("Error: 批量模式必须用 -o 指定输出目录", file=sys.stderr)
            sys.exit(1)
        process_batch(input_path, refs_dir, args.output)
    else:
        print(f"Error: 路径不存在: {input_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
