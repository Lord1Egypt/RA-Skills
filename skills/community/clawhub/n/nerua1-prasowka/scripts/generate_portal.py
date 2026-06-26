#!/usr/bin/env python3
"""
generate_portal.py - Nowy generator prasówki
Kroki: fetch → filter → summarize → generate HTML
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Ścieżki
BASE_DIR = Path("/Users/nerucb1/.openclaw/workspace/skills/prasowka")
REFS_DIR = BASE_DIR / "references"
DATA_DIR = BASE_DIR / "data"
CANVAS_DIR = Path("/Users/nerucb1/.openclaw/canvas")

# Mapowanie tematów na źródła (z topics.md)
TOPIC_SOURCES = {
    "ai-models": ["hackernews", "reddit-artificial", "reddit-singularity"],
    "ai-tools": ["hackernews", "github", "v2ex"],
    "ai-video": ["hackernews", "reddit-technology"],
    "ai-agents": ["hackernews", "reddit-artificial", "v2ex"],
    "ai-threats": ["reddit-worldnews", "yandex"],
    "ai-pricing": ["hackernews", "v2ex"],
    "ai-nsfw": ["hackernews"],
    "vibe-coding": ["hackernews", "github", "reddit-technology"],
    "tech-science": ["hackernews", "reddit-science", "v2ex"],
    "space": ["reddit-science", "hackernews"],
    "quantum": ["reddit-science", "hackernews"],
    "medicine": ["reddit-science", "hackernews"],
    "world": ["reddit-worldnews", "yandex", "wallstreetcn"],
    "market": ["wallstreetcn", "reddit-stocks", "reddit-investing"],
    "crypto": ["reddit-technology", "hackernews"],
    "polymarket": ["hackernews"],
    "layoffs": ["reddit-technology", "hackernews"],
    "poland": ["hackernews"],
}

def load_topics():
    """Wczytaj konfigurację tematów"""
    topics_file = REFS_DIR / "topics.md"
    topics = {}
    
    with open(topics_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("|") and "Topic ID" not in line and "---" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    topic_id = parts[1]
                    name = parts[2]
                    count = parts[3]
                    try:
                        topics[topic_id] = {
                            "name": name,
                            "count": int(count)
                        }
                    except ValueError:
                        continue
    
    return topics

def load_seen_urls():
    """Wczytaj już widziane URLe"""
    seen_file = DATA_DIR / "seen_urls.json"
    if seen_file.exists():
        with open(seen_file) as f:
            return set(json.load(f))
    return set()

def save_seen_urls(urls):
    """Zapisz widziane URLe"""
    seen_file = DATA_DIR / "seen_urls.json"
    seen_file.parent.mkdir(parents=True, exist_ok=True)
    with open(seen_file, "w") as f:
        json.dump(list(urls), f, indent=2)

def fetch_from_source(source, limit):
    """Pobierz newsy ze źródła"""
    result = subprocess.run(
        ["python3", str(BASE_DIR / "scripts/fetch_news.py"),
         "--source", source,
         "--limit", str(limit)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ⚠️  {source}: {result.stderr[:50]}", file=sys.stderr)
        return []
    
    try:
        data = json.loads(result.stdout)
        if isinstance(data, list):
            return data
        return []
    except json.JSONDecodeError:
        return []

def fetch_topic_news(topic_id, limit):
    """Pobierz newsy dla tematu ze wszystkich źródeł"""
    sources = TOPIC_SOURCES.get(topic_id, ["hackernews"])
    all_articles = []
    
    for source in sources:
        articles = fetch_from_source(source, limit // len(sources) + 2)
        # Dodaj tag tematu do każdego artykułu
        for a in articles:
            if isinstance(a, dict):
                a["_topic"] = topic_id
        all_articles.extend(articles)
    
    return all_articles

def generate_html(articles_by_topic, date_str):
    """Generuj HTML portalu"""
    
    # Kolorystyka dark mode (domyślna)
    html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prasówka — {date_str}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    :root {{
      --bg-primary: #0d0d0d;
      --bg-secondary: #1a1a1a;
      --bg-card: #171717;
      --text-primary: #e8e8e8;
      --text-secondary: #888;
      --accent: #c00;
      --border: #222;
    }}
    
    [data-theme="light"] {{
      --bg-primary: #fafafa;
      --bg-secondary: #fff;
      --bg-card: #f5f5f5;
      --text-primary: #0a0a0a;
      --text-secondary: #525252;
      --accent: #dc2626;
      --border: #e5e5e5;
    }}
    
    body {{ 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
      background: var(--bg-primary); 
      color: var(--text-primary);
      transition: background 0.3s, color 0.3s;
    }}
    
    .header {{ 
      background: var(--bg-secondary); 
      border-bottom: 3px solid var(--accent); 
      padding: 12px 20px; 
      position: sticky; 
      top: 0; 
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    
    .logo {{ font-size: 1.4em; font-weight: 900; letter-spacing: -1px; }}
    .logo span {{ color: var(--accent); }}
    
    .theme-toggle {{
      background: none;
      border: 1px solid var(--border);
      color: var(--text-secondary);
      padding: 6px 12px;
      border-radius: 20px;
      cursor: pointer;
    }}
    
    .nav {{ 
      background: var(--bg-secondary); 
      padding: 8px 20px; 
      display: flex; 
      gap: 6px; 
      overflow-x: auto;
      border-bottom: 1px solid var(--border);
    }}
    
    .nav a {{ 
      background: none; 
      border: 1px solid var(--border); 
      color: var(--text-secondary); 
      padding: 4px 12px; 
      border-radius: 20px; 
      text-decoration: none;
      font-size: 0.8em;
      white-space: nowrap;
    }}
    
    .nav a:hover {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    
    .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
    
    .section {{ margin-bottom: 40px; }}
    
    .section-title {{ 
      font-size: 0.75em; 
      font-weight: 700; 
      text-transform: uppercase; 
      letter-spacing: 2px; 
      color: var(--accent); 
      border-left: 3px solid var(--accent); 
      padding-left: 10px; 
      margin-bottom: 16px;
    }}
    
    .grid {{ 
      display: grid; 
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
      gap: 16px; 
    }}
    
    .card {{ 
      background: var(--bg-card); 
      border: 1px solid var(--border); 
      border-radius: 6px; 
      padding: 16px;
    }}
    
    .card-title {{ 
      font-size: 1em; 
      font-weight: 600; 
      line-height: 1.4; 
      margin-bottom: 8px; 
    }}
    
    .card-title a {{ color: var(--text-primary); text-decoration: none; }}
    .card-title a:hover {{ color: var(--accent); }}
    
    .card-meta {{ 
      font-size: 0.75em; 
      color: var(--text-secondary); 
      margin-bottom: 8px;
    }}
    
    .card-summary {{ 
      font-size: 0.88em; 
      color: var(--text-secondary); 
      line-height: 1.5; 
    }}
    
    .footer {{ 
      text-align: center; 
      padding: 30px; 
      color: var(--text-secondary); 
      font-size: 0.8em; 
      border-top: 1px solid var(--border);
      margin-top: 40px; 
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="logo">PRAS<span>ÓWKA</span></div>
    <div>{date_str}</div>
    <button class="theme-toggle" onclick="toggleTheme()">🌓</button>
  </div>
  
  <nav class="nav">
    {''.join(f'<a href="#{tid}">{tinfo["name"]}</a>' for tid, tinfo in articles_by_topic.items())}
  </nav>
  
  <div class="container">
'''
    
    # Dodaj sekcje dla każdego tematu
    for topic_id, topic_data in articles_by_topic.items():
        name = topic_data["name"]
        articles = topic_data["articles"]
        count = len(articles)
        
        html += f'''
    <section class="section" id="{topic_id}">
      <div class="section-title">{name} — {count} artykułów</div>
      <div class="grid">
'''
        
        for article in articles:
            title = article.get("title", "Bez tytułu")
            url = article.get("url", "#")
            source = article.get("source", "Unknown")
            summary = article.get("summary", "")[:200]
            if summary:
                summary += "..."
            
            html += f'''
        <article class="card">
          <div class="card-title"><a href="{url}" target="_blank">{title}</a></div>
          <div class="card-meta">{source}</div>
          <div class="card-summary">{summary}</div>
        </article>
'''
        
        html += '''
      </div>
    </section>
'''
    
    html += f'''
  </div>
  
  <div class="footer">
    Wygenerowano przez OpenClaw · {datetime.now().strftime("%H:%M CET")}
  </div>
  
  <script>
    function toggleTheme() {{
      document.documentElement.toggleAttribute('data-theme', 'light');
      localStorage.setItem('theme', document.documentElement.hasAttribute('data-theme') ? 'light' : 'dark');
    }}
    
    // Load saved theme
    if (localStorage.getItem('theme') === 'light') {{
      document.documentElement.setAttribute('data-theme', 'light');
    }}
  </script>
</body>
</html>'''
    
    return html

def main():
    date_str = datetime.now().strftime("%Y%m%d")
    full_date = datetime.now().strftime("%A, %d %B %Y")
    
    print(f"🗞️  Prasówka — {full_date}", flush=True)
    print("=" * 50, flush=True)
    
    # 1. Wczytaj konfigurację
    topics = load_topics()
    seen_urls = load_seen_urls()
    
    print(f"📋 Tematy do pobrania: {len(topics)}", flush=True)
    
    # 2. Pobierz newsy dla każdego tematu
    articles_by_topic = {}
    new_urls = set()
    
    for topic_id, topic_info in topics.items():
        print(f"🔍 {topic_info['name']}...", flush=True)
        
        # Pobierz newsy ze wszystkich źródeł dla tego tematu
        articles = fetch_topic_news(topic_id, topic_info["count"])
        
        if not articles:
            print(f"  ⚠️  brak wyników", flush=True)
            continue
        
        # Filtruj nowe
        new_articles = [a for a in articles if isinstance(a, dict) and a.get("url") not in seen_urls]
        
        # Ogranicz do limitu
        new_articles = new_articles[:topic_info["count"]]
        
        print(f"  ✓ {len(new_articles)} nowych", flush=True)
        
        if new_articles:
            articles_by_topic[topic_id] = {
                "name": topic_info["name"],
                "articles": new_articles
            }
            new_urls.update(a.get("url") for a in new_articles if isinstance(a, dict))
    
    if not articles_by_topic:
        print("❌ Brak artykułów do wyświetlenia", flush=True)
        return
    
    # 3. Generuj HTML
    print("\n📝 Generowanie HTML...", flush=True)
    html = generate_html(articles_by_topic, full_date)
    
    # 4. Zapisz
    output_file = CANVAS_DIR / f"prasowka-{date_str}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"💾 Zapisano: {output_file}", flush=True)
    
    # 5. Aktualizuj seen_urls
    seen_urls.update(new_urls)
    save_seen_urls(seen_urls)
    
    total_articles = sum(len(t["articles"]) for t in articles_by_topic.values())
    print(f"\n✅ Gotowe! {total_articles} artykułów z {len(articles_by_topic)} kategorii", flush=True)
    
    # Zwróć info do parent process
    print(f"OUTPUT_FILE:{output_file}", flush=True)
    print(f"ARTICLES:{total_articles}", flush=True)
    print(f"CATEGORIES:{len(articles_by_topic)}", flush=True)

if __name__ == "__main__":
    main()
