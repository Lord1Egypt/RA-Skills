#!/usr/bin/env python3
"""Speaker identification using UniSpeech-SAT x-vector embeddings.

Compare input audio against voice reference files in a library.
Reports ranked matches by cosine similarity or "unknown" if below threshold.

Usage:
  python3 voice_identify.py <audio_file> [--threshold 0.75] [--voice-dir ./voice-refs]

Requirements:
  pip install transformers librosa torch
  First run downloads model (~360MB) to /tmp/hf_models/
"""

import sys
import os
import glob
import argparse
import numpy as np
import librosa
import torch
from transformers import AutoFeatureExtractor, UniSpeechSatForXVector

MODEL_NAME = "microsoft/unispeech-sat-base-sv"
MODEL_CACHE = "/tmp/hf_models/unispeech-sat"

# Map filename prefixes to display names.
# Edit this dict to register new speakers in your voice library.
# Example: "alice": "Alice", "bob": "Bob"
SPEAKER_MAP = {
    # "alice": "Alice",
    # "bob": "Bob",
}

def get_speaker_name(filename):
    """Extract speaker name from filename like 'alice-ref1.ogg'."""
    basename = os.path.basename(filename)
    for key, name in SPEAKER_MAP.items():
        if basename.startswith(key):
            return name
    # Fallback: use filename prefix before '-ref'
    parts = basename.split("-ref")
    return parts[0] if len(parts) > 1 else basename

def load_audio(path, sr=16000):
    """Load audio and resample to 16kHz mono."""
    audio, _ = librosa.load(path, sr=sr, mono=True)
    return audio

def get_embedding(model, feature_extractor, audio):
    """Extract speaker x-vector embedding from audio."""
    inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.embeddings.squeeze()
    return embedding

def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def main():
    parser = argparse.ArgumentParser(description="Identify speaker from voice library")
    parser.add_argument("audio", help="Path to audio file to identify")
    parser.add_argument("--threshold", type=float, default=0.75,
                        help="Minimum cosine similarity to consider a match (default: 0.75)")
    parser.add_argument("--voice-dir", default=None,
                        help="Path to voice references directory (default: voice-refs/ relative to script)")
    args = parser.parse_args()

    if not os.path.exists(args.audio):
        print(f"Error: File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    voice_dir = args.voice_dir or os.path.join(os.path.dirname(__file__), "..", "voice-refs")
    if not os.path.isdir(voice_dir):
        # Fallback: try workspace root
        workspace_voice_dir = os.path.join(os.path.dirname(__file__), "..", "..", "voice-refs")
        if os.path.isdir(workspace_voice_dir):
            voice_dir = workspace_voice_dir
        else:
            print(f"Error: Voice refs directory not found: {voice_dir}", file=sys.stderr)
            sys.exit(1)

    print("Loading model...", file=sys.stderr)
    feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE)
    model = UniSpeechSatForXVector.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE)
    model.eval()

    print("Processing input audio...", file=sys.stderr)
    input_audio = load_audio(args.audio)
    if len(input_audio) > 16000 * 30:
        input_audio = input_audio[:16000 * 30]
    input_emb = get_embedding(model, feature_extractor, input_audio)

    ref_files = sorted(glob.glob(os.path.join(voice_dir, "*-ref*.*")))
    if not ref_files:
        print(f"Error: No reference audio files found in {voice_dir}", file=sys.stderr)
        sys.exit(1)

    results = []
    for ref_file in ref_files:
        speaker = get_speaker_name(ref_file)
        print(f"Comparing with {speaker} ({os.path.basename(ref_file)})...", file=sys.stderr)
        try:
            ref_audio = load_audio(ref_file)
            if len(ref_audio) > 16000 * 30:
                ref_audio = ref_audio[:16000 * 30]
            ref_emb = get_embedding(model, feature_extractor, ref_audio)
            sim = cosine_similarity(input_emb, ref_emb)
            results.append((speaker, os.path.basename(ref_file), sim))
        except Exception as e:
            print(f"  Warning: Failed to process {ref_file}: {e}", file=sys.stderr)

    results.sort(key=lambda x: x[2], reverse=True)

    print("\n=== Voice Identification Results ===")
    for speaker, filename, sim in results:
        marker = " ✓ MATCH" if sim >= args.threshold else ""
        print(f"  {speaker} ({filename}): {sim:.4f}{marker}")

    if results and results[0][2] >= args.threshold:
        print(f"\n→ Most likely: {results[0][0]} (similarity: {results[0][2]:.4f})")
    else:
        best = results[0] if results else None
        if best:
            print(f"\n→ Unknown speaker (best match: {best[0]} at {best[2]:.4f}, below threshold {args.threshold})")
        else:
            print("\n→ No reference voices to compare against")

if __name__ == "__main__":
    main()
