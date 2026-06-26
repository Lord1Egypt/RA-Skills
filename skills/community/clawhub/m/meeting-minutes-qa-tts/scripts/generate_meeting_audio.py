import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

import requests


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"
API_MODEL = "SenseAudio-TTS-1.0"
DEFAULT_VOICE_ID = "male_0004_a"
DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_BITRATE = 128000
DEFAULT_CHANNELS = 2
REQUEST_TIMEOUT = 60
LOCAL_ENCODINGS = ("utf-8", "utf-8-sig", "cp936", "latin-1")
SUPPORTED_MODES = {"full_text", "summary", "decisions", "action_items"}
MOJIBAKE_MARKERS = ("ѧ", "ϰ", "ǿ", "ڹ", "Լ", "ģ", "Ͷ", "ʽ", "Ϊ", "ɶ", "뻺")
DECISION_PATTERNS = (
    "decision",
    "decisions",
    "决定",
    "结论",
    "决议",
)
ACTION_ITEM_PATTERNS = (
    "action item",
    "action items",
    "todo",
    "owner",
    "next step",
    "行动项",
    "待办",
    "负责人",
    "下一步",
)


def generate_meeting_audio(
    input_text: str,
    output_path: str | None = None,
    mode: str = "full_text",
    voice_id: str | None = None,
    api_key: str | None = None,
) -> str:
    if mode not in SUPPORTED_MODES:
        supported = ", ".join(sorted(SUPPORTED_MODES))
        return f"ERROR: Unsupported mode '{mode}'. Supported modes: {supported}"

    resolved_api_key = resolve_senseaudio_api_key(api_key)
    if not resolved_api_key:
        return "ERROR: Missing SenseAudio API key. Set SENSEAUDIO_API_KEY or provide --api-key."

    prepared = _prepare_text(input_text, mode)
    if prepared["text"].startswith("ERROR:"):
        return prepared["text"]

    final_output_path = _resolve_output_path(output_path)
    final_voice_id = voice_id or os.getenv("SENSEAUDIO_DEFAULT_VOICE") or DEFAULT_VOICE_ID

    payload = {
        "model": API_MODEL,
        "text": prepared["text"],
        "stream": False,
        "voice_setting": {
            "voice_id": final_voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": DEFAULT_SAMPLE_RATE,
            "bitrate": DEFAULT_BITRATE,
            "format": DEFAULT_AUDIO_FORMAT,
            "channel": DEFAULT_CHANNELS,
        },
    }
    headers = {
        "Authorization": f"Bearer {resolved_api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        return f"ERROR: SenseAudio request timed out after {REQUEST_TIMEOUT}s"
    except requests.RequestException as exc:
        return f"ERROR: SenseAudio request failed: {exc}"

    if response.status_code != 200:
        detail = response.text.strip()[:300]
        return f"ERROR: SenseAudio API returned {response.status_code}: {detail}"

    try:
        parsed = response.json()
    except ValueError as exc:
        return f"ERROR: Failed to parse SenseAudio response JSON: {exc}"

    base_resp = parsed.get("base_resp") or {}
    if base_resp.get("status_code") not in (None, 0):
        return f"ERROR: SenseAudio API error: {base_resp.get('status_msg', 'unknown error')}"

    audio_hex = parsed.get("data", {}).get("audio")
    if not audio_hex:
        return "ERROR: SenseAudio response did not contain data.audio"

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError as exc:
        return f"ERROR: Failed to decode audio hex: {exc}"

    try:
        final_output_path.parent.mkdir(parents=True, exist_ok=True)
        final_output_path.write_bytes(audio_bytes)
    except OSError as exc:
        return f"ERROR: Failed to write audio file: {exc}"

    result = {
        "status": "ok",
        "requested_mode": mode,
        "resolved_mode": prepared["resolved_mode"],
        "fallback_used": prepared["fallback_used"],
        "voice_id": final_voice_id,
        "output_path": str(final_output_path),
        "text_length": len(prepared["text"]),
    }
    return json.dumps(result, ensure_ascii=True, indent=2)


def resolve_senseaudio_api_key(api_key: str | None = None) -> str | None:
    if api_key is not None:
        stripped = api_key.strip()
        if stripped:
            return stripped

    env_api_key = os.getenv("SENSEAUDIO_API_KEY")
    if env_api_key is None:
        return None

    stripped_env_api_key = env_api_key.strip()
    return stripped_env_api_key or None


def read_text_source(location: str) -> str:
    if location.startswith(("http://", "https://")):
        try:
            response = requests.get(location, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            return f"ERROR: Request timed out after {REQUEST_TIMEOUT}s"
        except requests.RequestException as exc:
            return f"ERROR: Failed to fetch URL: {exc}"

        if response.status_code != 200:
            return f"ERROR: URL fetch failed with status code {response.status_code}"
        return _normalize_source_text(response.text)

    abs_path = os.path.abspath(location)
    if not os.path.exists(abs_path):
        return f"ERROR: Local file does not exist: {abs_path}"
    if not os.path.isfile(abs_path):
        return f"ERROR: Local path is not a file: {abs_path}"

    for encoding in LOCAL_ENCODINGS:
        try:
            with open(abs_path, "r", encoding=encoding) as handle:
                return _normalize_source_text(handle.read())
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            return f"ERROR: Failed to read local file: {exc}"

    tried = ", ".join(LOCAL_ENCODINGS)
    return f"ERROR: Failed to decode local file with supported encodings: {tried}"


def _prepare_text(input_text: str, mode: str) -> dict[str, object]:
    text = input_text.strip()
    if not text:
        return {
            "text": "ERROR: Input text is empty",
            "resolved_mode": mode,
            "fallback_used": False,
        }

    if mode == "full_text":
        selected = _clean_text(text)
        return {
            "text": selected,
            "resolved_mode": mode,
            "fallback_used": False,
        }

    if mode == "decisions":
        extracted = _extract_matching_lines(text, DECISION_PATTERNS)
        if extracted:
            return {
                "text": extracted,
                "resolved_mode": "decisions",
                "fallback_used": False,
            }
        return _fallback_summary(text, mode)

    if mode == "action_items":
        extracted = _extract_matching_lines(text, ACTION_ITEM_PATTERNS)
        if extracted:
            return {
                "text": extracted,
                "resolved_mode": "action_items",
                "fallback_used": False,
            }
        return _fallback_summary(text, mode)

    return {
        "text": _make_summary(text),
        "resolved_mode": "summary",
        "fallback_used": False,
    }


def _fallback_summary(text: str, requested_mode: str) -> dict[str, object]:
    return {
        "text": _make_summary(text),
        "resolved_mode": "summary",
        "fallback_used": requested_mode != "summary",
    }


def _extract_matching_lines(text: str, patterns: tuple[str, ...]) -> str:
    matches: list[str] = []
    for line in _non_empty_lines(text):
        lowered = line.lower()
        if any(pattern in lowered for pattern in patterns):
            matches.append(line)
    return _clean_text("\n".join(matches))


def _make_summary(text: str) -> str:
    lines = _non_empty_lines(text)
    summary_lines = lines[:6]
    return _clean_text("\n".join(summary_lines))


def _non_empty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _clean_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return "ERROR: No usable text after preprocessing"
    max_chars = _max_input_chars()
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars].rstrip()
    return cleaned


def _max_input_chars() -> int:
    value = os.getenv("SENSEAUDIO_TTS_MAX_CHARS", "1000")
    try:
        parsed = int(value)
    except ValueError:
        return 1000
    return max(parsed, 100)


def _normalize_source_text(text: str) -> str:
    repaired = _repair_common_mojibake(text)
    return repaired.strip()


def _repair_common_mojibake(text: str) -> str:
    if not text:
        return text
    if not _looks_like_mojibake(text):
        return text

    attempts = (
        ("latin-1", "gbk"),
        ("latin-1", "utf-8"),
        ("cp1252", "gbk"),
        ("cp1252", "utf-8"),
    )
    best = text
    best_score = _mojibake_score(text)
    for source_encoding, target_encoding in attempts:
        try:
            candidate = text.encode(source_encoding).decode(target_encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        candidate_score = _mojibake_score(candidate)
        if candidate_score < best_score:
            best = candidate
            best_score = candidate_score
    return best


def _looks_like_mojibake(text: str) -> bool:
    return any(marker in text for marker in MOJIBAKE_MARKERS)


def _mojibake_score(text: str) -> int:
    score = 0
    for marker in MOJIBAKE_MARKERS:
        score += text.count(marker) * 2
    score += text.count("�") * 3
    score += text.count("?")
    return score


def _resolve_output_path(output_path: str | None) -> Path:
    if output_path:
        return Path(output_path).expanduser().resolve()

    skill_dir = Path(__file__).resolve().parent.parent
    outputs_dir = skill_dir / "outputs"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return outputs_dir / f"meeting-{timestamp}.{DEFAULT_AUDIO_FORMAT}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate meeting audio with SenseAudio TTS.")
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--text", help="Direct meeting text")
    source_group.add_argument("--location", help="Local file path or URL containing meeting text")
    parser.add_argument(
        "--mode",
        default="full_text",
        choices=sorted(SUPPORTED_MODES),
        help="Text selection mode",
    )
    parser.add_argument("--output-path", help="Local output path for the mp3 file")
    parser.add_argument("--voice-id", help="SenseAudio voice identifier")
    parser.add_argument("--api-key", help="SenseAudio API key. Falls back to SENSEAUDIO_API_KEY when omitted.")
    args = parser.parse_args()

    input_text = args.text if args.text is not None else read_text_source(args.location)
    if input_text.startswith("ERROR:"):
        print(input_text)
        return 1

    result = generate_meeting_audio(
        input_text=input_text,
        output_path=args.output_path,
        mode=args.mode,
        voice_id=args.voice_id,
        api_key=args.api_key,
    )
    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
