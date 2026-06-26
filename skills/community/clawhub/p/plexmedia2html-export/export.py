#!/usr/bin/env python3
"""
PlexMedia2HTML Export Skill - Multilingual + Secure Token Storage
Exportiert Plex Mediathek als statische HTML-Seiten.
Supports: German (de), English (en)
"""

import os
import sys
import json
import urllib.request
import ssl
import hashlib
import base64
from pathlib import Path
from html import escape as html_escape

# Skill-Konfiguration
SKILL_DIR = Path(__file__).parent
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "plexmedia2html-export"
CONFIG_FILE = DATA_DIR / "config.json"

# === SECURE TOKEN STORAGE ===


def get_machine_key():
    """Generiert einen eindeutigen Schlüssel für diese Maschine."""
    try:
        with open("/etc/machine-id", "r") as f:
            return f.read().strip()
    except:
        try:
            import socket
            import getpass

            return hashlib.sha256(
                f"{socket.gethostname()}-{getpass.getuser()}".encode()
            ).hexdigest()[:32]
        except:
            return "plexmedia2html-fallback-key-v1"


def encrypt_token(token):
    """Verschlüsselt einen Token mit XOR + Base64 (einfach aber effektiv)."""
    if not token:
        return ""
    key = get_machine_key()
    token_bytes = token.encode("utf-8")
    key_bytes = key.encode("utf-8")
    encrypted = bytearray()
    for i, byte in enumerate(token_bytes):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_token(encrypted_token):
    """Entschlüsselt einen Token."""
    if not encrypted_token:
        return ""
    key = get_machine_key()
    try:
        encrypted = base64.b64decode(encrypted_token)
        key_bytes = key.encode("utf-8")
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        return decrypted.decode("utf-8")
    except:
        return ""


# === I18N ===

TRANSLATIONS = {
    "de": {
        "title": "Plex Mediathek",
        "movies": "Filme",
        "series": "Serien",
        "season": "Staffel",
        "seasons": "Staffeln",
        "episode": "Episode",
        "episodes": "Episoden",
        "director": "Regie",
        "cast": "Besetzung",
        "summary": "Handlung",
        "media": "Medien",
        "genres": "Beliebte Genres",
        "latest_movies": "Neueste Filme",
        "latest_episodes": "Neueste Episoden",
        "stats": "Statistiken",
        "page": "Seite",
        "of": "von",
        "back": "Zurück",
        "next": "Weiter",
        "new": "NEU",
        "click_season": "Klicke auf eine Staffel",
        "export_complete": "✅ Export fertig!",
        "open_dashboard": "Öffne {path}/index.html im Browser",
        "loading_movies": "Lade Filme",
        "loading_series": "Lade Serien",
        "generating_html": "Generiere HTML",
        "total_movies": "{count} Filme",
        "total_series": "{count} Serien",
        "onboarding_required": "Onboarding erforderlich",
        "plex_url_prompt": "Plex-Server URL",
        "plex_token_prompt": "Plex Token",
        "export_path_prompt": "Export-Pfad",
        "config_saved": "Konfiguration gespeichert",
    },
    "en": {
        "title": "Plex Media Library",
        "movies": "Movies",
        "series": "TV Shows",
        "season": "Season",
        "seasons": "Seasons",
        "episode": "Episode",
        "episodes": "Episodes",
        "director": "Director",
        "cast": "Cast",
        "summary": "Summary",
        "media": "Media",
        "genres": "Popular Genres",
        "latest_movies": "Latest Movies",
        "latest_episodes": "Latest Episodes",
        "stats": "Statistics",
        "page": "Page",
        "of": "of",
        "back": "Back",
        "next": "Next",
        "new": "NEW",
        "click_season": "Click on a season",
        "export_complete": "✅ Export complete!",
        "open_dashboard": "Open {path}/index.html in browser",
        "loading_movies": "Loading movies",
        "loading_series": "Loading TV shows",
        "generating_html": "Generating HTML",
        "total_movies": "{count} Movies",
        "total_series": "{count} TV Shows",
        "onboarding_required": "Onboarding required",
        "plex_url_prompt": "Plex Server URL",
        "plex_token_prompt": "Plex Token",
        "export_path_prompt": "Export path",
        "config_saved": "Configuration saved",
    },
}


def _(key, lang="de", **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS["de"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


# === CONFIG ===

DEFAULT_CONFIG = {
    "plex_url": "",
    "plex_token_encrypted": "",
    "export_path": str(Path.home() / "Exports"),
    "movies_per_page": 18,
    "series_per_page": 18,
    "language": "de",
}


def load_config():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    return DEFAULT_CONFIG.copy()


def save_config(config):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Sicherstellen, dass Token verschlüsselt gespeichert wird
    if "plex_token" in config:
        if config["plex_token"]:
            config["plex_token_encrypted"] = encrypt_token(config["plex_token"])
        del config["plex_token"]
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    # Berechtigungen auf 600 setzen (nur Besitzer darf lesen/schreiben)
    CONFIG_FILE.chmod(0o600)


def get_token(config):
    return decrypt_token(config.get("plex_token_encrypted", ""))


def check_onboarding():
    config = load_config()
    lang = config.get("language", "de")
    token = get_token(config)

    if not config["plex_url"] or not token:
        print(f"⚠️  {_('onboarding_required', lang)}!")
        print()
        url = input(
            f"{_('plex_url_prompt', lang)} (e.g. http://192.168.1.100:32400): "
        ).strip()
        while not url:
            print("❌ URL required")
            url = input(f"{_('plex_url_prompt', lang)}: ").strip()
        config["plex_url"] = url

        print("\nPlex Token: Einstellungen → Allgemein → Erweitert → Token anzeigen")
        token = input(f"{_('plex_token_prompt', lang)}: ").strip()
        while not token:
            print("❌ Token required")
            token = input(f"{_('plex_token_prompt', lang)}: ").strip()
        config["plex_token"] = token  # Wird von save_config verschlüsselt

        print(f"\nLanguage [de/en] [{lang}]: ", end="")
        new_lang = input().strip()
        if new_lang in ["de", "en"]:
            config["language"] = new_lang
            lang = new_lang

        export_path = input(
            f"{_('export_path_prompt', lang)} [{config['export_path']}]: "
        ).strip()
        if export_path:
            config["export_path"] = export_path

        save_config(config)
        print(f"\n✅ {_('config_saved', lang)}!")
        print(f"🔐 Token is encrypted and stored securely.\n")

    return config


# === PLEX API ===


def fetch_plex_data(url, token, verify_ssl=True):
    """Fetches data from Plex API."""
    if verify_ssl:
        ctx = ssl.create_default_context()
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    headers = {"X-Plex-Token": token, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_libraries(base_url, token, verify_ssl=True):
    url = f"{base_url}/library/sections"
    data = fetch_plex_data(url, token, verify_ssl)
    return data.get("MediaContainer", {}).get("Directory", [])


def get_library_items(base_url, token, section_key, verify_ssl=True):
    url = f"{base_url}/library/sections/{section_key}/all"
    data = fetch_plex_data(url, token, verify_ssl)
    return data.get("MediaContainer", {}).get("Metadata", [])


def get_seasons(base_url, token, rating_key, verify_ssl=True):
    url = f"{base_url}/library/metadata/{rating_key}/children"
    data = fetch_plex_data(url, token, verify_ssl)
    return data.get("MediaContainer", {}).get("Metadata", [])


def get_episodes(base_url, token, season_key, verify_ssl=True):
    url = f"{base_url}/library/metadata/{season_key}/children"
    data = fetch_plex_data(url, token, verify_ssl)
    return data.get("MediaContainer", {}).get("Metadata", [])


def download_image(base_url, token, url_path, output_path, verify_ssl=True):
    if not url_path:
        return False
    if verify_ssl:
        ctx = ssl.create_default_context()
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    full_url = f"{base_url}{url_path}"
    headers = {"X-Plex-Token": token}
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return True
    except:
        return False


# === HTML GENERATION ===


def generate_html(config, movies, shows, lang="de", image_dir=None):
    t = lambda key: _(key, lang)

    OUTPUT_DIR = Path(config["export_path"]).expanduser()
    IMAGE_DIR = OUTPUT_DIR / "covers"
    MOVIES_PER_PAGE = config["movies_per_page"]
    SERIES_PER_PAGE = config["series_per_page"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)

    movies.sort(key=lambda x: x.get("titleSort") or x.get("title", ""))
    shows.sort(key=lambda x: x.get("titleSort") or x.get("title", ""))

    movie_pages = max(1, (len(movies) + MOVIES_PER_PAGE - 1) // MOVIES_PER_PAGE)
    series_pages = max(1, (len(shows) + SERIES_PER_PAGE - 1) // SERIES_PER_PAGE)

    from datetime import datetime

    exported_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_seasons = sum(len(s.get("seasons", [])) for s in shows)
    total_episodes = sum(
        sum(len(season.get("episodes", [])) for season in s.get("seasons", []))
        for s in shows
    )

    from collections import Counter

    movie_genres = Counter()
    for m in movies:
        for g in m.get("genres", []):
            movie_genres[g] += 1
    show_genres = Counter()
    for s in shows:
        for g in s.get("genres", []):
            show_genres[g] += 1

    top_movie_genres = movie_genres.most_common(10)

    def get_poster_html(rating_key, media_type):
        if image_dir:
            image_path = image_dir / f"{media_type}-{rating_key}.jpg"
            if image_path.exists():
                relative_path = f"covers/{media_type}-{rating_key}.jpg"
                return f'<img src="{relative_path}" alt="Poster" loading="lazy">'
        emoji = "🎬" if media_type == "movie" else "📺"
        return f'<div class="no-cover">{emoji}</div>'

    def get_large_poster_html(rating_key, media_type):
        if image_dir:
            image_path = image_dir / f"{media_type}-{rating_key}.jpg"
            if image_path.exists():
                relative_path = f"covers/{media_type}-{rating_key}.jpg"
                return f'<img src="{relative_path}" alt="Poster">'
        emoji = "🎬" if media_type == "movie" else "📺"
        return f'<div class="no-cover" style="width:100%;height:225px;font-size:4rem;">{emoji}</div>'

    css = f"""
:root {{ --bg-primary: #1a1a1a; --bg-secondary: #282828; --bg-tertiary: #333; --text-primary: #eee; --text-secondary: #aaa; --text-muted: #888; --accent: #e5a00d; --border: #333; }}
@media (prefers-color-scheme: light) {{ :root {{ --bg-primary: #f5f5f5; --bg-secondary: #fff; --bg-tertiary: #eee; --text-primary: #333; --text-secondary: #666; --text-muted: #999; --accent: #e5a00d; --border: #ddd; }}}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; line-height: 1.5; }}
header {{ background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary)); padding: 1.5rem; text-align: center; border-bottom: 1px solid var(--border); }}
h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
nav {{ display: flex; justify-content: center; gap: 1rem; padding: 1rem; background: var(--bg-secondary); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--border); }}
nav a {{ color: var(--text-secondary); text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; transition: all 0.2s; }}
nav a:hover, nav a.active {{ background: var(--accent); color: #000; }}
main {{ padding: 1rem; max-width: 1400px; margin: 0 auto; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }}
.card {{ background: var(--bg-secondary); border-radius: 8px; overflow: hidden; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; border: 1px solid var(--border); }}
.card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); border-color: var(--accent); }}
.poster {{ aspect-ratio: 2/3; background: var(--bg-tertiary); position: relative; overflow: hidden; }}
.poster img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }}
.card:hover .poster img {{ transform: scale(1.05); }}
.no-cover {{ width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 3rem; color: var(--text-muted); }}
.year {{ position: absolute; bottom: 0.5rem; left: 0.5rem; background: rgba(0,0,0,0.8); color: #fff; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }}
.info {{ padding: 0.75rem; }}
.info h3 {{ font-size: 0.9rem; margin-bottom: 0.3rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.meta {{ font-size: 0.75rem; color: var(--text-secondary); }}
.pagination {{ display: flex; justify-content: center; gap: 0.5rem; margin-top: 2rem; }}
.pagination a, .pagination button {{ padding: 0.5rem 1rem; background: var(--bg-secondary); color: var(--text-secondary); text-decoration: none; border-radius: 4px; border: 1px solid var(--border); cursor: pointer; font-size: 1rem; }}
.pagination a:hover, .pagination button:hover, .pagination a.active {{ background: var(--accent); color: #000; border-color: var(--accent); }}
.pagination button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
.modal-overlay {{ display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.85); z-index: 1000; padding: 2rem; overflow-y: auto; }}
.modal-overlay.active {{ display: flex; align-items: flex-start; justify-content: center; padding-top: 2rem; }}
.modal {{ background: var(--bg-secondary); border-radius: 12px; max-width: 800px; width: 100%; max-height: calc(100vh - 4rem); overflow-y: auto; position: relative; border: 1px solid var(--border); }}
.modal-close {{ position: absolute; top: 1rem; right: 1rem; background: var(--bg-tertiary); border: none; color: var(--text-primary); width: 36px; height: 36px; border-radius: 50%; cursor: pointer; font-size: 1.5rem; display: flex; align-items: center; justify-content: center; z-index: 10; }}
.modal-close:hover {{ background: var(--accent); color: #000; }}
.modal-header {{ display: flex; gap: 1.5rem; padding: 1.5rem; border-bottom: 1px solid var(--border); }}
.modal-poster {{ width: 150px; flex-shrink: 0; border-radius: 8px; overflow: hidden; background: var(--bg-tertiary); }}
.modal-poster img {{ width: 100%; height: auto; display: block; }}
.modal-title {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
.modal-meta {{ color: var(--text-secondary); margin-bottom: 0.5rem; }}
.modal-rating {{ color: #ffd700; }}
.modal-tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }}
.modal-tag {{ background: var(--bg-tertiary); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; }}
.modal-body {{ padding: 1.5rem; }}
.modal-section {{ margin-bottom: 1.5rem; }}
.modal-section h3 {{ color: var(--accent); margin-bottom: 0.5rem; font-size: 0.9rem; text-transform: uppercase; }}
.season-toggle {{ background: var(--bg-tertiary); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; transition: all 0.2s; }}
.season-toggle:hover {{ border-color: var(--accent); }}
.season-toggle h4 {{ font-size: 0.95rem; margin: 0; }}
.season-toggle .arrow {{ transition: transform 0.2s; }}
.season-toggle.open .arrow {{ transform: rotate(180deg); }}
.episodes-list {{ display: none; padding: 0.5rem 0 0.5rem 1rem; border-left: 2px solid var(--border); margin-left: 0.5rem; }}
.episodes-list.open {{ display: block; }}
.episode-item {{ padding: 0.5rem; border-radius: 4px; margin-bottom: 0.25rem; }}
.episode-item:hover {{ background: var(--bg-tertiary); }}
.episode-num {{ color: var(--accent); font-weight: bold; margin-right: 0.5rem; }}
.episode-title {{ font-size: 0.85rem; }}
.episode-date {{ color: var(--text-muted); font-size: 0.75rem; }}
.teaser-section {{ margin-top: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--border); }}
.teaser-grid-mini {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 0.75rem; }}
.teaser-poster-mini {{ aspect-ratio: 2/3; background: var(--bg-tertiary); border-radius: 4px; overflow: hidden; }}
.teaser-poster-mini img {{ width: 100%; height: 100%; object-fit: cover; }}
.genre-tag {{ background: var(--bg-tertiary); border: 1px solid var(--border); border-radius: 20px; padding: 0.4rem 0.8rem; display: inline-flex; align-items: center; gap: 0.4rem; cursor: pointer; margin: 0.25rem; }}
.genre-tag:hover {{ border-color: var(--accent); }}
.genre-tag .count {{ background: var(--accent); color: #000; font-size: 0.7rem; padding: 0.1rem 0.4rem; border-radius: 10px; font-weight: bold; }}
.link-card {{ display: flex; flex-direction: column; }}
.link-card .poster {{ flex: 1; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; min-height: 100px; }}
.link-card .info {{ padding: 0.6rem; text-align: center; }}
"""

    modal_js = """
    <script>
    const movieData = {};
    
    function openModal(key) {
        const modal = document.getElementById('modal-' + key);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeModal(key) {
        const modal = document.getElementById('modal-' + key);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    function toggleSeason(el) {
        el.classList.toggle('open');
        const list = el.nextElementSibling;
        if (list) list.classList.toggle('open');
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(m => {
                m.classList.remove('active');
            });
            document.body.style.overflow = '';
        }
    });
    </script>
    """

    movies_dir = OUTPUT_DIR / "movies"
    movies_dir.mkdir(exist_ok=True)

    series_dir = OUTPUT_DIR / "series"
    series_dir.mkdir(exist_ok=True)

    def make_movie_cards(items):
        return "".join(
            f"""
            <div class="card" onclick="openModal({m.get("ratingKey")})">
                <div class="poster">{get_poster_html(m.get("ratingKey"), "movie")}
                    <span class="year">{m.get("year", "-")}</span>
                </div>
                <div class="info">
                    <h3>{html_escape(m.get("title", "Unknown"))}</h3>
                    <p class="meta">⭐ {m.get("rating", "N/A")} • {m.get("duration", 0) // 60000 if m.get("duration") else 0} min</p>
                </div>
            </div>
            """
            for m in items
        )

    def make_series_cards(items):
        return "".join(
            f"""
            <div class="card" onclick="openModal({s.get("ratingKey")})">
                <div class="poster">{get_poster_html(s.get("ratingKey"), "show")}
                    <span class="year">{s.get("year", "-")}</span>
                </div>
                <div class="info">
                    <h3>{html_escape(s.get("title", "Unknown"))}</h3>
                    <p class="meta">{len(s.get("seasons", []))} {t("seasons")}</p>
                </div>
            </div>
            """
            for s in items
        )

    def make_movie_modals(items):
        return "".join(
            f"""
        <div class="modal-overlay" id="modal-{m.get("ratingKey")}" onclick="if(event.target===this)closeModal({m.get("ratingKey")})">
            <div class="modal">
                <button class="modal-close" onclick="closeModal({m.get("ratingKey")})">&times;</button>
                <div class="modal-header">
                    <div class="modal-poster">{get_large_poster_html(m.get("ratingKey"), "movie")}</div>
                    <div>
                        <h2 class="modal-title">{html_escape(m.get("title", "Unknown"))}</h2>
                        <p class="modal-meta">{m.get("year", "-")} • {m.get("duration", 0) // 60000 if m.get("duration") else 0} min</p>
                        <p class="modal-rating">{"⭐" * int(round(float(m.get("rating", 0))))}</p>
                        <div class="modal-tags">
                            {"".join(f'<span class="modal-tag">{html_escape(g)}</span>' for g in m.get("genres", []))}
                        </div>
                    </div>
                </div>
                <div class="modal-body">
                    {f'<div class="modal-section"><h3>{t("director", lang)}</h3><p>{html_escape(m.get("director", "-"))}</p></div>' if m.get("director") else ""}
                    {f'<div class="modal-section"><h3>{t("cast", lang)}</h3><p>{html_escape(m.get("cast", "-"))}</p></div>' if m.get("cast") else ""}
                    {f'<div class="modal-section"><h3>{t("summary", lang)}</h3><p>{html_escape(m.get("summary", ""))}</p></div>' if m.get("summary") else ""}
                </div>
            </div>
        </div>
        """
            for m in items
        )

    def make_series_modals(items):
        result = []
        for s in items:
            seasons_html = "".join(
                f"""
                <div class="season-toggle {
                    "open" if i == 0 else ""
                }" onclick="toggleSeason(this)">
                    <h4>{t("season", lang)} {season.get("seasonNumber", i + 1)} ({
                    len(season.get("episodes", []))
                } {t("episodes", lang)})</h4>
                    <span class="arrow">▼</span>
                </div>
                <div class="episodes-list {"open" if i == 0 else ""}">
                    {
                    "".join(
                        f'''
                    <div class="episode-item">
                        <span class="episode-num">E{ep.get('index', '')}</span>
                        <span class="episode-title">{html_escape(ep.get('title', 'Unknown'))}</span>
                        {f'<span class="episode-date"> • {ep.get("originallyAvailableAt", "")}</span>' if ep.get("originallyAvailableAt") else ''}
                    </div>
                    '''
                        for ep in season.get("episodes", [])
                    )
                }
                </div>
                """
                for i, season in enumerate(s.get("seasons", []))
            )

            result.append(f"""
        <div class="modal-overlay" id="modal-{s.get("ratingKey")}" onclick="if(event.target===this)closeModal({s.get("ratingKey")})">
            <div class="modal">
                <button class="modal-close" onclick="closeModal({s.get("ratingKey")})">&times;</button>
                <div class="modal-header">
                    <div class="modal-poster">{get_large_poster_html(s.get("ratingKey"), "show")}</div>
                    <div>
                        <h2 class="modal-title">{html_escape(s.get("title", "Unknown"))}</h2>
                        <p class="modal-meta">{s.get("year", "-")} • {len(s.get("seasons", []))} {t("seasons")}</p>
                        <div class="modal-tags">
                            {"".join(f'<span class="modal-tag">{html_escape(g)}</span>' for g in s.get("genres", []))}
                        </div>
                    </div>
                </div>
                <div class="modal-body">
                    <div class="modal-section">
                        <h3>{t("seasons", lang)} - {t("click_season", lang)}</h3>
                        {seasons_html}
                    </div>
                </div>
            </div>
        </div>
            """)
        return "".join(result)

    def make_pagination(page_num, total_pages, base_path, subdir=""):
        pages = []
        prev_disabled = page_num <= 1
        next_disabled = page_num >= total_pages

        if subdir:
            dir_path = f"{subdir}/"
        else:
            dir_path = ""

        prev_label = f"← {t('back', lang)}" if lang == "de" else f"← {t('back', lang)}"
        next_label = f"{t('next', lang)} →" if lang == "de" else f"{t('next', lang)} →"

        if page_num > 1:
            prev_class = "" if page_num > 1 else ' class="active"'
            pages.append(
                f'<a href="{dir_path}page{page_num - 1}.html">{prev_label}</a>'
            )

        for p in range(1, total_pages + 1):
            if p == page_num:
                pages.append(f'<a class="active" href="{dir_path}page{p}.html">{p}</a>')
            elif p == 1 or p == total_pages or abs(p - page_num) <= 2:
                pages.append(f'<a href="{dir_path}page{p}.html">{p}</a>')
            elif p == page_num - 3 or p == page_num + 3:
                pages.append("<span>...</span>")

        if page_num < total_pages:
            pages.append(
                f'<a href="{dir_path}page{page_num + 1}.html">{next_label}</a>'
            )

        return f"""
        <div class="pagination">
            {"".join(pages)}
        </div>"""

    index_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t("title")}</title>
    <style>{css}</style>
</head>
<body>
    <header>
        <h1>🎬 {t("title")}</h1>
        <p style="color: var(--text-muted);">Plex Media Library Export</p>
    </header>
    <nav>
        <a href="index.html" class="active">Start</a>
        <a href="movies/page1.html">{t("movies")}</a>
        <a href="series/page1.html">{t("series")}</a>
    </nav>
    <main>
        <div class="grid">
            <div class="card link-card" onclick="location.href='movies/page1.html'">
                <div class="poster">🎬</div>
                <div class="info">
                    <h3>{t("movies")}</h3>
                    <p class="meta">{len(movies)} {t("movies")}</p>
                </div>
            </div>
            <div class="card link-card" onclick="location.href='series/page1.html'">
                <div class="poster">📺</div>
                <div class="info">
                    <h3>{t("series")}</h3>
                    <p class="meta">{len(shows)} {t("series")}</p>
                </div>
            </div>
        </div>
        
        <div class="teaser-section">
            <h2>🏷️ {t("genres")}</h2>
            <div>
                {"".join(f'<div class="genre-tag"><span>{g}</span><span class="count">{c}</span></div>' for g, c in top_movie_genres)}
            </div>
        </div>
        
        <div class="teaser-section">
            <h2>📊 {t("stats")}</h2>
            <p><strong>{len(movies)}</strong> {t("movies")}</p>
            <p><strong>{len(shows)}</strong> {t("series")}</p>
            <p><strong>{total_seasons}</strong> {t("seasons")}</p>
            <p><strong>{total_episodes}</strong> {t("episodes")}</p>
            <p style="margin-top: 1rem; color: var(--text-muted); font-size: 0.8rem;">Exported: {exported_at}</p>
        </div>
    </main>
</body>
</html>"""

    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  ✓ index.html")

    if movies:
        for page_num in range(1, movie_pages + 1):
            start_idx = (page_num - 1) * MOVIES_PER_PAGE
            end_idx = start_idx + MOVIES_PER_PAGE
            page_movies = movies[start_idx:end_idx]

            page_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t("movies")} ({t("page", lang)} {page_num}/{movie_pages}) - {t("title")}</title>
    <style>{css}</style>
</head>
<body>
    <header>
        <h1>🎬 {t("movies")}</h1>
        <p style="color: var(--text-muted);">{t("page", lang)} {page_num} {t("of", lang)} {movie_pages} ({len(movies)} {t("movies")})</p>
    </header>
    <nav>
        <a href="../index.html">Start</a>
        <a href="page{page_num}.html" class="active">{t("movies")}</a>
        <a href="../series/page1.html">{t("series")}</a>
    </nav>
    <main>
        <div class="grid">
            {make_movie_cards(page_movies)}
        </div>
        {make_pagination(page_num, movie_pages, "movies")}
    </main>
    {make_movie_modals(movies)}
    {modal_js}
</body>
</html>"""

            with open(movies_dir / f"page{page_num}.html", "w", encoding="utf-8") as f:
                f.write(page_html)
        print(f"  ✓ movies/page1.html - page{movie_pages}.html ({movie_pages} pages)")

    if shows:
        for page_num in range(1, series_pages + 1):
            start_idx = (page_num - 1) * SERIES_PER_PAGE
            end_idx = start_idx + SERIES_PER_PAGE
            page_shows = shows[start_idx:end_idx]

            page_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t("series")} ({t("page", lang)} {page_num}/{series_pages}) - {t("title")}</title>
    <style>{css}</style>
</head>
<body>
    <header>
        <h1>📺 {t("series")}</h1>
        <p style="color: var(--text-muted);">{t("page", lang)} {page_num} {t("of", lang)} {series_pages} ({len(shows)} {t("series")})</p>
    </header>
    <nav>
        <a href="../index.html">Start</a>
        <a href="../movies/page1.html">{t("movies")}</a>
        <a href="page{page_num}.html" class="active">{t("series")}</a>
    </nav>
    <main>
        <div class="grid">
            {make_series_cards(page_shows)}
        </div>
        {make_pagination(page_num, series_pages, "series")}
    </main>
    {make_series_modals(shows)}
    {modal_js}
</body>
</html>"""

            with open(series_dir / f"page{page_num}.html", "w", encoding="utf-8") as f:
                f.write(page_html)
        print(f"  ✓ series/page1.html - page{series_pages}.html ({series_pages} pages)")

    return 0


# === MAIN ===


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PlexMedia2HTML Export")
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification (use with self-signed certs)",
    )
    args = parser.parse_args()

    config = check_onboarding()
    lang = config.get("language", "de")
    PLEX_URL = config["plex_url"].rstrip("/")
    PLEX_TOKEN = get_token(config)
    VERIFY_SSL = not args.insecure

    print(f"\n🎬 {_('title', lang)} Export")
    print(f"   Server: {PLEX_URL}")
    if not VERIFY_SSL:
        print(f"   ⚠️  SSL verification disabled (insecure mode)")
    print(f"   🔐 Token: securely loaded\n")

    try:
        print(f"{_('loading_movies', lang)}...")
        libraries = get_libraries(PLEX_URL, PLEX_TOKEN, VERIFY_SSL)

        movies = []
        shows = []

        for lib in libraries:
            lib_type = lib.get("type")
            lib_key = lib.get("key")

            if lib_type == "movie":
                items = get_library_items(PLEX_URL, PLEX_TOKEN, lib_key, VERIFY_SSL)
                for item in items:
                    movies.append(
                        {
                            "ratingKey": item.get("ratingKey"),
                            "title": item.get("title"),
                            "year": item.get("year"),
                            "rating": item.get("rating"),
                            "thumb": item.get("thumb"),
                            "genres": [g.get("tag") for g in item.get("Genre", [])],
                        }
                    )

            elif lib_type == "show":
                items = get_library_items(PLEX_URL, PLEX_TOKEN, lib_key, VERIFY_SSL)
                for item in items:
                    show = {
                        "ratingKey": item.get("ratingKey"),
                        "title": item.get("title"),
                        "year": item.get("year"),
                        "thumb": item.get("thumb"),
                        "genres": [g.get("tag") for g in item.get("Genre", [])],
                        "seasons": [],
                    }

                    seasons_data = get_seasons(
                        PLEX_URL, PLEX_TOKEN, item.get("ratingKey"), VERIFY_SSL
                    )
                    for season in seasons_data:
                        season_data = {
                            "seasonNumber": season.get("index"),
                            "episodes": [],
                        }
                        episodes_data = get_episodes(
                            PLEX_URL, PLEX_TOKEN, season.get("ratingKey"), VERIFY_SSL
                        )
                        for ep in episodes_data:
                            season_data["episodes"].append(
                                {
                                    "index": ep.get("index"),
                                    "title": ep.get("title"),
                                    "originallyAvailableAt": ep.get(
                                        "originallyAvailableAt", ""
                                    ),
                                }
                            )
                        show["seasons"].append(season_data)

                    shows.append(show)

        print(
            f"   ✓ {len(movies)} {_('movies', lang)}, {len(shows)} {_('series', lang)}"
        )

        if shows:
            total_seasons = sum(len(s.get("seasons", [])) for s in shows)
            total_episodes = sum(
                sum(len(season.get("episodes", [])) for season in s.get("seasons", []))
                for s in shows
            )
            print(
                f"   ✓ {total_seasons} {_('seasons', lang)}, {total_episodes} {_('episodes', lang)}"
            )

        # Download cover images
        OUTPUT_DIR = Path(config["export_path"]).expanduser()
        IMAGE_DIR = OUTPUT_DIR / "covers"
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        print(f"\n📥 Downloading cover images...")
        downloaded = 0
        failed = 0

        # Download movie covers
        for movie in movies:
            rating_key = movie.get("ratingKey")
            thumb = movie.get("thumb")
            if rating_key and thumb:
                output_path = IMAGE_DIR / f"movie-{rating_key}.jpg"
                if download_image(
                    PLEX_URL, PLEX_TOKEN, thumb, str(output_path), VERIFY_SSL
                ):
                    downloaded += 1
                else:
                    failed += 1

        # Download show covers
        for show in shows:
            rating_key = show.get("ratingKey")
            thumb = show.get("thumb")
            if rating_key and thumb:
                output_path = IMAGE_DIR / f"show-{rating_key}.jpg"
                if download_image(
                    PLEX_URL, PLEX_TOKEN, thumb, str(output_path), VERIFY_SSL
                ):
                    downloaded += 1
                else:
                    failed += 1

        print(f"  ✓ Downloaded {downloaded} images")
        if failed > 0:
            print(f"  ⚠️  {failed} failed")

        print(f"\n{_('generating_html', lang)}...")
        generate_html(config, movies, shows, lang, IMAGE_DIR)

        print(f"\n{_('export_complete', lang)}")
        print(f"   {_('open_dashboard', lang, path=config['export_path'])}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
