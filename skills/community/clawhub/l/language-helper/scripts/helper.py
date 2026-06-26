#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = ROOT_DIR / ".env"


_ENV_TEMPLATE = """\
# SenseAudio TTS API Key (required)
SENSEAUDIO_API_KEY=

# Feishu / Lark credentials (optional, for send-voice feature)
# FEISHU_APP_ID=cli_xxx
# FEISHU_APP_SECRET=xxx
# FEISHU_CHAT_ID=oc_xxx
"""


def _ensure_env_file():
    """Create .env template if it does not exist."""
    if _ENV_FILE.exists():
        return
    _ENV_FILE.write_text(_ENV_TEMPLATE, encoding="utf-8")


def _load_dotenv():
    """Load .env file into os.environ (simple key=value parser, no dependency)."""
    _ensure_env_file()
    for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        os.environ.setdefault(key, value)


_load_dotenv()


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"
MODEL_NAME = "SenseAudio-TTS-1.0"
FALLBACK_VOICE_IDS = ["child_0001_b", "male_0004_a", "male_0018_a"]
RETRYABLE_HTTP_STATUS_CODES = {500, 502, 503, 504}
CONTENT_TYPE_ERROR_MARKERS = ("input content type is not supported",)
ROLE_PREFIX_RE = re.compile(r"^\s*[\w\-\u4e00-\u9fff]{1,20}\s*[:：]\s*")
CLAUSE_SPLIT_RE = re.compile(r"[。！？!?；;，,:：\n]+")
SPACE_PUNCT_RE = re.compile(r"[。！？!?；;，,:：、]+")
PUNCT_TRANSLATION = str.maketrans(
    {
        "：": ":",
        "，": ",",
        "。": ".",
        "；": ";",
        "！": "!",
        "？": "?",
        "（": "(",
        "）": ")",
        "【": "[",
        "】": "]",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "—": "-",
        "～": "~",
        "\u3000": " ",
    }
)
SAFE_PUNCT_CHARS = set(".,!?;:()[]<>/=-_ ")

LANG_VOICE_MAP = {
    "ja": "male_0004_a",
    "en": "male_0004_a",
    "zh": "male_0004_a",
    "ko": "male_0004_a",
    "fr": "male_0004_a",
    "es": "male_0004_a",
    "de": "male_0004_a",
}
DEFAULT_VOICE = "male_0004_a"


class SenseAudioBusinessError(Exception):
    def __init__(self, status_code, status_msg, body, parsed_json):
        super().__init__(f"status_code={status_code} status_msg={status_msg}")
        self.status_code = status_code
        self.status_msg = status_msg
        self.body = body
        self.parsed_json = parsed_json


class VoiceAccessDeniedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def _configure_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="backslashreplace")
            except ValueError:
                continue


def _write_bytes(output, payload):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _json_dumps(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _build_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "User-Agent": "LanguageHelper/1.0",
    }


def _redact_headers(headers):
    redacted = dict(headers)
    if "Authorization" in redacted:
        redacted["Authorization"] = "Bearer ***"
    return redacted


def _preview_text(text, limit=120):
    compact = text.replace("\n", "\\n")
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit]}..."


def _read_text_file(path):
    return Path(path).read_text(encoding="utf-8-sig", errors="replace")


def _normalize_text(text):
    normalized = text.replace("\ufeff", "")
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\u3000", " ")
    normalized = unicodedata.normalize("NFKC", normalized)

    cleaned_chars = []
    for ch in normalized:
        category = unicodedata.category(ch)
        if ch == "\n":
            cleaned_chars.append(ch)
            continue
        if category == "Cc":
            if ch == "\t":
                cleaned_chars.append(" ")
            continue
        if category == "Cf":
            continue
        cleaned_chars.append(ch)

    normalized = "".join(cleaned_chars)
    lines = [re.sub(r"\s+", " ", line).strip() for line in normalized.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


def _strip_role_prefixes(text):
    stripped_lines = []
    for line in text.split("\n"):
        stripped = ROLE_PREFIX_RE.sub("", line).strip()
        if stripped:
            stripped_lines.append(stripped)
    return "\n".join(stripped_lines).strip()


def _normalize_punctuation(text):
    normalized = text.translate(PUNCT_TRANSLATION)
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s*([,.;:!?])\s*", r"\1", normalized)
    return normalized.strip()


def _strip_special_punctuation(text):
    cleaned_chars = []
    for ch in text:
        if ch == "\n":
            cleaned_chars.append(ch)
            continue
        category = unicodedata.category(ch)
        if category.startswith("P") and ch not in SAFE_PUNCT_CHARS:
            continue
        if category == "So":
            continue
        cleaned_chars.append(ch)
    return re.sub(r"\s+", " ", "".join(cleaned_chars)).strip()


def _make_plain_body(text):
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()


def _make_spaced_text(text):
    spaced = SPACE_PUNCT_RE.sub(" ", text)
    return re.sub(r"\s+", " ", spaced).strip()


def _make_no_punct_text(text):
    cleaned_chars = []
    for ch in text:
        category = unicodedata.category(ch)
        if ch.isspace():
            cleaned_chars.append(" ")
            continue
        if category.startswith("P") or category == "So":
            continue
        cleaned_chars.append(ch)
    return re.sub(r"\s+", " ", "".join(cleaned_chars)).strip()


def _build_short_text_variants(text):
    clauses = [part.strip() for part in CLAUSE_SPLIT_RE.split(text) if part.strip()]
    if len(clauses) <= 1:
        return []

    variants = []
    for clause in clauses:
        if len(clause) >= 6:
            variants.append(clause)

    joined_head = " ".join(clauses[:2]).strip()
    joined_tail = " ".join(clauses[-2:]).strip()
    if joined_head:
        variants.append(joined_head)
    if joined_tail:
        variants.append(joined_tail)

    unique = []
    seen = set()
    for item in variants:
        candidate = re.sub(r"\s+", " ", item).strip()
        if not candidate or candidate in seen or candidate == text:
            continue
        seen.add(candidate)
        unique.append(candidate)
        if len(unique) >= 4:
            break
    return unique


def _build_text_variants(raw_text):
    normalized = _normalize_text(raw_text)
    if not normalized:
        return {}

    variants = {}

    def add_variant(name, text):
        candidate = text.strip()
        if not candidate:
            return
        if candidate in variants.values():
            return
        variants[name] = candidate

    add_variant("normalized", normalized)

    no_role_prefix = _strip_role_prefixes(normalized)
    add_variant("no-role-prefix", no_role_prefix)

    normalized_punct = _normalize_punctuation(no_role_prefix or normalized)
    add_variant("normalized-punct", normalized_punct)

    no_special_punct = _strip_special_punctuation(normalized_punct or no_role_prefix or normalized)
    add_variant("no-special-punct", no_special_punct)

    plain_body = _make_plain_body(no_special_punct or normalized_punct or no_role_prefix or normalized)
    add_variant("plain-body", plain_body)

    spaced = _make_spaced_text(plain_body or normalized_punct)
    add_variant("spaced", spaced)

    no_punct = _make_no_punct_text(plain_body or normalized_punct)
    add_variant("no-punct", no_punct)

    for index, short_text in enumerate(_build_short_text_variants(normalized_punct or plain_body), start=1):
        add_variant(f"short-{index}", short_text)

    return variants


def _build_payload(
    args,
    text,
    voice_id,
    *,
    include_audio_setting=True,
    include_speed_pitch=True,
    minimal=False,
):
    payload = {
        "model": MODEL_NAME,
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id},
    }

    if minimal:
        return payload

    if include_speed_pitch and args.speed is not None:
        payload["voice_setting"]["speed"] = args.speed
    if args.vol is not None:
        payload["voice_setting"]["vol"] = args.vol
    if include_speed_pitch and args.pitch is not None:
        payload["voice_setting"]["pitch"] = args.pitch

    if include_audio_setting:
        audio_setting = {}
        if args.format is not None:
            audio_setting["format"] = args.format
        if args.sample_rate is not None:
            audio_setting["sample_rate"] = args.sample_rate
        if args.bitrate is not None:
            audio_setting["bitrate"] = args.bitrate
        if args.channel is not None:
            audio_setting["channel"] = args.channel
        if audio_setting:
            payload["audio_setting"] = audio_setting

    return payload


def _build_payload_variants(args, text, voice_id):
    variants = []
    seen = set()
    candidates = [
        (
            "full",
            _build_payload(
                args, text, voice_id,
                include_audio_setting=True, include_speed_pitch=True, minimal=False,
            ),
        ),
        (
            "no-audio-setting",
            _build_payload(
                args, text, voice_id,
                include_audio_setting=False, include_speed_pitch=True, minimal=False,
            ),
        ),
        (
            "no-speed-pitch",
            _build_payload(
                args, text, voice_id,
                include_audio_setting=False, include_speed_pitch=False, minimal=False,
            ),
        ),
        ("minimal", _build_payload(args, text, voice_id, minimal=True)),
    ]

    for payload_mode, payload in candidates:
        signature = _json_dumps(payload)
        if signature in seen:
            continue
        seen.add(signature)
        variants.append((payload_mode, payload))
    return variants


def _is_content_type_error(status_code, details):
    if str(status_code) != "400":
        return False
    lowered = (details or "").lower()
    return any(marker in lowered for marker in CONTENT_TYPE_ERROR_MARKERS)


def _is_voice_access_denied(status_code, details):
    lowered = (details or "").lower()
    return str(status_code) == "403" and "no access to the specified voice" in lowered


def _should_continue_after_http_error(status_code, details):
    if status_code in RETRYABLE_HTTP_STATUS_CODES:
        return True
    if _is_content_type_error(status_code, details):
        return True
    return False


def _should_continue_after_business_error(status_code, status_msg):
    code_text = str(status_code)
    details = status_msg or ""
    if code_text.startswith("5"):
        return True
    if code_text == "400":
        return True
    if _is_content_type_error(status_code, details):
        return True
    return False


def _capture_attempt(attempt_logs, payload, headers, text_mode, payload_mode, attempt_index):
    entry = {
        "attempt": attempt_index,
        "text_mode": text_mode,
        "payload_mode": payload_mode,
        "voice_id": ((payload.get("voice_setting") or {}).get("voice_id")),
        "request_format": "application/json",
        "headers": _redact_headers(headers),
        "text_length": len(payload["text"]),
        "text_preview": _preview_text(payload["text"]),
        "payload": payload,
        "request_body_json": _json_dumps(payload),
    }
    attempt_logs.append(entry)
    return entry


def _decode_response_body(response_body):
    return response_body.decode("utf-8", errors="replace")


def _parse_business_response(response_body_text):
    try:
        data = json.loads(response_body_text)
    except json.JSONDecodeError as exc:
        raise SenseAudioBusinessError("non_json", "non-JSON response", response_body_text, None) from exc

    base_resp = data.get("base_resp") or {}
    status_code = base_resp.get("status_code")
    status_msg = base_resp.get("status_msg")
    if status_code not in (0, "0", None):
        raise SenseAudioBusinessError(status_code, status_msg, response_body_text, data)

    audio_hex = ((data.get("data") or {}).get("audio") or "").strip()
    if not audio_hex:
        raise SenseAudioBusinessError("missing_audio", "response does not contain data.audio", response_body_text, data)

    return data


def _send_tts_request(api_key, payload, attempt_logs, text_mode, payload_mode, attempt_index):
    body_json = _json_dumps(payload)
    headers = _build_headers(api_key)
    request = urllib.request.Request(
        API_URL,
        data=body_json.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    attempt_entry = _capture_attempt(attempt_logs, payload, headers, text_mode, payload_mode, attempt_index)

    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read()
            response_text = _decode_response_body(response_body)
            attempt_entry["response_status"] = response.status
            attempt_entry["response_headers"] = dict(response.headers.items())
            attempt_entry["response_text"] = response_text

            try:
                parsed = _parse_business_response(response_text)
            except SenseAudioBusinessError as exc:
                attempt_entry["business_status_code"] = exc.status_code
                attempt_entry["business_status_msg"] = exc.status_msg
                raise

            base_resp = parsed.get("base_resp") or {}
            attempt_entry["business_status_code"] = base_resp.get("status_code")
            attempt_entry["business_status_msg"] = base_resp.get("status_msg")
            return parsed
    except urllib.error.HTTPError as exc:
        details = _decode_response_body(exc.read())
        attempt_entry["response_status"] = exc.code
        attempt_entry["response_headers"] = dict(exc.headers.items()) if exc.headers else {}
        attempt_entry["response_text"] = details

        try:
            parsed = json.loads(details)
        except json.JSONDecodeError:
            parsed = None
        if parsed:
            base_resp = parsed.get("base_resp") or {}
            attempt_entry["business_status_code"] = base_resp.get("status_code")
            attempt_entry["business_status_msg"] = base_resp.get("status_msg")
        raise
    except urllib.error.URLError as exc:
        attempt_entry["transport_error"] = str(exc.reason)
        raise


def _request_with_retries(
    api_key, payload, attempt_logs, text_mode, payload_mode, attempt_counter_start,
):
    attempt_counter = attempt_counter_start
    for retry_index in range(3):
        attempt_counter += 1
        try:
            data = _send_tts_request(
                api_key, payload, attempt_logs, text_mode, payload_mode, attempt_counter,
            )
            return data, attempt_counter
        except urllib.error.HTTPError as exc:
            if exc.code in RETRYABLE_HTTP_STATUS_CODES and retry_index < 2:
                time.sleep(0.8 * (2**retry_index))
                continue
            raise
        except urllib.error.URLError:
            if retry_index < 2:
                time.sleep(0.8 * (2**retry_index))
                continue
            raise
    raise SystemExit("TTS request failed after retries.")


def _write_debug_log(debug_log_path, payload):
    if not debug_log_path:
        return
    _write_json(debug_log_path, payload)


def _debug_summary(debug_log_path, attempt_logs):
    if not attempt_logs:
        return ""
    last = attempt_logs[-1]
    summary = (
        f"request_format={last.get('request_format')} "
        f"text_mode={last.get('text_mode')} "
        f"payload_mode={last.get('payload_mode')} "
        f"text_length={last.get('text_length')} "
        f"status={last.get('response_status')} "
        f"business_status={last.get('business_status_code')}"
    )
    if debug_log_path:
        summary += f" debug_log={debug_log_path}"
    return summary


def _write_failure_debug_log(debug_log_path, args, text_variants, attempt_logs):
    payload = {
        "api_url": API_URL,
        "text_file": str(Path(args.text_file).resolve()),
        "output": str(Path(args.output).resolve()),
        "voice_id": args.voice_id,
        "speed": args.speed,
        "pitch": args.pitch,
        "vol": args.vol,
        "format": args.format,
        "sample_rate": args.sample_rate,
        "bitrate": args.bitrate,
        "channel": args.channel,
        "text_variants": text_variants,
        "attempts": attempt_logs,
    }
    _write_debug_log(debug_log_path, payload)


def _voice_fallback_order(current_voice_id):
    return [voice_id for voice_id in FALLBACK_VOICE_IDS if voice_id != current_voice_id]


def _get_api_key():
    # Prefer the skill-local .env value so stale shell environment variables
    # do not override the known-good key configured for this skill.
    env_file_value = ""
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() == "SENSEAUDIO_API_KEY":
                env_file_value = value.strip()
                break

    api_key = env_file_value or os.environ.get("SENSEAUDIO_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "SENSEAUDIO_API_KEY is not set.\n"
            "Add it to skills/language-helper/.env:\n"
            "  SENSEAUDIO_API_KEY=your_key"
        )
    return api_key


def _try_payload_variants(api_key, args, text_mode, text_value, voice_id, attempt_logs, attempt_counter):
    last_error = None

    for payload_mode, payload in _build_payload_variants(args, text_value, voice_id):
        try:
            data, attempt_counter = _request_with_retries(
                api_key, payload, attempt_logs, text_mode, payload_mode, attempt_counter,
            )
            return data, payload, attempt_counter, last_error
        except urllib.error.HTTPError as exc:
            details = attempt_logs[-1].get("response_text", "")
            last_error = f"HTTP {exc.code}: {details}"
            if _is_voice_access_denied(exc.code, details):
                raise VoiceAccessDeniedError(details) from exc
            if _should_continue_after_http_error(exc.code, details):
                continue
            raise SystemExit(
                f"TTS request failed: {last_error}. {_debug_summary(None, attempt_logs)}"
            ) from exc
        except SenseAudioBusinessError as exc:
            details = exc.status_msg or ""
            last_error = f"SenseAudio error: status_code={exc.status_code} status_msg={details}"
            if _is_voice_access_denied(exc.status_code, details):
                raise VoiceAccessDeniedError(details) from exc
            if _should_continue_after_business_error(exc.status_code, details):
                continue
            if str(exc.status_code) == "non_json":
                continue
            if str(exc.status_code) == "missing_audio":
                continue
            raise SystemExit(
                f"TTS request failed: {last_error}. {_debug_summary(None, attempt_logs)}"
            ) from exc
        except urllib.error.URLError as exc:
            raise SystemExit(
                f"TTS request failed after transport retries: {exc.reason}. "
                f"{_debug_summary(None, attempt_logs)}"
            ) from exc

    return None, None, attempt_counter, last_error


def _attempt_tts(api_key, args, text_variants, debug_log_path):
    attempt_logs = []
    attempt_counter = 0
    requested_voice_id = args.voice_id
    last_error = None

    for text_mode, text_value in text_variants.items():
        try:
            data, payload, attempt_counter, last_error = _try_payload_variants(
                api_key, args, text_mode, text_value, requested_voice_id,
                attempt_logs, attempt_counter,
            )
            if data is not None:
                return data, payload, attempt_logs
        except VoiceAccessDeniedError as exc:
            last_error = f"Voice access denied: {exc.message}"
            for fallback_voice_id in _voice_fallback_order(requested_voice_id):
                try:
                    data, payload, attempt_counter, last_error = _try_payload_variants(
                        api_key, args, f"{text_mode}+voice-fallback", text_value,
                        fallback_voice_id, attempt_logs, attempt_counter,
                    )
                    if data is not None:
                        return data, payload, attempt_logs
                except VoiceAccessDeniedError as fallback_exc:
                    last_error = f"Voice access denied: {fallback_exc.message}"
                    continue
        except SystemExit:
            _write_failure_debug_log(debug_log_path, args, text_variants, attempt_logs)
            raise

    _write_failure_debug_log(debug_log_path, args, text_variants, attempt_logs)
    if last_error:
        raise SystemExit(
            f"TTS request failed after all text/payload variants: {last_error}. "
            f"{_debug_summary(debug_log_path, attempt_logs)}"
        )
    raise SystemExit(
        "TTS request failed after all text/payload variants. "
        f"{_debug_summary(debug_log_path, attempt_logs)}"
    )


def synthesize(args):
    api_key = _get_api_key()

    raw_text = _read_text_file(args.text_file)
    text_variants = _build_text_variants(raw_text)
    if not text_variants:
        raise SystemExit("Input text is empty.")

    output = Path(args.output)
    debug_log_path = Path(args.debug_log) if args.debug_log else None

    try:
        data, payload, attempt_logs = _attempt_tts(api_key, args, text_variants, debug_log_path)
    except SystemExit:
        if debug_log_path:
            print(f"[LanguageHelper] failure debug log written to: {debug_log_path}", file=sys.stderr)
        raise

    if debug_log_path:
        debug_payload = {
            "api_url": API_URL,
            "text_file": str(Path(args.text_file).resolve()),
            "output": str(output.resolve()),
            "voice_id_requested": args.voice_id,
            "voice_id_used": payload["voice_setting"]["voice_id"],
            "speed": args.speed,
            "pitch": args.pitch,
            "vol": args.vol,
            "format": args.format,
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "channel": args.channel,
            "text_variants": text_variants,
            "attempts": attempt_logs,
        }
        _write_debug_log(debug_log_path, debug_payload)

    base_resp = data.get("base_resp") or {}
    audio_hex = ((data.get("data") or {}).get("audio") or "").strip()

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError as exc:
        raise SystemExit("SenseAudio data.audio is not valid hex.") from exc

    _write_bytes(output, audio_bytes)
    info = {
        "output": str(output),
        "voice_id": payload["voice_setting"]["voice_id"],
        "audio_length": (data.get("extra_info") or {}).get("audio_length"),
        "audio_sample_rate": (data.get("extra_info") or {}).get("audio_sample_rate"),
        "status_msg": base_resp.get("status_msg"),
    }
    print(json.dumps(info, ensure_ascii=False))


def concat(args):
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = "ffmpeg"
    try:
        subprocess.run(
            [ffmpeg, "-version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit("ffmpeg is required for concat.") from exc

    inputs = [str(Path(item).resolve()) for item in args.inputs]
    with tempfile.TemporaryDirectory() as temp_dir:
        manifest = Path(temp_dir) / "concat.txt"
        lines = []
        for path in inputs:
            escaped = path.replace("'", "'\\''")
            lines.append(f"file '{escaped}'\n")
        manifest.write_text("".join(lines), encoding="utf-8")

        cmd = [
            ffmpeg, "-y", "-f", "concat", "-safe", "0",
            "-i", str(manifest), "-c", "copy", str(output),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            raise SystemExit(result.stderr.strip() or "ffmpeg concat failed.")

    print(str(output))


def build_parser():
    parser = argparse.ArgumentParser(description="Language Helper TTS tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    synth = subparsers.add_parser("synthesize", help="Send a TTS request and save audio")
    synth.add_argument("--text-file", required=True, help="UTF-8 text file containing the text")
    synth.add_argument("--voice-id", required=True, help="Voice identifier")
    synth.add_argument("--speed", type=float, help="Speech speed")
    synth.add_argument("--pitch", type=int, help="Pitch value")
    synth.add_argument("--vol", type=float, help="Volume multiplier")
    synth.add_argument("--format", help="Output format")
    synth.add_argument("--sample-rate", type=int, help="Output sample rate")
    synth.add_argument("--bitrate", type=int, help="MP3 bitrate")
    synth.add_argument("--channel", type=int, help="Number of audio channels")
    synth.add_argument("--output", required=True, help="Output audio path")
    synth.add_argument("--debug-log", help="Optional JSON debug log path")
    synth.set_defaults(func=synthesize)

    merge = subparsers.add_parser("concat", help="Concatenate multiple audio segments with ffmpeg")
    merge.add_argument("--output", required=True, help="Merged output path")
    merge.add_argument("inputs", nargs="+", help="Input audio files in playback order")
    merge.set_defaults(func=concat)

    return parser


def main():
    _configure_stdio()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
