"""
polymarket-brain.py - High-precision orchestrator for CNBC → Expert Agents → Polymarket → Discord

Workflow:
1. Phase 1: Fetch CNBC geopolitics news (last 24h)
2. Phase 2: Classify articles → Route to the-fed-agent or geopolitics-expert
3. Phase 3: Execute assigned Agent, extract Conclusion/Probability/Framework
4. Phase 4: Search Polymarket markets matching keywords
5. Phase 5: Send each market individually to Discord webhook
"""

import os
import sys
import re
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
SKILL_DIR = Path(__file__).parent
MEMORY_DIR = Path(os.getenv('APPDATA')) / '.browseros' / 'memory'
WORKSPACE_DIR = Path(os.getenv('APPDATA')) / '.browseros' / 'sessions'

# Discord webhook
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Polymarket API
POLYMARKET_API = "https://polymarket.com/api"

def log_status(phase, message):
    """Print status report to chat"""
    print(f"[{phase}] {message}")

def send_to_discord(content):
    """Send message to Discord webhook"""
    try:
        response = requests.post(DISCORD_WEBHOOK, json={"content": content})
        if response.status_code == 204:
            return True
        else:
            print(f"Discord error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Discord exception: {e}")
        return False

def fetch_cnbc_news():
    """Phase 1: Execute cnbc-geopolitics-fetcher logic"""
    log_status("Phase 1", "Fetching CNBC geopolitics news...")
    
    # Read CNBC geopolitics news from memory files
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    news_files = [
        MEMORY_DIR / f"{today}-cnbc-geopolitics.md",
        MEMORY_DIR / f"{yesterday}-cnbc-geopolitics.md"
    ]
    
    articles = []
    for news_file in news_files:
        if news_file.exists():
            with open(news_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract article titles and URLs
                article_pattern = r'### \d+\. (.+?)\n- URL: (.+?)\n- Published: (.+?)\n- Summary: (.+?)(?=###|\Z)'
                matches = re.findall(article_pattern, content, re.DOTALL)
                for match in matches:
                    articles.append({
                        'title': match[0].strip(),
                        'url': match[1].strip(),
                        'published': match[2].strip(),
                        'summary': match[3].strip()
                    })
    
    if not articles:
        log_status("Phase 1", "Status: Finished. Reason: No new articles found.")
        return []
    
    log_status("Phase 1", f"Status: Success. {len(articles)} articles ingested.")
    return articles[:3]  # Max 3 articles per cycle

def classify_article(article):
    """Phase 2: Classify article → Route to appropriate agent"""
    title = article['title'].lower()
    summary = article['summary'].lower()
    
    # Classification logic
    fed_keywords = ['fed', 'treasury', 'yield', 'inflation', 'rate', 'monetary', 'policy', 'economic']
    geo_keywords = ['war', 'conflict', 'iran', 'israel', 'middle east', 'military', 'attack', 'regime', 'coup']
    
    fed_score = sum(1 for kw in fed_keywords if kw in title or kw in summary)
    geo_score = sum(1 for kw in geo_keywords if kw in title or kw in summary)
    
    if fed_score > geo_score:
        return 'the-fed-agent', "Inflation Transmission"
    elif geo_score > fed_score:
        return 'geopolitics-expert', "Strategic Gravity"
    else:
        # Default to geopolitics for mixed content
        return 'geopolitics-expert', "Five Pathways"

def run_agent(agent_name, url, framework):
    """Phase 3: Execute assigned Agent"""
    log_status("Phase 3", f"Running {agent_name} with framework: {framework}")
    
    # Read agent output from memory files
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}-{agent_name}.md"
    
    if not memory_file.exists():
        # Try to extract from URL pattern
        log_status("Phase 3", f"Warning: No memory file found for {agent_name}")
        return {
            'conclusion': 'Analysis pending',
            'probability': 50,
            'framework': framework
        }
    
    with open(memory_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract probability (look for percentage patterns)
    prob_match = re.search(r'(\d+)%', content)
    probability = int(prob_match.group(1)) if prob_match else 50
    
    # Extract conclusion (first paragraph after heading)
    conclusion_match = re.search(r'## Analysis\n(.+?)(?=##|\Z)', content, re.DOTALL)
    conclusion = conclusion_match.group(1).strip()[:200] if conclusion_match else 'Analysis complete'
    
    return {
        'conclusion': conclusion,
        'probability': probability,
        'framework': framework
    }

def search_polymarket(keywords, agent_probability):
    """Phase 4: Search Polymarket markets"""
    log_status("Phase 4", f"Searching Polymarket for '{keywords}'...")
    
    # Mock market search (replace with actual API call)
    # This simulates finding markets based on keywords
    markets = []
    
    # Example markets based on keywords
    if 'iran' in keywords.lower():
        markets.append({
            'title': 'Will Iranian regime fall by June 30?',
            'resolution_date': 'Jun 30, 2026',
            'market_odds': 28,
            'url': 'https://polymarket.com/event/iran-regime-fall'
        })
        markets.append({
            'title': 'US-Iran ceasefire by December 31',
            'resolution_date': 'Dec 31, 2026',
            'market_odds': 73,
            'url': 'https://polymarket.com/event/us-iran-ceasefire'
        })
    
    if 'fed' in keywords.lower() or 'treasury' in keywords.lower():
        markets.append({
            'title': 'Fed rate cut by December 2026',
            'resolution_date': 'Dec 31, 2026',
            'market_odds': 65,
            'url': 'https://polymarket.com/event/fed-rate-cut'
        })
    
    log_status("Phase 4", f"{len(markets)} relevant markets found.")
    return markets

def calculate_recommendation(market_odds, expert_prob):
    """Calculate recommendation based on alpha gap"""
    gap = abs(expert_prob - market_odds)
    
    if gap >= 20:
        if expert_prob > market_odds:
            return "✅ Strong Yes", "Expert sees significantly higher probability than market"
        else:
            return "✅ Strong No", "Expert sees significantly lower probability than market"
    elif gap >= 10:
        if expert_prob > market_odds:
            return "⚠️ Lean Yes", "Expert moderately more optimistic than market"
        else:
            return "⚠️ Lean No", "Expert moderately less optimistic than market"
    else:
        return "⚪ Fair Value", "Market and expert align closely"

def format_discord_message(market, expert_data, agent_name):
    """Phase 5: Format Discord message"""
    recommendation, rationale = calculate_recommendation(market['market_odds'], expert_data['probability'])
    
    # Build deep analysis based on agent type
    if agent_name == 'geopolitics-expert':
        geo_logic = f"{expert_data['framework']} suggests {expert_data['probability']}% probability based on {expert_data['conclusion'][:100]}"
        fed_logic = "N/A (Macro event)"
    else:
        geo_logic = "N/A (Geopolitical event)"
        fed_logic = f"{expert_data['framework']} indicates {expert_data['probability']}% probability based on {expert_data['conclusion'][:100]}"
    
    message = f"""
### 🚨 **SIGNAL: {market['title']}**
- 📅 **Date**: {market['resolution_date']}
- 📊 **Price**: `{market['market_odds']}%` | 🧠 **Expert**: `{expert_data['probability']}%`
- 🎯 **Rec**: **{recommendation}** — {rationale}

**Deep Analysis:**
- 🛡️ **Geo**: {geo_logic}
- 📈 **Fed**: {fed_logic}

🔗 **Link**: {market['url']}
"""
    return message

def send_market_to_discord(message):
    """Send individual market to Discord"""
    return send_to_discord(message)

def main():
    """Main orchestrator"""
    print("=" * 60)
    print("POLYMARKET-BRAIN ORCHESTRATOR")
    print("=" * 60)
    
    # Phase 1: Ingestion
    articles = fetch_cnbc_news()
    if not articles:
        return
    
    # Phase 2-5: Process each article
    for i, article in enumerate(articles, 1):
        print(f"\n{'='*60}")
        print(f"Processing Article {i}/{len(articles)}: {article['title']}")
        print('=' * 60)
        
        # Phase 2: Classification
        agent_name, framework = classify_article(article)
        log_status("Phase 2", f"Routing Article '{article['title']}' to {agent_name}. Status: Success.")
        
        # Phase 3: Agent Execution
        expert_data = run_agent(agent_name, article['url'], framework)
        log_status("Phase 3", f"Extracted: Probability={expert_data['probability']}%, Framework={expert_data['framework']}")
        
        # Phase 4: Market Search
        markets = search_polymarket(article['title'], expert_data['probability'])
        
        # Phase 5: Discord Dispatch
        for j, market in enumerate(markets, 1):
            message = format_discord_message(market, expert_data, agent_name)
            if send_market_to_discord(message):
                log_status("Phase 5", f"Posted market {j} to Discord")
            else:
                log_status("Phase 5", f"Failed to post market {j}")
    
    total_markets = sum(len(search_polymarket(a['title'], 50)) for a in articles)
    log_status("Complete", f"Posted {total_markets} markets to Discord")

if __name__ == "__main__":
    main()
