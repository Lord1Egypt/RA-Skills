#!/usr/bin/env python3
"""
douyin-dubber pipeline:
  1. Download video from Douyin (Playwright + cookie)
  2. Transcribe audio with Whisper → SRT
  3. Translate SRT with LLM (agent writes translated.json)
  4. TTS each line with edge-tts (hard mode: stretch to fit timestamp)
  5. Mix: lower original audio to 10%, add TTS track
  6. Burn text overlay box (yellow) hiding original subs
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────── constants ──
FFMPEG  = shutil.which("ffmpeg") or "ffmpeg"
# Prefer whisper from PATH, fallback to python -m whisper
WHISPER = shutil.which("whisper") or None
# Python executable for Playwright subprocess
PYTHON311 = shutil.which("python") or sys.executable

# ── Douyin cookie file (cookie string format) ─────────────────────────
# Default: cookie file next to this script → skills/douyin-dubber/douyin_cookies.txt
DOUYIN_COOKIE_FILE = Path(os.environ.get(
    "DOUYIN_COOKIE_FILE",
    Path(__file__).parent.parent / "douyin_cookies.txt"
))

# ══════════════════════════════════════════════════ PROGRESS REPORTER ══
class ProgressReporter:
    """
    Báo cáo tiến trình mỗi 5 giây.
    Gồm: bước hiện tại, % hoàn thành, thời gian đã chạy, ETA.
    """
    STEPS = [
        ("download",   "📥 Tải video"),
        ("transcribe", "🎙️  Whisper transcribe"),
        ("translate",  "🌐 Dịch thuật"),
        ("tts_4a",     "🔊 [4a] Render raw TTS"),
        ("tts_4b",     "🔊 [4b] Stretch clips"),
        ("tts_4c",     "🔊 [4c] Silence track"),
        ("tts_4d",     "🔊 [4d] Mix TTS track"),
        ("mix",        "🎞️  Ghép video + subtitle"),
        ("done",       "✅ Hoàn tất"),
    ]
    # Trọng số thời gian ước tính (tổng = 100)
    WEIGHT = {
        "download":   15,
        "transcribe": 30,
        "translate":  10,
        "tts_4a":     15,
        "tts_4b":      5,
        "tts_4c":      2,
        "tts_4d":      3,
        "mix":        20,
        "done":        0,
    }

    def __init__(self, interval: float = 5.0):
        self.interval   = interval
        self.step_key   = "download"
        self.step_label = self.STEPS[0][1]
        self.sub_msg    = ""
        self.sub_pct    = 0.0   # 0–100 within current step
        self.start_time = time.time()
        self._step_start: dict[str, float] = {}
        self._step_done:  dict[str, float] = {}
        self._lock       = threading.Lock()
        self._stop       = threading.Event()
        self._thread     = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()

    def set_step(self, key: str, sub: str = ""):
        with self._lock:
            self._step_start[key] = time.time()
            self.step_key   = key
            self.step_label = dict(self.STEPS).get(key, key)
            self.sub_msg    = sub
            self.sub_pct    = 0.0

    def update(self, sub: str = "", pct: float = None):
        with self._lock:
            if sub:
                self.sub_msg = sub
            if pct is not None:
                self.sub_pct = min(max(float(pct), 0.0), 100.0)

    def _overall_pct(self) -> float:
        step_keys   = [s[0] for s in self.STEPS[:-1]]
        current_idx = step_keys.index(self.step_key) if self.step_key in step_keys else 0
        done_weight = sum(self.WEIGHT[k] for k in step_keys[:current_idx])
        cur_weight  = self.WEIGHT.get(self.step_key, 0) * (self.sub_pct / 100.0)
        return min(done_weight + cur_weight, 100.0)

    def _eta_str(self, overall_pct: float) -> str:
        elapsed = time.time() - self.start_time
        if overall_pct <= 1.0:
            return "đang ước tính…"
        total_est = elapsed / (overall_pct / 100.0)
        remaining = total_est - elapsed
        if remaining < 0:
            remaining = 0
        return str(timedelta(seconds=int(remaining)))

    def _bar(self, pct: float, width: int = 20) -> str:
        filled = int(width * pct / 100)
        return "█" * filled + "░" * (width - filled)

    def _loop(self):
        while not self._stop.is_set():
            try:
                self._print_status()
            except Exception:
                pass
            self._stop.wait(self.interval)

    def _print_status(self):
        with self._lock:
            elapsed  = time.time() - self.start_time
            overall  = self._overall_pct()
            eta      = self._eta_str(overall)
            bar      = self._bar(overall)
            ts       = datetime.now().strftime("%H:%M:%S")
            sub      = f"  | {self.sub_msg}" if self.sub_msg else ""
            elapsed_str = str(timedelta(seconds=int(elapsed)))

        msg = (
            f"\n+-- [{ts}] TIEN TRINH -----------------------------\n"
            f"|  Buoc    : {self.step_label}\n"
            f"|  Tong    : [{bar}] {overall:5.1f}%\n"
            f"|  Da chay : {elapsed_str}\n"
            f"|  ETA     : {eta}{sub}\n"
            f"+--------------------------------------------------"
        )
        try:
            print(msg, flush=True)
        except Exception:
            pass

    def done(self):
        self._stop.set()
        elapsed = time.time() - self.start_time
        elapsed_str = str(timedelta(seconds=int(elapsed)))
        msg = (
            f"\n+==================================================+\n"
            f"|  HOAN TAT!  Tong thoi gian: {elapsed_str:<20}|\n"
            f"+==================================================+"
        )
        try:
            print(msg, flush=True)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────── helpers ──
def run(cmd, progress: ProgressReporter = None, sub: str = "", **kw):
    """Run subprocess, optionally update progress sub-message."""
    if progress and sub:
        progress.update(sub=sub)
    print(f"[CMD] {' '.join(str(c) for c in cmd)}", flush=True)
    result = subprocess.run(cmd, check=True, **kw)
    return result


def _parse_cookie_string(cookie_str: str) -> list[dict]:
    """Parse cookie string (key=val; key2=val2) -> list of Playwright cookie dicts."""
    cookies = []
    for part in cookie_str.split(';'):
        part = part.strip()
        if '=' not in part:
            continue
        name, _, value = part.partition('=')
        name = name.strip()
        value = value.strip()
        if not name:
            continue
        cookies.append({
            'name': name, 'value': value,
            'domain': '.douyin.com', 'path': '/',
            'secure': True, 'httpOnly': False, 'sameSite': 'Lax',
        })
    return cookies


def download_with_playwright(url: str, out_path, cookie_file=None, progress=None):
    """
    Tai video Douyin qua Playwright Chromium + cookie string.
    1. Load page -> intercept network response -> bat video CDN URL
    2. Download file MP4 ve out_path
    Returns True neu thanh cong.
    """
    import urllib.request as _r

    # Doc cookie tu file hoac bien moi truong
    cookie_str = ""
    cf = cookie_file or DOUYIN_COOKIE_FILE
    if Path(str(cf)).exists():
        cookie_str = Path(str(cf)).read_text(encoding='utf-8', errors='replace').strip()
    if not cookie_str:
        print("[PW] Khong co cookie file - thu khong co cookie...", flush=True)

    # Chay sub-process Python311 de chay Playwright (tranh conflict event loop)
    pw_script = Path(__file__).parent / "pw_capture.py"
    if not pw_script.exists():
        # Viet script tam thoi
        pw_script = Path(tempfile.mktemp(suffix=".py"))

    pw_code = r'''
import asyncio, sys, json
from playwright.async_api import async_playwright

url = sys.argv[1]
cookie_str = sys.argv[2] if len(sys.argv) > 2 else ""

CDN_HOSTS = ['zjcdn.com','douyinvod.com','bytecdn.com','volces.com','iesdouyin.com','amemv.com']

def parse_cookies(s):
    out = []
    for p in s.split(';'):
        p = p.strip()
        if '=' not in p: continue
        n, _, v = p.partition('=')
        n = n.strip(); v = v.strip()
        if not n: continue
        out.append({'name':n,'value':v,'domain':'.douyin.com','path':'/','secure':True,'httpOnly':False,'sameSite':'Lax'})
    return out

async def main():
    video_urls = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        if cookie_str:
            await ctx.add_cookies(parse_cookies(cookie_str))
        async def on_response(resp):
            u = resp.url
            ct = resp.headers.get('content-type','')
            if 'video/mp4' in ct and any(h in u for h in CDN_HOSTS):
                video_urls.append(u)
        page = await ctx.new_page()
        page.on('response', on_response)
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=25000)
        except Exception:
            pass
        await asyncio.sleep(10)
        await browser.close()
    print(json.dumps({"urls": video_urls}))

asyncio.run(main())
'''
    pw_script.write_text(pw_code, encoding='utf-8')

    print(f"[PW] Bat video URL tu: {url}", flush=True)
    if progress: progress.update(sub="Playwright: dang load trang...", pct=5)

    try:
        result = subprocess.run(
            [PYTHON311, str(pw_script), url, cookie_str],
            capture_output=True, timeout=60,
            env={**os.environ, "PYTHONUTF8": "1"}
        )
        stdout = (result.stdout or b"").decode("utf-8", errors="replace").strip()
        stderr = (result.stderr or b"").decode("utf-8", errors="replace")
        if result.returncode != 0:
            print(f"[PW] Loi: {stderr[:300]}", flush=True)
            return False
        # Tim dong JSON cuoi
        json_line = ""
        for line in reversed(stdout.splitlines()):
            if line.strip().startswith('{"urls"'):
                json_line = line.strip()
                break
        if not json_line:
            print(f"[PW] Khong co JSON output\n{stdout[:300]}", flush=True)
            return False
        data = json.loads(json_line)
        video_urls = data.get("urls", [])
    except subprocess.TimeoutExpired:
        print("[PW] Timeout!", flush=True)
        return False
    except Exception as e:
        print(f"[PW] Exception: {e}", flush=True)
        return False

    if not video_urls:
        print("[PW] Khong tim thay video URL tren trang", flush=True)
        return False

    video_url = video_urls[0]
    print(f"[PW] Tai: {video_url[:100]}...", flush=True)
    if progress: progress.update(sub="Playwright: dang tai video...", pct=15)

    req = _r.Request(video_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    req.add_header("Referer", "https://www.douyin.com/")
    req.add_header("Accept", "*/*")
    try:
        with _r.urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            done = 0
            with open(out_path, "wb") as f:
                while True:
                    buf = resp.read(256 * 1024)
                    if not buf: break
                    f.write(buf)
                    done += len(buf)
                    if total and progress:
                        mb = done / 1024 / 1024
                        pct = 15 + (done / total) * 80
                        progress.update(sub=f"Playwright: {mb:.1f}/{total/1024/1024:.1f}MB", pct=pct)
    except Exception as e:
        print(f"[PW] Loi tai file: {e}", flush=True)
        return False

    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"[PW] Xong: {out_path} ({out_path.stat().st_size/1024/1024:.1f}MB)", flush=True)
        if progress: progress.update(sub="Playwright: xong!", pct=100)
        return True
    return False


def srt_to_segments(srt_path: Path) -> list[dict]:
    text   = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", text.strip())
    segments = []
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        idx   = lines[0].strip()
        times = lines[1].strip()
        txt   = " ".join(l.strip() for l in lines[2:])
        m = re.match(
            r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)",
            times,
        )
        if not m:
            continue
        def to_s(h, mi, s, ms):
            return int(h)*3600 + int(mi)*60 + int(s) + int(ms)/1000
        start_s = to_s(*m.group(1, 2, 3, 4))
        end_s   = to_s(*m.group(5, 6, 7, 8))
        segments.append({"index": idx, "start_s": start_s, "end_s": end_s, "text": txt})
    return segments


def segments_to_srt(segments: list[dict], path: Path):
    lines = []
    for seg in segments:
        def fmt(s):
            h = int(s // 3600); mi = int((s % 3600) // 60); sec = s % 60
            return f"{h:02d}:{mi:02d}:{sec:06.3f}".replace(".", ",")
        lines.append(seg["index"])
        lines.append(f"{fmt(seg['start_s'])} --> {fmt(seg['end_s'])}")
        lines.append(seg["text"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ───────────────────────────────────────────────────────── translate ──
def translate_segments(segments: list[dict], target_lang: str,
                       progress: ProgressReporter) -> list[dict]:
    # Thêm duration_s vào payload để AI biết thời lượng mỗi segment
    payload = [
        {
            "index": s["index"],
            "duration_s": round(s["end_s"] - s["start_s"], 2),
            "text": s["text"]
        }
        for s in segments
    ]
    prompt  = textwrap.dedent(f"""
        Translate the following subtitle segments to {target_lang}.
        Keep line count identical. Return ONLY valid JSON array in same structure.
        Each object: {{"index": "...", "text": "translated text"}}

        IMPORTANT — Fit translation to duration:
        Each segment has a "duration_s" field (seconds available for TTS playback).
        A TTS voice reads approximately 3–4 syllables per second in {target_lang}.
        If your translation is too long to be read naturally within duration_s,
        SHORTEN it (remove filler words, condense meaning) so it fits comfortably.
        Never sacrifice core meaning — prefer shorter natural phrasing over word-for-word.
        Do NOT include duration_s in your output JSON.

        Input:
        {json.dumps(payload, ensure_ascii=False, indent=2)}
    """).strip()

    prompt_file = Path(tempfile.gettempdir()) / "dubber_translate_prompt.txt"
    result_file = Path(tempfile.gettempdir()) / "dubber_translated.json"
    prompt_file.write_text(prompt, encoding="utf-8")
    result_file.unlink(missing_ok=True)

    print(f"\n[TRANSLATE] Prompt → {prompt_file}", flush=True)
    print(f"[TRANSLATE] Chờ agent dịch và ghi → {result_file}", flush=True)
    progress.update(sub=f"Chờ agent dịch {len(segments)} dòng sub…", pct=5)

    for i in range(300):
        if result_file.exists():
            break
        # Update pct (tối đa 90% trong lúc chờ)
        wait_pct = min(5 + i * 0.28, 90)
        progress.update(pct=wait_pct)
        time.sleep(1)

    if not result_file.exists():
        raise TimeoutError("Không nhận được kết quả dịch sau 5 phút.")

    progress.update(sub="Đã nhận kết quả dịch, đang áp dụng…", pct=95)
    translated = json.loads(result_file.read_text(encoding="utf-8"))
    lookup = {str(t["index"]): t["text"] for t in translated}
    for seg in segments:
        if str(seg["index"]) in lookup:
            seg["text"] = lookup[str(seg["index"])]
    progress.update(pct=100)
    return segments


# ─────────────────────────────────────── TTS PROVIDER SELECTION ──

GTTS_LANG_MAP = {
    "Vietnamese": "vi", "English": "en", "Chinese": "zh-CN",
    "Japanese": "ja", "Korean": "ko", "Thai": "th",
    "French": "fr", "German": "de", "Spanish": "es",
}

ELEVENLABS_VOICES_VI = {
    "Rachel (Nữ - tự nhiên)":     "21m00Tcm4TlvDq8ikWAM",
    "Bella (Nữ - nhẹ nhàng)":     "EXAVITQu4vr4xnSDxMaL",
    "Antoni (Nam - trầm ấm)":     "ErXwobaYiN019PkySvjV",
    "Josh (Nam - rõ ràng)":       "TxGEqnHWrfWFTfGW9XjX",
    "Arnold (Nam - mạnh mẽ)":     "VR6AewLTigWG4xSOukaG",
    "Elli (Nữ - trẻ trung)":      "MF3mGyEYCl7XYWbV9V6O",
}

def ask_tts_provider(lang: str) -> dict:
    """
    Hỏi người dùng chọn provider TTS khi bắt đầu pipeline.
    Returns dict: { "provider": "gtts"|"elevenlabs"|"edge", "voice": ..., "api_key": ... }
    """
    print("\n" + "═"*55)
    print("  🔊 CHỌN GIỌNG ĐỌC (TTS PROVIDER)")
    print("═"*55)
    print()
    print("  1️⃣   gTTS  (Google TTS)")
    print("       ✅ Miễn phí hoàn toàn, không cần API key")
    print("       ⚠️  Giọng hơi robot, không điều chỉnh được")
    print()
    print("  2️⃣   ElevenLabs")
    print("       ✅ Giọng AI cực tự nhiên, nhiều lựa chọn")
    print("       ✅ Free tier: 10,000 ký tự/tháng")
    print("       ⚠️  Cần API key (đăng ký tại elevenlabs.io)")
    print()
    print("  3️⃣   Edge TTS  (Microsoft Neural)")
    print("       ✅ Giọng tự nhiên, miễn phí")
    print("       ⚠️  Hay bị rate limit khi dùng nhiều")
    print()

    while True:
        choice = input("  👉 Nhập 1, 2 hoặc 3 (mặc định = 1): ").strip() or "1"
        if choice in ("1", "2", "3"):
            break
        print("  ❌ Vui lòng nhập 1, 2 hoặc 3")

    if choice == "1":
        gtts_lang = GTTS_LANG_MAP.get(lang, "vi")
        print(f"\n  ✅ Dùng gTTS — ngôn ngữ: {gtts_lang}")
        return {"provider": "gtts", "voice": gtts_lang, "api_key": None}

    elif choice == "2":
        print("\n  📋 Các giọng ElevenLabs phổ biến:")
        voice_list = list(ELEVENLABS_VOICES_VI.items())
        for i, (name, vid) in enumerate(voice_list, 1):
            print(f"     {i}. {name}")
        print(f"     {len(voice_list)+1}. Nhập Voice ID tùy chỉnh")
        while True:
            v = input(f"  👉 Chọn giọng (mặc định = 1): ").strip() or "1"
            if v.isdigit() and 1 <= int(v) <= len(voice_list)+1:
                break
            print("  ❌ Lựa chọn không hợp lệ")
        v = int(v)
        if v <= len(voice_list):
            vname, voice_id = voice_list[v-1]
        else:
            voice_id = input("  👉 Nhập Voice ID: ").strip()
            vname = "Custom"
        api_key = input("  🔑 Nhập ElevenLabs API key: ").strip()
        if not api_key:
            print("  ❌ Cần API key cho ElevenLabs. Chuyển sang gTTS.")
            gtts_lang = GTTS_LANG_MAP.get(lang, "vi")
            return {"provider": "gtts", "voice": gtts_lang, "api_key": None}

        # Model (mặc định eleven_multilingual_v2)
        print("\n  📋 ElevenLabs Model:")
        print("     1. eleven_multilingual_v2  (mặc định, đa ngôn ngữ)")
        print("     2. eleven_turbo_v2_5       (nhanh hơn, chất lượng cao)")
        print("     3. eleven_flash_v2_5       (nhanh nhất, tiết kiệm credits)")
        m = input("  👉 Chọn model (mặc định = 1): ").strip() or "1"
        model_map = {
            "1": "eleven_multilingual_v2",
            "2": "eleven_turbo_v2_5",
            "3": "eleven_flash_v2_5",
        }
        el_model = model_map.get(m, "eleven_multilingual_v2")

        # Stability (0.0 - 1.0)
        stab_raw = input("  🎚️  Stability 0-100% (mặc định = 50): ").strip() or "50"
        try:
            el_stability = min(max(float(stab_raw), 0), 100) / 100
        except ValueError:
            el_stability = 0.5

        # Language override
        lang_raw = input("  🌐 Language code override (Enter để bỏ qua, vd: vi, en, zh): ").strip()
        el_language = lang_raw if lang_raw else None

        print(f"\n  ✅ Dùng ElevenLabs — giọng: {vname} | model: {el_model} | stability: {el_stability:.0%}")
        return {
            "provider": "elevenlabs",
            "voice": voice_id,
            "api_key": api_key,
            "el_model": el_model,
            "el_stability": el_stability,
            "el_language": el_language,
        }

    else:  # Edge TTS
        print("\n  📋 Giọng Edge TTS tiếng Việt:")
        print("     1. vi-VN-HoaiMyNeural  (Nữ - giọng Bắc)")
        print("     2. vi-VN-NamMinhNeural (Nam - giọng Bắc)")
        v = input("  👉 Chọn (mặc định = 1): ").strip() or "1"
        voice = "vi-VN-HoaiMyNeural" if v != "2" else "vi-VN-NamMinhNeural"
        print(f"\n  ✅ Dùng Edge TTS — giọng: {voice}")
        return {"provider": "edge", "voice": voice, "api_key": None}


# ────────────────────────────────────────────────── TTS BACKENDS ──

def _tts_gtts(text: str, lang: str, out_path: Path):
    """Google TTS — free, stable, không bị rate limit."""
    from gtts import gTTS
    import unicodedata, time as _time
    text_clean = unicodedata.normalize("NFC", text).strip() or "..."
    for attempt in range(3):
        try:
            gTTS(text_clean, lang=lang).save(str(out_path))
            return
        except Exception as e:
            if attempt < 2:
                _time.sleep(1.5)
            else:
                raise RuntimeError(f"gTTS failed: {e}")


def _tts_elevenlabs(text: str, voice_id: str, api_key: str, out_path: Path,
                    model_id: str = "eleven_multilingual_v2",
                    stability: float = 0.5, similarity_boost: float = 0.75,
                    language_code: str = None):
    """ElevenLabs TTS — hỗ trợ model, stability, language_code tùy chỉnh."""
    import unicodedata, urllib.request, json as _json
    text_clean = unicodedata.normalize("NFC", text).strip() or "..."
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    body = {
        "text": text_clean,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    if language_code:
        body["language_code"] = language_code
    payload = _json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")
    with urllib.request.urlopen(req, timeout=30) as resp:
        out_path.write_bytes(resp.read())


def _tts_edge(text: str, voice: str, out_path: Path):
    """Edge TTS — subprocess per request + fake headers."""
    import unicodedata, time as _time, random, sys as _sys, textwrap as _tw
    text_clean = unicodedata.normalize("NFC", text).strip() or "..."
    script = _tw.dedent(f"""
import asyncio, edge_tts, random
_orig = edge_tts.Communicate.__init__
def _patch(self, text, voice, **kw):
    _orig(self, text, voice, **kw)
    self.headers = {{
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/124.0.0.0",
        "Origin": "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold",
    }}
edge_tts.Communicate.__init__ = _patch
async def main():
    c = edge_tts.Communicate({repr(text_clean)}, {repr(voice)})
    await c.save({repr(str(out_path))})
asyncio.run(main())
""")
    for attempt in range(5):
        # Delay tăng dần: lần 1 = 2-4s, retry = 5-10s để tránh rate limit
        delay = 2.0 + random.uniform(1.0, 2.0) if attempt == 0 else 5.0 + random.uniform(2.0, 5.0)
        _time.sleep(delay)
        r = subprocess.run([_sys.executable, "-c", script],
                           capture_output=True, text=True,
                           env={**os.environ, "PYTHONUTF8": "1"})
        if r.returncode == 0 and out_path.exists() and out_path.stat().st_size > 100:
            return
        print(f"[TTS/Edge] Retry {attempt+1}/5…")
    raise RuntimeError(f"Edge TTS failed after 5 attempts: {text_clean[:40]}")


def tts_segment(text: str, voice: str, out_path: Path,
                provider: str = "gtts", api_key: str = None,
                el_model: str = "eleven_multilingual_v2",
                el_stability: float = 0.5, el_language: str = None):
    """Route đến đúng TTS backend dựa theo provider."""
    if provider == "gtts":
        _tts_gtts(text, voice, out_path)
    elif provider == "elevenlabs":
        _tts_elevenlabs(text, voice, api_key, out_path,
                        model_id=el_model, stability=el_stability,
                        language_code=el_language)
    elif provider == "edge":
        _tts_edge(text, voice, out_path)
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")


def stretch_audio(src: Path, dst: Path, target_duration_s: float):
    """Stretch/compress audio to fit target_duration_s using FFmpeg atempo."""
    probe  = subprocess.run([FFMPEG, "-i", str(src), "-hide_banner"],
                            capture_output=True, text=True)
    dur_m  = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", probe.stderr)
    if not dur_m:
        shutil.copy(src, dst); return
    src_dur = (int(dur_m.group(1))*3600 + int(dur_m.group(2))*60 +
               int(dur_m.group(3)) + int(dur_m.group(4))/100)
    if src_dur <= 0:
        shutil.copy(src, dst); return

    ratio = src_dur / target_duration_s
    filters = []
    r = ratio
    while r > 2.0:  filters.append("atempo=2.0"); r /= 2.0
    while r < 0.5:  filters.append("atempo=0.5"); r *= 2.0
    filters.append(f"atempo={r:.4f}")
    subprocess.run(
        [FFMPEG, "-y", "-i", str(src), "-filter:a", ",".join(filters), str(dst)],
        check=True, capture_output=True
    )


def build_tts_track(segments: list[dict], voice: str, total_dur: float,
                    workdir: Path, progress: ProgressReporter,
                    provider: str = "gtts", api_key: str = None,
                    el_model: str = "eleven_multilingual_v2",
                    el_stability: float = 0.5, el_language: str = None) -> Path:
    """
    Bước 4 — Render TTS (4 bước nhỏ):
      4a. Render raw TTS audio cho từng segment
      4b. Stretch/compress từng clip cho khớp timestamp
      4c. Tạo silence base track
      4d. Mix tất cả segments vào 1 track hoàn chỉnh
    """
    tts_dir = workdir / "tts_segments"
    tts_dir.mkdir(exist_ok=True)
    active_segs = [s for s in segments if s["text"].strip()]
    total = len(active_segs)

    if not total:
        raise ValueError("Không có segment TTS nào được tạo.")

    # ── 4a. Render raw TTS ───────────────────────────────────────────
    print("\n[4a] Render raw TTS từng segment…", flush=True)
    progress.update(sub=f"[4a] Render TTS — 0/{total} segments…", pct=0)
    raw_files = {}
    for i, seg in enumerate(active_segs):
        raw_mp3 = tts_dir / f"{str(seg['index']).zfill(4)}_raw.mp3"
        tts_segment(seg["text"], voice, raw_mp3,
                    provider=provider, api_key=api_key,
                    el_model=el_model, el_stability=el_stability,
                    el_language=el_language)
        import time as _ttime; _ttime.sleep(0.3)
        raw_files[seg["index"]] = raw_mp3
        pct = ((i + 1) / total) * 40   # 4a chiếm 0–40%
        progress.update(sub=f"[4a] TTS {i+1}/{total}: {seg['text'][:35]}…", pct=pct)
    print(f"[4a] Xong — {total} file raw", flush=True)

    # ── 4b. Stretch/compress từng clip ──────────────────────────────
    print("\n[4b] Stretch audio cho khớp timestamp…", flush=True)
    progress.set_step("tts_4b", f"Stretch {total} clips…")
    progress.update(pct=0)
    parts = []
    for i, seg in enumerate(active_segs):
        raw_mp3   = raw_files[seg["index"]]
        stretched = tts_dir / f"{str(seg['index']).zfill(4)}_stretched.mp3"
        duration  = seg["end_s"] - seg["start_s"]
        if duration > 0.2:
            stretch_audio(raw_mp3, stretched, duration)
        else:
            shutil.copy(raw_mp3, stretched)
        parts.append((seg["start_s"], stretched))
        pct = ((i + 1) / total) * 95   # 4b chiếm 0–95%
        progress.update(sub=f"[4b] Stretch {i+1}/{total}…", pct=pct)
    print(f"[4b] Xong — tất cả clips đã stretch", flush=True)

    # ── 4c. Tạo silence base track ───────────────────────────────────
    print("\n[4c] Tạo silence base track…", flush=True)
    progress.set_step("tts_4c", "Tạo silence base…")
    progress.update(pct=0)
    silence = workdir / "silence.mp3"
    subprocess.run(
        [FFMPEG, "-y", "-f", "lavfi", "-i",
         f"anullsrc=r=44100:cl=stereo:d={total_dur+1}",
         "-acodec", "libmp3lame", "-q:a", "4", str(silence)],
        check=True, capture_output=True
    )
    print(f"[4c] Xong — silence: {silence}", flush=True)
    progress.update(sub="Silence xong!", pct=100)

    # ── 4d. Mix tất cả vào 1 track ───────────────────────────────────
    print("\n[4d] Mix tất cả segments → TTS track…", flush=True)
    progress.set_step("tts_4d", "Mix audio track…")
    progress.update(pct=5)

    inputs = ["-i", str(silence)]
    for _, f in parts:
        inputs += ["-i", str(f)]

    filter_parts = []
    for i, (start_s, _) in enumerate(parts):
        delay_ms = int(start_s * 1000)
        filter_parts.append(f"[{i+1}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    mix_inputs = "".join(f"[a{i}]" for i in range(len(parts)))
    filter_parts.append(
        f"[0:a]{mix_inputs}amix=inputs={len(parts)+1}:normalize=0[aout]"
    )

    tts_track = workdir / "tts_track.mp3"
    subprocess.run(
        [FFMPEG, "-y"] + inputs + [
            "-filter_complex", ";".join(filter_parts),
            "-map", "[aout]",
            "-acodec", "libmp3lame", "-q:a", "4",
            "-t", str(total_dur), str(tts_track)
        ],
        check=True, capture_output=True
    )
    progress.update(sub="TTS track hoàn tất!", pct=100)
    print(f"[4d] Xong — TTS track: {tts_track}", flush=True)
    return tts_track


# ─────────────────────────────────────────────────── overlay filter ──
FONT_FILE = "C\\:/Windows/Fonts/arial.ttf"
FONT_FILE_ABS = "C:/Windows/Fonts/arial.ttf"

# Vị trí sub gốc Douyin (detect từ frame analysis): 69–77% chiều cao
# Box overlay che đúng vùng đó + một chút margin
SUB_Y_START  = 0.67   # 67% chiều cao — top của box che
SUB_Y_END    = 0.79   # 79% chiều cao — bottom của box che
# Font size cho ASS (points, tính cho 1920px height)
ASS_FONT_SIZE = 52    # ~h/37, vừa phải


def _seconds_to_ass_time(s: float) -> str:
    """Convert seconds float → ASS timestamp H:MM:SS.cs"""
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"


def build_ass_subtitle(segments: list[dict], video_w: int, video_h: int,
                       ass_path: Path) -> Path:
    """
    Tạo file ASS subtitle với:
    - Vị trí đặt đúng vùng sub gốc (SUB_Y_START ~ SUB_Y_END)
    - Box nền vàng bo góc
    - Text wrap tự động (ASS tự wrap theo PlayResX)
    - Hỗ trợ Unicode/tiếng Việt đầy đủ
    """
    # Box coordinates in pixels
    box_top    = int(video_h * SUB_Y_START)
    box_bottom = int(video_h * SUB_Y_END)
    box_h      = box_bottom - box_top
    # Vertical position: bottom edge của box (ASS dùng MarginV từ bottom)
    margin_v   = video_h - box_bottom  # px từ bottom lên đến bottom-of-box
    margin_h   = 32                    # left/right margin

    # ASS header
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {video_w}",
        f"PlayResY: {video_h}",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,
        #         Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle,
        #         Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
        "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # PrimaryColour = &H00000000 (black text)
        # BackColour = &H1500D7FF (vàng #FFD700 với alpha ~85%, ASS format AABBGGRR)
        # BorderStyle=4 → box background, Alignment=2 → bottom-center
        f"Style: Default,Arial,{ASS_FONT_SIZE},&H00000000,&H000000FF,&H00FFFFFF,"
        f"&H1500D7FF,-1,0,0,0,100,100,0,0,4,10,0,2,{margin_h},{margin_h},{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for seg in segments:
        start = _seconds_to_ass_time(seg["start_s"])
        end   = _seconds_to_ass_time(seg["end_s"])
        # Escape ASS special chars
        text = seg["text"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    ass_path.write_text("\n".join(lines), encoding="utf-8-sig")
    return ass_path


def mix_video(video: Path, tts_track: Path, segments: list[dict],
              output: Path, original_vol: float, progress: ProgressReporter):
    """Mix video + TTS audio + ASS subtitle overlay."""
    progress.update(sub="Đang tạo ASS subtitle…", pct=5)

    # Detect video resolution
    probe = subprocess.run([FFMPEG, "-i", str(video), "-hide_banner"],
                           capture_output=True, text=True)
    w, h = 1080, 1920  # default dọc
    m = re.search(r"(\d{3,4})x(\d{3,4})", probe.stderr)
    if m:
        w, h = int(m.group(1)), int(m.group(2))

    ass_path = output.parent / "dubber_work" / "subtitle.ass"
    build_ass_subtitle(segments, w, h, ass_path)
    print(f"[OK] ASS subtitle: {ass_path}", flush=True)

    progress.update(sub="FFmpeg đang encode video cuối…", pct=10)

    # subtitles filter dùng ASS file — hỗ trợ Unicode, tự wrap, box nền
    ass_path_fwd = str(ass_path).replace("\\", "/").replace(":", "\\:")
    sub_filter = f"subtitles='{ass_path_fwd}':fontsdir='C\\:/Windows/Fonts'"

    subprocess.run([
        FFMPEG, "-y",
        "-i", str(video), "-i", str(tts_track),
        "-filter_complex",
        f"[0:v]{sub_filter}[vout];"
        f"[0:a]volume={original_vol}[orig];"
        f"[orig][1:a]amix=inputs=2:normalize=0[aout]",
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        str(output)
    ], check=True)
    progress.update(sub="Encode xong!", pct=100)


# ─────────────────────────────────────────────────────────── MAIN ──
def main():
    ap = argparse.ArgumentParser(description="Douyin Auto Dubber")
    ap.add_argument("url",               help="Douyin/TikTok video URL")
    ap.add_argument("--lang",            default="Vietnamese",          help="Ngôn ngữ đích")
    ap.add_argument("--voice",           default="vi-VN-HoaiMyNeural",  help="Edge-TTS voice ID")
    ap.add_argument("--whisper-model",   default="medium",              help="Whisper model")
    ap.add_argument("--outdir",          default=".",                   help="Output folder")
    ap.add_argument("--skip-download",   help="Dùng video có sẵn (bỏ qua bước tải)")
    ap.add_argument("--skip-transcribe", help="Dùng SRT có sẵn (bỏ qua Whisper)")
    ap.add_argument("--translated-srt",  help="Dùng SRT đã dịch (bỏ qua bước dịch)")
    ap.add_argument("--original-vol",    type=float, default=0.10,      help="Volume gốc (0–1)")
    ap.add_argument("--progress-interval", type=float, default=5.0,    help="Khoảng báo cáo (giây)")
    ap.add_argument("--cookies",         default=None,                  help="Cookies file cho yt-dlp")
    args = ap.parse_args()

    outdir  = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    workdir = outdir / "dubber_work"
    workdir.mkdir(exist_ok=True)

    # Khởi động progress reporter
    prog = ProgressReporter(interval=args.progress_interval)
    prog.start()

    try:
        # -- 0. Chon TTS provider (hoi nguoi dung) --------------------
        tts_config = ask_tts_provider(args.lang)
        tts_provider  = tts_config["provider"]
        tts_voice     = tts_config["voice"]
        tts_api_key   = tts_config["api_key"]
        tts_el_model  = tts_config.get("el_model", "eleven_multilingual_v2")
        tts_el_stab   = tts_config.get("el_stability", 0.5)
        tts_el_lang   = tts_config.get("el_language", None)

        if args.voice and tts_provider == "edge":
            tts_voice = args.voice

        print(f"\n[INFO] Provider: {tts_provider} | Voice: {tts_voice}\n")
        if args.skip_download:
            video_path = Path(args.skip_download)
            print(f"\n[SKIP] Video có sẵn: {video_path}", flush=True)
        else:
            prog.set_step("download", "Đang tải video…")
            video_path = workdir / "original.mp4"

            # Bước 1: Playwright + cookie (phương pháp chính, ổn định nhất)
            cookie_file = Path(args.cookies) if args.cookies else DOUYIN_COOKIE_FILE
            pw_ok = download_with_playwright(args.url, video_path, cookie_file=cookie_file, progress=prog)

            if not pw_ok:
                # Fallback: yt-dlp (backup)
                print("\n[DOWNLOAD] Playwright thất bại → thử yt-dlp…", flush=True)
                prog.update(sub="Fallback: yt-dlp đang tải…", pct=10)
                ytdlp_cmd = [YTDLP, "-o", str(video_path), "--merge-output-format", "mp4",
                     "--newline",
                     "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"]
                if args.cookies:
                    ytdlp_cmd += ["--cookies", args.cookies]
                ytdlp_cmd += [args.url]
                run(ytdlp_cmd, progress=prog, sub="yt-dlp đang tải…")

            candidates = list(workdir.glob("original*.mp4"))
            if candidates and not video_path.exists():
                video_path = candidates[0]
            prog.update(sub=f"Tải xong: {video_path.name}", pct=100)

        # Lấy thời lượng video
        probe   = subprocess.run([FFMPEG, "-i", str(video_path), "-hide_banner"],
                                 capture_output=True, text=True)
        dur_m   = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", probe.stderr)
        total_dur = 60.0
        if dur_m:
            total_dur = (int(dur_m.group(1))*3600 + int(dur_m.group(2))*60 +
                         int(dur_m.group(3)) + int(dur_m.group(4))/100)
        print(f"[INFO] Thời lượng video: {total_dur:.1f}s", flush=True)

        # ── 2. Whisper ─────────────────────────────────────────────────
        if args.skip_transcribe:
            srt_path = Path(args.skip_transcribe)
            print(f"\n[SKIP] SRT có sẵn: {srt_path}", flush=True)
        else:
            prog.set_step("transcribe", f"Chạy Whisper model={args.whisper_model}…")
            run([WHISPER, str(video_path),
                 "--model", args.whisper_model,
                 "--output_format", "srt",
                 "--output_dir", str(workdir)],
                progress=prog, sub="Whisper đang xử lý audio…")
            srt_candidates = list(workdir.glob("*.srt"))
            if not srt_candidates:
                raise FileNotFoundError("Whisper không tạo ra file SRT.")
            srt_path = srt_candidates[0]
            prog.update(sub=f"Whisper xong: {srt_path.name}", pct=100)

        segments = srt_to_segments(srt_path)
        print(f"[INFO] {len(segments)} segments", flush=True)

        # ── 3. Translate ───────────────────────────────────────────────
        if args.translated_srt:
            print(f"\n[SKIP] SRT đã dịch: {args.translated_srt}", flush=True)
            segments = srt_to_segments(Path(args.translated_srt))
        else:
            prog.set_step("translate", f"Đang dịch sang {args.lang}…")
            segments = translate_segments(segments, args.lang, prog)
            translated_srt = workdir / "translated.srt"
            segments_to_srt(segments, translated_srt)
            print(f"[OK] SRT đã dịch: {translated_srt}", flush=True)

        # ── 4. TTS ────────────────────────────────────────────────────
        prog.set_step("tts_4a", f"[4a] Render raw TTS ({tts_provider}: {tts_voice})…")
        tts_track = build_tts_track(segments, tts_voice, total_dur, workdir, prog,
                                    provider=tts_provider, api_key=tts_api_key,
                                    el_model=tts_el_model, el_stability=tts_el_stab,
                                    el_language=tts_el_lang)
        print(f"[OK] TTS track: {tts_track}", flush=True)

        # ── 5. Mix ────────────────────────────────────────────────────
        prog.set_step("mix", "Đang encode video cuối + burn subtitle overlay…")
        output_video = outdir / f"dubbed_{video_path.stem}.mp4"
        mix_video(video_path, tts_track, segments, output_video, args.original_vol, prog)

        prog.done()
        print(f"\n🎬 Output: {output_video}", flush=True)

    except Exception as e:
        prog.stop()
        print(f"\n❌ LỖI: {e}", flush=True)
        raise


if __name__ == "__main__":
    main()
