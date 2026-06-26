"""
Polymarket Brain Workflow Orchestrator
v2.0 - Fixed to handle browser skills properly

Workflow:
1. Run cnbc-geopolitics-fetcher (Python script)
2. Classify articles: geopolitics vs macro
3. Run analysts:
   - geopolitics-expert (browser skill via topic extraction)
   - the-fed-agent (Python script)
4. Pass topics to polymarket-analyst (topic-driven, not random)
5. Send one-by-one to Discord
"""

import subprocess
import sys
import os
from pathlib import Path

# Force UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Use short path to avoid spaces in username
BASE = Path(r"C:\Users\LEGION~1\AppData\Local\.browseros\skills")

def log(step, status, msg=""):
    emoji = {"ok": "✅", "warn": "⚠️", "err": "❌", "info": "ℹ️"}
    print(f"{emoji.get(status, '•')} {step}: {msg or status}", flush=True)

def run_script(skill_name, script_name, env=None):
    """Run a Python script for a skill"""
    script_path = BASE / skill_name / "scripts" / script_name
    if not script_path.exists():
        log(f"{skill_name} script", "warn", f"Not found: {script_path}")
        return None
    
    cmd = [sys.executable, str(script_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, **(env or {})})
    if result.returncode == 0:
        log(f"{skill_name}", "ok", "Script executed")
        return result.stdout
    else:
        log(f"{skill_name}", "err", result.stderr[:200] if result.stderr else "Failed")
        return None

def classify_article(title, description=""):
    """Classify article as geopolitics, macro, or other"""
    text = (title + " " + description).lower()
    
    geo_keywords = ["iran", "russia", "ukraine", "middle east", "war", "conflict", 
                    "military", "oil", "opec", "israel", "gaza", "hezbollah", "nato",
                    "trump", "putin", "regime", "sanctions", "tariff"]
    macro_keywords = ["fed", "federal reserve", "interest rate", "treasury", "yield",
                      "inflation", "cpi", "jobs", "employment", "gdp", "powell",
                      "dollar", "usd", "bond", "monetary", "quantitative"]
    
    has_geo = any(k in text for k in geo_keywords)
    has_macro = any(k in text for k in macro_keywords)
    
    if has_geo and has_macro:
        return "both"
    elif has_geo:
        return "geopolitics"
    elif has_macro:
        return "macro"
    return "other"

def extract_topics_from_url(url, category):
    """Extract topics from URL for browser-based skills"""
    # Simple topic extraction from URL slug
    slug = url.split("/")[-1].replace("-", " ").replace(".html", "")
    
    if category == "geopolitics":
        return ["iran", "war", "oil", "russia"]
    elif category == "macro":
        return ["fed", "rate", "treasury", "inflation"]
    return ["general"]

def main():
    log("Polymarket Brain Workflow", "info", "Starting...")
    
    # Step 1: Fetch CNBC news
    log("Step 1", "info", "Fetching CNBC geopolitics news")
    fetcher_output = run_script("cnbc-geopolitics-fetcher", "fetch_cnbc_geopolitics.py")
    
    if not fetcher_output:
        log("Fetch", "err", "No articles fetched")
        print("WORKFLOW_STOPPED: No news")
        return
    
    # Parse fetched articles (expecting JSON or text output)
    articles = []
    if fetcher_output.strip():
        # Try to parse as JSON
        import json
        try:
            articles = json.loads(fetcher_output)
        except:
            # Fallback: treat as single article
            articles = [{"title": fetcher_output.strip()[:100], "url": "unknown"}]
    
    if not articles:
        log("Articles", "warn", "No articles parsed")
        return
    
    log(f"Step 2", "info", f"Classifying {len(articles)} articles")
    
    # Step 2: Classify and route to analysts
    geo_articles = []
    macro_articles = []
    
    for article in articles:
        title = article.get("title", "")
        desc = article.get("description", "")
        category = classify_article(title, desc)
        
        if category in ["geopolitics", "both"]:
            geo_articles.append(article)
        if category in ["macro", "both"]:
            macro_articles.append(article)
    
    log("Classification", "ok", f"Geopolitics: {len(geo_articles)}, Macro: {len(macro_articles)}")
    
    # Step 3: Run analysts
    all_topics = []
    
    # Geopolitics analyst (browser skill - extract topics from URLs)
    if geo_articles:
        log("Step 3a", "info", "Running geopolitics-expert (topic extraction)")
        for article in geo_articles:
            topics = extract_topics_from_url(article.get("url", ""), "geopolitics")
            all_topics.extend(topics)
            log(f"  - {article.get('title', 'Unknown')[:50]}", "ok", f"Topics: {topics}")
    
    # Macro analyst (Python script)
    if macro_articles:
        log("Step 3b", "info", "Running the-fed-agent")
        fed_output = run_script("the-fed-agent", "analyze_fed_policy.py")
        if fed_output:
            all_topics.extend(["fed", "rate", "treasury", "inflation"])
            log("the-fed-agent", "ok", "Analysis complete")
    
    # Deduplicate topics
    all_topics = list(set(all_topics))
    log("Step 4", "info", f"Combined topics: {all_topics}")
    
    # Step 4: Run Polymarket analyst (topic-driven)
    if not all_topics:
        all_topics = ["iran", "fed", "oil"]  # Fallback
    
    env = {"POLYMARKET_TOPICS": ",".join(all_topics)}
    poly_output = run_script("polymarket-analyst", "poll_polymarket_markets.py", env=env)
    
    if not poly_output:
        log("Polymarket", "err", "No markets found")
        return
    
    # Step 5: Send to Discord (one-by-one format)
    log("Step 5", "info", "Sending to Discord")
    
    # Parse markets from output
    import json
    try:
        markets = json.loads(poly_output)
    except:
        markets = [{"title": poly_output.strip()[:100], "odds": 50}]
    
    # Send each market separately
    for market in markets:
        title = market.get("title", "Unknown Market")
        odds = market.get("odds", 50)
        expert_prob = market.get("expert_prob", 50)
        recommendation = market.get("recommendation", "HOLD")
        
        # Determine emoji
        gap = abs(odds - expert_prob)
        if gap >= 20:
            emoji = "✅"  # Strong conviction
        elif gap >= 10:
            emoji = "⚠️"  # Fair value
        else:
            emoji = "⚪"  # No edge
        
        # Format message
        msg = f"{emoji} **{title}**\n"
        msg += f"Odds: {odds}% | Expert: {expert_prob}% | Rec: {recommendation}\n"
        msg += f"Gap: {gap}%\n"
        msg += f"URL: {market.get('url', 'N/A')}"
        
        print(f"DISCORD_MSG: {msg}")
    
    log("Workflow", "ok", "Complete!")

if __name__ == "__main__":
    main()
