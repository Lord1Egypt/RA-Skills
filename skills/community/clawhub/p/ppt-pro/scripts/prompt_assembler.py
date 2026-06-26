#!/usr/bin/env python3
"""Prompt 组装工具 -- 将设计 Prompt 模板 + 所有动态内容一次性拼装为完整可用的 prompt

彻底消除 LLM 在 HTML 生成阶段 "忘记读资源 / 忘记注入变量" 的问题。
脚本机械化地完成所有占位符替换，LLM 只需 view_file 即可获得开箱即用的完整 prompt。

替换的占位符:
  {{STYLE_DEFINITION}}  <- style.json 的 CSS 变量定义
  {{PLANNING_JSON}}     <- planning{n}.json 的完整 JSON
  {{PAGE_CONTENT}}      <- planning{n}.json 中提取的内容摘要
  {{IMAGE_INFO}}        <- 配图信息（usage + path + placement）
  {{TECHNIQUE_CARDS}}   <- 从 director_command 提取技法牌编号，展开为完整 CSS 原子代码
  {{RESOURCES}}         <- resource_assembler 组装的完整资源块

用法:
  # 单页模式
  python prompt_assembler.py \\
    planning4.json \\
    --refs ./references/ \\
    --style style.json \\
    --image-dir images/ \\
    -o prompts-ready/prompt-ready-4.txt

  # 批量模式（为所有 planning JSON 生成完整 prompt）
  python prompt_assembler.py \\
    planning/ \\
    --refs ./references/ \\
    --style style.json \\
    --image-dir images/ \\
    -o prompts-ready/

SKILL.md Step 5c 集成方式:
  # 首页前批量组装（推荐）
  python3 SKILL_DIR/scripts/prompt_assembler.py \\
    OUTPUT_DIR/planning/ \\
    --refs SKILL_DIR/references \\
    --style OUTPUT_DIR/style.json \\
    --image-dir OUTPUT_DIR/images/ \\
    -o OUTPUT_DIR/prompts-ready/

  # 然后每页生成前只需:
  view_file OUTPUT_DIR/prompts-ready/prompt-ready-{n}.txt
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 复用 resource_assembler 的核心逻辑
from resource_assembler import assemble_resources


PROMPT_TEMPLATE_REL = "prompts/prompt-4-design.md"
TECHNIQUE_CARDS_REL = "technique-cards.md"


def extract_prompt_body(template_path: Path) -> str:
    """从 prompt-4-design.md 中提取 ```text ... ``` 之间的 prompt 正文。

    使用行级扫描而非正则，正确处理模板内嵌套的代码块（```html 等）。
    逻辑：找到 ```text 起始行后，向后扫描找到最后一个独占一行的 ``` 作为结束标记。
    """
    lines = template_path.read_text(encoding="utf-8").splitlines(keepends=True)

    # 1. 找 ```text 起始行
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "```text":
            start_idx = i + 1  # 内容从下一行开始
            break
    if start_idx is None:
        print("Error: prompt-4-design.md 中未找到 ```text 起始标记",
              file=sys.stderr)
        sys.exit(1)

    # 2. 从末尾向前找最后一个独占一行的 ```（这是外层代码块的结束标记）
    end_idx = None
    for i in range(len(lines) - 1, start_idx - 1, -1):
        if lines[i].strip() == "```":
            end_idx = i
            break
    if end_idx is None or end_idx <= start_idx:
        print("Error: prompt-4-design.md 中未找到 ``` 结束标记",
              file=sys.stderr)
        sys.exit(1)

    return "".join(lines[start_idx:end_idx])


# ── 技法牌展开（方案 B 核心） ──────────────────────────────────────────

def parse_technique_cards(refs_dir: Path) -> dict[str, str]:
    """解析 technique-cards.md，按 T1-T10 编号建立索引。

    返回 {"T1": "完整的 T1 章节文本", "T2": "...", ...}
    """
    tc_path = refs_dir / TECHNIQUE_CARDS_REL
    if not tc_path.is_file():
        print(f"Warning: 技法牌文件不存在: {tc_path}", file=sys.stderr)
        return {}

    text = tc_path.read_text(encoding="utf-8")
    # 按 ## T{N}. 标题分割
    sections = re.split(r"(?=^## T\d+\.)", text, flags=re.MULTILINE)

    cards = {}
    for section in sections:
        match = re.match(r"^## (T\d+)\.", section)
        if match:
            card_id = match.group(1)
            cards[card_id] = section.strip()
    return cards


def extract_technique_refs(director_command: str) -> list[str]:
    """从 director_command 文本中提取技法牌编号（T1-T10）。

    支持格式：
    - "T1 破界水印"
    - "T2"
    - "（T7 留白压迫）"
    - "用 T1+T3+T7 组合"
    """
    if not director_command:
        return []
    refs = re.findall(r"\bT(\d{1,2})\b", director_command)
    # 去重并保持顺序
    seen = set()
    result = []
    for num in refs:
        card_id = f"T{num}"
        if card_id not in seen and 1 <= int(num) <= 10:
            seen.add(card_id)
            result.append(card_id)
    return result


def build_technique_cards_block(
    planning: dict,
    technique_cards: dict[str, str],
) -> str:
    """根据 director_command 中的技法牌引用，组装展开后的技法牌文本块。

    输出格式：
    - 仅注入本页引用的 2-3 张牌的完整 CSS 原子代码和 ADAPT 参数
    - 未被引用的牌不注入（减少上下文噪音）
    """
    director_cmd = planning.get("director_command", "")
    refs = extract_technique_refs(director_cmd)

    if not refs:
        return ("（director_command 中未引用技法牌编号。"
                "请根据本页情绪自由选择 2-3 个技法，"
                "参考 technique-cards.md 的 T1-T10。）")

    parts = []
    parts.append(f"本页 director_command 引用了 {len(refs)} 张技法牌："
                 f" {' + '.join(refs)}")
    parts.append("")

    missing = []
    for card_id in refs:
        if card_id in technique_cards:
            parts.append(technique_cards[card_id])
            parts.append("")  # 空行分隔
        else:
            missing.append(card_id)

    if missing:
        parts.append(f"[WARNING] 以下技法牌未找到定义: {', '.join(missing)}")

    parts.append("### 组合规则")
    parts.append("1. 技法服务于 director_command 的情绪 -- "
                 "先感受画面，再选参数")
    parts.append("2. ADAPT 参数必须变异 -- "
                 "即使两页用了同一张牌，尺寸/位置/内容都必须不同")
    parts.append("3. 不要堆砌 -- 内容完整性（P0）永远优先于视觉效果（P3）")

    return "\n".join(parts)


# ── 风格定义构建 ────────────────────────────────────────────────────────

def build_style_definition(style_path: Path) -> str:
    """从 style.json 构建风格定义文本（灵魂描述 + CSS 变量）。

    输出三层信息：
    1. 灵魂层 -- mood_keywords / design_soul / variation_strategy（情绪锚点）
    2. 装饰基因层 -- decoration_dna（标志手法/禁止手法/推荐组合）
    3. 色值层 -- css_variables 映射为 :root 变量
    """
    style = json.loads(style_path.read_text(encoding="utf-8"))

    sections = []

    # 灵魂层
    soul_parts = []
    if style.get("design_soul"):
        soul_parts.append(f"**灵魂宣言**: {style['design_soul']}")
    if style.get("mood_keywords"):
        keywords = " / ".join(style["mood_keywords"])
        soul_parts.append(f"**情绪关键词**: {keywords}")
    if style.get("variation_strategy"):
        soul_parts.append(f"**跨页变奏策略**: {style['variation_strategy']}")
    if soul_parts:
        sections.append("### 风格灵魂（设计时的情绪锚点）\n" + "\n".join(soul_parts))

    # 装饰基因层
    dna = style.get("decoration_dna", {})
    if dna:
        dna_parts = []
        if dna.get("signature_move"):
            dna_parts.append(f"- **标志手法**: {dna['signature_move']}")
        if dna.get("forbidden"):
            dna_parts.append(f"- **禁止**: {', '.join(dna['forbidden'])}")
        if dna.get("recommended_combos"):
            combos = " | ".join(dna["recommended_combos"])
            dna_parts.append(f"- **推荐组合**: {combos}")
        if dna_parts:
            sections.append("### 装饰基因\n" + "\n".join(dna_parts))

    # CSS 变量层
    css_vars = style.get("css_variables", {})
    if css_vars:
        css_lines = [":root {"]
        var_map = {
            "bg_primary": "--bg-primary",
            "bg_secondary": "--bg-secondary",
            "card_bg_from": "--card-bg-from",
            "card_bg_to": "--card-bg-to",
            "card_border": "--card-border",
            "card_radius": "--card-radius",
            "text_primary": "--text-primary",
            "text_secondary": "--text-secondary",
            "accent_1": "--accent-1",
            "accent_2": "--accent-2",
            "accent_3": "--accent-3",
            "accent_4": "--accent-4",
        }
        for json_key, css_var in var_map.items():
            if json_key in css_vars:
                css_lines.append(f"  {css_var}: {css_vars[json_key]};")
        css_lines.append("}")
        sections.append("### CSS 变量\n```css\n" + "\n".join(css_lines) + "\n```")
    else:
        # 兼容旧格式 style.json（纯 CSS 变量平铺）
        sections.append("### 风格定义\n```json\n"
                        + json.dumps(style, indent=2, ensure_ascii=False)
                        + "\n```")

    return "\n\n".join(sections)


def build_planning_json(planning: dict) -> str:
    """将 planning JSON 格式化为可读文本。"""
    return "```json\n" + json.dumps(planning, indent=2, ensure_ascii=False) + "\n```"


def extract_page_content(planning: dict) -> str:
    """从 planning JSON 中提取页面内容摘要。"""
    parts = []

    title = planning.get("title", "")
    subtitle = planning.get("subtitle", "")
    if title:
        parts.append(f"页面标题: {title}")
    if subtitle:
        parts.append(f"副标题: {subtitle}")

    # 提取 cards 中的内容
    for idx, card in enumerate(planning.get("cards", [])):
        card_type = card.get("card_type", "unknown")
        card_title = card.get("title", "")
        content = card.get("content", "")
        data_points = card.get("data_points", [])

        card_desc = f"card[{idx}] ({card_type}): {card_title}"
        if content:
            card_desc += f"\n  内容: {content}"
        if data_points:
            for dp in data_points:
                if isinstance(dp, dict):
                    val = dp.get("value", "")
                    label = dp.get("label", "")
                    card_desc += f"\n  数据: {val} {label}"
                else:
                    card_desc += f"\n  数据: {dp}"
        parts.append(card_desc)

    return "\n\n".join(parts) if parts else "（策划稿中无额外内容字段）"


def build_image_info(planning: dict, image_dir: Path | None) -> str:
    """从 planning JSON 的 image 字段构建配图信息。"""
    image = planning.get("image", {})
    if not image:
        return ""

    usage = image.get("usage", "none")
    if usage == "none":
        return ""

    placement = image.get("placement", "")
    alt = image.get("alt", "")
    page_num = planning.get("page_number", "?")

    # 尝试在 image_dir 中查找该页的配图
    image_path = ""
    if image_dir and image_dir.is_dir():
        # 搜索匹配该页码的图片文件
        patterns = [
            f"*{page_num}*",           # 文件名含页码
            f"slide*{page_num}*",
            f"page*{page_num}*",
        ]
        for pattern in patterns:
            matches = list(image_dir.glob(pattern))
            if matches:
                # 取最新的一个
                image_path = str(sorted(matches)[-1].resolve())
                break

        # 如果按页码没找到，尝试按 alt 文本中的关键词查找
        if not image_path and alt:
            # 将 alt 转为文件名友好格式并搜索
            alt_key = alt.lower().replace(" ", "_")[:20]
            for f in image_dir.iterdir():
                if f.is_file() and alt_key in f.name.lower():
                    image_path = str(f.resolve())
                    break

    info_parts = [f"usage: {usage}"]
    if image_path:
        info_parts.append(f"path: {image_path}")
    else:
        info_parts.append("path: [待确认 -- image_dir 中未找到匹配的配图文件]")
    if placement:
        info_parts.append(f"placement: {placement}")
    if alt:
        info_parts.append(f"alt: {alt}")

    return " | ".join(info_parts)


# ── 主组装逻辑 ──────────────────────────────────────────────────────────

def assemble_prompt(
    planning_path: Path,
    refs_dir: Path,
    style_path: Path,
    image_dir: Path | None,
    technique_cards: dict[str, str],
) -> str:
    """组装完整的设计 prompt（所有占位符已替换）。"""

    # 1. 读取 prompt 模板
    template_path = refs_dir / PROMPT_TEMPLATE_REL
    if not template_path.is_file():
        print(f"Error: prompt 模板文件不存在: {template_path}", file=sys.stderr)
        sys.exit(1)
    prompt_body = extract_prompt_body(template_path)

    # 2. 读取 planning JSON
    planning = json.loads(planning_path.read_text(encoding="utf-8"))
    page_num = planning.get("page_number", "?")
    title = planning.get("title", "?")
    page_type = planning.get("page_type", "?")

    # 3. 构建各占位符内容
    style_def = build_style_definition(style_path)
    planning_json = build_planning_json(planning)
    page_content = extract_page_content(planning)
    image_info = build_image_info(planning, image_dir)
    tc_block = build_technique_cards_block(planning, technique_cards)
    resources = assemble_resources(planning_path, refs_dir)

    # 4. 替换占位符
    result = prompt_body
    result = result.replace("{{STYLE_DEFINITION}}", style_def)
    result = result.replace("{{PLANNING_JSON}}", planning_json)
    result = result.replace("{{PAGE_CONTENT}}", page_content)
    result = result.replace("{{TECHNIQUE_CARDS}}", tc_block)

    if image_info:
        result = result.replace("{{IMAGE_INFO}}", image_info)
    else:
        # 无配图时，用正则移除整个 IMAGE_INFO 相关段落
        result = re.sub(
            r"###\s*配图信息[^\n]*\n.*?\{\{IMAGE_INFO\}\}[^\n]*\n"
            r"(?:\n\([^)]*\)\n)?",  # 可选的括号说明行
            "### 配图信息\n无配图（usage=none）\n\n",
            result,
            flags=re.DOTALL,
        )
        # 兜底
        result = result.replace("{{IMAGE_INFO}}", "无配图（usage=none）")

    result = result.replace("{{RESOURCES}}", resources)

    # 5. 添加文件头
    header = (
        f"# ================================================================\n"
        f"# 完整设计 Prompt -- 第 {page_num} 页: {title} ({page_type})\n"
        f"# 自动生成 by prompt_assembler.py\n"
        f"# 所有占位符已替换，view_file 后直接用于 HTML 生成\n"
        f"# ================================================================\n\n"
    )

    return header + result


def process_single(
    planning_path: Path,
    refs_dir: Path,
    style_path: Path,
    image_dir: Path | None,
    technique_cards: dict[str, str],
    output: str | None,
):
    """处理单个 planning JSON。"""
    result = assemble_prompt(
        planning_path, refs_dir, style_path, image_dir, technique_cards,
    )

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"OK: {planning_path.name} -> {out_path}", file=sys.stderr)
    else:
        print(result)


def process_batch(
    planning_dir: Path,
    refs_dir: Path,
    style_path: Path,
    image_dir: Path | None,
    technique_cards: dict[str, str],
    output_dir: str,
):
    """批量处理目录下所有 planning JSON。"""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(planning_dir.glob("planning*.json"))
    if not files:
        print(f"Error: No planning*.json files in {planning_dir}",
              file=sys.stderr)
        sys.exit(1)

    for f in files:
        num = f.stem.replace("planning", "")
        out_file = out_dir / f"prompt-ready-{num}.txt"
        result = assemble_prompt(
            f, refs_dir, style_path, image_dir, technique_cards,
        )
        out_file.write_text(result, encoding="utf-8")
        print(f"OK: {f.name} -> {out_file}", file=sys.stderr)

    print(f"\nDone: {len(files)} prompt files -> {out_dir}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Assembler -- "
                    "组装完整设计 Prompt（模板 + 风格 + 策划 + 技法牌 + 资源 + 配图）",
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
        "--style", required=True,
        help="style.json 文件路径（OUTPUT_DIR/style.json）",
    )
    parser.add_argument(
        "--image-dir", default=None,
        help="配图目录路径（OUTPUT_DIR/images/）",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="输出路径（单页: 文件路径，批量: 目录路径）",
    )
    args = parser.parse_args()

    input_path = Path(args.path)
    refs_dir = Path(args.refs)
    style_path = Path(args.style)
    image_dir = Path(args.image_dir) if args.image_dir else None

    if not refs_dir.is_dir():
        print(f"Error: references 目录不存在: {refs_dir}", file=sys.stderr)
        sys.exit(1)
    if not style_path.is_file():
        print(f"Error: style.json 不存在: {style_path}", file=sys.stderr)
        sys.exit(1)
    if image_dir and not image_dir.is_dir():
        print(f"Warning: 配图目录不存在: {image_dir}", file=sys.stderr)
        image_dir = None

    # 预加载技法牌索引（全局一次）
    technique_cards = parse_technique_cards(refs_dir)
    if technique_cards:
        print(f"Loaded {len(technique_cards)} technique cards: "
              f"{', '.join(sorted(technique_cards.keys()))}",
              file=sys.stderr)
    else:
        print("Warning: 未加载到技法牌定义", file=sys.stderr)

    if input_path.is_file():
        process_single(
            input_path, refs_dir, style_path, image_dir,
            technique_cards, args.output,
        )
    elif input_path.is_dir():
        if not args.output:
            print("Error: 批量模式必须用 -o 指定输出目录", file=sys.stderr)
            sys.exit(1)
        process_batch(
            input_path, refs_dir, style_path, image_dir,
            technique_cards, args.output,
        )
    else:
        print(f"Error: 路径不存在: {input_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
