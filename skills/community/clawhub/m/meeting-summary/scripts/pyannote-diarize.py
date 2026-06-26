#!/usr/bin/env python3
"""Run local speaker diarization with pyannote community-1.

This wrapper avoids torchcodec decoding by loading audio with soundfile and
passing an in-memory waveform dictionary to the pipeline.
"""

import argparse
import json
import os
import sys

import numpy as np
import soundfile as sf
import torch
from pyannote.audio import Pipeline

DEFAULT_MODEL_ID = "pyannote/speaker-diarization-community-1"
DEFAULT_LOCAL_PIPELINE_PATH = os.path.expanduser("~/.openclaw/workspace/models/pyannote-community-1")


def load_audio(path: str):
    data, sr = sf.read(path, dtype="float32")
    if data.ndim > 1:
        data = np.mean(data, axis=1)
    waveform = torch.from_numpy(data).unsqueeze(0)
    return {"waveform": waveform, "sample_rate": sr}


def load_pipeline(args):
    pipeline_path = args.pipeline_path or os.environ.get("PYANNOTE_PIPELINE_PATH", "") or DEFAULT_LOCAL_PIPELINE_PATH
    hf_token = args.hf_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN") or ""
    model_id = args.model_id

    # Strategy 1: try loading from local path (as a config file)
    if pipeline_path:
        config_file = pipeline_path
        if os.path.isdir(pipeline_path):
            config_file = os.path.join(pipeline_path, "config.yaml")
        if os.path.isfile(config_file):
            try:
                return Pipeline.from_pretrained(config_file)
            except Exception:
                pass  # fall through to other strategies

    # Strategy 2: try loading from HF hub (uses cache if available)
    try:
        if hf_token:
            return Pipeline.from_pretrained(model_id, use_auth_token=hf_token)
        else:
            return Pipeline.from_pretrained(model_id)
    except Exception:
        pass

    raise RuntimeError(
        "Pyannote pipeline is not available. Tried local path and HF hub.\n"
        "Set PYANNOTE_PIPELINE_PATH to a local clone, or provide HF_TOKEN after "
        "accepting the pyannote/speaker-diarization-community-1 agreement at "
        "https://hf.co/pyannote/speaker-diarization-community-1"
    )


def main():
    parser = argparse.ArgumentParser(description="Run pyannote speaker diarization locally")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="Hugging Face model id")
    parser.add_argument("--pipeline-path", default="", help="Local pyannote pipeline directory")
    parser.add_argument("--hf-token", default="", help="Hugging Face token")
    parser.add_argument("--num-speakers", type=int, help="Known speaker count hint")
    args = parser.parse_args()

    pipeline = load_pipeline(args)
    audio = load_audio(args.audio)
    kwargs = {}
    if args.num_speakers:
        kwargs["num_speakers"] = args.num_speakers
    diarization = pipeline(audio, **kwargs)

    annotation = getattr(diarization, "exclusive_speaker_diarization", None)
    if annotation is None:
        annotation = getattr(diarization, "speaker_diarization", diarization)
    if not hasattr(annotation, "itertracks"):
        raise RuntimeError(f"Unsupported pyannote diarization output: {type(diarization).__name__}")

    segments = []
    for turn, _, speaker in annotation.itertracks(yield_label=True):
        segments.append(
            {
                "start_time": int(turn.start * 1000),
                "end_time": int(turn.end * 1000),
                "speaker_hint": speaker,
                "source": "pyannote",
            }
        )

    output = {
        "segments": segments,
        "speaker_hints": sorted({seg["speaker_hint"] for seg in segments}),
        "backend": "pyannote-community-1",
        "annotation_type": type(annotation).__name__,
    }

    payload = json.dumps(output, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(payload)
    print(payload)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)
