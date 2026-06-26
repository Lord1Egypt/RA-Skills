#!/usr/bin/env python3
"""
Ads Pipeline — Facebook Ads Library via Apify
Implements all 4 query scenarios from the requirements doc.
"""

import sys, os, json, urllib.parse
from datetime import datetime, timezone, timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

from apify_client import run_actor

ACTOR_ID = "apify~facebook-ads-scraper"

# Competitor page names to monitor
COMPETITOR_PAGES = [
    'Lensa AI', 'FaceApp', 'Remini', 'PhotoRoom', 'Fotor', 'Picsart',
    'Remove.bg', 'Cutout.pro', 'Pixlr', 'Pose - AI Photo&Video Generator',
    'Beauty AI Camera', 'MePic - AI Photo Editor', 'OpenArt AI'
]


def _build_fb_url(search_terms: str, country: str = "US", media_type: str = "all",
                  active_only: bool = True) -> str:
    """Build Facebook Ads Library search URL."""
    params = urllib.parse.urlencode({
        "active_status": "active" if active_only else "all",
        "ad_type": "all",
        "country": country,
        "is_targeted_country": "false",
        "media_type": media_type,
        "q": search_terms,
        "search_type": "keyword_unordered",
        "sort_data[direction]": "desc",
        "sort_data[mode]": "total_impressions",
    })
    return f"https://www.facebook.com/ads/library/?{params}"


def fetch_ads(search_terms: str, country: str = "US", media_type: str = "all",
              max_results: int = 30, active_only: bool = True) -> list:
    """Fetch ads from Facebook Ads Library via Apify."""
    url = _build_fb_url(search_terms, country, media_type, active_only)
    input_data = {
        "startUrls": [{"url": url}],
        "resultsLimit": max_results,
    }
    return run_actor(ACTOR_ID, input_data)


def extract_ad_data(items: list) -> list:
    """Extract structured ad data from raw Apify results."""
    ads = []
    for item in items:
        snapshot = item.get("snapshot", {}) or {}
        cards = snapshot.get("cards", []) or []
        
        body = ""
        if cards:
            body = cards[0].get("body", "") or ""
        if not body:
            body = snapshot.get("body", "") or ""
        if isinstance(body, dict):
            body = body.get("text", "")
        
        title = snapshot.get("title", "") or ""
        cta = snapshot.get("ctaText", "") or ""
        link_url = snapshot.get("linkUrl", "") or ""
        if cards and not title:
            title = cards[0].get("title", "") or ""
        if cards and not link_url:
            link_url = cards[0].get("linkUrl", "") or ""
        
        # Determine media type
        has_video = bool(snapshot.get("videos") or any(c.get("videoHdUrl") for c in cards))
        has_image = bool(snapshot.get("images") or any(c.get("originalImageUrl") for c in cards))
        
        # Determine platforms
        platforms = []
        if snapshot.get("pageProfileUri", "").startswith("https://www.facebook"):
            platforms.append("fb")
        if any("instagram" in str(c.get("linkUrl", "")) for c in cards):
            platforms.append("ig")
        if not platforms:
            platforms = ["fb", "ig"]  # default assumption
        
        ads.append({
            "pageName": str(snapshot.get("pageName", "") or ""),
            "pageID": str(item.get("pageID", "") or item.get("pageId", "")),
            "adArchiveID": str(item.get("adArchiveID", "") or item.get("adArchiveId", "")),
            "startDate": str(item.get("startDateFormatted", "") or "")[:10],
            "endDate": str(item.get("endDateFormatted", "") or "")[:10],
            "isActive": not bool(item.get("endDateFormatted")),
            "title": str(title)[:200],
            "body": str(body)[:200],
            "ctaText": str(cta),
            "linkUrl": str(link_url),
            "platforms": platforms,
            "hasVideo": has_video,
            "hasImage": has_image,
            "collationCount": item.get("collationCount", 1),
            "snapshotUrl": f"https://www.facebook.com/ads/library/?id={item.get('adArchiveID', '')}",
        })
    return ads


# ─── 4 Query Scenarios from Doc ───

def scenario_competitor_active_ads(search_terms: str = "ai photo generator",
                                    country: str = "US", days: int = 15) -> dict:
    """Scenario 1: 查看竞品近N天活跃广告"""
    print(f"[Ads] Scenario 1: Competitor active ads ('{search_terms}', last {days} days)")
    raw = fetch_ads(search_terms, country, active_only=True, max_results=30)
    ads = extract_ad_data(raw)
    
    # Filter to recent N days
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d')
    recent = [a for a in ads if a['startDate'] >= cutoff or not a['endDate']]
    
    return {"scenario": "competitor_active_ads", "query": search_terms, "ads": recent, "raw_count": len(raw)}


def scenario_video_creatives(search_terms: str = "ai generator",
                              country: str = "US") -> dict:
    """Scenario 2: 搜AI生图视频素材"""
    print(f"[Ads] Scenario 2: Video creatives ('{search_terms}')")
    raw = fetch_ads(search_terms, country, media_type="video", max_results=30)
    ads = extract_ad_data(raw)
    video_ads = [a for a in ads if a['hasVideo']]
    return {"scenario": "video_creatives", "query": search_terms, "ads": video_ads, "raw_count": len(raw)}


def scenario_image_creatives(search_terms: str = "ai generator",
                              country: str = "US") -> dict:
    """Scenario 3: 搜AI生图图片素材"""
    print(f"[Ads] Scenario 3: Image creatives ('{search_terms}')")
    raw = fetch_ads(search_terms, country, media_type="image", max_results=30)
    ads = extract_ad_data(raw)
    image_ads = [a for a in ads if a['hasImage']]
    return {"scenario": "image_creatives", "query": search_terms, "ads": image_ads, "raw_count": len(raw)}


def scenario_copy_analysis(search_terms: str = "ai photo generator",
                            country: str = "US") -> dict:
    """Scenario 4: 分析竞品文案"""
    print(f"[Ads] Scenario 4: Copy analysis ('{search_terms}')")
    raw = fetch_ads(search_terms, country, active_only=True, max_results=30)
    ads = extract_ad_data(raw)
    
    # Analyze copy patterns
    cta_counts = {}
    body_patterns = []
    for ad in ads:
        cta = ad['ctaText']
        cta_counts[cta] = cta_counts.get(cta, 0) + 1
        if ad['body']:
            body_patterns.append({"pageName": ad['pageName'], "body": ad['body'][:100], "title": ad['title'][:80]})
    
    return {
        "scenario": "copy_analysis",
        "query": search_terms,
        "ads": ads,
        "cta_distribution": cta_counts,
        "body_samples": body_patterns[:15],
        "raw_count": len(raw),
    }


def run_ads_pipeline(search_terms: str = "ai photo generator", country: str = "US") -> dict:
    """Run all 4 ads scenarios."""
    results = {}
    
    results["active_ads"] = scenario_competitor_active_ads(search_terms, country)
    results["video_creatives"] = scenario_video_creatives(search_terms, country)
    results["image_creatives"] = scenario_image_creatives(search_terms, country)
    results["copy_analysis"] = scenario_copy_analysis(search_terms, country)
    
    return results


def format_ads_slack_report(results: dict) -> str:
    """Format ads results as Slack report matching doc template."""
    lines = []
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines.append(f"📢 *投放端 — Facebook Ads 竞品监控 — {ts}*\n")
    
    # Scenario 1: Active ads
    active = results.get("active_ads", {})
    ads = active.get("ads", [])
    if ads:
        lines.append(f"*① 竞品活跃广告* (关键词: {active.get('query','')}, 共{len(ads)}条)\n```")
        lines.append(f"{'广告主':<28s}  {'标题':<22s}  {'文案（截取）':<28s}  {'平台':<8s}  {'开始投放':<12s}  {'素材链接'}")
        lines.append("─" * 115)
        for ad in ads[:15]:
            name = (ad['pageName'] or '')[:26]
            title = (ad['title'] or '')[:20]
            body = (ad['body'] or '')[:26]
            plat = ','.join(ad.get('platforms', []))[:6]
            start = ad['startDate'][:10]
            snap = ad.get('snapshotUrl', '')[:30] + '...' if ad.get('snapshotUrl') else ''
            lines.append(f"{name:<28s}  {title:<22s}  {body:<28s}  {plat:<8s}  {start:<12s}  {snap}")
        lines.append("```")
    
    # Scenario 2: Video
    video = results.get("video_creatives", {})
    vads = video.get("ads", [])
    if vads:
        lines.append(f"\n*② AI生图视频素材* ({len(vads)}条)\n```")
        lines.append(f" #  {'广告主':<28s}  {'CTA':<14s}  {'文案摘要'}")
        lines.append("─" * 75)
        for i, ad in enumerate(vads[:10], 1):
            lines.append(f"{i:>2d}  {(ad['pageName'] or '')[:26]:<28s}  {(ad['ctaText'] or '')[:12]:<14s}  {(ad['body'] or '')[:30]}")
        lines.append("```")
    
    # Scenario 3: Image
    image = results.get("image_creatives", {})
    iads = image.get("ads", [])
    if iads:
        lines.append(f"\n*③ AI生图图片素材* ({len(iads)}条)\n```")
        lines.append(f" #  {'广告主':<28s}  {'CTA':<14s}  {'文案摘要'}")
        lines.append("─" * 75)
        for i, ad in enumerate(iads[:10], 1):
            lines.append(f"{i:>2d}  {(ad['pageName'] or '')[:26]:<28s}  {(ad['ctaText'] or '')[:12]:<14s}  {(ad['body'] or '')[:30]}")
        lines.append("```")
    
    # Scenario 4: Copy analysis
    copy = results.get("copy_analysis", {})
    cta_dist = copy.get("cta_distribution", {})
    if cta_dist:
        lines.append(f"\n*④ 竞品文案分析*\n_CTA 分布：_\n```")
        total_cta = sum(cta_dist.values())
        for cta, count in sorted(cta_dist.items(), key=lambda x: -x[1]):
            pct = count / total_cta * 100 if total_cta > 0 else 0
            lines.append(f"  {cta:<20s}  {count:>3d}条  (~{pct:.0f}%)")
        lines.append("```")
    
    samples = copy.get("body_samples", [])
    if samples:
        lines.append("\n_高频文案模式：_\n```")
        for s in samples[:8]:
            lines.append(f"  [{(s['pageName'] or '')[:15]}] {(s['body'] or '')[:60]}")
        lines.append("```")
    
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="ai photo generator")
    parser.add_argument("--country", default="US")
    parser.add_argument("--scenario", type=int, default=0, help="1-4 for single scenario, 0 for all")
    args = parser.parse_args()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if args.scenario == 0:
        results = run_ads_pipeline(args.query, args.country)
    elif args.scenario == 1:
        results = {"active_ads": scenario_competitor_active_ads(args.query, args.country)}
    elif args.scenario == 2:
        results = {"video_creatives": scenario_video_creatives(args.query, args.country)}
    elif args.scenario == 3:
        results = {"image_creatives": scenario_image_creatives(args.query, args.country)}
    elif args.scenario == 4:
        results = {"copy_analysis": scenario_copy_analysis(args.query, args.country)}
    
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    with open(os.path.join(OUTPUT_DIR, f"ads_pipeline_{ts}.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    report = format_ads_slack_report(results)
    print(report)
    with open(os.path.join(OUTPUT_DIR, f"ads_report_{ts}.txt"), "w") as f:
        f.write(report)
