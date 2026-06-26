"""消息模板系统 — Jinja2 模板 + 分级播报策略。"""

from datetime import datetime
from typing import Any

from jinja2 import Environment, BaseLoader


# -- Jinja2 模板定义 --

IMMEDIATE_TEMPLATE = """\
### {{ novel.title }} 更新了！

- **站点**: {{ novel.site }}
- **作者**: {{ novel.author or '未知' }}
- **分级**: {{ novel.grade }}
- **新增内容**: {{ new_count }} 章/集
{% if chapters %}
{% for ch in chapters[:5] %}
  - {{ ch.title }}
{% endfor %}
{% if chapters|length > 5 %}
  - ...及其他 {{ chapters|length - 5 }} 章
{% endif %}
{% endif %}
{% if novel.url %}
- [查看原文]({{ novel.url }})
{% endif %}

> 更新时间: {{ now }}
"""

DAILY_DIGEST_TEMPLATE = """\
### 今日更新汇总 ({{ date }})

共 {{ novels|length }} 部作品有更新：

{% for item in novels %}
**{{ loop.index }}. {{ item.novel.title }}** ({{ item.novel.site }})
  - 新增 {{ item.new_count }} 章/集
  - 分级: {{ item.novel.grade }}
{% endfor %}

> 生成时间: {{ now }}
"""

WEEKLY_DIGEST_TEMPLATE = """\
### 本周更新汇总 ({{ week_start }} ~ {{ week_end }})

共 {{ novels|length }} 部作品有更新：

{% for item in novels %}
**{{ loop.index }}. {{ item.novel.title }}** ({{ item.novel.site }})
  - 累计更新 {{ item.new_count }} 章/集
  - 分级: {{ item.novel.grade }}
  - 状态: {{ item.novel.status }}
{% endfor %}

> 生成时间: {{ now }}
"""

# -- 模板渲染 --

_env = Environment(loader=BaseLoader())


def render_immediate(novel: Any, chapters: list[Any] | None = None, new_count: int = 0) -> str:
    """渲染即时播报消息。

    Args:
        novel: Novel 模型实例。
        chapters: 新增章节列表。
        new_count: 新增数量。

    Returns:
        Markdown 格式消息。
    """
    template = _env.from_string(IMMEDIATE_TEMPLATE)
    return template.render(
        novel=novel,
        chapters=chapters or [],
        new_count=new_count,
        now=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
    )


def render_daily_digest(novels: list[dict[str, Any]]) -> str:
    """渲染日汇总消息。

    Args:
        novels: [{"novel": Novel, "new_count": int}, ...] 列表。

    Returns:
        Markdown 格式消息。
    """
    template = _env.from_string(DAILY_DIGEST_TEMPLATE)
    return template.render(
        novels=novels,
        date=datetime.utcnow().strftime("%Y-%m-%d"),
        now=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
    )


def render_weekly_digest(novels: list[dict[str, Any]], week_start: str = "", week_end: str = "") -> str:
    """渲染周汇总消息。

    Args:
        novels: [{"novel": Novel, "new_count": int}, ...] 列表。
        week_start: 周起始日期。
        week_end: 周结束日期。

    Returns:
        Markdown 格式消息。
    """
    now = datetime.utcnow()
    template = _env.from_string(WEEKLY_DIGEST_TEMPLATE)
    return template.render(
        novels=novels,
        week_start=week_start or now.strftime("%Y-%m-%d"),
        week_end=week_end or now.strftime("%Y-%m-%d"),
        now=now.strftime("%Y-%m-%d %H:%M"),
    )


# -- 分级播报策略 --

STRATEGY_MAP = {
    "high": "immediate",
    "medium": "daily_digest",
    "low": "weekly_digest",
}


def get_broadcast_strategy(grade: str) -> str:
    """根据分级获取播报策略。

    Args:
        grade: 内容分级。

    Returns:
        策略名称。
    """
    return STRATEGY_MAP.get(grade, "weekly_digest")
