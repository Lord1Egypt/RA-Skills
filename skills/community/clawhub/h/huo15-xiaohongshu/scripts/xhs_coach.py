"""火一五小红书"写作教练"核心库。

定位
====
比 polish_post 多一层："为什么这里不好 + 应该怎么改 + 参考是什么样"。
不是替你写，是教你为什么这样写更好。

诊断维度
========
1. **风格偏离** — 标题/段落/emoji 是否偏离用户自己的 baseline
2. **公式诊断** — 这个标题命中了哪种公式？为什么没用上更适合的？
3. **首段抓力** — 钩子词命中了吗？前 3 行能不能让人停？
4. **结构判断** — 这段正文像哪种骨架？该补什么？
5. **类比参考** — 从用户 baseline 里找相似主题的"好"样本对照
6. **演进 / 学习** — 反复同类问题 → 标记为成长方向

输出
====
一组 `Diagnosis(what, why, how, example)`：
- `what`  — 哪里有问题（一句话）
- `why`   — 为什么有问题（原理 / 数据）
- `how`   — 怎么改（一两个具体操作）
- `example` — 改后的样子（可选）

LLM 钩子
========
默认靠规则推理。如果环境变量 `XHS_LLM_PROVIDER` 设置（如 anthropic），
且安装了对应 SDK，会调一次 LLM 把「why / how / example」生成得更具体。
未设置时完全离线。
"""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from xhs_profile import RuleOverride, StyleProfile
from xhs_writer import (
    Draft,
    _EMOJI_RE,
    _count_emoji,
    score_post,
)


# =====================================================================
# 数据结构
# =====================================================================


@dataclass
class Diagnosis:
    where: str               # "title" / "first_lines" / "emoji" / "structure" / "style"
    severity: str            # "high" / "medium" / "low"
    what: str
    why: str
    how: str
    example: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoachReport:
    overall: int                     # 0~100，重用 score_post 总分
    breakdown: Dict[str, int]
    diagnoses: List[Diagnosis]
    growth_hints: List[str]          # 长线成长建议（基于历史 feedback）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": self.overall,
            "breakdown": self.breakdown,
            "diagnoses": [d.to_dict() for d in self.diagnoses],
            "growth_hints": self.growth_hints,
        }


# =====================================================================
# 标题诊断 — 公式 + 风格
# =====================================================================


_FORMULA_FEATURES = {
    "T1": ("数字对比", re.compile(r"^\s*\d+\s*[个件招种]")),
    "T2": ("痛点共情", re.compile(r"为什么|怎么办|不能再")),
    "T3": ("反差冲突", re.compile(r"我以为|没想到|看着.+其实")),
    "T4": ("悬念钩子", re.compile(r"居然|没想到|这一招")),
    "T5": ("身份代入", re.compile(r"^作为")),
    "T6": ("福利免费", re.compile(r"免费|0\s?元|白嫖")),
    "T7": ("时间节点", re.compile(r"\d+\s*年|\d+\s*岁|换季|今年")),
    "T8": ("提问诱发", re.compile(r"是不是|为什么|真的吗|是真是假|\?$|？$")),
    "T9": ("极端结果", re.compile(r"最|第一次|唯一")),
    "T10": ("步骤指南", re.compile(r"保姆级|手把手|从零")),
    "T11": ("故事开场", re.compile(r"上周|那天|朋友说|前几天")),
}


def detect_formula(title: str) -> Optional[str]:
    for code, (_, pat) in _FORMULA_FEATURES.items():
        if pat.search(title):
            return code
    return None


def diagnose_title(title: str, profile: StyleProfile) -> List[Diagnosis]:
    diags: List[Diagnosis] = []
    n = len(title)

    # 长度
    if n < 12:
        diags.append(Diagnosis(
            where="title", severity="high",
            what=f"标题只有 {n} 字，钩子不足",
            why="小红书首页标题黄金区间是 16~22 字，太短信息密度不够、读者一滑就走。",
            how="加上 ① 数字（3/5/7） ② 利益点 ③ 反差词。例如 '5 个 + 名词复数 + 结果'",
            example=f"3 个被严重低估的 {profile.niche or '小习惯'}，{profile.persona or '我'} 体感真的不一样",
        ))
    elif n > 28:
        diags.append(Diagnosis(
            where="title", severity="medium",
            what=f"标题 {n} 字偏长",
            why="超过 26~28 字会被首页截断，截掉的部分往往就是关键词。",
            how="把利益点收口成 1 句话，去掉重复修饰词。",
        ))

    # 公式识别
    formula = detect_formula(title)
    if not formula:
        diags.append(Diagnosis(
            where="title", severity="medium",
            what="标题没有明显的钩子模式",
            why=("爆款标题 90% 命中至少一种公式（数字、痛点、反差、悬念等）。"
                 "无公式 = 平淡叙述句 = 容易被算法和读者一起忽略。"),
            how="选一个公式重写，比如 '为什么...怎么办'（痛点）/ '我以为 X 结果 Y'（反差）",
            example="见 data/title_templates.md",
        ))
    else:
        # 用了公式，但是不是用户自己擅长的？
        favs = profile.favorite_formulas or {}
        if favs and formula not in favs:
            top = max(favs, key=favs.get)
            diags.append(Diagnosis(
                where="title", severity="low",
                what=f"用的公式是 {formula}，但你 baseline 里最常用的是 {top}",
                why="保持公式一致性会让账号画像更清晰，读者形成预期。同时不强求 — 偶尔变换是好事。",
                how=f"如果想稳，参考 baseline 里 {top} 公式的标题；想突破，继续用 {formula}。",
            ))

    # emoji 浮夸
    e = _count_emoji(title)
    if e > 3:
        diags.append(Diagnosis(
            where="title", severity="medium",
            what=f"标题 {e} 个 emoji 偏多",
            why="emoji 多的标题会被识别为低质营销号，掉权重。",
            how="保留 0~2 个最贴主题的，其他删掉。",
        ))

    return diags


# =====================================================================
# 首段诊断
# =====================================================================


_HOOK_PATTERNS = [
    ("代入式提问", re.compile(r"你是不是|你也|你有过|你最近")),
    ("数据冲击", re.compile(r"\d+%|\d+\s?(?:年|个月|天|斤|块|万|w)")),
    ("反差陈述", re.compile(r"我以为|本以为|没想到|结果")),
    ("场景白描", re.compile(r"上周|那天|今天|周\w|早上|晚上")),
]


def diagnose_first_lines(content: str, profile: StyleProfile) -> List[Diagnosis]:
    diags: List[Diagnosis] = []
    head = "\n".join([ln for ln in content.splitlines() if ln.strip()][:3])

    if len(head) < 30:
        diags.append(Diagnosis(
            where="first_lines", severity="high",
            what="首段不到 30 字",
            why="80% 用户只看首 3 行就决定要不要继续读。这里不抓住，后面写得再好也白搭。",
            how="补 1~2 个具体场景或数字，让读者感到'就是说我'。",
            example="✨ 你是不是也遇到过这种情况？\n下午脸又紧又起皮，妆面卡得怀疑人生。",
        ))
        return diags

    matched = [name for name, pat in _HOOK_PATTERNS if pat.search(head)]
    if not matched:
        diags.append(Diagnosis(
            where="first_lines", severity="medium",
            what="首段没有可识别的钩子模式",
            why="爆款首段 4 选 1：① 代入式提问 ② 数据冲击 ③ 反差陈述 ④ 场景白描。"
                "缺了钩子，读者会把它当成普通介绍直接划走。",
            how="选一种钩子重写第一句。",
            example="✨ 你是不是也每次到下午就脸又紧又起皮？/ 上周第一次试这个方法，没想到真的有用。",
        ))
    return diags


# =====================================================================
# 结构 / 排版诊断
# =====================================================================


_SKELETON_HINTS = {
    "S1": ("钩子-痛点-方案-金句", ["📌", "✨", "其实", "方案", "三件"]),
    "S3": ("测评对比", ["对比", "推荐", "回购", "避雷", "🔹"]),
    "S4": ("清单", ["1️⃣", "2️⃣", "整理了", "盘点"]),
    "S5": ("教程", ["Step 1", "保姆级", "步骤", "📦"]),
    "S6": ("观点", ["我认为", "不主流", "反共识", "理由"]),
    "S7": ("Vlog", ["☕", "🌙", "周末", "下午"]),
}


def detect_skeleton(content: str) -> Optional[str]:
    best = None
    best_hits = 0
    for code, (_name, markers) in _SKELETON_HINTS.items():
        hits = sum(1 for m in markers if m in content)
        if hits > best_hits:
            best, best_hits = code, hits
    return best if best_hits >= 2 else None


def diagnose_structure(content: str, profile: StyleProfile) -> List[Diagnosis]:
    diags: List[Diagnosis] = []
    skeleton = detect_skeleton(content)
    if not skeleton:
        diags.append(Diagnosis(
            where="structure", severity="medium",
            what="正文没有可识别的骨架",
            why=("读者扫读时靠 '视觉锚点'（emoji 项目符号 / 步骤词 / 小标题）抓信息。"
                 "无骨架 = 一团文字 = 收藏率低。"),
            how="选一种骨架（S1~S7）重排：每段 1~3 句，关键句用 📌/✨ 当锚点。",
            example="见 data/content_structures.md",
        ))

    # 段落
    lines = content.splitlines()
    long_paragraphs = [ln for ln in lines if len(ln) > 80]
    if len(long_paragraphs) > 2:
        diags.append(Diagnosis(
            where="layout", severity="medium",
            what=f"有 {len(long_paragraphs)} 段超过 80 字",
            why="手机一屏一行约 22 字，超过 80 字 = 4 屏一坨，扫读体验崩。",
            how="把长段在自然停顿处拆成 2~3 行，加空行。",
        ))
    return diags


# =====================================================================
# 风格偏离 — 拿用户自己的 baseline 当尺
# =====================================================================


def diagnose_style_drift(draft: Draft, profile: StyleProfile) -> List[Diagnosis]:
    diags: List[Diagnosis] = []
    if profile.sample_count < 1:
        return diags

    # 标题长度偏离
    if draft.title:
        tl = len(draft.title)
        lo, hi = profile.title_len_range
        if not (lo - 2 <= tl <= hi + 2):
            diags.append(Diagnosis(
                where="style", severity="low",
                what=f"标题 {tl} 字，偏离你常用范围 {lo}~{hi}",
                why="账号画像稳定的核心是 '读者预期一致' — 标题长短跳脱会让算法重新打标。",
                how=f"压缩或扩展到 {lo}~{hi} 字（如果有意尝试新风格可忽略）。",
            ))

    # emoji 偏离
    e = _count_emoji(draft.content)
    if profile.emoji_per_post > 0 and (e < 0.4 * profile.emoji_per_post or e > 2.0 * profile.emoji_per_post):
        diags.append(Diagnosis(
            where="style", severity="low",
            what=f"全文 emoji {e} 个，与你常态（{profile.emoji_per_post}）差较多",
            why="emoji 是你账号 '语气' 的一部分，跳脱也会影响识别度。",
            how=f"调到 {int(profile.emoji_per_post * 0.6)}~{int(profile.emoji_per_post * 1.4)} 之间。",
        ))

    # 口头禅
    if profile.common_phrases:
        any_phrase = any(p in (draft.content + draft.title) for p in profile.common_phrases)
        if not any_phrase:
            diags.append(Diagnosis(
                where="style", severity="low",
                what="文案里没出现你常用的口头禅",
                why=f"baseline 里常出现 {', '.join(profile.common_phrases[:3])}，"
                    "这些是读者认你的 IP 标记。",
                how=f"自然地加 1 处，比如开头或转折。",
            ))

    return diags


# =====================================================================
# 长线成长建议（看反馈历史 + 快照表现）
# =====================================================================


def derive_growth_hints(feedback_log: List[Dict[str, Any]],
                        post_history: List[Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    if not feedback_log and not post_history:
        return out

    # 反馈：哪类规则反复被 reject
    by_rule: Dict[str, int] = {}
    for fb in feedback_log:
        if fb.get("reaction") == "reject":
            k = (fb.get("rule_key") or "").split(":", 1)[0]
            by_rule[k] = by_rule.get(k, 0) + 1
    if by_rule:
        top = max(by_rule, key=by_rule.get)
        if by_rule[top] >= 3:
            out.append(f"📈 你已经多次拒绝「{top}」检查。可以跑 "
                       "`profile_init.py evolve` 让助手自动禁用它。")

    # 历史分数趋势
    scored = [p for p in post_history if isinstance(p.get("score"), (int, float))]
    if len(scored) >= 5:
        recent = sum(p["score"] for p in scored[-5:]) / 5
        early = sum(p["score"] for p in scored[:5]) / 5
        if recent > early + 5:
            out.append(f"📈 最近 5 篇平均分 {recent:.0f}，比早期 5 篇 {early:.0f} 高 — 在进步。")
        elif early > recent + 5:
            out.append(f"📉 最近 5 篇平均分 {recent:.0f}，比早期 {early:.0f} 低 — 注意是否飘了。")
    return out


# =====================================================================
# LLM 钩子（可选）
# =====================================================================


def _maybe_enrich_with_llm(draft: Draft, diagnoses: List[Diagnosis]) -> List[Diagnosis]:
    """如果设置了 XHS_LLM_PROVIDER，调一次 LLM 把每条 diag 的 how/example 写得更具体。

    只是增强；失败静默回退到规则版本。
    """
    provider = os.environ.get("XHS_LLM_PROVIDER", "").lower()
    if not provider:
        return diagnoses
    try:
        if provider == "anthropic":
            return _enrich_anthropic(draft, diagnoses)
    except Exception:
        return diagnoses
    return diagnoses


def _enrich_anthropic(draft: Draft, diagnoses: List[Diagnosis]) -> List[Diagnosis]:
    try:
        from anthropic import Anthropic  # type: ignore
    except ImportError:
        return diagnoses
    client = Anthropic()
    sys_prompt = (
        "你是小红书写作教练。给定一篇笔记草稿和一组诊断，"
        "针对每条诊断，写一句更具体、更可操作的'how'，并给一行示例。"
        "保留原始结构 (where/severity/what/why)，只改 how 和 example。"
    )
    payload = {
        "draft": {"title": draft.title, "content": draft.content[:1200], "tags": draft.tags},
        "diagnoses": [d.to_dict() for d in diagnoses],
    }
    msg = client.messages.create(
        model=os.environ.get("XHS_LLM_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=1500,
        system=sys_prompt,
        messages=[{"role": "user", "content": str(payload)}],
    )
    text = msg.content[0].text if msg.content else ""
    # 简化：失败就直接回退
    import json as _json
    try:
        data = _json.loads(text)
        out = []
        for raw, d in zip(data.get("diagnoses", []), diagnoses):
            d.how = raw.get("how", d.how)
            d.example = raw.get("example", d.example)
            out.append(d)
        return out
    except Exception:
        return diagnoses


# =====================================================================
# 顶层入口
# =====================================================================


def diagnose_allen(draft: Draft) -> List[Diagnosis]:
    """从 Allen 美学体系生成诊断 — 留白 / AI腔 / 教带 / 共鸣 / 邀请。"""
    try:
        from xhs_aesthetic import aesthetic_score
    except ImportError:
        return []
    a = aesthetic_score(draft.title, draft.content)
    out: List[Diagnosis] = []
    label_map = {
        "breath": ("留白度", "Allen 第一课：留白是给读者填情绪的空间"),
        "ai_speak": ("AI 腔", "汇报化 / 模板化词汇会让读者觉得疏离"),
        "teach_vs_lead": ("带读者", "Allen 第一课：从'教读者'到'带读者'"),
        "resonance": ("共鸣度", "Allen 实战教训：场景共鸣 = 共同记忆，不是冷知识"),
        "invitation": ("邀请语", "Allen 第三课：互动是邀请，不是任务指令"),
    }
    for key, info in a.by_dim.items():
        if info["score"] >= 7:
            continue  # 高分项不诊断
        what_label, why_base = label_map.get(key, (key, ""))
        severity = "high" if info["score"] <= 3 else "medium" if info["score"] <= 5 else "low"
        what = (info["issues"][0] if info["issues"] else f"{what_label} 偏低（{info['score']}/10）")
        why = why_base
        how = (info["suggestions"][0] if info["suggestions"] else "见 data/allen_method.md")
        out.append(Diagnosis(
            where="allen",
            severity=severity,
            what=f"【{what_label}】{what}",
            why=why,
            how=how,
            example="",
        ))
    return out


def coach(
    draft: Draft,
    profile: Optional[StyleProfile] = None,
    rules: Optional[RuleOverride] = None,
    feedback_log: Optional[List[Dict[str, Any]]] = None,
    post_history: Optional[List[Dict[str, Any]]] = None,
    *,
    enrich_llm: bool = True,
    include_allen: bool = True,
) -> CoachReport:
    profile = profile or StyleProfile()
    diagnoses: List[Diagnosis] = []
    diagnoses += diagnose_title(draft.title, profile)
    diagnoses += diagnose_first_lines(draft.content, profile)
    diagnoses += diagnose_structure(draft.content, profile)
    diagnoses += diagnose_style_drift(draft, profile)
    if include_allen:
        diagnoses += diagnose_allen(draft)

    if enrich_llm:
        diagnoses = _maybe_enrich_with_llm(draft, diagnoses)

    score = score_post(draft.title, draft.content, draft.tags, rules=rules)
    growth = derive_growth_hints(feedback_log or [], post_history or [])

    return CoachReport(
        overall=score.total,
        breakdown=score.breakdown,
        diagnoses=diagnoses,
        growth_hints=growth,
    )
