#!/usr/bin/env python3
"""
Omni-Channel Selection Agent — Full Pipeline
Fetches data from all available social media sources via Apify + free APIs.
Outputs formatted Slack report.

Usage:
    python3 run_all.py                         # All sources, default query
    python3 run_all.py --query "ai filter"     # Custom query
    python3 run_all.py --source tiktok         # Single source
    python3 run_all.py --keywords "k1,k2,k3"  # Multiple keywords
"""

import sys, os, json, argparse, time, subprocess
from datetime import datetime, timezone

# Ensure project root on path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load tokens from ~/.bashrc if not in env
def _ensure_env():
    """Load API tokens from ~/.bashrc if not already in environment."""
    needed = {"APIFY_TOKEN": None, "TWITTER_TOKEN": None, "OPENNEWS_TOKEN": None}
    bashrc = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc):
        with open(bashrc) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                for key in needed:
                    if line.startswith(f"{key}=") and not os.environ.get(key):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        os.environ[key] = val

_ensure_env()


def run_source_script(name: str, script: str, args: list = None, timeout: int = 180) -> dict:
    """Run a source script as a subprocess and capture results."""
    cmd = [sys.executable, os.path.join(PROJECT_DIR, "sources", script)]
    if args:
        cmd.extend(args)
    
    print(f"\n{'='*60}")
    print(f"📡 [{name}] Starting... ({script} {' '.join(args or [])})")
    print(f"{'='*60}")
    
    start = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            env={**os.environ},
            cwd=PROJECT_DIR,
        )
        elapsed = time.time() - start
        
        if result.returncode == 0:
            print(f"✅ [{name}] Completed in {elapsed:.1f}s")
            if result.stdout:
                # Print last 15 lines of output
                lines = result.stdout.strip().split("\n")
                for line in lines[-15:]:
                    print(f"   {line}")
        else:
            print(f"❌ [{name}] Failed (code {result.returncode}) in {elapsed:.1f}s")
            if result.stderr:
                # Print last 5 lines of error
                for line in result.stderr.strip().split("\n")[-5:]:
                    print(f"   ERR: {line}")
        
        return {
            "name": name,
            "success": result.returncode == 0,
            "elapsed": elapsed,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"⏰ [{name}] Timed out after {elapsed:.1f}s")
        return {"name": name, "success": False, "elapsed": elapsed, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        elapsed = time.time() - start
        print(f"💥 [{name}] Exception: {e}")
        return {"name": name, "success": False, "elapsed": elapsed, "stdout": "", "stderr": str(e)}


def load_latest_output(prefix: str) -> any:
    """Load the latest processed output file for a source."""
    import glob
    # Try multiple naming patterns
    candidates = []
    for pattern in [
        os.path.join(OUTPUT_DIR, f"{prefix}_trends.json"),
        os.path.join(OUTPUT_DIR, f"{prefix}.json"),
        os.path.join(OUTPUT_DIR, f"{prefix}_2*.json"),
    ]:
        candidates.extend(glob.glob(pattern))
    # Filter out raw files
    candidates = [f for f in candidates if "_raw" not in f and "all_data" not in f]
    candidates = sorted(candidates, key=os.path.getmtime, reverse=True)
    if candidates:
        with open(candidates[0]) as f:
            return json.load(f)
    return [] if prefix != "google_trends" else {}


def generate_slack_report(results: dict) -> str:
    """Generate a comprehensive Slack-formatted report from all source data."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sections = []
    
    sections.append(f"🔥 *社媒热点速报 — {ts}*")
    sections.append(f"📅 近1周 | 🇺🇸 美国\n")
    
    def fmt_num(n):
        if not n: return "N/A"
        if isinstance(n, str): return n
        if n >= 100_000_000: return f"{n/100_000_000:.1f}亿"
        if n >= 10_000: return f"{n/10_000:.1f}万"
        if n >= 1_000: return f"{n:,}"
        return str(n)
    
    # TikTok
    tiktok = results.get("tiktok", [])
    if tiktok:
        lines = ["🎵 *TikTok 热门内容*", "```"]
        lines.append(f" #  {'描述':<38s}  {'播放量':>10s}  {'点赞':>8s}  {'评论':>6s}")
        lines.append("─" * 72)
        for i, t in enumerate(tiktok[:10], 1):
            desc = (t.get("desc","") or "")[:36]
            lines.append(f"{i:>2d}  {desc:<38s}  {fmt_num(t.get('plays',0)):>10s}  {fmt_num(t.get('likes',0)):>8s}  {fmt_num(t.get('comments',0)):>6s}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # YouTube
    youtube = results.get("youtube", [])
    if youtube:
        lines = ["▶️ *YouTube 热门视频*", "```"]
        lines.append(f" #  {'标题':<43s}  {'播放量':>10s}  {'频道'}")
        lines.append("─" * 80)
        for i, t in enumerate(youtube[:10], 1):
            title = (t.get("title","") or "")[:41]
            channel = (t.get("channel","") or "")[:20]
            lines.append(f"{i:>2d}  {title:<43s}  {fmt_num(t.get('views',0)):>10s}  {channel}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Facebook Ads
    fb_ads = results.get("facebook_ads", [])
    if fb_ads:
        lines = ["📢 *Facebook Ads 竞品广告*", "```"]
        lines.append(f" #  {'广告主':<28s}  {'投放起始':<12s}  {'CTA':<14s}  {'文案摘要'}")
        lines.append("─" * 90)
        for i, ad in enumerate(fb_ads[:10], 1):
            name = (ad.get("pageName","") or "")[:26]
            start = (ad.get("startDate","") or "")[:10]
            cta = (ad.get("ctaText","") or "")[:12]
            body = (ad.get("body","") or ad.get("title","") or "")[:30]
            lines.append(f"{i:>2d}  {name:<28s}  {start:<12s}  {cta:<14s}  {body}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Reddit
    reddit = results.get("reddit", [])
    if reddit:
        lines = ["🔥 *Reddit 热门讨论*", "```"]
        lines.append(f" #  {'子版块':<20s}  {'⬆️':>6s}  {'💬':>5s}  {'标题'}")
        lines.append("─" * 75)
        for i, t in enumerate(reddit[:10], 1):
            sub = (t.get("subreddit","") or "")[:18]
            lines.append(f"{i:>2d}  r/{sub:<20s}  {t.get('upvotes',0):>6,}  {t.get('comments',0):>5,}  {(t.get('title','') or '')[:30]}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Google Trends
    gt = results.get("google_trends", {})
    if gt and gt.get("related_queries"):
        lines = ["📈 *Google Trends 关联查询*", "```"]
        for kw, queries in gt["related_queries"].items():
            lines.append(f" [{kw}]")
            for q in (queries or [])[:3]:
                lines.append(f"   → {q.get('query',''):28s} (热度: {q.get('value',0)})")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Instagram  
    instagram = results.get("instagram", [])
    if instagram:
        lines = ["📸 *Instagram 热门内容*", "```"]
        lines.append(f" #  {'作者':<20s}  {'点赞':>10s}  {'评论':>8s}  {'播放':>10s}")
        lines.append("─" * 60)
        for i, t in enumerate(instagram[:10], 1):
            owner = (t.get("owner","") or "")[:18]
            lines.append(f"{i:>2d}  @{owner:<20s}  {fmt_num(t.get('likes',0)):>10s}  {fmt_num(t.get('comments',0)):>8s}  {fmt_num(t.get('views',0)):>10s}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Summary
    source_count = sum(1 for v in results.values() if v)
    sections.append(f"\n📊 *数据源：{source_count} 个* | 💡 切换区域：发送 \"查看欧洲\" / \"查看亚洲\"")
    
    return "\n\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Omni-Channel Selection Agent Pipeline")
    parser.add_argument("--query", default="ai filter", help="Primary search query")
    parser.add_argument("--keywords", default=None, help="Comma-separated keywords for Google Trends")
    parser.add_argument("--source", default="all", help="Single source to run, or 'all'")
    parser.add_argument("--max-results", type=int, default=15, help="Max results per source")
    parser.add_argument("--region", default="US", help="Region")
    parser.add_argument("--skip", default="", help="Comma-separated sources to skip")
    parser.add_argument("--slack-output", default=None, help="Path to write Slack report")
    args = parser.parse_args()
    
    skip = set(args.skip.split(",")) if args.skip else set()
    query = args.query
    max_r = str(args.max_results)
    
    # Define all sources and their scripts
    all_sources = {
        "tiktok":       ("tiktok.py", [query]),
        "youtube":      ("youtube.py", [query]),
        "facebook_ads": ("facebook_ads.py", [query]),
        "reddit":       ("reddit.py", [query]),
        "instagram":    ("instagram.py", [query.replace(" ", "")]),  # IG uses hashtag format
        "google_trends": ("google_trends.py", (args.keywords or "ai filter,ai photo,face filter,ai art,ai generator").split(",")),
    }
    
    if args.source != "all":
        if args.source in all_sources:
            run_list = {args.source: all_sources[args.source]}
        else:
            print(f"Unknown source: {args.source}. Available: {list(all_sources.keys())}")
            sys.exit(1)
    else:
        run_list = {k: v for k, v in all_sources.items() if k not in skip}
    
    total_start = time.time()
    run_results = {}
    
    print(f"🚀 Pipeline starting — {len(run_list)} sources, query='{query}'")
    print(f"   Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    for name, (script, script_args) in run_list.items():
        result = run_source_script(name, script, script_args, timeout=180)
        run_results[name] = result
    
    total_elapsed = time.time() - total_start
    
    # Load processed data for report generation
    print(f"\n{'='*60}")
    print(f"📊 PIPELINE COMPLETE — {total_elapsed:.1f}s total")
    print(f"{'='*60}")
    
    all_data = {}
    for name in run_list:
        if run_results[name]["success"]:
            data = load_latest_output(name)
            if data:
                all_data[name] = data
                count = len(data) if isinstance(data, list) else "dict"
                print(f"  ✅ {name}: {count} items")
            else:
                print(f"  ⚠️  {name}: completed but no output file found")
        else:
            print(f"  ❌ {name}: failed")
    
    # Generate Slack report
    report = generate_slack_report(all_data)
    
    # Save report
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    report_path = args.slack_output or os.path.join(OUTPUT_DIR, f"slack_report_{ts}.txt")
    with open(report_path, "w") as f:
        f.write(report)
    
    # Also save all data as single JSON
    all_data_path = os.path.join(OUTPUT_DIR, f"all_data_{ts}.json")
    with open(all_data_path, "w") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📝 Slack report: {report_path}")
    print(f"📦 All data JSON: {all_data_path}")
    
    # Print report preview
    print(f"\n{'='*60}")
    print("📋 REPORT PREVIEW:")
    print(f"{'='*60}")
    print(report)
    
    return all_data


if __name__ == "__main__":
    main()
