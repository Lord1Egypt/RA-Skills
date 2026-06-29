#!/usr/bin/env python3
"""Validate HTML-first user-report behavior for the Life Fork skill."""

from __future__ import annotations

import re
import importlib.util
from pathlib import Path
from typing import Union


ROOT = Path(__file__).resolve().parents[1]


def join_terms(parts: list[tuple[str, ...]]) -> list[str]:
    return ["".join(item) for item in parts]


FORBIDDEN_KEY_FILE_TERMS = join_terms(
    [
        ("而", "非"),
        ("不", "是"),
        ("而", "是"),
        ("P", "D", "F", " Snapshot"),
    ]
)

OLD_VISIBLE_HTML_TERMS = join_terms(
    [
        ("Life", " Fork"),
        ("HTML", " Report"),
        ("Generated", " as"),
        ("MULTI",),
        ("signal", "-card"),
        ("visual", "-panel"),
        ("多", "视", "角", "对", "照"),
        ("影", "响", "这", "条", "路", "的", "时", "代", "事", "件"),
        ("多", "视", "角", "审", "计"),
        ("质", "量", "检", "查", "和", "修", "订", "记", "录"),
        ("质", "量", "评", "分"),
        ("报", "告", "质", "量"),
        ("回", "写", "记", "录"),
        ("依", "据", "摘", "要"),
        ("使", "用", "到", "的", "时", "代", "事", "件"),
        ("材", "料", "充", "分", "度", "与", "待", "补", "信", "息"),
        ("材", "料", "充", "分", "度", "："),
        ("当", "前", "材", "料", "："),
        ("事", "件", "来", "源", "："),
        ("每", "条", "路"),
        ("那", "条", "路"),
        ("没", "走", "的", "线"),
        ("安", "全", "边", "界"),
    ]
)

REQUIRED_FOLDED_TITLES = [
    "你当年没算进去的事",
    "哪些是你选的，哪些是时代推的",
    "我为什么会这样判断",
    "换几个角度看这件事",
    "那几年，外部环境也在变",
    "还有哪些信息会改写结论",
    "这份报告不能替你决定什么",
]

REQUIRED_REPORT_MARKERS = [
    "判词：",
    "看清：",
    "## 1. 你真正放不下的是什么",
    "## 2. 三种结果",
    "## 3. 事件冲击卡",
    "| 事件锚点 | 生活场景 | 现实代价 | 情绪代价 | 误判点 | 今天验证 |",
    "## 4. 哪些来自选择，哪些来自时代",
    "## 5. 30 天验证实验",
    "## 6. 继续解释：这份报告怎么判断",
]

OLD_REPORT_MARKERS = [
    "".join(("## 1. ", "一页", "摘要")),
    "".join(("## 3. ", "多视角", "结论")),
    "".join(("## 4. ", "事件", "影响")),
    "".join(("## 附录 A：", "Agent", " 详细输出")),
]

CALIBRATION_FIELDS = [
    "fork_action",
    "system_switch",
    "narrative_break",
    "primary_archetype",
    "secondary_archetype",
    "recoverable_assets",
    "event_shock_count",
    "magic_score",
]

ALLOWED_FORK_ACTIONS = [
    "留下",
    "离开",
    "回流",
    "错过",
    "延迟",
    "押注",
    "撤退",
    "转向",
    "被迫中断",
]

ALLOWED_ARCHETYPES = [
    "城市折返",
    "海外未竟",
    "AI 错过窗口",
    "买房绑定",
    "体制安全",
    "大厂牌桌",
    "旧公司离开",
    "小城回流",
    "创业未尝试",
]


def allowed_archetype(value: str) -> bool:
    if value in ALLOWED_ARCHETYPES:
        return True
    if value.startswith("临时原型：") and len(value.replace("临时原型：", "").strip()) >= 6:
        return True
    return False


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def has_class(text: str, class_name: str) -> bool:
    pattern = r'class="[^"]*\b' + re.escape(class_name) + r'\b[^"]*"'
    return re.search(pattern, text) is not None


def count_class(text: str, class_name: str) -> int:
    pattern = r'class="[^"]*\b' + re.escape(class_name) + r'\b[^"]*"'
    return len(re.findall(pattern, text))


def strip_tags(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", cleaned).strip()


def visible_page_text(text: str) -> str:
    cleaned = re.sub(r"<style[\s\S]*?</style>", " ", text)
    cleaned = re.sub(r"<script[\s\S]*?</script>", " ", cleaned)
    cleaned = re.sub(r"<!--[\s\S]*?-->", " ", cleaned)
    return strip_tags(cleaned)


def parse_calibration(text: str) -> dict[str, str]:
    match = re.search(r"<!--\s*life-fork-calibration\s*([\s\S]*?)-->", text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def front_report_html(text: str) -> str:
    start = text.find('<section class="screen hero-screen"')
    end = text.find('<section class="folded"', start)
    if start == -1 or end == -1:
        return ""
    return text[start:end]


def visible_text_blocks(html_text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"<(p|h[1-3])\b[^>]*>([\s\S]*?)</\1>", html_text):
        clean = strip_tags(match.group(2))
        if clean:
            blocks.append((match.group(1), clean))
    return blocks


def validate_front_reading_budget(path: Path, text: str, errors: list[str]) -> None:
    front = front_report_html(text)
    if not front:
        fail(f"{path} missing front report area before folded appendix", errors)
        return

    blocks = visible_text_blocks(front)
    total_chars = sum(len(block) for _, block in blocks)
    max_paragraph = max((len(block) for tag, block in blocks if tag == "p"), default=0)
    path_count = len(re.findall(r"<path\b", front))

    if total_chars > 9800:
        fail(f"{path} front report text is too dense: {total_chars} chars", errors)
    if max_paragraph > 190:
        fail(f"{path} front report paragraph too long: {max_paragraph} chars", errors)
    if len(blocks) > 130:
        fail(f"{path} front report has too many visible text blocks: {len(blocks)}", errors)
    if path_count < 4:
        fail(f"{path} front report should keep at least four SVG route paths", errors)
    if count_class(front, "result-card") != 3:
        fail(f"{path} front report should render exactly three result cards, found {count_class(front, 'result-card')}", errors)
    shock_count = count_class(front, "variable-chip-card")
    if shock_count < 4 or shock_count > 6:
        fail(f"{path} front report should render 4-6 event shock cards, found {shock_count}", errors)
    if count_class(front, "action-card") != 4:
        fail(f"{path} front report should keep exactly four weekly action cards", errors)
    if "<table" in front:
        fail(f"{path} front report should not contain visible tables", errors)


def action_card_texts(text: str) -> list[str]:
    return [
        strip_tags(match)
        for match in re.findall(r'<article class="action-card">([\s\S]*?)</article>', text)
    ]


def validate_action_cards(path: Path, text: str, errors: list[str]) -> None:
    cards = action_card_texts(text)
    if len(cards) != 4:
        fail(f"{path} should render exactly four weekly action cards, found {len(cards)}", errors)
        return

    vague_terms = ("多思考", "多了解", "保持关注", "提升自己", "长期坚持", "做规划")
    project_terms = ("每周都有动作", "产物", "判断门槛", "试运行", "交付")
    high_risk_terms = ("辞职", "离职", "搬家", "投资", "分手", "借钱", "贷款")
    action_verbs = ("找", "聊", "问", "写", "发", "记录", "整理", "做一次", "决定")
    observe_terms = ("看", "说出", "证明", "记录", "反馈", "最真实", "最累", "价值", "代价")

    for index, card in enumerate(cards, start=1):
        if len(card) < 28 or len(card) > 240:
            fail(f"{path} action card {index} length should stay readable: {len(card)}", errors)
        for term in vague_terms + project_terms + high_risk_terms:
            if term in card:
                fail(f"{path} action card {index} contains disallowed term: {term}", errors)
        if not any(verb in card for verb in action_verbs):
            fail(f"{path} action card {index} lacks a concrete action verb", errors)
        if not any(term in card for term in observe_terms):
            fail(f"{path} action card {index} lacks an observable result cue", errors)


def variable_card_texts(text: str) -> list[str]:
    return [
        strip_tags(match)
        for match in re.findall(r'<article class="variable-chip-card[^"]*">([\s\S]*?)</article>', text)
    ]


def validate_variable_cards(path: Path, text: str, errors: list[str]) -> None:
    front = front_report_html(text)
    cards = variable_card_texts(front)
    if len(cards) < 4 or len(cards) > 6:
        fail(f"{path} should render 4-6 event shock cards, found {len(cards)}", errors)
        return
    required_labels = ("事件锚点", "生活场景", "现实代价", "情绪代价", "误判点", "今天验证")
    anchor_pattern = re.compile(
        r"(?:19|20)\d{2}(?:-(?:19|20)\d{2})?|疫情|Brexit|毕业当年|选择当年|离开前\s*\d+\s*个月|中断[前后]\s*\d+(?:-\d+)?\s*(?:个月|年)"
    )
    weak_anchor_terms = ("当年", "作品资产", "现金流", "熟人支持", "身体恢复力", "安全感来源", "家庭支持", "时间窗口")
    for index, card in enumerate(cards, start=1):
        for label in required_labels:
            if label not in card:
                fail(f"{path} event shock card {index} missing label: {label}", errors)
        anchor_match = re.search(r"事件锚点\s*(.*?)\s*生活场景", card)
        anchor = anchor_match.group(1).strip() if anchor_match else ""
        if not anchor or not anchor_pattern.search(anchor):
            fail(f"{path} event shock card {index} anchor lacks year/stage cue: {anchor}", errors)
        for weak_term in weak_anchor_terms:
            if anchor == weak_term or anchor.startswith(f"{weak_term} "):
                fail(f"{path} event shock card {index} anchor is too generic: {anchor}", errors)
        compact = "".join(card.split())
        if len(compact) < 160:
            fail(f"{path} event shock card {index} is too thin: {len(compact)} chars", errors)
        if len(compact) > 720:
            fail(f"{path} event shock card {index} is too dense: {len(compact)} chars", errors)
    if "事件冲击" not in front:
        fail(f"{path} should label front cards as event shocks", errors)


def validate_key_files(errors: list[str]) -> None:
    key_files = [
        "SKILL.md",
        "README.md",
        "references/onboarding-question-flow.md",
        "references/first-response-protocol.md",
        "examples/real-dialogue-flows.md",
    ]
    for relative in key_files:
        text = read(relative)
        for term in FORBIDDEN_KEY_FILE_TERMS:
            if term in text:
                fail(f"{relative} contains forbidden term: {term}", errors)


def validate_real_dialogue(errors: list[str]) -> None:
    text = read("examples/real-dialogue-flows.md")
    required = [
        "流程 A：如果当年去了北京",
        "流程 B：如果留学后没有回国",
        "流程 C：如果那年没买房",
        "流程 D：如果当年进了体制",
        "流程 E：如果没有离开上一家公司",
        "流程 F：如果早点做 AI",
        "事件冲击卡",
        "30 天实验",
        "回归评分",
        "HTML 首屏",
        "回归检查",
    ]
    for item in required:
        if item not in text:
            fail(f"real dialogue file missing: {item}", errors)


def validate_html_document(path: Union[Path, str], text: str, errors: list[str]) -> None:
    if "life-fork-calibration" in text:
        fail(f"{path} leaks developer calibration into rendered HTML", errors)
    if not has_class(text, "hero-screen"):
        fail(f"{path} missing user-first hero screen", errors)
    if "人生岔路复盘报告" not in text:
        fail(f"{path} missing report name", errors)
    if 'class="verdict"' not in text:
        fail(f"{path} missing verdict sentence", errors)
    if 'class="hero-explain"' not in text:
        fail(f"{path} missing one-line hero explanation", errors)
    if "向下看" not in text:
        fail(f"{path} missing scroll cue", errors)
    if not has_class(text, "fork-screen") or "一次选择，后来分出了三种结果" not in text:
        fail(f"{path} missing fork screen", errors)
    if '<svg class="fork-map-svg"' not in text:
        fail(f"{path} missing fork-map-svg", errors)
    for route_class in ("past-route", "route-chosen", "route-unchosen", "route-repair"):
        if not re.search(r"<path[^>]+class=\"[^\"]*\b" + re.escape(route_class) + r"\b", text):
            fail(f"{path} missing SVG route path: {route_class}", errors)
    for label in ("现实结果", "假设结果", "回补结果"):
        if label not in text:
            fail(f"{path} missing result label: {label}", errors)
    front = front_report_html(text)
    if count_class(front, "result-card") != 3:
        fail(f"{path} should render three result cards in the default expanded area", errors)
    if text.count('class="action-card"') < 4:
        fail(f"{path} missing four weekly action cards", errors)
    validate_action_cards(path, text, errors)
    validate_variable_cards(path, text, errors)
    if text.count("<details>") < 4:
        fail(f"{path} missing folded detail sections", errors)
    if count_class(text, "audit-card") < 5:
        fail(f"{path} missing visual audit cards", errors)
    if count_class(text, "event-card") < 3:
        fail(f"{path} missing visual event cards", errors)
    if '<svg class="attribution-mini-svg"' not in text:
        fail(f"{path} missing attribution mini SVG in folded explanation", errors)
    if '<svg class="event-timeline-svg"' not in text:
        fail(f"{path} missing event timeline SVG in folded explanation", errors)
    visible_text = visible_page_text(text)
    for term in FORBIDDEN_KEY_FILE_TERMS:
        if term in visible_text:
            fail(f"{path} leaks forbidden phrasing into user-visible text: {term}", errors)
    for title in REQUIRED_FOLDED_TITLES:
        if title not in visible_text:
            fail(f"{path} missing user-facing folded title: {title}", errors)
    if count_class(text, "detail-intro") < 6:
        fail(f"{path} folded details should open with human-readable intro text", errors)
    for term in join_terms(
        [
            ("质", "量", "检", "查"),
            ("质", "量", "评", "分"),
            ("报", "告", "质", "量"),
            ("开", "发", "者", "内", "部", "检", "查"),
            ("Magic", " Score"),
            ("结", "构", "与", "交", "付", "评", "分"),
            ("开", "发", "者", "判", "断"),
            ("修", "订", "记", "录"),
            ("回", "写"),
            ("Agent",),
            ("审", "计"),
            ("矩", "阵"),
            ("变", "量"),
            ("事", "件", "库"),
            ("置", "信", "度"),
            ("材", "料", "充", "分", "度", "："),
            ("当", "前", "材", "料", "："),
            ("事", "件", "来", "源", "："),
            ("每", "条", "路"),
            ("那", "条", "路"),
            ("没", "走", "的", "线"),
            ("产", "物"),
            ("判", "断", "门", "槛"),
            ("Generated", " as"),
            ("依", "据", "摘", "要"),
            ("使", "用", "到", "的", "时", "代", "事", "件"),
            ("材", "料", "充", "分", "度", "与", "待", "补", "信", "息"),
            ("安", "全", "边", "界"),
        ]
    ):
        if term in visible_text:
            fail(f"{path} leaks backend term into user-visible text: {term}", errors)
    if "最后提醒" not in visible_text:
        fail(f"{path} missing user-facing final reminder", errors)
    validate_front_reading_budget(path, text, errors)
    hero_start = text.find('<section class="screen hero-screen">')
    hero_end = text.find("</section>", hero_start)
    hero = text[hero_start:hero_end] if hero_start != -1 and hero_end != -1 else ""
    for term in ("<table", "Agent", "变量", "置信度", "产物", "判断门槛", "评分", "回写"):
        if term in hero:
            fail(f"{path} leaks backend term into hero: {term}", errors)
    folded_start = text.find('<section class="folded">')
    front_text = text[:folded_start] if folded_start != -1 else text
    if "beijing" not in str(path) and "你补不回当年的北京" in front_text:
        fail(f"{path} leaks Beijing recovery copy into another topic", errors)
    for term in ("每周都有动作", "产物", "判断门槛", "交付", "回写", "Demo"):
        if term in front_text:
            fail(f"{path} leaks project-management term into front report: {term}", errors)
    if "每周都有动作、可保存记录和结果判断" in text:
        fail(f"{path} uses planning-style quality evidence", errors)
    if 'class="' + "".join(("hero", "-action")) + '"' in text:
        fail(f"{path} still shows first-screen action", errors)
    if "置信度：" in text[:2500]:
        fail(f"{path} shows confidence too early", errors)
    if 'class="' + "".join(("insight", "-card")) + '"' in text:
        fail(f"{path} still renders summary cards above the report", errors)
    if 'class="' + "".join(("view", "-card")) + '"' in text:
        fail(f"{path} still renders backend view cards above the report", errors)
    if 'class="' + "".join(("event", "-item")) + '"' in text:
        fail(f"{path} still renders event cards above the report", errors)
    for term in OLD_VISIBLE_HTML_TERMS:
        if term in text:
            fail(f"{path} contains old visible HTML term: {term}", errors)


def validate_rendered_html(errors: list[str]) -> None:
    html_paths = sorted((ROOT.parents[1] / "final-review").glob("life-fork-*-user-report-*/report.html"))
    if not html_paths:
        return
    for path in html_paths:
        validate_html_document(path, path.read_text(encoding="utf-8"), errors)


def load_renderer():
    renderer_path = ROOT / "scripts" / "render_html_report.py"
    spec = importlib.util.spec_from_file_location("life_fork_render_html_report", renderer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load renderer: {renderer_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_fresh_rendered_html(errors: list[str]) -> None:
    package_fixtures = [
        ROOT / "examples" / "html-render-fixture.md",
    ]
    report_paths = [
        path
        for path in package_fixtures
        if path.is_file()
    ] + sorted((ROOT.parents[1] / "final-review").glob("life-fork-*-user-report-*/report.md"))
    if not report_paths:
        fail("missing markdown render fixture for fresh HTML validation", errors)
        return
    renderer = load_renderer()
    for path in report_paths:
        markdown_text = path.read_text(encoding="utf-8")
        title = renderer.infer_title(markdown_text, path.stem)
        rendered = renderer.build_html(markdown_text, title)
        validate_html_document(f"{path} fresh-render", rendered, errors)


def validate_final_review_markdown(errors: list[str]) -> None:
    report_paths = sorted((ROOT.parents[1] / "final-review").glob("life-fork-*-user-report-*/report.md"))
    for path in report_paths:
        text = path.read_text(encoding="utf-8")
        calibration = parse_calibration(text)
        if not calibration:
            fail(f"{path} missing life-fork-calibration developer record", errors)
        else:
            for field in CALIBRATION_FIELDS:
                if not calibration.get(field):
                    fail(f"{path} calibration missing field: {field}", errors)
            for term in FORBIDDEN_KEY_FILE_TERMS:
                if term in "\n".join(calibration.values()):
                    fail(f"{path} calibration contains forbidden phrasing: {term}", errors)
            if not any(action in calibration.get("fork_action", "") for action in ALLOWED_FORK_ACTIONS):
                fail(f"{path} calibration fork_action lacks allowed grammar action", errors)
            primary = calibration.get("primary_archetype", "")
            secondary = calibration.get("secondary_archetype", "")
            if not allowed_archetype(primary):
                fail(f"{path} calibration primary_archetype is not allowed: {primary}", errors)
            if secondary and not allowed_archetype(secondary):
                fail(f"{path} calibration secondary_archetype is not allowed: {secondary}", errors)
            assets = [item.strip() for item in re.split(r"[,，、]", calibration.get("recoverable_assets", "")) if item.strip()]
            if len(assets) < 2:
                fail(f"{path} calibration should include at least two recoverable assets", errors)
            try:
                shock_count = int(calibration.get("event_shock_count", "0"))
            except ValueError:
                shock_count = 0
            if shock_count < 4 or shock_count > 6:
                fail(f"{path} calibration event_shock_count should be 4-6: {shock_count}", errors)
            try:
                magic_score = int(calibration.get("magic_score", "0"))
            except ValueError:
                magic_score = 0
            if magic_score < 18:
                fail(f"{path} calibration magic_score should be at least 18: {magic_score}", errors)
        for term in FORBIDDEN_KEY_FILE_TERMS:
            if term in text:
                fail(f"{path} contains forbidden phrasing: {term}", errors)
        for marker in REQUIRED_REPORT_MARKERS:
            if marker not in text:
                fail(f"{path} missing user-report marker: {marker}", errors)
        for marker in OLD_REPORT_MARKERS:
            if marker in text:
                fail(f"{path} contains old report marker: {marker}", errors)
        for backend_term in join_terms(
            [
                ("质", "量", "评", "分", "与", "回", "写", "记", "录"),
                ("交", "付", "判", "断", "："),
                ("回", "写", "记", "录", "："),
                ("总", "分", "：", "30 / 30"),
                ("总", "分", "：", "35 / 35"),
                ("## 6. ", "附", "录", "："),
                ("### ", "依", "据", "摘", "要"),
                ("### ", "使", "用", "到", "的", "时", "代", "事", "件"),
                ("### ", "置", "信", "度", "与", "待", "补", "信", "息"),
                ("材", "料", "充", "分", "度", "："),
                ("当", "前", "材", "料", "："),
                ("事", "件", "来", "源", "："),
                ("每", "条", "路"),
                ("那", "条", "路"),
                ("没", "走", "的", "线"),
                ("### ", "安", "全", "边", "界"),
                ("反", "方", "审", "计"),
                ("Agent",),
                ("可", "审", "计"),
                ("置", "信", "度", "："),
            ]
        ):
            if backend_term in text:
                fail(f"{path} exposes backend review term: {backend_term}", errors)


def main() -> int:
    errors: list[str] = []
    validate_key_files(errors)
    validate_real_dialogue(errors)
    validate_final_review_markdown(errors)
    validate_rendered_html(errors)
    validate_fresh_rendered_html(errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
