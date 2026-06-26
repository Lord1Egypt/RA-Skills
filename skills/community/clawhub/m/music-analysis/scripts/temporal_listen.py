#!/usr/bin/env python3
"""Temporal Listener v2 — groove, structure, harmonic motion, explainable mood timeline."""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import librosa
import numpy as np

from music_analysis_v2 import analyze_track, format_ts, safe_div, to_native

warnings.filterwarnings("ignore")


def mood_from_features(energy_rel: float, brightness: float, onset_density: float, harmonic_ratio: float, tension: float) -> str:
    if energy_rel < 0.42:
        if tension > 0.55:
            return "fragile / suspended"
        if brightness < 1400:
            return "submerged"
        return "ethereal"
    if energy_rel < 0.8:
        if onset_density > 2.8:
            return "restless"
        if harmonic_ratio > 0.72:
            return "floating"
        return "simmering"
    if energy_rel < 1.25:
        if tension > 0.55:
            return "driving / unresolved"
        if harmonic_ratio > 0.72:
            return "soaring"
        return "locked in"
    if onset_density > 4.5:
        return "erupting"
    if brightness > 2800:
        return "searing"
    if tension > 0.55:
        return "full force / unstable"
    return "full force"


def analyze_temporal(path, window_sec=4.0, hop_sec=2.0):
    y, sr = librosa.load(path, sr=22050, mono=True)
    duration = len(y) / sr
    track = analyze_track(Path(path))

    global_rms = float(np.sqrt(np.mean(y ** 2)))
    window_samples = int(window_sec * sr)
    hop_samples = int(hop_sec * sr)

    timeline = []
    position = 0
    prev_energy = None
    prev_centroid = None
    prev_tension = None
    prev_mood = None
    tension_accumulator = 0.0

    while position + window_samples <= len(y):
        chunk = y[position:position + window_samples]
        t_start = position / sr
        t_end = (position + window_samples) / sr
        t_mid = (t_start + t_end) / 2

        rms = float(np.sqrt(np.mean(chunk ** 2)))
        energy_relative = rms / (global_rms + 1e-9)
        centroid = float(np.mean(librosa.feature.spectral_centroid(y=chunk, sr=sr)))
        rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=chunk, sr=sr)))
        flatness = float(np.mean(librosa.feature.spectral_flatness(y=chunk)))
        bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=chunk, sr=sr)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(chunk)))

        h, p = librosa.effects.hpss(chunk)
        harmonic_ratio = float(np.sqrt(np.mean(h ** 2)) / (rms + 1e-9))
        percussive_ratio = float(np.sqrt(np.mean(p ** 2)) / (rms + 1e-9))
        onsets = librosa.onset.onset_detect(y=chunk, sr=sr, units="frames")
        onset_density = len(onsets) / window_sec

        chroma = librosa.feature.chroma_cqt(y=chunk, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        chroma_norm = chroma_mean / (np.sum(chroma_mean) + 1e-9)
        chroma_entropy = float(-np.sum(chroma_norm * np.log2(chroma_norm + 1e-12)) / np.log2(12))
        chroma_diff = float(np.mean(np.linalg.norm(np.diff(chroma, axis=1), axis=0))) if chroma.shape[1] > 1 else 0.0
        tonnetz = librosa.feature.tonnetz(chroma=chroma, sr=sr)
        tonal_motion = float(np.mean(np.linalg.norm(np.diff(tonnetz, axis=1), axis=0))) if tonnetz.shape[1] > 1 else 0.0
        tension = min(1.0, 0.9 * chroma_diff + 0.6 * tonal_motion + chroma_entropy * 0.25)

        energy_delta = safe_div((rms - prev_energy), (prev_energy + 1e-9)) if prev_energy is not None else 0.0
        brightness_delta = safe_div((centroid - prev_centroid), (prev_centroid + 1e-9)) if prev_centroid is not None else 0.0
        tension_delta = (tension - prev_tension) if prev_tension is not None else 0.0

        if energy_delta > 0.18 or tension_delta > 0.12:
            tension_accumulator = max(0.0, tension_accumulator + 0.18)
        elif energy_delta < -0.15:
            tension_accumulator = max(0.0, tension_accumulator - 0.10)
        else:
            tension_accumulator = max(0.0, tension_accumulator * 0.98)

        mood = mood_from_features(energy_relative, centroid, onset_density, harmonic_ratio, tension)

        transition = None
        if prev_mood and mood != prev_mood:
            if energy_delta > 0.2:
                transition = "drop hits"
            elif energy_delta < -0.18:
                transition = "pulls back"
            elif tension_delta > 0.1:
                transition = "tightens harmonically"
            elif abs(brightness_delta) > 0.14:
                transition = "shifts color"
            else:
                transition = "evolves"

        moment = {
            "time": round(t_mid, 1),
            "time_fmt": format_ts(t_mid),
            "energy": round(energy_relative, 2),
            "energy_delta": round(energy_delta, 2),
            "brightness": round(centroid, 0),
            "rolloff": round(rolloff, 0),
            "flatness": round(flatness, 4),
            "bandwidth": round(bandwidth, 0),
            "mood": mood,
            "texture": {
                "harmonic": round(harmonic_ratio, 2),
                "percussive": round(percussive_ratio, 2),
                "roughness": round(zcr, 4),
                "onset_density": round(onset_density, 1),
            },
            "tension": round(tension, 3),
            "tension_accumulator": round(tension_accumulator, 3),
            "harmonic_motion": round(tonal_motion, 4),
            "chroma_entropy": round(chroma_entropy, 3),
        }
        if transition:
            moment["transition"] = transition
        timeline.append(moment)

        prev_energy = rms
        prev_centroid = centroid
        prev_tension = tension
        prev_mood = mood
        position += hop_samples

    arc = build_narrative(timeline, duration, track)
    return {
        "track": Path(path).name,
        "duration": round(duration, 1),
        "duration_fmt": format_ts(duration),
        "tempo": track["groove"]["tempo_bpm"],
        "window_sec": window_sec,
        "hop_sec": hop_sec,
        "moments": len(timeline),
        "timeline": timeline,
        "narrative": arc,
        "track_context": {
            "structure_summary": track["structure"]["structure_summary"],
            "repeated_sections": track["structure"]["repeated_sections"],
            "key_estimate": track["harmony"]["key_estimate"],
            "tension_description": track["harmony"]["tension_description"],
            "pulse": track["groove"]["pocket"],
        },
    }


def build_narrative(timeline, duration, track):
    if not timeline:
        return {"arc_shape": "empty", "story": "No data."}

    peak_moment = max(timeline, key=lambda m: (m["energy"], m["tension"]))
    quietest = min(timeline, key=lambda m: m["energy"])
    tensest = max(timeline, key=lambda m: m["tension"])
    transitions = [m for m in timeline if "transition" in m]

    third = max(1, len(timeline) // 3)
    opening = timeline[:third]
    middle = timeline[third:2 * third] or timeline[:1]
    closing = timeline[2 * third:] or timeline[-1:]

    avg_energy = lambda ms: sum(m["energy"] for m in ms) / len(ms)
    avg_tension = lambda ms: sum(m["tension"] for m in ms) / len(ms)
    common_mood = lambda ms: max(set(m["mood"] for m in ms), key=lambda mood: sum(1 for m in ms if m["mood"] == mood))

    e_open, e_mid, e_close = avg_energy(opening), avg_energy(middle), avg_energy(closing)
    if e_mid > e_open and e_mid > e_close:
        arc_shape = "mountain"
    elif e_close > e_open + 0.12:
        arc_shape = "ascending"
    elif e_open > e_close + 0.12:
        arc_shape = "descending"
    elif max(e_open, e_mid, e_close) - min(e_open, e_mid, e_close) < 0.15:
        arc_shape = "plateau"
    else:
        arc_shape = "wave"

    return {
        "arc_shape": arc_shape,
        "opening": {"mood": common_mood(opening), "energy": round(e_open, 2), "tension": round(avg_tension(opening), 2)},
        "middle": {"mood": common_mood(middle), "energy": round(e_mid, 2), "tension": round(avg_tension(middle), 2)},
        "closing": {"mood": common_mood(closing), "energy": round(e_close, 2), "tension": round(avg_tension(closing), 2)},
        "peak": {"time": peak_moment["time_fmt"], "mood": peak_moment["mood"], "energy": round(peak_moment["energy"], 2)},
        "quietest": {"time": quietest["time_fmt"], "mood": quietest["mood"], "energy": round(quietest["energy"], 2)},
        "tensest": {"time": tensest["time_fmt"], "mood": tensest["mood"], "tension": round(tensest["tension"], 2)},
        "transitions": len(transitions),
        "mood_journey": " → ".join(dict.fromkeys(m["mood"] for m in timeline)),
        "structure_summary": track["structure"]["structure_summary"],
        "pulse": track["groove"]["pocket"],
        "emotion_overview": track["emotion"]["overview"],
    }


def print_listening_experience(result):
    n = result["narrative"]
    tl = result["timeline"]

    print(f"\n🎧 TEMPORAL LISTEN: {result['track']}")
    print(f"   {result['duration_fmt']} | ~{result['tempo']} BPM | {result['moments']} moments captured")
    print(f"\n📐 Arc shape: {n['arc_shape']}")
    print(f"   Opening → {n['opening']['mood']} (energy {n['opening']['energy']}, tension {n['opening']['tension']})")
    print(f"   Middle  → {n['middle']['mood']} (energy {n['middle']['energy']}, tension {n['middle']['tension']})")
    print(f"   Closing → {n['closing']['mood']} (energy {n['closing']['energy']}, tension {n['closing']['tension']})")
    print(f"\n🔥 Peak moment:   {n['peak']['time']} — {n['peak']['mood']} (energy {n['peak']['energy']})")
    print(f"🌊 Quietest:      {n['quietest']['time']} — {n['quietest']['mood']} (energy {n['quietest']['energy']})")
    print(f"🪢 Tensest:       {n['tensest']['time']} — {n['tensest']['mood']} (tension {n['tensest']['tension']})")
    print(f"\n🎭 Mood journey: {n['mood_journey']}")
    print(f"🏗️ Structure: {n['structure_summary']} | Pulse: {n['pulse']}")
    print(f"   {n['transitions']} transitions detected")

    print("\n⏱️ TIMELINE (highlights):")
    for m in tl:
        marker = ""
        if "transition" in m:
            marker += f" ⚡ {m['transition']}"
        if m["tension"] >= n["tensest"]["tension"] * 0.95:
            marker += " 🪢"
        if m["energy"] >= n["peak"]["energy"] * 0.95:
            marker += " 🔥"
        if marker:
            bar_len = min(20, int(m["energy"] * 12))
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"   {m['time_fmt']} [{bar}] {m['mood']}{marker}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: temporal_listen.py <audio_file> [--json]")
        sys.exit(1)

    path = sys.argv[1]
    use_json = "--json" in sys.argv
    result = analyze_temporal(path)
    if use_json:
        print(json.dumps(to_native(result), indent=2))
    else:
        print_listening_experience(result)
