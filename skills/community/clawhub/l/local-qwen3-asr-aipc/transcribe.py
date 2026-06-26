SKILL_VERSION = "__SKILL_VERSION__"  # placeholder — replaced by setup.py with SKILL.md version on deploy
import sys, io, os, json, string, argparse
from pathlib import Path

_STATE_CACHE = None
_MODEL_CACHE = None
_MODEL_CACHE_KEY = None

# Qwen3-ASR API supports long audio natively; no manual chunking needed.
# Truncation is controlled by max_new_tokens; 4096 covers ~30 minutes.
MAX_NEW_TOKENS = 4096
# max_inference_batch_size controls internal concurrency; 32 is the recommended value.
MAX_BATCH_SIZE = 32


def get_state():
    global _STATE_CACHE
    if _STATE_CACHE is not None:
        return _STATE_CACHE
    for d in string.ascii_uppercase:
        sf = Path(f"{d}:\\") / f"{os.environ.get('USERNAME', 'user').lower()}_openvino" / "asr" / "state.json"
        if sf.exists():
            _STATE_CACHE = json.loads(sf.read_text(encoding='utf-8'))
            return _STATE_CACHE
    return None


def get_device():
    import openvino as ov
    core = ov.Core()
    devs = core.available_devices
    print(f"[INFO] Devices: {devs}", file=sys.stderr)
    for d in devs:
        if "GPU" in d:
            print(f"[INFO] Using {d}", file=sys.stderr)
            return d
    print("[INFO] Using CPU", file=sys.stderr)
    return "CPU"



def transcribe(audio_path, language=None, topic='', output_path=None):
    state = get_state()
    if not state:
        print("[ERROR] state.json not found - run setup.py", file=sys.stderr)
        sys.exit(1)

    asr_dir = Path(state['ASR_DIR'])
    sys.path.insert(0, str(asr_dir))

    model_dir = asr_dir / "Qwen3-ASR-0.6B-fp16-ov"

    if not Path(audio_path).exists():
        print(f"[ERROR] Audio not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    # load model (reused in-process)
    # max_new_tokens caps output tokens; this is the true cause of long-audio truncation
    device = get_device()
    from asr_engine import OVQwen3ASRModel
    global _MODEL_CACHE, _MODEL_CACHE_KEY
    model_key = (str(model_dir), str(device), MAX_NEW_TOKENS, MAX_BATCH_SIZE)
    if _MODEL_CACHE is None or _MODEL_CACHE_KEY != model_key:
        print(f"[INFO] Loading model: {model_dir} (max_new_tokens={MAX_NEW_TOKENS}, batch={MAX_BATCH_SIZE})", file=sys.stderr)
        _MODEL_CACHE = OVQwen3ASRModel.from_pretrained(
            str(model_dir),
            device=device,
            max_new_tokens=MAX_NEW_TOKENS,
            max_inference_batch_size=MAX_BATCH_SIZE,
        )
        _MODEL_CACHE_KEY = model_key
    else:
        print("[INFO] Reusing loaded model", file=sys.stderr)
    model = _MODEL_CACHE

    # normalize language: "auto"/empty/None all map to None (model API convention)
    if language in (None, '', 'auto', 'Auto', 'AUTO', 'none', 'null'):
        language = None

    import time
    t0 = time.time()
    # model API handles long audio internally; pass the full file
    results = model.transcribe(audio=str(audio_path), language=language)
    elapsed = time.time() - t0

    if not results:
        print("[ERROR] Empty transcription result", file=sys.stderr)
        sys.exit(1)

    result_data = {
        "text": results[0].text,
        "language": results[0].language,
        "time_elapsed": elapsed,
        "audio_path": str(audio_path),
    }
    print(f"[INFO] Language: {results[0].language} | Time: {elapsed:.2f}s", file=sys.stderr)
    return result_data


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--audio", required=True)
        parser.add_argument("--language", default=None)
        parser.add_argument("--topic", default='')
        parser.add_argument("--output", default=None)
        args = parser.parse_args()
        language = None if args.language in (None, '', 'None', 'none', 'null') else args.language
        result = transcribe(args.audio, language, args.topic, args.output)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        sys.stdout.flush()
    except Exception as exc:
        import traceback
        print(f"[FATAL] {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        sys.exit(1)

