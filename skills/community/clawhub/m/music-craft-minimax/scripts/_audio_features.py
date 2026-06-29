#!/usr/bin/env python3
"""_audio_features.py — Shared audio feature extraction utilities.

Used by both analyze_audio.py (single-song analysis) and
analyze_two_songs.py (mashup analysis) to avoid duplicating
Krumhansl-Schmuckler key detection, tempo/energy classification,
and section estimation logic.

This module is internal (prefixed with _) — scripts import from it
but it is not meant to be run directly.
"""
import numpy as np

# Krumhansl-Schmuckler key profiles (12 chroma bins, C major / C minor)
KEY_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


def detect_key(chroma_avg):
    """Detect key using Krumhansl-Schmuckler algorithm.

    Args:
        chroma_avg: 12-element array of average chroma energy per pitch class.

    Returns:
        Tuple of (key_string, confidence).
        key_string is e.g. "C major" or "A minor".
        confidence is the correlation coefficient rounded to 3 decimals.
    """
    best_corr = -2
    best_key = "C major"
    for i in range(12):
        rotated = np.roll(chroma_avg, -i)
        corr_maj = np.corrcoef(rotated, MAJOR_PROFILE)[0, 1]
        corr_min = np.corrcoef(rotated, MINOR_PROFILE)[0, 1]
        if corr_maj > best_corr:
            best_corr = corr_maj
            best_key = f"{KEY_NAMES[i]} major"
        if corr_min > best_corr:
            best_corr = corr_min
            best_key = f"{KEY_NAMES[i]} minor"
    return best_key, round(float(best_corr), 3)


def classify_tempo(bpm):
    """Classify BPM into a tempo feel label.

    Args:
        bpm: Beats per minute (float or int).

    Returns:
        One of: "very slow ballad", "slow ballad", "moderate",
        "upbeat", "fast energetic", "very fast intense".
    """
    if bpm < 70:
        return "very slow ballad"
    elif bpm < 90:
        return "slow ballad"
    elif bpm < 110:
        return "moderate"
    elif bpm < 130:
        return "upbeat"
    elif bpm < 150:
        return "fast energetic"
    else:
        return "very fast intense"


def classify_energy(rms_or_profile):
    """Classify overall RMS energy level.

    Accepts either a scalar mean RMS or a 1-D RMS profile (we average
    internally). This keeps callers from having to know which form to pass.

    Args:
        rms_or_profile: Scalar mean RMS or 1-D array of RMS values per frame
                        (typically 0.0-0.2 for normalized audio).

    Returns:
        One of: "very low, intimate", "low, gentle", "moderate",
        "high, energetic", "very high, intense".
    """
    rms_avg = float(np.mean(rms_or_profile))
    if rms_avg < 0.02:
        return "very low, intimate"
    elif rms_avg < 0.05:
        return "low, gentle"
    elif rms_avg < 0.1:
        return "moderate"
    elif rms_avg < 0.15:
        return "high, energetic"
    else:
        return "very high, intense"


def estimate_sections(rms, sr, duration, hop_length=512, max_sections=10):
    """Estimate song sections from the energy envelope.

    Args:
        rms: 1-D array of RMS energy per frame.
        sr: Sample rate.
        duration: Total audio duration in seconds (used for logging only;
                  not strictly needed since we derive from rms and hop_length).
        hop_length: Samples per frame (default 512 — the librosa default).
        max_sections: Maximum number of sections to label.

    Returns:
        List of section dicts. Each dict has:
            - section: human label (intro, verse, pre-chorus, chorus,
              bridge, outro — see labels below)
            - start_seconds: section start time
            - end_seconds: section end time
            - avg_energy: mean RMS in this section
            - peak_energy: max RMS in this section
    """
    n = len(rms)
    if n < 4:
        return []

    # Smooth RMS with a moving average
    window = max(1, n // 50)
    smooth_rms = np.convolve(rms, np.ones(window) / window, mode='same')

    # Find significant energy transitions
    diff = np.diff(smooth_rms)
    threshold = np.std(diff) * 1.5

    boundaries = [0]
    for i in range(len(diff)):
        if abs(diff[i]) > threshold:
            if not boundaries or (i - boundaries[-1]) > n // 8:
                boundaries.append(i)
    boundaries.append(n - 1)

    # Generic section labels — caller can re-label via section classifier
    labels = ["intro", "verse", "pre-chorus", "chorus",
              "verse", "pre-chorus", "chorus", "bridge",
              "chorus", "outro"]

    sections = []
    for idx in range(len(boundaries) - 1):
        start = boundaries[idx]
        end = boundaries[idx + 1]
        segment = rms[start:end]
        if len(segment) == 0:
            continue

        label = labels[min(idx, len(labels) - 1)]
        start_time = round(float(start * hop_length / sr), 1)
        end_time = round(float(end * hop_length / sr), 1)

        sections.append({
            "section": label,
            "start_seconds": start_time,
            "end_seconds": end_time,
            "avg_energy": round(float(np.mean(segment)), 5),
            "peak_energy": round(float(np.max(segment)), 5),
        })

    return sections
