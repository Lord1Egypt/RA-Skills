#!/usr/bin/env python3
"""
generate_html.py - Generuje prasówkę HTML z użyciem szablonu modern.html
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Template z placeholderami
TEMPLATE = '''<!DOCTYPE html>
<html lang="pl" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="description" content="Prasówka — codzienny przegląd najważniejszych wiadomości z AI, technologii, nauki i świata">
  <meta name="theme-color" content="#dc2626">
  <meta name="color-scheme" content="light dark">
  <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiUHJhc8OzdrthIiwic2hvcnRfbmFtZSI6IlByYXNvd2thIiwic3RhcnRfdXJsIjoiLyIsImRpc3BsYXkiOiJzdGFuZGFsb25lIiwiYmFja2dyb3VuZF9jb2xvciI6IiMwYTBhMGEiLCJ0aGVtZV9jb2xvciI6IiNkYzI2MjYiLCJpY29ucyI6W3sic3JjIjoiZGF0YTppbWFnZS9zdmcreG1sLCUzQ3N2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAxOTIgMTkyJyUzRSUzQ3JlY3Qgd2lkdGg9JzE5MicgaGVpZ2h0PScxOTInIGZpbGw9JyUyM2RjMjYyNicgcng9JzI0Jy8lM0UlM0N0ZXh0IHg9Jzk2JyB5PScxMjAnIGZvbnQtc2l6ZT0nMTAwJyB0ZXh0LWFuY2hvcj0nbWlkZGxlJyUzRSUztZG8lMjIlM0UlM0Mvc3ZnJTNFIiwic2l6ZXMiOiIxOTJ4MTkyIiwidHlwZSI6ImltYWdlL3N2Zyt4bWwifV19">
  <title>Prasówka — {date}</title>
  <style>
{css}
  </style>
</head>
<body>
  <div class="scroll-progress" role="progressbar" aria-label="Scroll progress"></div>
  
  <header class="site-header">
    <div class="header-container">
      <div class="site-brand">
        <a href="#" class="site-logo">
          <span class="site-logo-icon">🗞️</span>
          <span class="site-logo-text">PRASÓWKA</span>
        </a>
      </div>
      <div class="site-date">{full_date} · {article_count} artykułów</div>
      <div class="header-controls">
        <button class="theme-toggle" aria-label="Toggle dark/light mode" title="Toggle theme (T)">
          <span class="theme-toggle-slider">☀️</span>
        </button>
        <button class="refresh-btn" aria-label="Refresh news" title="Refresh (R)">🔄</button>
      </div>
    </div>
  </header>
  
  <nav class="site-nav" aria-label="Category navigation">
    <div class="nav-container">
      <a href="#models" class="nav-item active"><span>🧠 Modele</span></a>
      <a href="#tools" class="nav-item"><span>🛠️ Narzędzia</span></a>
      <a href="#video" class="nav-item"><span>🎬 Wideo</span></a>
      <a href="#agents" class="nav-item"><span>🤝 Agenty</span></a>
      <a href="#coding" class="nav-item"><span>💻 Coding</span></a>
      <a href="#tech" class="nav-item"><span>🔬 Tech</span></a>
      <a href="#space" class="nav-item"><span>🚀 Kosmos</span></a>
      <a href="#med" class="nav-item"><span>💊 Medycyna</span></a>
      <a href="#market" class="nav-item"><span>📈 Rynek</span></a>
      <a href="#world" class="nav-item"><span>🌍 Świat</span></a>
      <a href="#poland" class="nav-item"><span>🇵🇱 Polska</span></a>
    </div>
  </nav>
  
  <main class="main-content">
    <section class="stats-bar" aria-label="Statistics">
      <div class="stat-item"><div class="stat-value">{article_count}</div><div class="stat-label">Artykułów</div></div>
      <div class="stat-item"><div class="stat-value">{source_count}</div><div class="stat-label">Źródeł</div></div>
      <div class="stat-item"><div class="stat-value">{category_count}</div><div class="stat-label">Kategorii</div></div>
      <div class="stat-item"><div class="stat-value">{timestamp}</div><div class="stat-label">Aktualizacja</div></div>
    </section>
    
    <section class="section" id="models" aria-labelledby="models-heading">
      <header class="section-header">
        <h2 class="section-title" id="models-heading"><span class="section-icon">🧠</span>Nowe modele AI</h2>
        <span class="section-count">{ai_models_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{ai_models_articles}</div>
    </section>
    
    <section class="section" id="tools" aria-labelledby="tools-heading">
      <header class="section-header">
        <h2 class="section-title" id="tools-heading"><span class="section-icon">🛠️</span>Nowe narzędzia AI</h2>
        <span class="section-count">{ai_tools_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{ai_tools_articles}</div>
    </section>
    
    <section class="section" id="video" aria-labelledby="video-heading">
      <header class="section-header">
        <h2 class="section-title" id="video-heading"><span class="section-icon">🎬</span>AI Wideo i Film</h2>
        <span class="section-count">{ai_video_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{ai_video_articles}</div>
    </section>
    
    <section class="section" id="agents" aria-labelledby="agents-heading">
      <header class="section-header">
        <h2 class="section-title" id="agents-heading"><span class="section-icon">🤝</span>Agenty i Automatyzacja</h2>
        <span class="section-count">{ai_agents_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{ai_agents_articles}</div>
    </section>
    
    <section class="section" id="coding" aria-labelledby="coding-heading">
      <header class="section-header">
        <h2 class="section-title" id="coding-heading"><span class="section-icon">💻</span>Vibe Coding i Programowanie</h2>
        <span class="section-count">{vibe_coding_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{vibe_coding_articles}</div>
    </section>
    
    <section class="section" id="tech" aria-labelledby="tech-heading">
      <header class="section-header">
        <h2 class="section-title" id="tech-heading"><span class="section-icon">🔬</span>Technika i Wynalazki</h2>
        <span class="section-count">{tech_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{tech_articles}</div>
    </section>
    
    <section class="section" id="space" aria-labelledby="space-heading">
      <header class="section-header">
        <h2 class="section-title" id="space-heading"><span class="section-icon">🚀</span>Kosmos i Astronomia</h2>
        <span class="section-count">{space_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{space_articles}</div>
    </section>
    
    <section class="section" id="med" aria-labelledby="med-heading">
      <header class="section-header">
        <h2 class="section-title" id="med-heading"><span class="section-icon">💊</span>Medycyna — Przełomy</h2>
        <span class="section-count">{medicine_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{medicine_articles}</div>
    </section>
    
    <section class="section" id="market" aria-labelledby="market-heading">
      <header class="section-header">
        <h2 class="section-title" id="market-heading"><span class="section-icon">📈</span>Rynek i Finanse</h2>
        <span class="section-count">{market_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{market_articles}</div>
    </section>
    
    <section class="section" id="world" aria-labelledby="world-heading">
      <header class="section-header">
        <h2 class="section-title" id="world-heading"><span class="section-icon">🌍</span>Świat</h2>
        <span class="section-count">{world_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{world_articles}</div>
    </section>
    
    <section class="section" id="poland" aria-labelledby="poland-heading">
      <header class="section-header">
        <h2 class="section-title" id="poland-heading"><span class="section-icon">🇵🇱</span>Polska</h2>
        <span class="section-count">{poland_count} artykułów</span>
      </header>
      <div class="bento-grid" role="feed">{poland_articles}</div>
    </section>
  </main>
  
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-brand"><span>🗞️</span><span>Prasówka — generowane przez OpenClaw</span></div>
      <div class="footer-meta">{timestamp} · {article_count} artykułów z {source_count} źródeł</div>
      <nav class="footer-links" aria-label="Footer navigation">
        <a href="#" class="footer-link">O projekcie</a>
        <a href="#" class="footer-link">Źródła</a>
        <a href="#" class="footer-link">RSS</a>
      </nav>
    </div>
  </footer>
  
  <script>
{js}
  </script>
</body>
</html>'''

def generate_article_card(title, url, source, summary, date, size, tags):
    """Generuje kartę artykułu HTML"""
    return f'''    <article class="article-card {size}" data-url="{url}">
      <div class="article-meta">
        <span class="article-source">{source}</span>
        <span class="article-date">📅 {date}</span>
      </div>
      <h3 class="article-title">
        <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
      </h3>
      <p class="article-summary">{summary}</p>
      <div class="article-footer">
        <div class="article-tags">{tags}</div>
        <div class="article-actions">
          <button class="action-btn" data-action="bookmark" title="Bookmark">☆</button>
          <button class="action-btn" data-action="share" title="Share">↗️</button>
        </div>
      </div>
    </article>'''

def generate_tag(name):
    return f'<span class="tag">#{name}</span>'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, help='Output HTML file path')
    parser.add_argument('--css', required=True, help='Path to CSS file')
    parser.add_argument('--js', required=True, help='Path to JS file')
    args = parser.parse_args()
    
    # Read CSS and JS inline
    css = Path(args.css).read_text(encoding='utf-8')
    js = Path(args.js).read_text(encoding='utf-8')
    
    # Date
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    full_date = now.strftime('%A, %d %B %Y')
    timestamp = now.strftime('%H:%M CET')
    
    # Generate sample articles for each category
    ai_models_articles = [
        generate_article_card("OpenAI GPT-5 — pierwsze wrażenia", "https://openai.com", "OpenAI", 
            "Najnowszy model językowy od OpenAI zrewolucjonizuje sposób, w jaki pracujemy z AI. Lepsze rozumienie kontekstu, szybsze odpowiedzi.", 
            "2026-04-06", "featured", generate_tag("gpt5") + generate_tag("openai")),
        generate_article_card("Claude 4 — Anthropic odpowiada", "https://anthropic.com", "Anthropic",
            "Anthropic nie pozostaje w tyle i prezentuje Claude 4 z możliwościami agentowymi.",
            "2026-04-06", "large", generate_tag("claude") + generate_tag("anthropic")),
        generate_article_card("Google Gemini Ultra publicznie", "https://deepmind.google", "Google",
            "Gemini Ultra w końcu dostępny dla wszystkich bez opłat.",
            "2026-04-06", "medium", generate_tag("gemini") + generate_tag("google")),
        generate_article_card("Meta Llama 4", "https://ai.meta.com", "Meta",
            "Meta publikuje Llama 4 z licencją open source.",
            "2026-04-06", "medium", generate_tag("llama") + generate_tag("meta")),
    ]
    
    ai_tools_articles = [
        generate_article_card("Claude Code — edytor przyszłości", "https://claude.ai/code", "Anthropic",
            "Nowy edytor kodu od Anthropic integruje AI bezpośrednio w workflow deweloperski.",
            "2026-04-06", "large", generate_tag("coding") + generate_tag("ide")),
        generate_article_card("Cursor AI 1.0", "https://cursor.sh", "Cursor",
            "Cursor osiąga wersję 1.0 z agentami kodującymi end-to-end.",
            "2026-04-06", "medium", generate_tag("cursor") + generate_tag("ai")),
        generate_article_card("V0 by Vercel", "https://v0.dev", "Vercel",
            "Generowanie UI z promptów tekstowych osiąga nowy poziom.",
            "2026-04-06", "medium", generate_tag("v0") + generate_tag("ui")),
    ]
    
    ai_video_articles = [
        generate_article_card("Sora publiczne — rewolucja w video", "https://openai.com/sora", "OpenAI",
            "Sora od OpenAI teraz dostępna dla wszystkich. Generowanie filmów 1080p z tekstu.",
            "2026-04-06", "featured", generate_tag("sora") + generate_tag("video")),
        generate_article_card("Runway Gen-4", "https://runwayml.com", "Runway",
            "Nowa generacja modeli Runway z lepszą kontrolą nad ruchem kamery.",
            "2026-04-06", "medium", generate_tag("runway") + generate_tag("gen4")),
    ]
    
    ai_agents_articles = [
        generate_article_card("AutoGPT 2.0 — autonomiczne agenty", "https://agpt.co", "AutoGPT",
            "Powrót AutoGPT z prawdziwie autonomicznymi agentami.",
            "2026-04-06", "large", generate_tag("autogpt") + generate_tag("agents")),
        generate_article_card("LangGraph 1.0", "https://langchain.com", "LangChain",
            "Framework do budowania aplikacji z agentami osiąga dojrzałość.",
            "2026-04-06", "medium", generate_tag("langchain") + generate_tag("graph")),
    ]
    
    vibe_coding_articles = [
        generate_article_card("Vibe Coding — przyszłość dev", "https://x.com/karpathy", "Twitter/X",
            "Andrej Karpathy promuje nową erę programowania opartą na AI.",
            "2026-04-06", "featured", generate_tag("vibe") + generate_tag("coding")),
        generate_article_card("Bolt.new — fullstack AI", "https://bolt.new", "StackBlitz",
            "Generowanie pełnych aplikacji webowych z jednego promptu.",
            "2026-04-06", "medium", generate_tag("bolt") + generate_tag("fullstack")),
    ]
    
    tech_articles = [
        generate_article_card("TSMC 2nm w produkcji", "https://tsmc.com", "TSMC",
            "Najnowszy proces technologiczny obiecuje 30% wzrost wydajności.",
            "2026-04-06", "large", generate_tag("tsmc") + generate_tag("2nm")),
        generate_article_card("Apple M5 chip preview", "https://apple.com", "Apple",
            "Pierwsze testy M5 pokazują znaczący skok w ML.",
            "2026-04-06", "medium", generate_tag("apple") + generate_tag("m5")),
    ]
    
    space_articles = [
        generate_article_card("SpaceX Stacja Księżycowa", "https://spacex.com", "SpaceX",
            "Pierwsze moduły stacji księżycowej w drodze.",
            "2026-04-06", "featured", generate_tag("spacex") + generate_tag("moon")),
        generate_article_card("Webb — nowe egzoplanety", "https://nasa.gov", "NASA",
            "Teleskop Webba odkrył atrybuty atmosfery egzoplanety podobnej do Ziemi.",
            "2026-04-06", "medium", generate_tag("webb") + generate_tag("exoplanet")),
    ]
    
    medicine_articles = [
        generate_article_card("CRISPR 3.0 — nowe możliwości", "https://nature.com", "Nature",
            "Nowa generacja edycji genów z precyzją atomową.",
            "2026-04-06", "large", generate_tag("crispr") + generate_tag("genetics")),
    ]
    
    market_articles = [
        generate_article_card("NVIDIA traci 20% — AI bubble?", "https://bloomberg.com", "Bloomberg",
            "Analiza rynku sugeruje korektę po parabolicznym wzroście.",
            "2026-04-06", "featured", generate_tag("nvidia") + generate_tag("market")),
        generate_article_card("Fed obniża stopy", "https://reuters.com", "Reuters",
            "Pierwsza obniżka stóp od 2 lat. Reakcja rynków.",
            "2026-04-06", "medium", generate_tag("fed") + generate_tag("rates")),
    ]
    
    world_articles = [
        generate_article_card("Szczyt G7 o regulacji AI", "https://ft.com", "Financial Times",
            "Przywódcy G7 omawiają globalne standardy bezpieczeństwa AI.",
            "2026-04-06", "large", generate_tag("g7") + generate_tag("regulation")),
    ]
    
    poland_articles = [
        generate_article_card("Polski startup AI zyskuje $50M", "https://techcrunch.com", "TechCrunch",
            "Warszawski startup buduje konkurencję dla OpenAI.",
            "2026-04-06", "medium", generate_tag("poland") + generate_tag("startup")),
    ]
    
    # Join articles with newlines
    data = {
        'date': date_str,
        'full_date': full_date,
        'timestamp': timestamp,
        'article_count': 30,
        'source_count': 15,
        'category_count': 12,
        'css': css,
        'js': js,
        'ai_models_count': len(ai_models_articles),
        'ai_tools_count': len(ai_tools_articles),
        'ai_video_count': len(ai_video_articles),
        'ai_agents_count': len(ai_agents_articles),
        'vibe_coding_count': len(vibe_coding_articles),
        'tech_count': len(tech_articles),
        'space_count': len(space_articles),
        'medicine_count': len(medicine_articles),
        'market_count': len(market_articles),
        'world_count': len(world_articles),
        'poland_count': len(poland_articles),
        'ai_models_articles': '\n'.join(ai_models_articles),
        'ai_tools_articles': '\n'.join(ai_tools_articles),
        'ai_video_articles': '\n'.join(ai_video_articles),
        'ai_agents_articles': '\n'.join(ai_agents_articles),
        'vibe_coding_articles': '\n'.join(vibe_coding_articles),
        'tech_articles': '\n'.join(tech_articles),
        'space_articles': '\n'.join(space_articles),
        'medicine_articles': '\n'.join(medicine_articles),
        'market_articles': '\n'.join(market_articles),
        'world_articles': '\n'.join(world_articles),
        'poland_articles': '\n'.join(poland_articles),
    }
    
    # Generate HTML
    html = TEMPLATE.format(**data)
    
    # Write output
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"Generated: {args.output}")

if __name__ == '__main__':
    main()
