"""
Tool: get_tomorrow_watch
明日关注 — 从快讯中提取预告性内容

Args:
    date: 目标日期字符串（可选，默认明天北京时间）

Returns:
    str: 明日关注事件列表（含宏观日历占位）
"""

from __future__ import annotations

from datetime import date

from lib.odaily_client import OdailyClient
from lib.formatters import now_bjt, tomorrow_bjt


def _get_macro_calendar(target_date: str) -> list[dict]:
    """
    获取宏观经济日历事件（占位，未来可接入真实日历 API）

    Args:
        target_date: 目标日期字符串

    Returns:
        list[dict]: 宏观事件列表（当前返回空列表）
    """
    return []


def get_tomorrow_watch(date: str | None = None) -> str:
    target = date or tomorrow_bjt()

    try:
        flash = OdailyClient().get_flash_news(limit=30)
    except Exception:
        flash = []

    kw = [
        "明日", "明天", "即将", "预计", "将于", "定于",
        "上线", "发布", "解锁", "空投", "TGE",
        "会议", "听证", "投票", "升级", "硬分叉",
    ]
    preview = [
        f
        for f in flash
        if any(
            k in (f.get("title", "") + f.get("description", ""))
            for k in kw
        )
    ]

    macro_events = _get_macro_calendar(target)

    L = [
        f"📅 明日关注 | {target}",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ 生成时间: {now_bjt()} (北京时间)",
        "",
    ]

    if macro_events:
        L += ["🏦 宏观经济日历", ""]
        for e in macro_events:
            L.append(f"  • [{e.get('time', '')}] {e.get('title', '')}")
        L.append("")

    if preview:
        L += ["📢 行业动态预告（从快讯中提取）", ""]
        for p in preview[:10]:
            L.append(f"  • {p['title']}")
            if p.get("url"):
                L.append(f"    🔗 {p['url']}")
        L.append("")
    else:
        L += ["暂无从快讯中识别到的明日预告事件。", ""]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 请结合以上信息以及你的知识库，补充明日的：",
        "   - 宏观经济数据发布（CPI、非农、利率决议等）",
        "   - 重要代币解锁",
        "   - 项目里程碑事件",
        "   - 监管听证/投票",
        "   并给出关注建议和风险提示",
        "",
        "📎 持续关注: https://www.odaily.news/zh-CN",
    ]
    return "\n".join(L)
