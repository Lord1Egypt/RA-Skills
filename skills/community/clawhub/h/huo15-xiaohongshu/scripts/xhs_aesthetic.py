"""火一五小红书"Allen 美学诊断"核心库。

来源：司志远（Allen）的小红书文案教学体系（三课 + 五技法 + 11 案例）。
区别于 v2.0 的"工程师视角"打分，这里是"哲学家视角"评估。

五个新维度
==========
1. **breath_score 留白度** — 句子是否有呼吸空间，让读者自己填情绪
2. **ai_speak_score AI 腔指数** — 汇报化 / 模板化 / 装腔词检测
3. **teach_vs_lead 教 vs 带** — "你应该" 还是 "你可以试试"
4. **resonance_score 共鸣度** — 共同记忆 vs 冷知识 / 装文化
5. **invitation_score 邀请语** — 互动是任务指令还是 "这里有个局"

每一项都是 0~10 分 + 命中样本 + 改写建议。

设计原则
========
- 每一项**单独可关**（disabled_checks 写进 profile/rules.json）
- 默认**只在用户开 Allen-mode 时生效**（避免误伤工程类干货号）
- 所有判断有可解释规则（不依赖 LLM），同时支持 LLM 增强
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# =====================================================================
# 数据加载
# =====================================================================


def _load_ai_speak_patterns() -> List[Dict[str, Any]]:
    p = _DATA_DIR / "ai_speak_patterns.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    out: List[Dict[str, Any]] = []
    for cat_name, cat in (data.get("categories") or {}).items():
        for item in cat.get("patterns") or []:
            out.append({
                "category": cat_name,
                "bad": item.get("bad", ""),
                "good": item.get("good", []),
                "why": item.get("why", ""),
            })
    return out


# =====================================================================
# 1. 留白度（Breath）
# =====================================================================


_NO_BREATH_MARKERS = [
    # 信息密度过高的特征
    re.compile(r"，[^，。！？\n]{30,}"),  # 一句话超 30 字不停顿
    re.compile(r"[1-9][\.、] ?\S+"),     # 显式编号「1. 2. 3.」 — 教科书结构
    re.compile(r"首先[^。]+。.*其次[^。]+。"),  # 首先...其次...
    re.compile(r"综上|综合来看|总结一下|总而言之"),
]


_BREATH_MARKERS = [
    # 留白的特征
    re.compile(r"^[—…]{2,}\s*$", re.MULTILINE),     # 单独一行省略号或破折号
    re.compile(r"\n\s*\n"),                          # 空行
    re.compile(r"[。？！]\s*$", re.MULTILINE),       # 短句独立成段
]


def score_breath(content: str) -> Tuple[int, List[str], List[str]]:
    """留白度 0~10。看句子能不能让读者停下来。"""
    if not content.strip():
        return 0, ["正文为空"], []

    issues: List[str] = []
    suggestions: List[str] = []
    score = 6

    # 长句过多
    long_phrases = sum(1 for ln in content.splitlines()
                       for _ in re.finditer(r"，[^，。！？\n]{30,}", ln))
    if long_phrases >= 3:
        score -= 2
        issues.append(f"有 {long_phrases} 处一句话超 30 字不停顿，信息密度过高（说明书感）")
        suggestions.append("把长句子在自然停顿处断开 — 一个意思一行")

    # 显式编号 1.2.3
    if len(re.findall(r"[1-9][\.、] ?\S+", content)) >= 3:
        score -= 1
        issues.append("出现 1. 2. 3. 显式编号 — 教科书结构，不像小红书的'松散感'")
        suggestions.append("把数字编号换成 emoji 项目符号或自然过渡（'还有'/'另外'/'对了'）")

    # 总分总
    if re.search(r"首先[^。]+。.*其次", content) or "综上" in content or "总而言之" in content:
        score -= 2
        issues.append("出现总分总结构关键词 — 论文腔，不是生活感")
        suggestions.append("改成'我把这天写下来'或者直接列散点，不要框")

    # 空行
    paragraphs = [p for p in content.split("\n\n") if p.strip()]
    blanks = content.count("\n\n")
    if paragraphs and blanks / max(1, len(paragraphs)) < 0.5:
        score -= 1
        issues.append("段间空行偏少，文字像挤在一起，没有呼吸口")
        suggestions.append("每 2~3 句之间加一个空行，让读者有眼睛能落的地方")

    # 加分项：关键句独立成段
    short_punch = sum(1 for ln in content.splitlines()
                      if 6 < len(ln.strip()) < 25 and ln.strip().endswith(("。", "！", "？", "—")))
    if short_punch >= 2:
        score += 1

    # 加分项：留白符号
    if re.search(r"^—{2,}\s*$|^…{2,}\s*$", content, re.MULTILINE):
        score += 1

    return max(0, min(10, score)), issues, suggestions


# =====================================================================
# 2. AI 腔指数（AI-speak）
# =====================================================================


def score_ai_speak(text: str) -> Tuple[int, List[str], List[str]]:
    """AI 腔检测 0~10（高分 = 没什么 AI 腔，低分 = AI 腔严重）。"""
    patterns = _load_ai_speak_patterns()
    if not patterns:
        return 7, [], []

    hits: List[Dict[str, Any]] = []
    for p in patterns:
        bad = p["bad"]
        if not bad:
            continue
        if bad in text:
            hits.append(p)

    issues: List[str] = []
    suggestions: List[str] = []
    score = 10
    score -= min(8, len(hits))

    # 限制：只展示前 8 条最相关的
    seen_bad = set()
    for h in hits:
        if h["bad"] in seen_bad:
            continue
        seen_bad.add(h["bad"])
        good_options = [g for g in h["good"] if g]
        rep = " / ".join(good_options) if good_options else "（删掉它）"
        issues.append(f"AI 腔：{h['bad']!r}（{h['category']}）")
        suggestions.append(f"{h['bad']!r} → {rep}  // {h['why']}")
        if len(issues) >= 8:
            break

    return max(0, min(10, score)), issues, suggestions


# =====================================================================
# 3. 教 vs 带（Teach vs Lead）
# =====================================================================


_TEACH_PATTERNS = [
    (re.compile(r"你应该|你必须|你需要|你要"), "命令式"),
    (re.compile(r"记住|划重点|敲黑板|注意了|划个重点"), "教官式"),
    (re.compile(r"答案是|正确的做法|标准做法|最佳实践"), "标准答案式"),
    (re.compile(r"^三大|^五大|^几大要点"), "教科书式"),
    (re.compile(r"误区[一二三]?[:：]|常见误区"), "纠错式"),
    (re.compile(r"切记|千万不要|绝对不能"), "警告式"),
]

_LEAD_PATTERNS = [
    (re.compile(r"你可以试试|不妨"), "邀请式"),
    (re.compile(r"我自己|我体感|我之前"), "自身经历式"),
    (re.compile(r"也许|或许|有时候|可能"), "留余地式"),
    (re.compile(r"我把这[天份]?记下来|我想到|我后来发现"), "记录式"),
    (re.compile(r"你呢|你那边怎么样"), "回声式"),
]


def score_teach_vs_lead(text: str) -> Tuple[int, List[str], List[str]]:
    """0~10：高分 = 带读者，低分 = 教读者。"""
    teach_hits: List[str] = []
    lead_hits: List[str] = []
    for pat, kind in _TEACH_PATTERNS:
        for m in pat.finditer(text):
            teach_hits.append(f"{m.group(0)} ({kind})")
    for pat, kind in _LEAD_PATTERNS:
        for m in pat.finditer(text):
            lead_hits.append(f"{m.group(0)} ({kind})")

    score = 5 + len(set(lead_hits)) - len(set(teach_hits))
    score = max(0, min(10, score))

    issues: List[str] = []
    suggestions: List[str] = []
    if teach_hits:
        # 去重前 5
        seen = set()
        unique = []
        for h in teach_hits:
            if h in seen:
                continue
            seen.add(h)
            unique.append(h)
        issues.append(f"教读者腔 {len(unique)} 处：{', '.join(unique[:5])}")
        suggestions.append(
            "Allen 第一课：从'教'到'带'。"
            "把 '你应该 / 必须 / 记住' 改成 '我自己 / 不妨 / 有时候'，"
            "把答案语气改成留白，让读者自己填进去。"
        )
    if not lead_hits and not teach_hits:
        suggestions.append("没有明显的'带读者'语气词，也没有'教读者' — 偏中性。"
                           "可以加 1~2 处 '我自己是这么..' / '不妨试试' 拉近。")
    return score, issues, suggestions


# =====================================================================
# 4. 共鸣度（Resonance）
# =====================================================================

# 装文化 / 冷知识标志（命中扣分）
_COLD_MARKERS = [
    "井水", "蝉七年", "二十四番", "文人雅士", "古人云", "诗云",
    "据《", "《本草", "《诗经》", "节气习俗", "封建社会",
    "考据", "传统认为", "民俗记载",
]

# 共同记忆体验词（命中加分）
_WARM_MARKERS = [
    "风扇", "凉席", "冰箱", "外婆", "奶奶", "妈妈", "阳台", "巷子",
    "早八", "下班", "通勤", "周三", "周五", "周日",
    "草地", "树荫", "晚风", "蝉鸣", "雨声", "桂花", "栀子",
    "电梯", "地铁", "便利店", "小卖部", "校服",
    "伸懒腰", "搓搓手", "踢被子", "打哈欠", "揉眼睛",
    "热水袋", "冰可乐", "绿豆汤", "冰棍", "麻辣烫",
    "翻箱倒柜", "猫咪", "狗子",
]


def score_resonance(text: str) -> Tuple[int, List[str], List[str]]:
    """共鸣度 0~10。"""
    cold = [w for w in _COLD_MARKERS if w in text]
    warm = [w for w in _WARM_MARKERS if w in text]

    score = 5 + min(4, len(set(warm))) - min(4, len(set(cold)))
    score = max(0, min(10, score))

    issues: List[str] = []
    suggestions: List[str] = []
    if cold:
        issues.append(f"装文化 / 冷知识词 {len(set(cold))} 处：{', '.join(set(cold))[:60]}")
        suggestions.append(
            "Allen 教训：场景共鸣不是选有'时间感'的事物，是选**人人都有过的共同记忆**。"
            "把 '井水西瓜' 换成 '冰箱里捞冰镇西瓜'，把 '蝉七年' 换成 '夏夜窗外蝉鸣'。"
        )
    if not warm and not cold:
        suggestions.append(
            "没找到具象的共鸣体验词。"
            "试着写 1~2 个**画面**（草地/晚风/凉席/翻箱倒柜），让读者能看见自己。"
        )
    return score, issues, suggestions


# =====================================================================
# 5. 邀请语（Invitation）
# =====================================================================


_COMMAND_TONE = [
    re.compile(r"必须关注"),
    re.compile(r"赶紧关注"),
    re.compile(r"立刻"),
    re.compile(r"现在就"),
    re.compile(r"马上"),
    re.compile(r"快冲|冲冲冲"),
    re.compile(r"\d+小时内"),
]

_INVITATION_TONE = [
    re.compile(r"如果你也"),
    re.compile(r"要是你"),
    re.compile(r"你那一天"),
    re.compile(r"你呢"),
    re.compile(r"评论区聊聊"),
    re.compile(r"你的[\S]{1,4}是怎样"),
    re.compile(r"留个[^\n]{1,8}给我"),
]


def score_jarvis_trap(text: str) -> Tuple[int, List[str], List[str], Dict[str, bool]]:
    """贾维斯陷阱检测 — Allen 实战对照的 5 维偏差。

    返回：(score 0~10, issues, suggestions, hits_by_dimension)
    score 高 = 没掉进陷阱，写得像范本；score 低 = 像攻略不是范本。
    """
    hits: Dict[str, bool] = {
        "开头挖痛点": False,
        "引导建议动作": False,
        "我在说话": False,
        "运营口吻": False,
        "教做型结尾": False,
    }
    issues: List[str] = []
    suggestions: List[str] = []

    # 1) 开头挖痛点（前 3 段）
    head = "\n".join([ln for ln in text.splitlines() if ln.strip()][:3])
    pain_patterns = [
        re.compile(r"你是不是.{0,15}也"),       # 你是不是也...
        re.compile(r"还在.{0,12}吗[？\?]?"),    # 还在 X 吗
        re.compile(r"是不是.{0,15}很.{0,8}[？\?吗]?"),  # 是不是 X 很 Y
        re.compile(r"为什么.{0,10}总是"),
        re.compile(r"明明.{0,15}却"),
        re.compile(r"累.{0,5}吗|焦虑|内卷|崩溃|emo"),
    ]
    pain_hit = sum(1 for p in pain_patterns if p.search(head))
    if pain_hit >= 1:
        hits["开头挖痛点"] = True
        issues.append(f"开头在挖痛点 / 制造焦虑（命中 {pain_hit} 处）")
        suggestions.append(
            "Allen 范本：把开头从'挖痛点'改成'重新定义'。"
            "例如：「你是不是也总是 X」→「X 不是 Y，是 Z」。"
        )

    # 2) 引导建议动作（vs 展示画面）
    action_patterns = [
        re.compile(r"建议你"),
        re.compile(r"你可以试试[:：]"),
        re.compile(r"你需要"),
        re.compile(r"^[1-9][\.、]\s*[一-鿿]", re.MULTILINE),
        re.compile(r"第[一二三四五]步"),
        re.compile(r"步骤[一二三四五1-5]"),
        re.compile(r"教程[:：]"),
    ]
    action_hit = sum(1 for p in action_patterns if p.search(text))
    # 但如果有"展示画面"句式，抵消
    show_patterns = [
        re.compile(r"有人在.{2,20}"),
        re.compile(r"有[人个].{1,8}[正在]?"),
        re.compile(r"她[在的].{2,20}|他[在的].{2,20}"),
    ]
    show_hit = sum(1 for p in show_patterns if p.search(text))
    if action_hit >= 2 and show_hit == 0:
        hits["引导建议动作"] = True
        issues.append(f"引导在让读者'做事'而不是'看见画面'（建议动作 {action_hit} 处，画面 0 处）")
        suggestions.append(
            "Allen 范本：把'你可以试试 X'改成'有人在 X'。"
            "「你可以早起追日出」→「有人在追这周第二次日出」。"
            "展示在做的人，不是教读者怎么做。"
        )

    # 3) 我（作者）在说话（vs 引用用户）
    self_patterns = [re.compile(r"我推荐|我建议|我觉得|我认为|我的建议")]
    user_voice_patterns = [
        re.compile(r"一个粉丝"),
        re.compile(r"读者[告说]"),
        re.compile(r"有人[告说]"),
        re.compile(r"评论里"),
        re.compile(r"她[跟和]我说|他[跟和]我说"),
        re.compile(r"姐妹[跟和]我说"),
    ]
    self_hit = sum(len(p.findall(text)) for p in self_patterns)
    user_voice_hit = sum(len(p.findall(text)) for p in user_voice_patterns)
    if self_hit >= 3 and user_voice_hit == 0:
        hits["我在说话"] = True
        issues.append(f"全文都是'我'在说话（{self_hit} 处），没有引用真实用户")
        suggestions.append(
            "Allen 范本：让真实用户来说一句话。"
            "「我觉得每个人都需要独处」→「一个粉丝告诉我：'那 20 分钟是我每天唯一不被需要的时刻'」。"
        )

    # 4) 运营口吻
    operating_tone = [
        re.compile(r"扣\s?1"),
        re.compile(r"过\s?\d+\s?(?:个赞|赞|我就|更新)"),
        re.compile(r"下期更精彩"),
        re.compile(r"敬请期待"),
        re.compile(r"想看.{2,10}的[扣举手]"),
        re.compile(r"评论区[抽送]"),
        re.compile(r"点击.{0,10}链接"),
        re.compile(r"点击.{0,10}主页"),
    ]
    op_hit = sum(1 for p in operating_tone if p.search(text))
    if op_hit >= 1:
        hits["运营口吻"] = True
        issues.append(f"运营公告腔 {op_hit} 处")
        suggestions.append(
            "Allen 范本：换成朋友凑过来说。"
            "「想看下期的扣 1」→「你呢？你的那一天是怎样的」。"
        )

    # 5) 教做型结尾（vs 让读者感觉被珍视）
    last_chunk = "\n".join([ln for ln in text.splitlines() if ln.strip()][-3:])
    teach_ending = [
        re.compile(r"希望大家"),
        re.compile(r"总之.{0,10}很重要"),
        re.compile(r"以上.{0,8}希望"),
        re.compile(r"学会.{0,10}就能"),
        re.compile(r"最后.{0,10}建议"),
        re.compile(r"记住.{0,15}就"),
    ]
    cherished_patterns = [
        re.compile(r"都很对"),
        re.compile(r"都值得"),
        re.compile(r"都[挺很]?好"),
        re.compile(r"都可以"),
        re.compile(r"无论你"),
        re.compile(r"不论你"),
        re.compile(r"被珍视|被看见|被在意"),
    ]
    teach_e = sum(1 for p in teach_ending if p.search(last_chunk))
    cherish_e = sum(1 for p in cherished_patterns if p.search(last_chunk))
    if teach_e >= 1 and cherish_e == 0:
        hits["教做型结尾"] = True
        issues.append("结尾在'希望大家 X'而不是'让读者感觉被珍视'")
        suggestions.append(
            "Allen 范本：让读者感觉被看见。"
            "「希望大家都能找到属于自己的尽兴方式」"
            "→「不论你这周末是去看了海，还是只在阳台坐了一下午 — 都很对」。"
        )

    n_hits = sum(1 for v in hits.values() if v)
    score = 10 - n_hits * 2  # 每命中一维扣 2 分
    score = max(0, min(10, score))

    if n_hits >= 2 and not issues:
        # 兜底：命中数高但 issues 没收集到
        for k, v in hits.items():
            if v:
                issues.append(f"命中陷阱：{k}")
    if n_hits >= 3:
        suggestions.insert(0,
            f"⚠️ 整篇可能是'攻略型'而非'范本型'（{n_hits}/5 维命中陷阱）。"
            "重写时换思路：你在'教读者怎么做' → 改成'展示什么样的人已经在做'。"
        )

    return score, issues, suggestions, hits


def score_invitation(text: str) -> Tuple[int, List[str], List[str]]:
    """互动语气：邀请 vs 任务指令。0~10。"""
    cmd: List[str] = []
    inv: List[str] = []
    for pat in _COMMAND_TONE:
        cmd.extend(m.group(0) for m in pat.finditer(text))
    for pat in _INVITATION_TONE:
        inv.extend(m.group(0) for m in pat.finditer(text))

    score = 5 + min(4, len(set(inv))) - min(4, len(set(cmd)))
    score = max(0, min(10, score))

    issues: List[str] = []
    suggestions: List[str] = []
    if cmd:
        issues.append(f"命令式互动语 {len(set(cmd))} 处：{', '.join(set(cmd))}")
        suggestions.append(
            "Allen 第三课：互动不是任务指令，是邀请语。"
            "「赶紧关注」→「如果你也喜欢这种感觉」；「立刻参与」→「这里有个落脚点」。"
        )
    if not inv:
        suggestions.append(
            "正文里没有'邀请语' — 读者读完，没有被'拉进来'的位置。"
            "末段加一句：'你呢？' / '你那一天是怎样的，留个故事给我'。"
        )
    return score, issues, suggestions


# =====================================================================
# 综合
# =====================================================================


@dataclass
class AestheticScore:
    breath: int
    ai_speak: int
    teach_vs_lead: int
    resonance: int
    invitation: int
    jarvis_trap: int                 # Allen 实战对照 5 维差距，10 = 没掉陷阱
    total: int                       # 加权总分 0~100
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    by_dim: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    jarvis_hits: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


_DIM_LABELS = {
    "breath": "留白度",
    "ai_speak": "去 AI 腔",
    "teach_vs_lead": "带读者",
    "resonance": "共鸣度",
    "invitation": "邀请语",
    "jarvis_trap": "范本范",   # Allen 实战对照
}


_DEFAULT_AESTHETIC_WEIGHTS = {
    "breath": 0.20,
    "ai_speak": 0.15,
    "teach_vs_lead": 0.15,
    "resonance": 0.15,
    "invitation": 0.10,
    "jarvis_trap": 0.25,        # 系统性思路偏差权重最高
}


def aesthetic_score(
    title: str,
    content: str,
    *,
    disabled: Optional[List[str]] = None,
    weights: Optional[Dict[str, float]] = None,
) -> AestheticScore:
    full = f"{title}\n{content}"
    disabled = set(disabled or [])
    weights = weights or _DEFAULT_AESTHETIC_WEIGHTS

    by_dim: Dict[str, Dict[str, Any]] = {}
    issues_all: List[str] = []
    suggestions_all: List[str] = []
    jarvis_hits: Dict[str, bool] = {}

    def _run(name: str, fn, arg):
        if name in disabled:
            return None
        s, i, sg = fn(arg)
        by_dim[name] = {"score": s, "issues": i, "suggestions": sg}
        issues_all.extend(f"[{_DIM_LABELS[name]}] {x}" for x in i)
        suggestions_all.extend(f"[{_DIM_LABELS[name]}] {x}" for x in sg)
        return s

    breath = _run("breath", score_breath, content)
    ai = _run("ai_speak", score_ai_speak, full)
    tvl = _run("teach_vs_lead", score_teach_vs_lead, full)
    res = _run("resonance", score_resonance, full)
    inv = _run("invitation", score_invitation, content)

    # jarvis_trap 返回值多一个 hits 字典
    jt: Optional[int] = None
    if "jarvis_trap" not in disabled:
        jt, jt_issues, jt_sg, jarvis_hits = score_jarvis_trap(full)
        by_dim["jarvis_trap"] = {"score": jt, "issues": jt_issues, "suggestions": jt_sg,
                                 "hits": jarvis_hits}
        issues_all.extend(f"[{_DIM_LABELS['jarvis_trap']}] {x}" for x in jt_issues)
        suggestions_all.extend(f"[{_DIM_LABELS['jarvis_trap']}] {x}" for x in jt_sg)

    # 归一化加权
    norm: Dict[str, float] = {}
    s_total_w = sum(w for k, w in weights.items() if k in by_dim) or 1.0
    for k, w in weights.items():
        if k in by_dim:
            norm[k] = w / s_total_w

    total = int(round(sum(by_dim[k]["score"] / 10 * norm[k] for k in by_dim) * 100))

    return AestheticScore(
        breath=breath if breath is not None else 0,
        ai_speak=ai if ai is not None else 0,
        teach_vs_lead=tvl if tvl is not None else 0,
        resonance=res if res is not None else 0,
        invitation=inv if inv is not None else 0,
        jarvis_trap=jt if jt is not None else 0,
        total=total,
        issues=issues_all,
        suggestions=suggestions_all,
        by_dim=by_dim,
        jarvis_hits=jarvis_hits,
    )


# =====================================================================
# Allen-mode：与 score_post 整合的合并打分
# =====================================================================


def merge_with_engineering_score(
    eng_breakdown: Dict[str, int],
    eng_total: int,
    aesthetic: AestheticScore,
    *,
    aesthetic_weight: float = 0.4,
) -> Dict[str, Any]:
    """把工程打分（v2.0 那套 6 维）和 Allen 打分混合。

    aesthetic_weight = 0 → 纯工程分；= 1 → 纯 Allen 分。
    默认 0.4 — Allen 占四成。
    """
    eng = max(0, min(100, eng_total))
    aes = max(0, min(100, aesthetic.total))
    final = int(round(eng * (1 - aesthetic_weight) + aes * aesthetic_weight))
    return {
        "final": final,
        "engineering": eng,
        "aesthetic": aes,
        "aesthetic_weight": aesthetic_weight,
        "engineering_breakdown": eng_breakdown,
        "aesthetic_breakdown": {k: v["score"] for k, v in aesthetic.by_dim.items()},
    }
