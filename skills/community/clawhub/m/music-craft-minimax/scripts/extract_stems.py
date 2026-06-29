#!/usr/bin/env python3
"""extract_stems.py — Source separation via Demucs (vocals / drums / bass / other).

Wraps Meta's Demucs (https://github.com/facebookresearch/demucs) to separate an
input audio file into its component stems. The vocal stem is then usable as a
clean input to analyze_vocal_emotion.py — the absence of drums/bass masking
dramatically improves pitch tracking, HNR, and Whisper lyrics accuracy.

Default model is htdemucs (MIT-licensed). The htdemucs_ft model has CC-BY-NC
weights and is opt-in via --model htdemucs_ft.

Usage:
    python3 extract_stems.py <input.wav> --out-dir /tmp/stems
    python3 extract_stems.py song.mp3 --out-dir /tmp/stems --model htdemucs
    python3 extract_stems.py song.wav --stems vocals,drums

Output:
    /tmp/stems/<basename>/vocals.wav
    /tmp/stems/<basename>/drums.wav
    /tmp/stems/<basename>/bass.wav
    /tmp/stems/<basename>/other.wav
    Plus a JSON report: /tmp/stems/<basename>/stems.json
"""
import sys
import os
import json
import argparse
import hashlib
import warnings
from pathlib import Path

# Optional: torchaudio for fast wav writing; demucs requires torch anyway
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import torchaudio
    HAS_TORCHAUDIO = True
except ImportError:
    HAS_TORCHAUDIO = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Demucs is optional — graceful fallback with install hint
try:
    from demucs.pretrained import get_model
    HAS_DEMUCS = True
except ImportError:
    HAS_DEMUCS = False

# Soundfile for wav IO fallback
try:
    import soundfile as sf
    HAS_SF = True
except ImportError:
    HAS_SF = False


def cache_key(audio_path, model_name, target_stems):
    """Cache key: file content hash is too slow for large files; use path+mtime+size+model."""
    try:
        st = os.stat(audio_path)
        sig = f"{audio_path}|{st.st_mtime}|{st.st_size}|{model_name}|{','.join(sorted(target_stems))}"
        return hashlib.sha256(sig.encode()).hexdigest()[:16]
    except OSError:
        return hashlib.sha256(audio_path.encode()).hexdigest()[:16]


def load_audio(audio_path, target_sr=44100):
    """Load audio to (channels, samples) tensor at target_sr.

    Prefers torchaudio (fast, but needs torchcodec installed for some formats).
    Falls back to soundfile + numpy for portability — handles WAV/MP3/FLAC
    through libsndfile and demucs' built-in audio loading.
    """
    if not HAS_TORCH:
        raise RuntimeError("torch required for extract_stems.py — pip install torch demucs")
    # Try soundfile first (more portable, no torchcodec dependency)
    if HAS_SF and HAS_NUMPY:
        try:
            data, sr = sf.read(audio_path, always_2d=True)
            wav = torch.from_numpy(data.T.astype(np.float32))
            if sr != target_sr:
                import scipy.signal  # type: ignore
                num_samples = int(wav.shape[-1] * target_sr / sr)
                wav = torch.from_numpy(
                    scipy.signal.resample(wav.numpy(), num_samples, axis=-1)
                ).float()
                sr = target_sr
            return wav, sr
        except Exception:
            pass
    if HAS_TORCHAUDIO:
        wav, sr = torchaudio.load(audio_path)
        if sr != target_sr:
            wav = torchaudio.functional.resample(wav, sr, target_sr)
        return wav, target_sr
    raise RuntimeError("Need soundfile (with numpy) or torchaudio to load audio")


def save_wav(path, wav_tensor, sr):
    """Save (channels, samples) tensor to wav. Prefers soundfile for portability."""
    if HAS_SF and HAS_NUMPY:
        sf.write(path, wav_tensor.cpu().numpy().T, sr)
    elif HAS_TORCHAUDIO:
        torchaudio.save(path, wav_tensor.cpu(), sr)
    else:
        raise RuntimeError("Need soundfile (with numpy) or torchaudio to save wavs")


def separate_stems(audio_path, model_name='htdemucs', target_stems=None, device='cpu',
                   out_dir=None, segment=None, shifts=0):
    """Run Demucs source separation.

    Args:
        audio_path: input audio file
        model_name: 'htdemucs' (MIT, default) or 'htdemucs_ft' (CC-BY-NC, opt-in)
        target_stems: list of stem names to extract. Default: all 4.
            For analyzing vocal emotion, just ['vocals'] is fastest.
        device: 'cpu' or 'cuda'
        out_dir: where to write stems. Default: ~/.cache/openclaw/stems/<key>/
        segment: Demucs segment length in seconds (None = auto)
        shifts: Demucs random shifts for quality (0 = fastest, 5 = best)

    Returns:
        dict with 'stems' (paths), 'duration_seconds', 'sample_rate', 'model'
    """
    if not HAS_DEMUCS:
        return {
            'error': 'demucs not installed',
            'install': 'pip install demucs',
        }

    if target_stems is None:
        target_stems = ['vocals', 'drums', 'bass', 'other']

    if out_dir is None:
        cache_k = cache_key(audio_path, model_name, target_stems)
        out_dir = os.path.expanduser(f"~/.cache/openclaw/stems/{cache_k}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Check cache: if all target stems already exist, skip
    stem_paths = {s: out_dir / f"{s}.wav" for s in target_stems}
    if all(p.exists() and p.stat().st_size > 0 for p in stem_paths.values()):
        return {
            'stems': {k: str(v) for k, v in stem_paths.items()},
            'duration_seconds': _wav_duration_seconds(str(stem_paths[target_stems[0]])),
            'sample_rate': 44100,
            'model': model_name,
            'cache': 'hit',
            'out_dir': str(out_dir),
        }

    print(f"Loading model: {model_name} (device={device})", file=sys.stderr)
    from demucs.apply import apply_model
    model = get_model(model_name)
    model.to(device)
    model.eval()

    print(f"Loading audio: {audio_path}", file=sys.stderr)
    wav, sr = load_audio(audio_path, target_sr=model.samplerate)
    duration = wav.shape[-1] / sr
    print(f"  duration: {duration:.1f}s, channels: {wav.shape[0]}", file=sys.stderr)

    # Demucs 4.x: use apply_model (handles overlapping + batching for long audio)
    print(f"  running separation (shifts={shifts})...", file=sys.stderr)
    if HAS_TORCH:
        with torch.no_grad():
            sources = apply_model(
                model, wav.unsqueeze(0), shifts=shifts, num_workers=0,
                progress=False, device=device,
            )
    else:
        sources = apply_model(
            model, wav.unsqueeze(0), shifts=shifts, num_workers=0,
            progress=False, device=device,
        )
    # sources shape: (batch, n_sources, channels, samples)
    sources = sources[0]

    # Save requested stems
    for i, stem_name in enumerate(model.sources):
        if stem_name not in target_stems:
            continue
        stem_tensor = sources[i]  # (channels, samples)
        out_path = stem_paths[stem_name]
        save_wav(str(out_path), stem_tensor, sr)
        print(f"  Wrote: {out_path}", file=sys.stderr)

    result = {
        'stems': {k: str(v) for k, v in stem_paths.items()},
        'duration_seconds': round(duration, 1),
        'sample_rate': sr,
        'model': model_name,
        'cache': 'miss',
        'out_dir': str(out_dir),
    }

    # Write report
    report_path = out_dir / "stems.json"
    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)

    return result


def _wav_duration_seconds(path):
    """Quickly read wav duration via soundfile or torchaudio."""
    try:
        if HAS_SF:
            info = sf.info(path)
            return round(info.frames / info.samplerate, 1)
        if HAS_TORCHAUDIO:
            info = torchaudio.info(path)
            return round(info.num_frames / info.sample_rate, 1)
    except Exception:
        return 0
    return 0


def main():
    parser = argparse.ArgumentParser(description='Source-separate audio with Demucs')
    parser.add_argument('audio', help='Input audio file (WAV/MP3/FLAC)')
    parser.add_argument('--out-dir', help='Output directory for stems (default: ~/.cache/openclaw/stems/<key>/)')
    parser.add_argument('--model', default='htdemucs',
                        choices=['htdemucs', 'htdemucs_ft', 'htdemucs_6s'],
                        help='Demucs model (default: htdemucs, MIT-licensed). '
                             'htdemucs_ft has CC-BY-NC weights — opt-in only for non-commercial use.')
    parser.add_argument('--stems', default='vocals,drums,bass,other',
                        help='Comma-separated stem names to extract')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'],
                        help='Device for Demucs inference (default: cpu)')
    parser.add_argument('--shifts', type=int, default=0,
                        help='Demucs random shifts for quality (0 = fastest, default)')
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"ERROR: audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    target_stems = [s.strip() for s in args.stems.split(',') if s.strip()]
    result = separate_stems(
        audio_path=args.audio,
        model_name=args.model,
        target_stems=target_stems,
        device=args.device,
        out_dir=args.out_dir,
        shifts=args.shifts,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
