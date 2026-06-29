#!/usr/bin/env python3
"""Validate dialogue onboarding, event cards, and multi-agent conflict scaffolding."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def join_terms(parts: list[tuple[str, ...]]) -> list[str]:
    return ["".join(item) for item in parts]


DIALOGUE_FILE = ROOT / "examples" / "real-dialogue-flows.md"
LOW_INFO_FILE = ROOT / "examples" / "low-information-report.md"
MAGIC_REGRESSION_FILE = ROOT / "examples" / "magic-score-regression.md"
FIRST_RESPONSE_FILE = ROOT / "references" / "first-response-protocol.md"
EVENT_FILE = ROOT / "references" / "era-event-timeline-2008-2026.md"
AGENT_FILE = ROOT / "references" / "agent-simulation-stack.md"
GRAMMAR_FILE = ROOT / "references" / "life-fork-grammar.md"
ARCHETYPE_FILE = ROOT / "references" / "life-archetype-library.md"
TENSION_FILE = ROOT / "references" / "archetype-tension-axes.md"
MAGIC_FILE = ROOT / "references" / "magic-score-rubric.md"
VERDICT_FILE = ROOT / "references" / "verdict-rewrite-patterns.md"
SKILL_FILE = ROOT / "SKILL.md"
QUALITY_FILE = ROOT / "references" / "report-quality-rubric.md"
DELIVERY_FILE = ROOT / "templates" / "delivery-pack.md"
OPENAI_YAML_FILE = ROOT / "agents" / "openai.yaml"
ONBOARDING_FILE = ROOT / "references" / "onboarding-question-flow.md"

USER_FACING_SAMPLE_FILES = [
    ROOT / "templates" / "life-fork-report.md",
    ROOT / "examples" / "city-choice-beijing.md",
    ROOT / "examples" / "system-career-choice.md",
    ROOT / "examples" / "study-abroad-no-return.md",
    ROOT / "examples" / "stable-job-left.md",
]

LEGACY_USER_REPORT_TERMS = join_terms(
    [
        ("三", "条", "人", "生", "线"),
        ("真", "实", "人", "生", "线"),
        ("未", "选", "择", "人", "生", "线"),
        ("变", "量", "显", "影"),
        ("当", "年", "没", "看", "见", "的", "变", "量"),
        ("附", "录", "：", "依", "据", "、", "审", "计", "、", "事", "件", "表", "、", "置", "信", "度"),
        ("置", "信", "度", "与", "待", "补", "信", "息"),
        ("质", "量", "评", "分", "与", "回", "写", "记", "录"),
        ("使", "用", "到", "的", "时", "代", "事", "件"),
        ("依", "据", "摘", "要"),
        ("多", "视", "角", "审", "计"),
        ("图", "文", "标", "题"),
        ("传", "播", "资", "产"),
        ("口", "播"),
    ]
)

GRAMMAR_TERMS = [
    "## 1. 岔路动作层",
    "留下",
    "离开",
    "回流",
    "错过",
    "延迟",
    "押注",
    "撤退",
    "转向",
    "被迫中断",
    "## 2. 系统切换层",
    "大城市 vs 小城市",
    "海外 vs 国内",
    "市场化 vs 体制 / 国企",
    "## 3. 自我叙事断裂层",
    "## 4. 事件冲击层",
    "## 5. 三种结果层",
    "## 6. 可回收资产层",
    "## 8. 语法回归表",
]

ARCHETYPE_TERMS = [
    "城市折返",
    "海外未竟",
    "AI 错过窗口",
    "买房绑定",
    "体制安全",
    "大厂牌桌",
    "旧公司离开",
    "小城回流",
    "创业未尝试",
    "隐藏不甘",
    "典型判词",
    "事件冲击",
    "幻想校正",
    "可回收资产",
    "混合原型处理",
    "原型命中要求",
]

TENSION_TERMS = [
    "熟悉环境 vs 陌生竞争",
    "安全感 vs 可见度",
    "国际身份 vs 中文舒适区",
    "作品资产 vs 收藏观察",
    "张力轴组合示例",
    "禁止退化",
]

MAGIC_TERMS = [
    "首屏判词击中",
    "不可替换",
    "隐秘交换",
    "具体事件承托",
    "18-20 分",
    "任一维度低于 4 分",
    "替换测试",
    "交换测试",
    "事件测试",
]

FLOW_MARKERS = [
    "## 流程 A：如果当年去了北京",
    "## 流程 B：如果留学后没有回国",
    "## 流程 C：如果那年没买房",
    "## 流程 D：如果当年进了体制",
    "## 流程 E：如果没有离开上一家公司",
    "## 流程 F：如果早点做 AI",
]

EVENT_FIELDS = [
    "时间范围：",
    "影响人群：",
    "影响变量：",
    "适用岔路：",
    "影响机制：",
    "使用边界：",
    "待确认问题：",
]

EVENT_COVERAGE_TERMS = [
    "2008",
    "2016",
    "2020-2022",
    "2023-2026",
    "Brexit",
    "疫情",
    "互联网裁员",
    "AI",
    "签证",
    "地产",
    "留学大众化",
    "新零售",
    "内容合规",
    "微短剧",
    "大模型开源",
    "制造业出海遇到规则",
]

AGENT_ROLES = [
    "用户画像 Agent",
    "人生叙事 Agent",
    "职业路径 Agent",
    "资产现金流 Agent",
    "关系与家庭 Agent",
    "健康与能量 Agent",
    "事件检索 Agent",
    "时代事件 Agent",
    "反方审计 Agent",
    "交付编辑 Agent",
]

AGENT_OUTPUT_FIELDS = [
    "核心判断：",
    "最担心的风险：",
    "最支持哪条路径：",
    "需要反方审计的地方：",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def question_count(block: str) -> int:
    return len(re.findall(r"^\d+\.\s", block, flags=re.MULTILINE))


def validate_dialogue(errors: list[str]) -> None:
    text = read(DIALOGUE_FILE)

    for marker in FLOW_MARKERS:
        if marker not in text:
            fail(errors, f"dialogue file missing flow marker: {marker}")

    if text.count("Skill 处理：") < 6:
        fail(errors, "dialogue file should contain six concrete Skill handling blocks")

    required_dialogue_terms = [
        "材料有限",
        "事件冲击卡",
        "30 天实验",
        "回归评分",
        "HTML 首屏",
        "HTML 第二屏",
        "分叉图",
        "HTML 默认展开区",
        "质量评分",
        "4 周动作",
        "默认服务用户本人复盘",
        "原型回归映射",
        "Magic 回归映射",
        "判词替换测试",
    ]
    for term in required_dialogue_terms:
        if term not in text:
            fail(errors, f"dialogue file missing required behavior: {term}")

    front_text = text[: text.find("## 回归检查")]
    for social_term in join_terms([("小", "红", "书"), ("抖", "音"), ("口", "播"), ("传", "播", "资", "产")]):
        if social_term in front_text:
            fail(errors, f"dialogue default delivery contains social-output term: {social_term}")


def validate_first_response_protocol(errors: list[str]) -> None:
    text = read(FIRST_RESPONSE_FILE)
    onboarding = read(ONBOARDING_FILE)
    for term in (
        "## 问题预算",
        "一句话",
        "中等材料",
        "高材料",
        "0 个问题",
        "先交付中材料报告",
        "补充问题只用于升级报告",
        "首轮所有问题合计最多 3 个",
        "跳过这三个问题",
        "报告结尾",
    ):
        if term not in text:
            fail(errors, f"first-response protocol missing question-budget rule: {term}")
    for term in (
        "先交付报告",
        "3 个补充问题放在结尾",
        "立刻材料有限版运行",
        "问题前置只适用于一句话输入",
        "先交付，再校准",
    ):
        if term not in onboarding:
            fail(errors, f"onboarding flow missing report-first rule: {term}")


def validate_low_information_report(errors: list[str]) -> None:
    text = read(LOW_INFO_FILE)
    required_terms = [
        "材料有限版报告骨架",
        "内部识别",
        "张力轴识别",
        "原型识别",
        "Magic Score：18 / 20",
        "已知事实",
        "关键假设",
        "下面内容只用于生成，不进入用户版报告前台",
        "现在已知信息：有限",
        "一次选择，后来分出了三种结果",
        "现实结果：",
        "假设结果：",
        "回补结果：",
        "事件使用",
        "事件冲击卡",
        "30 天验证实验",
        "5 个补充问题",
        "最后提醒",
    ]
    for term in required_terms:
        if term not in text:
            fail(errors, f"low-information report missing required term: {term}")

    supplement_start = text.find("### 5 个补充问题")
    supplement_end = text.find("\n## ", supplement_start + 1) if supplement_start != -1 else -1
    supplement_block = text[supplement_start:supplement_end] if supplement_start != -1 and supplement_end != -1 else ""
    if question_count(supplement_block) != 5:
        fail(errors, "low-information report should contain exactly five supplement questions")

    action_start = text.find("### 30 天验证实验")
    action_end = text.find("底部判词", action_start)
    action_block = text[action_start:action_end] if action_start != -1 and action_end != -1 else ""
    for week in ("第 1 周", "第 2 周", "第 3 周", "第 4 周"):
        if week not in action_block:
            fail(errors, f"low-information report missing weekly action: {week}")

    for backend_term in ("报告质量评分", "回写记录", "交付判断：", "总分：29 / 35"):
        if backend_term in text:
            fail(errors, f"low-information report should not expose backend term: {backend_term}")

    for social_term in join_terms([("小", "红", "书"), ("抖", "音"), ("口", "播"), ("传", "播", "资", "产")]):
        if social_term in text:
            fail(errors, f"low-information report contains social-output term: {social_term}")


def event_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^####\s+(.+)$", text, flags=re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1).strip(), text[start:end]))
    return sections


def validate_events(errors: list[str]) -> None:
    text = read(EVENT_FILE)
    sections = event_sections(text)
    if len(sections) < 20:
        fail(errors, f"event timeline should contain at least 20 event cards, found {len(sections)}")

    for title, body in sections:
        for field in EVENT_FIELDS:
            if field not in body:
                fail(errors, f"event card missing {field} in {title}")

    for term in EVENT_COVERAGE_TERMS:
        if term not in text:
            fail(errors, f"event timeline missing coverage term: {term}")

    for section_heading in ("## 使用规则", "## 事件卡片格式", "## 阶段索引"):
        if section_heading not in text:
            fail(errors, f"event timeline missing section: {section_heading}")

    late_section_match = re.search(
        r"^### 2025-2026[\s\S]*?(?=^## 快速检索表)",
        text,
        flags=re.MULTILINE,
    )
    if late_section_match:
        late_section = late_section_match.group(0)
        early_ranges = re.findall(r"时间范围：(?:201\d|2020|2021|2022|2023|2024(?:-\d{4})?)", late_section)
        if early_ranges:
            fail(errors, f"2025-2026 section contains early event ranges: {', '.join(early_ranges)}")


def validate_agents(errors: list[str]) -> None:
    text = read(AGENT_FILE)
    for role in AGENT_ROLES:
        if role not in text:
            fail(errors, f"agent stack missing role: {role}")
    for field in AGENT_OUTPUT_FIELDS:
        if field not in text:
            fail(errors, f"agent stack missing fixed output field: {field}")
    for term in ("冲突摘要", "职业上限 vs 现金流承受", "城市机会 vs 家庭支持", "短期跃迁 vs 长期健康"):
        if term not in text:
            fail(errors, f"agent stack missing conflict scaffold: {term}")


def validate_grammar(errors: list[str]) -> None:
    text = read(GRAMMAR_FILE)
    for term in GRAMMAR_TERMS:
        if term not in text:
            fail(errors, f"life-fork grammar missing term: {term}")
    for term in ("去北京", "留学未回国", "买房 / 没买房", "进体制 / 市场化", "离开上一家公司", "2023 年认真做 AI"):
        if term not in text:
            fail(errors, f"grammar regression table missing topic: {term}")
    for field in ("事件锚点", "生活场景", "现实代价", "情绪代价", "误判点", "今日验证"):
        if field not in text:
            fail(errors, f"grammar event card missing field: {field}")


def validate_archetypes(errors: list[str]) -> None:
    text = read(ARCHETYPE_FILE)
    for term in ARCHETYPE_TERMS:
        if term not in text:
            fail(errors, f"life archetype library missing term: {term}")

    tension = read(TENSION_FILE)
    for term in TENSION_TERMS:
        if term not in tension:
            fail(errors, f"tension axes missing term: {term}")

    magic = read(MAGIC_FILE)
    for term in MAGIC_TERMS:
        if term not in magic:
            fail(errors, f"magic score rubric missing term: {term}")

    verdict = read(VERDICT_FILE)
    for term in ("判词四件套", "替换测试", "弱判词与强判词", "失败判词"):
        if term not in verdict:
            fail(errors, f"verdict rewrite patterns missing term: {term}")

    regression = read(MAGIC_REGRESSION_FILE)
    for term in ("小城回流", "创业未尝试", "留出样本目的", "20 / 20"):
        if term not in regression:
            fail(errors, f"magic regression example missing term: {term}")

    first_response = read(FIRST_RESPONSE_FILE)
    for term in ("首轮响应协议", "首轮最多问 3 个问题", "用户拒绝填表时", "材料有限版首屏要求"):
        if term not in first_response:
            fail(errors, f"first response protocol missing term: {term}")


def validate_skill_links(errors: list[str]) -> None:
    text = read(SKILL_FILE)
    required_links = [
        "references/life-fork-grammar.md",
        "references/first-response-protocol.md",
        "references/archetype-tension-axes.md",
        "references/life-archetype-library.md",
        "references/verdict-rewrite-patterns.md",
        "references/magic-score-rubric.md",
        "references/onboarding-question-flow.md",
        "references/era-event-timeline-2008-2026.md",
        "references/agent-simulation-stack.md",
        "examples/real-dialogue-flows.md",
        "examples/low-information-report.md",
        "examples/magic-score-regression.md",
        "scripts/validate_dialogue_event_agent_flow.py",
        "scripts/validate_magic_score.py",
        "scripts/validate_skill_package.py",
    ]
    for link in required_links:
        if link not in text:
            fail(errors, f"SKILL.md missing workflow link: {link}")
    for link in ("references/event-shock-engine.md", "references/anti-generic-writing-rules.md"):
        if link not in text:
            fail(errors, f"SKILL.md missing event-shock link: {link}")


def validate_openai_yaml(errors: list[str]) -> None:
    if not OPENAI_YAML_FILE.exists():
        fail(errors, "agents/openai.yaml missing")
        return
    text = read(OPENAI_YAML_FILE)
    required_terms = [
        'display_name: "人生岔路模拟栈"',
        'short_description: "用事件冲击和三种结果，把如果当年问题复盘成可保存报告"',
        "$life-fork-simulation-stack",
        "HTML 用户报告",
        "事件冲击卡",
        "30 天验证实验",
        "allow_implicit_invocation: true",
    ]
    for term in required_terms:
        if term not in text:
            fail(errors, f"agents/openai.yaml missing term: {term}")
    for forbidden in join_terms([("小", "红", "书"), ("抖", "音"), ("口", "播"), ("P", "D", "F"), ("HTML", " Report")]):
        if forbidden in text:
            fail(errors, f"agents/openai.yaml should not include old/default-mixed term: {forbidden}")


def validate_user_facing_samples(errors: list[str]) -> None:
    for path in USER_FACING_SAMPLE_FILES:
        text = read(path)
        for term in LEGACY_USER_REPORT_TERMS:
            if term in text:
                fail(errors, f"{path.relative_to(ROOT)} contains legacy user-report term: {term}")


def validate_delivery_quality_rules(errors: list[str]) -> None:
    quality = read(QUALITY_FILE)
    for term in (
        "30 天实验满分硬标准",
        "Magic Score 附加门槛",
        "4 周动作完整",
        "第 1 周找真实人或真实材料",
        "第 4 周根据反馈决定加码、缩小或换题",
        "四周动作都能低风险启动，并能看见真实反馈",
    ):
        if term not in quality:
            fail(errors, f"quality rubric missing action-quality rule: {term}")

    forbidden_quality_phrases = [
        "每周都有动作、可保存记录和结果判断",
        "第几周计划",
    ]
    for phrase in forbidden_quality_phrases:
        if phrase in quality and "不要写" not in quality:
            fail(errors, f"quality rubric contains unguarded planning phrase: {phrase}")

    delivery = read(DELIVERY_FILE)
    for term in ("事件冲击卡", "第 1 周", "第 4 周", "30 天验证实验"):
        if term not in delivery:
            fail(errors, f"delivery template missing generic action term: {term}")
    if "北京同行" in delivery:
        fail(errors, "delivery template should not hardcode Beijing action copy")


def main() -> int:
    errors: list[str] = []
    validate_first_response_protocol(errors)
    validate_dialogue(errors)
    validate_low_information_report(errors)
    validate_events(errors)
    validate_agents(errors)
    validate_grammar(errors)
    validate_archetypes(errors)
    validate_skill_links(errors)
    validate_openai_yaml(errors)
    validate_user_facing_samples(errors)
    validate_delivery_quality_rules(errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
