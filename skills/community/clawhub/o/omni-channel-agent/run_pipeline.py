#!/usr/bin/env python3
"""
全渠道选品 Agent — Master Pipeline
Runs all 3 channels: 社媒端 + SEO端 + 投放端
Outputs comprehensive Slack report.

Usage:
    python3 run_pipeline.py                    # Full pipeline
    python3 run_pipeline.py --channel social   # Social media only
    python3 run_pipeline.py --channel seo      # SEO only
    python3 run_pipeline.py --channel ads      # Ads only
    python3 run_pipeline.py --test             # Quick test (reduced data)
"""

import sys, os, json, time, argparse, subprocess
from datetime import datetime, timezone

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Load env ───
def _ensure_env():
    bashrc = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc):
        with open(bashrc) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                for key in ["APIFY_TOKEN", "SEMRUSH_API_KEY", "NOTION_API_KEY",
                            "NOTION_IMAGE_BOT_TOKEN", "TWITTER_TOKEN", "OPENNEWS_TOKEN"]:
                    if line.startswith(f"{key}=") and not os.environ.get(key):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        os.environ[key] = val

_ensure_env()


def fmt_num(n):
    """Format numbers: 1234567 → 123.5万"""
    if not n or not isinstance(n, (int, float)): return "N/A"
    if n >= 100_000_000: return f"{n/100_000_000:.1f}亿"
    if n >= 10_000: return f"{n/10_000:.1f}万"
    if n >= 1_000: return f"{n:,.0f}"
    return str(int(n))


# ═══════════════════════════════════════════════════
# Channel 1: 社媒端 — Social Media Trends
# ═══════════════════════════════════════════════════

def run_social_channel(query: str = "ai filter", max_results: int = 15, region: str = "US") -> dict:
    """Run all social media data sources, including KOL radar."""
    from sources.tiktok import fetch_tiktok_trending, extract_tiktok_trends
    from sources.youtube import fetch_youtube_trending, extract_youtube_trends
    from sources.reddit import fetch_reddit_search, extract_reddit_trends
    from sources.google_trends import fetch_google_trends
    from sources.instagram import fetch_instagram_posts, extract_instagram_trends
    from sources.kol_radar import fetch_all_kol_profiles, evaluate_trend_for_ai, aggregate_audio_trends

    results = {}
    
    # ─── KOL 雷达（优先级最高）───
    print(f"\n🎯 [社媒] KOL 趋势雷达 — 11个核心账号")
    try:
        kol_data = fetch_all_kol_profiles(max_per_kol=max_results)
        results["kol_radar"] = kol_data
        
        # 音频趋势聚合
        audio_trends = aggregate_audio_trends(kol_data)
        results["audio_trends"] = audio_trends
        if audio_trends:
            strong = [a for a in audio_trends if a["kol_count"] >= 2]
            print(f"   ✅ KOL雷达完成 | 🎵 音频趋势: {len(audio_trends)} ({len(strong)} 强趋势)")
        
        # 评估 top posts
        all_posts = []
        for tier in kol_data.values():
            for handle, data in tier.get("accounts", {}).items():
                for post in data.get("posts", []):
                    post["_kol"] = handle
                    post["_eval"] = evaluate_trend_for_ai(post)
                    all_posts.append(post)
        
        high_potential = [p for p in all_posts if p["_eval"]["score"] >= 50]
        results["kol_high_potential"] = sorted(high_potential, key=lambda x: x["_eval"]["score"], reverse=True)[:20]
        print(f"   ✅ 高潜力趋势: {len(high_potential)} 条")
    except Exception as e:
        print(f"   ❌ KOL雷达: {e}")
    
    # TikTok
    print(f"\n📡 [社媒] TikTok — '{query}'")
    try:
        raw = fetch_tiktok_trending(query, max_results)
        results["tiktok"] = extract_tiktok_trends(raw)
        print(f"   ✅ {len(results['tiktok'])} items")
    except Exception as e:
        print(f"   ❌ TikTok: {e}")
    
    # Instagram
    print(f"📡 [社媒] Instagram — '#{query.replace(' ', '')}'")
    try:
        ig_query = query.replace(" ", "")  # hashtag format
        raw = fetch_instagram_posts(ig_query, max_results)
        results["instagram"] = extract_instagram_trends(raw)
        print(f"   ✅ {len(results['instagram'])} items")
    except Exception as e:
        print(f"   ❌ Instagram: {e}")
    
    # YouTube
    print(f"📡 [社媒] YouTube — '{query}'")
    try:
        raw = fetch_youtube_trending(query, max_results)
        results["youtube"] = extract_youtube_trends(raw)
        print(f"   ✅ {len(results['youtube'])} items")
    except Exception as e:
        print(f"   ❌ YouTube: {e}")
    
    # Reddit
    print(f"📡 [社媒] Reddit — '{query}'")
    try:
        raw = fetch_reddit_search(query, max_results)
        results["reddit"] = extract_reddit_trends(raw)
        print(f"   ✅ {len(results['reddit'])} items")
    except Exception as e:
        print(f"   ❌ Reddit: {e}")
    
    # Google Trends
    print(f"📡 [社媒] Google Trends")
    try:
        keywords = ["ai filter", "ai photo", "face filter", "ai art", "ai generator"]
        results["google_trends"] = fetch_google_trends(keywords, geo=region)
        print(f"   ✅ fetched")
    except Exception as e:
        print(f"   ❌ Google Trends: {e}")
    
    return results


def format_social_report(data: dict, region: str = "US") -> str:
    """Format social data to match the exact doc template."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    region_flag = {"US": "🇺🇸 美国", "EU": "🇪🇺 欧洲", "ASIA": "🇯🇵🇰🇷 日韩"}.get(region, f"🌍 {region}")
    
    sections = []
    sections.append(f"🔥 *社媒热点速报 — {ts}*")
    sections.append(f"📅 近1周 | {region_flag}\n")
    
    # 🎨 AI 滤镜/特效 — from TikTok + YouTube combined
    tiktok = data.get("tiktok", [])
    youtube = data.get("youtube", [])
    if tiktok:
        lines = ["🎨 *AI 滤镜/特效 Top 10*", "```"]
        lines.append(f"{'排名':>4s}  {'名称':<36s}  {'播放量':>8s}  {'点赞':>8s}  {'评论':>6s}  {'平台':<8s}")
        lines.append("───  " + "─" * 75)
        for i, t in enumerate(tiktok[:10], 1):
            desc = (t.get('desc','') or '')[:34]
            plays = fmt_num(t.get('plays', 0))
            likes = fmt_num(t.get('likes', 0))
            comments = fmt_num(t.get('comments', 0))
            lines.append(f" {i:>2d}   {desc:<36s}  {plays:>8s}  {likes:>8s}  {comments:>6s}  {'TikTok':<8s}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # ▶️ YouTube 热门视频
    if youtube:
        lines = ["▶️ *热门视频 Top 10*", "```"]
        lines.append(f"{'排名':>4s}  {'标题':<40s}  {'播放量':>10s}  {'频道':<20s}")
        lines.append("───  " + "─" * 78)
        for i, t in enumerate(youtube[:10], 1):
            title = (t.get('title','') or '')[:38]
            views = fmt_num(t.get('views', 0))
            channel = (t.get('channel','') or '')[:18]
            lines.append(f" {i:>2d}   {title:<40s}  {views:>10s}  {channel:<20s}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # 🔥 Reddit
    reddit = data.get("reddit", [])
    if reddit:
        lines = ["🔥 *Reddit 热门讨论*", "```"]
        lines.append(f"{'排名':>4s}  {'子版块':<22s}  {'⬆️':>7s}  {'💬':>5s}  {'标题'}")
        lines.append("───  " + "─" * 72)
        for i, t in enumerate(reddit[:10], 1):
            sub = ('r/' + (t.get('subreddit','') or ''))[:20]
            lines.append(f" {i:>2d}   {sub:<22s}  {t.get('upvotes',0):>7,}  {t.get('comments',0):>5,}  {(t.get('title','') or '')[:30]}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # 📈 Google Trends
    gt = data.get("google_trends", {})
    if gt and gt.get("related_queries"):
        lines = ["📈 *Google Trends 关联查询*", "```"]
        for kw, queries in gt["related_queries"].items():
            lines.append(f" [{kw}]")
            for q in (queries or [])[:3]:
                lines.append(f"   → {q.get('query',''):28s} (热度: {q.get('value',0)})")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # 📸 Instagram
    instagram = data.get("instagram", [])
    if instagram:
        lines = ["📸 *Instagram 热门内容*", "```"]
        lines.append(f"{'排名':>4s}  {'作者':<22s}  {'类型':<8s}  {'点赞':>10s}  {'评论':>8s}  {'内容摘要'}")
        lines.append("───  " + "─" * 72)
        for i, t in enumerate(instagram[:10], 1):
            owner = ('@' + (t.get('owner','') or ''))[:20]
            itype = (t.get('type','') or '')[:6]
            caption = (t.get('caption','') or '')[:25]
            lines.append(f" {i:>2d}   {owner:<22s}  {itype:<8s}  {fmt_num(t.get('likes',0)):>10s}  {fmt_num(t.get('comments',0)):>8s}  {caption}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # 🎯 KOL 雷达
    kol_radar = data.get("kol_radar", {})
    if kol_radar:
        from sources.kol_radar import format_kol_radar_report
        kol_report = format_kol_radar_report(kol_radar)
        sections.append(kol_report)
    
    # 🔥 高潜力趋势 (AI 适配度评估)
    high_potential = data.get("kol_high_potential", [])
    if high_potential:
        lines = ["🏆 *高潜力 AI 趋势 Top 10（KOL雷达评估）*", "```"]
        lines.append(f"{'分数':>4s}  {'优先级':<10s}  {'KOL':<16s}  {'播放':>10s}  {'描述'}")
        lines.append("─" * 72)
        for p in high_potential[:10]:
            ev = p.get("_eval", {})
            lines.append(
                f" {ev.get('score',0):>3d}  {ev.get('priority','?'):<10s}  "
                f"@{p.get('_kol','?'):<14s}  {fmt_num(p.get('plays',0)):>10s}  "
                f"{(p.get('desc','') or '')[:28]}"
            )
            if ev.get("signals"):
                lines.append(f"{'':>6s}  → {' | '.join(ev['signals'][:3])}")
        lines.append("```")
        lines.append("⚠️ 数据评估仅供初筛，最终判断需人类直觉验证「视觉区分度 + AI可复制性 + 虚荣心触发」")
        sections.append("\n".join(lines))
    
    # 🎵 音频趋势信号
    audio_trends = data.get("audio_trends", [])
    if audio_trends:
        strong = [a for a in audio_trends if a.get("kol_count", 0) >= 2]
        if strong:
            lines = ["🎵 *热门音频趋势（多KOL共用 = 强信号）*", "```"]
            for at in strong[:5]:
                lines.append(f"  {at['trend_strength']}  {at['music'][:35]}  (by {at.get('music_author','')[:15]})")
                lines.append(f"{'':>4s}使用KOL: {', '.join('@'+k for k in at['kols'][:5])}  总播放: {fmt_num(at['total_plays'])}")
            lines.append("```")
            sections.append("\n".join(lines))
    
    sections.append(f"\n💡 切换区域：发送 \"查看欧洲\" / \"查看亚洲\" / \"查看全部\"")
    return "\n\n".join(sections)


# ═══════════════════════════════════════════════════
# Channel 2: SEO端
# ═══════════════════════════════════════════════════

def run_seo_channel(database: str = "us", limit: int = 50) -> list:
    """Run SEO pipeline."""
    from sources.seo_pipeline import run_seo_pipeline, format_seo_slack_report
    return run_seo_pipeline(database=database, limit=limit)


# ═══════════════════════════════════════════════════
# Channel 3: 投放端
# ═══════════════════════════════════════════════════

def run_ads_channel(query: str = "ai photo generator", country: str = "US") -> dict:
    """Run ads pipeline."""
    from sources.ads_pipeline import run_ads_pipeline
    return run_ads_pipeline(query, country)


# ═══════════════════════════════════════════════════
# Master Orchestrator
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="全渠道选品 Agent — Master Pipeline")
    parser.add_argument("--channel", default="all", choices=["all", "social", "seo", "ads"],
                        help="Which channel to run")
    parser.add_argument("--query", default="ai filter", help="Search query for social/ads")
    parser.add_argument("--region", default="US", help="Region (US/EU/ASIA)")
    parser.add_argument("--max-results", type=int, default=15, help="Max results per source")
    parser.add_argument("--test", action="store_true", help="Quick test mode (reduced data)")
    args = parser.parse_args()
    
    if args.test:
        args.max_results = 5
    
    total_start = time.time()
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    all_results = {}
    all_reports = []
    
    print(f"🚀 全渠道选品 Agent — Pipeline 启动")
    print(f"   时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"   频道: {args.channel} | 查询: '{args.query}' | 区域: {args.region}")
    print(f"   {'[TEST MODE]' if args.test else ''}")
    
    # ─── Social ───
    if args.channel in ("all", "social"):
        print(f"\n{'='*60}")
        print(f"📱 Channel 1: 社媒端")
        print(f"{'='*60}")
        start = time.time()
        social_data = run_social_channel(args.query, args.max_results, args.region)
        all_results["social"] = social_data
        
        report = format_social_report(social_data, args.region)
        all_reports.append(report)
        
        with open(os.path.join(OUTPUT_DIR, f"social_{ts}.json"), "w") as f:
            json.dump(social_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n⏱️ 社媒端完成: {time.time()-start:.1f}s")
    
    # ─── SEO ───
    if args.channel in ("all", "seo"):
        print(f"\n{'='*60}")
        print(f"🔍 Channel 2: SEO端")
        print(f"{'='*60}")
        start = time.time()
        seo_data = run_seo_channel(database=args.region.lower() if args.region != "ASIA" else "us",
                                   limit=30 if args.test else 50)
        all_results["seo"] = seo_data
        
        from sources.seo_pipeline import format_seo_slack_report
        report = format_seo_slack_report(seo_data)
        all_reports.append(report)
        
        with open(os.path.join(OUTPUT_DIR, f"seo_{ts}.json"), "w") as f:
            json.dump(seo_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n⏱️ SEO端完成: {time.time()-start:.1f}s")
    
    # ─── Ads ───
    if args.channel in ("all", "ads"):
        print(f"\n{'='*60}")
        print(f"📢 Channel 3: 投放端")
        print(f"{'='*60}")
        start = time.time()
        ads_query = "ai photo generator" if args.query == "ai filter" else args.query
        ads_data = run_ads_channel(ads_query, args.region if args.region != "ASIA" else "US")
        all_results["ads"] = ads_data
        
        from sources.ads_pipeline import format_ads_slack_report
        report = format_ads_slack_report(ads_data)
        all_reports.append(report)
        
        with open(os.path.join(OUTPUT_DIR, f"ads_{ts}.json"), "w") as f:
            json.dump(ads_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n⏱️ 投放端完成: {time.time()-start:.1f}s")
    
    # ─── Summary ───
    total_elapsed = time.time() - total_start
    
    # Save all data
    with open(os.path.join(OUTPUT_DIR, f"all_data_{ts}.json"), "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    # Save combined report
    full_report = "\n\n" + "━" * 60 + "\n\n".join(all_reports)
    report_path = os.path.join(OUTPUT_DIR, f"full_report_{ts}.txt")
    with open(report_path, "w") as f:
        f.write(full_report)
    
    print(f"\n{'='*60}")
    print(f"📊 PIPELINE COMPLETE — {total_elapsed:.1f}s")
    print(f"{'='*60}")
    
    if "social" in all_results:
        sources = [k for k, v in all_results["social"].items() if v]
        print(f"  📱 社媒端: {len(sources)} sources")
    if "seo" in all_results:
        print(f"  🔍 SEO端: {len(all_results['seo'])} keywords")
    if "ads" in all_results:
        scenarios = [k for k, v in all_results["ads"].items() if v]
        print(f"  📢 投放端: {len(scenarios)} scenarios")
    
    print(f"\n📝 Report: {report_path}")
    print(f"📦 Data: {os.path.join(OUTPUT_DIR, f'all_data_{ts}.json')}")
    
    # Print report preview
    print(f"\n{'='*60}")
    print("📋 FULL REPORT:")
    print(f"{'='*60}")
    print(full_report)
    
    return all_results


if __name__ == "__main__":
    main()
