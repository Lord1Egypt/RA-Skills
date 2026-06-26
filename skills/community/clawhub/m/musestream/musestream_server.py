#!/usr/bin/env python3
"""
MuseStream — AI Music Generation & Streaming Server
- Provider-agnostic: plug in any music generation API (Sonauto, Udio, Suno, …)
- Agent creates a shareable session URL via GET /start?prompt=...
- User opens the URL — prompt is hidden, auto-streams music continuously
- Saves completed songs + metadata to OUTPUT_DIR
- Context-aware prompts: weather, mood, activity → music description via rule-based engine
  (agent should use its own LLM to refine prompts before calling /start)

Environment variables:
  MUSIC_PROVIDER          — "sonauto" (default) or any registered provider key
  SONAUTO_API_KEY         — API key for Sonauto (https://sonauto.ai)
  MUSESTREAM_OUTPUT_DIR   — Where to save generated songs (default ~/Music/MuseStream)
  MUSESTREAM_PORT         — Server port (default 5001)
"""

import hashlib
import json
import os
import threading
import time
import requests
from datetime import datetime
from flask import Flask, Response, request, jsonify, stream_with_context

# ── Load config.json ──────────────────────────────────────────────────────────
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
if os.path.exists(_CONFIG_PATH):
    with open(_CONFIG_PATH) as _f:
        _cfg = json.load(_f)
else:
    _cfg = {}

def _conf(key, default=""):
    """Read from config.json, fall back to env var, then default."""
    return _cfg.get(key, os.environ.get(key, default))

app = Flask(__name__)

# ── Provider registry ─────────────────────────────────────────────────────────
# To add a new provider, add an entry here and implement its generate/stream
# logic in start_generation() and wait_for_stream() below.

PROVIDERS = {
    "sonauto": {
        "name":          "Sonauto",
        "register_url":  "https://sonauto.ai",
        "key_env":       "SONAUTO_API_KEY",
        "generate_url":  "https://api.sonauto.ai/v1/generations/v3",
        "stream_base":   "https://api-stream.sonauto.ai/stream",
        "status_url":    "https://api.sonauto.ai/v1/generations/status",
        "meta_url":      "https://api.sonauto.ai/v1/generations",
        "audio_fmt":     "ogg",
        "mime":          "audio/ogg",
    },
    # ── Future providers (uncomment and fill in URLs) ──────────────────────
    # "udio": {
    #     "name":         "Udio",
    #     "register_url": "https://udio.com",
    #     "key_env":      "UDIO_API_KEY",
    #     "generate_url": "https://api.udio.com/v1/generate",
    #     "stream_base":  "https://api.udio.com/v1/stream",
    #     "status_url":   "https://api.udio.com/v1/status",
    #     "meta_url":     "https://api.udio.com/v1/songs",
    #     "audio_fmt":    "mp3",
    #     "mime":         "audio/mpeg",
    # },
}

_PROVIDER_ID = _conf("MUSIC_PROVIDER", "sonauto")
if _PROVIDER_ID not in PROVIDERS:
    raise ValueError(f"Unknown MUSIC_PROVIDER '{_PROVIDER_ID}'. Available: {list(PROVIDERS)}")

_P       = PROVIDERS[_PROVIDER_ID]
API_KEY  = _conf(_P["key_env"])

OUTPUT_DIR = _conf("MUSESTREAM_OUTPUT_DIR", os.path.expanduser("~/Music/MuseStream"))
if OUTPUT_DIR.startswith("~"):
    OUTPUT_DIR = os.path.expanduser(OUTPUT_DIR)
LOG_FILE   = os.path.join(OUTPUT_DIR, "log.jsonl")
PORT       = int(_conf("MUSESTREAM_PORT", 5001))

os.makedirs(OUTPUT_DIR, exist_ok=True)

_sessions      = {}   # key -> prompt
_tasks         = {}   # task_id -> task dict
_session_tasks = {}   # session_key -> [task_id, ...]


# ── Provider API helpers ───────────────────────────────────────────────────────

def api_headers():
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def start_generation(prompt):
    """Start a music generation job. Returns task_id."""
    if _PROVIDER_ID == "sonauto":
        payload = {"prompt": prompt, "enable_streaming": True}
        resp = requests.post(
            _P["generate_url"],
            headers=api_headers(),
            json=payload,
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"Sonauto API error {resp.status_code}: {resp.text}")
            print(f"  Payload sent: {payload}")
        resp.raise_for_status()
        task_id = resp.json().get("task_id")
        if not task_id:
            raise ValueError(f"No task_id in response: {resp.text}")
        return task_id
    # Add elif blocks here for additional providers
    raise NotImplementedError(f"start_generation not implemented for provider '{_PROVIDER_ID}'")


def wait_for_stream(task_id):
    """Background thread: poll until audio stream is available."""
    task = _tasks[task_id]
    stream_url = f"{_P['stream_base']}/{task_id}"
    status_url = f"{_P['status_url']}/{task_id}"
    audio_magic = b"OggS" if _P["audio_fmt"] == "ogg" else b"\xff\xfb"  # OGG or MP3 sync

    while not task["stop"].is_set():
        try:
            r = requests.get(
                stream_url,
                headers={"Authorization": f"Bearer {API_KEY}", "Accept": f"audio/{_P['audio_fmt']}"},
                timeout=15, stream=True,
            )
            if r.status_code == 200:
                for chunk in r.iter_content(512):
                    if chunk[:4] == audio_magic or (len(chunk) > 0 and _P["audio_fmt"] == "mp3"):
                        task["status"] = "ready"
                        task["ready"].set()
                        threading.Thread(target=fetch_metadata, args=(task_id, None), daemon=True).start()
                        return
                    break
        except Exception:
            pass
        try:
            s = requests.get(
                status_url,
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=10,
            ).text.strip('"')
            if "FAILURE" in s or "FAILED" in s or "error" in s.lower():
                task["status"] = "failed"
                task["ready"].set()
                return
        except Exception:
            pass
        time.sleep(3)


def fetch_metadata(task_id, saved_path=None):
    """Poll provider until title/tags are available, then store for display.
    If saved_path provided, also append to log.jsonl."""
    task = _tasks.get(task_id, {})
    meta_url = f"{_P['meta_url']}/{task_id}"
    data = {}
    for attempt in range(20):
        if task.get("stop", threading.Event()).is_set():
            return
        try:
            resp = requests.get(
                meta_url,
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=30,
            )
            data = resp.json()
            title = data.get("title", "")
            tags  = data.get("tags", [])
            if title or tags:
                break  # metadata is ready
        except Exception as e:
            print(f"Metadata fetch attempt {attempt+1} error {task_id}: {e}")
        time.sleep(5)

    meta = {
        "title":           data.get("title", ""),
        "tags":            data.get("tags", []),
        "lyrics":          data.get("lyrics", ""),
        "prompt_strength": data.get("prompt_strength", ""),
    }
    if task_id in _tasks:
        _tasks[task_id]["metadata"] = meta
    print(f"Metadata ready for {task_id}: {meta.get('title', '(no title)')}")

    if saved_path:
        data["_prompt"]     = task.get("prompt", "")
        data["_saved_path"] = saved_path
        data["_task_id"]    = task_id
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")


# ── Flask endpoints ────────────────────────────────────────────────────────────

@app.route("/start")
def start_session():
    """Agent calls this to create a shareable player URL without exposing the prompt."""
    prompt = request.args.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    key = hashlib.md5((prompt + str(time.time())).encode()).hexdigest()[:8]
    _sessions[key] = prompt
    url = f"http://localhost:{PORT}/player?s={key}"
    return jsonify({"url": url, "key": key, "prompt": prompt})


@app.route("/player")
def player():
    key    = request.args.get("s", "")
    prompt = _sessions.get(key, "")
    if not prompt:
        return "Session not found or expired.", 404
    return _player_html(prompt)


@app.route("/generate")
def generate():
    prompt  = request.args.get("prompt", "").strip()
    session = request.args.get("session", "")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    try:
        task_id = start_generation(prompt)
        _tasks[task_id] = {
            "ready":      threading.Event(),
            "stop":       threading.Event(),
            "save_only":  threading.Event(),  # stop playback but finish saving
            "status":     "pending",
            "prompt":     prompt,
            "session":    session,
            "bytes_sent": 0,
            "metadata":   {},
        }
        if session:
            _session_tasks.setdefault(session, []).append(task_id)
        threading.Thread(target=wait_for_stream, args=(task_id,), daemon=True).start()
        return jsonify({"task_id": task_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status/<task_id>")
def status(task_id):
    task = _tasks.get(task_id)
    if not task:
        return jsonify({"error": "unknown"}), 404
    return jsonify({
        "task_id":      task_id,
        "status":       task["status"],
        "stream_ready": task["ready"].is_set(),
        "bytes_sent":   task.get("bytes_sent", 0),
    })


@app.route("/metadata/<task_id>")
def metadata(task_id):
    task = _tasks.get(task_id)
    if not task:
        return jsonify({"error": "unknown"}), 404
    return jsonify(task.get("metadata", {}))


@app.route("/stream/<task_id>")
def stream_audio(task_id):
    task = _tasks.get(task_id)
    if not task:
        return jsonify({"error": "unknown task_id"}), 404

    def generate_audio():
        task["ready"].wait(timeout=120)
        if task["status"] != "ready" or task["stop"].is_set():
            return

        ext = _P["audio_fmt"]
        tmp = os.path.join(OUTPUT_DIR, f"_tmp_{task_id}.{ext}")
        received = 0
        bg_saving = False
        r = None

        def _finish_save(stream, bytes_received):
            """Drain remaining stream to file in background and save."""
            rcv = bytes_received
            try:
                with open(tmp, "ab") as f:
                    for chunk in stream.iter_content(4096):
                        if task["stop"].is_set():
                            break
                        if chunk:
                            f.write(chunk)
                            rcv += len(chunk)
                            task["bytes_sent"] = rcv
            except Exception as e:
                print(f"Background drain error {task_id}: {e}")
            finally:
                task["status"] = "done"
                if rcv > 10_000:
                    final = os.path.join(OUTPUT_DIR, f"{task_id}.{ext}")
                    try:
                        os.rename(tmp, final)
                        print(f"Stream saved (background): {final}")
                        threading.Thread(target=fetch_metadata, args=(task_id, final), daemon=True).start()
                    except Exception:
                        pass
                elif os.path.exists(tmp):
                    os.remove(tmp)

        def _stop_queued_session_tasks():
            session = task.get("session", "")
            if session:
                for tid in _session_tasks.get(session, []):
                    if tid != task_id and tid in _tasks:
                        _tasks[tid]["stop"].set()
                        _tasks[tid]["status"] = "stopped"
                        print(f"Session {session}: stopped queued task {tid}")

        try:
            r = requests.get(
                f"{_P['stream_base']}/{task_id}",
                headers={"Authorization": f"Bearer {API_KEY}", "Accept": f"audio/{ext}"},
                timeout=300, stream=True,
            )
            f = open(tmp, "wb")
            try:
                for chunk in r.iter_content(4096):
                    if task["stop"].is_set():
                        break
                    if task["save_only"].is_set():
                        # Stop yielding to browser; hand off stream to background thread
                        if chunk:
                            f.write(chunk)
                            received += len(chunk)
                        f.close()
                        bg_saving = True
                        _stop_queued_session_tasks()
                        threading.Thread(target=_finish_save, args=(r, received), daemon=True).start()
                        return
                    if chunk:
                        f.write(chunk)
                        received += len(chunk)
                        task["bytes_sent"] = received
                        yield chunk
            finally:
                try:
                    f.close()
                except Exception:
                    pass
        except GeneratorExit:
            # Browser disconnected — finish saving in background
            _stop_queued_session_tasks()
            if not task["stop"].is_set() and r:
                bg_saving = True
                threading.Thread(target=_finish_save, args=(r, received), daemon=True).start()
            return
        except Exception as e:
            print(f"Stream proxy error {task_id}: {e}")
        finally:
            if not bg_saving:
                task["status"] = "done"
                if received > 10_000:
                    final = os.path.join(OUTPUT_DIR, f"{task_id}.{ext}")
                    try:
                        os.rename(tmp, final)
                        print(f"Stream saved: {final}")
                        threading.Thread(target=fetch_metadata, args=(task_id, final), daemon=True).start()
                    except Exception:
                        pass
                elif os.path.exists(tmp):
                    os.remove(tmp)

    return Response(
        stream_with_context(generate_audio()),
        mimetype=_P["mime"],
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/stop", methods=["POST"])
def stop():
    data = request.json or {}
    ids  = ([data.get("task_id")] if data.get("task_id") else []) + data.get("task_ids", [])
    for tid in ids:
        if tid and tid in _tasks:
            t = _tasks[tid]
            if t.get("status") == "ready":
                # Currently streaming — stop playback but finish saving in background
                t["save_only"].set()
            else:
                # Queued or pending — hard stop
                t["stop"].set()
                t["status"] = "stopped"
    return jsonify({"ok": True})


@app.route("/")
def index():
    return _library_html()


@app.route("/library")
def library():
    """List all completed songs in OUTPUT_DIR with metadata from log file."""
    meta = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    tid = d.get("_task_id") or d.get("id", "")
                    if tid:
                        meta[tid] = {
                            "title":  d.get("title", ""),
                            "tags":   d.get("tags", []),
                            "prompt": d.get("_prompt", ""),
                        }
                except Exception:
                    pass

    songs = []
    for fname in sorted(os.listdir(OUTPUT_DIR), reverse=True):
        ext = os.path.splitext(fname)[1].lower()
        if fname.startswith("_tmp_") or ext not in (".ogg", ".mp3"):
            continue
        task_id = os.path.splitext(fname)[0]
        m = meta.get(task_id, {})
        songs.append({
            "task_id":  task_id,
            "filename": fname,
            "size":     os.path.getsize(os.path.join(OUTPUT_DIR, fname)),
            "title":    m.get("title", ""),
            "tags":     m.get("tags", []),
            "prompt":   m.get("prompt", ""),
        })

    return jsonify({"songs": songs, "count": len(songs)})


@app.route("/files/<path:filename>")
def serve_file(filename):
    """Serve a saved ogg file with range support for seeking."""
    fpath = os.path.realpath(os.path.join(OUTPUT_DIR, filename))
    if not fpath.startswith(os.path.realpath(OUTPUT_DIR)) or not os.path.exists(fpath):
        return "Not found", 404

    file_size    = os.path.getsize(fpath)
    range_header = request.headers.get("Range")

    mime = "audio/mpeg" if fpath.endswith(".mp3") else "audio/ogg"

    if range_header:
        spec  = range_header.replace("bytes=", "")
        start_s, _, end_s = spec.partition("-")
        start  = int(start_s) if start_s else 0
        end    = int(end_s)   if end_s   else file_size - 1
        length = end - start + 1
        with open(fpath, "rb") as f:
            f.seek(start)
            data = f.read(length)
        resp = Response(data, status=206, mimetype=mime)
        resp.headers["Content-Range"]  = f"bytes {start}-{end}/{file_size}"
        resp.headers["Accept-Ranges"]  = "bytes"
        resp.headers["Content-Length"] = str(length)
        return resp

    return Response(open(fpath, "rb").read(), mimetype=mime,
                    headers={"Accept-Ranges": "bytes", "Content-Length": str(file_size)})


# ── Context-based prompt generation ───────────────────────────────────────────

def _build_context_lines(ctx: dict) -> list:
    lines = []
    if ctx.get("time"):        lines.append(f"Time: {ctx['time']}")
    if ctx.get("weather"):     lines.append(f"Weather: {ctx['weather']}")
    if ctx.get("mood"):        lines.append(f"Mood: {ctx['mood']}")
    if ctx.get("activity"):    lines.append(f"Activity: {ctx['activity']}")
    if ctx.get("driving"):     lines.append(f"Driving: {ctx['driving']}")
    if ctx.get("traffic"):     lines.append(f"Traffic: {ctx['traffic']}")
    if ctx.get("destination"): lines.append(f"Destination: {ctx['destination']}")
    if ctx.get("schedule"):    lines.append(f"Schedule: {ctx['schedule']}")
    if ctx.get("notes"):       lines.append(f"Notes: {ctx['notes']}")
    return lines

def _context_to_prompt_rules(ctx: dict) -> str:
    """Fallback rule-based prompt builder (no API key needed)."""
    parts = []

    # Time of day
    hour = datetime.now().hour
    time_label = ctx.get("time", "")
    if not time_label:
        if 5 <= hour < 9:    time_label = "early morning"
        elif 9 <= hour < 12: time_label = "morning"
        elif 12 <= hour < 17:time_label = "afternoon"
        elif 17 <= hour < 21:time_label = "evening"
        else:                 time_label = "late night"

    activity = ctx.get("activity", "").lower()
    mood = ctx.get("mood", "").lower()
    weather = ctx.get("weather", "").lower()
    driving = ctx.get("driving", "").lower()
    traffic = ctx.get("traffic", "").lower()
    destination = ctx.get("destination", "").lower()

    # Energy mapping
    if any(w in activity for w in ("workout", "gym", "run", "exercise")):
        parts.append("high-energy driving")
    elif driving or "driving" in activity:
        if "heavy" in traffic or "standstill" in traffic:
            parts.append("relaxed ambient")
        else:
            parts.append("upbeat road-trip")
    elif any(w in activity for w in ("work", "focus", "study")):
        parts.append("focused lo-fi")
    elif any(w in activity for w in ("relax", "chill", "rest")):
        parts.append("chill ambient")
    elif any(w in activity for w in ("party", "social")):
        parts.append("upbeat party")
    else:
        parts.append("background music")

    # Mood modifiers
    mood_map = {
        "happy": "joyful",  "sad": "melancholic",    "tired": "mellow",
        "excited": "euphoric","anxious": "calming",  "focused": "minimal and focused",
        "romantic": "romantic","angry": "intense",
    }
    for k, v in mood_map.items():
        if k in mood:
            parts.append(v)
            break

    # Weather texture
    if "rain" in weather:    parts.append("with soft rain ambiance")
    elif "sunny" in weather or "clear" in weather: parts.append("bright and sunny")
    elif "cloud" in weather: parts.append("overcast and mellow")
    elif "snow" in weather:  parts.append("cold and sparse")

    # Time texture
    parts.append(f"for {time_label}")

    # Destination hint
    if "home" in destination:   parts.append("homecoming warmth")
    elif "office" in destination or "work" in destination: parts.append("productive energy")
    elif "gym" in destination:  parts.append("motivation and power")

    return " ".join(parts)


def build_context_prompt(ctx: dict) -> str:
    """Build a music prompt from context using rule-based engine."""
    return _context_to_prompt_rules(ctx)


@app.route("/api/context", methods=["POST", "GET"])
def api_context():
    """Accept context JSON, generate music prompt, create session, return player URL.

    POST: JSON body with context fields
    GET:  query params (for Tasker simplicity)
    """
    if request.method == "POST":
        ctx = request.json or {}
    else:
        ctx = {k: v for k, v in request.args.items()}

    if not any(ctx.values()):
        return jsonify({"error": "No context provided"}), 400

    try:
        prompt = build_context_prompt(ctx)
    except Exception as e:
        return jsonify({"error": f"Prompt generation failed: {e}"}), 500

    # Create session
    key = hashlib.md5((prompt + str(time.time())).encode()).hexdigest()[:8]
    _sessions[key] = prompt
    url = f"http://localhost:{PORT}/player?s={key}"

    print(f"Context session {key}: {prompt}")
    return jsonify({"url": url, "prompt": prompt, "key": key})


@app.route("/context-ui")
def context_ui():
    return _context_ui_html()


# ── Player HTML ────────────────────────────────────────────────────────────────

def _player_html(prompt):
    prompt_js = json.dumps(prompt)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>MuseStream</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: monospace; background: #0d0d0d; color: #ddd;
         display: flex; flex-direction: column; align-items: center;
         min-height: 100vh; padding: 30px 20px; }}
  .card {{ background: #1a1a2e; border-radius: 12px; padding: 28px;
           width: 100%; max-width: 580px; }}
  #tapOverlay {{ position: fixed; inset: 0; background: rgba(0,0,0,.85);
                 display: flex; flex-direction: column; align-items: center;
                 justify-content: center; z-index: 99; cursor: pointer; }}
  #tapOverlay h2 {{ color: #e94560; font-size: 1.6em; margin-bottom: 12px; }}
  #tapOverlay p  {{ color: #888; font-size: 14px; }}
  h1 {{ color: #e94560; margin-bottom: 20px; font-size: 1.3em; letter-spacing: 1px; }}
  .prompt-display {{ background: #0d0d0d; border: 1px solid #2a2a3e; border-radius: 6px;
                     padding: 10px 14px; font-size: 14px; color: #aaa;
                     margin-bottom: 14px; word-break: break-word; }}
  .prompt-label {{ font-size: 11px; color: #555; margin-bottom: 4px; }}
  .btns {{ display: flex; gap: 10px; margin-bottom: 14px; }}
  button {{ flex: 1; padding: 10px; border: none; border-radius: 6px;
            font-size: 14px; cursor: pointer; transition: opacity .2s; }}
  button:disabled {{ opacity: .4; cursor: default; }}
  #stopBtn {{ background: #c0392b; color: #fff; }}
  #statusEl {{ font-size: 13px; color: #888; margin-bottom: 8px; min-height: 18px; }}
  audio {{ width: 100%; border-radius: 6px; margin-bottom: 16px; }}
  .meta-card {{ background: #111122; border: 1px solid #2a2a3e; border-radius: 8px;
                padding: 16px; margin-top: 8px; display: none; }}
  .meta-card.visible {{ display: block; }}
  .meta-title {{ color: #e94560; font-size: 15px; font-weight: bold; margin-bottom: 10px; }}
  .meta-row {{ margin-bottom: 8px; font-size: 12px; }}
  .meta-label {{ color: #555; margin-bottom: 2px; }}
  .meta-value {{ color: #ccc; }}
  .meta-tags {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }}
  .tag {{ background: #2a2a3e; border-radius: 4px; padding: 2px 8px; font-size: 11px; color: #aaa; }}
  .lyrics {{ white-space: pre-wrap; line-height: 1.7; color: #bbb; max-height: 200px;
             overflow-y: auto; font-size: 12px; }}
  #log {{ margin-top: 14px; font-size: 11px; color: #444;
          max-height: 120px; overflow-y: auto; line-height: 1.6; }}
</style>
</head>
<body>
<div id="tapOverlay" onclick="dismissOverlay()">
  <h2>▶ Tap to Start</h2>
  <p>Preparing your stream…</p>
</div>
<div class="card">
  <h1>♪ MuseStream</h1>
  <div class="prompt-label">Prompt</div>
  <div class="prompt-display" id="promptDisplay"></div>
  <div class="btns">
    <button id="stopBtn" onclick="stopStream()">■ Stop Stream</button>
  </div>
  <div id="statusEl">Starting…</div>
  <audio id="audio1" controls></audio>
  <audio id="audio2" controls style="display:none"></audio>

  <div class="meta-card" id="metaCard">
    <div class="meta-title" id="metaTitle"></div>
    <div class="meta-row">
      <div class="meta-label">Tags</div>
      <div class="meta-tags" id="metaTags"></div>
    </div>
    <div class="meta-row" id="metaStrengthRow">
      <div class="meta-label">Prompt strength</div>
      <div class="meta-value" id="metaStrength"></div>
    </div>
    <div class="meta-row" id="metaLyricsRow">
      <div class="meta-label">Lyrics</div>
      <div class="lyrics" id="metaLyrics"></div>
    </div>
  </div>

  <div id="log"></div>
</div>

<script>
const PROMPT   = {prompt_js};
const SESSION  = new URLSearchParams(location.search).get('s') || '';
const TRIGGER_SECS = 120;

let userGesture = false;
let pendingPlay = null;  // audio element waiting to play after gesture

function dismissOverlay() {{
  userGesture = true;
  $('tapOverlay').style.display = 'none';
  if (pendingPlay) {{
    pendingPlay.play().catch(() => {{}});
    pendingPlay = null;
  }}
}}

let currentTaskId = null;
let nextTaskId    = null;
let stopped       = false;

const $ = id => document.getElementById(id);
$('promptDisplay').textContent = PROMPT;

function log(msg) {{
  $('log').innerHTML = '<span>' + new Date().toLocaleTimeString() + ' ' + msg + '</span><br>' + $('log').innerHTML;
}}
function setStatus(msg) {{ $('statusEl').textContent = msg; }}

async function apiGenerate() {{
  const r = await fetch('/generate?prompt=' + encodeURIComponent(PROMPT) + '&session=' + encodeURIComponent(SESSION));
  const d = await r.json();
  if (d.error) throw new Error(d.error);
  return d.task_id;
}}

async function waitReady(taskId, timeoutMs = 120000) {{
  const end = Date.now() + timeoutMs;
  while (Date.now() < end) {{
    const r = await fetch('/status/' + taskId);
    const d = await r.json();
    if (d.stream_ready) return true;
    if (d.status === 'failed' || d.status === 'stopped') return false;
    await new Promise(r => setTimeout(r, 1500));
  }}
  return false;
}}

async function showMetadata(taskId) {{
  // Poll until metadata is available (fetched server-side after stream ready)
  for (let i = 0; i < 20; i++) {{
    try {{
      const r = await fetch('/metadata/' + taskId);
      const m = await r.json();
      if (m && !m.error && m.title) {{
        $('metaCard').classList.add('visible');
        $('metaTitle').textContent = m.title || '(untitled)';
        $('metaTags').innerHTML = (m.tags || []).map(t => `<span class="tag">${{t}}</span>`).join('');
        if (m.prompt_strength) {{
          $('metaStrength').textContent = m.prompt_strength;
          $('metaStrengthRow').style.display = 'block';
        }} else {{
          $('metaStrengthRow').style.display = 'none';
        }}
        if (m.lyrics) {{
          $('metaLyrics').textContent = m.lyrics;
          $('metaLyricsRow').style.display = 'block';
        }} else {{
          $('metaLyricsRow').style.display = 'none';
        }}
        return;
      }}
    }} catch(e) {{}}
    await new Promise(r => setTimeout(r, 3000));
  }}
}}

function playTask(taskId, audioId) {{
  const audio = $(audioId);
  audio.style.display = 'block';
  audio.src = '/stream/' + taskId;
  audio.load();
  if (userGesture) {{
    audio.play().catch(() => {{}});
  }} else {{
    pendingPlay = audio;  // will play once user taps overlay
  }}
  setStatus('Streaming…');
  log('Playing ' + taskId);

  let nextQueued = false;
  let switched   = false;

  async function queueNext() {{
    if (nextQueued || stopped) return;
    nextQueued = true;
    log('Queueing next song…');
    try {{ nextTaskId = await apiGenerate(); }} catch(e) {{ log('Queue error: ' + e.message); }}
  }}

  async function switchToNext() {{
    if (switched || stopped) return;
    switched = true;

    if (!nextTaskId) {{
      log('Generating next (may gap)…');
      try {{ nextTaskId = await apiGenerate(); }} catch(e) {{ stopStream(); return; }}
    }}

    setStatus('Loading next song…');
    const ready = await waitReady(nextTaskId, 120000);
    if (!ready || stopped) {{ stopStream(); return; }}

    const nextAudioId = audioId === 'audio1' ? 'audio2' : 'audio1';
    const newTaskId = nextTaskId;
    playTask(newTaskId, nextAudioId);
    $(audioId).style.display = 'none';
    currentTaskId = newTaskId;
    nextTaskId    = null;

    // Show metadata for the now-playing song
    showMetadata(newTaskId);
  }}

  let triggerFired = false;
  const poll = setInterval(async () => {{
    if (stopped || switched) {{ clearInterval(poll); return; }}
    try {{
      if (!triggerFired && audio.currentTime >= TRIGGER_SECS) {{
        triggerFired = true;
        log(Math.round(audio.currentTime) + 's played — queuing next');
        queueNext();
      }}
      const d = await (await fetch('/status/' + taskId)).json();
      if (d.status === 'done') {{
        clearInterval(poll);
        log('Stream done at ' + Math.round(audio.currentTime) + 's played');
        // Do NOT generate next song here — wait for audio.onended to avoid wasting credits.
        // If 90s trigger already fired, next song is already being generated.
        if (audio.ended) await switchToNext();
        else audio.onended = () => switchToNext();
      }}
    }} catch(e) {{}}
  }}, 3000);

  audio.onended = () => {{ clearInterval(poll); queueNext().then(() => switchToNext()); }};
  audio.onerror = () => {{ log('Audio error'); clearInterval(poll); }};
}}

async function startStream() {{
  stopped = false;
  $('stopBtn').disabled = false;
  setStatus('Generating first song…');
  log('Starting');
  try {{
    currentTaskId = await apiGenerate();
    log('Task ' + currentTaskId);
    setStatus('Waiting for audio…');
    const ready = await waitReady(currentTaskId);
    if (!ready || stopped) {{ stopStream(); return; }}
    playTask(currentTaskId, 'audio1');
    showMetadata(currentTaskId);
  }} catch(e) {{
    log('Error: ' + e.message);
    stopStream();
  }}
}}

async function stopStream() {{
  stopped = true;
  $('stopBtn').disabled = true;
  setStatus('Stopped.');
  ['audio1','audio2'].forEach(id => {{
    const a = $(id);
    a.pause(); a.src = '';
    a.style.display = id === 'audio1' ? 'block' : 'none';
  }});
  const ids = [currentTaskId, nextTaskId].filter(Boolean);
  if (ids.length) {{
    await fetch('/stop', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{task_ids: ids}}),
    }}).catch(() => {{}});
  }}
  currentTaskId = null; nextTaskId = null;
  log('Stopped.');
}}

window.addEventListener('beforeunload', () => {{
  const ids = [currentTaskId, nextTaskId].filter(Boolean);
  if (ids.length) navigator.sendBeacon('/stop', JSON.stringify({{task_ids: ids}}));
}});

window.addEventListener('DOMContentLoaded', startStream);
</script>
</body>
</html>"""


def _library_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sonauto Library</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #0d0d0d; color: #ddd;
         padding: 20px; max-width: 640px; margin: 0 auto; }
  h1 { color: #e94560; margin-bottom: 18px; font-size: 1.3em; letter-spacing: 1px; }
  .player-card { background: #1a1a2e; border-radius: 12px; padding: 20px; margin-bottom: 18px; }
  .np-title  { font-size: 15px; font-weight: bold; color: #e94560; margin-bottom: 4px; min-height: 20px; }
  .np-prompt { font-size: 12px; color: #555; margin-bottom: 10px; min-height: 16px; font-style: italic; }
  .np-tags   { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; min-height: 20px; }
  .tag { background: #2a2a3e; border-radius: 4px; padding: 2px 8px; font-size: 11px; color: #aaa; }
  audio { width: 100%; border-radius: 6px; margin-bottom: 10px; }
  .controls { display: flex; gap: 8px; }
  .controls button { flex: 1; padding: 9px; border: none; border-radius: 6px;
                     background: #2a2a3e; color: #ddd; font-size: 13px; cursor: pointer; }
  .controls button:hover { background: #3a3a4e; }
  .library h2 { color: #555; font-size: 12px; text-transform: uppercase;
                letter-spacing: 1px; margin-bottom: 10px; }
  .song { background: #1a1a2e; border-radius: 8px; padding: 11px 14px; margin-bottom: 6px;
          cursor: pointer; display: flex; align-items: center; gap: 12px; }
  .song:hover { background: #222236; }
  .song.playing { border: 1px solid #e94560; }
  .song .idx { color: #444; font-size: 12px; min-width: 22px; text-align: right; }
  .song .info .title { font-size: 13px; color: #ddd; }
  .song .info .sub   { font-size: 11px; color: #555; margin-top: 2px; }
  #status { font-size: 12px; color: #555; margin-bottom: 14px; }
  a.new-stream { display: inline-block; margin-bottom: 16px; color: #e94560;
                 font-size: 13px; text-decoration: none; }
  a.new-stream:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>♪ MuseStream Library</h1>
<a class="new-stream" href="/context-ui">+ New stream from context</a>

<div class="player-card">
  <div class="np-title"  id="npTitle">Select a song</div>
  <div class="np-prompt" id="npPrompt"></div>
  <div class="np-tags"   id="npTags"></div>
  <audio id="audio" controls></audio>
  <div class="controls">
    <button onclick="prev()">&#9664; Prev</button>
    <button onclick="next()">Next &#9654;</button>
    <button onclick="shufflePlay()">&#x1F500; Shuffle</button>
  </div>
</div>

<div id="status">Loading…</div>
<div class="library">
  <h2 id="libLabel"></h2>
  <div id="songList"></div>
</div>

<script>
let songs = [], currentIdx = -1;
const audio = document.getElementById('audio');

async function load() {
  const d = await (await fetch('/library')).json();
  songs = d.songs;
  document.getElementById('status').textContent = '';
  document.getElementById('libLabel').textContent = songs.length + ' saved songs';
  render();
}

function render() {
  document.getElementById('songList').innerHTML = songs.map((s, i) =>
    `<div class="song${i===currentIdx?' playing':''}" id="s${i}" onclick="play(${i})">
      <span class="idx">${i+1}</span>
      <div class="info">
        <div class="title">${s.title || s.filename}</div>
        <div class="sub">${(s.tags||[]).slice(0,4).join(' · ') || s.prompt.slice(0,60)}</div>
      </div>
    </div>`).join('');
}

function play(idx) {
  currentIdx = idx;
  const s = songs[idx];
  audio.src = '/files/' + s.filename;
  audio.play();
  document.getElementById('npTitle').textContent  = s.title || s.filename;
  document.getElementById('npPrompt').textContent = s.prompt;
  document.getElementById('npTags').innerHTML = (s.tags||[]).map(t=>`<span class="tag">${t}</span>`).join('');
  render();
}

function next() { if (songs.length) play((currentIdx + 1) % songs.length); }
function prev() { if (songs.length) play((currentIdx - 1 + songs.length) % songs.length); }
function shufflePlay() {
  if (!songs.length) return;
  for (let i = songs.length-1; i > 0; i--) {
    const j = Math.floor(Math.random()*(i+1));
    [songs[i], songs[j]] = [songs[j], songs[i]];
  }
  currentIdx = -1;
  render();
  play(0);
}

audio.addEventListener('ended', next);
load();
</script>
</body>
</html>"""


def _context_ui_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Music Context</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #0d0d0d; color: #ddd;
         padding: 20px; max-width: 480px; margin: 0 auto; }
  h1 { color: #e94560; font-size: 1.2em; margin-bottom: 20px; }
  .field { margin-bottom: 14px; }
  label { display: block; font-size: 12px; color: #888; margin-bottom: 5px; }
  select, input[type=text] {
    width: 100%; padding: 10px 12px; background: #1a1a2e; border: 1px solid #2a2a3e;
    border-radius: 8px; color: #ddd; font-size: 15px; appearance: none; }
  select:focus, input:focus { outline: none; border-color: #e94560; }
  .row { display: flex; gap: 10px; }
  .row .field { flex: 1; }
  #goBtn { width: 100%; padding: 14px; background: #e94560; color: #fff; border: none;
           border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;
           margin-top: 6px; }
  #goBtn:disabled { opacity: .5; cursor: default; }
  #result { margin-top: 20px; padding: 14px; background: #1a1a2e; border-radius: 8px;
            display: none; }
  #result .prompt-text { color: #aaa; font-size: 13px; margin-bottom: 14px;
                          font-style: italic; line-height: 1.6; }
  #openBtn { display: block; width: 100%; padding: 12px; background: #27ae60;
             color: #fff; border: none; border-radius: 8px; font-size: 15px;
             font-weight: bold; cursor: pointer; text-align: center; }
  #status { margin-top: 10px; font-size: 13px; color: #888; text-align: center; }
  .section-title { font-size: 11px; color: #555; text-transform: uppercase;
                   letter-spacing: 1px; margin: 18px 0 10px; }
</style>
</head>
<body>
<h1>♪ Music Context</h1>

<div class="section-title">Situation</div>
<div class="row">
  <div class="field">
    <label>Activity</label>
    <select id="activity">
      <option value="">—</option>
      <option>driving</option>
      <option>working</option>
      <option>working out</option>
      <option>running</option>
      <option>relaxing</option>
      <option>studying</option>
      <option>cooking</option>
      <option>party</option>
      <option>walking</option>
    </select>
  </div>
  <div class="field">
    <label>Mood</label>
    <select id="mood">
      <option value="">—</option>
      <option>happy</option>
      <option>excited</option>
      <option>focused</option>
      <option>tired</option>
      <option>relaxed</option>
      <option>sad</option>
      <option>anxious</option>
      <option>romantic</option>
      <option>angry</option>
    </select>
  </div>
</div>

<div class="section-title">Environment</div>
<div class="row">
  <div class="field">
    <label>Weather</label>
    <select id="weather">
      <option value="">—</option>
      <option>sunny and clear</option>
      <option>cloudy</option>
      <option>rainy</option>
      <option>stormy</option>
      <option>snowy</option>
      <option>foggy</option>
      <option>hot</option>
      <option>cold</option>
    </select>
  </div>
  <div class="field">
    <label>Time of day</label>
    <select id="time">
      <option value="">Auto-detect</option>
      <option>early morning</option>
      <option>morning</option>
      <option>afternoon</option>
      <option>evening</option>
      <option>late night</option>
    </select>
  </div>
</div>

<div class="section-title">Driving (optional)</div>
<div class="row">
  <div class="field">
    <label>Traffic</label>
    <select id="traffic">
      <option value="">—</option>
      <option>light</option>
      <option>moderate</option>
      <option>heavy</option>
      <option>standstill</option>
    </select>
  </div>
  <div class="field">
    <label>Destination</label>
    <input type="text" id="destination" placeholder="office, gym, home…">
  </div>
</div>

<div class="section-title">Schedule & Notes</div>
<div class="field">
  <label>Next event / schedule hint</label>
  <input type="text" id="schedule" placeholder="meeting in 30 min, free afternoon…">
</div>
<div class="field">
  <label>Extra notes</label>
  <input type="text" id="notes" placeholder="anything else…">
</div>

<button id="goBtn" onclick="generate()">Generate Music</button>
<div id="status"></div>

<div id="result">
  <div class="prompt-text" id="promptText"></div>
  <button id="openBtn" onclick="openPlayer()">Open Player</button>
</div>

<script>
let playerUrl = null;

function val(id) { return document.getElementById(id).value.trim(); }
function setStatus(msg) { document.getElementById('status').textContent = msg; }

async function generate() {
  const ctx = {};
  ['activity','mood','weather','time','traffic','destination','schedule','notes']
    .forEach(k => { if (val(k)) ctx[k] = val(k); });

  if (Object.keys(ctx).length === 0) {
    setStatus('Please fill in at least one field.'); return;
  }

  document.getElementById('goBtn').disabled = true;
  document.getElementById('result').style.display = 'none';
  setStatus('Generating prompt…');

  try {
    const r = await fetch('/api/context', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(ctx),
    });
    const d = await r.json();
    if (d.error) throw new Error(d.error);

    playerUrl = d.url;
    document.getElementById('promptText').textContent = '\\u201c' + d.prompt + '\\u201d';
    document.getElementById('result').style.display = 'block';
    setStatus('');
  } catch(e) {
    setStatus('Error: ' + e.message);
  } finally {
    document.getElementById('goBtn').disabled = false;
  }
}

function openPlayer() {
  if (playerUrl) window.location.href = playerUrl;
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    print(f"MuseStream — provider: {_P['name']} | port: {PORT}")
    print(f"  Output : {OUTPUT_DIR}")
    print(f"  Log    : {LOG_FILE}")
    print(f"  Access : http://localhost:{PORT}")
    if not API_KEY:
        print(f"  WARNING: {_P['key_env']} not set — register at {_P['register_url']}")
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
