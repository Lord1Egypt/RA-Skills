#!/usr/bin/env python3
"""Instrument detection from mixed stereo audio using spectral analysis.

Returns likely instrument palette and per-section arrangement roles,
designed to be woven into emotional narrative rather than presented as clinical data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import librosa


# ---------------------------------------------------------------------------
# Instrument family profiles: rough spectral fingerprints
# Each profile has: centroid_range, flatness_range, harmonicity, attack, bandwidth
# ---------------------------------------------------------------------------

INSTRUMENT_PROFILES = {
    "bowed strings": {
        "centroid": (300, 2200),
        "flatness_max": 0.08,
        "harmonicity_min": 0.55,
        "attack": "slow",
        "tags": ["ache", "human voice quality", "warmth"],
    },
    "piano": {
        "centroid": (600, 3500),
        "flatness_max": 0.10,
        "harmonicity_min": 0.45,
        "attack": "sharp",
        "tags": ["architecture", "clarity", "shape"],
    },
    "acoustic guitar": {
        "centroid": (800, 3000),
        "flatness_max": 0.12,
        "harmonicity_min": 0.40,
        "attack": "sharp",
        "tags": ["intimacy", "texture", "earthiness"],
    },
    "upright bass": {
        "centroid": (80, 700),
        "flatness_max": 0.10,
        "harmonicity_min": 0.40,
        "attack": "moderate",
        "tags": ["gravity", "warmth", "foundation"],
    },
    "electric bass": {
        "centroid": (120, 900),
        "flatness_max": 0.18,
        "harmonicity_min": 0.30,
        "attack": "sharp",
        "tags": ["groove", "weight", "anchor"],
    },
    "drums / percussion": {
        "centroid": (1000, 8000),
        "flatness_max": 1.0,  # drums can be very noisy
        "harmonicity_min": 0.0,
        "attack": "sharp",
        "tags": ["pulse", "momentum", "energy"],
    },
    "brass": {
        "centroid": (500, 3500),
        "flatness_max": 0.06,
        "harmonicity_min": 0.55,
        "attack": "moderate",
        "tags": ["power", "declaration", "warmth"],
    },
    "woodwinds / reeds": {
        "centroid": (600, 3000),
        "flatness_max": 0.07,
        "harmonicity_min": 0.50,
        "attack": "moderate",
        "tags": ["breath", "color", "longing"],
    },
    "low saxophone": {
        "centroid": (200, 1200),
        "flatness_max": 0.08,
        "harmonicity_min": 0.50,
        "attack": "moderate",
        "tags": ["breath", "warmth", "weight"],
    },
    "synth pad": {
        "centroid": (200, 2500),
        "flatness_max": 0.25,
        "harmonicity_min": 0.30,
        "attack": "slow",
        "tags": ["atmosphere", "space", "drift"],
    },
    "voice": {
        "centroid": (300, 3500),
        "flatness_max": 0.08,
        "harmonicity_min": 0.60,
        "attack": "moderate",
        "tags": ["intimacy", "directness", "human presence"],
    },
}


def _attack_time(y_segment: np.ndarray, sr: int) -> str:
    """Estimate attack character from onset envelope shape."""
    onset_env = librosa.onset.onset_strength(y=y_segment, sr=sr)
    if onset_env.size < 4:
        return "moderate"
    # Look at how quickly onset strength rises
    onset_diff = np.diff(onset_env)
    max_rise = float(np.percentile(onset_diff[onset_diff > 0], 90)) if np.any(onset_diff > 0) else 0.0
    mean_rise = float(np.mean(onset_diff[onset_diff > 0])) if np.any(onset_diff > 0) else 0.0
    # Sharp attack = high max rise relative to mean
    if max_rise > 0 and mean_rise > 0:
        attack_ratio = max_rise / (mean_rise + 1e-9)
        if attack_ratio > 3.0:
            return "sharp"
        elif attack_ratio < 1.5:
            return "slow"
    return "moderate"


def _harmonicity(y_segment: np.ndarray, sr: int) -> float:
    """Estimate harmonicity via harmonic/percussive decomposition energy ratio."""
    harmonic, percussive = librosa.effects.hpss(y_segment)
    h_energy = float(np.sum(harmonic ** 2))
    p_energy = float(np.sum(percussive ** 2))
    total = h_energy + p_energy
    if total < 1e-12:
        return 0.5
    return h_energy / total


def _spectral_features(y_segment: np.ndarray, sr: int) -> dict[str, float]:
    """Extract key spectral features for instrument matching."""
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y_segment, sr=sr)[0]))
    flatness = float(np.mean(librosa.feature.spectral_flatness(y=y_segment)[0]))
    bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y_segment, sr=sr)[0]))

    # Low-end energy ratio
    stft = np.abs(librosa.stft(y_segment))
    power = stft ** 2
    freqs = librosa.fft_frequencies(sr=sr)
    low_mask = freqs < 250
    total_power = float(np.sum(power) + 1e-9)
    low_ratio = float(np.sum(power[low_mask, :]) / total_power) if np.any(low_mask) else 0.0

    return {
        "centroid": centroid,
        "flatness": flatness,
        "bandwidth": bandwidth,
        "low_ratio": low_ratio,
    }


def _match_instruments(features: dict[str, float], harmonicity: float, attack: str) -> list[dict[str, Any]]:
    """Score each instrument profile against observed features."""
    candidates = []
    centroid = features["centroid"]
    flatness = features["flatness"]
    low_ratio = features["low_ratio"]

    for name, profile in INSTRUMENT_PROFILES.items():
        score = 0.0
        reasons = []

        # Centroid range check
        c_low, c_high = profile["centroid"]
        if c_low <= centroid <= c_high:
            # How centered in the range
            mid = (c_low + c_high) / 2
            range_width = c_high - c_low
            closeness = 1.0 - abs(centroid - mid) / (range_width / 2 + 1e-9)
            score += 0.25 * closeness
            reasons.append("centroid fits")
        else:
            score -= 0.3
            continue  # Hard filter: if centroid doesn't fit, skip

        # Flatness check
        if flatness <= profile["flatness_max"]:
            score += 0.2
            reasons.append("tonal quality matches")
        else:
            if name != "drums / percussion":
                score -= 0.2

        # Harmonicity check
        if harmonicity >= profile["harmonicity_min"]:
            score += 0.25
            reasons.append("harmonicity level fits")
        else:
            if profile["harmonicity_min"] > 0.4:
                score -= 0.15

        # Attack character
        if attack == profile["attack"]:
            score += 0.15
            reasons.append("attack character matches")
        elif (attack == "sharp" and profile["attack"] == "slow") or (attack == "slow" and profile["attack"] == "sharp"):
            score -= 0.15

        # Special: bass instruments need strong low-end
        if "bass" in name.lower():
            if low_ratio > 0.15:
                score += 0.15
                reasons.append("strong low-end presence")
            else:
                score -= 0.3

        # Special: drums need low harmonicity
        if "drums" in name:
            if harmonicity < 0.45:
                score += 0.2
                reasons.append("percussive energy dominant")
            else:
                score -= 0.2

        # Special: bowed strings - slow attack + high harmonicity is the killer combo
        if "bowed" in name and attack == "slow" and harmonicity > 0.55:
            score += 0.15
            reasons.append("sustained bowed character")

        # Special: upright bass vs electric bass tiebreaker
        # Very high harmonicity + very low flatness = deeply tonal, acoustic character
        # Upright bass can be plucked (sharp attack) or bowed — attack alone doesn't decide
        if name == "upright bass" and harmonicity > 0.65 and flatness < 0.02:
            score += 0.25
            reasons.append("deeply tonal and resonant — acoustic character")
        elif name == "upright bass" and attack != "sharp" and harmonicity > 0.45 and flatness < 0.06:
            score += 0.2
            reasons.append("warm woody resonance favors acoustic")

        if name == "electric bass" and harmonicity > 0.70 and flatness < 0.02:
            score -= 0.25  # Too warm and resonant for electric — this is acoustic
        elif name == "electric bass" and attack != "sharp" and harmonicity > 0.50 and flatness < 0.06:
            score -= 0.15

        if score > 0.1:
            candidates.append({
                "instrument": name,
                "score": round(score, 3),
                "emotional_tags": profile["tags"],
                "reasons": reasons,
            })

    # Sort by score
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # Mutual exclusivity — don't return both electric bass AND upright bass
    # Keep the higher-scoring one
    EXCLUSIVE_GROUPS = [
        {"electric bass", "upright bass"},
        {"acoustic guitar", "electric bass"},  # rarely both dominant
    ]
    seen_instruments = set()
    filtered = []
    for c in candidates:
        blocked = False
        for group in EXCLUSIVE_GROUPS:
            if c["instrument"] in group and (group & seen_instruments):
                blocked = True
                break
        if not blocked:
            filtered.append(c)
            seen_instruments.add(c["instrument"])
    return filtered


def _confidence_label(score: float) -> str:
    """Human-readable confidence without sounding clinical."""
    if score >= 0.6:
        return "strong"
    elif score >= 0.35:
        return "likely"
    else:
        return "possible"


def detect_instruments_full(y: np.ndarray, sr: int) -> dict[str, Any]:
    """Detect likely instruments across the full track."""
    features = _spectral_features(y, sr)
    harmonicity = _harmonicity(y, sr)
    attack = _attack_time(y, sr)
    candidates = _match_instruments(features, harmonicity, attack)

    palette = []
    for c in candidates[:5]:  # Top 5 max
        palette.append({
            "instrument": c["instrument"],
            "confidence": _confidence_label(c["score"]),
            "emotional_color": c["emotional_tags"],
        })

    return {
        "palette": palette,
        "features": {
            "centroid": round(features["centroid"], 1),
            "flatness": round(features["flatness"], 4),
            "harmonicity": round(harmonicity, 3),
            "attack_character": attack,
            "low_end_ratio": round(features["low_ratio"], 3),
        },
    }


def detect_instruments_windowed(y: np.ndarray, sr: int, sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect instruments per structural section, noting what enters/exits."""
    total_samples = len(y)
    section_results = []
    prev_instruments = set()

    for section in sections:
        start_sample = int(section["start"] * sr)
        end_sample = min(int(section["end"] * sr), total_samples)
        if end_sample - start_sample < sr:  # Skip sections < 1 second
            continue

        y_section = y[start_sample:end_sample]
        features = _spectral_features(y_section, sr)
        harmonicity = _harmonicity(y_section, sr)
        attack = _attack_time(y_section, sr)
        candidates = _match_instruments(features, harmonicity, attack)

        current_instruments = set()
        section_palette = []
        for c in candidates[:4]:
            current_instruments.add(c["instrument"])
            section_palette.append({
                "instrument": c["instrument"],
                "confidence": _confidence_label(c["score"]),
                "emotional_color": c["emotional_tags"],
                "role": _guess_role(c["instrument"], features),
            })

        enters = current_instruments - prev_instruments
        exits = prev_instruments - current_instruments

        section_results.append({
            "label": section.get("label", "?"),
            "start": section["start"],
            "end": section["end"],
            "start_fmt": section.get("start_fmt", ""),
            "end_fmt": section.get("end_fmt", ""),
            "instruments": section_palette,
            "enters": list(enters) if enters else [],
            "exits": list(exits) if exits else [],
        })
        prev_instruments = current_instruments

    return section_results


def _guess_role(instrument: str, features: dict[str, float]) -> str:
    """Guess the arrangement role an instrument is playing."""
    if "bass" in instrument.lower():
        return "foundation"
    if "drums" in instrument.lower() or "percussion" in instrument.lower():
        return "pulse"
    if "pad" in instrument.lower() or "synth" in instrument.lower():
        return "texture"
    if features["centroid"] > 1500:
        return "lead / color"
    if "piano" in instrument.lower():
        return "harmony"
    if "strings" in instrument.lower():
        return "melody / voice"
    return "color"


def render_palette_narrative(full_detection: dict[str, Any], section_detection: list[dict[str, Any]]) -> str:
    """Render instrument detection as natural language, not a data table.

    The goal: sound like a person describing what they hear, not a lab report.
    """
    lines = []

    palette = full_detection.get("palette", [])
    if not palette:
        return "Couldn't get a clear read on individual instruments — the mix is too blended to pull apart with confidence."

    # Group by confidence
    strong = [p for p in palette if p["confidence"] == "strong"]
    likely = [p for p in palette if p["confidence"] == "likely"]
    possible = [p for p in palette if p["confidence"] == "possible"]

    # Core palette — describe what drives the sound
    if strong:
        names = [p["instrument"] for p in strong]
        if len(names) == 1:
            colors = strong[0].get("emotional_color", [])
            color_note = f" — giving the track its sense of {_join_natural(colors[:2])}" if colors else ""
            lines.append(f"The backbone is {names[0]}{color_note}.")
        else:
            lines.append(f"Built on {_join_natural(names)}.")
    if likely:
        names = [p["instrument"] for p in likely]
        color_bits = []
        for p in likely:
            c = p.get("emotional_color", [])
            if c:
                color_bits.append(f"{p['instrument']} adding {c[0]}")
        if color_bits:
            lines.append(f"Additional layers include {_join_natural([p['instrument'] for p in likely])} — {_join_natural(color_bits)}.")
        else:
            lines.append(f"Additional layers include {_join_natural(names)}.")
    if possible:
        names = [p["instrument"] for p in possible]
        lines.append(f"Possible traces of {_join_natural(names)} are present too, though the blend makes them harder to call with certainty.")

    # Section changes — only the meaningful ones
    meaningful_changes = [sec for sec in section_detection if sec["enters"] or sec["exits"]]
    # Skip the first section "enters" if it's just everything appearing at 0:00
    if meaningful_changes and meaningful_changes[0].get("start", 0) < 1.0:
        meaningful_changes = meaningful_changes[1:]

    for sec in meaningful_changes:
        time_str = sec.get("start_fmt", "")
        if sec["enters"] and sec["exits"]:
            lines.append(f"Around {time_str}, {_join_natural(sec['enters'])} {'comes' if len(sec['enters']) == 1 else 'come'} in as {_join_natural(sec['exits'])} drops away — you can feel the color shift.")
        elif sec["enters"]:
            entering = _join_natural(sec['enters'])
            # Try to describe the emotional effect
            enter_colors = []
            for inst in sec["enters"]:
                for p in palette:
                    if p["instrument"] == inst:
                        enter_colors.extend(p.get("emotional_color", []))
            if enter_colors:
                lines.append(f"Around {time_str}, {entering} {'enters' if len(sec['enters']) == 1 else 'enter'} and it brings {enter_colors[0]} with it.")
            else:
                lines.append(f"Around {time_str}, {entering} {'enters' if len(sec['enters']) == 1 else 'enter'} the picture.")
        elif sec["exits"]:
            lines.append(f"Around {time_str}, {_join_natural(sec['exits'])} {'falls' if len(sec['exits']) == 1 else 'fall'} away.")

    return " ".join(lines)


def _join_natural(items: list[str]) -> str:
    """Join items as natural English: 'a, b, and c'."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_instruments(audio_path: Path, sections: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Full instrument analysis: palette + per-section + narrative.

    Args:
        audio_path: Path to audio file
        sections: Structure sections from analyze_structure (optional)

    Returns:
        Dict with palette, section_detail, narrative, and raw features
    """
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    full = detect_instruments_full(y, sr)
    section_detail = []
    if sections:
        section_detail = detect_instruments_windowed(y, sr, sections)
    narrative = render_palette_narrative(full, section_detail)

    return {
        "palette": full["palette"],
        "features": full["features"],
        "section_detail": section_detail,
        "narrative": narrative,
    }
