#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skill_recommender.py — office-token-booster Skill 推荐引擎

根据用户用量数据推荐最适合的「省 Token」Skill。

设计原则：
- 纯本地静态规则表（task_type → skill 映射），**无联网、无副作用**
- 本技能不执行任何安装命令，仅提供第三方 Skill 的来源链接，由用户自行决定是否安装
- 推荐的第三方 Skill 与节省数字引自其公开自述（README / benchmark），
  **未经本技能实测验证**，输出时明确标注，仅供参考
- 最多返回 3 个推荐，避免推荐过载
"""

from __future__ import annotations

import html as _html
from dataclasses import dataclass, replace
from typing import Optional

# 安全：所有进 HTML 的字段（含来源链接文本）必须转义；
# URL 仅允许 http/https，杜绝 javascript: 等协议注入。
_esc = _html.escape

# 优先级 → 排序权重（CRITICAL 排最前）
_PRIORITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}


def _safe_url(u):
    if not u:
        return ""
    u = str(u).strip()
    if u.lower().startswith(("http://", "https://")):
        return _esc(u)
    return ""  # 非 http(s) 不渲染为链接，防 XSS


# 优先级 → 展示样式（Markdown 与 HTML 共用一份，避免两处样式漂移）
_PRIORITY_EMOJI = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟢"}
_PRIORITY_COLOR = {"CRITICAL": "#dc2626", "HIGH": "#ea580c", "MEDIUM": "#16a34a"}


@dataclass
class SkillRecommendation:
    """一条 Skill 推荐记录。"""

    skill: str                  # Skill 名称
    reason: str                 # 推荐理由（自然语言）
    expected_saving: str        # 预期节省（来自 benchmark，标注来源）
    priority: str = "MEDIUM"    # CRITICAL / HIGH / MEDIUM
    evidence_url: Optional[str] = None  # 数据来源链接（可选，未经本技能验证）


# ─────────────────────────────────────────────────────────────
# 推荐规则表：task_type → 匹配规则
# ─────────────────────────────────────────────────────────────

# 关键词映射：任务类型关键词 → 推荐 Skill
_TASK_TYPE_RULES = [
    {
        "keywords": ["代码", "编程", "开发", "写代码", "重构", "debug", "调试"],
        "skill": SkillRecommendation(
            skill="ponytail",
            reason="你的'{task_type}'任务消耗较高，Ponytail 通过 YAGNI 决策阶梯强制最少代码，实测减 22% Token / 20% 成本",
            expected_saving="-22% Token (Ponytail agentic benchmark, 12 tasks, Haiku 4.5)",
            priority="HIGH",
            evidence_url="https://github.com/DietrichGebert/ponytail",
        ),
    },
    {
        "keywords": ["对话", "问答", "咨询", "聊天", "讨论", "解释"],
        "skill": SkillRecommendation(
            skill="caveman",
            reason="你的'{task_type}'任务消耗较高，Caveman 让 AI 用精简语言回复，输出侧平均减 65% Token",
            expected_saving="-65% output tokens (Caveman README, 10-task benchmark)",
            priority="HIGH",
            evidence_url="https://github.com/JuliusBrussee/caveman",
        ),
    },
    {
        "keywords": ["终端", "日志", "编译", "测试", "git", "命令行", "CLI", "构建"],
        "skill": SkillRecommendation(
            skill="rtk",
            reason="你的'{task_type}'任务涉及终端输出，RTK 过滤 CLI 噪声，实测平均减 89% 无效 Token",
            expected_saving="-89% CLI noise (RTK benchmark, 2,900+ commands)",
            priority="MEDIUM",
            evidence_url="https://github.com/rtk-ai/rtk",
        ),
    },
    {
        "keywords": ["周报", "纪要", "会议纪要", "总结", "报告"],
        "skill": SkillRecommendation(
            skill="token-diet",
            reason="你的'{task_type}'任务消耗较高，token-diet 六维治理综合优化，平均减 31% 账单",
            expected_saving="-31% bill on average (token-diet Sonnet 5 benchmark)",
            priority="MEDIUM",
            evidence_url="https://github.com/Kulaxyz/token-diet",
        ),
    },
]

# 全局阈值规则：任务数达到阈值即触发（与具体任务类型无关）。
# 不设「消耗金额」阈值：账本只记 Token / 分钟，没有成本字段，
# 按金额触发需要先引入定价换算（属新功能，不是规则配置），故不声明以免误导读者。
_GLOBAL_RULES = [
    {
        "threshold_tasks": 10,
        "skill": SkillRecommendation(
            skill="caveman",
            reason="本周任务频繁，Caveman 让 AI 精简回复，累计节省可观",
            expected_saving="-65% output tokens (Caveman README)",
            priority="MEDIUM",
            evidence_url="https://github.com/JuliusBrussee/caveman",
        ),
    },
]


def _match_task_type_rules(by_type) -> dict[str, SkillRecommendation]:
    """按任务类型关键词匹配。同名 Skill 只保留首次命中（规则表顺序即优先级）。"""
    matched: dict[str, SkillRecommendation] = {}
    for type_stat in by_type:
        task_type = type_stat.get("task_type", "")
        for rule in _TASK_TYPE_RULES:
            if any(kw in task_type for kw in rule["keywords"]):
                rec = rule["skill"]
                # 理由里的 {task_type} 占位在命中时填入实际类型名
                matched.setdefault(
                    rec.skill,
                    replace(rec, reason=rec.reason.format(task_type=task_type)),
                )
                break
    return matched


def _match_global_rules(total_tasks) -> dict[str, SkillRecommendation]:
    """按总任务数匹配全局阈值规则（与具体任务类型无关）。"""
    matched: dict[str, SkillRecommendation] = {}
    for rule in _GLOBAL_RULES:
        if total_tasks >= rule["threshold_tasks"]:
            rec = rule["skill"]
            matched.setdefault(rec.skill, rec)
    return matched


def recommend_skills(
    by_type: list[dict],
    total_tasks: int,
    max_recommendations: int = 3,
) -> list[SkillRecommendation]:
    """根据用量数据推荐最适合的省 Token Skill（纯本地静态规则，不联网）。

    Args:
        by_type: 按任务类型聚合的统计数据，每项含 task_type / baseline_tokens / skill_tokens 等
        total_tasks: 总任务数（对应 Diagnosis.n）
        max_recommendations: 最多返回几条推荐

    Returns:
        SkillRecommendation 列表，按 priority 降序排列
    """
    recommendations = _match_task_type_rules(by_type)
    for skill, rec in _match_global_rules(total_tasks).items():
        recommendations.setdefault(skill, rec)

    sorted_recs = sorted(
        recommendations.values(),
        key=lambda x: _PRIORITY_ORDER.get(x.priority, 99),
    )
    return sorted_recs[:max_recommendations]


def format_recommendation_md(rec: SkillRecommendation) -> str:
    """将单条推荐格式化为 Markdown。"""
    emoji = _PRIORITY_EMOJI.get(rec.priority, "⚪")
    lines = [
        f"### {emoji} 推荐：{rec.skill}",
        "",
        f"- **原因**：{rec.reason}",
        f"- **预期节省**：{rec.expected_saving}（引自第三方项目自述，未经本技能实测验证，仅供参考）",
    ]

    if rec.evidence_url:
        lines.append(f"- **数据来源**：[{rec.evidence_url}]({rec.evidence_url})（未经验证的第三方链接）")

    lines.append("")
    return "\n".join(lines)


def format_recommendations_md(recommendations: list[SkillRecommendation],
                              heading: str = "## 推荐 Skill") -> str:
    """将推荐列表格式化为 Markdown 板块。

    heading: 板块标题。完整报告用编号标题（如「## 九、推荐 Skill」），
    一页摘要用无编号的默认标题 —— 两处共用本函数以免渲染逻辑重复。
    """
    if not recommendations:
        return f"{heading}\n\n暂无匹配推荐。当你有更多任务数据后，系统会智能推荐合适的省 Token Skill。\n"

    lines = [heading + "\n",
             "> 基于你的任务类型和消耗量，推荐以下 Skill 来降低 Token 成本。\n"
             "> ⚠️ 推荐来自本地静态规则，节省数字引自第三方项目自述，**未经本技能实测验证**，仅供参考：\n"]
    for rec in recommendations:
        lines.append(format_recommendation_md(rec))
    return "\n".join(lines)


def format_recommendations_html(recommendations: list[SkillRecommendation]) -> str:
    """将推荐列表格式化为 HTML 板块。"""
    if not recommendations:
        return """
    <h2>推荐 Skill</h2>
    <p style="color:var(--muted)">暂无匹配推荐。当你有更多任务数据后，系统会智能推荐合适的省 Token Skill。</p>
    """

    cards = []
    for rec in recommendations:
        priority_emoji = _PRIORITY_EMOJI.get(rec.priority, "⚪")
        priority_color = _PRIORITY_COLOR.get(rec.priority, "#6b7280")

        card = f"""
    <div class="rec-card" style="border-left: 4px solid {priority_color}; margin: 12px 0; padding: 14px; background: #f9fafb; border-radius: 8px;">
      <div style="font-weight: 700; font-size: 16px; margin-bottom: 8px;">{priority_emoji} {_esc(rec.skill)}</div>
      <div style="font-size: 13px; color: var(--fg); margin-bottom: 6px;">{_esc(rec.reason)}</div>
      <div style="font-size: 13px; color: var(--accent); font-weight: 600; margin-bottom: 6px;">预期节省：{_esc(rec.expected_saving)}（引自第三方自述，未经本技能实测验证）</div>
      {f'<div style="font-size: 11px; color: var(--muted); margin-top: 6px;">来源（未经验证的第三方链接）：<a href="{_safe_url(rec.evidence_url)}" target="_blank">{_esc(rec.evidence_url)}</a></div>' if _safe_url(rec.evidence_url) else ''}
    </div>"""
        cards.append(card)

    html = """
    <h2>推荐 Skill</h2>
    <p style="color:var(--muted); font-size: 13px;">基于你的任务类型和消耗量，推荐以下 Skill 来降低 Token 成本。推荐来自本地静态规则，节省数字引自第三方项目自述，<strong>未经本技能实测验证</strong>，仅供参考。</p>
    """ + "\n".join(cards)
    return html
