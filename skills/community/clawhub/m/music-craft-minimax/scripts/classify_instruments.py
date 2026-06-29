#!/usr/bin/env python3
"""classify_instruments.py — 527-class audio tagging via MIT's AST.

Wraps the Audio Spectrogram Transformer (AST, MIT/ast-finetuned-audioset-10-10-0.4593)
for fine-grained instrument / sound-event classification. 527 AudioSet classes
includes both common (guitar, drums, piano) and edge (oud, sitar, harmonica,
turntabilism) instruments that CLAP often misses.

Cache disclosure: this script writes AST classification results to
~/.cache/openclaw/ast/ to speed up repeated runs on the same audio.
Pass --no-cache to disable. The AST model itself is fetched via
from_pretrained() on first use (network access required once).

Usage:
    python3 classify_instruments.py <input.wav> [--output out.json] [--top-k 20]

Output:
    {
      "duration_seconds": 228.6,
      "top_instruments": [
        {"label": "Electric guitar", "score": 0.85},
        {"label": "Rock music", "score": 0.72},
        ...
      ],
      "model": "MIT/ast-finetuned-audioset-10-10-0.4593"
    }
"""
import sys
import os
import json
import argparse
import hashlib
from pathlib import Path

# Optional: torch + transformers
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    import soundfile as sf
    import numpy as np
    HAS_SF = True
except ImportError:
    HAS_SF = False


_AST_MODEL = None
_AST_EXTRACTOR = None
_AST_MODEL_ID = 'MIT/ast-finetuned-audioset-10-10-0.4593'


def cache_key(audio_path):
    try:
        st = os.stat(audio_path)
        sig = f"{audio_path}|{st.st_mtime}|{st.st_size}|ast_audioset"
        return hashlib.sha256(sig.encode()).hexdigest()[:16]
    except OSError:
        return hashlib.sha256(audio_path.encode()).hexdigest()[:16]


def _load_cached(audio_path, cache_dir):
    cache_file = Path(cache_dir) / f"{cache_key(audio_path)}.json"
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                return json.load(f)
        except Exception:
            return None
    return None


def _save_cached(audio_path, cache_dir, result):
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    cache_file = Path(cache_dir) / f"{cache_key(audio_path)}.json"
    with open(cache_file, 'w') as f:
        json.dump(result, f, indent=2)


def _load_model():
    global _AST_MODEL, _AST_EXTRACTOR
    if _AST_MODEL is None:
        _AST_EXTRACTOR = AutoFeatureExtractor.from_pretrained(_AST_MODEL_ID)
        _AST_MODEL = AutoModelForAudioClassification.from_pretrained(_AST_MODEL_ID)
        _AST_MODEL.eval()
    return _AST_MODEL, _AST_EXTRACTOR


def classify_instruments(audio_path, top_k=20, device='cpu', cache_dir=None, use_cache=True):
    """Classify audio with AST and return top-k AudioSet labels.

    Args:
        audio_path: input audio file
        top_k: how many top classes to return
        device: 'cpu' or 'cuda'
        cache_dir: optional cache directory (default: ~/.cache/openclaw/ast/).
            Ignored when use_cache is False.
        use_cache: when True (default), read and write the on-disk cache.
            Set False to skip caching entirely.

    Returns:
        dict with top_instruments (list of {label, score}) and metadata.
    """
    if not HAS_TORCH or not HAS_TRANSFORMERS:
        return {
            'error': 'torch + transformers required',
            'install': "pip install 'transformers>=4.40' torch",
        }

    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/openclaw/ast")

    if use_cache:
        cached = _load_cached(audio_path, cache_dir)
        if cached is not None:
            cached['_cache'] = 'hit'
            # Trim to top_k
            if 'top_instruments' in cached:
                cached['top_instruments'] = cached['top_instruments'][:top_k]
            return cached
    else:
        # Caller asked to skip caching; do not touch the cache directory at all.
        cache_dir = None

    if not HAS_SF:
        return {'error': 'soundfile required', 'install': 'pip install soundfile'}

    # Load audio
    import time
    t0 = time.time()
    data, sr = sf.read(audio_path, always_2d=False)
    if data.ndim > 1:
        data = data.mean(axis=1)  # to mono
    duration = len(data) / sr
    print(f"Classifying {duration:.1f}s with AST (device={device})", file=sys.stderr)

    model, extractor = _load_model()
    model.to(device)

    # AST expects 16kHz mono
    if sr != 16000:
        data_t = torch.from_numpy(data.astype(np.float32))
        data_t = torch.nn.functional.interpolate(
            data_t.unsqueeze(0).unsqueeze(0), scale_factor=16000/sr, mode='linear',
        ).squeeze().numpy()

    # Process in 10s chunks (AST limit is ~10s for 128-mel)
    chunk_seconds = 10
    chunk_samples = 16000 * chunk_seconds
    n_chunks = max(1, int(np.ceil(len(data_t) / chunk_samples)))
    all_logits = []
    with torch.no_grad():
        for i in range(n_chunks):
            start = i * chunk_samples
            end = min(start + chunk_samples, len(data_t))
            chunk = data_t[start:end]
            # Pad if needed
            if len(chunk) < chunk_samples:
                chunk = np.pad(chunk, (0, chunk_samples - len(chunk)))
            inputs = extractor(
                chunk, sampling_rate=16000, return_tensors='pt',
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            outputs = model(**inputs)
            logits = outputs.logits[0].cpu().numpy()
            all_logits.append(logits)

    # Mean-pool logits across chunks, then sigmoid (multi-label classification)
    mean_logits = np.mean(all_logits, axis=0)
    # AudioSet is multi-label: use sigmoid, not softmax
    scores = 1.0 / (1.0 + np.exp(-mean_logits))  # sigmoid

    # Top-k
    top_indices = np.argsort(-scores)[:top_k]
    top_instruments = [
        {'label': model.config.id2label[int(i)], 'score': round(float(scores[i]), 4)}
        for i in top_indices
    ]

    result = {
        'duration_seconds': round(duration, 2),
        'top_instruments': top_instruments,
        'top_genres': [t for t in top_instruments if any(g in t['label'].lower()
                        for g in ['music', 'rock', 'pop', 'jazz', 'classical', 'blues', 'electronic', 'hip hop', 'metal'])][:5],
        'model': _AST_MODEL_ID,
        'compute_seconds': round(time.time() - t0, 2),
        'n_chunks': n_chunks,
        '_cache': 'miss',
    }

    if use_cache and cache_dir:
        print(f"notice: caching AST results to {cache_dir} (pass --no-cache to disable)",
              file=sys.stderr)
        try:
            _save_cached(audio_path, cache_dir, result)
        except Exception as e:
            print(f"Cache write failed: {e}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(description='527-class instrument tagging via MIT AST')
    parser.add_argument('audio', help='Input audio file (WAV/MP3/FLAC)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--top-k', type=int, default=20, help='Number of top classes to return')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'])
    parser.add_argument('--no-cache', action='store_true',
                        help='Skip the ~/.cache/openclaw/ast cache (no read, no write).')
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"ERROR: audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    result = classify_instruments(
        args.audio,
        top_k=args.top_k,
        device=args.device,
        use_cache=not args.no_cache,
    )

    json_out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
