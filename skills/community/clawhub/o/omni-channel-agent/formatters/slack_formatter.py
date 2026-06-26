"""
Slack Report Formatter — outputs Slack-ready code block tables.
"""
from datetime import datetime

def format_number(n):
    """Format large numbers: 1234567 → 123.5万"""
    if not n: return "N/A"
    if n >= 100_000_000: return f"{n/100_000_000:.1f}亿"
    if n >= 10_000: return f"{n/10_000:.1f}万"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return str(n)


def format_tiktok_report(trends: list, query: str, region: str = "US") -> str:
    header = f"🎵 TikTok 热门内容 — {query}\n📅 {datetime.utcnow().strftime('%Y-%m-%d')} | 🇺🇸 {region}\n"
    lines = [header, "```"]
    lines.append(f"{'排名':4s} {'描述':<40s} {'播放量':>10s} {'点赞':>8s} {'评论':>6s} {'分享':>6s}")
    lines.append("─" * 80)
    for i, t in enumerate(trends[:10], 1):
        lines.append(
            f"{i:>3d}  {t['desc'][:38]:<40s} {format_number(t['plays']):>10s} "
            f"{format_number(t['likes']):>8s} {format_number(t['comments']):>6s} {format_number(t['shares']):>6s}"
        )
    lines.append("```")
    return "\n".join(lines)


def format_instagram_report(trends: list, query: str, region: str = "US") -> str:
    header = f"📸 Instagram 热门内容 — #{query}\n📅 {datetime.utcnow().strftime('%Y-%m-%d')} | 🇺🇸 {region}\n"
    lines = [header, "```"]
    lines.append(f"{'排名':4s} {'作者':<22s} {'类型':<8s} {'点赞':>10s} {'评论':>8s} {'播放':>10s}")
    lines.append("─" * 70)
    for i, t in enumerate(trends[:10], 1):
        lines.append(
            f"{i:>3d}  @{t['owner'][:20]:<22s} {t.get('type','post')[:6]:<8s} "
            f"{format_number(t['likes']):>10s} {format_number(t['comments']):>8s} {format_number(t.get('views',0)):>10s}"
        )
    lines.append("```")
    return "\n".join(lines)


def format_facebook_ads_report(ads: list, query: str) -> str:
    header = f"📢 Facebook Ads 竞品监控 — \"{query}\"\n📅 {datetime.utcnow().strftime('%Y-%m-%d')} | 按曝光排序\n"
    lines = [header, "```"]
    lines.append(f"{'#':>3s}  {'广告主':<30s} {'投放起始':<12s} {'状态':<6s} {'CTA':<15s} {'文案摘要'}")
    lines.append("─" * 100)
    for i, ad in enumerate(ads[:15], 1):
        status = "🟢投" if ad.get("isActive") else "🔴停"
        body = (ad.get("body", "") or "")[:30]
        lines.append(
            f"{i:>3d}  {ad['pageName'][:28]:<30s} {ad.get('startDate','')[:10]:<12s} "
            f"{status:<6s} {ad.get('ctaText','')[:13]:<15s} {body}"
        )
    lines.append("```")
    return "\n".join(lines)


def format_youtube_report(trends: list, query: str) -> str:
    header = f"▶️ YouTube 热门视频 — \"{query}\"\n📅 {datetime.utcnow().strftime('%Y-%m-%d')}\n"
    lines = [header, "```"]
    lines.append(f"{'#':>3s}  {'标题':<45s} {'播放量':>10s} {'频道':<20s}")
    lines.append("─" * 85)
    for i, t in enumerate(trends[:10], 1):
        lines.append(
            f"{i:>3d}  {t['title'][:43]:<45s} {format_number(t['views']):>10s} {t['channel'][:18]:<20s}"
        )
    lines.append("```")
    return "\n".join(lines)


def format_reddit_report(trends: list, query: str) -> str:
    header = f"🔥 Reddit 热门讨论 — \"{query}\"\n📅 {datetime.utcnow().strftime('%Y-%m-%d')}\n"
    lines = [header, "```"]
    lines.append(f"{'#':>3s}  {'子版块':<22s} {'⬆️':>6s} {'💬':>5s} {'标题'}")
    lines.append("─" * 80)
    for i, t in enumerate(trends[:10], 1):
        lines.append(
            f"{i:>3d}  r/{t['subreddit'][:18]:<22s} {t['upvotes']:>6,} {t['comments']:>5,} {t['title'][:35]}"
        )
    lines.append("```")
    return "\n".join(lines)


def format_google_trends_report(data: dict) -> str:
    header = f"📈 Google Trends 搜索趋势\n📅 {datetime.utcnow().strftime('%Y-%m-%d')} | 🇺🇸 US\n"
    lines = [header]
    
    # Trending searches
    if data.get("trending_searches"):
        lines.append("*今日热搜 Top 10:*")
        lines.append("```")
        for i, t in enumerate(data["trending_searches"][:10], 1):
            lines.append(f"  {i:>2d}. {t}")
        lines.append("```")
    
    # Related queries
    if data.get("related_queries"):
        lines.append("\n*关键词关联查询:*")
        lines.append("```")
        for kw, queries in data["related_queries"].items():
            lines.append(f"\n  [{kw}]")
            for q in (queries or [])[:5]:
                lines.append(f"    → {q.get('query',''):30s} (热度: {q.get('value',0)})")
        lines.append("```")
    
    return "\n".join(lines)


def format_full_report(all_data: dict) -> str:
    """Combine all reports into one comprehensive Slack message."""
    sections = []
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    sections.append(f"🔥 *社媒热点速报 — {ts}*\n📅 近1周 | 🇺🇸 美国\n")
    
    if "tiktok" in all_data:
        sections.append(format_tiktok_report(all_data["tiktok"], "AI Filter/Photo"))
    if "instagram" in all_data:
        sections.append(format_instagram_report(all_data["instagram"], "aifilter"))
    if "youtube" in all_data:
        sections.append(format_youtube_report(all_data["youtube"], "AI Filter"))
    if "facebook_ads" in all_data:
        sections.append(format_facebook_ads_report(all_data["facebook_ads"], "ai photo generator"))
    if "reddit" in all_data:
        sections.append(format_reddit_report(all_data["reddit"], "AI Filter"))
    if "google_trends" in all_data:
        sections.append(format_google_trends_report(all_data["google_trends"]))
    
    sections.append("\n💡 切换区域：发送 \"查看欧洲\" / \"查看亚洲\" / \"查看全部\"")
    
    return "\n\n".join(sections)
