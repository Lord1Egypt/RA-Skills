#!/usr/bin/env python3
"""
prasowka_real.py - Generuje prasówkę z PRAWDAZIWYCH danych + streszczenia
Łączy fetch_news.py z generate_html.py
v2.0 - Więcej źródeł, streszczenia 1-2 zdania
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

# Template HTML - rozbudowany
TEMPLATE = '''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prasówka — {date}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; min-height: 100vh; }}
    .header {{ background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); padding: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1); position: sticky; top: 0; z-index: 100; }}
    .header h1 {{ font-size: 2.5rem; background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .header .meta {{ color: #888; margin-top: 0.5rem; }}
    .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
    .section {{ margin-bottom: 3rem; }}
    .section-title {{ font-size: 1.5rem; margin-bottom: 1rem; color: #f5576c; border-left: 4px solid #f5576c; padding-left: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .section-count {{ background: rgba(245,87,108,0.2); color: #f5576c; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; }}
    .card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1); transition: all 0.3s; display: flex; flex-direction: column; }}
    .card:hover {{ transform: translateY(-4px); background: rgba(255,255,255,0.08); box-shadow: 0 10px 40px rgba(0,0,0,0.3); }}
    .card-source {{ color: #f093fb; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }}
    .card-title {{ font-size: 1.15rem; margin-bottom: 0.75rem; line-height: 1.4; font-weight: 600; }}
    .card-title a {{ color: #fff; text-decoration: none; }}
    .card-title a:hover {{ color: #f5576c; }}
    .card-summary {{ color: #aaa; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem; flex-grow: 1; }}
    .card-meta {{ color: #666; font-size: 0.8rem; display: flex; gap: 1rem; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 0.75rem; }}
    .score {{ color: #4ade80; }}
    .comments {{ color: #60a5fa; }}
    .footer {{ text-align: center; padding: 3rem; color: #666; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 3rem; }}
    .stats {{ display: flex; gap: 2rem; margin-top: 1rem; flex-wrap: wrap; }}
    .stat {{ background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 8px; }}
    .stat-value {{ color: #f5576c; font-weight: 700; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="container">
      <h1>🗞️ PRASÓWKA</h1>
      <div class="meta">{full_date} · {total} artykułów z {sources} źródeł</div>
      <div class="stats">
        <div class="stat">🔥 <span class="stat-value">{total}</span> artykułów</div>
        <div class="stat">📡 <span class="stat-value">{sources}</span> źródeł</div>
        <div class="stat">⭐ <span class="stat-value">{top_score}</span> max score</div>
      </div>
    </div>
  </div>
  <div class="container">
    {sections}
  </div>
  <div class="footer">
    Generowane przez OpenClaw · {timestamp}
  </div>
</body>
</html>'''

def fetch_all_news():
    """Pobiera newsy z wszystkich źródeł - ROZSZERZONA LISTA"""
    sources = [
        # AI & Tech
        ("hackernews", "Hacker News", 15),
        ("github", "GitHub Trending", 10),
        ("reddit-artificial", "Reddit r/artificial", 12),
        ("reddit-singularity", "Reddit r/singularity", 10),
        ("v2ex", "V2EX", 10),
        # General Tech
        ("reddit-tech", "Reddit r/technology", 12),
        ("reddit-programming", "Reddit r/programming", 10),
        # Science
        ("reddit-science", "Reddit r/science", 10),
        ("reddit-space", "Reddit r/space", 8),
        # World & Business
        ("reddit-worldnews", "Reddit r/worldnews", 12),
        ("wallstreetcn", "WallStreetCN", 10),
        # Markets & Crypto
        ("reddit-stocks", "Reddit r/stocks", 8),
        ("reddit-investing", "Reddit r/investing", 8),
        ("reddit-crypto", "Reddit r/CryptoCurrency", 8),
    ]
    
    all_news = []
    for source, label, limit in sources:
        try:
            print(f"  🔍 {label}...", flush=True)
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "fetch_news.py"), "--source", source, "--limit", str(limit)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                items = json.loads(result.stdout)
                count = 0
                for item in items:
                    if isinstance(item, dict) and "error" not in item and "note" not in item:
                        item["_category"] = label
                        item["_summary"] = generate_summary(item)
                        all_news.append(item)
                        count += 1
                print(f"     ✓ {count} artykułów")
            else:
                print(f"     ✗ błąd: {result.stderr[:50]}")
        except Exception as e:
            print(f"     ✗ error: {e}")
    
    return all_news

def generate_summary(item):
    """Generuje streszczenie 1-2 zdania na podstawie dostępnych danych"""
    title = item.get("title", "")
    
    # Jeśli jest opis (z GitHub), użyj go
    if "description" in item and item["description"]:
        desc = item["description"].strip()
        if len(desc) > 20:
            # Skróć do 1-2 zdań
            sentences = desc.split('. ')
            if len(sentences) >= 2:
                return sentences[0] + '. ' + sentences[1] + '.'
            return desc[:150] + "..." if len(desc) > 150 else desc
    
    # Fallback: wygeneruj kontekst z tytułu
    source = item.get("source", "")
    score = item.get("score", 0)
    comments = item.get("comments", 0)
    
    parts = []
    if score > 0:
        parts.append(f"popularny artykuł ({score} pkt)")
    if comments > 0:
        parts.append(f"{comments} komentarzy")
    if "language" in item and item["language"]:
        parts.append(f"tech: {item['language']}")
    
    if parts:
        return f"{' | '.join(parts)}. Kliknij aby przeczytać więcej."
    
    return "Kliknij aby przeczytać pełny artykuł."

def generate_card(item):
    """Generuje kartę artykułu ze streszczeniem"""
    title = item.get("title", "Bez tytułu")
    url = item.get("url", "#")
    source = item.get("source", "Unknown")
    time = item.get("time", "")
    score = item.get("score", 0)
    comments = item.get("comments", 0)
    summary = item.get("_summary", "")
    
    score_html = f'<span class="score">▲ {score}</span>' if score else ''
    comments_html = f'<span class="comments">💬 {comments}</span>' if comments else ''
    
    return f'''
    <div class="card">
      <div class="card-source">{source}</div>
      <h3 class="card-title"><a href="{url}" target="_blank">{title}</a></h3>
      <div class="card-summary">{summary}</div>
      <div class="card-meta">
        <span>📅 {time}</span>
        {score_html}
        {comments_html}
      </div>
    </div>
'''

def main():
    print("🗞️ Pobieram prawdziwe newsy...")
    print("=" * 50)
    
    news = fetch_all_news()
    
    if not news:
        print("❌ Brak newsów - generuję pusty template")
        news = [{"title": "Brak danych - sprawdź połączenie", "url": "#", "source": "Error", "time": "now", "_summary": "Problem z pobieraniem danych."}]
    
    # Grupuj według kategorii
    by_category = {}
    for item in news:
        cat = item.get("_category", "Inne")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)
    
    # Sortuj kategorie po liczbie artykułów
    sorted_categories = sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Generuj sekcje
    sections_html = ""
    for category, items in sorted_categories:
        cards = "\n".join(generate_card(item) for item in items[:10])  # Max 10 per category
        sections_html += f'''
    <div class="section">
      <h2 class="section-title">{category} <span class="section-count">{len(items)}</span></h2>
      <div class="grid">
        {cards}
      </div>
    </div>
'''
    
    # Znajdź max score
    max_score = max((item.get("score", 0) for item in news if isinstance(item.get("score"), (int, float))), default=0)
    
    # Generuj HTML
    now = datetime.now()
    html = TEMPLATE.format(
        date=now.strftime('%Y%m%d'),
        full_date=now.strftime('%A, %d %B %Y'),
        timestamp=now.strftime('%H:%M CET'),
        total=len(news),
        sources=len(by_category),
        top_score=max_score,
        sections=sections_html
    )
    
    # Zapisz
    output_dir = Path("/Volumes/2TB_APFS/openclaw-data/canvas")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"prasowka-{now.strftime('%Y%m%d')}.html"
    
    output_file.write_text(html, encoding='utf-8')
    print("=" * 50)
    print(f"✅ Prasówka zapisana: {output_file}")
    print(f"📊 {len(news)} artykułów z {len(by_category)} kategorii")
    print(f"🔥 Najwyższy score: {max_score}")
    
    # Pokaż breakdown
    print("\n📈 Breakdown:")
    for cat, items in sorted_categories[:5]:
        print(f"   {cat}: {len(items)} artykułów")

if __name__ == "__main__":
    main()
