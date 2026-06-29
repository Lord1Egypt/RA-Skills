#!/usr/bin/env python3
"""Source separation helper for local music-craft workflows.

Demucs is optional. When installed, this script writes normalized stem paths and
a `stems.json` report that downstream helpers can consume. It does not install
anything automatically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


DEFAULT_STEMS = ("vocals", "drums", "bass", "other")


def planned_stem_paths(out_dir: Path, stems: list[str] | tuple[str, ...]) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    return {stem: out_dir / f"{stem}.wav" for stem in stems}


def _cache_key(audio_path: Path, model: str, stems: list[str]) -> str:
    try:
        stat = audio_path.stat()
        raw = f"{audio_path}|{stat.st_mtime_ns}|{stat.st_size}|{model}|{','.join(sorted(stems))}"
    except OSError:
        raw = f"{audio_path}|{model}|{','.join(sorted(stems))}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _load_optional_demucs():
    try:
        from demucs.apply import apply_model  # type: ignore
        from demucs.audio import AudioFile  # type: ignore
        from demucs.pretrained import get_model  # type: ignore
        import torch  # type: ignore
        import torchaudio  # type: ignore
    except ImportError as exc:
        raise RuntimeError("demucs, torch, and torchaudio are required; install with: pip install demucs") from exc
    return apply_model, AudioFile, get_model, torch, torchaudio


def separate_stems(
    audio_path: Path,
    out_dir: Path | None = None,
    model_name: str = "htdemucs",
    stems: list[str] | None = None,
    device: str = "cpu",
    shifts: int = 0,
) -> dict[str, object]:
    if stems is None:
        stems = list(DEFAULT_STEMS)
    if not audio_path.exists():
        raise FileNotFoundError(f"audio file not found: {audio_path}")
    if out_dir is None:
        out_dir = Path.home() / ".cache" / "openclaw" / "music-craft-stems" / _cache_key(audio_path, model_name, stems)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem_paths = planned_stem_paths(out_dir, stems)
    if all(path.exists() and path.stat().st_size > 0 for path in stem_paths.values()):
        return {
            "status": "ok",
            "cache": "hit",
            "model": model_name,
            "out_dir": str(out_dir),
            "stems": {name: str(path) for name, path in stem_paths.items()},
        }

    apply_model, AudioFile, get_model, torch, torchaudio = _load_optional_demucs()
    model = get_model(model_name)
    model.to(device)
    model.eval()
    wav = AudioFile(str(audio_path)).read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / (ref.std() + 1e-8)
    with torch.no_grad():
        sources = apply_model(model, wav[None], shifts=shifts, split=True, overlap=0.25, device=device)[0]
    sources = sources * (ref.std() + 1e-8) + ref.mean()

    model_sources = list(model.sources)
    for index, stem_name in enumerate(model_sources):
        if stem_name not in stem_paths:
            continue
        torchaudio.save(str(stem_paths[stem_name]), sources[index].cpu(), model.samplerate)

    result = {
        "status": "ok",
        "cache": "miss",
        "model": model_name,
        "out_dir": str(out_dir),
        "stems": {name: str(path) for name, path in stem_paths.items()},
    }
    report_path = out_dir / "stems.json"
    report_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Separate local audio into stems with Demucs")
    parser.add_argument("audio", type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--model", default="htdemucs", choices=["htdemucs", "htdemucs_ft", "htdemucs_6s"])
    parser.add_argument("--stems", default="vocals,drums,bass,other")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    parser.add_argument("--shifts", type=int, default=0)
    args = parser.parse_args(argv)

    stems = [stem.strip() for stem in args.stems.split(",") if stem.strip()]
    try:
        result = separate_stems(
            args.audio.expanduser(),
            out_dir=args.out_dir.expanduser() if args.out_dir else None,
            model_name=args.model,
            stems=stems,
            device=args.device,
            shifts=args.shifts,
        )
    except Exception as exc:  # noqa: BLE001 - CLI emits JSON errors
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
