#!/usr/bin/env python3
# modules/reporter.py - 每日热点报告生成器 v3
"""
生成结构化的每日热点日报（Markdown格式）
包含：跨平台共振 + AI专题热报 + 生命周期 + PM洞察 + 选题建议
"""
import sys, os, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LIFECYCLE_EMOJI = {'新兴': '🆕', '爆发中': '🔥', '持续发酵': '📈', '衰减中': '📉'}

PLATFORM_EMOJI = {
    '知乎': '💬', '知乎热榜': '💬', '微博': '🌐', '微博热搜': '🌐',
    '抖音': '🎵', '抖音热点': '🎵', 'B站': '📺', '小红书': '📕',
    '36氪': '📌', '36krAI': '🤖', '虎嗅': '🐯', '雷锋网': '🔧', 'IT之家': '💻',
    '爱范儿': '📱', '界面新闻': '🏢', '今日热榜': '📊',
    'YouTube': '▶️', 'X/Twitter': '𝕏', 'Twitter趋势': '𝕏',
    'Instagram': '📷', 'TechCrunch': '🌍', 'The Verge': '🌍',
    'Wired': '🌍', 'Engadget': '🌍', 'Ars Technica': '🌍',
    '量子位': '🤖', 'AIbase': '🤖', 'AI产品榜': '🤖',
    'PM-AI学习库': '🤖', '掘金AI': '🤖', '超神经': '🤖',
    '华尔街见闻': '💹', '雪球': '🎱', '21财经': '📊', '格隆汇': '📈', '第一财经': '🏦', '新浪财经': '📰', '集思录': '🔖',
}

OVERSEAS_PLATFORMS = {'TechCrunch', 'The Verge', 'Wired', 'Engadget', 'Ars Technica'}

# AI 专题平台（重点关注板块）
AI_PLATFORMS = {
    '36krAI': {'name': '36氪AI', 'desc': '创投视角', 'emoji': '📌'},
    '量子位': {'name': '量子位', 'desc': 'AI行业媒体', 'emoji': '🤖'},
    'AIbase': {'name': 'AIbase', 'desc': 'AI产品日报', 'emoji': '📰'},
    'AI产品榜': {'name': 'AI产品榜', 'desc': '产品动态速递', 'emoji': '🚀'},
    'PM-AI学习库': {'name': 'PM-AI学习库', 'desc': 'PM专属内容', 'emoji': '📚'},
    '掘金AI': {'name': '掘金AI', 'desc': '技术实战', 'emoji': '⌨️'},
    '超神经': {'name': '超神经', 'desc': '学术/开源进展', 'emoji': '🔬'},
}

# 财经专题平台（重点关注板块）
FINANCE_PLATFORMS = {
    '华尔街见闻': {'name': '华尔街见闻', 'desc': '宏观/市场', 'emoji': '💹'},
    '雪球': {'name': '雪球', 'desc': '投资社区', 'emoji': '🎱'},
    '21财经': {'name': '21财经', 'desc': '财经热点', 'emoji': '📊'},
    '格隆汇': {'name': '格隆汇', 'desc': '投资研判', 'emoji': '📈'},
    '第一财经': {'name': '第一财经', 'desc': '商业财经', 'emoji': '🏦'},
    '新浪财经': {'name': '新浪财经', 'desc': '点击量排行', 'emoji': '📰'},
    '集思录': {'name': '集思录', 'desc': '低风险投资', 'emoji': '🔖'},
}


def _html_escape(text):
    """清理 HTML 实体"""
    return (text
        .replace('&#8212;', '—').replace('&#8216;', "'").replace('&#8217;', "'")
        .replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        .replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' '))


def _safe_resonance(item, all_items):
    """安全获取共鸣度"""
    try:
        from .analyzer import resonance_score
        return resonance_score(item, all_items)
    except Exception:
        return item.get('resonance', 0)


def generate_report(date, raw, analysis):
    scored = analysis.get('scored', [])
    stats = analysis.get('stats', {})
    history_ok = analysis.get('summary', {}).get('history_loaded', False)

    # 提取 AI 专题数据
    ai_platforms_in_raw = {k: v for k, v in raw.items() if k in AI_PLATFORMS}
    total_ai_items = sum(len(v) for v in ai_platforms_in_raw.values())

    # 提取财经专题数据
    finance_platforms_in_raw = {k: v for k, v in raw.items() if k in FINANCE_PLATFORMS}
    total_finance_items = sum(len(v) for v in finance_platforms_in_raw.values())

    # 跨平台共振
    cross_platform = [i for i in scored if i.get('platform_count', 1) >= 2]
    cross_platform.sort(key=lambda x: _safe_resonance(x, scored), reverse=True)

    # 爆发 + 持续
    peak_items = sorted(
        [i for i in scored if i.get('lifecycle') == '爆发中' and _safe_resonance(i, scored) >= 6],
        key=lambda x: _safe_resonance(x, scored), reverse=True
    )
    sustain_items = sorted(
        [i for i in scored if i.get('lifecycle') == '持续发酵' and _safe_resonance(i, scored) >= 5],
        key=lambda x: _safe_resonance(x, scored), reverse=True
    )

    total_items = sum(len(v) for v in raw.values())
    total_ai_items = sum(len(v) for v in ai_platforms_in_raw.values())

    # ================================================
    # 构建报告
    # ================================================
    md = f"""# 📡 热点日报 · {date}

> 本报告由热点收集雷达自动生成 · 共追踪 {total_items} 条热点，覆盖 {len(raw)} 个平台
{"（含 AI/财经 专题重点关注）" if ai_platforms_in_raw else ""}

---

## ⭐ 跨平台共振话题

"""

    if cross_platform:
        for item in cross_platform[:3]:
            emoji = LIFECYCLE_EMOJI.get(item.get('lifecycle', ''), '📌')
            score = _safe_resonance(item, scored)
            platforms_str = '、'.join(sorted({
                i.get('platform', '') for i in scored if i.get('title') == item.get('title')
            }))[:30]
            md += f"""### {emoji} {item.get('title', '')[:45]}

- **平台**: {platforms_str}
- **生命周期**: {item.get('lifecycle', '持续发酵')}
- **共鸣度**: ⭐{score}
- **主题**: {item.get('theme', '其他')}

"""
    else:
        md += "> 今日暂无明显的跨平台共振话题。\n\n"

    # 提取财经专题数据
    finance_platforms_in_raw = {k: v for k, v in raw.items() if k in FINANCE_PLATFORMS}
    total_finance_items = sum(len(v) for v in finance_platforms_in_raw.values())

    # ================================================
    # 🤖 AI 专题热报（重点板块）
    # ================================================
    if ai_platforms_in_raw:
        md += f"""---

## 🤖 AI 专题热报（重点关注）

> 来源：tophub.today/c/ai · 共 {total_ai_items} 条

"""

        for platform, items in ai_platforms_in_raw.items():
            if not items:
                continue
            info = AI_PLATFORMS.get(platform, {})
            emoji = info.get('emoji', '🤖')
            desc = info.get('desc', '')
            md += f"### {emoji} **{info.get('name', platform)}**（{desc}）\n\n"
            for item in items[:5]:  # 每源展示前5条
                title = _html_escape(item.get('title', '')[:60])
                link = item.get('link', '')
                hot = item.get('hot', '')
                if link and not link.startswith('javascript'):
                    md += f"- {title}{' · ' + hot if hot else ''}\n"
                else:
                    md += f"- {title}{' · ' + hot if hot else ''}\n"
            md += "\n"


    # ================================================
    # 财经专题热报（重点板块）
    # ================================================
    if finance_platforms_in_raw:
        md += """

---

## 财经专题热报（重点关注）

> 来源：tophub.today/c/finance · 共 35 条

"""
        for platform, items in finance_platforms_in_raw.items():
            if not items:
                continue
            info = FINANCE_PLATFORMS.get(platform, {})
            emoji = info.get('emoji', '💹')
            desc = info.get('desc', '')
            md += f"### {emoji} **{info.get('name', platform)}**（{desc}）\n\n"
            for item in items[:5]:
                title = _html_escape(item.get('title', '')[:60])
                link = item.get('link', '')
                hot = item.get('hot', '')
                if link and not link.startswith('javascript'):
                    md += f"- {title}{' · ' + hot if hot else ''}\n"
                else:
                    md += f"- {title}{' · ' + hot if hot else ''}\n"
            md += "\n"

    # ================================================
    # 热点排行榜
    # ================================================
    md += """---

## 🔥 热点 Top 10

"""
    md += "| # | 话题 | 平台 | 生命周期 | 共鸣度 |\n"
    md += "|---|------|------|---------|--------|\n"
    for i, item in enumerate(scored[:10], 1):
        lc = item.get('lifecycle', '衰减中')
        lc_sym = LIFECYCLE_EMOJI.get(lc, '📌')
        score = _safe_resonance(item, scored)
        md += f"| {i} | {item.get('title', '')[:22]} | {item.get('platform', '')[:5]} | {lc_sym}{lc} | ⭐{score} |\n"

    # ================================================
    # 海外科技头条
    # ================================================
    md += """

---

## 🌍 海外科技头条

"""
    for platform in OVERSEAS_PLATFORMS:
        platform_data = raw.get(platform, [])
        if not platform_data:
            continue
        emoji = PLATFORM_EMOJI.get(platform, '🌍')
        md += f"### {emoji} **{platform}**\n\n"
        for item in platform_data[:3]:
            title = _html_escape(item.get('title', '')[:60])
            excerpt = _html_escape(item.get('excerpt', '') or '')[:147].strip()
            link = item.get('link', '')
            if excerpt:
                md += f"- **{title}**\n  {excerpt}...\n"
            else:
                md += f"- **{title}**\n"
            if link:
                md += f"  🔗 [阅读原文]({link})\n"
            md += '\n'

    # ================================================
    # 选题建议
    # ================================================
    md += """---

## 🎯 今日选题建议

"""

    # AI 专题选题建议（优先）
    if ai_platforms_in_raw:
        # 直接从 AI 专题数据中提取有价值的话题
        ai_keywords_lower = ['AI', 'Claude', 'DeepSeek', 'GPT', 'Agent', '大模型', 'Copilot',
                           'Codex', '算力', 'LLM', 'AIGC', '具身', '人形', '模型', '智能']
        for platform, items in ai_platforms_in_raw.items():
            for item in items:
                item['_platform'] = platform
                if any(kw.lower() in item.get('title', '').lower() for kw in ai_keywords_lower):
                    item['_is_ai_topic'] = True

        ai_related = [i for i in scored if any(
            kw.lower() in i.get('title', '').lower()
            for kw in ['AI', 'Claude', 'DeepSeek', 'GPT', 'Agent', '大模型', 'Copilot', 'Codex', '算力', 'LLM', 'AIGC', '具身']
        )]

        if ai_related or ai_platforms_in_raw:
            md += "### 🤖 AI 专题选题\n\n"
            # 先从 AI 专题找相关话题
            ai_top_from_raw = [
                i for platform, items in ai_platforms_in_raw.items()
                for i in items
                if i.get('_is_ai_topic') or any(kw.lower() in i.get('title', '').lower()
                    for kw in ai_keywords_lower)
            ][:6]
            if ai_top_from_raw:
                for item in ai_top_from_raw:
                    title = item.get('title', '')[:42]
                    platform = item.get('_platform', item.get('platform', ''))
                    # 用 analyzer 提取选题建议
                    from .analyzer import detect_theme
                    item['theme'] = detect_theme(title)
                    from .analyzer import pm_topic_suggestion
                    sg = pm_topic_suggestion(item)
                    md += f"""**{title}**

- 来源：{platform}
- 选题角度：{sg['angle']}
- 内容切入点：{sg['take']}
- 适合形式：{sg['form']}

"""
            elif ai_related:
                for item in ai_related[:5]:
                    from .analyzer import pm_topic_suggestion
                    sg = pm_topic_suggestion(item)
                    score = _safe_resonance(item, scored)
                    lc = item.get('lifecycle', '衰减中')
                    lc_sym = LIFECYCLE_EMOJI.get(lc, '📌')
                    md += f"""**{item.get('title', '')[:42]}** ({lc_sym}{lc})

- 共鸣度：⭐{score}
- 选题角度：{sg['angle']}
- 内容切入点：{sg['take']}
- 适合形式：{sg['form']}
- {sg['timing']}

"""

    # 爆发/持续话题
    if peak_items:
        md += "### 🔴 第一梯队：爆发中话题\n\n"
        for item in peak_items[:3]:
            from .analyzer import pm_topic_suggestion
            sg = pm_topic_suggestion(item)
            score = _safe_resonance(item, scored)
            md += f"""**{item.get('title', '')[:42]}**

- 共鸣度：⭐{score}
- 选题角度：{sg['angle']}
- 内容切入点：{sg['take']}
- 适合形式：{sg['form']}
- {sg['timing']}

"""

    if sustain_items:
        md += "### 🟡 第二梯队：持续发酵话题\n\n"
        used_titles = {i.get('title') for i in peak_items}
        for item in sustain_items:
            if item.get('title') in used_titles:
                continue
            from .analyzer import pm_topic_suggestion
            sg = pm_topic_suggestion(item)
            score = _safe_resonance(item, scored)
            md += f"""**{item.get('title', '')[:42]}**

- 共鸣度：⭐{score}
- 选题角度：{sg['angle']}
- 内容切入点：{sg['take']}
- 适合形式：{sg['form']}
- {sg['timing']}

"""
            if len([i for i in sustain_items if i.get('title') not in used_titles]) >= 3:
                break

    # ================================================
    # 平台数据摘要
    # ================================================
    md += """---

## 📊 平台数据摘要

"""
    for platform, info in stats.items():
        if info.get('count', 0) == 0:
            continue
        emoji = PLATFORM_EMOJI.get(platform, '📌')
        top = info.get('top', '')[:35]
        md += f"| {emoji} **{platform}** | {info.get('count', 0)}条 | {top or '无'} |\n"

    # ================================================
    # PM 洞察
    # ================================================
    md += "\n---\n\n## 💡 PM 洞察\n\n"
    for item in scored[:5]:
        title = item.get('title', '')[:35]
        lc = item.get('lifecycle', '衰减中')
        from .analyzer import pm_topic_suggestion
        sg = pm_topic_suggestion(item)
        lc_sym = LIFECYCLE_EMOJI.get(lc, '📌')
        md += f"**{title}**\n\n{lc_sym} **{lc}**：{sg['angle']} — {sg['take']}\n\n"

    md += f"\n---\n\n*报告生成时间: {date} · 由热点收集雷达自动分析*\n"
    return md


if __name__ == '__main__':
    print('PM reporter module loaded OK')
