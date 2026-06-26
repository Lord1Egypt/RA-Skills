#!/usr/bin/env python3
"""
Smart Music Indexer
Scans a directory for audio files, extracts metadata via ffprobe,
uses an LLM to infer/verify/enrich all fields, and saves to SQLite.

Supported LLM services:
  haiku     claude-haiku-4-5-20251001  (default, override with --model)
  minimax   MiniMax-M2.7

Usage:
    python3 smart_indexer.py --path /media/Music --llm haiku   --key YOUR_KEY
    python3 smart_indexer.py --path /media/Music --llm minimax --key YOUR_KEY
    python3 smart_indexer.py --path /media/Music --llm haiku   --key YOUR_KEY --db music.db --batch 40
    python3 smart_indexer.py --path /media/Music --llm haiku   --key YOUR_KEY --force
    python3 smart_indexer.py --path /media/Music --llm haiku   --key YOUR_KEY --dry-run
"""

import os
import sys
import json
import time
import re
import random
import sqlite3
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


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

# ── Audio formats ──────────────────────────────────────────────────────────────
AUDIO_EXTENSIONS = {'.mp3', '.flac', '.wav', '.m4a', '.ogg', '.wma', '.aac', '.opus', '.ape', '.alac'}

# ── LLM endpoints ──────────────────────────────────────────────────────────────
LLM_CONFIGS = {
    'haiku': {
        'url': 'https://api.anthropic.com/v1/messages',
        'default_model': 'claude-haiku-4-5-20251001',
    },
    'minimax': {
        'url': 'https://api.minimaxi.chat/v1/chat/completions',
        'default_model': 'MiniMax-M2.7',
    },
}

GENRE_LIST = [
    "Rock", "Pop", "R&B", "Hip-Hop", "Electronic", "Jazz", "Blues", "Folk",
    "Country", "Metal", "Punk", "Reggae", "Funk", "Classical", "World",
    "Alternative", "Hardcore", "Soul", "Ambient", "Indie"
]
MOOD_LIST = [
    "Energetic", "Upbeat", "Dark & Brooding", "Melancholic", "Chill & Dreamy",
    "Anthemic", "Aggressive", "Romantic", "Atmospheric", "Psychedelic",
    "Soulful", "Groovy", "Intense", "Hopeful", "Bittersweet", "Haunting",
    "Triumphant", "Laid-back", "Playful", "Explosive"
]
CONTEXT_LIST = [
    "driving", "working out", "party", "chill", "romance", "sad",
    "nostalgia", "morning", "night", "summer", "rainy day", "focus"
]


# ── DB ─────────────────────────────────────────────────────────────────────────

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS songs (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        path            TEXT UNIQUE,
        filename        TEXT,
        root_dir        TEXT,
        artist          TEXT,
        title           TEXT,
        album           TEXT,
        year            TEXT,
        track_num       TEXT,
        genre           TEXT,
        subgenre        TEXT,
        mood            TEXT,
        usage_context   TEXT,
        theme           TEXT,
        energy          TEXT,
        language        TEXT,
        region          TEXT,
        popularity      TEXT,
        duration        REAL,
        bitrate         INTEGER,
        codec           TEXT,
        sample_rate     INTEGER,
        channels        INTEGER,
        valid           INTEGER DEFAULT 1,
        indexed_at      INTEGER
    )''')
    # Add new columns to existing DBs that predate this schema
    for col in ('language TEXT', 'region TEXT', 'popularity TEXT'):
        try:
            conn.execute(f'ALTER TABLE songs ADD COLUMN {col}')
        except sqlite3.OperationalError:
            pass  # already exists
    conn.execute('CREATE INDEX IF NOT EXISTS idx_artist ON songs(artist)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_genre  ON songs(genre)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_mood   ON songs(mood)')
    conn.commit()
    return conn


# ── File scan ──────────────────────────────────────────────────────────────────

def scan_files(root_path):
    """Walk root_path and return list of absolute audio file paths."""
    files = []
    for dirpath, _, filenames in os.walk(root_path):
        for fn in sorted(filenames):
            if Path(fn).suffix.lower() in AUDIO_EXTENSIONS:
                files.append(os.path.join(dirpath, fn))
    return files


# ── ffprobe ────────────────────────────────────────────────────────────────────

def probe_file(filepath):
    """Return cleaned ffprobe metadata dict for a single file."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', '-show_streams', filepath],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(result.stdout)
    except Exception:
        return {}

    fmt = data.get('format', {})
    stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), {})

    # Clean tags — strip binary/private fields and empty values
    raw_tags = fmt.get('tags', {})
    tags = {}
    for k, v in raw_tags.items():
        if k.lower().startswith('id3v2_priv') or k.lower().startswith('wm/'):
            continue
        v = v.strip() if isinstance(v, str) else v
        if v:
            tags[k.lower()] = v

    return {
        'tags':        tags,
        'duration':    float(fmt.get('duration', 0) or 0),
        'bitrate':     int(fmt.get('bit_rate', 0) or 0),
        'codec':       stream.get('codec_name', ''),
        'sample_rate': int(stream.get('sample_rate', 0) or 0),
        'channels':    int(stream.get('channels', 0) or 0),
    }


# ── LLM calls ─────────────────────────────────────────────────────────────────

def build_prompt(songs):
    """Build the classification prompt for a batch of songs."""
    lines = []
    for s in songs:
        parts = [f"#{s['idx']}"]
        parts.append(f"path={s['rel_path']}")
        tags = s['probe'].get('tags', {})
        for key in ('artist', 'album_artist', 'title', 'album', 'date', 'track', 'genre'):
            if tags.get(key):
                parts.append(f"{key}={tags[key]}")
        dur = s['probe'].get('duration', 0)
        if dur:
            parts.append(f"duration={int(dur//60)}:{int(dur%60):02d}")
        lines.append(' | '.join(parts))

    return f"""You are a music expert with deep knowledge of artists, albums, and songs worldwide.

For each song below you are given: a file path (structure: Artist/Album/track-title.ext) and any embedded audio tags.

Tasks per song:
1. **Infer** artist, title, album, year from the path and embedded tags. Clean artifacts (track numbers, underscores, suffixes like "-nvs"). Use proper title casing. For Chinese artists/songs stored in pinyin or romanisation (e.g. "Zhou Jie Lun", "Wo De Xin Li Zhi You Ni", "Wang Fei"), keep the romanised form as-is — do not convert to Chinese characters.
2. **Verify** — set "valid": false if the song identity cannot be reasonably determined.
3. **Enrich** with:
   - genre (from: {', '.join(GENRE_LIST)})
   - subgenre (specific, e.g. Grunge, Neo-Soul, Trip Hop, Post-Punk, Stoner Rock)
   - mood (1-3 words, NEVER "Unknown", e.g. {', '.join(MOOD_LIST[:6])})
   - usage_context (1-3 tags, NEVER "General Listening", from: {', '.join(CONTEXT_LIST)} — also include lyrical/sonic themes as extra tags when relevant, e.g. "love, romance", "rebellion, driving", "introspection, night")
   - energy (low | medium | high)
   - language (primary vocal language, e.g. English, Mandarin, Japanese, Korean, Cantonese, Spanish, French, Indonesian — use "Instrumental" if no vocals. Note: Chinese songs are often stored with pinyin or romanised artist/title/album names (e.g. "Wo De Xin Li Zhi You Ni", "Jay Chou", "Faye Wong") — recognise these as Mandarin or Cantonese accordingly)
   - region (country or region of origin, e.g. USA, UK, Japan, South Korea, China, Taiwan, Hong Kong, France, Australia. Apply the same pinyin/romanisation awareness for Chinese-language artists)
   - popularity (mainstream | popular | indie | niche | obscure — based on commercial reach and general recognition)
   - track_num (numeric string if identifiable)

Base mood, context, language, region, and popularity on the **specific song**, not the artist's general style.

Songs:
{chr(10).join(lines)}

Respond with a JSON array only. Each object:
{{"idx": <int>, "artist": "...", "title": "...", "album": "...", "year": "YYYY", "track_num": "...", "genre": "...", "subgenre": "...", "mood": "...", "usage_context": "...", "energy": "low|medium|high", "language": "...", "region": "...", "popularity": "mainstream|popular|indie|niche|obscure", "valid": true}}

Always include "idx" and "valid". Omit fields you have no basis to fill."""


def _retry_on_429(func):
    """Decorator that retries on 429 with exponential backoff (5s, 10s, 20s)."""
    import requests as _req
    def wrapper(*args, **kwargs):
        for attempt in range(4):
            try:
                return func(*args, **kwargs)
            except _req.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 429 and attempt < 3:
                    wait = 2 ** attempt * 5
                    print(f"\n    429 rate limited, waiting {wait}s (retry {attempt+1}/3)...")
                    time.sleep(wait)
                    continue
                raise
    return wrapper


@_retry_on_429
def call_minimax(api_key, model, prompt, timeout=120):
    import requests
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 40960,
        'temperature': 0.1,
    }
    t0 = time.time()
    try:
        resp = requests.post(LLM_CONFIGS['minimax']['url'], headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        elapsed = time.time() - t0
        return resp.json()['choices'][0]['message']['content'].strip(), elapsed
    except Exception:
        elapsed = time.time() - t0
        raise


@_retry_on_429
def call_haiku(api_key, model, prompt):
    import requests
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
    }
    payload = {
        'model': model,
        'max_tokens': 8192,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    resp = requests.post(LLM_CONFIGS['haiku']['url'], headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()['content'][0]['text'].strip()


def parse_llm_response(text):
    """Strip think blocks, code fences, and parse JSON. Falls back to extracting partial objects."""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text).strip()

    # Try full parse first
    try:
        results = json.loads(text)
        # Handle array (expected) or dict keyed by idx
        if isinstance(results, list):
            return {r['idx']: r for r in results if isinstance(r, dict) and 'idx' in r}
        elif isinstance(results, dict):
            if 'idx' in results:
                return {results['idx']: results}
            # {"420": {...}, ...} — skip non-dict values
            out = {}
            for k, v in results.items():
                if isinstance(v, dict):
                    try:
                        out[int(k)] = v
                    except (ValueError, TypeError):
                        pass
            return out
    except json.JSONDecodeError:
        pass

    # Fallback: extract individual complete JSON objects from truncated array
    recovered = []
    for m in re.finditer(r'\{[^{}]*\}', text, re.DOTALL):
        try:
            obj = json.loads(m.group())
            if 'idx' in obj:
                recovered.append(obj)
        except json.JSONDecodeError:
            continue
    if recovered:
        print(f"    Recovered {len(recovered)} objects from partial JSON")
        return {r['idx']: r for r in recovered}

    raise ValueError(f"Could not parse LLM response: {text[:200]}")


def classify_batch(llm, api_key, model, songs, dry_run=False, timeout=120, quiet=True, _depth=0):
    """Classify a batch. On failure, split in half and retry recursively (max 2 splits; 3rd failure drops)."""
    def _log(*a, **kw):
        if not quiet:
            print(*a, **kw)

    if dry_run:
        _log(f"    [dry-run] {len(songs)} songs | sample: {songs[0]['rel_path']}")
        return {}, 0.0

    prompt = build_prompt(songs)
    t0 = time.time()
    text = '(no response)'
    try:
        if llm == 'minimax':
            text, elapsed = call_minimax(api_key, model, prompt, timeout=timeout)
        else:
            text = call_haiku(api_key, model, prompt)
            elapsed = time.time() - t0

        results = parse_llm_response(text)

        enriched = sum(
            1 for r in results.values()
            if any(r.get(f) for f in ('mood', 'subgenre', 'usage_context', 'energy'))
        )
        if enriched == 0 and results:
            raise ValueError(f"got {len(results)} results but all fields empty")

        return results, elapsed

    except Exception as e:
        elapsed = time.time() - t0
        attempt_label = ['1st', '2nd', '3rd'][min(_depth, 2)]
        # Always print errors so the agent can see what's going wrong
        print(f"\n    {attempt_label} attempt failed ({len(songs)} songs, {elapsed:.1f}s): {e}")
        _log(f"    Raw ({len(text)} chars): {repr(text[:300])}")

        max_depth = 1 if len(songs) < 4 else 2
        if _depth >= max_depth or len(songs) <= 1:
            print(f"    Dropping {len(songs)} song(s) after retries exhausted")
            return {}, elapsed

        mid = len(songs) // 2
        print(f"    Splitting {len(songs)} → {mid} + {len(songs) - mid} and retrying...")
        combined = {}
        total_elapsed = elapsed
        for half in [songs[:mid], songs[mid:]]:
            r, t = classify_batch(llm, api_key, model, half, dry_run=dry_run, timeout=timeout, quiet=quiet, _depth=_depth + 1)
            combined.update(r)
            total_elapsed += t
        return combined, total_elapsed


# ── Main ───────────────────────────────────────────────────────────────────────

def run(path, llm, api_key, model, db_path, batch_size, force, dry_run, workers=4, timeout=120, quiet=True):
    def log(*a, **kw):
        if not quiet:
            print(*a, **kw)

    root = os.path.abspath(path)
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    log(f"Scanning: {root}")
    all_files = scan_files(root)
    log(f"Found {len(all_files):,} audio files")

    conn = init_db(db_path)

    # ── Phase 0: mark missing files invalid ───────────────────────────────────
    all_files_set = set(all_files)
    db_paths = [r[0] for r in conn.execute('SELECT path FROM songs WHERE valid=1 AND root_dir=?', (root,))]
    missing = [p for p in db_paths if p not in all_files_set]
    if missing:
        conn.executemany('UPDATE songs SET valid=0 WHERE path=?', [(p,) for p in missing])
        conn.commit()
        print(f"Marked {len(missing):,} missing files as invalid (deleted or moved).")
    else:
        log("No missing files detected.")

    # ── Phase 1: ffprobe new files ────────────────────────────────────────────
    already_probed = set(r[0] for r in conn.execute('SELECT path FROM songs'))
    if force:
        files_to_probe = all_files
        log(f"Force mode: re-probing all {len(files_to_probe):,} files")
    else:
        files_to_probe = [f for f in all_files if f not in already_probed]
        log(f"Already probed: {len(already_probed):,} | New to probe: {len(files_to_probe):,}")

    if files_to_probe:
        log("Running ffprobe...")
        ts = int(time.time())
        for i, fp in enumerate(files_to_probe):
            probe = probe_file(fp)
            tags = probe.get('tags', {})
            def _tag(*keys):
                for k in keys:
                    v = tags.get(k, '').strip()
                    if v:
                        return v
                return ''
            row = {
                'path':          fp,
                'filename':      os.path.basename(fp),
                'root_dir':      root,
                'artist':        _tag('artist', 'album_artist'),
                'title':         _tag('title'),
                'album':         _tag('album'),
                'year':          _tag('date'),
                'track_num':     _tag('track'),
                'genre':         _tag('genre'),
                'subgenre':      '',
                'mood':          '',
                'usage_context': '',
                'energy':        '',
                'duration':      probe.get('duration', 0),
                'bitrate':       probe.get('bitrate', 0),
                'codec':         probe.get('codec', ''),
                'sample_rate':   probe.get('sample_rate', 0),
                'channels':      probe.get('channels', 0),
                'valid':         1,
                'indexed_at':    ts,
            }
            conn.execute('''INSERT OR IGNORE INTO songs
                (path,filename,root_dir,artist,title,album,year,track_num,genre,subgenre,
                 mood,usage_context,energy,duration,bitrate,codec,sample_rate,channels,valid,indexed_at)
                VALUES (:path,:filename,:root_dir,:artist,:title,:album,:year,:track_num,:genre,:subgenre,
                        :mood,:usage_context,:energy,:duration,:bitrate,:codec,:sample_rate,:channels,:valid,:indexed_at)''',
                row)
            pct = (i + 1) / len(files_to_probe) * 100
            print(f"\rPhase 1 (ffprobe): {i+1:,}/{len(files_to_probe):,} ({pct:.1f}%)", end='', flush=True)
            if (i + 1) % 500 == 0:
                conn.commit()
        conn.commit()
        print()  # newline after \r progress
        log(f"ffprobe done. {len(files_to_probe):,} new songs saved to DB.")
    else:
        log("No new files to probe.")

    # ── Phase 2: LLM enrichment for songs missing any enrichment fields ──────
    # Covers: newly probed, previously interrupted, and already-enriched songs
    # lacking language/region/popularity (added later to schema).
    rows = conn.execute(
        '''SELECT path, filename, artist, title, album, year, genre
           FROM songs
           WHERE root_dir = ? AND (
               mood = "" OR mood IS NULL OR
               subgenre = "" OR subgenre IS NULL OR
               language = "" OR language IS NULL OR
               region = "" OR region IS NULL OR
               popularity = "" OR popularity IS NULL
           )
           ORDER BY path''',
        (root,)
    ).fetchall()

    random.shuffle(rows)
    songs = [
        {'idx': i, 'filepath': r[0], 'filename': r[1],
         'rel_path': os.path.relpath(r[0], root),
         'probe': {'tags': {k: v for k, v in zip(
                       ('artist', 'title', 'album', 'date', 'genre'), r[2:7]) if v},
                   'duration': 0, 'bitrate': 0, 'codec': '', 'sample_rate': 0, 'channels': 0}}
        for i, r in enumerate(rows)
    ]

    if not songs:
        print("All songs already fully enriched.")
        conn.close()
        return

    log(f"Starting LLM classification ({llm} / {model}) for {len(songs):,} songs needing enrichment | workers={workers}...")

    # Split into batches upfront
    batches = [songs[i:i + batch_size] for i in range(0, len(songs), batch_size)]
    total_batches = len(batches)
    indexed = 0
    llm_enriched = 0
    failed = 0
    dropped = 0
    timeouts = 0
    ts = int(time.time())
    phase2_start = time.time()
    durations = []
    recent = []  # last 10 durations (including failures)

    print(f"Phase 2 (LLM): {len(songs):,} songs in {total_batches} batches | {llm}/{model} | workers={workers} | timeout={timeout}s")

    def process_batch(batch_num, batch):
        log(f"Batch {batch_num}/{total_batches} ({len(batch)} songs)...")
        results, elapsed = classify_batch(llm, api_key, model, batch, dry_run=dry_run, timeout=timeout, quiet=quiet)
        return batch_num, batch, results, elapsed

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_batch, i + 1, batch): i for i, batch in enumerate(batches)}

        for future in as_completed(futures):
            batch_num, batch, results, elapsed = future.result()
            if elapsed > 0:
                durations.append(elapsed)
                recent.append(elapsed)
                if len(recent) > 10:
                    recent.pop(0)
            if not results:
                timeouts += 1
                dropped += len(batch)

            if dry_run:
                continue

            for song in batch:
                r = results.get(song['idx'], {})

                # Skip songs where LLM returned no result — leave them un-enriched for next run
                if not r:
                    continue

                probe = song['probe']
                tags = probe.get('tags', {})

                def to_str(val):
                    """Coerce LLM value to string — handles lists like ['driving', 'chill']."""
                    if isinstance(val, list):
                        return ', '.join(str(v) for v in val if v)
                    return str(val).strip() if val else ''

                def pick(llm_field, *tag_keys):
                    v = to_str(r.get(llm_field, ''))
                    if v and v not in ('Unknown', 'General Listening', 'N/A'):
                        return v
                    for k in tag_keys:
                        t = tags.get(k, '').strip()
                        if t:
                            return t
                    return ''

                def norm_mood(val):
                    """Sort comma-separated moods alphabetically for consistency.
                    'Upbeat, Energetic' and 'Energetic, Upbeat' → 'Energetic, Upbeat'
                    '&' is part of established mood names ('Chill & Dreamy') — not a separator.
                    """
                    s = to_str(val)
                    if not s:
                        return ''
                    parts = sorted(p.strip().title() for p in s.split(',') if p.strip())
                    return ', '.join(parts)

                def norm_usage_context(val):
                    """Sort comma-separated contexts alphabetically so order is deterministic.
                    'driving, party' and 'party, driving' both → 'driving, party'
                    Handles LLM returning a list or a string.
                    """
                    s = to_str(val)
                    if not s:
                        return ''
                    parts = sorted(p.strip().lower() for p in s.split(',') if p.strip())
                    return ', '.join(parts)

                _REGION_MAP = {
                    'united kingdom':           'UK',
                    'england':                  'UK',
                    'great britain':            'UK',
                    'britain':                  'UK',
                    'uk':                       'UK',
                    'u.k.':                     'UK',
                    'us':                       'USA',
                    'usa':                      'USA',
                    'united states':            'USA',
                    'united states of america': 'USA',
                    'the usa':                  'USA',
                    'u.s.a.':                   'USA',
                    'u.s.':                     'USA',
                    'south korea':              'South Korea',
                    'korea':                    'South Korea',
                    'republic of korea':        'South Korea',
                    'hong kong sar':            'Hong Kong',
                    'prc':                      'China',
                    'mainland china':           'China',
                }

                def norm_region(val):
                    """Normalize region aliases. Title-case only all-lowercase values."""
                    s = to_str(val).strip()
                    if not s:
                        return ''
                    mapped = _REGION_MAP.get(s.lower())
                    if mapped:
                        return mapped
                    return s.title() if s == s.lower() else s

                def norm_popularity(val):
                    """Lowercase popularity so 'Indie' and 'indie' unify."""
                    return to_str(val).strip().lower()

                try:
                    row = {
                        'path':          song['filepath'],
                        'filename':      song['filename'],
                        'root_dir':      root,
                        'artist':        pick('artist', 'artist', 'album_artist'),
                        'title':         pick('title', 'title'),
                        'album':         pick('album', 'album'),
                        'year':          pick('year', 'date'),
                        'track_num':     pick('track_num', 'track'),
                        'genre':         pick('genre', 'genre'),
                        'subgenre':      to_str(r.get('subgenre')),
                        'mood':          norm_mood(r.get('mood')),
                        'usage_context': norm_usage_context(r.get('usage_context')),
                        'energy':        to_str(r.get('energy')).lower(),
                        'language':      to_str(r.get('language')).strip(),
                        'region':        norm_region(r.get('region')),
                        'popularity':    norm_popularity(r.get('popularity')),
                        'duration':      probe.get('duration', 0),
                        'bitrate':       probe.get('bitrate', 0),
                        'codec':         probe.get('codec', ''),
                        'sample_rate':   probe.get('sample_rate', 0),
                        'channels':      probe.get('channels', 0),
                        'valid':         1 if r.get('valid', True) else 0,
                        'indexed_at':    ts,
                    }
                    conn.execute('''UPDATE songs SET
                        artist=:artist, title=:title, album=:album, year=:year, track_num=:track_num,
                        genre=:genre, subgenre=:subgenre, mood=:mood, usage_context=:usage_context,
                        energy=:energy, language=:language, region=:region,
                        popularity=:popularity, valid=:valid, indexed_at=:indexed_at
                        WHERE path=:path''', row)
                    indexed += 1
                    if row.get('mood') and row.get('subgenre'):
                        llm_enriched += 1
                except Exception as e:
                    print(f"    DB error for {song['filename']}: {e}")
                    failed += 1

            conn.commit()
            completed_batches = sum(1 for f in futures if f.done())
            pct = completed_batches / total_batches * 100
            wall = time.time() - phase2_start
            rate = (completed_batches * batch_size) / wall if wall > 0 else 0
            remaining = (total_batches - completed_batches) * (sum(recent) / len(recent)) / workers if recent else 0
            eta_str = f" | ETA {int(remaining//60)}m{int(remaining%60):02d}s" if recent else ""
            avg_str = f" | avg {sum(recent)/len(recent):.1f}s/batch" if recent else ""
            err_str = f" | {dropped} dropped, {failed} err" if (dropped or failed) else ""
            if quiet:
                print(f"\rPhase 2 (LLM): {completed_batches}/{total_batches} ({pct:.1f}%) [{rate:.1f} songs/s]{avg_str}{err_str}{eta_str}", end='', flush=True)
            else:
                timing = f" | last {len(recent)}: avg={sum(recent)/len(recent):.1f}s max={max(recent):.1f}s" if recent else ""
                print(f"  [{batch_num}/{total_batches}] {indexed:,} saved, {llm_enriched:,} enriched, {failed:,} failed, {dropped:,} dropped{timing}{eta_str}")

    if quiet:
        print()  # newline after \r progress

    # Final summary
    total_db = conn.execute('SELECT COUNT(*) FROM songs').fetchone()[0]
    enriched_db = conn.execute('SELECT COUNT(*) FROM songs WHERE mood != "" AND mood IS NOT NULL').fetchone()[0]
    wall_total = time.time() - phase2_start
    print(f"\n=== Done in {int(wall_total//60)}m{int(wall_total%60):02d}s: {indexed:,} saved, {llm_enriched:,} LLM-enriched, {failed:,} failed, {dropped:,} dropped ===")
    print(f"DB total: {total_db:,} songs ({enriched_db:,} enriched, {total_db - enriched_db:,} remaining) in {db_path}")

    if not quiet:
        print("\nTop genres:")
        for r in conn.execute('SELECT genre, COUNT(*) n FROM songs WHERE genre != "" GROUP BY genre ORDER BY n DESC LIMIT 10'):
            print(f"  {r[0]}: {r[1]:,}")

        print("\nTop moods:")
        for r in conn.execute('SELECT mood, COUNT(*) n FROM songs WHERE mood != "" GROUP BY mood ORDER BY n DESC LIMIT 8'):
            print(f"  {r[0]}: {r[1]:,}")

        print("\nEnergy distribution:")
        for r in conn.execute('SELECT energy, COUNT(*) n FROM songs GROUP BY energy ORDER BY n DESC'):
            label = r[0] or '(unset)'
            print(f"  {label}: {r[1]:,}")

        print("\nTop languages:")
        for r in conn.execute('SELECT language, COUNT(*) n FROM songs WHERE language != "" AND language IS NOT NULL GROUP BY language ORDER BY n DESC LIMIT 10'):
            print(f"  {r[0]}: {r[1]:,}")

        print("\nTop regions:")
        for r in conn.execute('SELECT region, COUNT(*) n FROM songs WHERE region != "" AND region IS NOT NULL GROUP BY region ORDER BY n DESC LIMIT 10'):
            print(f"  {r[0]}: {r[1]:,}")

        print("\nPopularity distribution:")
        for r in conn.execute('SELECT popularity, COUNT(*) n FROM songs GROUP BY popularity ORDER BY n DESC'):
            label = r[0] or '(unset)'
            print(f"  {label}: {r[1]:,}")

        print("\nYear coverage:")
        with_year = conn.execute('SELECT COUNT(*) FROM songs WHERE LENGTH(year) = 4').fetchone()[0]
        print(f"  {with_year:,} / {total_db:,} ({with_year/total_db*100:.1f}% have year)" if total_db else "  0 songs")

    conn.close()


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smart Music Indexer — LLM-powered metadata extraction')
    parser.add_argument('--path',    required=True, help='Root directory to scan for music files')
    parser.add_argument('--llm',     required=True, choices=['minimax', 'haiku'], help='LLM service to use')
    parser.add_argument('--key',     help='API key (or set MINIMAX_API_KEY / ANTHROPIC_API_KEY env var)')
    parser.add_argument('--model',   help='Override default model name')
    parser.add_argument('--db',      default='music.db', help='Output SQLite database (default: music.db)')
    parser.add_argument('--batch',   type=int, default=40, help='Songs per LLM call (default: 40)')
    parser.add_argument('--force',   action='store_true', help='Re-index already indexed files')
    parser.add_argument('--workers', type=int, default=1, help='Parallel LLM workers (default: 1)')
    parser.add_argument('--timeout', type=int, default=120, help='LLM request timeout in seconds (default: 120)')
    parser.add_argument('--dry-run', action='store_true', help='Scan and probe without calling LLM or writing DB')
    parser.add_argument('--verbose', action='store_true', help='Show detailed per-batch logs and stats (default: progress % only)')
    args = parser.parse_args()

    quiet = not args.verbose

    # Resolve API key
    env_key = 'MINIMAX_API_KEY' if args.llm == 'minimax' else 'ANTHROPIC_API_KEY'
    api_key = args.key or os.environ.get(env_key, '')
    if not api_key and not args.dry_run:
        print(f"Error: provide --key or set {env_key} environment variable")
        sys.exit(1)

    # Resolve model
    model = args.model or LLM_CONFIGS[args.llm]['default_model']

    if not quiet:
        print(f"LLM: {args.llm} / {model}")
        print(f"DB:  {args.db}")

    run(
        path=args.path,
        llm=args.llm,
        api_key=api_key,
        model=model,
        db_path=args.db,
        batch_size=args.batch,
        force=args.force,
        dry_run=args.dry_run,
        workers=args.workers,
        timeout=args.timeout,
        quiet=quiet,
    )
