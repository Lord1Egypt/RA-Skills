#!/usr/bin/env python3
"""
Movie Page Generator
Generates an HTML page for movie playback with an embedded player.
Supports multiple streaming sources with in-page switching.
"""

import sys
import json
import argparse
from datetime import datetime


def _escape_html(text: str) -> str:
    """Escape HTML special characters to prevent injection / broken layout."""
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _build_genre_tags(genres: list) -> str:
    """Build HTML for genre tag chips."""
    if not genres:
        return ""
    tags = []
    for g in genres:
        g = _escape_html(g)
        tags.append(f'<span class="genre-chip">{g}</span>')
    return "".join(tags)


def _build_source_buttons(sources: list) -> str:
    """Build HTML for source selector buttons (with data-src for JS switching)."""
    if not sources:
        return ""
    buttons = []
    for i, src in enumerate(sources):
        name = _escape_html(src.get("name", f"Source {i+1}"))
        url = _escape_html(src.get("url", ""))
        active = "active" if i == 0 else ""
        buttons.append(
            f'<button class="src-btn {active}" data-src="{url}" onclick="switchSource(this)">{name}</button>'
        )
    return "".join(buttons)


def generate_movie_html(
    title,
    year,
    rating="0",
    plot="",
    poster_url="",
    runtime="",
    director="",
    cast="",
    genres=None,
    sources=None,
):
    """Generate a self-contained HTML page for movie playback.

    Args:
        title:       Movie title.
        year:        Release year.
        rating:      Rating string (e.g. "8.5").
        plot:        Plot summary.
        poster_url:  Poster image URL.
        runtime:     Runtime string (e.g. "148" minutes).
        director:    Director name(s).
        cast:        Cast string.
        genres:      List of genre strings.
        sources:     List of {"name": str, "url": str} dicts. First entry is the
                     default source. All sources are switchable in-page.
    """
    if sources is None:
        sources = []
    if genres is None:
        genres = []

    safe_title = _escape_html(title)
    safe_plot = _escape_html(plot)
    safe_director = _escape_html(director)
    safe_cast = _escape_html(cast)
    safe_poster = _escape_html(poster_url)
    safe_year = _escape_html(year)
    safe_rating = _escape_html(rating)
    safe_runtime = _escape_html(runtime)

    genre_tags = _build_genre_tags(genres)
    source_buttons = _build_source_buttons(sources)
    primary_src = sources[0]["url"] if sources else ""

    runtime_html = f'<span class="meta-item">⏱ {safe_runtime} 分钟</span>' if safe_runtime else ""
    director_html = f'<span class="meta-item">🎬 {safe_director}</span>' if safe_director else ""
    genres_html = f'<div class="genres">{genre_tags}</div>' if genre_tags else ""
    cast_html = f'<p class="cast"><strong>主演：</strong>{safe_cast}</p>' if safe_cast else ""

    sources_section = ""
    if len(sources) > 1:
        sources_section = f'''
  <div class="sources-bar">
    <span class="sources-label">播放源：</span>
    <div class="source-buttons">{source_buttons}</div>
  </div>'''

    generated_date = datetime.now().strftime("%Y-%m-%d")

    # NOTE: Using a plain string (NOT an f-string) so CSS braces need no escaping.
    template = '''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ (__YEAR__) - 在线观看</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0f0f1a;
    --card: rgba(255,255,255,0.05);
    --card-border: rgba(255,255,255,0.1);
    --text: #fff;
    --text-dim: #aaa;
    --text-muted: #666;
    --accent: #e50914;
    --accent-hover: #ff1a25;
    --gold: #f5c518;
  }
  body {
    background: linear-gradient(135deg, #0f0f1a 0%, #16213e 100%);
    color: var(--text);
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    line-height: 1.6;
    padding: 20px;
    min-height: 100vh;
  }
  .container { max-width: 1000px; margin: 0 auto; }

  /* --- Movie info card --- */
  .movie-info {
    display: flex; gap: 30px; margin-bottom: 25px;
    background: var(--card); border: 1px solid var(--card-border);
    padding: 25px; border-radius: 15px; flex-wrap: wrap;
  }
  .poster { flex: 0 0 220px; }
  .poster img {
    width: 100%; border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .details { flex: 1; min-width: 280px; }
  .details h1 { font-size: 1.9em; margin-bottom: 12px; }
  .meta-row { display: flex; gap: 16px; margin-bottom: 14px; flex-wrap: wrap; align-items: center; }
  .meta-item { color: var(--text-dim); font-size: 0.92em; }
  .rating-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(245,197,24,0.15); color: var(--gold);
    padding: 4px 14px; border-radius: 20px; font-weight: bold; font-size: 0.95em;
  }
  .year-badge {
    background: rgba(255,255,255,0.1); padding: 4px 14px;
    border-radius: 20px; font-size: 0.92em;
  }
  .genres { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .genre-chip {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
    padding: 3px 12px; border-radius: 15px; font-size: 0.82em; color: var(--text-dim);
  }
  .plot { line-height: 1.8; color: #ccc; margin-bottom: 14px; }
  .cast { color: var(--text-dim); font-size: 0.9em; }
  .cast strong { color: #bbb; }

  /* --- Player --- */
  .player-section { margin-bottom: 20px; }
  .player-wrapper {
    position: relative; width: 100%; padding-top: 56.25%; /* 16:9 */
    background: #000; border-radius: 12px; overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
  }
  .player-wrapper iframe {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;
  }
  .player-loading {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    color: var(--text-dim); font-size: 1.1em;
    background: #000; z-index: 1; transition: opacity 0.4s;
  }
  .player-loading.hidden { opacity: 0; pointer-events: none; }
  .player-loading .spinner {
    width: 42px; height: 42px; border: 3px solid rgba(255,255,255,0.15);
    border-top-color: var(--accent); border-radius: 50%;
    animation: spin 0.8s linear infinite; margin-bottom: 14px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .player-loading-inner { display: flex; flex-direction: column; align-items: center; }

  /* --- Source switcher --- */
  .sources-bar {
    display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
    background: var(--card); border: 1px solid var(--card-border);
    padding: 14px 20px; border-radius: 12px; margin-bottom: 20px;
  }
  .sources-label { color: var(--text-dim); font-size: 0.9em; white-space: nowrap; }
  .source-buttons { display: flex; gap: 8px; flex-wrap: wrap; }
  .src-btn {
    padding: 7px 18px; background: rgba(255,255,255,0.08);
    color: var(--text-dim); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 6px; cursor: pointer; font-size: 0.88em; transition: all 0.2s;
  }
  .src-btn:hover { background: rgba(255,255,255,0.15); color: var(--text); }
  .src-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }

  .footer { text-align: center; margin-top: 35px; color: var(--text-muted); font-size: 0.82em; }
  .footer a { color: var(--text-dim); }

  @media (max-width: 640px) {
    body { padding: 12px; }
    .movie-info { padding: 16px; gap: 16px; }
    .poster { flex: 0 0 130px; }
    .details h1 { font-size: 1.4em; }
  }
</style>
</head>
<body>
<div class="container">

  <div class="movie-info">
    <div class="poster">
      <img src="__POSTER__" alt="__TITLE__"
           onerror="this.onerror=null;this.src='data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22220%22 height=%22330%22%3E%3Crect fill=%22%23222%22 width=%22220%22 height=%22330%22/%3E%3Ctext x=%22110%22 y=%22172%22 fill=%22%23666%22 font-size=%2216%22 text-anchor=%22middle%22 font-family=%22sans-serif%22%3E无海报%3C/text%3E%3C/svg%3E';">
    </div>
    <div class="details">
      <h1>__TITLE__</h1>
      <div class="meta-row">
        <span class="year-badge">__YEAR__</span>
        <span class="rating-badge">★ __RATING__</span>
        __RUNTIME__
        __DIRECTOR__
      </div>
      __GENRES__
      <p class="plot">__PLOT__</p>
      __CAST__
    </div>
  </div>

  <div class="player-section">
    <div class="player-wrapper">
      <div class="player-loading" id="playerLoading">
        <div class="player-loading-inner">
          <div class="spinner"></div>
          <span>正在加载播放器…</span>
        </div>
      </div>
      <iframe id="playerFrame" src="__PRIMARY_SRC__"
              allowfullscreen allow="autoplay; encrypted-media; picture-in-picture"
              referrerpolicy="origin"
              onload="document.getElementById('playerLoading').classList.add('hidden')"></iframe>
    </div>
  </div>
__SOURCES_SECTION__
  <div class="footer">
    <p>__TITLE__ (__YEAR__) · 由 Movie Finder Skill 生成 · __DATE__</p>
    <p style="margin-top:6px;">播放源来自第三方，仅供学习交流，请支持正版</p>
  </div>
</div>
<script>
  function switchSource(btn) {
    var src = btn.getAttribute("data-src");
    if (!src) return;
    document.querySelectorAll(".src-btn").forEach(function(b){ b.classList.remove("active"); });
    btn.classList.add("active");
    var loading = document.getElementById("playerLoading");
    var frame = document.getElementById("playerFrame");
    loading.classList.remove("hidden");
    frame.src = src;
  }
  // Hide loading after a timeout as a fallback (some embeds don't fire onload reliably)
  setTimeout(function(){
    document.getElementById("playerLoading").classList.add("hidden");
  }, 8000);
</script>
</body>
</html>'''

    # Simple placeholder replacement — no f-string, so CSS braces are untouched.
    html = template
    replacements = {
        "__TITLE__": safe_title,
        "__YEAR__": safe_year,
        "__RATING__": safe_rating,
        "__PLOT__": safe_plot,
        "__POSTER__": safe_poster,
        "__RUNTIME__": runtime_html,
        "__DIRECTOR__": director_html,
        "__GENRES__": genres_html,
        "__CAST__": cast_html,
        "__PRIMARY_SRC__": _escape_html(primary_src),
        "__SOURCES_SECTION__": sources_section,
        "__DATE__": generated_date,
    }
    for key, val in replacements.items():
        html = html.replace(key, val)

    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate a movie playback HTML page with embedded player."
    )
    parser.add_argument("--title", required=True, help="Movie title")
    parser.add_argument("--year", required=True, help="Release year")
    parser.add_argument("--rating", default="0", help="Rating (e.g. 8.5)")
    parser.add_argument("--plot", default="", help="Plot summary")
    parser.add_argument("--poster", default="", help="Poster image URL")
    parser.add_argument("--runtime", default="", help="Runtime in minutes")
    parser.add_argument("--director", default="", help="Director name(s)")
    parser.add_argument("--cast", default="", help="Cast (comma-separated)")
    parser.add_argument("--genres", default="", help="Genres (comma-separated)")
    parser.add_argument(
        "--sources",
        default="",
        help='Streaming sources as JSON: [{"name":"src1","url":"..."},...]. '
        "First entry is the default. All are switchable in-page.",
    )
    parser.add_argument("--output", default="", help="Output file path (stdout if omitted)")

    args = parser.parse_args()

    genres = [g.strip() for g in args.genres.split(",") if g.strip()] if args.genres else []

    sources = []
    if args.sources:
        try:
            sources = json.loads(args.sources)
        except json.JSONDecodeError as e:
            print(f"Warning: failed to parse --sources JSON: {e}", file=sys.stderr)

    if not sources:
        print("Error: at least one streaming source is required via --sources.", file=sys.stderr)
        sys.exit(1)

    html = generate_movie_html(
        title=args.title,
        year=args.year,
        rating=args.rating,
        plot=args.plot,
        poster_url=args.poster,
        runtime=args.runtime,
        director=args.director,
        cast=args.cast,
        genres=genres,
        sources=sources,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML page saved to: {args.output}")
    else:
        print(html)


if __name__ == "__main__":
    main()
