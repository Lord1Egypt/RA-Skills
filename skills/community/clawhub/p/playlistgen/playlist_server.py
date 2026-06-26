#!/usr/bin/env python3
"""
Music Library Indexer & Web Player
Serves on port 5678
"""
import os
import re
import json
import hashlib
import time as _time
import random
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import unquote, urlparse, parse_qs


def _load_dotenv():
    """Load .env from the script's directory into os.environ (no-op if missing)."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.isfile(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, val = line.partition('=')
            os.environ.setdefault(key.strip(), val.strip())

_load_dotenv()
import sqlite3

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

try:
    import anthropic  # type: ignore
    _anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    HAS_ANTHROPIC = True
except Exception:
    HAS_ANTHROPIC = False
    _anthropic_client = None

# MiniMax OpenAI-compatible client for interpret endpoint
try:
    import openai  # type: ignore
    _minimax_client = openai.OpenAI(
        api_key=os.environ.get("MINIMAX_API_KEY", ""),
        base_url="https://api.minimax.io/v1"
    )
    HAS_MINIMAX = bool(os.environ.get("MINIMAX_API_KEY", ""))
except Exception:
    _minimax_client = None
    HAS_MINIMAX = False

# Default interpreter provider: "claude" or "minimax"
_INTERPRET_PROVIDER = os.environ.get("MUSIC_INTERPRET_PROVIDER", "claude")


_LANG_SCRIPT = {
    'chinese':  re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]'),
    'japanese': re.compile(r'[\u3040-\u30ff\u31f0-\u31ff]'),  # kana only (unique to Japanese)
    'korean':   re.compile(r'[\uac00-\ud7af]'),
}


def _script_match(song, language):
    """Return True if song's artist/title/path contains characters of the given language script."""
    lang = language.lower()
    pat = next((v for k, v in _LANG_SCRIPT.items() if k in lang), None)
    if not pat:
        return False
    text = ' '.join(filter(None, [song.get('artist', ''), song.get('title', ''), song.get('path', '')]))
    return bool(pat.search(text))


def interpret_prompt(prompt, provider="claude"):
    """Use AI to extract structured music tags from a natural language prompt.

    Args:
        prompt: Free-form text — musical or not
        provider: "claude" (default) or "minimax"

    Returns:
        dict with keys: genres, subgenres, moods, usage_contexts, language, regions
    """
    # Use pre-built catalog vocab (populated at startup, avoids per-request DB queries)
    cat = _catalog_vocab if _catalog_vocab else {}

    catalog_section = f"""
CATALOG VOCABULARY (sorted by frequency; [LT] line = long-tail tags with count ≤ {LONG_TAIL_THRESHOLD} — niche/rare, use deliberately)
{_fmt_vocab_section('Genres',         cat.get('genres', {}),         reg_limit=0,  lt_limit=15)}
{_fmt_vocab_section('Subgenres',      cat.get('subgenres', {}),      reg_limit=60, lt_limit=20)}
{_fmt_vocab_section('Moods',          cat.get('moods', {}),          reg_limit=0,  lt_limit=20)}
{_fmt_vocab_section('Usage contexts', cat.get('usage_contexts', {}), reg_limit=25, lt_limit=20)}
{_fmt_vocab_section('Energy',         cat.get('energy', {}),         reg_limit=0,  lt_limit=0)}
{_fmt_vocab_section('Languages',      cat.get('languages', {}),      reg_limit=0,  lt_limit=0)}
{_fmt_vocab_section('Regions',        cat.get('regions', {}),        reg_limit=0,  lt_limit=0)}
{_fmt_vocab_section('Popularity',     cat.get('popularity', {}),     reg_limit=0,  lt_limit=0)}
""" if cat else ""

    interpret_rules = _music_rules.get("interpret", "") or """- genres: pick 2 values (regular tags only, no long-tail)
- subgenres: pick 3 regular tags + 1 long-tail tag
- moods: pick 2 regular tags + 1 long-tail tag
- usage_contexts: pick 2 regular tags + 1 long-tail tag
- year: [start_year, end_year] if era implied, else []
- energy: list of Energy values if energy implied, else []
- language: one Languages value if language/genre implies it, else ""
- regions: matching Regions values if geography implied, else []
- popularity_hint: infer from cues; else "any"

Always return all 9 keys. Use "", [] for empty values, never null.
Only use values verbatim from catalog vocabulary (year is a free integer range).
Return plain tag names only — no counts, no [LT] markers in the output."""

    systemPrompt = f"""You are a creative music mood interpreter. Any text — however short, mundane, or non-musical — can be translated into a musical feeling.
{catalog_section}
SELECTION RULES:
{interpret_rules}

IMPORTANT — output format: return plain tag names only (no counts, no [LT] markers).
Return JSON only with these exact keys:
{{"genres": [], "subgenres": [], "moods": [], "usage_contexts": [], "year": [], "energy": [], "language": "", "regions": [], "popularity_hint": ""}}

popularity_hint values: "mainstream", "popular", "indie", "niche", "obscure", "any"
year: [start_year, end_year] integer list, or [] if no era implied
energy: list of Energy values, or []

Examples (output uses plain tag names, chosen following the selection rules above):
- "Chinese-pop" → {{"genres": ["Pop", "Electronic"], "subgenres": ["Mandopop", "City Pop", "J-Pop", "Cantopop"], "moods": ["Upbeat", "Romantic", "Nostalgic"], "usage_contexts": ["chill", "driving", "night, nostalgia"], "year": [], "energy": [], "language": "Mandarin", "regions": ["Taiwan", "China"], "popularity_hint": "any"}}
- "obscure 80s synth" → {{"genres": ["Electronic", "Pop"], "subgenres": ["Synthpop", "New Wave", "IDM", "Electro"], "moods": ["Dark & Brooding", "Atmospheric", "Hypnotic"], "usage_contexts": ["night", "chill", "night, rainy day"], "year": [1978, 1989], "energy": ["medium", "low"], "language": "", "regions": [], "popularity_hint": "niche"}}
- "sad rainy day" → {{"genres": ["Rock", "Indie"], "subgenres": ["Dream Pop", "Shoegaze", "Indie Folk", "Slowcore"], "moods": ["Melancholic", "Dreamy", "Bittersweet"], "usage_contexts": ["chill, night", "sad", "night, rainy day"], "year": [], "energy": ["low", "medium"], "language": "", "regions": [], "popularity_hint": "any"}}
- "high energy workout" → {{"genres": ["Electronic", "Rock"], "subgenres": ["EDM", "Hard Rock", "Drum and Bass", "Metalcore"], "moods": ["Energetic", "Anthemic", "Intense"], "usage_contexts": ["workout", "gym", "running"], "year": [], "energy": ["high"], "language": "", "regions": [], "popularity_hint": "any"}}"""

    userMsg = f'Interpret this as a musical mood and extract tags: "{prompt}"'

    try:
        if provider == "claude" and HAS_ANTHROPIC:
            response = _anthropic_client.messages.create( # type: ignore
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                messages=[{"role": "user", "content": systemPrompt + "\n\n" + userMsg}]
            )
            text = response.content[0].text.strip()  # type: ignore
        elif provider == "minimax" and HAS_MINIMAX:
            response = _minimax_client.chat.completions.create( # type: ignore
                model="MiniMax-M2.7",
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user",   "content": userMsg}
                ],
                max_tokens=512,
                temperature=0.3
            )
            text = response.choices[0].message.content.strip()  # type: ignore
        else:
            return {"error": f"Provider '{provider}' not available. Set MINIMAX_API_KEY or ANTHROPIC_API_KEY."}

        # Strip <think>...</think> reasoning blocks, then parse JSON
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            result = json.loads(match.group())
            # Post-process: replace nulls with safe defaults
            result['language']       = result.get('language') or ''
            result['regions']        = result.get('regions') or []
            result['popularity_hint']= result.get('popularity_hint') or 'any'
            result['genres']         = result.get('genres') or []
            result['subgenres']      = result.get('subgenres') or []
            result['moods']          = result.get('moods') or []
            result['usage_contexts'] = result.get('usage_contexts') or []
            result['year']           = result.get('year') or []
            result['energy']         = result.get('energy') or []
            # Filter any field value not present in catalog vocab
            if cat:
                valid_moods = set(cat.get('moods', {}).keys())
                result['moods'] = [m for m in result['moods'] if m in valid_moods]
                valid_genres = set(cat.get('genres', {}).keys())
                result['genres'] = [g for g in result['genres'] if g in valid_genres]
                valid_energy = set(cat.get('energy', {}).keys())
                result['energy'] = [e for e in result['energy'] if e in valid_energy]
            return result

        # Fallback: parse plain text tag lists
        items = re.split(r'[,·\n\-–]+', text)
        tags = [t.strip().strip('•*0123456789. ").').lower() for t in items if t.strip() and len(t.strip()) > 1]
        seen = set(); deduped = []
        for t in tags:
            if t not in seen and t not in ('music tags extracted from','the user wants','here are','tags','tag','extract'):
                seen.add(t); deduped.append(t)
        if deduped:
            genre_kw   = {'rock','pop','r&b','hip-hop','electronic','jazz','blues','folk','country','metal','punk','reggae','funk','classical','world','alternative','hardcore','soul','indie','dance','trap','edm','ambient'}
            mood_kw    = {'happy','sad','chill','melancholic','upbeat','dark','brooding','energetic','dreamy','anthemic','uplifting','romantic','playful','reflective','nostalgic','sensual','fiery','intense','confident','relaxing','peaceful','浪漫','悲伤','开心','快乐','忧郁','放松','愉悦','热烈','平静','怀旧','思念'}
            context_kw = {'driving','workout','party','chill','romance','sad','nostalgia','morning','night','summer','rainy day','focus','working out','exercise','gym','running','coding','studying','relaxing','latenight','浪漫','欢快','轻松','夜深','清晨','雨天','通勤','运动','健身','派对'}
            result = {"genres": [], "subgenres": [], "moods": [], "usage_contexts": []}
            for t in deduped:
                if t in genre_kw:   result["genres"].append(t.title())
                elif t in mood_kw: result["moods"].append(t.title())
                elif t in context_kw: result["usage_contexts"].append(t)
            return result

        return {"error": "Could not parse response", "raw": text}
    except Exception as e:
        return {"error": str(e)}

_HERE      = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR  = os.environ.get("MUSIC_DIR",  "/music/").rstrip("/") + "/"
DB_PATH    = os.environ.get("DB_PATH",    os.path.join(_HERE, "music.db"))
PORT       = int(os.environ.get("PORT",   "5678"))
PUBLIC_URL = os.environ.get("MUSIC_SERVER_URL", f"http://localhost:{PORT}")
_saved_playlists = {}  # key -> {title, songs} for LLM-curated playlists

# ── Music rules (loaded from MUSIC_RULES.md at startup) ──────────────────────
_music_rules: dict = {}  # keys: "interpret", "curate"

MUSIC_RULES_PATH = os.path.join(_HERE, "MUSIC_RULES.md")

def _load_music_rules() -> dict:
    """Parse MUSIC_RULES.md and return {'interpret': str, 'curate': str}."""
    rules = {"interpret": "", "curate": ""}
    try:
        with open(MUSIC_RULES_PATH, "r") as f:
            text = f.read()
        # Split on ## headings
        sections = re.split(r'^##\s+', text, flags=re.MULTILINE)
        for sec in sections:
            lines = sec.strip().splitlines()
            if not lines:
                continue
            heading = lines[0].strip().lower()
            body = "\n".join(lines[1:]).strip()
            if "prompt interpretation" in heading:
                rules["interpret"] = body
            elif "final playlist curation" in heading:
                rules["curate"] = body
        print(f"Loaded MUSIC_RULES.md ({len(rules['interpret'])} + {len(rules['curate'])} chars)")
    except FileNotFoundError:
        print(f"MUSIC_RULES.md not found at {MUSIC_RULES_PATH} — using built-in defaults")
    except Exception as e:
        print(f"Warning: could not load MUSIC_RULES.md: {e}")
    return rules

# ── Catalog vocabulary (pre-built at startup, refreshable) ────────────────────
_catalog_vocab: dict = {}

LONG_TAIL_THRESHOLD = 2  # tags with count <= this are "long-tail"


def _build_catalog_vocab() -> dict:
    """
    Build the full catalog vocabulary (all distinct values with counts) used by
    interpret_prompt().  Called once at startup; refreshable via /api/catalog/vocab/refresh.

    Returns {field: {tag: count}} for all fields — no top-N cap.
    Mood values are individual comma-split tokens, not compound strings.
    Tags with count <= LONG_TAIL_THRESHOLD are considered long-tail.
    """
    import collections
    conn = sqlite3.connect(DB_PATH)
    try:
        def dist(col):
            return {r[0]: r[1] for r in conn.execute(
                f'SELECT {col}, COUNT(*) n FROM songs '
                f'WHERE {col} IS NOT NULL AND {col}!="" AND valid=1 '
                f'GROUP BY {col} ORDER BY n DESC').fetchall()}

        token_counts: collections.Counter = collections.Counter()
        for (mood,) in conn.execute(
                "SELECT mood FROM songs WHERE mood!='' AND valid=1").fetchall():
            for tok in mood.split(','):
                tok = tok.strip()
                if tok:
                    token_counts[tok] += 1

        return {
            'genres':         dist('genre'),
            'subgenres':      dist('subgenre'),
            'moods':          dict(token_counts.most_common()),
            'usage_contexts': dist('usage_context'),
            'languages':      dist('language'),
            'regions':        dist('region'),
            'popularity':     dist('popularity'),
        }
    finally:
        conn.close()


def _fmt_vocab_section(label: str, tag_counts: dict,
                       reg_limit: int = 0, lt_limit: int = 20) -> str:
    """Format a catalog field as two compact lines: regular tags and long-tail sample.

    reg_limit=0 means no cap on regular tags.
    lt_limit=0 suppresses the long-tail line entirely.
    """
    regular  = [t for t, c in tag_counts.items() if c > LONG_TAIL_THRESHOLD]
    if reg_limit:
        regular = regular[:reg_limit]
    longtail = [t for t, c in tag_counts.items() if c <= LONG_TAIL_THRESHOLD][:lt_limit]
    lines = [f"{label}: {', '.join(regular)}"]
    if longtail:
        lines.append(f"{label} [LT]: {', '.join(longtail)}")
    return '\n'.join(lines)


def _write_catalog_vocab_file():
    """Write music_catalog_vocab.json with tag→count format for human review."""
    conn = sqlite3.connect(DB_PATH)
    try:
        def counts(col, limit=None):
            q = (f'SELECT {col}, COUNT(*) n FROM songs WHERE {col} IS NOT NULL AND {col}!="" '
                 f'AND valid=1 GROUP BY {col} ORDER BY n DESC')
            if limit:
                q += f' LIMIT {limit}'
            return {r[0]: r[1] for r in conn.execute(q).fetchall()}

        import collections
        token_counts: collections.Counter = collections.Counter()
        for (mood,) in conn.execute("SELECT mood FROM songs WHERE mood!='' AND valid=1").fetchall():
            for tok in mood.split(','):
                tok = tok.strip()
                if tok:
                    token_counts[tok] += 1

        out = {
            'total_songs':    conn.execute('SELECT COUNT(*) FROM songs WHERE valid=1').fetchone()[0],
            'genres':         counts('genre'),
            'subgenres':      counts('subgenre'),
            'moods':          dict(token_counts.most_common()),
            'usage_contexts': counts('usage_context'),
            'languages':      counts('language'),
            'regions':        counts('region'),
            'energy':         counts('energy'),
            'popularity':     counts('popularity'),
        }
    finally:
        conn.close()

    vocab_path = os.path.join(os.path.dirname(DB_PATH), "music_catalog_vocab.json")
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


def _refresh_catalog_vocab():
    global _catalog_vocab
    _catalog_vocab = _build_catalog_vocab()
    _write_catalog_vocab_file()

def parse_path_to_metadata(filepath):
    """Extract metadata from directory structure and filename"""
    filepath = unquote(filepath)
    rel_path = filepath.replace(MUSIC_DIR, '')
    parts = rel_path.split(os.sep)
    
    metadata = {
        'artist': '',
        'album': '',
        'year': '',
        'genre': '',
        'title': '',
        'track_num': ''
    }
    
    if len(parts) >= 3:
        # Artist/Album/Track structure
        metadata['artist'] = parts[0]
        
        # Album might contain year: "1991 - Dangerous"
        album_raw = parts[1]
        if ' - ' in album_raw[:5]:
            year_part = album_raw.split(' - ')[0]
            if year_part.isdigit() and len(year_part) == 4:
                metadata['year'] = year_part
                metadata['album'] = ' - '.join(album_raw.split(' - ')[1:])
            else:
                metadata['album'] = album_raw
        else:
            metadata['album'] = album_raw
            
    if len(parts) >= 1:
        filename = parts[-1]
        # Remove extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # Try to parse track number: "01 - Song Name" or "01amulet-song"
        if ' - ' in name_without_ext:
            parts_name = name_without_ext.split(' - ', 1)
            if parts_name[0].isdigit():
                metadata['track_num'] = parts_name[0]
                metadata['title'] = parts_name[1]
            else:
                metadata['title'] = name_without_ext
        else:
            # Try to extract track number from start like "01songname"
            import re
            match = re.match(r'^(\d+)[-_]?(.*)', name_without_ext)
            if match:
                metadata['track_num'] = match.group(1)
                metadata['title'] = match.group(2).replace('_', ' ').replace('-', ' ')
            else:
                metadata['title'] = name_without_ext.replace('_', ' ').replace('-', ' ')
    
    # Clean up
    for key in metadata:
        if metadata[key]:
            metadata[key] = metadata[key].strip()
            
    return metadata

class MusicHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=MUSIC_DIR, **kwargs)
    
    def serve_wma_transcoded(self, path):
        """Transcode WMA to MP3 on-the-fly via ffmpeg (browsers can't play WMA natively)."""
        if not os.path.exists(path):
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', 'audio/mpeg')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        proc = subprocess.Popen(
            ['ffmpeg', '-i', path, '-f', 'mp3', '-b:a', '192k', '-vn', 'pipe:1'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        try:
            while True:
                chunk = proc.stdout.read(65536)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except Exception:
            pass
        finally:
            proc.terminate()
            proc.wait()

    def do_GET(self):
        # WMA files must be transcoded — browsers don't support them natively
        if self.path.lower().split('?')[0].endswith('.wma'):
            self.serve_wma_transcoded(self.translate_path(self.path))
            return

        # Check if it's a range request for audio seeking
        if self.headers.get('Range') and self.path.endswith(('.mp3', '.flac', '.wav', '.m4a', '.ogg', '.wma', '.aac')):
            self.handle_audio_range()
            return
        
        parsed = urlparse(self.path)
        path = parsed.path
        
        # API endpoints
        if path == '/api/stats':
            self.send_json_response(self.get_stats())
            return
        elif path == '/api/search':
            self.send_json_response(self.searchSongs(parsed.query))
            return
        elif path == '/api/playlist':
            self.send_json_response(self.generate_playlist(parsed.query))
            return
        elif path == '/api/catalog/summary':
            self.send_json_response(self.get_catalog_summary())
            return
        elif path == '/api/catalog/vocab':
            self.send_json_response(_catalog_vocab)
            return
        elif path == '/api/catalog/vocab/refresh':
            _refresh_catalog_vocab()
            self.send_json_response({'status': 'refreshed', 'counts': {k: len(v) for k, v in _catalog_vocab.items()}})
            return
        elif path == '/api/songs':
            self.send_json_response(self.get_songs(parsed.query))
            return
        elif path == '/api/interpret':
            self.send_json_response(self.interpret_prompt_api(parsed.query))
            return
        elif path == '/':
            self.send_html_response(self.get_index_html())
            return
        elif path == '/player':
            saved_key = parse_qs(parsed.query).get('saved', [None])[0]
            saved = None
            if saved_key:
                saved = _saved_playlists.get(saved_key)
                if not saved:
                    # Load from DB (survives server restarts)
                    conn = sqlite3.connect(DB_PATH)
                    row = conn.execute('SELECT title, songs_json FROM playlists WHERE key = ? LIMIT 1',
                                       (saved_key,)).fetchone()
                    conn.close()
                    if row:
                        saved = {'title': row[0], 'songs': json.loads(row[1])}
                        _saved_playlists[saved_key] = saved
            self.send_html_response(self.get_player_html(saved))
            return
        
        # Serve music files
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        if parsed.path == '/api/playlist/save':
            self.send_json_response(self.save_playlist(body))
        elif parsed.path == '/api/curate':
            self.send_json_response(self.curate_songs(body))
        elif parsed.path == '/api/generate':
            self.send_json_response(self.generate_full(body))
        else:
            self.send_error(404)

    def handle_audio_range(self):
        """Handle Range requests for seeking in audio files"""
        path = self.translate_path(self.path)
        if not os.path.exists(path):
            self.send_error(404)
            return
        
        file_size = os.path.getsize(path)
        range_header = self.headers.get('Range')
        
        # Parse Range header (e.g., "bytes=1024-")
        if isinstance(range_header, str):
            range_spec = range_header.replace('bytes=', '')
            if '-' in range_spec:
                start, end = range_spec.split('-')
                start = int(start) if start else 0
                end = file_size - 1 if not end else int(end)
            else:
                start, end = map(int, range_spec.split('-'))
        else:
            start, end = 0, file_size - 1
        
        content_length = end - start + 1
        
        with open(path, 'rb') as f:
            f.seek(start)
            data = f.read(content_length)
        
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        mime = {'mp3': 'audio/mpeg', 'flac': 'audio/flac', 'ogg': 'audio/ogg',
                'wav': 'audio/wav', 'm4a': 'audio/mp4', 'aac': 'audio/aac',
                'wma': 'audio/x-ms-wma'}.get(ext, 'audio/mpeg')
        self.send_response(206)  # Partial Content
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(content_length))
        self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)
    
    def get_stats(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM songs')
        total = c.fetchone()[0]
        c.execute('SELECT artist, COUNT(*) as cnt FROM songs GROUP BY artist ORDER BY cnt DESC LIMIT 20')
        top_artists = [{'artist': r[0], 'count': r[1]} for r in c.fetchall()]
        c.execute('SELECT album, artist, COUNT(*) as cnt FROM songs GROUP BY album, artist ORDER BY cnt DESC LIMIT 10')
        top_albums = [{'album': r[0], 'artist': r[1], 'count': r[2]} for r in c.fetchall()]
        conn.close()
        return {'total': total, 'top_artists': top_artists, 'top_albums': top_albums}
    
    def searchSongs(self, query):
        params = parse_qs(query)
        q = params.get('q', [''])[0]
        artist = params.get('artist', [''])[0]
        album = params.get('album', [''])[0]
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        sel = 'SELECT path, filename, artist, album, year, title, genre, subgenre, mood, usage_context, energy, duration, language, region, popularity FROM songs'
        if q:
            search = f'%{q}%'
            c.execute(sel + ' WHERE (title LIKE ? OR artist LIKE ? OR album LIKE ?) AND valid=1 LIMIT 50',
                      (search, search, search))
        elif artist:
            c.execute(sel + ' WHERE artist = ? AND valid=1 LIMIT 50', (artist,))
        elif album:
            c.execute(sel + ' WHERE album = ? AND valid=1 LIMIT 50', (album,))
        else:
            c.execute(sel + ' WHERE valid=1 LIMIT 50')

        results = []
        for r in c.fetchall():
            abs_path = r[0]
            results.append({
                'path': abs_path,
                'url':  abs_path[len(MUSIC_DIR):] if abs_path.startswith(MUSIC_DIR) else abs_path.lstrip('/'),
                'filename': r[1], 'artist': r[2], 'album': r[3], 'year': r[4],
                'title': r[5] or r[1], 'genre': r[6], 'subgenre': r[7],
                'mood': r[8], 'usage_context': r[9],
                'energy': r[10], 'duration': r[11],
                'language': r[12] or '', 'region': r[13] or '', 'popularity': r[14] or '',
            })
        conn.close()
        return results
    
    def generate_playlist(self, query):
        """Generate playlist from prompt using keyword scoring across all fields.
        
        Params: q, mood, save (if 'save=true', auto-saves and returns saved_url)
        """
        params = parse_qs(query)
        q = params.get('q', [''])[0]
        mood = params.get('mood', [''])[0]
        do_save = params.get('save', ['false'])[0].lower() == 'true'

        # Mood → genre/keyword expansion
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        scores = {}  # path -> [score, row]

        # --- Semantic path: use AI to interpret the prompt ---
        tags = interpret_prompt(q) if q else None

        if tags:
            # Weight: usage_context > mood > subgenre > genre (most specific to least)
            field_weights = [
                ('usage_context', 3, tags.get('usage_contexts', [])),
                ('mood',          2, tags.get('moods', [])),
                ('subgenre',      2, tags.get('subgenres', [])),
                ('genre',         1, tags.get('genres', [])),
            ]
            for field, weight, values in field_weights:
                for val in values:
                    search = f'%{val}%'
                    c.execute(f'''SELECT path, filename, artist, album, year, title, genre, subgenre, mood, usage_context, energy, duration, language, region, popularity
                                  FROM songs WHERE {field} LIKE ? AND valid=1''', (search,))
                    for row in c.fetchall():
                        path = row[0]
                        if path not in scores:
                            scores[path] = [0, row]
                        scores[path][0] += weight

        # --- Fallback: keyword matching if no AI results ---
        if not scores:
            stop_words = {'a', 'an', 'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on',
                          'with', 'some', 'me', 'my', 'i', 'is', 'it', 'that', 'this',
                          'want', 'like', 'give', 'make', 'create', 'generate', 'playlist',
                          'music', 'songs', 'something'}
            keywords = [mood] if mood else []
            if q:
                keywords += [w.lower().strip('.,!?') for w in q.split() if w.lower() not in stop_words]
            if not keywords:
                keywords = ['']
            for kw in keywords:
                search = f'%{kw}%'
                c.execute('''SELECT path, filename, artist, album, year, title, genre, subgenre, mood, usage_context, energy, duration, language, region, popularity
                             FROM songs
                             WHERE (title LIKE ? OR artist LIKE ? OR album LIKE ?
                                OR genre LIKE ? OR mood LIKE ? OR usage_context LIKE ?) AND valid=1''',
                          (search,) * 6)
                for row in c.fetchall():
                    path = row[0]
                    if path not in scores:
                        scores[path] = [0, row]
                    scores[path][0] += 1

        conn.close()

        ranked = sorted(scores.values(), key=lambda x: x[0], reverse=True)[:30]
        results = []
        for _sc, s in ranked:
            p = s[0]
            results.append({
                'path': p,
                'url':  p[len(MUSIC_DIR):] if p.startswith(MUSIC_DIR) else p.lstrip('/'),
                'filename': s[1], 'artist': s[2], 'album': s[3], 'year': s[4],
                'title': s[5] or s[1], 'genre': s[6], 'subgenre': s[7],
                'mood': s[8], 'usage_context': s[9],
                'energy': s[10], 'duration': s[11],
                'language': s[12] or '', 'region': s[13] or '', 'popularity': s[14] or '',
            })

        response = {'songs': results, 'query': q, 'mood': mood}

        # Auto-save if requested
        if do_save and results:
            save_result = self.save_playlist({
                'title': q or mood or 'Playlist',
                'songs': [s['path'] for s in results]
            })
            if 'url' in save_result:
                response['saved_url'] = save_result['url']
                response['saved_key'] = save_result['url'].split('saved=')[-1]

        return response
    
    def get_catalog_summary(self):
        """Return catalog distributions so an LLM agent can understand what's available."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        def dist(col):
            c.execute(f'SELECT {col}, COUNT(*) as n FROM songs WHERE {col} IS NOT NULL AND {col} != "" GROUP BY {col} ORDER BY n DESC')
            return [{'value': r[0], 'count': r[1]} for r in c.fetchall()]
        result = {
            'total_songs':    c.execute('SELECT COUNT(*) FROM songs WHERE valid=1').fetchone()[0],
            'enriched_songs': c.execute("SELECT COUNT(*) FROM songs WHERE valid=1 AND mood!='' AND subgenre!=''").fetchone()[0],
            'genres':         dist('genre'),
            'subgenres':      dist('subgenre'),
            'moods':          dist('mood'),
            'usage_contexts': dist('usage_context'),
            'energy':         dist('energy'),
            'languages':      dist('language'),
            'regions':        dist('region'),
            'popularity':     dist('popularity'),
        }
        conn.close()
        return result

    def get_songs(self, query):
        """Fetch candidate songs by structured filters. Designed for LLM agent use.
        Params: genre, subgenre, mood, usage_context, artist, limit (default 100)
        All params are substring-matched. Multiple values comma-separated.
        
        New params (v2):
        - mode: "or" (default, any match), "and" (all must match), "weighted" (score by match count)
        - artist_limit: max songs per artist (default 5, 0 = unlimited)
        """
        params = parse_qs(query)
        limit = int(params.get('limit', ['300'])[0])
        mode = params.get('mode', ['or'])[0]
        artist_limit = int(params.get('artist_limit', ['5'])[0])
        language = params.get('language', [''])[0].strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        conditions = []
        args = []
        for field in ('genre', 'subgenre', 'mood', 'usage_context', 'artist'):
            values = params.get(field, [])
            if values:
                for val in values[0].split(','):
                    val = val.strip()
                    if val:
                        conditions.append(f'{field} LIKE ?')
                        args.append(f'%{val}%')

        where = f'WHERE ({" OR ".join(conditions)}) AND valid=1' if conditions else 'WHERE valid=1'

        def _fetch_rows(cursor, where_clause, args):
            cursor.execute(f'''SELECT path, filename, artist, album, year, title, genre, subgenre,
                                      mood, usage_context, energy, duration, language, region, popularity
                              FROM songs {where_clause}''', args)
            result = []
            for s in cursor.fetchall():
                p = s[0]
                result.append({
                    'path': p,
                    'url':  p[len(MUSIC_DIR):] if p.startswith(MUSIC_DIR) else p.lstrip('/'),
                    'filename': s[1], 'artist': s[2], 'album': s[3], 'year': s[4],
                    'title': s[5] or s[1], 'genre': s[6], 'subgenre': s[7],
                    'mood': s[8], 'usage_context': s[9],
                    'energy': s[10], 'duration': s[11],
                    'language': s[12] or '', 'region': s[13] or '', 'popularity': s[14] or '',
                })
            return result

        all_songs = _fetch_rows(c, where, args)

        # ── Language filter ────────────────────────────────────────────────────
        # Priority: DB language column (exact/substring) → script detection fallback
        if language and language.lower() not in ('any', ''):
            lang_lower = language.lower()
            # 1. Match by DB language column
            db_matched = [s for s in all_songs if lang_lower in (s.get('language') or '').lower()]
            # 2. Fallback: script-based detection for CJK languages
            if len(db_matched) < 30 and lang_lower in ('chinese', 'mandarin', 'cantonese', 'japanese', 'korean'):
                script_matched = [s for s in all_songs if _script_match(s, language)]
                seen = {s['path'] for s in db_matched}
                for s in script_matched:
                    if s['path'] not in seen:
                        db_matched.append(s)
                        seen.add(s['path'])
            # 3. If still sparse, scan full library by DB column
            if len(db_matched) < 30:
                extra = _fetch_rows(c, 'WHERE valid=1', [])
                seen = {s['path'] for s in db_matched}
                for s in extra:
                    if s['path'] not in seen and lang_lower in (s.get('language') or '').lower():
                        db_matched.append(s)
                        seen.add(s['path'])
                # CJK script fallback on full library
                if len(db_matched) < 30 and lang_lower in ('chinese', 'mandarin', 'cantonese', 'japanese', 'korean'):
                    for s in extra:
                        if s['path'] not in seen and _script_match(s, language):
                            db_matched.append(s)
                            seen.add(s['path'])
            all_songs = db_matched

        # Region and popularity are NOT filtered here — they are soft hints
        # passed to curate_songs() (Step 3) so the LLM can apply them flexibly.

        conn.close()

        # Score and filter
        scored = []
        for song in all_songs:
            # Count how many conditions this song matches
            score = 0
            for field in ('genre', 'subgenre', 'mood', 'usage_context'):
                val = song.get(field, '') or ''
                for arg in args:
                    if arg.lower() in val.lower():
                        score += 1
                        break
            
            if mode == 'and':
                # Only include songs matching ALL conditions
                expected_conditions = len(conditions)
                if score < expected_conditions:
                    continue
                score = 1000  # All same rank for AND mode
            elif mode == 'or':
                score = 1  # All OR matches equally ranked
            # else weighted mode: score = number of matched conditions
            
            scored.append((score, song))
        
        # Sort by score descending, then shuffle within score groups to break ties fairly
        scored.sort(key=lambda x: x[0], reverse=True)
        # Shuffle within each score group
        score_groups = {}
        for score, song in scored:
            score_groups.setdefault(score, []).append((score, song))
        for score in sorted(score_groups.keys(), reverse=True):
            random.shuffle(score_groups[score])
        shuffled = []
        for score in sorted(score_groups.keys(), reverse=True):
            shuffled.extend(score_groups[score])
        scored = shuffled
        
        # Apply artist limit
        artist_counts = {}
        final_songs = []
        for score, song in scored:
            artist = song.get('artist', '')
            if artist_limit > 0:
                artist_counts[artist] = artist_counts.get(artist, 0) + 1
                if artist_counts[artist] > artist_limit:
                    continue
            final_songs.append(song)
            if len(final_songs) >= limit:
                break
        
        return {'songs': final_songs, 'count': len(final_songs), 'mode': mode, 'artist_limit': artist_limit}

    def interpret_prompt_api(self, query):
        """AI-powered conversion of free-form text to structured music tags.
        
        GET /api/interpret?q=<prompt>&provider=claude|minimax

        Returns: {genres, subgenres, moods, usage_contexts, provider, prompt}
        """
        params = parse_qs(query)
        prompt = params.get('q', [''])[0]
        provider = params.get('provider', [_INTERPRET_PROVIDER])[0]
        
        if not prompt:
            return {'error': 'Missing required param: q'}
        
        result = interpret_prompt(prompt, provider=provider)
        result['prompt'] = prompt
        result['provider'] = provider
        return result

    def curate_songs(self, body):
        """LLM-powered curation of a song list for diversity and long-tail variety.
        Body: {
            "songs": [{"id": "...", "artist": "...", "title": "...", "genre": "...", "mood": "..."}],
            "prompt": "...",   # optional playlist request text
            "max_count": 30
        }
        Returns: {"curated": ["/path/to/song1", ...]}
        """
        songs            = body.get('songs', [])
        prompt           = body.get('prompt', '')
        language         = body.get('language', '')
        popularity_hint  = body.get('popularity_hint', 'any')
        regions          = body.get('regions', [])   # soft hint from interpret
        max_count        = min(body.get('max_count', 30), 50)

        if not songs:
            return {'error': 'No songs provided'}
        if len(songs) <= max_count:
            return {'curated': [s.get('id') or s.get('path', '') for s in songs]}

        # Diversity-preserving sample: 150 candidates for the LLM
        sampled = self._diversity_sample(songs, max(150, max_count * 5))

        song_list = '\n'.join(
            f'{i+1}. [{s.get("genre","")}/{s.get("subgenre","")}/{s.get("language","")}/{s.get("region","")}/{s.get("popularity","")}/{s.get("mood","")}] '
            f'{s.get("artist","")} — {s.get("title","")}'
            for i, s in enumerate(sampled)
        )

        lang_rule = f"\n- HARD REQUIREMENT: Select ONLY songs in {language} language (judge by the language field, artist name, and song title)" if language and language.lower() not in ('any', 'english', '') else ""

        popularity_rule = ""
        if popularity_hint and popularity_hint.lower() not in ('any', ''):
            if popularity_hint.lower() in ('niche', 'obscure'):
                popularity_rule = "\n- STRONGLY PREFER songs with popularity 'niche' or 'obscure' — avoid 'mainstream' tracks"
            elif popularity_hint.lower() == 'indie':
                popularity_rule = "\n- PREFER songs with popularity 'indie' or 'niche' — avoid 'mainstream' tracks"
            elif popularity_hint.lower() in ('mainstream', 'popular'):
                popularity_rule = f"\n- PREFER songs with popularity '{popularity_hint}'"

        region_rule = ""
        if regions:
            region_list = ", ".join(regions)
            region_rule = f"\n- PREFER songs from these regions: {region_list} — include others for diversity"

        curate_rules_template = _music_rules.get("curate", "") or """- Select between {min_count} and {max_count} tracks
- HARD LIMIT: Never select more than 2 tracks from the same artist
- Maintain genre consistency (or subgenre consistency if the playlist targets a specific subgenre)
- Maximize artist diversity — avoid clustering the same artist back-to-back                                                             
- If the prompt implies a specific era (decade or period), prefer songs whose year falls in that range; otherwise spread across eras for variety                                                                                                                                
- If the prompt implies a specific region or culture, prefer songs from that region; otherwise spread across regions for variety        
- If the prompt implies a popularity level (e.g. "obscure", "hits"), apply it as a strong preference; otherwise mix mainstream and niche tracks for variety                                                                                                                     
- Order for smooth energy and mood transitions"""
        curate_rules = curate_rules_template.replace("{min_count}", str(max_count // 2)).replace("{max_count}", str(max_count))

        system_msg = f"""You are an expert music curator. Given a playlist request and candidate songs, select and order tracks for a cohesive, diverse playlist.

Each song is listed as: [genre/subgenre/language/region/popularity/mood] Artist — Title

Rules:
{curate_rules}{lang_rule}{popularity_rule}{region_rule}

Output ONLY this JSON object, nothing else:
{{"track_order": [3, 17, 8, 22, ...]}}
Positions are 1-indexed from the candidate list above."""

        user_msg = f'Playlist request: {prompt or "Make a great diverse playlist"}\n\nCandidate songs:\n{song_list}'

        if not HAS_ANTHROPIC and not HAS_MINIMAX:
            return {'error': 'No API key set (ANTHROPIC_API_KEY or MINIMAX_API_KEY)'}

        try:
            if HAS_ANTHROPIC:
                resp = _anthropic_client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": system_msg + "\n\n" + user_msg}]
                )
                raw = resp.content[0].text.strip()
            else:
                resp = _minimax_client.chat.completions.create(
                    model='MiniMax-M2.7',
                    messages=[
                        {'role': 'system', 'content': system_msg},
                        {'role': 'user',   'content': user_msg}
                    ],
                    max_tokens=2048,
                    temperature=0.2
                )
                raw = resp.choices[0].message.content.strip()
                # Strip <think>...</think> reasoning blocks before parsing
                raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()

            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not match:
                return {'error': 'Could not parse LLM response', 'raw': raw[:200]}

            data = json.loads(match.group())
            indices = data.get('track_order', [])

            curated = []
            seen = set()
            for idx in indices:
                song = sampled[idx - 1]  # 1-indexed
                path = song.get('id') or song.get('path', '')
                if path and path not in seen:
                    seen.add(path)
                    curated.append(path)
                if len(curated) >= max_count:
                    break

            if not curated:
                # Fallback: return first N from diversity sample
                curated = [s.get('id') or s.get('path', '') for s in sampled[:max_count]]

            return {'curated': curated, 'count': len(curated)}

        except Exception as e:
            return {'error': str(e)}

    def _diversity_sample(self, songs, target):
        """Sample songs to maximize artist, region, and popularity spread.

        Strategy: round-robin by artist first, then by region within each round,
        so the LLM candidate pool spans multiple regions and popularity tiers.
        """
        by_artist = {}
        for s in songs:
            by_artist.setdefault(s.get('artist', '') or 'Unknown', []).append(s)

        # Sort artists so that less-represented regions appear early
        region_counts = {}
        for s in songs:
            region_counts[s.get('region', '') or 'Unknown'] = region_counts.get(s.get('region', '') or 'Unknown', 0) + 1
        # Artists ordered by their region's frequency (rarer regions first)
        artists = sorted(by_artist.keys(), key=lambda a: region_counts.get(by_artist[a][0].get('region', '') or 'Unknown', 0))

        selected = []
        seen_paths = set()
        pos_map = {a: 0 for a in artists}

        round_ = 0
        while len(selected) < target and round_ < len(songs):
            for artist in artists:
                if len(selected) >= target:
                    break
                artist_songs = by_artist[artist]
                pos = (round_ + pos_map[artist]) % len(artist_songs)
                song = artist_songs[pos]
                path = song.get('id') or song.get('path', '')
                if path and path not in seen_paths:
                    selected.append(song)
                    seen_paths.add(path)
                    pos_map[artist] = (pos_map[artist] + 1) % len(artist_songs)
            round_ += 1

        # Fill remainder in original order
        if len(selected) < target:
            for s in songs:
                path = s.get('id') or s.get('path', '')
                if path and path not in seen_paths:
                    selected.append(s)
                    seen_paths.add(path)
                if len(selected) >= target:
                    break

        return selected

    def generate_full(self, body):
        """Full LLM-native workflow: interpret → fetch → curate → save.
        Body: {"prompt": "...", "max_count": 30}
        Returns: {"title": "...", "url": "...", "count": N, "tags": {...}}
        """
        from urllib.parse import urlencode

        prompt    = body.get('prompt', '').strip()
        max_count = min(body.get('max_count', 30), 50)

        if not prompt:
            return {'error': 'prompt is required'}

        # Step 1: Interpret
        tags = interpret_prompt(prompt)
        if 'error' in tags:
            return {'error': f"interpret failed: {tags['error']}"}

        genres          = tags.get('genres', [])
        subgenres       = tags.get('subgenres', [])
        moods           = tags.get('moods', [])
        usage_contexts  = tags.get('usage_contexts', [])
        language        = (tags.get('language', '') or '').strip()
        regions         = tags.get('regions', []) or []
        popularity_hint = tags.get('popularity_hint', '') or ''
        if language.lower() == 'any':
            language = ''
        if popularity_hint.lower() == 'any':
            popularity_hint = ''

        # Step 2: Fetch candidates — language is hard filter; region/popularity → Step 3
        def _fetch(genres=None, subgenres=None, moods=None, usage_contexts=None, language=None):
            p = {'limit': '300'}
            if genres:         p['genre']         = ','.join(genres)
            if subgenres:      p['subgenre']      = ','.join(subgenres)
            if moods:          p['mood']          = ','.join(moods)
            if usage_contexts: p['usage_context'] = ','.join(usage_contexts)
            if language:       p['language']      = language
            return self.get_songs(urlencode(p)).get('songs', [])

        songs = _fetch(genres=genres or None, subgenres=subgenres or None,
                       moods=moods or None, usage_contexts=usage_contexts or None,
                       language=language or None)
        if not songs:
            # Fallback 1: drop mood
            songs = _fetch(genres=genres or None, subgenres=subgenres or None,
                           usage_contexts=usage_contexts or None, language=language or None)
        if not songs and language:
            # Fallback 2: language only
            songs = _fetch(language=language)
        if not songs:
            return {'error': 'No songs found matching those tags.'}

        # Step 3: Curate
        curate_result = self.curate_songs({
            'songs':           songs,
            'prompt':          prompt,
            'max_count':       max_count,
            'language':        language,
            'popularity_hint': popularity_hint,
            'regions':         regions,
        })
        if 'error' in curate_result:
            return {'error': curate_result['error']}

        # Step 4: Save
        title       = f"🎵 {prompt.strip().title()}"
        save_result = self.save_playlist({'title': title, 'songs': curate_result.get('curated', [])})
        return {
            'title': title,
            'url':   save_result.get('url', ''),
            'count': save_result.get('count', 0),
            'tags':  tags,
        }

    def save_playlist(self, body):
        """Accept a curated list of song IDs from the LLM agent, return a player URL.
        Body: { "title": "...", "songs": ["path1", "path2", ...] }"""
        import hashlib, time as _time
        songs_ids = body.get('songs', [])
        title = body.get('title', 'Playlist')
        if not songs_ids:
            return {'error': 'No songs provided'}

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Ensure playlists table exists
        c.execute('''CREATE TABLE IF NOT EXISTS playlists (
            key TEXT PRIMARY KEY,
            title TEXT,
            songs_json TEXT,
            created_at INTEGER
        )''')

        resolved = []
        for sid in songs_ids:
            c.execute('SELECT path, filename, artist, album, year, title, genre, subgenre, mood, usage_context, energy, duration, language, region, popularity FROM songs WHERE path = ?', (sid,))
            row = c.fetchone()
            if row:
                p = row[0]
                resolved.append({
                    'path': p,
                    'url':  p[len(MUSIC_DIR):] if p.startswith(MUSIC_DIR) else p.lstrip('/'),
                    'filename': row[1], 'artist': row[2], 'album': row[3], 'year': row[4],
                    'title': row[5] or row[1], 'genre': row[6], 'subgenre': row[7],
                    'mood': row[8], 'usage_context': row[9],
                    'energy': row[10], 'duration': row[11],
                    'language': row[12] or '', 'region': row[13] or '', 'popularity': row[14] or '',
                })

        key = hashlib.md5((''.join(songs_ids) + str(_time.time())).encode()).hexdigest()[:8]
        c.execute('INSERT OR REPLACE INTO playlists (key, title, songs_json, created_at) VALUES (?, ?, ?, ?)',
                  (key, title, json.dumps(resolved, ensure_ascii=False), int(_time.time())))
        conn.commit()
        conn.close()

        _saved_playlists[key] = {'title': title, 'songs': resolved}
        return {
            'url': f'{PUBLIC_URL}/player?saved={key}',
            'title': title,
            'count': len(resolved),
        }

    def send_json_response(self, data):
        response = json.dumps(data, ensure_ascii=False)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def send_html_response(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def get_index_html(self):
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Music Library</title>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #00d4ff; }
        .stats { background: #16213e; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .search-box { width: 100%; padding: 15px; font-size: 18px; border-radius: 8px; border: none; background: #0f3460; color: #fff; }
        .results { margin-top: 20px; }
        .song { background: #16213e; padding: 15px; margin: 10px 0; border-radius: 8px; cursor: pointer; }
        .song:hover { background: #1f4068; }
        .song-title { font-weight: bold; color: #00d4ff; }
        .song-artist { color: #aaa; }
        .player-link { display: inline-block; background: #e94560; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🎵 Music Library</h1>
    <div class="stats" id="stats">Loading...</div>
    <input type="text" class="search-box" id="search" placeholder="Search songs, artists, albums..." onkeyup="search(this.value)">
    <div class="results" id="results"></div>
    <script>
        async function loadStats() {
            const r = await fetch('/api/stats');
            const d = await r.json();
            document.getElementById('stats').innerHTML = '<h2>' + d.total + ' songs</h2><p>Top artists: ' + 
                d.top_artists.slice(0,5).map(a => a.artist).join(', ') + '</p>';
        }
        async function search(q) {
            if (q.length < 2) return;
            const r = await fetch('/api/search?q=' + encodeURIComponent(q));
            const songs = await r.json();
            document.getElementById('results').innerHTML = songs.map(s =>
                '<div class="song" onclick="play(\\'' + s.url + '\\')"><span class="song-title">' + s.title +
                '</span><br><span class="song-artist">' + s.artist + ' - ' + s.album + '</span></div>'
            ).join('');
        }
        function play(url) {
            window.open('/player?file=' + encodeURIComponent(url), '_blank');
        }
        loadStats();
    </script>
</body>
</html>'''
    
    def get_player_html(self, saved=None):
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Music Player</title>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #00d4ff; text-align: center; }
        .now-playing { background: #16213e; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .song-title { font-size: 22px; color: #00d4ff; margin-bottom: 5px; }
        .song-artist { font-size: 16px; color: #aaa; }
        audio { width: 100%; margin: 20px 0; }
        .playlist { margin-top: 20px; }
        .playlist h2 { color: #e94560; }
        .song { background: #16213e; padding: 12px; margin: 8px 0; border-radius: 8px; cursor: pointer; }
        .song:hover { background: #1f4068; }
        .song.playing { border: 2px solid #00d4ff; }
        .song-info { font-size: 14px; color: #888; }
        .shuffle-btn { background: #e94560; color: white; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; margin-left: 12px; vertical-align: middle; }
        .shuffle-btn:hover { background: #c73652; }
        .shuffle-btn.active { background: #00d4ff; color: #1a1a2e; }
    </style>
</head>
<body>
    <h1>🎧 Music Player</h1>
    <div class="now-playing">
        <div class="song-title" id="title">Select a song</div>
        <div class="song-artist" id="artist"></div>
    </div>
    <audio id="audio" controls></audio>
    <div class="playlist" id="playlist"></div>
    <script>
        let playlist = [];
        let currentIndex = -1;
        let shuffled = false;
        const params = new URLSearchParams(window.location.search);
        const file = params.get('file');
        const audio = document.getElementById('audio');
        const _savedData = ''' + (json.dumps(saved) if saved else 'null') + ''';

        function getBaseUrl() {
            return window.location.protocol + '//' + window.location.host;
        }

        if (file) {
            audio.src = getBaseUrl() + '/' + file;
            audio.play();
            const name = file.split('/').pop().replace(/^\\\\d+[-_]?/, '').replace(/\\\\.[^.]+$/, '');
            document.getElementById('title').textContent = name;
        }

        function renderPlaylist(label) {
            const container = document.getElementById('playlist');
            const header = '<h2>Playlist: ' + label + ' (' + playlist.length + ' songs)' +
                '<button class="shuffle-btn' + (shuffled ? ' active' : '') + '" onclick="toggleShuffle()">&#x1F500; Shuffle' + (shuffled ? ' ON' : '') + '</button></h2>';
            const items = playlist.map((s, i) =>
                '<div class="song" id="song-' + i + '" onclick="playSong(' + i + ', this)">' +
                '<strong>' + (i+1) + '. ' + s.title + '</strong>' +
                '<div class="song-info">' + s.artist + ' - ' + s.album + '</div></div>'
            ).join('');
            container.innerHTML = header + items;
        }

        function toggleShuffle() {
            shuffled = !shuffled;
            if (shuffled) {
                for (let i = playlist.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [playlist[i], playlist[j]] = [playlist[j], playlist[i]];
                }
            } else {
                playlist.sort((a, b) => (b._score || 0) - (a._score || 0));
            }
            currentIndex = -1;
            renderPlaylist(currentLabel);
            playSong(0, document.getElementById('song-0'));
        }

        let currentLabel = '';

        async function loadPlaylist() {
            const pl = params.get('playlist');
            if (pl) {
                const r = await fetch('/api/playlist?q=' + encodeURIComponent(pl));
                const data = await r.json();
                if (data.songs && data.songs.length > 0) {
                    playlist = data.songs.map((s, i) => ({ ...s, _score: data.songs.length - i }));
                    currentLabel = data.query || pl;
                    renderPlaylist(currentLabel);
                    if (!file) {
                        playSong(0, document.querySelector('.song'));
                    }
                }
            }
        }

        function playSong(index, el) {
            currentIndex = index;
            const s = playlist[index];
            document.querySelectorAll('.song').forEach(song => song.classList.remove('playing'));
            if (el) el.classList.add('playing');
            audio.src = getBaseUrl() + '/' + (s.url || s.path);
            document.getElementById('title').textContent = s.title;
            document.getElementById('artist').textContent = s.artist + ' - ' + s.album;
            audio.play();
        }

        // Auto-play next
        audio.addEventListener('ended', () => {
            if (currentIndex < playlist.length - 1) {
                playSong(currentIndex + 1, document.getElementById('song-' + (currentIndex + 1)));
            }
        });

        loadPlaylist();

        // Load saved playlist (must run after all functions are defined)
        if (_savedData) {
            playlist = _savedData.songs.map((s, i) => ({ ...s, _score: _savedData.songs.length - i }));
            currentLabel = _savedData.title;
            renderPlaylist(currentLabel);
            if (!file) playSong(0, document.querySelector('.song'));
        }
    </script>
</body>
</html>'''

def start_server():
    global _catalog_vocab, _music_rules
    _music_rules = _load_music_rules()
    conn = sqlite3.connect(DB_PATH)
    total    = conn.execute("SELECT COUNT(*) FROM songs WHERE valid=1").fetchone()[0]
    enriched = conn.execute("SELECT COUNT(*) FROM songs WHERE valid=1 AND mood!='' AND subgenre!=''").fetchone()[0]
    conn.close()

    print("Building catalog vocabulary…", end=" ", flush=True)
    _catalog_vocab = _build_catalog_vocab()
    _write_catalog_vocab_file()
    print(f"done ({len(_catalog_vocab['genres'])} genres, {len(_catalog_vocab['subgenres'])} subgenres, "
          f"{len(_catalog_vocab['moods'])} mood tokens, {len(_catalog_vocab['languages'])} languages, "
          f"{len(_catalog_vocab['regions'])} regions)")

    print(f"Music server — {total:,} songs ({enriched:,} LLM-enriched) | http://localhost:{PORT}")
    print(f"Music dir: {MUSIC_DIR}")
    server = ThreadingHTTPServer(('0.0.0.0', PORT), MusicHandler)
    print("Press Ctrl+C to stop")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
