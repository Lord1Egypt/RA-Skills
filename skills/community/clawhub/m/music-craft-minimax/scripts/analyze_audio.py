#!/usr/bin/env python3
"""analyze_audio.py — Extract musical features for song parody generation.

Usage:
    python3 analyze_audio.py <audio_file.wav>

Output: JSON with BPM, key, duration, energy profile, section estimates.
"""
import sys
import json
import librosa
import numpy as np

# Optional: transformers for CLAP zero-shot audio classification
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

# Shared audio feature utilities (key detection, tempo/energy classification,
# section estimation). See _audio_features.py for the canonical implementations.
from _audio_features import (
    detect_key,
    estimate_sections,
    classify_tempo,
    classify_energy,
)

# Default hop length for librosa energy/feature analysis. Used to convert frame indices
# back to time (frame * HOP_LENGTH / sr = seconds). Must match the hop_length used
# by librosa.feature.* in this file.
HOP_LENGTH = 512








def analyze(audio_path):
    print(f"Loading: {audio_path}", file=sys.stderr)
    y, sr = librosa.load(audio_path, sr=22050)

    # 1. Tempo / BPM
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_intervals = np.diff(beat_times) if len(beat_times) > 1 else np.array([0.5])
    tempo_consistency = float(1.0 - min(np.std(beat_intervals) / (np.mean(beat_intervals) + 1e-8), 1.0))

    # 2. Key detection
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)
    key, key_confidence = detect_key(chroma_avg)

    # 3. Duration
    duration = len(y) / sr

    # 4. RMS energy profile (20 samples across duration)
    rms = librosa.feature.rms(y=y)[0]
    rms_resampled = np.interp(
        np.linspace(0, len(rms) - 1, 20),
        np.arange(len(rms)),
        rms
    )
    energy_profile = [round(float(e), 5) for e in rms_resampled]
    energy_description = classify_energy(rms_resampled)

    # 5. Section estimation
    sections = estimate_sections(rms, sr, duration, hop_length=HOP_LENGTH)

    # 6. Onset density (notes per second — proxy for complexity)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_density = len(onset_frames) / duration

    # 7. Spectral features (brightness)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    avg_brightness = float(np.mean(spectral_centroid))
    brightness = "bright/treble-heavy" if avg_brightness > 3000 else \
                 "balanced" if avg_brightness > 1500 else "warm/bass-heavy"

    # 8. Tempo feel
    tempo_feel = classify_tempo(bpm)

    # 9. CLAP zero-shot classification (genre / mood / instruments / vocal style / era)
    if HAS_TRANSFORMERS:
        try:
            classifier = pipeline("zero-shot-audio-classification", model="laion/clap-htsat-unfused")
            candidate_labels = [
                # Genres
                "pop", "rock", "jazz", "blues", "classical", "electronic", "hip hop", "rnb",
                "country", "folk", "metal", "punk", "reggae", "latin", "soul", "funk",
                "disco", "house", "techno", "ambient", "indie", "alternative",
                "dream pop", "synthwave", "post-rock", "shoegaze", "lo-fi",
                # Moods
                "happy", "sad", "melancholic", "euphoric", "aggressive", "tender",
                "dark", "bright", "nostalgic", "epic", "peaceful", "tense",
                # Instruments
                "piano", "guitar", "drums", "bass", "synthesizer", "strings",
                "brass", "vocals", "choir", "organ", "saxophone", "violin",
                # Vocal style
                "female vocals", "male vocals", "duet", "choir vocals",
                # Era
                "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s",
            ]
            results = classifier(audio_path, candidate_labels=candidate_labels)
            # Take top results per category
            genre_labels = ["pop", "rock", "jazz", "blues", "classical", "electronic", "hip hop",
                            "rnb", "country", "folk", "metal", "punk", "reggae", "latin", "soul",
                            "funk", "disco", "house", "techno", "ambient", "indie", "alternative",
                            "dream pop", "synthwave", "post-rock", "shoegaze", "lo-fi"]
            mood_labels = ["happy", "sad", "melancholic", "euphoric", "aggressive", "tender",
                           "dark", "bright", "nostalgic", "epic", "peaceful", "tense"]
            instrument_labels = ["piano", "guitar", "drums", "bass", "synthesizer", "strings",
                                "brass", "vocals", "choir", "organ", "saxophone", "violin"]
            vocal_labels = ["female vocals", "male vocals", "duet", "choir vocals"]
            era_labels = ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]

            def top_n(results, labels, n=3):
                filtered = [(r['label'], round(float(r['score']), 3)) for r in results if r['label'] in labels]
                filtered.sort(key=lambda x: x[1], reverse=True)
                return filtered[:n]

            clap_data = {
                "detected": True,
                "top_genres": top_n(results, genre_labels),
                "top_moods": top_n(results, mood_labels),
                "top_instruments": top_n(results, instrument_labels),
                "top_vocal_style": top_n(results, vocal_labels, n=2),
                "top_era": top_n(results, era_labels, n=2),
            }
        except Exception as e:
            clap_data = {"detected": False, "error": str(e)}
    else:
        clap_data = {"note": "transformers not installed — install with: pip install transformers torch"}

    return {
        "bpm": round(bpm, 1),
        "tempo_feel": tempo_feel,
        "tempo_consistency": round(tempo_consistency, 2),
        "estimated_key": key,
        "key_confidence": key_confidence,
        "duration_seconds": round(duration, 1),
        "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
        "beat_count": len(beat_frames),
        "onset_density": round(onset_density, 2),
        "brightness": brightness,
        "energy_description": energy_description,
        "energy_profile": energy_profile,
        "approximate_sections": sections,
        "clap_classification": clap_data,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: analyze_audio.py <audio_file.wav>", file=sys.stderr)
        sys.exit(1)

    result = analyze(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
