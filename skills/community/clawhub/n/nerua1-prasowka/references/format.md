# Format HTML — Portal Newsowy

## Styl: CNN-like, ciemny motyw, responsywny

Użyj tego szablonu jako bazy. Wypełnij sekcje artykułami z każdego tematu.

```html
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prasówka — [DATA]</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, 'Helvetica Neue', sans-serif; background: #0d0d0d; color: #e8e8e8; }

/* Header */
.site-header { background: #111; border-bottom: 3px solid #c00; padding: 12px 20px; position: sticky; top: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; }
.site-logo { font-size: 1.4em; font-weight: 900; color: #fff; letter-spacing: -1px; }
.site-logo span { color: #c00; }
.site-date { color: #888; font-size: 0.85em; }

/* Nav categories */
.cat-nav { background: #1a1a1a; padding: 8px 20px; display: flex; gap: 6px; overflow-x: auto; border-bottom: 1px solid #222; }
.cat-btn { background: none; border: 1px solid #333; color: #aaa; padding: 4px 12px; border-radius: 20px; cursor: pointer; font-size: 0.8em; white-space: nowrap; text-decoration: none; }
.cat-btn:hover { background: #c00; border-color: #c00; color: #fff; }

/* Main layout */
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }

/* Section */
.section { margin-bottom: 40px; }
.section-title { font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: #c00; border-left: 3px solid #c00; padding-left: 10px; margin-bottom: 16px; }

/* Article grid */
.articles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }

/* Article card */
.article { background: #171717; border: 1px solid #222; border-radius: 6px; padding: 16px; transition: border-color 0.2s; }
.article:hover { border-color: #c00; }
.article-title { font-size: 1em; font-weight: 600; line-height: 1.4; margin-bottom: 8px; }
.article-title a { color: #f0f0f0; text-decoration: none; }
.article-title a:hover { color: #ff6b6b; }
.article-meta { font-size: 0.75em; color: #666; margin-bottom: 8px; display: flex; gap: 10px; }
.article-summary { font-size: 0.88em; color: #aaa; line-height: 1.5; }
.article-tags { margin-top: 10px; display: flex; gap: 6px; flex-wrap: wrap; }
.tag { font-size: 0.7em; background: #222; color: #888; padding: 2px 8px; border-radius: 10px; }

/* Featured (top story) */
.featured { grid-column: 1 / -1; background: #1a0a0a; border-color: #c00; }
.featured .article-title { font-size: 1.3em; }

/* Footer */
.site-footer { text-align: center; padding: 30px; color: #444; font-size: 0.8em; border-top: 1px solid #1a1a1a; margin-top: 40px; }
</style>
</head>
<body>

<header class="site-header">
  <div class="site-logo">PRAS<span>ÓWKA</span></div>
  <div class="site-date">[DZIEŃ TYGODNIA], [DATA PEŁNA] · [GODZINA] CET</div>
</header>

<nav class="cat-nav">
  <a class="cat-btn" href="#ai-models">🤖 Modele AI</a>
  <a class="cat-btn" href="#ai-tools">🛠️ Narzędzia AI</a>
  <a class="cat-btn" href="#ai-video">🎬 AI Wideo</a>
  <a class="cat-btn" href="#vibe-coding">💻 Vibe Coding</a>
  <a class="cat-btn" href="#tech-science">🔬 Technika</a>
  <a class="cat-btn" href="#space">🚀 Kosmos</a>
  <a class="cat-btn" href="#medicine">💊 Medycyna</a>
  <a class="cat-btn" href="#market">📈 Rynek</a>
  <a class="cat-btn" href="#world">🌍 Świat</a>
  <a class="cat-btn" href="#poland">🇵🇱 Polska</a>
</nav>

<div class="container">

  <section class="section" id="ai-models">
    <div class="section-title">🤖 Nowe modele AI — [LICZBA] artykułów</div>
    <div class="articles-grid">
      <!-- ARTYKUŁY AI-MODELS -->
      <!-- format każdego artykułu: -->
      <!--
      <article class="article [featured jeśli top]">
        <div class="article-title"><a href="[URL]" target="_blank">[WŁASNY TYTUŁ — nie clickbait]</a></div>
        <div class="article-meta"><span>[ŹRÓDŁO]</span><span>[DATA]</span></div>
        <div class="article-summary">[2-3 zdania własnego streszczenia po polsku]</div>
        <div class="article-tags"><span class="tag">#[TAG1]</span><span class="tag">#[TAG2]</span></div>
      </article>
      -->
    </div>
  </section>

  <section class="section" id="ai-tools">
    <div class="section-title">🛠️ Nowe narzędzia AI</div>
    <div class="articles-grid"><!-- ARTYKUŁY AI-TOOLS --></div>
  </section>

  <section class="section" id="ai-video">
    <div class="section-title">🎬 AI Wideo i Film</div>
    <div class="articles-grid"><!-- ARTYKUŁY AI-VIDEO --></div>
  </section>

  <section class="section" id="ai-agents">
    <div class="section-title">🤝 Agenty i Automatyzacja</div>
    <div class="articles-grid"><!-- ARTYKUŁY AI-AGENTS --></div>
  </section>

  <section class="section" id="ai-nsfw">
    <div class="section-title">🔞 Branża dla dorosłych AI</div>
    <div class="articles-grid"><!-- ARTYKUŁY AI-NSFW --></div>
  </section>

  <section class="section" id="vibe-coding">
    <div class="section-title">💻 Vibe Coding i Programowanie</div>
    <div class="articles-grid"><!-- ARTYKUŁY VIBE-CODING --></div>
  </section>

  <section class="section" id="tech-science">
    <div class="section-title">🔬 Technika i Wynalazki</div>
    <div class="articles-grid"><!-- ARTYKUŁY TECH-SCIENCE --></div>
  </section>

  <section class="section" id="space">
    <div class="section-title">🚀 Kosmos i Astronomia</div>
    <div class="articles-grid"><!-- ARTYKUŁY SPACE --></div>
  </section>

  <section class="section" id="quantum">
    <div class="section-title">⚛️ Fizyka Kwantowa</div>
    <div class="articles-grid"><!-- ARTYKUŁY QUANTUM --></div>
  </section>

  <section class="section" id="medicine">
    <div class="section-title">💊 Medycyna — Przełomy</div>
    <div class="articles-grid"><!-- ARTYKUŁY MEDICINE --></div>
  </section>

  <section class="section" id="market">
    <div class="section-title">📈 Rynek i Finanse</div>
    <div class="articles-grid"><!-- ARTYKUŁY MARKET --></div>
  </section>

  <section class="section" id="crypto">
    <div class="section-title">₿ Krypto</div>
    <div class="articles-grid"><!-- ARTYKUŁY CRYPTO --></div>
  </section>

  <section class="section" id="layoffs">
    <div class="section-title">📉 Zwolnienia i Podwyżki</div>
    <div class="articles-grid"><!-- ARTYKUŁY LAYOFFS --></div>
  </section>

  <section class="section" id="world">
    <div class="section-title">🌍 Świat</div>
    <div class="articles-grid"><!-- ARTYKUŁY WORLD --></div>
  </section>

  <section class="section" id="poland">
    <div class="section-title">🇵🇱 Polska</div>
    <div class="articles-grid"><!-- ARTYKUŁY POLAND --></div>
  </section>

</div>

<footer class="site-footer">
  Wygenerowano przez OpenClaw · [TIMESTAMP] · [LICZBA ARTYKUŁÓW] artykułów z [LICZBA ŹRÓDEŁ] źródeł
</footer>

</body>
</html>
```
