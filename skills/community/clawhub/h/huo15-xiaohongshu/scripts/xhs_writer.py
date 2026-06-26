"""火一五小红书文案创作核心库。

负责三件事：
1. **生成（draft）**：根据主题 / 受众 / 骨架代号，给出标题候选 + 正文骨架填充。
2. **打分（score）**：从标题钩子、首段抓力、emoji 节奏、话题数、合规
   等维度给一篇笔记打分。
3. **优化（polish）**：基于打分结果给出可执行的修改建议。

设计原则
========
- **不依赖大模型** — 所有生成逻辑都是规则驱动 + 模板填充，离线可跑。
  这样脚本既是 skill 内部用的，也能让 Claude 在调用时拿到可解释的中间产物。
- **可被 LLM 复用** — 把"标题公式""正文骨架""敏感词"暴露成数据，
  Claude 在生成时也能直接 import / 读取。
- **从不调用发布接口** — 任何写操作（发文 / 点赞 / 关注）都不在本模块。
"""

from __future__ import annotations

import json
import os
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 数据目录的解析：跑脚本时按相对路径找
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# =====================================================================
# 数据加载
# =====================================================================


def _load_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    out: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def load_sensitive_words(path: Optional[Path] = None) -> List[str]:
    return _load_lines(path or _DATA_DIR / "sensitive_words.txt")


# =====================================================================
# 标题模板（11 种公式 → 生成函数）
# =====================================================================
# 每个模板返回多个候选，让 Claude / 用户挑。
# 占位符：{topic} 主题词 / {persona} 受众身份 / {payoff} 利益点 / {number} 数字


def _pick_number(default: int = 3) -> int:
    return random.choice([3, 5, 7])


_TITLE_GENERATORS: Dict[str, Any] = {}


def _register_title(code: str):
    def deco(fn):
        _TITLE_GENERATORS[code] = fn
        return fn

    return deco


@_register_title("T1")  # 数字对比
def _t1(topic: str, persona: str, payoff: str) -> List[str]:
    n = _pick_number()
    base = [
        f"{n} 个被严重低估的 {topic}，{payoff}",
        f"{n} 招让你的 {topic} {payoff}",
        f"{n} 件 {persona or '我'} 做了真的不后悔的 {topic} 小事",
    ]
    return base


@_register_title("T2")  # 痛点共情
def _t2(topic: str, persona: str, payoff: str) -> List[str]:
    p = persona or "成年人"
    return [
        f"{p}，为什么 {topic} 总是越做越累",
        f"{p} 怎么办：3 个不靠运气也能 {payoff or '改善'} 的笨办法",
        f"{p} 真的不能再这么 {topic} 了，记住 4 个动作",
    ]


@_register_title("T3")  # 反差冲突
def _t3(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"我以为 {topic} 没用，结果 {payoff or '真香了'}",
        f"看着普通的 {topic}，其实藏着 {payoff or '一个反常识'}",
        f"被 {topic} 救了一次，才知道 {payoff or '之前都白折腾了'}",
    ]


@_register_title("T4")  # 悬念钩子
def _t4(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"把 {topic} 这样用，居然能 {payoff or '省一半时间'}",
        f"没想到 {topic} 还能 {payoff or '这样玩'}，亲测有效",
        f"这一招让 {topic} 的效率翻倍，方法很笨",
    ]


@_register_title("T5")  # 身份代入
def _t5(topic: str, persona: str, payoff: str) -> List[str]:
    p = persona or "前从业者"
    return [
        f"作为{p}，我来劝你别盲目入 {topic}",
        f"作为常年研究 {topic} 的人，亲测有效的 3 件小事",
        f"作为 30+ {p}，关于 {topic} 我有 5 句真心话",
    ]


@_register_title("T6")  # 福利免费
def _t6(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"免费！整理好的 {topic} 资料合集，分类清晰可用",
        f"0 元学完 {topic}，这 3 个渠道真的够用",
        f"{topic} 必备清单 — 不花冤枉钱版",
    ]


@_register_title("T7")  # 时间节点
def _t7(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"2026 年再做 {topic}，请先看完这 5 点",
        f"{persona or '28 岁'} 之前一定要做的 {topic} 5 件事",
        f"换季 {topic} 救命指南：从 0 到 1 的 4 步",
    ]


@_register_title("T8")  # 提问诱发
def _t8(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"为什么有些人做 {topic} 越做越轻松？我观察了 30 个案例",
        f"{topic} 是不是真的有那么难？我自己试了 3 个月",
        f"网传 {topic} 的几种说法，是真是假",
    ]


@_register_title("T9")  # 极端结果（避绝对化用语，用主观）
def _t9(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"这是我用过觉得舒服的 {topic}，回购了好几次",
        f"第一次认真做 {topic}，被效果惊到了",
        f"30 岁前唯一让我后悔没早做的 {topic} 这件事",
    ]


@_register_title("T10")  # 步骤指南
def _t10(topic: str, persona: str, payoff: str) -> List[str]:
    n = _pick_number(5)
    return [
        f"保姆级！从零开始做 {topic}，这 {n} 步少走弯路",
        f"手把手教 {persona or '小白'} 入门 {topic}，含模板",
        f"{topic} 入门 SOP：记住这 {n} 步就够了",
    ]


@_register_title("T11")  # 故事开场
def _t11(topic: str, persona: str, payoff: str) -> List[str]:
    return [
        f"上周开始 {topic}，每天花 30 分钟也很值",
        f"那天因为 {topic} 加班到半夜，我决定换种活法",
        f"朋友说我变了，原来是开始 {topic} 之后",
    ]


def generate_titles(
    topic: str,
    *,
    persona: str = "",
    payoff: str = "",
    formulas: Optional[List[str]] = None,
    n_each: int = 1,
) -> List[Dict[str, str]]:
    """根据公式代号生成标题候选。

    Args:
        topic: 主题关键词，例如 "护肤""副业""减脂"。
        persona: 目标受众身份，例如 "干皮女生""互联网打工人"。
        payoff: 利益点 / 结果，例如 "效率翻倍""不踩坑"。
        formulas: 想用的公式代号列表（T1 ~ T11）；空 = 全部。
        n_each: 每种公式生成几条。

    Returns:
        [{"formula": "T1", "title": "..."}]
    """
    keys = formulas or list(_TITLE_GENERATORS.keys())
    out: List[Dict[str, str]] = []
    for code in keys:
        gen = _TITLE_GENERATORS.get(code)
        if not gen:
            continue
        candidates = gen(topic, persona, payoff)
        for t in candidates[:n_each]:
            out.append({"formula": code, "title": t.strip()})
    return out


# =====================================================================
# 正文骨架渲染（S1 ~ S7）
# =====================================================================


_BODY_SKELETONS: Dict[str, List[str]] = {
    "S1": [
        "✨ 你是不是也 {hook}？",
        "我之前 {pain1}，",
        "试过 {pain2}，{pain3}，最后发现都是治标不治本。",
        "",
        "其实只要 {breakthrough}，整件事就 {result}。",
        "",
        "📌 {step1_label}",
        "{step1_detail}",
        "",
        "📌 {step2_label}",
        "{step2_detail}",
        "",
        "📌 {step3_label}",
        "{step3_detail}",
        "",
        "⚠️ {warning}",
        "",
        "{closing} {cta}",
    ],
    "S2": [
        "{scene}",
        "",
        "那一刻我突然意识到，{insight}。",
        "",
        "之前我一直 {old_pattern}，以为 {old_belief}。",
        "其实 {new_realization}。",
        "",
        "如果你也在 {similar_situation}，可以试试 {action}。",
        "",
        "{closing}",
        "",
        "{cta}",
    ],
    "S3": [
        "✨ 这次给大家测了 {n} 款 {category}。",
        "我筛选标准：{criteria}",
        "",
        "🔹 {item1_name}",
        "{item1_detail}",
        "",
        "🔹 {item2_name}",
        "{item2_detail}",
        "",
        "🔹 {item3_name}",
        "{item3_detail}",
        "",
        "🏆 我自己最回购的是 {pick}，因为 {reason}。",
        "",
        "❌ 避雷：{avoid}",
        "",
        "{cta}",
    ],
    "S4": [
        "整理了 {n} 个 {topic}，分门别类放好了 ✨",
        "",
        "1️⃣ {item1}",
        "2️⃣ {item2}",
        "3️⃣ {item3}",
        "4️⃣ {item4}",
        "5️⃣ {item5}",
        "",
        "💡 我自己最常用的是 {favorite}。",
        "",
        "{cta}",
    ],
    "S5": [
        "今天写一份保姆级 {topic} 教程 ✍️",
        "看完你能 {outcome}。",
        "",
        "📦 准备工作：{prep}",
        "",
        "Step 1：{step1}",
        "{step1_note}",
        "",
        "Step 2：{step2}",
        "{step2_note}",
        "",
        "Step 3：{step3}",
        "{step3_note}",
        "",
        "❓ 常见问题",
        "Q: {q1}  A: {a1}",
        "Q: {q2}  A: {a2}",
        "",
        "{cta}",
    ],
    "S6": [
        "💡 我有个不太主流的观点：{opinion}",
        "",
        "大多数人觉得 {common_view}，但我的体感是 — {counter}。",
        "",
        "理由 1：{reason1}",
        "理由 2：{reason2}",
        "理由 3：{reason3}",
        "",
        "🤔 也许会有人说 {objection}，我的回应是 {response}。",
        "",
        "{cta}",
    ],
    "S7": [
        "{when} / {where}",
        "",
        "{moment1}",
        "{moment2}",
        "{moment3}",
        "",
        "{tiny_thought}",
        "",
        "{cta}",
    ],
}


def get_skeleton(code: str) -> List[str]:
    if code not in _BODY_SKELETONS:
        raise ValueError(f"未知正文骨架代号：{code}（可用：{', '.join(_BODY_SKELETONS)})")
    return list(_BODY_SKELETONS[code])


def render_skeleton(code: str, fields: Optional[Dict[str, str]] = None) -> str:
    """把骨架代号 + 字段映射渲染成正文。未填的字段保留 `{name}`，让 LLM/作者后填。"""
    lines = get_skeleton(code)
    fields = fields or {}
    rendered = []
    for ln in lines:
        try:
            rendered.append(ln.format_map(_DefaultDict(fields)))
        except Exception:
            rendered.append(ln)
    return "\n".join(rendered)


class _DefaultDict(dict):
    """缺失键时返回 `{key}` 占位，避免 KeyError。"""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


# =====================================================================
# 文案打分
# =====================================================================


@dataclass
class PostScore:
    """一篇笔记的总分 + 子项分 + 修改建议。"""

    total: int  # 0 ~ 100
    breakdown: Dict[str, int] = field(default_factory=dict)  # 各子项 0~10
    issues: List[str] = field(default_factory=list)  # 警示
    suggestions: List[str] = field(default_factory=list)  # 修改建议

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "breakdown": self.breakdown,
            "issues": self.issues,
            "suggestions": self.suggestions,
        }


_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "‍️]"
)


def _count_emoji(text: str) -> int:
    return len(_EMOJI_RE.findall(text))


def score_title(title: str, *, keyword: str = "") -> Tuple[int, List[str], List[str]]:
    """标题打分。0~10。

    Args:
        keyword: 主关键词（赛道核心词），用来检查是否在前 13 字。
                 不传则从标题里启发式提取。
    """
    score = 5
    issues: List[str] = []
    suggestions: List[str] = []

    n = len(title)
    if n < 10:
        score -= 2
        issues.append(f"标题过短（{n} 字），钩子不足")
        suggestions.append("加上利益点 / 数字 / 反差词，扩到 16~22 字")
    elif n > 30:
        score -= 2
        issues.append(f"标题过长（{n} 字），首页可能被截断")
        suggestions.append("精简到 22 字以内")
    elif 16 <= n <= 22:
        score += 2

    # 钩子词
    hook_words = ["3 ", "5 ", "7 ", "为什么", "怎么办", "居然", "没想到", "亲测",
                  "保姆级", "手把手", "我以为", "作为", "免费", "0 元", "白嫖"]
    if any(w in title for w in hook_words):
        score += 2

    # emoji
    e = _count_emoji(title)
    if e > 3:
        score -= 2
        issues.append(f"标题 emoji {e} 个，太多显廉价")
        suggestions.append("减到 0~2 个")

    # 关键词位置（小红书搜索权重 40% 在前 13 字）
    if keyword and len(title) >= 5:
        head = title[:13]
        if keyword in head:
            score += 1
        elif keyword in title:
            score -= 1
            issues.append(f"关键词 {keyword!r} 在 13 字之后（搜索权重大幅下降）")
            suggestions.append(f"把 {keyword!r} 挪到标题前 13 字内 — 小红书搜索 40% 权重在这里")
        else:
            issues.append(f"标题没有出现关键词 {keyword!r}")
            suggestions.append(f"标题至少出现 1 次 {keyword!r} 让搜索能找到")

    return max(0, min(10, score)), issues, suggestions


# ---------- CES 互动设计分（v3.3 新增） ----------
# 小红书 CES 算法权重：关注(8) > 转发(4) ≈ 评论(4) > 点赞(1) ≈ 收藏(1)
# 引导用户做高分动作（关注 / 评论）的笔记进入下一级流量池更快。
_FOLLOW_HOOKS = [
    re.compile(r"如果你也.{0,15}的话"),    # 软引导关注
    re.compile(r"想看.{0,8}的"),
    re.compile(r"主页[有还]"),
    re.compile(r"系列|栏目|连载"),           # 暗示连载，鼓励关注
]

_COMMENT_HOOKS = [
    re.compile(r"你呢[？?]?$", re.MULTILINE),
    re.compile(r"你[那的].{1,8}是怎样"),
    re.compile(r"评论区[聊见]"),
    re.compile(r"留个故事给我"),
    re.compile(r"留言告诉我"),
    re.compile(r"你[最更].{1,8}的[是哪]"),
]

_LIKE_ONLY_HOOKS = [
    re.compile(r"求点赞"),
    re.compile(r"点个赞"),
    re.compile(r"双击屏幕"),
]


def score_ces_design(title: str, content: str) -> Tuple[int, List[str], List[str]]:
    """CES 互动设计分 0~10。优先看高权重引导（关注 8 > 评论 4 > 点赞 1）。"""
    full = f"{title}\n{content}"
    follow_hits = sum(1 for p in _FOLLOW_HOOKS if p.search(full))
    comment_hits = sum(1 for p in _COMMENT_HOOKS if p.search(full))
    like_hits = sum(1 for p in _LIKE_ONLY_HOOKS if p.search(full))

    score = 4  # 中等基础分
    issues: List[str] = []
    suggestions: List[str] = []

    # 高权重命中加分（关注 +3，评论 +2）
    if follow_hits:
        score += 3
    if comment_hits:
        score += 2

    # 全靠"求赞"扣分（CES 权重最低）
    if like_hits and follow_hits == 0 and comment_hits == 0:
        score -= 2
        issues.append(f"只引导点赞（{like_hits} 处） — CES 权重 1，最低")
        suggestions.append(
            "小红书 CES 算法：关注(8) > 评论(4) > 点赞(1)。"
            "把 '求点赞' 改成 '你呢，留个故事给我'（评论 4 倍权重）"
            "或 '想看类似的可以蹲一下'（软关注 8 倍权重）。"
        )

    # 完全没有互动设计
    if follow_hits == 0 and comment_hits == 0 and like_hits == 0:
        score -= 1
        suggestions.append(
            "没有互动引导 — 至少加 1 处评论邀请（'你呢？'/ '你那一天是怎样的'），"
            "CES 算法把评论按 4 分计权，比点赞高 4 倍。"
        )

    return max(0, min(10, score)), issues, suggestions


def score_first_lines(content: str) -> Tuple[int, List[str], List[str]]:
    """首 3 行打分（决定是否被滑走）。0~10。"""
    score = 5
    issues: List[str] = []
    suggestions: List[str] = []

    lines = [ln for ln in content.splitlines() if ln.strip()]
    if not lines:
        return 0, ["正文为空"], ["补全正文"]

    head = "\n".join(lines[:3])
    if len(head) < 30:
        score -= 2
        issues.append("首段过短，钩子不够")
        suggestions.append("首段加 1~2 个具体场景或数字")

    # 钩子模式
    hook_patterns = ["你是不是", "你也", "为什么", "我之前", "其实", "上周", "那天",
                     "我以为", "亲测", "整理了", "测了", "不主流", "💡", "✨", "🔥"]
    if any(p in head for p in hook_patterns):
        score += 3
    else:
        suggestions.append("首段可以加'你是不是也...'、'我之前也...'之类的代入钩子")

    return max(0, min(10, score)), issues, suggestions


def score_paragraph_layout(content: str) -> Tuple[int, List[str], List[str]]:
    """段落排版打分 — 段落是否过长 / 有没有空行。0~10。"""
    score = 6
    issues: List[str] = []
    suggestions: List[str] = []

    lines = content.splitlines()
    long_paragraphs = sum(1 for ln in lines if len(ln) > 80)
    if long_paragraphs > 2:
        score -= 3
        issues.append(f"有 {long_paragraphs} 段超过 80 字，手机阅读会很累")
        suggestions.append("把长段落拆短，每段控制在 1~3 句")

    # 是否有空行
    blank = sum(1 for ln in lines if not ln.strip())
    text_lines = max(1, len(lines) - blank)
    if blank / text_lines < 0.15:
        score -= 2
        issues.append("段间空行偏少，看起来像大字报")
        suggestions.append("每 2~3 句加一个空行")

    return max(0, min(10, score)), issues, suggestions


def score_emoji_density(content: str) -> Tuple[int, List[str], List[str]]:
    """emoji 节奏打分。0~10。"""
    score = 7
    issues: List[str] = []
    suggestions: List[str] = []

    e = _count_emoji(content)
    chars = max(1, len(content))
    rate = e / chars

    if e == 0:
        score -= 2
        issues.append("全文没有 emoji，缺少视觉节奏")
        suggestions.append("加 3~6 个 emoji 当项目符号 / 强调")
    elif e > 18:
        score -= 3
        issues.append(f"全文 {e} 个 emoji，密度过高显廉价")
        suggestions.append("精简到 6~12 个，关键句留就好")
    elif rate > 0.05:
        score -= 1
        issues.append("emoji 密度偏高")

    return max(0, min(10, score)), issues, suggestions


# 大词样本（百万级，泛流量）— 命中越多说明分级偏向"大词"
_BIG_TAGS = {
    "今日穿搭", "日常", "好物分享", "美食", "旅行", "护肤", "减肥", "健身",
    "学习", "职场", "育儿", "家居", "vlog", "早八", "周末日常", "生活记录",
    "穿搭", "美妆", "数码", "情感", "副业", "美食探店", "OOTD",
}


def _classify_tag(tag: str) -> str:
    """粗略分级：big（大词）/ mid（中词）/ long（长尾/自创）。"""
    t = tag.strip().lstrip("#")
    if t in _BIG_TAGS:
        return "big"
    # 长尾特征：长度 > 6 字 / 含具体年龄/季节/品牌/场景
    if len(t) > 5 or any(w in t for w in ["30+", "30岁", "干皮", "油皮", "敏感肌",
                                           "微胖", "i人", "梨形", "学生党",
                                           "通勤", "周三", "周日", "约会"]):
        return "long"
    return "mid"


def score_hashtags(tags: List[str]) -> Tuple[int, List[str], List[str]]:
    """话题数量 + 分级质量。0~10。

    理想结构（来自市场调研 + 主流工具实践）：2 个泛词 + 2~3 个垂直 + 1 个长尾。
    """
    score = 5
    issues: List[str] = []
    suggestions: List[str] = []
    clean = [t.strip() for t in tags if t.strip()]
    n = len(clean)

    if n == 0:
        return 2, ["没有话题，分发会很差"], [
            "加 3~6 个相关 #话题（参考 data/hashtag_topics.md）"
        ]
    if n < 3:
        return 4, [], [f"话题只有 {n} 个，建议补到 3~6 个"]
    if n > 8:
        score = 5
        issues.append(f"话题 {n} 个偏多，会被识别为营销号")
        suggestions.append("精简到 6 个以内")
    elif 3 <= n <= 6:
        score = 9

    # 分级检查
    levels = [_classify_tag(t) for t in clean]
    n_big = levels.count("big")
    n_mid = levels.count("mid")
    n_long = levels.count("long")

    # 全是大词 — 竞争激烈，难露出
    if n_big >= n - 1 and n_big >= 3:
        score -= 2
        issues.append(f"{n_big}/{n} 都是大词 — 竞争激烈，新号难露出")
        suggestions.append(
            "改成 2 个泛词 + 2~3 个垂直词 + 1 个长尾词。"
            "把 1~2 个 #护肤 / #美食 这种泛词换成 #干皮护肤 / #一人食 这种细分词。"
        )
    # 完全没有长尾 — 错过精准受众
    if n >= 3 and n_long == 0:
        score -= 1
        suggestions.append(
            "没有长尾话题（如 #30岁干皮 / #i人独居 / #早C晚A）— "
            "长尾竞争小、受众精准，至少加 1 个。"
        )
    # 完全没大词 — 失去基础流量池
    if n >= 4 and n_big == 0:
        score -= 1
        suggestions.append(
            "没有大词（#护肤 / #美食 / #日常） — 失去基础流量池。"
            "至少留 1 个赛道根词。"
        )

    return max(0, min(10, score)), issues, suggestions


def score_sensitive(text: str, sensitive: Optional[List[str]] = None) -> Tuple[int, List[str], List[str]]:
    """敏感词打分（命中即扣分）。0~10。"""
    sw = sensitive if sensitive is not None else load_sensitive_words()
    if not sw:
        return 8, [], []

    hits: List[str] = []
    low = text  # 中文不区分大小写也无所谓
    for w in sw:
        if w and w in low:
            hits.append(w)

    score = 10
    issues: List[str] = []
    suggestions: List[str] = []

    for h in hits:
        score -= 2
        issues.append(f"命中敏感词：{h!r}")
        suggestions.append(f"把 {h!r} 改成主观表达（'我自己用下来' / '我体感'）或删掉")

    return max(0, score), issues, suggestions


def score_post(
    title: str,
    content: str,
    tags: Optional[List[str]] = None,
    sensitive: Optional[List[str]] = None,
    *,
    rules: Optional[Any] = None,
) -> PostScore:
    """综合打分（0~100）。

    Args:
        rules: 可选 `xhs_profile.RuleOverride` — 用户的规则覆盖。
            传入后会按用户设置调整权重 / 禁用检查项 / 加自定义敏感词。
    """
    tags = tags or []
    breakdown: Dict[str, int] = {}
    issues: List[str] = []
    suggestions: List[str] = []

    # 解析 RuleOverride（避免循环 import）
    disabled: set = set()
    weights = {
        "title": 0.20, "first_lines": 0.15, "layout": 0.10,
        "emoji": 0.05, "hashtags": 0.10, "ces_design": 0.15,
        "compliance": 0.25,
    }
    keyword = ""
    if rules is not None:
        keyword = getattr(rules, "main_keyword", "") or ""
    if rules is not None:
        for k in getattr(rules, "disabled_checks", []) or []:
            disabled.add(k)
        for k, v in (getattr(rules, "weights", {}) or {}).items():
            if k in weights:
                weights[k] = max(0.0, float(v))
        for k in disabled:
            if k in weights:
                weights[k] = 0.0
        # sensitive 列表：去掉用户允许的，加上用户额外的
        if sensitive is None:
            sensitive = load_sensitive_words()
        allowed = set(getattr(rules, "allowed_words", []) or [])
        sensitive = [w for w in sensitive if w not in allowed]
        sensitive.extend(w for w in (getattr(rules, "custom_sensitive", []) or [])
                         if w not in allowed)

    def _run(name: str, fn, *args):
        if name in disabled:
            return
        s, i, sg = fn(*args)
        breakdown[name] = s
        issues.extend(f"[{_LABELS.get(name, name)}] {x}" for x in i)
        suggestions.extend(f"[{_LABELS.get(name, name)}] {x}" for x in sg)

    # title 需要传 keyword
    if "title" not in disabled:
        s, i, sg = score_title(title, keyword=keyword)
        breakdown["title"] = s
        issues.extend(f"[{_LABELS.get('title','title')}] {x}" for x in i)
        suggestions.extend(f"[{_LABELS.get('title','title')}] {x}" for x in sg)

    _run("first_lines", score_first_lines, content)
    _run("layout", score_paragraph_layout, content)
    _run("emoji", score_emoji_density, content)
    _run("hashtags", score_hashtags, tags)
    # CES 互动设计分（v3.3 新加）
    if "ces_design" not in disabled:
        s, i, sg = score_ces_design(title, content)
        breakdown["ces_design"] = s
        issues.extend(f"[{_LABELS.get('ces_design','ces')}] {x}" for x in i)
        suggestions.extend(f"[{_LABELS.get('ces_design','ces')}] {x}" for x in sg)
    full_text = f"{title}\n{content}\n{' '.join(tags)}"
    _run("compliance", score_sensitive, full_text, sensitive)

    # 归一化权重（disabled 的 = 0，其他重新分配）
    total_w = sum(w for k, w in weights.items() if k in breakdown) or 1.0
    norm = {k: w / total_w for k, w in weights.items() if k in breakdown}
    total = sum(breakdown[k] / 10 * w for k, w in norm.items()) * 100

    return PostScore(
        total=int(round(total)),
        breakdown=breakdown,
        issues=issues,
        suggestions=suggestions,
    )


_LABELS = {
    "title": "标题",
    "first_lines": "首段",
    "layout": "排版",
    "emoji": "emoji",
    "hashtags": "话题",
    "ces_design": "CES互动",
    "compliance": "合规",
}


# =====================================================================
# 完整笔记数据结构
# =====================================================================


@dataclass
class Draft:
    """一份待发布的草稿。"""

    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    cover_hint: str = ""  # 封面建议（Claude/作者补图前的描述）
    image_hints: List[str] = field(default_factory=list)  # 各张配图描述
    formula: str = ""  # 标题公式代号 T1~T11
    skeleton: str = ""  # 正文骨架代号 S1~S7
    notes: str = ""  # 其他说明
    score: Optional[Dict[str, Any]] = None  # 自我打分（可选）

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "cover_hint": self.cover_hint,
            "image_hints": self.image_hints,
            "formula": self.formula,
            "skeleton": self.skeleton,
            "notes": self.notes,
        }
        if self.score is not None:
            d["score"] = self.score
        return d

    def to_markdown(self) -> str:
        """渲染成发布前预览的 Markdown。"""
        parts = [f"# {self.title}", ""]
        parts.append(self.content)
        parts.append("")
        if self.tags:
            parts.append("**话题：** " + " ".join(f"#{t}" for t in self.tags))
        if self.cover_hint:
            parts.append("")
            parts.append(f"**封面建议：** {self.cover_hint}")
        if self.image_hints:
            parts.append("")
            parts.append("**配图建议：**")
            for i, h in enumerate(self.image_hints, 1):
                parts.append(f"- 图{i}：{h}")
        if self.notes:
            parts.append("")
            parts.append(f"_备注：{self.notes}_")
        return "\n".join(parts) + "\n"

    def to_clipboard_text(self) -> str:
        """渲染成"可以直接粘贴到小红书 App"的纯文本。"""
        body = self.content.rstrip()
        tags_line = " ".join(f"#{t}" for t in self.tags) if self.tags else ""
        if tags_line:
            return f"{body}\n\n{tags_line}\n"
        return body + "\n"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Draft":
        return cls(
            title=d.get("title", ""),
            content=d.get("content", ""),
            tags=list(d.get("tags") or []),
            cover_hint=d.get("cover_hint", ""),
            image_hints=list(d.get("image_hints") or []),
            formula=d.get("formula", ""),
            skeleton=d.get("skeleton", ""),
            notes=d.get("notes", ""),
            score=d.get("score"),
        )


def load_draft(path: str) -> Draft:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        return Draft.from_dict(json.loads(text))
    # 否则按 Markdown 解析（标题取第一行 #，话题取最后一行 # 标签，正文取中间）
    return _parse_markdown_draft(text)


def _parse_markdown_draft(text: str) -> Draft:
    lines = text.splitlines()
    title = ""
    content_lines: List[str] = []
    tags: List[str] = []

    for ln in lines:
        if not title and ln.strip().startswith("# "):
            title = ln.strip()[2:].strip()
            continue
        if ln.strip().startswith("#") and " " not in ln.strip()[1:].strip():
            # 单 hashtag 行：当成话题
            for t in re.findall(r"#([\w一-鿿]+)", ln):
                tags.append(t)
            continue
        # 行内的 # 话题（如末尾一行）
        inline_tags = re.findall(r"#([\w一-鿿]+)", ln)
        if inline_tags and len(inline_tags) >= 2 and len(ln.strip()) < 200:
            tags.extend(inline_tags)
            continue
        content_lines.append(ln)

    content = "\n".join(content_lines).strip()
    return Draft(title=title, content=content, tags=tags)


def save_draft(draft: Draft, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == ".json":
        p.write_text(json.dumps(draft.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        p.write_text(draft.to_markdown(), encoding="utf-8")


# =====================================================================
# 完整生成（标题 + 骨架 + 话题 占位）
# =====================================================================


def make_draft(
    topic: str,
    *,
    persona: str = "",
    payoff: str = "",
    formula: str = "T2",
    skeleton: str = "S1",
    tags: Optional[List[str]] = None,
) -> Draft:
    """一键生成草稿 — 标题选 1 条，正文是骨架占位，让用户/LLM 后续填。"""
    titles = generate_titles(topic, persona=persona, payoff=payoff, formulas=[formula])
    title = titles[0]["title"] if titles else topic
    body = render_skeleton(skeleton)
    return Draft(
        title=title,
        content=body,
        tags=list(tags or []),
        formula=formula,
        skeleton=skeleton,
        notes=f"骨架占位文本，请替换 {{...}} 中的内容；建议跑 polish_post.py 检查。",
    )
