import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

MAX_TEXT = 10_000
ALLOWED_MODELS = {"tiny", "base", "small", "medium", "large", "turbo"}


def _workspace_root() -> Path:
    return Path.cwd().resolve()


def validate_file_path(file_path, must_exist=True) -> str:
    """Resolve a path and keep it inside the current workspace, including symlinks."""
    if not file_path or not isinstance(file_path, str):
        raise ValueError("file_path is required")
    root = _workspace_root()
    candidate = Path(file_path).expanduser()
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Access denied: path must stay inside workspace ({root})") from exc
    if must_exist and not resolved.exists():
        raise FileNotFoundError(f"File not found: {resolved}")
    if must_exist and not resolved.is_file():
        raise ValueError(f"Input is not a regular file: {resolved}")
    if not must_exist:
        resolved.parent.mkdir(parents=True, exist_ok=True)
        try:
            resolved.parent.resolve().relative_to(root)
        except ValueError as exc:
            raise ValueError("Access denied: output directory escapes workspace") from exc
    return str(resolved)


def get_whisper():
    import whisper
    return whisper


def get_gtts():
    from gtts import gTTS
    return gTTS


def get_librosa():
    import librosa
    return librosa


def run_ffmpeg(args):
    if not shutil.which("ffmpeg"):
        return False, "ffmpeg not found in PATH"
    try:
        process = subprocess.run(
            ["ffmpeg", "-nostdin", "-hide_banner", "-y", *args],
            check=True, capture_output=True, text=True, timeout=900,
        )
        return True, process.stderr
    except subprocess.TimeoutExpired:
        return False, "FFmpeg timed out after 900 seconds"
    except subprocess.CalledProcessError as exc:
        return False, exc.stderr or str(exc)
    except OSError as exc:
        return False, str(exc)


def transcribe(file_path, model_name="base"):
    try:
        safe_path = validate_file_path(file_path)
        if model_name not in ALLOWED_MODELS:
            raise ValueError(f"Unsupported model; choose one of {sorted(ALLOWED_MODELS)}")
        result = get_whisper().load_model(model_name).transcribe(safe_path)
        return {"text": result.get("text", ""), "segments": result.get("segments", [])}
    except Exception as exc:
        return {"error": str(exc)}


def tts(text, output_path=None, lang="en", allow_network=False):
    try:
        if not allow_network:
            raise ValueError("Remote Google TTS is disabled by default; pass --allow-network after confirming text may be sent to Google")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")
        if len(text) > MAX_TEXT:
            raise ValueError(f"text too long (max {MAX_TEXT} characters)")
        if not isinstance(lang, str) or not re.fullmatch(r"[a-z]{2,3}(?:-[A-Z]{2})?", lang):
            raise ValueError("lang must be a language code such as en or fr")
        safe_output = validate_file_path(output_path or f"tts_{int(time.time())}.mp3", must_exist=False)
        get_gtts()(text=text, lang=lang).save(safe_output)
        return {"file_path": safe_output, "status": "created"}
    except Exception as exc:
        return {"error": str(exc)}


def extract_features(file_path):
    try:
        y, sr = get_librosa().load(validate_file_path(file_path), sr=None, mono=True)
        librosa = get_librosa()
        return {
            "duration": float(librosa.get_duration(y=y, sr=sr)),
            "sample_rate": int(sr),
            "mfcc_mean": librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1).tolist(),
            "rms_mean": float(librosa.feature.rms(y=y).mean()),
        }
    except Exception as exc:
        return {"error": str(exc)}


def vad_segments(file_path, aggressiveness=2):
    try:
        safe_path = validate_file_path(file_path)
        if not isinstance(aggressiveness, int) or aggressiveness not in range(4):
            raise ValueError("aggressiveness must be an integer from 0 to 3")
        threshold = -30 - (aggressiveness * 5)
        ok, stderr = run_ffmpeg(["-i", safe_path, "-af", f"silencedetect=noise={threshold}dB:d=0.3", "-f", "null", "-"])
        if not ok:
            return {"error": f"FFmpeg VAD failed: {stderr}"}
        starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", stderr)]
        ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", stderr)]
        duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", stderr)
        duration = (int(duration_match.group(1)) * 3600 + int(duration_match.group(2)) * 60 + float(duration_match.group(3))) if duration_match else 0.0
        silences = []
        for i, start in enumerate(starts):
            end = ends[i] if i < len(ends) else duration
            if end > start:
                silences.append((max(0.0, start), min(duration, end)))
        segments = []
        cursor = 0.0
        for start, end in silences:
            if start > cursor:
                segments.append({"start": round(cursor, 3), "end": round(start, 3)})
            cursor = max(cursor, end)
        if duration > cursor:
            segments.append({"start": round(cursor, 3), "end": round(duration, 3)})
        return {"segments": segments}
    except Exception as exc:
        return {"error": str(exc)}


def transform(file_path, operations):
    try:
        safe_path = validate_file_path(file_path)
        if not isinstance(operations, list) or not operations:
            raise ValueError("operations must be a non-empty JSON array")
        filters = []
        cmd = ["-i", safe_path]
        for op in operations:
            if not isinstance(op, dict) or op.get("op") not in {"trim", "resample", "normalize"}:
                raise ValueError("each operation must be trim, resample, or normalize")
            kind = op["op"]
            if kind == "trim":
                start = float(op.get("start", 0))
                end = float(op["end"]) if "end" in op else None
                if start < 0 or (end is not None and (end <= start)):
                    raise ValueError("trim requires 0 <= start < end")
                cmd = ["-ss", f"{start:g}", *cmd]
                if end is not None:
                    cmd += ["-t", f"{end - start:g}"]
            elif kind == "resample":
                rate = int(op.get("rate", 0))
                if rate < 8_000 or rate > 192_000:
                    raise ValueError("resample rate must be between 8000 and 192000 Hz")
                cmd += ["-ar", str(rate)]
            else:
                filters.append("loudnorm")
        if filters:
            cmd += ["-af", ",".join(filters)]
        output = validate_file_path(str(Path(safe_path).with_suffix(".processed.wav")), must_exist=False)
        ok, err = run_ffmpeg([*cmd, "-map_metadata", "-1", output])
        return {"file_path": output} if ok else {"error": f"FFmpeg failed: {err}"}
    except Exception as exc:
        return {"error": str(exc)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["transcribe", "tts", "extract_features", "vad_segments", "transform"])
    parser.add_argument("--file_path"); parser.add_argument("--text"); parser.add_argument("--output_path")
    parser.add_argument("--model", default="base"); parser.add_argument("--ops"); parser.add_argument("--aggressiveness", type=int, default=2)
    parser.add_argument("--lang", default="en"); parser.add_argument("--allow-network", action="store_true")
    args = parser.parse_args()
    if args.action in {"transcribe", "extract_features", "vad_segments", "transform"} and not args.file_path:
        parser.error("--file_path is required")
    if args.action == "transcribe": result = transcribe(args.file_path, args.model)
    elif args.action == "tts": result = tts(args.text, args.output_path, args.lang, args.allow_network)
    elif args.action == "extract_features": result = extract_features(args.file_path)
    elif args.action == "vad_segments": result = vad_segments(args.file_path, args.aggressiveness)
    else:
        try: operations = json.loads(args.ops or "[]")
        except json.JSONDecodeError: result = {"error": "Invalid JSON for --ops"}
        else: result = transform(args.file_path, operations)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
