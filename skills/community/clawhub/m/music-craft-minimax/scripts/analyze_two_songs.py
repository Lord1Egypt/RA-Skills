#!/usr/bin/env python3
"""analyze_two_songs.py — Extract musical features from one or two songs for mashup.

Supports ANY combination of inputs:
- Two audio files (Song A + Song B)
- Single audio file (analyzed as Song A, LLM provides style for Song B later)
- Song name as text (LLM fills in features)

Usage:
    # Two songs:
    python3 analyze_two_songs.py --song-a /tmp/song_a.wav --song-b /tmp/song_b.wav

    # Single song (Song A only):
    python3 analyze_two_songs.py --song-a /tmp/song_a.wav

    # With song names for LLM context:
    python3 analyze_two_songs.py --song-a /tmp/song_a.wav --name-a "EagleWow" --name-b "La Vie en Rose"

Output: JSON with features from analyzed songs, plus mashup recommendations.

Requires: librosa, numpy
"""
import sys
import os
import json
import argparse
import librosa
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _key_compat import mashup_compatibility

# Shared audio feature utilities (key detection, tempo/energy classification,
# section estimation). See _audio_features.py for the canonical implementations.
from _audio_features import (
    detect_key,
    estimate_sections,
    classify_tempo,
    classify_energy,
)

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

# Default hop length for librosa energy/feature analysis. Used to convert frame
# indices back to time. Must match the hop_length used by librosa.feature.* in this file.
HOP_LENGTH = 512



def classify_brightness(centroid):
    """Classify tonal brightness."""
    if centroid > 4000: return "bright treble-heavy"
    elif centroid > 2500: return "balanced warm"
    elif centroid > 1500: return "warm mellow"
    else: return "dark bass-heavy"


def detect_instrumentation_hints(y, sr):
    """Estimate instrumentation characteristics from spectral analysis."""
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y)[0]
    spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]

    avg_centroid = float(np.mean(spectral_centroid))
    avg_rolloff = float(np.mean(spectral_rolloff))
    avg_zcr = float(np.mean(zcr))
    avg_flatness = float(np.mean(spectral_flatness))

    hints = {
        'centroid': round(avg_centroid, 1),
        'rolloff': round(avg_rolloff, 1),
        'zcr': round(avg_zcr, 4),
        'flatness': round(avg_flatness, 5),
        'likely_acoustic': avg_centroid < 2500 and avg_zcr > 0.08,
        'likely_electronic': avg_centroid > 4000 and avg_flatness > 0.01,
        'likely_orchestral': avg_rolloff > 6000 and avg_flatness < 0.005,
        'likely_distorted': avg_flatness < 0.001 and avg_rolloff > 5000,
    }
    return hints


def classify_with_clap(audio_path, top_n=3):
    """Run CLAP zero-shot classification on audio.

    Returns dict with top_genres, top_moods, top_instruments, top_vocal_style, top_era.
    """
    if not HAS_TRANSFORMERS:
        return {"detected": False, "note": "transformers not installed - install with: pip install transformers torch"}
    try:
        classifier = pipeline("zero-shot-audio-classification", model="laion/clap-htsat-unfused")
        candidate_labels = [
            "pop", "rock", "jazz", "blues", "classical", "electronic", "hip hop", "rnb",
            "country", "folk", "metal", "punk", "reggae", "latin", "soul", "funk",
            "disco", "house", "techno", "ambient", "indie", "alternative",
            "dream pop", "synthwave", "post-rock", "shoegaze", "lo-fi",
            "happy", "sad", "melancholic", "euphoric", "aggressive", "tender",
            "dark", "bright", "nostalgic", "epic", "peaceful", "tense",
            "piano", "guitar", "drums", "bass", "synthesizer", "strings",
            "brass", "vocals", "choir", "organ", "saxophone", "violin",
            "female vocals", "male vocals", "duet", "choir vocals",
            "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s",
        ]
        results = classifier(audio_path, candidate_labels=candidate_labels)
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

        def top_n_in(results, labels, n=top_n):
            filtered = [(r['label'], round(float(r['score']), 3)) for r in results if r['label'] in labels]
            filtered.sort(key=lambda x: x[1], reverse=True)
            return filtered[:n]

        return {
            'detected': True,
            'top_genres': top_n_in(results, genre_labels),
            'top_moods': top_n_in(results, mood_labels),
            'top_instruments': top_n_in(results, instrument_labels),
            'top_vocal_style': top_n_in(results, vocal_labels, n=2),
            'top_era': top_n_in(results, era_labels, n=2),
        }
    except Exception as e:
        return {'detected': False, 'error': str(e)}


def analyze_song(audio_path, song_label="song"):
    """Analyze a single song and return features."""
    print(f"Analyzing {song_label}: {audio_path}", file=sys.stderr)

    y, sr = librosa.load(audio_path, sr=22050)
    duration = len(y) / sr

    # Tempo / BPM
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Key detection
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)
    key, key_confidence = detect_key(chroma_avg)

    # Energy profile
    rms = librosa.feature.rms(y=y)[0]
    rms_resampled = np.interp(
        np.linspace(0, len(rms) - 1, 20),
        np.arange(len(rms)),
        rms
    )

    # Spectral analysis
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    avg_brightness = float(np.mean(spectral_centroid))

    # Instrument hints
    instr_hints = detect_instrumentation_hints(y, sr)

    # Onset density
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_density = len(onset_frames) / duration

    # Sections
    sections = estimate_sections(rms, sr, duration, hop_length=HOP_LENGTH)

    # CLAP classification (if available)
    clap_data = classify_with_clap(audio_path)

    return {
        "label": song_label,
        "source_file": audio_path,
        "bpm": round(bpm, 1),
        "tempo_feel": classify_tempo(bpm),
        "estimated_key": key,
        "key_confidence": key_confidence,
        "duration_seconds": round(duration, 1),
        "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
        "brightness": classify_brightness(avg_brightness),
        "energy_description": classify_energy(float(np.mean(rms))),
        "energy_profile": [round(float(e), 5) for e in rms_resampled],
        "onset_density": round(onset_density, 2),
        "instrument_hints": instr_hints,
        "approximate_sections": sections,
        "clap_classification": clap_data,
    }


def generate_mashup_recommendations(song_a, song_b):
    """Generate BPM and style transformation recommendations."""
    a_bpm = song_a.get('bpm', 100)
    b_bpm = song_b.get('bpm', 100) if song_b else 100

    # Default: match reference song BPM
    target_bpm = b_bpm

    # Smart adjustments
    if song_b:
        a_energy = song_a.get('energy_description', '')
        b_energy = song_b.get('energy_description', '')

        # Pop → slow style (e.g., French Chanson)
        if a_bpm > 120 and b_bpm < 90:
            target_bpm = max(b_bpm - 5, 70)
        # Slow → fast style
        elif a_bpm < 80 and b_bpm > 140:
            target_bpm = min(b_bpm, a_bpm * 1.8)
        # Similar range — blend
        elif abs(a_bpm - b_bpm) < 30:
            target_bpm = round((a_bpm + b_bpm) / 2, 1)

    style_notes = ""
    if song_b:
        style_notes = f"Use {song_b.get('label', 'reference')} style characteristics"

    return {
        "target_bpm": round(target_bpm, 1),
        "bpm_transformation": f"{a_bpm} → {target_bpm} BPM",
        "style_notes": style_notes,
        "instrument_prompt_additions": get_style_prompt_additions(song_b or {}),
    }


def get_style_prompt_additions(song_features):
    """Get music prompt text based on song features."""
    brightness = song_features.get('brightness', 'balanced')
    energy = song_features.get('energy_description', 'moderate')
    instr_hints = song_features.get('instrument_hints', {})

    additions = []

    if 'bright' in str(brightness):
        additions.append("bright treble-forward sound")
    elif 'warm' in str(brightness) or 'mellow' in str(brightness):
        additions.append("warm analog sound")
    elif 'dark' in str(brightness):
        additions.append("dark moody atmosphere")

    if 'high' in str(energy) or 'very high' in str(energy):
        additions.append("energetic driving rhythm")
    elif 'low' in str(energy) or 'very low' in str(energy):
        additions.append("intimate sparse arrangement")

    if instr_hints.get('likely_orchestral'):
        additions.append("orchestral strings prominent")
    if instr_hints.get('likely_electronic'):
        additions.append("synthesizer and electronic textures")
    if instr_hints.get('likely_acoustic'):
        additions.append("acoustic instruments focus")
    if instr_hints.get('likely_distorted'):
        additions.append("overdriven guitar, rock energy")

    return ", ".join(additions) if additions else "balanced arrangement"


def main():
    parser = argparse.ArgumentParser(
        description='Analyze one or two songs for mashup preparation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Two songs:
  %(prog)s --song-a song_a.wav --song-b song_b.wav

  # Single song (Song A only):
  %(prog)s --song-a song_a.wav

  # With names:
  %(prog)s --song-a song_a.wav --name-a "EagleWow" --name-b "La Vie en Rose"
        """
    )
    parser.add_argument('--song-a', help='Song A audio file (content/emotion source)')
    parser.add_argument('--song-b', help='Song B audio file (style reference)')
    parser.add_argument('--name-a', help='Song A name (for context)')
    parser.add_argument('--name-b', help='Song B name (for context)')
    parser.add_argument('--output', '-o', help='Output JSON file path')

    # Legacy positional args support
    parser.add_argument('positional', nargs='*', help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Handle legacy positional args: analyze_two_songs.py <a> <b>
    if not args.song_a and len(args.positional) >= 1:
        args.song_a = args.positional[0]
    if not args.song_b and len(args.positional) >= 2:
        args.song_b = args.positional[1]

    if not args.song_a:
        print("Error: --song-a is required", file=sys.stderr)
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    # Analyze Song A (always required)
    song_a = analyze_song(args.song_a, args.name_a or "Song A (content)")

    # Analyze Song B (optional)
    song_b = None
    if args.song_b:
        song_b = analyze_song(args.song_b, args.name_b or "Song B (style reference)")
    elif args.name_b:
        # Song B is named but has no audio — LLM will need to fill in
        print(f"Song B '{args.name_b}' has no audio file — LLM should provide style context", file=sys.stderr)
        song_b = {
            "label": args.name_b,
            "source": "llm_knowledge",
            "note": "Style characteristics should be provided by LLM based on song name"
        }

    # Generate mashup plan
    mashup_plan = generate_mashup_recommendations(song_a, song_b or {})

    if song_b and 'bpm' in song_b and 'estimated_key' in song_b:
        compat = mashup_compatibility(song_a, song_b)
        mashup_plan['compatibility'] = compat
        if compat.get('suggested_target_bpm'):
            mashup_plan['target_bpm'] = compat['suggested_target_bpm']

    result = {
        "song_a_original": song_a,
        "song_b_reference": song_b,
        "mashup_plan": mashup_plan,
    }

    json_out = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == "__main__":
    main()
