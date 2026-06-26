#!/usr/bin/env python3
"""策划稿 JSON 验证器 -- 在 Step 4 每页策划写入后立即校验

彻底消除 planning JSON 格式错误静默传播到下游的问题。
验证分两层：
  - 单页验证：字段完整性、值有效性、资源路径合法性
  - 跨页验证：布局多样性、visual_weight 节奏、image usage 多样性

用法:
  # 单页验证
  python planning_validator.py planning/planning4.json --refs references/

  # 全量验证（所有页面 + 跨页规则）
  python planning_validator.py planning/ --refs references/

  # 严格模式（warning 也视为失败，exit code = 1）
  python planning_validator.py planning/ --refs references/ --strict

SKILL.md 集成方式:
  Step 4 每页策划稿写入后立即执行:
  python3 SKILL_DIR/scripts/planning_validator.py \
    OUTPUT_DIR/planning/planning{n}.json \
    --refs SKILL_DIR/references
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# jsonschema 可选依赖（未安装时降级到内置验证逻辑）
try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False

# planning.schema.json 路径（相对于本脚本所在目录的父级 references/）
_SCHEMA_PATH = Path(__file__).parent.parent / "references" / "planning.schema.json"

# ── 合法枚举值 ──────────────────────────────────────────────────────────

VALID_PAGE_TYPES = {"cover", "toc", "section", "content", "end"}

VALID_CARD_TYPES = {
    # 基础
    "text", "data", "list", "process", "tag_cloud", "data_highlight",
    # 复合
    "timeline", "diagram", "quote", "comparison", "people",
    "image_hero", "matrix_chart",
}

VALID_CARD_STYLES = {
    "filled", "transparent", "outline", "accent", "glass", "elevated",
}

VALID_CHART_TYPES = {
    "progress_bar", "ring", "comparison_bar", "sparkline", "waffle",
    "kpi", "metric_row", "rating", "radar", "stacked_bar", "treemap",
    "timeline", "funnel",
}

VALID_IMAGE_USAGES = {
    "hero-blend", "atmosphere", "tint-overlay", "split-content",
    "card-inset", "card-header", "circle-badge", "none",
}

VALID_LAYOUT_HINTS = {
    "单一焦点", "50/50 对称", "非对称两栏", "三栏等宽", "主次结合",
    "英雄式", "顶部英雄式", "混合网格", "L 型", "T 型", "瀑布流",
}

COMPLEX_CARD_TYPES = {
    "timeline", "diagram", "quote", "comparison", "people",
    "image_hero", "matrix_chart",
}

CHART_REQUIRING_TYPES = {"data", "data_highlight"}


class ValidationResult:
    """收集验证结果。"""
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def summary(self, label: str = "") -> str:
        prefix = f"[{label}] " if label else ""
        lines = []
        for e in self.errors:
            lines.append(f"  ERROR: {prefix}{e}")
        for w in self.warnings:
            lines.append(f"  WARN:  {prefix}{w}")
        return "\n".join(lines)


def _schema_validate(planning: dict, r: ValidationResult, label: str) -> None:
    """使用 JSON Schema 做快速结构预检（jsonschema 可用时启用）。

    仅补充内置验证逻辑未覆盖的 Schema 层约束（如 if/then required）。
    不重复已有的细粒度检查。
    """
    if not _HAS_JSONSCHEMA or not _SCHEMA_PATH.is_file():
        return
    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft7Validator(schema)
        for err in validator.iter_errors(planning):
            # 只上报内置逻辑未覆盖的 schema 错误（避免重复）
            path = " -> ".join(str(p) for p in err.absolute_path) or "(root)"
            r.warn(f"[{label}] [Schema] {path}: {err.message}")
    except Exception:
        pass  # schema 验证失败不阻断内置逻辑


def validate_single(planning: dict, refs_dir: Path | None) -> ValidationResult:
    """验证单个 planning JSON 的字段完整性和值有效性。"""
    r = ValidationResult()
    pn = planning.get("page_number", "?")
    label = f"p{pn}"

    # JSON Schema 快速预检（可选，jsonschema 库存在时启用）
    _schema_validate(planning, r, label)

    # ── 顶层必填字段 ──────────────────────────────────────────────────
    required_top_hints = {
        "page_number": "整数，如 1",
        "page_type": f"字符串枚举，合法值: {VALID_PAGE_TYPES}",
        "title": "字符串，每页必须有标题，如 \"核心成果概览\"",
        "goal": "字符串，3秒目标描述",
        "cards": "数组，至少包含 1 个卡片对象",
        "visual_weight": "整数 2-9，表示视觉密度",
    }
    for field, hint in required_top_hints.items():
        if field not in planning:
            r.error(f"[{label}] 缺少必填字段: {field}（{hint}）")

    # ── page_type ─────────────────────────────────────────────────────
    pt = planning.get("page_type", "")
    if pt and pt not in VALID_PAGE_TYPES:
        r.error(f"[{label}] page_type 无效: '{pt}'（合法值: {VALID_PAGE_TYPES}）")

    # ── visual_weight ─────────────────────────────────────────────────
    vw = planning.get("visual_weight")
    if vw is not None:
        try:
            vw_num = int(vw)
            if vw_num < 2 or vw_num > 9:
                r.error(f"[{label}] visual_weight 超出范围 [2-9]: {vw_num}")
        except (ValueError, TypeError):
            r.error(f"[{label}] visual_weight 必须是整数: {vw}")

    # ── layout_hint ───────────────────────────────────────────────────
    lh = planning.get("layout_hint", "")
    if pt == "content" and not lh:
        r.error(f"[{label}] content 页必须有 layout_hint")
    if lh and lh not in VALID_LAYOUT_HINTS:
        r.warn(f"[{label}] layout_hint 不在已知列表中: '{lh}'（可能是自定义值）")

    # ── cards[] ────────────────────────────────────────────────────────
    cards = planning.get("cards", [])
    if pt == "content" and len(cards) < 2:
        r.warn(f"[{label}] content 页卡片数量偏少: {len(cards)}（推荐 3-5）")

    card_styles_used = set()
    for idx, card in enumerate(cards):
        # 类型防御：card 必须是 dict
        if not isinstance(card, dict):
            r.error(
                f"[{label}] cards[{idx}] 类型错误: 必须是 JSON 对象 {{...}}，"
                f"实际为 {type(card).__name__}（如 string）"
            )
            continue

        # card_type
        ct = card.get("card_type", "")
        if not ct:
            r.error(f"[{label}] cards[{idx}] 缺少 card_type")
        elif ct not in VALID_CARD_TYPES:
            r.error(f"[{label}] cards[{idx}] card_type 无效: '{ct}'")

        # card_style
        cs = card.get("card_style", "filled")
        if cs not in VALID_CARD_STYLES:
            r.error(f"[{label}] cards[{idx}] card_style 无效: '{cs}'")
        card_styles_used.add(cs)

        # chart_type（data/data_highlight 类型必须有）
        chart_type = card.get("chart_type")
        if ct in CHART_REQUIRING_TYPES and not chart_type:
            r.error(f"[{label}] cards[{idx}] {ct} 卡片必须指定 chart_type")
        if chart_type and chart_type not in VALID_CHART_TYPES:
            r.error(f"[{label}] cards[{idx}] chart_type 无效: '{chart_type}'")

        # resource_ref（复合类型必须有 block 引用）
        ref = card.get("resource_ref", {})
        if ct in COMPLEX_CARD_TYPES:
            block_ref = ref.get("block", "")
            if not block_ref:
                r.warn(f"[{label}] cards[{idx}] 复合类型 '{ct}' 建议填写 resource_ref.block")

        # resource_ref 路径存在性检查
        if refs_dir and isinstance(ref, dict):
            for key in ("block", "chart", "principle"):
                path = ref.get(key, "")
                if path:
                    clean = path.removeprefix("references/")
                    full_path = refs_dir / clean
                    if not full_path.is_file():
                        r.error(f"[{label}] cards[{idx}] resource_ref.{key} 文件不存在: {path}")

        # content 非空检查
        content = card.get("content", "")
        title = card.get("title", "")
        if not title and not content:
            r.warn(f"[{label}] cards[{idx}] 无标题且无内容")

    # card_style 多样性（仅统计有效 dict 卡片）
    valid_cards = [c for c in cards if isinstance(c, dict)]
    if pt == "content" and len(card_styles_used) < 2 and len(valid_cards) >= 2:
        r.error(f"[{label}] content 页至少需要 2 种 card_style（当前: {card_styles_used}）")

    # accent/elevated 限制
    accent_count = sum(1 for c in valid_cards if c.get("card_style") == "accent")
    elevated_count = sum(1 for c in valid_cards if c.get("card_style") == "elevated")
    if accent_count > 1:
        r.warn(f"[{label}] accent style 建议每页最多 1 个（当前: {accent_count}）")
    if elevated_count > 1:
        r.warn(f"[{label}] elevated style 建议每页最多 1 个（当前: {elevated_count}）")

    # ── 按 page_type 的内容质量校验 ───────────────────────────────────
    _validate_page_type_quality(planning, cards, pt, label, r)

    # ── required_resources ─────────────────────────────────────────────
    rr_raw = planning.get("required_resources", {})

    # 类型防御：required_resources 必须是 dict，不能是 list 或其他类型
    if not isinstance(rr_raw, dict):
        r.error(
            f"[{label}] required_resources 类型错误: 必须是 JSON 对象 {{...}}，"
            f"不能是 {type(rr_raw).__name__}（如 list）。"
            f"正确格式: {{\"layout\": \"references/layouts/hero-top.md\", "
            f"\"principles\": [\"references/principles/visual-hierarchy.md\"]}}"
        )
        # 类型错误时跳过后续对 rr 的字段访问，避免 AttributeError
        rr = {}
    else:
        rr = rr_raw

    if pt == "content":
        if not rr.get("layout"):
            r.error(f"[{label}] content 页 required_resources.layout 为空")
    elif pt in ("cover", "toc", "section", "end"):
        if not rr.get("page_template"):
            r.warn(f"[{label}] {pt} 页建议填写 required_resources.page_template（顶层字符串字段）")

    if not rr.get("principles"):
        r.warn(f"[{label}] required_resources.principles 为空（建议至少 1 条原则文件路径）")

    # required_resources 路径检查
    if refs_dir:
        for key in ("layout", "page_template"):
            path = rr.get(key, "")
            if path:
                clean = path.removeprefix("references/")
                full_path = refs_dir / clean
                if not full_path.is_file():
                    r.error(f"[{label}] required_resources.{key} 文件不存在: {path}")
        for p in rr.get("principles", []):
            if p:
                clean = p.removeprefix("references/")
                full_path = refs_dir / clean
                if not full_path.is_file():
                    r.error(f"[{label}] required_resources.principles 文件不存在: {p}")

    # ── image ──────────────────────────────────────────────────────────
    img = planning.get("image", {})
    usage = img.get("usage", "none")
    if usage not in VALID_IMAGE_USAGES:
        r.error(f"[{label}] image.usage 无效: '{usage}'")
    if usage != "none":
        if not img.get("prompt"):
            r.error(f"[{label}] image.usage={usage} 但 image.prompt 为空")
        if not img.get("placement"):
            r.warn(f"[{label}] image.placement 为空")

    # ── decoration_hints ───────────────────────────────────────────────
    dh = planning.get("decoration_hints", {})
    if pt == "content" and not dh:
        r.warn(f"[{label}] content 页 decoration_hints 为空")

    return r


def _is_brand_info_card(card: dict) -> bool:
    """检测卡片是否只是伪装成卡片的品牌/页脚信息。

    判定标准：无标题且内容只含姓名|日期|公司等元数据，
    不承载任何实质内容。
    """
    title = card.get("title", "").strip()
    content = card.get("content", "").strip()
    data_points = card.get("data_points", [])

    # 有标题的卡片不算纯品牌信息（除非标题也是空的）
    if title:
        return False

    # 有实质数据点的不算
    if data_points and any(len(str(dp)) > 15 for dp in data_points):
        return False

    # 内容只有短文本且包含常见品牌信息分隔符
    if content and len(content) < 60:
        separators = ["|", "/", "·", "--", "—"]
        if any(sep in content for sep in separators):
            # 进一步检测：内容中是否有日期模式或极短片段
            parts = [p.strip() for p in content.replace("|", "/").replace("·", "/").split("/")]
            # 如果每段都少于 15 字且没有动词/论点，大概率是品牌信息
            if all(len(p) < 15 for p in parts if p):
                return True

    return False


def _validate_page_type_quality(
    planning: dict, cards: list, pt: str, label: str, r: ValidationResult
) -> None:
    """按 page_type 检查卡片质量和数量。

    核心原则：品牌信息（演讲人/日期/公司）是页脚元素，不是卡片。
    只含品牌信息的卡片不计入有效内容卡片数。
    """
    # 统计有效内容卡片（排除非 dict 和纯品牌信息卡片）
    dict_cards = [c for c in cards if isinstance(c, dict)]
    content_cards = [c for c in dict_cards if not _is_brand_info_card(c)]
    brand_cards = [c for c in dict_cards if _is_brand_info_card(c)]

    if brand_cards:
        for idx, card in enumerate(cards):
            if _is_brand_info_card(card):
                r.warn(
                    f"[{label}] cards[{idx}] 疑似品牌信息伪装成卡片"
                    f"（内容: '{card.get('content', '')[:30]}...'）。"
                    f"品牌信息应写入 content_summary.supporting_points，"
                    f"不占用 cards[] 名额"
                )

    if pt == "cover":
        # 封面至少 2 张有效内容卡片
        if len(content_cards) < 2:
            r.error(
                f"[{label}] 封面页有效内容卡片不足: {len(content_cards)} 张"
                f"（最低 2 张。品牌信息不算卡片，应放入 supporting_points）"
            )
        # 封面必须有至少一个数据可视化或 quote
        has_visual = any(
            c.get("card_type") in ("data_highlight", "data", "quote")
            for c in content_cards
        )
        if not has_visual:
            r.warn(
                f"[{label}] 封面页缺少数据/金句卡片"
                f"（推荐 data_highlight/data/quote 作为视觉爆裂点）"
            )

    elif pt == "end":
        # 结束页至少 2 张有效内容卡片
        if len(content_cards) < 2:
            r.error(
                f"[{label}] 结束页有效内容卡片不足: {len(content_cards)} 张"
                f"（最低 2 张：要点总结 + 行动号召）"
            )
        # 结束页推荐有 list 卡片做要点回顾
        has_list = any(c.get("card_type") == "list" for c in content_cards)
        if not has_list:
            r.warn(
                f"[{label}] 结束页缺少 list 卡片"
                f"（推荐用 list 回顾 3-5 条核心要点）"
            )


def validate_cross_page(plannings: list[dict]) -> ValidationResult:
    """跨页验证：布局多样性、visual_weight 节奏、image 多样性。"""
    r = ValidationResult()

    content_pages = [p for p in plannings if p.get("page_type") == "content"]

    if len(content_pages) < 2:
        return r

    # ── 布局多样性 ─────────────────────────────────────────────────────
    # 规则 1: 相邻 content 页不能相同 layout_hint
    for i in range(len(content_pages) - 1):
        lh1 = content_pages[i].get("layout_hint", "")
        lh2 = content_pages[i + 1].get("layout_hint", "")
        pn1 = content_pages[i].get("page_number", "?")
        pn2 = content_pages[i + 1].get("page_number", "?")
        if lh1 and lh2 and lh1 == lh2:
            r.error(
                f"相邻 content 页 p{pn1} 和 p{pn2} 使用了相同布局: '{lh1}'"
            )

    # 规则 2: 任一 layout_hint 占比不超 30%
    layout_counter = Counter(
        p.get("layout_hint", "") for p in content_pages if p.get("layout_hint")
    )
    total_content = len(content_pages)
    for layout, count in layout_counter.items():
        ratio = count / total_content
        if ratio > 0.3:
            r.error(
                f"布局 '{layout}' 占比 {ratio:.0%}（{count}/{total_content}），"
                f"超过 30% 上限"
            )

    # ── visual_weight 节奏 ─────────────────────────────────────────────
    # 规则 1: 相邻页差不超过 5
    sorted_pages = sorted(plannings, key=lambda p: p.get("page_number", 0))
    for i in range(len(sorted_pages) - 1):
        vw1 = sorted_pages[i].get("visual_weight")
        vw2 = sorted_pages[i + 1].get("visual_weight")
        pn1 = sorted_pages[i].get("page_number", "?")
        pn2 = sorted_pages[i + 1].get("page_number", "?")
        if vw1 is not None and vw2 is not None:
            try:
                diff = abs(int(vw1) - int(vw2))
                if diff > 5:
                    r.error(
                        f"p{pn1}(vw={vw1}) -> p{pn2}(vw={vw2}) "
                        f"视觉重量差 {diff}，超过阈值 5"
                    )
            except (ValueError, TypeError):
                pass

    # 规则 2: 不连续 3 页高密度 (>= 7)
    for i in range(len(sorted_pages) - 2):
        vws = []
        for j in range(3):
            vw = sorted_pages[i + j].get("visual_weight")
            try:
                vws.append(int(vw))
            except (ValueError, TypeError):
                break
        if len(vws) == 3 and all(v >= 7 for v in vws):
            pn_start = sorted_pages[i].get("page_number", "?")
            r.warn(
                f"从 p{pn_start} 起连续 3 页高密度（vw={vws}），"
                f"建议中间插入低密度页"
            )

    # ── image usage 多样性（总页数 >= 8 时） ──────────────────────────────
    if len(plannings) >= 8:
        usages = [
            p.get("image", {}).get("usage", "none") for p in plannings
        ]
        content_usages = set(u for u in usages if u != "none")
        has_split = "split-content" in content_usages
        has_card_inset = "card-inset" in content_usages
        if not has_split:
            r.warn("全 PPT 中未使用 split-content 配图用法（>= 8 页时建议至少 1 次）")
        if not has_card_inset:
            r.warn("全 PPT 中未使用 card-inset 配图用法（>= 8 页时建议至少 1 次）")

    return r


def load_planning(path: Path) -> dict:
    """加载并解析 planning JSON，处理可能的格式问题。"""
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON 解析失败: {path.name} -> {e}", file=sys.stderr)
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description="Planning Validator -- 策划稿 JSON 格式与规则验证",
    )
    parser.add_argument(
        "path",
        help="单个 planning JSON 文件，或包含 planning*.json 的目录",
    )
    parser.add_argument(
        "--refs", default=None,
        help="references 目录路径（用于检查资源文件存在性，可选）",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="严格模式：warning 也视为失败",
    )
    args = parser.parse_args()

    input_path = Path(args.path)
    refs_dir = Path(args.refs) if args.refs else None

    if refs_dir and not refs_dir.is_dir():
        print(f"Warning: references 目录不存在: {refs_dir}", file=sys.stderr)
        refs_dir = None

    all_errors = 0
    all_warnings = 0
    plannings = []

    if input_path.is_file():
        files = [input_path]
    elif input_path.is_dir():
        files = sorted(input_path.glob("planning*.json"))
        if not files:
            print(f"Error: 目录中无 planning*.json: {input_path}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: 路径不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    # ── 单页验证 ────────────────────────────────────────────────────────
    print(f"验证 {len(files)} 个策划稿...\n", file=sys.stderr)

    for f in files:
        planning = load_planning(f)
        plannings.append(planning)
        result = validate_single(planning, refs_dir)
        pn = planning.get("page_number", "?")
        title = planning.get("title", "?")

        if result.errors or result.warnings:
            print(f"p{pn}: {title}", file=sys.stderr)
            print(result.summary(), file=sys.stderr)
            all_errors += len(result.errors)
            all_warnings += len(result.warnings)
        else:
            print(f"p{pn}: {title} -- OK", file=sys.stderr)

    # ── 跨页验证（仅目录模式） ──────────────────────────────────────────
    if len(plannings) > 1:
        print(f"\n跨页规则验证...", file=sys.stderr)
        cross = validate_cross_page(plannings)
        if cross.errors or cross.warnings:
            print(cross.summary(), file=sys.stderr)
            all_errors += len(cross.errors)
            all_warnings += len(cross.warnings)
        else:
            print("跨页规则 -- OK", file=sys.stderr)

    # ── 汇总 ────────────────────────────────────────────────────────────
    print(f"\n{'=' * 50}", file=sys.stderr)
    print(
        f"验证完成: {all_errors} errors, {all_warnings} warnings",
        file=sys.stderr,
    )

    if all_errors > 0:
        print("FAILED -- 请修正 errors 后再继续", file=sys.stderr)
        sys.exit(1)
    elif args.strict and all_warnings > 0:
        print("FAILED (strict) -- 请修正 warnings 后再继续", file=sys.stderr)
        sys.exit(1)
    else:
        print("PASSED", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
