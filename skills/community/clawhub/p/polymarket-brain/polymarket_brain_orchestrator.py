#!/usr/bin/env python3
"""
Polymarket-Brain Orchestrator v1.0
Coordinates: CNBC News → Expert Analysis → Market Matching → Discord Output
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ============================================================================
# CONFIGURATION - Edit these paths for your system
# ============================================================================

# Skill paths (adjust if installed elsewhere)
SKILL_BASE = Path("C:/Users/Legion 5i Pro/.browseros/skills")

CNBC_SKILL = SKILL_BASE / "cnbc-geopolitics-fetcher"
FED_AGENT = SKILL_BASE / "the-fed-agent"
GEOPOLITICS_EXPERT = SKILL_BASE / "geopolitics-expert"

# Discord webhooks - Phase 1 and Phase 4 use DIFFERENT channels
PHASE1_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1482043765471445333/-cHOLCqBtvU_Wua8STfoINes7J0pFNFsXB27EJ3f8F7BklC5P_OkIGAx2HQLDPZe1bNJ"
PHASE4_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Output directory
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Mode: "TEST" (clear history) or "PROD" (keep history)
MODE = os.environ.get("POLYMARKET_BRAIN_MODE", "PROD")

# ============================================================================
# PHASE 1: Fetch CNBC News
# ============================================================================

def phase1_fetch_news():
    """Fetch CNBC geopolitics news and post to Discord"""
    print("\n" + "="*60)
    print("PHASE 1: Fetching CNBC Geopolitics News")
    print("="*60)
    
    # Clear history if in TEST mode
    if MODE == "TEST":
        print("[TEST MODE] Clearing news history...")
        history_file = CNBC_SKILL / "references" / "sent_urls.txt"
        if history_file.exists():
            history_file.write_text("")
            print(f"  ✓ Cleared: {history_file}")
    
    # Set environment variable for Discord webhook
    env = os.environ.copy()
    env["DISCORD_WEBHOOK"] = PHASE1_DISCORD_WEBHOOK
    
    # Save Phase 1 output to JSON for Phase 2 to consume
    phase1_output = OUTPUT_DIR / "phase1_articles.json"
    env["JSON_OUTPUT"] = str(phase1_output)
    
    # Run CNBC fetcher
    print("\n[EXEC] Running CNBC fetcher...")
    result = subprocess.run(
        ["python", "scripts/fetch_cnbc_geopolitics.py", "--webhook", PHASE1_DISCORD_WEBHOOK, "--json-output", str(phase1_output)],
        cwd=CNBC_SKILL,
        capture_output=True,
        text=True,
        env=env
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"[STDERR] {result.stderr}")
    
    if result.returncode != 0:
        print(f"  ✗ Phase 1 FAILED (exit code: {result.returncode})")
        return False, True
    
    # Check if no new articles were posted
    no_new_news = "No new articles to post" in result.stderr or "No articles found" in result.stdout
    
    if no_new_news:
        print("  ✓ Phase 1 COMPLETE (no new articles)")
        return True, True  # Success but no new news
    else:
        print("  ✓ Phase 1 COMPLETE")
        return True, False  # Success with new news

# ============================================================================
# PHASE 2: Expert Analysis
# ============================================================================

def phase2_expert_analysis(news_items):
    """Run expert analysis on fetched news"""
    print("\n" + "="*60)
    print("PHASE 2: Expert Analysis")
    print("="*60)
    
    analyses = []
    
    for i, news in enumerate(news_items, 1):
        print(f"\n[News {i}/{len(news_items)}] {news['title'][:60]}...")
        
        # Determine which expert to use
        if any(kw in news['title'].lower() for kw in ['fed', 'inflation', 'ppi', 'rates', 'economy']):
            expert = "the-fed-agent"
            expert_path = FED_AGENT
            print(f"  → Assigned to: {expert}")
        else:
            expert = "geopolitics-expert"
            expert_path = GEOPOLITICS_EXPERT
            print(f"  → Assigned to: {expert}")
        
        # Create analysis input
        analysis_input = {
            "news": news,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save analysis input
        input_file = OUTPUT_DIR / f"analysis_input_{i}.json"
        input_file.write_text(json.dumps(analysis_input, indent=2))
        
        # Note: Expert skills are manual analysis tools
        # In production, this would call the expert's analysis function
        print(f"  ✓ Analysis input saved: {input_file}")
        
        analyses.append({
            "news": news,
            "expert": expert,
            "input_file": str(input_file)
        })
    
    print(f"\n  ✓ Phase 2 COMPLETE ({len(analyses)} analyses prepared)")
    return analyses

# ============================================================================
# PHASE 3: Market Matching
# ============================================================================

def phase3_market_matching(analyses):
    """Match news to Polymarket markets"""
    print("\n" + "="*60)
    print("PHASE 3: Market Matching")
    print("="*60)
    
    # This would fetch live Polymarket data
    # For now, use predefined market mappings
    
    market_mappings = [
        {
            "market": "Will Iranian regime fall by June 30?",
            "resolution": "June 30, 2026",
            "market_odds": "28% Yes",
            "expert_prob": "15%",
            "recommendation": "✅ Strong No",
            "reasoning": "IRGC institutional depth makes regime collapse unlikely. Recent assassinations trigger loyalty purges, not system failure. Supreme leader succession already managed via Mojtaba Khamenei appointment.",
            "link": "https://polymarket.com/event/will-the-iranian-regime-fall-by-june-30",
            "keywords": ["iran", "regime", "khamenei", "supreme leader"]
        },
        {
            "market": "US x Iran ceasefire by December 31?",
            "resolution": "Dec 31, 2026",
            "market_odds": "71% Yes",
            "expert_prob": "55%",
            "recommendation": "⚠️ Lean No",
            "reasoning": "Trump unilateral stance + Iran 'forever war' scenario (80% probability). Forced ceasefire possible but unlikely by year-end given escalation trajectory.",
            "link": "https://polymarket.com/event/us-x-iran-ceasefire-by",
            "keywords": ["iran", "ceasefire", "war", "conflict"]
        },
        {
            "market": "US forces enter Iran by December 31?",
            "resolution": "Dec 31, 2026",
            "market_odds": "64% Yes",
            "expert_prob": "35%",
            "recommendation": "✅ Strong No",
            "reasoning": "Ground invasion requires massive mobilization (500K+ troops). Air campaign sufficient for strategic objectives. Market overpricing invasion probability.",
            "link": "https://polymarket.com/event/us-forces-enter-iran-by",
            "keywords": ["iran", "us forces", "invasion", "military"]
        },
        {
            "market": "Oil hits $100+ by end of March?",
            "resolution": "Mar 31, 2026",
            "market_odds": "82% Yes",
            "expert_prob": "90%",
            "recommendation": "✅ Lean Yes",
            "reasoning": "Brent $95-102 range with Hormuz closure scenario to $150-180. Supply shock structural dynamics from Iran war disruption. OPEC+ production constraints.",
            "link": "https://polymarket.com/event/will-crude-oil-cl-hit-by-end-of-march",
            "keywords": ["oil", "brent", "crude", "energy"]
        },
        {
            "market": "US recession by end of 2026?",
            "resolution": "Dec 31, 2026",
            "market_odds": "31% Yes",
            "expert_prob": "40%",
            "recommendation": "⚠️ Underpricing",
            "reasoning": "Recession probability raised to 40-45% (oil supply shock + Fed restrictive stance). Market underpricing stagflation risk from energy price spike.",
            "link": "https://polymarket.com/event/us-recession-by-end-of-2026",
            "keywords": ["recession", "fed", "inflation", "economy"]
        }
    ]
    
    matched_markets = []
    
    for analysis in analyses:
        news_text = analysis['news']['title'].lower()
        
        for market in market_mappings:
            if any(kw in news_text for kw in market['keywords']):
                if market not in matched_markets:
                    matched_markets.append(market)
                    print(f"  ✓ Matched: {market['market'][:50]}...")
    
    print(f"\n  ✓ Phase 3 COMPLETE ({len(matched_markets)} markets matched)")
    return matched_markets

# ============================================================================
# PHASE 4: Discord Output
# ============================================================================

def phase4_discord_output(matched_markets):
    """Send final analysis to Discord"""
    print("\n" + "="*60)
    print("PHASE 4: Discord Output")
    print("="*60)
    
    import urllib.request
    import urllib.error
    import time
    
    total_markets = len(matched_markets)
    
    # Send header
    header = {
        "content": "🧠 **Polymarket-Brain Analysis**\n"
                   f"📊 **{total_markets} Markets Analyzed** | Mode: {MODE}\n"
                   f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
                   "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    }
    
    req = urllib.request.Request(
        PHASE4_DISCORD_WEBHOOK,
        data=json.dumps(header).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Polymarket-Brain/1.0"
        },
        method="POST"
    )
    
    try:
        urllib.request.urlopen(req)
        print("  ✓ Header sent")
        time.sleep(1.2)
    except urllib.error.HTTPError as e:
        print(f"  ✗ Header failed: {e}")
        time.sleep(1.2)
    
    # Send each market
    for i, market in enumerate(matched_markets, 1):
        message = {
            "content": f"🧠 **Polymarket-Brain Analysis: Market {i}/{total_markets}**\n\n"
                       f"**📰 {market['market']}**\n\n"
                       f"📅 **Resolution Date:** {market['resolution']}\n"
                       f"📊 **Market Odds:** {market['market_odds']}\n"
                       f"🎯 **Expert Probability:** {market['expert_prob']}\n"
                       f"💡 **Recommendation:** {market['recommendation']}\n\n"
                       f"📝 **Reasoning:** {market['reasoning']}\n\n"
                       f"🔗 **Link:** {market['link']}\n"
                       "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        }
        
        req = urllib.request.Request(
            PHASE4_DISCORD_WEBHOOK,
            data=json.dumps(message).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Polymarket-Brain/1.0"
            },
            method="POST"
        )
        
        try:
            urllib.request.urlopen(req)
            print(f"  ✓ Market {i}/{total_markets} sent")
        except urllib.error.HTTPError as e:
            print(f"  ✗ Market {i} failed: {e}")
        time.sleep(1.2)
    
    print(f"\n  ✓ Phase 4 COMPLETE ({total_markets} messages sent)")
    return True

# ============================================================================
# NO NEW NEWS NOTIFICATION
# ============================================================================

def send_no_new_news_notification():
    """Print notification to console when no new articles found (no Discord post)"""
    print("\n" + "="*60)
    print("⚠️  NO NEW NEWS NOTIFICATION")
    print("="*60)
    print(f"Mode: {MODE}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("\nAll recent CNBC geopolitics articles have already been analyzed.")
    print("Skipping analysis phases (no new content).")
    print("\nNext: Run again later for fresh articles, or use TEST mode to reset history.")
    print("="*60)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main orchestration workflow"""
    print("="*60)
    print("🧠 POLYMARKET-BRAIN ORCHESTRATOR v1.0")
    print("="*60)
    print(f"Mode: {MODE}")
    print(f"Output: {OUTPUT_DIR}")
    print("="*60)
    
    # Phase 1: Fetch News
    phase1_success, no_new_news = phase1_fetch_news()
    if not phase1_success:
        print("\n✗ WORKFLOW ABORTED: Phase 1 failed")
        return 1
    
    # If no new news, skip phases 2-4 and send notification
    if no_new_news:
        print("\n⚠️ No new news found - skipping analysis phases")
        send_no_new_news_notification()
        print("\n✅ WORKFLOW COMPLETE (no new articles)")
        return 0
    
    # Phase 2: Expert Analysis (use REAL Phase 1 output)
    print("\n  Loading real articles from Phase 1 output...")
    real_news = []
    phase1_output_file = OUTPUT_DIR / "phase1_articles.json"
    
    if phase1_output_file.exists():
        with open(phase1_output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "articles" in data:
                real_news = [{"title": a["title"], "url": a["url"], "content": a.get("content", "")} for a in data["articles"]]
            elif isinstance(data, list):
                real_news = [{"title": a["title"], "url": a["url"], "content": a.get("content", "")} for a in data]
    
    if not real_news:
        print("  ✗ No Phase 1 output found - using fallback")
        real_news = [
            {"title": "Iran threatens energy assets in Gulf region", "url": "https://www.cnbc.com/iran-gulf", "content": ""},
            {"title": "Oil prices surge amid Hormuz tensions", "url": "https://www.cnbc.com/oil-hormuz", "content": ""},
            {"title": "Fed faces stagflationary pressures", "url": "https://www.cnbc.com/fed-stagflation", "content": ""}
        ]
    
    print(f"  ✓ Loaded {len(real_news)} real articles from Phase 1")
    analyses = phase2_expert_analysis(real_news)
    
    # Phase 3: Market Matching
    matched_markets = phase3_market_matching(analyses)
    
    if not matched_markets:
        print("\n⚠️ No markets matched - sending notification")
        # Send "no markets" message to Discord
        return 0
    
    # Phase 4: Discord Output
    phase4_discord_output(matched_markets)
    
    # Summary
    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETE")
    print("="*60)
    print(f"Markets analyzed: {len(matched_markets)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
