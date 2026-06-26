#!/usr/bin/env python3
"""
Cross-platform audio bridge for meeting-notes-skill.

Features:
- ASR transcription (installed engine first, then cloud/built-in fallback)
- TTS synthesis (built-in macOS / edge-tts / OpenAI fallback)
- Unified naming: <meeting-topic>-<YYYYMMDD-HHMMSS>.<ext>
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
import tempfile
import platform
import re
import shutil
import subprocess
import sys
import time
import threading
import urllib.error
import urllib.request
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILL_SLUG = SKILL_ROOT.name
WORKSPACE_ROOT = SKILL_ROOT.parent.parent if SKILL_ROOT.parent.name == "skills" else SKILL_ROOT.parent
DEFAULT_OUTPUT_DIR = WORKSPACE_ROOT / f"{SKILL_SLUG}-data"
PRIVATE_OUTPUT_DIR = Path.home() / "clawdhome_shared" / "private" / f"{SKILL_SLUG}-data"
PUBLIC_RESOURCE_DIR = Path.home() / "clawdhome_shared" / "public"
COMPRESSED_AUDIO_SUFFIXES = {".m4a", ".mp3", ".aac", ".mp4"}
FFMPEG_INSTALL_HINT = "brew install ffmpeg (or run: bash scripts/bootstrap_macos.sh)"


def ts_now() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def is_compressed_audio(path: Path) -> bool:
    return path.suffix.lower() in COMPRESSED_AUDIO_SUFFIXES


def print_first_run_notice_once() -> None:
    """
    Print a clear setup notice on first run so users know required deps.
    """
    state_dir = Path.home() / ".meeting-notes-skill"
    marker = state_dir / "first_run_notice_shown"
    if marker.exists():
        return

    print("=== meeting-notes-skill: first-run setup notice ===", file=sys.stderr)
    print("- This skill has NO plugin requirement.", file=sys.stderr)
    print("- Installed ASR engines are preferred by default; built-in ASR is fallback.", file=sys.stderr)
    print("- First run is HARD-GATED by dependency checks.", file=sys.stderr)
    print("- Required dependencies:", file=sys.stderr)
    print("  1) edge-tts (mandatory): python3 -m pip install edge-tts", file=sys.stderr)
    print("  2) ffmpeg (mandatory): brew install ffmpeg", file=sys.stderr)
    print("- Default local ASR dependency:", file=sys.stderr)
    print("  3) local Whisper (default): python3 -m pip install openai-whisper", file=sys.stderr)
    print("- One-click bootstrap (macOS): bash scripts/bootstrap_macos.sh", file=sys.stderr)
    print("- Required check: bash scripts/doctor.sh --strict", file=sys.stderr)
    print("===============================================", file=sys.stderr)

    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        marker.write_text(dt.datetime.now().isoformat(), encoding="utf-8")
    except Exception:
        # Non-fatal if the environment is read-only.
        pass


def safe_topic(topic: str) -> str:
    topic = topic.strip()
    topic = re.sub(r"[\\/:*?\"<>|]+", "-", topic)
    topic = re.sub(r"\s+", "-", topic)
    topic = re.sub(r"-{2,}", "-", topic).strip("-")
    return topic or "meeting"


def clean_tts_text(raw: str) -> str:
    """
    Normalize speaking text so special symbols are not read literally.
    """
    text = raw
    # Markdown links: [label](url) -> label
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    # Raw URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Control tags like [停顿1s], [加重], [放慢]
    text = re.sub(r"\[(停顿[^\]]*|加重|放慢|重读|语速[^\]]*)\]", "", text)
    # HTML/XML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove markdown bullets/headers/quotes prefix
    text = re.sub(r"^\s{0,3}(#{1,6}|\-|\*|\+|>+)\s*", "", text, flags=re.M)
    # Table separators and code markers
    text = text.replace("|", " ")
    text = text.replace("`", "")
    # Remove noisy symbols that are often spoken out
    text = re.sub(r"[_*~^=+\\/@$%&{}\[\]<>]", "", text)
    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_section(text: str, heading: str) -> str:
    # Match markdown heading blocks like "## 核心决议清单"
    pattern = rf"(?:^|\n)##\s*{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, text, flags=re.S)
    return m.group(1).strip() if m else ""


def _extract_numbered_items(section_text: str) -> list[str]:
    items = []
    for line in section_text.splitlines():
        mm = re.match(r"^\s*\d+\.\s*(.+?)\s*$", line)
        if mm:
            items.append(mm.group(1))
    return items


def _extract_bullet_items(section_text: str) -> list[str]:
    items = []
    for line in section_text.splitlines():
        mm = re.match(r"^\s*[-*]\s*(.+?)\s*$", line)
        if mm:
            items.append(mm.group(1))
    return items


def _extract_action_items(section_text: str) -> list[dict]:
    rows = [ln.strip() for ln in section_text.splitlines() if ln.strip().startswith("|")]
    parsed = []
    if len(rows) < 3:
        return parsed
    for row in rows[2:]:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) < 4:
            continue
        task, owner, due, note = cols[:4]
        if not any([task, owner, due, note]):
            continue
        parsed.append({"task": task, "owner": owner, "due": due, "note": note})
    return parsed


def build_spoken_script(minutes_text: str) -> str:
    """
    Build a focused briefing script from minutes.
    Prioritize: 核心决议 -> Action Items -> 风险提示
    """
    decisions_sec = _extract_section(minutes_text, "核心决议清单")
    action_sec = _extract_section(minutes_text, "Action Items")
    risk_sec = _extract_section(minutes_text, "风险提示")

    decisions = _extract_numbered_items(decisions_sec)[:3]
    actions = _extract_action_items(action_sec)[:3]
    risks = _extract_bullet_items(risk_sec)[:2]

    lines = []
    lines.append("各位好，下面用一分钟同步本次会议重点。")

    if decisions:
        lines.append(f"本次会议形成 {len(decisions)} 项核心决议。")
        for i, d in enumerate(decisions, start=1):
            lines.append(f"第{i}项，{d}。")
    else:
        lines.append("本次会议核心决议仍在整理中，请以会后确认版本为准。")

    if actions:
        lines.append(f"需要立即推进的待办共 {len(actions)} 项。")
        for i, a in enumerate(actions, start=1):
            owner = a["owner"] or "待指定"
            due = a["due"] or "待确认"
            lines.append(f"待办{i}，{a['task']}。负责人是{owner}，交付或截止为{due}。")
    else:
        lines.append("当前待办信息不完整，请补充负责人和截止日期。")

    if risks:
        lines.append("最后提示两项风险。")
        for r in risks:
            lines.append(f"{r}。")
    else:
        lines.append("当前主要风险是信息不完整导致执行偏差。")

    lines.append("以上是本次会议口播简报。")
    return "\n".join(lines)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def is_writable_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test = path / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def resolve_output_dir(user_outdir: str | None = None) -> Path:
    """
    Path policy:
    1) Prefer private shared dir.
    2) Then user/env/default fallbacks.
    3) Public dir is read-only for shared resources.
    """
    candidates: list[Path] = []
    candidates.append(PRIVATE_OUTPUT_DIR.expanduser().resolve())
    if user_outdir:
        candidates.append(Path(user_outdir).expanduser().resolve())
    env_out = os.getenv("MEETING_OUTPUT_DIR")
    if env_out:
        candidates.append(Path(env_out).expanduser().resolve())
    candidates.append(DEFAULT_OUTPUT_DIR)
    candidates.append(Path.cwd() / f"{SKILL_SLUG}-data")

    for c in candidates:
        if is_writable_dir(c):
            return c
    raise RuntimeError("no writable output directory found")


def run(cmd: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(cmd, check=False, text=True, capture_output=True, env=merged_env)


def print_install_steps(mode: str) -> None:
    is_macos = platform.system() == "Darwin"
    print("Install guide:", file=sys.stderr)
    print("- 0) Install mandatory dependency: python3 -m pip install edge-tts", file=sys.stderr)
    if mode == "asr":
        print("- 1) Enable Speech Recognition permission for the app/terminal", file=sys.stderr)
        if is_macos:
            print("- 2) Install ffmpeg for compressed audio: brew install ffmpeg", file=sys.stderr)
        else:
            print("- 2) Install ffmpeg: sudo apt-get install -y ffmpeg", file=sys.stderr)
        print("- 3) Install local ASR whisper (default): python3 -m pip install openai-whisper", file=sys.stderr)
    elif mode == "tts":
        print("- 1) Install mandatory dependency: python3 -m pip install edge-tts", file=sys.stderr)
        if is_macos:
            print("- 2) Optional: local TTS uses macOS say/afconvert (preinstalled on most macOS)", file=sys.stderr)
        if is_macos:
            print("- 3) Install mandatory dependency: brew install ffmpeg", file=sys.stderr)
        else:
            print("- 3) Install mandatory dependency: sudo apt-get install -y ffmpeg", file=sys.stderr)
    else:
        if is_macos:
            print("- Install ffmpeg: brew install ffmpeg", file=sys.stderr)
        else:
            print("- Install ffmpeg: sudo apt-get install -y ffmpeg", file=sys.stderr)
        print("- Install edge-tts: python3 -m pip install edge-tts", file=sys.stderr)
        print("- Install whisper (default local ASR): python3 -m pip install openai-whisper", file=sys.stderr)
    print("- Verify: bash scripts/doctor.sh --strict", file=sys.stderr)
    if platform.system() == "Darwin":
        print(f"- One-command setup: bash scripts/bootstrap_macos.sh --mode={mode}", file=sys.stderr)


def maybe_auto_install_deps(mode: str, enabled: bool) -> None:
    if not enabled:
        return
    if platform.system() != "Darwin":
        print("[auto-install] skipped: only supported on macOS", file=sys.stderr)
        return
    bootstrap = Path(__file__).resolve().parent / "bootstrap_macos.sh"
    if not bootstrap.exists():
        print(f"[auto-install] skipped: bootstrap script missing: {bootstrap}", file=sys.stderr)
        return
    cmd = ["bash", str(bootstrap), f"--mode={mode}"]
    if mode == "asr":
        cmd.append("--with-whisper")

    install_items = ["edge-tts", "ffmpeg"]
    if mode in {"asr", "all"}:
        install_items.append("openai-whisper (and tiny model)")
    print(
        "[auto-install] installing dependencies: " + ", ".join(install_items),
        file=sys.stderr,
    )
    print("[auto-install] please wait, this may take a few minutes...", file=sys.stderr)

    result: dict[str, subprocess.CompletedProcess] = {}

    def _runner() -> None:
        result["p"] = run(cmd)

    th = threading.Thread(target=_runner, daemon=True)
    th.start()
    heartbeat_sec = 8
    elapsed = 0
    while th.is_alive():
        time.sleep(heartbeat_sec)
        elapsed += heartbeat_sec
        print(
            f"[auto-install] still running ({elapsed}s): downloading/installing dependencies...",
            file=sys.stderr,
        )
    th.join()
    p = result.get("p")
    if not p:
        print("[auto-install] failed: no result returned from installer", file=sys.stderr)
        return
    out, err = p.stdout, p.stderr
    if out:
        print("[auto-install] " + out.strip().replace("\n", "\n[auto-install] "), file=sys.stderr)
    if err:
        print("[auto-install] " + err.strip().replace("\n", "\n[auto-install] "), file=sys.stderr)
    if p.returncode != 0:
        print(f"[auto-install] failed with code={p.returncode}", file=sys.stderr)


def print_first_run_env_check_once() -> None:
    state_dir = Path.home() / ".meeting-notes-skill"
    marker = state_dir / "first_run_env_check_shown"
    if marker.exists():
        return
    doctor = Path(__file__).resolve().parent / "doctor.sh"
    print("=== meeting-notes-skill: environment check ===", file=sys.stderr)
    if doctor.exists():
        p = run(["bash", str(doctor), "all"])
        if p.stdout:
            print(p.stdout.strip(), file=sys.stderr)
        if p.stderr:
            print(p.stderr.strip(), file=sys.stderr)
    else:
        print(f"[WARN] doctor.sh not found: {doctor}", file=sys.stderr)
    print("=== end environment check ===", file=sys.stderr)
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        marker.write_text(dt.datetime.now().isoformat(), encoding="utf-8")
    except Exception:
        pass


def enforce_install_gate(mode: str) -> None:
    """
    Block execution until required dependencies are installed.
    """
    doctor = Path(__file__).resolve().parent / "doctor.sh"
    if not doctor.exists():
        raise RuntimeError(f"doctor script missing: {doctor}")
    p = run(["bash", str(doctor), mode, "--strict"])
    if p.returncode != 0:
        msg = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
        raise RuntimeError(
            "Dependency gate not passed. Please install all required dependencies first.\n"
            + msg.strip()
        )


def module_exists(name: str) -> bool:
    p = run([sys.executable, "-c", f"import {name}"])
    return p.returncode == 0


def print_first_use_hint(mode: str, provider: str) -> None:
    # mode: asr|tts, provider: builtin|edge|local|openai
    print("First-use setup hint:", file=sys.stderr)
    if mode == "asr" and provider == "builtin":
        print("- Grant Speech Recognition permission to your app/terminal in macOS Privacy settings", file=sys.stderr)
        print("- If needed, reset and retry: tccutil reset SpeechRecognition", file=sys.stderr)
        print(f"- For compressed audio (m4a/mp3/aac/mp4), install ffmpeg: {FFMPEG_INSTALL_HINT}", file=sys.stderr)
    elif mode == "asr" and provider == "openai":
        print("- Set OPENAI_API_KEY for OpenAI ASR fallback", file=sys.stderr)
    elif mode == "asr" and provider == "local":
        print("- Install local ASR whisper (default): python3 -m pip install openai-whisper", file=sys.stderr)
        print("- Install ffmpeg: brew install ffmpeg (macOS) / apt-get install ffmpeg (Linux)", file=sys.stderr)
    elif mode == "tts" and provider in {"local", "builtin"}:
        print("- Local TTS requires macOS say/afconvert (install CLT: xcode-select --install)", file=sys.stderr)
    elif mode == "tts" and provider == "edge":
        print("- Install free neural TTS: python3 -m pip install edge-tts", file=sys.stderr)
    elif mode == "tts" and provider == "openai":
        print("- Set OPENAI_API_KEY for OpenAI TTS fallback", file=sys.stderr)
    print("- Run: bash scripts/doctor.sh", file=sys.stderr)


def is_decodable_audio(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 5000:
        return False
    if shutil.which("ffprobe"):
        p = run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "stream=codec_type",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ]
        )
        if p.returncode == 0 and "audio" in (p.stdout or ""):
            return True
    if platform.system() == "Darwin" and shutil.which("afinfo"):
        p = run(["afinfo", str(path)])
        if p.returncode == 0 and "estimated duration" in (p.stdout or ""):
            return True
    return False


def postprocess_audio_inplace(audio_path: Path) -> tuple[bool, str]:
    """
    Run ffmpeg post-processing in place.
    Returns (success, message).
    """
    if not shutil.which("ffmpeg"):
        return False, "ffmpeg not installed, skipped postprocess"

    ext = audio_path.suffix.lower()
    filt = (
        "highpass=f=70,"
        "lowpass=f=13500,"
        "compand=attacks=0.02:decays=0.20:points=-80/-80|-35/-22|-20/-12|0/-6,"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    tmp = audio_path.with_name(f".{audio_path.stem}-tmp{audio_path.suffix}")

    cmd = ["ffmpeg", "-y", "-i", str(audio_path), "-af", filt]
    if ext in {".m4a", ".mp4", ".aac"}:
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    elif ext == ".mp3":
        cmd += ["-c:a", "libmp3lame", "-b:a", "128k"]
    elif ext == ".wav":
        cmd += ["-c:a", "pcm_s16le"]
    else:
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd.append(str(tmp))

    p = run(cmd)
    if p.returncode != 0 or not tmp.exists():
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        return False, f"ffmpeg postprocess failed: {p.stderr.strip()}"
    tmp.replace(audio_path)
    return True, "audio enhanced"


def ensure_mp3_output(audio_path: Path) -> tuple[Path, str]:
    """
    Normalize audio output to mp3.
    """
    if audio_path.suffix.lower() == ".mp3":
        return audio_path, "already mp3"
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to normalize output to mp3")
    out_mp3 = audio_path.with_suffix(".mp3")
    p = run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(audio_path),
            "-c:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(out_mp3),
        ]
    )
    if p.returncode != 0 or not is_decodable_audio(out_mp3):
        raise RuntimeError(f"mp3 transcode failed: {p.stderr.strip()}")
    audio_path.unlink(missing_ok=True)
    return out_mp3, "transcoded to mp3"


def choose_macos_voices(local_voice: str | None = None, style: str = "neutral") -> list[str]:
    # Siri-like first, then robust Chinese fallback
    preferred = ["Eddy", "Flo", "Reed", "Shelley", "Sandy", "Rocko"]
    fallback = ["Tingting", "Meijia", "Sinji"]
    if style == "warm":
        fallback = ["Meijia", "Sinji", "Tingting"]
    elif style == "professional":
        fallback = ["Tingting", "Meijia", "Sinji"]
    locked = local_voice or os.getenv("MEETING_TTS_LOCAL_VOICE", "Tingting")
    all_voices = [locked] + preferred + fallback
    p = run(["say", "-v", "?"])
    if p.returncode != 0:
        return []
    names = {line.split()[0] for line in p.stdout.splitlines() if line.strip()}
    return [v for v in all_voices if v in names]


def is_valid_audio(path: Path) -> bool:
    if not path.exists():
        return False
    if path.stat().st_size < 5000:
        return False
    p = run(["afinfo", str(path)])
    if p.returncode != 0:
        return False
    m = re.search(r"estimated duration:\s*([0-9.]+)", p.stdout)
    if not m:
        return False
    try:
        return float(m.group(1)) > 0.5
    except ValueError:
        return False


def local_tts_macos(
    text_file: Path,
    out_prefix: Path,
    local_voice: str | None = None,
    style: str = "neutral",
    rate: int | None = None,
) -> tuple[str, Path]:
    if platform.system() != "Darwin":
        raise RuntimeError("local macOS TTS unavailable on this OS")
    if not shutil.which("say") or not shutil.which("afconvert"):
        raise RuntimeError("local macOS TTS tools not found (say/afconvert)")

    voices = choose_macos_voices(local_voice=local_voice, style=style)
    if not voices:
        raise RuntimeError("no usable Chinese macOS voice found")

    aiff = out_prefix.with_suffix(".aiff")
    m4a = out_prefix.with_suffix(".m4a")

    last_err = "unknown"
    for voice in voices:
        cmd = ["say", "-v", voice]
        if rate is not None:
            cmd += ["-r", str(rate)]
        cmd += ["-f", str(text_file), "-o", str(aiff)]
        p1 = run(cmd)
        if p1.returncode != 0:
            last_err = p1.stderr.strip() or f"say failed for {voice}"
            continue
        if not is_valid_audio(aiff):
            last_err = f"empty/invalid render for {voice}"
            continue

        p2 = run(["afconvert", "-f", "m4af", "-d", "aac", str(aiff), str(m4a)])
        if p2.returncode != 0:
            last_err = p2.stderr.strip() or f"afconvert failed for {voice}"
            continue
        if not is_valid_audio(m4a):
            last_err = f"invalid converted audio for {voice}"
            continue
        return voice, m4a

    raise RuntimeError(f"local macOS TTS failed: {last_err}")


def local_asr_whisper(audio_file: Path, language: str | None, model: str) -> dict:
    if not module_exists("whisper"):
        raise RuntimeError("python module 'whisper' not installed")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required for local whisper ASR")
    import whisper  # type: ignore

    whisper_model = whisper.load_model(model)
    kw = {"verbose": False}
    if language:
        kw["language"] = language
    result = whisper_model.transcribe(str(audio_file), **kw)

    low_confidence_segments = []
    for seg in result.get("segments", []) or []:
        avg_lp = seg.get("avg_logprob")
        no_speech = seg.get("no_speech_prob")
        is_low = False
        if avg_lp is not None and isinstance(avg_lp, (int, float)) and avg_lp < -1.0:
            is_low = True
        if no_speech is not None and isinstance(no_speech, (int, float)) and no_speech > 0.6:
            is_low = True
        if is_low:
            low_confidence_segments.append(
                {
                    "start": seg.get("start"),
                    "end": seg.get("end"),
                    "text": (seg.get("text") or "").strip(),
                    "avg_logprob": avg_lp,
                    "no_speech_prob": no_speech,
                }
            )

    return {
        "text": (result.get("text") or "").strip(),
        "language": result.get("language", "unknown"),
        "low_confidence_segments": low_confidence_segments,
        "confidence_note": "whisper segment heuristics: avg_logprob < -1.0 or no_speech_prob > 0.6",
    }


def builtin_asr_macos(audio_file: Path, language: str | None) -> dict:
    if platform.system() != "Darwin":
        raise RuntimeError("built-in ASR is only available on macOS")

    swift_script = Path(__file__).resolve().parent / "builtin_asr.swift"
    if not swift_script.exists():
        raise RuntimeError(f"built-in ASR script missing: {swift_script}")

    # Prefer `xcrun swift` for better SDK/toolchain matching, fallback to `swift`.
    if shutil.which("xcrun"):
        swift_cmd = ["xcrun", "swift"]
    elif shutil.which("swift"):
        swift_cmd = ["swift"]
    else:
        raise RuntimeError("swift runtime not found for built-in ASR")

    # Convert compressed formats to wav for better stability on built-in recognizer.
    # For m4a/mp3/aac/mp4 we prefer ffmpeg first (more robust across codec variants).
    src_for_asr = audio_file
    tmp_wav: Path | None = None
    if is_compressed_audio(audio_file):
        fd, tmp_name = tempfile.mkstemp(prefix="builtin_asr_", suffix=".wav")
        os.close(fd)
        tmp_wav = Path(tmp_name)
        converted = False
        convert_err = ""
        if not shutil.which("ffmpeg"):
            tmp_wav.unlink(missing_ok=True)
            raise RuntimeError(
                "ffmpeg not found; compressed audio input (m4a/mp3/aac/mp4) requires ffmpeg. "
                f"Install it first: {FFMPEG_INSTALL_HINT}"
            )
        p = run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_file),
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ac",
                "1",
                "-ar",
                "16000",
                str(tmp_wav),
            ]
        )
        converted = p.returncode == 0 and tmp_wav.exists() and tmp_wav.stat().st_size > 0
        if not converted:
            convert_err = (p.stderr or p.stdout or "").strip()

        # Fallback to macOS native converter only when ffmpeg conversion fails.
        if (not converted) and shutil.which("afconvert"):
            af_cmds = [
                ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", str(audio_file), str(tmp_wav)],
                ["afconvert", "-f", "WAVE", "-d", "LEI16", "-c", "1", str(audio_file), str(tmp_wav)],
                ["afconvert", "-f", "WAVE", "-d", "LEI16", str(audio_file), str(tmp_wav)],
            ]
            for c in af_cmds:
                p = run(c)
                converted = p.returncode == 0 and tmp_wav.exists() and tmp_wav.stat().st_size > 0
                if converted:
                    break
                convert_err = (p.stderr or p.stdout or "").strip()

        if converted:
            src_for_asr = tmp_wav
        else:
            tmp_wav.unlink(missing_ok=True)
            tmp_wav = None
            raise RuntimeError(f"built-in ASR audio conversion failed for {audio_file.name}. {convert_err}")

    locale_candidates = [language or "zh-CN", "zh-CN", "zh-Hans-CN", "en-US"]
    # Keep order and uniqueness.
    seen = set()
    locale_candidates = [x for x in locale_candidates if x and not (x in seen or seen.add(x))]

    last_err = "built-in ASR failed"
    swift_cache_dir = tempfile.mkdtemp(prefix="builtin_asr_swift_cache_")
    swift_env = {
        "CLANG_MODULE_CACHE_PATH": swift_cache_dir,
        "SWIFT_MODULECACHE_PATH": swift_cache_dir,
        "MODULE_CACHE_DIR": swift_cache_dir,
    }
    try:
        for loc in locale_candidates:
            cmd = [*swift_cmd, str(swift_script), str(src_for_asr), loc]
            p = run(cmd, env=swift_env)
            txt = (p.stdout or "").strip()
            if p.returncode == 0 and txt:
                return {
                    "text": txt,
                    "language": loc,
                    "low_confidence_segments": [],
                    "confidence_note": "built-in Speech recognizer (no segment confidence exposed)",
                }
            err = (p.stderr or p.stdout or f"built-in ASR failed for locale={loc}").strip()
            if "Speech authorization status:" in err:
                last_err = (
                    "built-in ASR permission denied. "
                    "Please grant Speech Recognition permission in macOS Privacy settings, "
                    "then retry. Details: " + err
                )
            else:
                last_err = err
    finally:
        shutil.rmtree(swift_cache_dir, ignore_errors=True)
        if tmp_wav:
            tmp_wav.unlink(missing_ok=True)

    raise RuntimeError(last_err)


def openai_headers(api_key: str, content_type: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": content_type}


def post_json(url: str, headers: dict[str, str], payload: dict) -> bytes:
    req = urllib.request.Request(
        url=url,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def post_multipart(url: str, headers: dict[str, str], fields: dict[str, str], file_field: str, file_path: Path) -> bytes:
    boundary = f"----codex-{uuid.uuid4().hex}"
    body = bytearray()
    for k, v in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
        body.extend(v.encode())
        body.extend(b"\r\n")

    file_bytes = file_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'.encode()
    )
    body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())

    hdrs = dict(headers)
    hdrs["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(url=url, method="POST", data=bytes(body), headers=hdrs)
    with urllib.request.urlopen(req, timeout=600) as resp:
        return resp.read()


def openai_tts(text_file: Path, out_prefix: Path, voice: str | None) -> tuple[str, Path]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    chosen_voice = voice or os.getenv("OPENAI_TTS_VOICE", "alloy")
    out_mp3 = out_prefix.with_suffix(".mp3")
    payload = {
        "model": model,
        "voice": chosen_voice,
        "input": text_file.read_text(encoding="utf-8"),
        "format": "mp3",
    }
    data = post_json(
        "https://api.openai.com/v1/audio/speech",
        openai_headers(api_key, "application/json"),
        payload,
    )
    out_mp3.write_bytes(data)
    return chosen_voice, out_mp3


def edge_tts_synthesize(text_file: Path, out_prefix: Path, style: str, edge_voice: str | None = None) -> tuple[str, Path]:
    if not module_exists("edge_tts"):
        raise RuntimeError("python module 'edge_tts' not installed")

    primary_voice = edge_voice or os.getenv("MEETING_TTS_EDGE_VOICE") or "zh-CN-XiaoxiaoNeural"
    backup_map = {
        "warm": ["zh-CN-XiaoxiaoNeural", "zh-CN-XiaoyiNeural", "zh-CN-liaoning-XiaobeiNeural"],
        "professional": ["zh-CN-YunxiNeural", "zh-CN-YunjianNeural", "zh-CN-XiaoxiaoNeural"],
        "neutral": ["zh-CN-XiaoxiaoNeural", "zh-CN-XiaoyiNeural", "zh-CN-YunxiNeural"],
    }
    voice_candidates = [primary_voice] + [v for v in backup_map.get(style, []) if v != primary_voice]
    voice_candidates = [v for i, v in enumerate(voice_candidates) if v and v not in voice_candidates[:i]]
    out_mp3 = out_prefix.with_suffix(".mp3")

    async def _run(voice_name: str) -> None:
        import edge_tts  # type: ignore

        text = text_file.read_text(encoding="utf-8")
        communicate = edge_tts.Communicate(text=text, voice=voice_name)
        await communicate.save(str(out_mp3))

    last_err = "unknown"
    for voice_name in voice_candidates:
        for attempt in range(1, 4):
            try:
                asyncio.run(_run(voice_name))
                if is_decodable_audio(out_mp3):
                    return voice_name, out_mp3
                last_err = f"edge-tts rendered empty/invalid audio for voice={voice_name}"
            except Exception as e:  # noqa: BLE001
                last_err = f"{voice_name} attempt {attempt}: {e}"
            time.sleep(0.6 * attempt)

    raise RuntimeError(f"edge-tts failed after retries and backup voices: {last_err}")


def openai_asr(audio_file: Path, language: str | None) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    model = os.getenv("OPENAI_ASR_MODEL", "gpt-4o-mini-transcribe")
    fields = {"model": model}
    if language:
        fields["language"] = language

    data = post_multipart(
        "https://api.openai.com/v1/audio/transcriptions",
        {"Authorization": f"Bearer {api_key}"},
        fields=fields,
        file_field="file",
        file_path=audio_file,
    )
    obj = json.loads(data.decode("utf-8"))
    return {
        "text": obj.get("text", "").strip(),
        "language": language or obj.get("language", "unknown"),
        "low_confidence_segments": [],
        "confidence_note": "provider does not expose segment confidence in this integration",
    }


def cmd_tts(args: argparse.Namespace) -> int:
    maybe_auto_install_deps("tts", bool(getattr(args, "auto_install", False)))
    try:
        enforce_install_gate("tts")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        print_install_steps("tts")
        return 2

    text_file = Path(args.input).resolve()
    if not text_file.exists():
        print(f"Error: file not found: {text_file}", file=sys.stderr)
        return 1
    outdir = resolve_output_dir(args.outdir)

    prefix = outdir / f"{safe_topic(args.topic)}-{ts_now()}"
    doc_out = prefix.with_suffix(".txt")
    spoken_out = prefix.with_suffix(".spoken.txt")
    full_text_out = prefix.with_suffix(".full.txt")

    raw_text = text_file.read_text(encoding="utf-8")
    # Keep document output as provided content; generate spoken script separately.
    doc_out.write_text(raw_text.strip() + "\n", encoding="utf-8")
    spoken_script = build_spoken_script(raw_text)
    cleaned_text = clean_tts_text(spoken_script)
    # Full-text audio must be verbatim from source text (no rewrite/cleanup),
    # to keep the generated recording fully aligned with the provided manuscript.
    verbatim_full_text = raw_text.strip()
    spoken_out.write_text(cleaned_text + "\n", encoding="utf-8")
    full_text_out.write_text(verbatim_full_text + "\n", encoding="utf-8")
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as tmpf:
        tmpf.write(cleaned_text)
        tmp_brief_tts_file = Path(tmpf.name)
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as tmpf2:
        tmpf2.write(verbatim_full_text)
        tmp_full_tts_file = Path(tmpf2.name)

    providers = [args.provider] if args.provider != "auto" else ["edge", "builtin", "local", "openai"]
    last_err = None

    def synth_once(provider: str, tf: Path, out_prefix: Path) -> tuple[str, Path]:
        if provider in {"local", "builtin"}:
            return local_tts_macos(
                tf,
                out_prefix,
                local_voice=args.local_voice,
                style=args.style,
                rate=args.rate,
            )
        if provider == "edge":
            return edge_tts_synthesize(tf, out_prefix, style=args.style, edge_voice=args.edge_voice)
        return openai_tts(tf, out_prefix, args.voice)

    brief_provider = None
    brief_voice = None
    brief_audio = None
    for p in providers:
        try:
            voice, audio_path = synth_once(p, tmp_brief_tts_file, prefix)
            if not is_decodable_audio(audio_path):
                raise RuntimeError(f"rendered audio is not decodable: {audio_path.name}")
            ok, msg = postprocess_audio_inplace(audio_path)
            audio_path, mp3_msg = ensure_mp3_output(audio_path)
            brief_provider = p
            brief_voice = voice
            brief_audio = audio_path
            brief_post_ok = ok
            brief_post_msg = f"{msg}; {mp3_msg}"
            break
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"[{p}] {e}", file=sys.stderr)
            print_first_use_hint("tts", p)

    if not brief_audio:
        tmp_brief_tts_file.unlink(missing_ok=True)
        tmp_full_tts_file.unlink(missing_ok=True)
        print(f"Error: TTS failed on providers {providers}: {last_err}", file=sys.stderr)
        return 1

    full_prefix = prefix.with_name(f"{prefix.name}.full")
    full_last_err = None
    full_audio = None
    full_voice = None
    # Prefer the same provider used by brief audio for consistency.
    full_providers = [brief_provider] + [x for x in providers if x != brief_provider]
    for p in full_providers:
        try:
            voice2, audio2 = synth_once(p, tmp_full_tts_file, full_prefix)
            if not is_decodable_audio(audio2):
                raise RuntimeError(f"rendered full audio is not decodable: {audio2.name}")
            postprocess_audio_inplace(audio2)
            audio2, _ = ensure_mp3_output(audio2)
            full_audio = audio2
            full_voice = voice2
            break
        except Exception as e:  # noqa: BLE001
            full_last_err = e
            print(f"[full:{p}] {e}", file=sys.stderr)

    tmp_brief_tts_file.unlink(missing_ok=True)
    tmp_full_tts_file.unlink(missing_ok=True)

    if not full_audio:
        print("Error: full-text audio generation failed.", file=sys.stderr)
        print(f"full_audio_error={full_last_err}", file=sys.stderr)
        return 1

    print(f"provider={brief_provider}")
    print(f"voice={brief_voice}")
    print(f"output_dir={outdir}")
    print(f"doc={doc_out}")
    print(f"spoken_script={spoken_out}")
    print(f"full_text={full_text_out}")
    print(f"audio={brief_audio}")
    print(f"audio_full={full_audio if full_audio else 'N/A'}")
    print(f"voice_full={full_voice if full_voice else 'N/A'}")
    print(f"postprocess={'on' if brief_post_ok else 'off'}")
    print(f"postprocess_note={brief_post_msg}")
    return 0


def cmd_asr(args: argparse.Namespace) -> int:
    maybe_auto_install_deps("asr", bool(getattr(args, "auto_install", False)))
    try:
        enforce_install_gate("asr")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        print_install_steps("asr")
        return 2

    audio_file = Path(args.input).resolve()
    if not audio_file.exists():
        print(f"Error: file not found: {audio_file}", file=sys.stderr)
        return 1
    outdir = resolve_output_dir(args.outdir)
    prefix = outdir / f"{safe_topic(args.topic)}-{ts_now()}"
    out_json = prefix.with_suffix(".transcript.json")
    out_txt = prefix.with_suffix(".transcript.txt")
    out_doc = prefix.with_suffix(".txt")

    # Auto mode prefers installed engines first, then cloud, then built-in fallback.
    providers = [args.provider] if args.provider != "auto" else ["local", "openai", "builtin"]
    compressed_input = is_compressed_audio(audio_file)
    if args.provider == "auto" and compressed_input and (not shutil.which("ffmpeg")):
        # Without ffmpeg, local/builtin compressed-audio paths are unstable.
        providers = ["openai", "local", "builtin"]
        print(
            "notice=compressed audio detected without ffmpeg; auto route switched to openai-first. "
            f"Install ffmpeg for local/built-in ASR: {FFMPEG_INSTALL_HINT}",
            file=sys.stderr,
        )
    last_err = None
    for p in providers:
        try:
            if p == "builtin":
                obj = builtin_asr_macos(audio_file, args.language)
            elif p == "local":
                obj = local_asr_whisper(audio_file, args.language, args.model)
            else:
                obj = openai_asr(audio_file, args.language)
            out_json.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
            transcript_text = obj.get("text", "").strip()
            out_txt.write_text(transcript_text + "\n", encoding="utf-8")
            # Final doc for downstream 3-artifact workflow.
            out_doc.write_text(transcript_text + "\n", encoding="utf-8")
            print(f"provider={p}")
            print(f"output_dir={outdir}")
            print(f"json={out_json}")
            print(f"text={out_txt}")
            print(f"doc={out_doc}")
            return 0
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"[{p}] {e}", file=sys.stderr)
            print_first_use_hint("asr", p)

    print(f"Error: ASR failed on providers {providers}: {last_err}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-platform ASR/TTS bridge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_tts = sub.add_parser("tts", help="Synthesize meeting briefing audio")
    p_tts.add_argument("--input", required=True, help="Briefing text file path")
    p_tts.add_argument("--topic", required=True, help="Meeting topic for file naming")
    p_tts.add_argument("--outdir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory (fixed to skill outputs)")
    p_tts.add_argument("--provider", choices=["auto", "builtin", "edge", "local", "openai"], default="auto")
    p_tts.add_argument("--voice", default=None, help="OpenAI voice override (openai provider)")
    p_tts.add_argument("--edge-voice", default=None, help="Edge TTS voice override, e.g. zh-CN-XiaoxiaoNeural")
    p_tts.add_argument("--local-voice", default=None, help="Local macOS voice override, e.g. Tingting")
    p_tts.add_argument("--style", choices=["neutral", "professional", "warm"], default="warm")
    p_tts.add_argument("--rate", type=int, default=None, help="Local speech rate, e.g. 170-210")
    p_tts.add_argument("--auto-install", action="store_true", help="Try auto-installing missing macOS deps before run")
    p_tts.set_defaults(func=cmd_tts)

    p_asr = sub.add_parser("asr", help="Transcribe meeting audio")
    p_asr.add_argument("--input", required=True, help="Audio file path")
    p_asr.add_argument("--topic", required=True, help="Meeting topic for file naming")
    p_asr.add_argument("--outdir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory (fixed to skill outputs)")
    p_asr.add_argument("--provider", choices=["auto", "builtin", "local", "openai"], default="auto")
    p_asr.add_argument("--language", default=None, help="Language code, e.g. zh")
    p_asr.add_argument("--model", default="tiny", help="Local whisper model (for local provider)")
    p_asr.add_argument("--auto-install", action="store_true", help="Try auto-installing missing macOS deps before run")
    p_asr.set_defaults(func=cmd_asr)

    return parser


def main() -> int:
    wants_help = any(x in {"-h", "--help"} for x in sys.argv[1:])
    if not wants_help:
        print_first_run_notice_once()
        print_first_run_env_check_once()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
