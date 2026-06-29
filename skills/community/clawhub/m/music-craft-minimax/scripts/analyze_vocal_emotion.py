#!/usr/bin/env python3
"""analyze_vocal_emotion.py — Extract vocal emotion dynamics from audio.

Analyzes vocal recordings to detect:
- Emotional intensity curve (calm → intense → calm)
- Pitch patterns (rising, falling, stable) with parselmouth accuracy
- Vocal strain and breathiness
- Dynamic section boundaries (verse → chorus → bridge)
- Repetitive intensification (phrases getting louder/higher)
- Emotional transitions (sudden vs gradual)

Usage:
    python3 analyze_vocal_emotion.py <audio.wav> [--sections 20] [--output out.json]

Output: JSON with emotion profile per section, intensity curve,
pitch analysis, and recommendations for music generation.

Requires: librosa, numpy, scipy, praat-parselmouth (optional, better pitch)
"""
import sys
import json
import argparse
import warnings

import librosa
import numpy as np
from scipy import signal as scipy_signal
from scipy.ndimage import uniform_filter1d

# Optional: parselmouth gives more accurate pitch tracking via Praat
try:
    import parselmouth
    from parselmouth.praat import call as praat_call
    HAS_PARSELMOUTH = True
except ImportError:
    HAS_PARSELMOUTH = False

# Optional: pyloudnorm for LUFS/LRA dynamic profiling
try:
    import pyloudnorm as pyln
    HAS_PYLOUDNORM = True
except ImportError:
    HAS_PYLOUDNORM = False

# Optional: autochord for chord progression extraction
try:
    import autochord
    HAS_AUTOCHORD = True
except ImportError:
    HAS_AUTOCHORD = False

# Optional: allin1 for song structure detection
try:
    import allin1
    HAS_ALLIN1 = True
except ImportError:
    HAS_ALLIN1 = False

# Shared cache module (optional)
try:
    import os as _os
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from _analysis_cache import cached_or_compute
except ImportError:
    cached_or_compute = None

KEY_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# ─── Pitch extraction ───────────────────────────────────────────

def extract_pitch_contour(y, sr):
    """Extract F0 pitch contour. Uses parselmouth (Praat) if available, else librosa pyin."""
    if HAS_PARSELMOUTH:
        return _pitch_parselmouth(y, sr)
    return _pitch_librosa(y, sr)


def _pitch_parselmouth(y, sr):
    """Extract pitch using Praat via parselmouth — more accurate for vocals."""
    # parselmouth needs a Sound object
    snd = parselmouth.Sound(y, sampling_frequency=sr)
    pitch_obj = snd.to_pitch(
        time_step=0.01,          # 10ms resolution
        pitch_floor=60.0,        # Hz — covers low male voices
        pitch_ceiling=1200.0     # Hz — covers high female/child
    )
    # Extract F0 values using the time-based API (parselmouth >=0.4.x)
    n_frames = pitch_obj.get_number_of_frames()
    f0_values = np.array([
        pitch_obj.get_value_at_time(pitch_obj.get_time_from_frame_number(i + 1))
        for i in range(n_frames)
    ])

    # Replace NaN/undef with 0
    f0_clean = np.where(np.isnan(f0_values), 0, f0_values)
    voiced_flag = f0_clean > 0
    return f0_clean, voiced_flag, f0_clean, None


def _pitch_librosa(y, sr):
    """Extract pitch using librosa pyin."""
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C1'),
        fmax=librosa.note_to_hz('C8'),
        sr=sr
    )
    f0_clean = np.nan_to_num(f0, nan=0)
    return f0_clean, voiced_flag, f0_clean, None


# ─── Parselmouth vocal quality (formants, HNR, jitter, shimmer) ─
def compute_parselmouth_vocal_quality(y, sr):
    """Compute Praat-based vocal quality metrics via parselmouth. None if parselmouth unavailable."""
    if not HAS_PARSELMOUTH:
        return None

    snd = parselmouth.Sound(y, sampling_frequency=sr)

    # Formant analysis — vocal tract resonances (F1..F5 per frame)
    formant_obj = snd.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500.0)
    n_ff = formant_obj.get_number_of_frames()
    formants_2d = np.full((n_ff, 5), np.nan)
    formant_times = np.array([formant_obj.get_time_from_frame_number(i + 1) for i in range(n_ff)])
    for i in range(n_ff):
        t = formant_times[i]
        for fi in range(1, 6):
            try:
                formants_2d[i, fi - 1] = formant_obj.get_value_at_time(fi, t)
            except Exception:
                pass

    # Harmonics-to-Noise Ratio — better breathiness measure than ZCR
    harmonicity = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=75.0)
    n_hf = harmonicity.get_number_of_frames()
    hnr_times = np.array([harmonicity.get_time_from_frame_number(i + 1) for i in range(n_hf)])
    # parselmouth >=0.4.x: Harmonicity is a 2D matrix; use get_value_at_xy(time, freq)
    hnr_values = np.nan_to_num(
        np.array([harmonicity.get_value_at_xy(hnr_times[i], 0.0) for i in range(n_hf)]),
        nan=0.0,
    )

    # Jitter and shimmer — voice perturbation (PointProcess can fail on noisy audio)
    jitter, shimmer, jitter_available = 0.0, 0.0, False
    try:
        pp = praat_call(snd, "To PointProcess (periodic, cc)", 60, 1200)
        jitter = float(praat_call(pp, "Get jitter (local)", 0, 0, 0, 0, 0))
        shimmer = float(praat_call(pp, "Get shimmer (local)", 0, 0, 0, 0, 0, 0))
        jitter_available = True
    except Exception:
        pass

    return {
        'formants': formants_2d, 'formant_times': formant_times, 'hnr': hnr_values, 'hnr_times': hnr_times,
        'jitter_local': jitter, 'shimmer_local': shimmer, 'jitter_available': jitter_available,
    }


# ─── Intensity / energy ─────────────────────────────────────────

def compute_intensity_envelope(y, sr, frame_length=2048, hop_length=512):
    """Compute RMS energy envelope and its gradient."""
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_gradient = np.gradient(rms)
    return rms, rms_gradient


# ─── Spectral features for vocal quality ────────────────────────

def compute_spectral_features(y, sr, hop_length=512):
    """Compute spectral features useful for vocal emotion classification."""
    # Spectral centroid — brightness
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    # Spectral bandwidth — timbre width
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=hop_length)[0]
    # Spectral rolloff — high frequency content
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=hop_length)[0]
    # Zero crossing rate — noisiness / breathiness proxy
    zcr = librosa.feature.zero_crossing_rate(y=y, hop_length=hop_length)[0]
    # MFCCs (first 6) — timbre descriptors
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=6, hop_length=hop_length)
    # New: tempogram ratio (swing vs straight), tonnetz (consonance), spectral contrast (timbre)
    tempogram_ratio = librosa.feature.tempogram_ratio(y=y, sr=sr, hop_length=hop_length)[0]
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr, hop_length=hop_length)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=hop_length)

    return {
        'centroid': centroid, 'bandwidth': bandwidth, 'rolloff': rolloff,
        'zcr': zcr, 'mfcc': mfcc,
        'tempogram_ratio': tempogram_ratio, 'tonnetz': tonnetz,
        'spectral_contrast': spectral_contrast,
    }


# ─── Section boundary detection ─────────────────────────────────

def detect_section_boundaries(rms, sr, hop_length=512, min_section_sec=3.0):
    """Detect section boundaries from energy transitions.

    Uses smoothed RMS energy derivative peaks to find where the song
    changes character (verse → chorus, etc.).
    """
    n = len(rms)
    min_frames = int(min_section_sec * sr / hop_length)

    # Smooth heavily to find macro changes
    smooth_window = max(1, n // 30)
    smooth_rms = uniform_filter1d(rms.astype(float), size=smooth_window)

    # Normalise
    if smooth_rms.max() > 0:
        smooth_rms = smooth_rms / smooth_rms.max()

    # Find significant energy transitions
    diff = np.diff(smooth_rms)
    threshold = np.std(diff) * 1.2

    boundaries = [0]
    for i in range(1, len(diff)):
        if abs(diff[i]) > threshold:
            last = boundaries[-1]
            if (i - last) >= min_frames:
                boundaries.append(i)
    boundaries.append(n - 1)

    return boundaries


def label_sections_by_energy(rms, boundaries, hop_length, sr):
    """Assign structural labels (intro/verse/chorus/bridge/outro) based on energy."""
    if len(boundaries) < 2:
        return []

    # Compute average energy per section
    section_energies = []
    for i in range(len(boundaries) - 1):
        s, e = boundaries[i], boundaries[i + 1]
        seg = rms[s:e]
        avg_e = float(np.mean(seg)) if len(seg) > 0 else 0
        section_energies.append(avg_e)

    if not section_energies:
        return []

    mean_energy = np.mean(section_energies)
    std_energy = np.std(section_energies) + 1e-9

    labels = []
    n = len(section_energies)
    for i, e in enumerate(section_energies):
        z = (e - mean_energy) / std_energy
        if i == 0:
            label = "intro"
        elif i == n - 1:
            label = "outro"
        elif z > 1.0:
            label = "chorus"
        elif z > 0.3:
            label = "pre-chorus"
        elif z < -0.5:
            label = "bridge"
        else:
            label = "verse"
        labels.append(label)

    # Build sections with times
    sections = []
    for i in range(len(boundaries) - 1):
        start_sec = round(boundaries[i] * hop_length / sr, 2)
        end_sec = round(boundaries[i + 1] * hop_length / sr, 2)
        sections.append({
            'index': i,
            'start_seconds': start_sec,
            'end_seconds': end_sec,
            'structural_label': labels[i],
            'avg_energy': round(section_energies[i], 5),
        })
    return sections


# ─── Per-section emotion analysis ───────────────────────────────

def analyze_section_emotion(rms, f0, voiced_flag, spectral, sr, start_sec, end_sec, hop_length=512, vocal_quality=None):
    """Analyze emotional characteristics of a time section."""
    start_idx = max(0, int(start_sec * sr / hop_length))
    end_idx = min(len(rms), int(end_sec * sr / hop_length))

    if end_idx <= start_idx:
        return None

    section_rms = rms[start_idx:end_idx]
    section_f0 = f0[start_idx:end_idx]
    section_voiced = voiced_flag[start_idx:end_idx]

    if len(section_rms) == 0:
        return None

    # Intensity metrics
    avg_intensity = float(np.mean(section_rms))
    max_intensity = float(np.max(section_rms))
    min_intensity = float(np.min(section_rms))
    intensity_range = max_intensity - min_intensity

    # Pitch metrics (only voiced frames)
    voiced_f0 = section_f0[section_voiced]
    voiced_f0_nz = voiced_f0[voiced_f0 > 0]

    if len(voiced_f0_nz) > 2:
        avg_pitch = float(np.mean(voiced_f0_nz))
        pitch_std = float(np.std(voiced_f0_nz))
        pitch_range = float(np.max(voiced_f0_nz) - np.min(voiced_f0_nz))

        # Pitch trend: linear regression slope over voiced frames
        x = np.arange(len(voiced_f0_nz))
        coeffs = np.polyfit(x, voiced_f0_nz, 1)
        pitch_trend_val = float(coeffs[0])  # Hz per frame

        # Pitch stability (inverse of jitter-like measure)
        diffs = np.diff(voiced_f0_nz)
        pitch_stability = float(1.0 - min(np.mean(np.abs(diffs)) / (avg_pitch + 1e-9), 1.0))
    else:
        avg_pitch = 0
        pitch_std = 0
        pitch_range = 0
        pitch_trend_val = 0
        pitch_stability = 0.5

    # Vocal effort: combines intensity, pitch range, and instability
    effort_score = 0
    if avg_intensity > 0.02:
        effort_score += 1
    if avg_intensity > 0.06:
        effort_score += 1
    if avg_intensity > 0.12:
        effort_score += 1
    if pitch_range > 80:
        effort_score += 1
    if pitch_range > 200:
        effort_score += 1
    if pitch_stability < 0.7:
        effort_score += 1  # instability = effort

    if effort_score >= 4:
        vocal_effort = "high"
    elif effort_score >= 2:
        vocal_effort = "medium"
    else:
        vocal_effort = "low"

    # Spectral features for this section
    s_centroid = spectral['centroid'][start_idx:end_idx] if start_idx < len(spectral['centroid']) else np.array([])
    s_zcr = spectral['zcr'][start_idx:end_idx] if start_idx < len(spectral['zcr']) else np.array([])
    s_bandwidth = spectral['bandwidth'][start_idx:end_idx] if start_idx < len(spectral['bandwidth']) else np.array([])

    avg_centroid = float(np.mean(s_centroid)) if len(s_centroid) > 0 else 0
    avg_zcr = float(np.mean(s_zcr)) if len(s_zcr) > 0 else 0
    avg_bandwidth = float(np.mean(s_bandwidth)) if len(s_bandwidth) > 0 else 0

    # Breathiness proxy: high ZCR + low energy = breathy
    breathiness = float(min(avg_zcr * 5 - avg_intensity * 50, 1.0))
    breathiness = max(breathiness, 0.0)

    # ── New spectral features (tempogram_ratio, tonnetz, spectral_contrast) ──
    s_tempogram = spectral['tempogram_ratio'][start_idx:end_idx] if start_idx < len(spectral['tempogram_ratio']) else np.array([])
    s_tonnetz = spectral['tonnetz'][:, start_idx:end_idx] if start_idx < spectral['tonnetz'].shape[1] else np.empty((6, 0))
    s_contrast = spectral['spectral_contrast'][:, start_idx:end_idx] if start_idx < spectral['spectral_contrast'].shape[1] else np.empty((7, 0))
    avg_tempogram_ratio = float(np.mean(s_tempogram)) if len(s_tempogram) > 0 else 0.0
    tonnetz_tension = float(np.std(np.mean(s_tonnetz, axis=1)[:2])) if s_tonnetz.size > 0 else 0.0
    avg_spectral_contrast = float(np.mean(s_contrast)) if s_contrast.size > 0 else 0.0
    rhythm_feel = "swing" if avg_tempogram_ratio > 0.6 else "straight" if avg_tempogram_ratio < 0.3 else "mixed"
    harmony_quality = "consonant" if tonnetz_tension < 0.1 else "tense" if tonnetz_tension > 0.3 else "rich"

    # ── Parselmouth vocal quality (formants, HNR, jitter, shimmer) per section ──
    vocal_register, section_hnr_db, section_jitter, section_shimmer = "unknown", 0.0, 0.0, 0.0
    if vocal_quality is not None:
        f_mask = (vocal_quality['formant_times'] >= start_sec) & (vocal_quality['formant_times'] < end_sec)
        h_mask = (vocal_quality['hnr_times'] >= start_sec) & (vocal_quality['hnr_times'] < end_sec)
        formants_sec = vocal_quality['formants'][f_mask]
        if formants_sec.shape[0] >= 3:
            voiced_mask = ~np.isnan(formants_sec[:, 0]) & ~np.isnan(formants_sec[:, 1])
            if np.sum(voiced_mask) >= 3:
                f1 = float(np.nanmean(formants_sec[voiced_mask, 0]))
                f2 = float(np.nanmean(formants_sec[voiced_mask, 1]))
                if f1 > 800 and f2 > 1500: vocal_register = "falsetto"
                elif f1 > 700 and f2 < 1200: vocal_register = "chest"
                elif f1 < 400 and f2 > 1500: vocal_register = "head"
                else: vocal_register = "mixed"
        hnr_sec = vocal_quality['hnr'][h_mask]
        if len(hnr_sec) > 0:
            section_hnr_db = float(np.mean(hnr_sec))
        section_jitter = vocal_quality.get('jitter_local', 0.0)
        section_shimmer = vocal_quality.get('shimmer_local', 0.0)

    return {
        "start_seconds": round(start_sec, 2), "end_seconds": round(end_sec, 2),
        "avg_intensity": round(avg_intensity, 5), "max_intensity": round(max_intensity, 5),
        "intensity_range": round(intensity_range, 5),
        "avg_pitch_hz": round(avg_pitch, 1) if avg_pitch > 0 else 0,
        "pitch_std_hz": round(pitch_std, 1), "pitch_range_hz": round(pitch_range, 1),
        "pitch_trend": "rising" if pitch_trend_val > 3 else "falling" if pitch_trend_val < -3 else "steady",
        "pitch_trend_val": round(pitch_trend_val, 2), "pitch_stability": round(pitch_stability, 3),
        "vocal_effort": vocal_effort, "voiced_ratio": round(float(np.mean(section_voiced)), 3),
        "spectral_centroid": round(avg_centroid, 1), "breathiness": round(breathiness, 3),
        "tempogram_ratio": round(avg_tempogram_ratio, 3), "rhythm_feel": rhythm_feel,
        "tonnetz_tension": round(tonnetz_tension, 3), "harmony_quality": harmony_quality,
        "spectral_contrast": round(avg_spectral_contrast, 3), "vocal_register": vocal_register,
        "hnr_db": round(section_hnr_db, 2), "jitter_pct": round(section_jitter, 3),
        "shimmer_pct": round(section_shimmer, 3),
    }


def classify_emotion(section):
    """Classify the primary emotions of a section based on its computed features.

    Returns a list of 1-4 emotion labels from a 25-label vocabulary that the
    emotion cookbook documents (see references/emotion-analysis.md). Each
    classifier branch contributes 0-1 labels; we de-duplicate and cap at 4.
    """
    emotions = []
    intensity = section.get('avg_intensity', 0)
    pitch_range = section.get('pitch_range_hz', 0)
    vocal_effort = section.get('vocal_effort', 'low')
    pitch_trend = section.get('pitch_trend', 'steady')
    stability = section.get('pitch_stability', 0.5)
    breathiness = section.get('breathiness', 0)
    spectral_centroid = section.get('spectral_centroid', 0)
    hnr = section.get('hnr_db', 20)
    tempo = section.get('tempo_bpm', 100)  # may not be present; safe default

    # 1. Intensity-based (3 states: calm / moderate / intense)
    if intensity > 0.12:
        emotions.append("intense")
    elif intensity > 0.05:
        emotions.append("moderate")
    else:
        emotions.append("calm")

    # 2. Pitch range → drama (3 states: controlled / expressive / dramatic)
    if pitch_range > 200:
        emotions.append("dramatic")
    elif pitch_range > 100:
        emotions.append("expressive")
    else:
        emotions.append("controlled")

    # 3. Vocal effort (4 states: restrained / engaged / passionate / desperate)
    if vocal_effort == "high":
        if stability < 0.5:
            emotions.append("desperate")
        else:
            emotions.append("passionate")
    elif vocal_effort == "medium":
        emotions.append("engaged")
    else:
        emotions.append("restrained")

    # 4. Pitch trend (2 states: building / releasing)
    if pitch_trend == "rising":
        emotions.append("building")
    elif pitch_trend == "falling":
        emotions.append("releasing")

    # 5. Breathiness (1 state: breathy) — close-mic intimate quality
    if breathiness > 0.6:
        emotions.append("breathy")

    # 6. Calm + low breathiness + low pitch range → intimate / vulnerable
    if intensity < 0.04 and breathiness < 0.3 and pitch_range < 100:
        emotions.append("intimate")

    # 7. Calm + high stability + high breathiness → wistful / longing
    if intensity < 0.05 and stability > 0.7 and breathiness > 0.4:
        emotions.append("wistful")

    # 8. High intensity + dramatic pitch range → triumphant (uplift)
    if intensity > 0.15 and pitch_range > 250:
        emotions.append("triumphant")

    # 9. High intensity + low stability + very high effort → defiant
    if intensity > 0.10 and stability < 0.3 and vocal_effort == "high":
        emotions.append("defiant")

    # 10. Low intensity + high breathiness + high spectral centroid (airy) → dreamy
    if intensity < 0.04 and breathiness > 0.5 and spectral_centroid > 2500:
        emotions.append("dreamy")

    # 11. Low intensity + very stable + descending pitch → contemplative
    if intensity < 0.04 and stability > 0.8 and pitch_trend == "falling":
        emotions.append("contemplative")

    # 12. Moderate intensity + rising pitch trend + low breathiness → hopeful
    if 0.05 < intensity < 0.10 and pitch_trend == "rising" and breathiness < 0.3:
        emotions.append("hopeful")

    # 13. Moderate intensity + falling pitch + high breathiness → nostalgic
    if 0.04 < intensity < 0.10 and pitch_trend == "falling" and breathiness > 0.4:
        emotions.append("nostalgic")

    # 14. High intensity + high breathiness + low HNR → raw / mournful
    if intensity > 0.08 and hnr < 12 and breathiness > 0.5:
        emotions.append("mournful")

    # 15. Dramatic + low HNR + high effort → aggressive / angry
    if pitch_range > 200 and hnr < 10 and vocal_effort == "high":
        emotions.append("aggressive")

    # 16. Calm + low breathiness + low HNR → mysterious
    if intensity < 0.03 and breathiness < 0.3 and hnr < 14:
        emotions.append("mysterious")

    # 17. Euphoric — high intensity + bright + high stability (chorus climax)
    if intensity > 0.18 and stability > 0.7 and spectral_centroid > 3000:
        emotions.append("euphoric")

    # 18. Restless — moderate intensity + high pitch range + low stability
    if 0.06 < intensity < 0.12 and pitch_range > 200 and stability < 0.4:
        emotions.append("restless")

    # 19. Bittersweet — moderate intensity + falling trend + breathy
    if 0.04 < intensity < 0.08 and pitch_trend == "falling" and breathiness > 0.5:
        emotions.append("bittersweet")

    # 20. Yearning — slow tempo + rising pitch + low intensity
    if tempo < 90 and pitch_trend == "rising" and intensity < 0.05:
        emotions.append("yearning")

    # 21. Longing — low intensity + breathy + descending
    if intensity < 0.04 and breathiness > 0.4 and pitch_trend == "falling":
        emotions.append("longing")

    # 22. Vulnerable — very low intensity + intimate + breathy
    if intensity < 0.025 and breathiness > 0.5:
        emotions.append("vulnerable")

    # 23. Mystical — low intensity + high stability + spectral centroid moderate
    if intensity < 0.04 and stability > 0.8 and 1500 < spectral_centroid < 3500:
        emotions.append("mystical")

    # 24. Euphoric-graceful — high intensity + flowing + smooth (placeholder logic, kept for richness)
    # Skipped to avoid noise.

    # 25. Steady (anchor) — used when nothing else triggered beyond baseline
    if len(emotions) <= 1:
        emotions.append("grounded")

    # De-duplicate, cap at 4
    seen = set()
    unique = []
    for e in emotions:
        if e not in seen:
            unique.append(e)
            seen.add(e)
        if len(unique) >= 4:
            break
    return unique


# ─── Intensity curve pattern detection ──────────────────────────

def detect_intensity_curve(emotion_sections):
    """Detect the overall intensity curve pattern across all sections."""
    if len(emotion_sections) < 3:
        return {"pattern": "unknown", "description": "Not enough sections"}

    intensities = [s['avg_intensity'] for s in emotion_sections]

    # Normalise intensities to 0-1
    i_min, i_max = min(intensities), max(intensities)
    i_range = i_max - i_min + 1e-9
    normed = [(v - i_min) / i_range for v in intensities]

    n = len(normed)

    # Linear regression to find overall trend
    x = np.arange(n)
    slope, _ = np.polyfit(x, normed, 1)

    # Find peak position
    peak_idx = int(np.argmax(normed))
    peak_ratio = peak_idx / n if n > 0 else 0.5

    # Count direction changes (for wave detection)
    direction_changes = 0
    for i in range(2, n):
        prev_dir = normed[i-1] - normed[i-2]
        curr_dir = normed[i] - normed[i-1]
        if prev_dir * curr_dir < 0:
            direction_changes += 1

    # Count local maxima (peaks)
    peaks = 0
    for i in range(1, n - 1):
        if normed[i] > normed[i-1] and normed[i] > normed[i+1]:
            peaks += 1

    # Classify
    if peaks >= 3 or direction_changes >= n * 0.4:
        pattern = "wave"
        desc = "Multiple emotional peaks throughout — dynamic, varied intensity"
    elif slope > 0.03:
        pattern = "crescendo"
        desc = "Builds steadily from calm to intense — tension rising throughout"
    elif slope < -0.03:
        pattern = "decrescendo"
        desc = "Starts intense, gradually releases tension"
    elif peak_ratio > 0.75:
        pattern = "climax_late"
        desc = "Emotional climax toward the end — delayed gratification"
    elif peak_ratio < 0.25:
        pattern = "climax_early"
        desc = "Opens with maximum intensity, then retreats"
    else:
        pattern = "wave"
        desc = "Central climax with surrounding variation"

    return {
        "pattern": pattern,
        "description": desc,
        "peak_position_ratio": round(peak_ratio, 2),
        "peak_section_index": peak_idx,
        "overall_slope": round(float(slope), 4),
        "direction_changes": direction_changes,
        "num_peaks": peaks,
    }


# ─── Repetitive intensification detection ───────────────────────

def detect_repetitive_intensification(rms, sr, hop_length=512, window_sec=5.0):
    """Detect if successive similar-energy windows increase in intensity.

    Looks for repeated energy-level patterns where each repetition is louder
    than the last — the hallmark of intensifying refrains.
    """
    window_frames = int(window_sec * sr / hop_length)
    if window_frames < 10 or len(rms) < window_frames * 3:
        return {"detected": False, "confidence": 0.0, "description": "Audio too short for analysis"}

    # Compute energy per window
    n_windows = len(rms) // window_frames
    window_energies = []
    for i in range(n_windows):
        seg = rms[i * window_frames:(i + 1) * window_frames]
        window_energies.append(float(np.mean(seg)))

    if len(window_energies) < 3:
        return {"detected": False, "confidence": 0.0, "description": "Not enough windows"}

    # Look for groups of consecutive windows with similar energy pattern
    # but increasing magnitude
    intensification_found = False
    best_group = []
    best_increase = 0

    # Compare adjacent windows for increasing energy runs
    increasing_run = [0]
    for i in range(1, len(window_energies)):
        if window_energies[i] > window_energies[i-1] * 1.05:  # 5% increase threshold
            increasing_run.append(i)
        else:
            if len(increasing_run) >= 3:
                run_energies = [window_energies[j] for j in increasing_run]
                increase = max(run_energies) / (min(run_energies) + 1e-9)
                if increase > best_increase:
                    best_increase = increase
                    best_group = list(increasing_run)
                    intensification_found = True
            increasing_run = [i]

    # Check final run
    if len(increasing_run) >= 3:
        run_energies = [window_energies[j] for j in increasing_run]
        increase = max(run_energies) / (min(run_energies) + 1e-9)
        if increase > best_increase:
            best_increase = increase
            best_group = list(increasing_run)
            intensification_found = True

    if intensification_found and best_increase > 1.15:
        return {
            "detected": True,
            "confidence": round(min((best_increase - 1.0) * 2, 1.0), 2),
            "pattern": "crescendo_repetitive",
            "increase_ratio": round(best_increase, 2),
            "affected_windows": best_group,
            "description": f"Detected intensifying repetition — energy increases {best_increase:.1f}x across repetitions",
            "music_generation_note": "Increase dynamics and layer density with each repetition"
        }

    return {
        "detected": False,
        "confidence": 0.0,
        "description": "No significant repetitive intensification detected",
        "music_generation_note": "Maintain steady dynamics across repeated sections"
    }


# ─── Sudden emotional shifts ────────────────────────────────────

def detect_emotional_shifts(emotion_sections):
    """Detect sudden vs gradual emotional transitions between sections."""
    if len(emotion_sections) < 2:
        return []

    shifts = []
    for i in range(1, len(emotion_sections)):
        prev = emotion_sections[i - 1]
        curr = emotion_sections[i]

        # Intensity change
        i_change = abs(curr['avg_intensity'] - prev['avg_intensity'])
        # Pitch change
        p_change = abs(curr.get('avg_pitch_hz', 0) - prev.get('avg_pitch_hz', 0))
        # Effort change
        effort_levels = {'low': 0, 'medium': 1, 'high': 2}
        e_change = abs(effort_levels.get(curr.get('vocal_effort', 'low'), 0) -
                       effort_levels.get(prev.get('vocal_effort', 'low'), 0))

        # Classify shift magnitude
        shift_score = i_change * 100 + (p_change / 50) + e_change * 0.5

        if shift_score > 2.0:
            shifts.append({
                "at_seconds": curr['start_seconds'],
                "type": "sudden" if shift_score > 4.0 else "gradual",
                "score": round(shift_score, 2),
                "from_effort": prev.get('vocal_effort', 'unknown'),
                "to_effort": curr.get('vocal_effort', 'unknown'),
                "from_intensity": prev['avg_intensity'],
                "to_intensity": curr['avg_intensity'],
                "description": f"{'Sudden' if shift_score > 4.0 else 'Gradual'} shift at {curr['start_seconds']:.1f}s"
            })

    return shifts


# ─── Overall emotion profile ────────────────────────────────────

def generate_emotion_profile(emotion_sections, intensity_curve, repetitive_analysis, emotional_shifts):
    """Generate overall emotion profile for the entire song."""
    if not emotion_sections:
        return {"status": "insufficient_data"}

    all_intensities = [s['avg_intensity'] for s in emotion_sections]
    all_pitch_ranges = [s['pitch_range_hz'] for s in emotion_sections]

    avg_intensity = float(np.mean(all_intensities))
    max_intensity = float(np.max(all_intensities))
    min_intensity = float(np.min(all_intensities))

    # Count effort distribution
    efforts = [s['vocal_effort'] for s in emotion_sections]
    high_count = efforts.count('high')
    total = len(efforts)

    # Determine overall emotion type
    if avg_intensity > 0.08 and high_count > total * 0.3:
        overall_type = "intense_dramatic"
    elif avg_intensity > 0.05 and max_intensity > 0.1:
        overall_type = "dynamic_passionate"
    elif avg_intensity < 0.03:
        overall_type = "calm_intimate"
    else:
        overall_type = "moderate_varied"

    # Emotional arc
    curve_pattern = intensity_curve.get('pattern', 'unknown')
    arc_descriptions = {
        'crescendo': "Starts calm, builds steadily to emotional climax",
        'decrescendo': "Opens with maximum intensity, gradually releases",
        'climax_late': "Slow build with powerful climax near the end",
        'climax_early': "Opens powerfully then settles into more reflective mood",
        'wave': "Multiple emotional peaks — dynamic journey throughout",
        'unknown': "Emotional arc could not be determined",
    }

    # Sudden shifts summary
    sudden_count = sum(1 for s in emotional_shifts if s.get('type') == 'sudden')
    gradual_count = sum(1 for s in emotional_shifts if s.get('type') == 'gradual')

    return {
        "overall_emotion_type": overall_type,
        "emotional_arc": arc_descriptions.get(curve_pattern, "Varied emotional journey"),
        "avg_intensity": round(avg_intensity, 5),
        "max_intensity": round(max_intensity, 5),
        "min_intensity": round(min_intensity, 5),
        "dynamic_range": round(max_intensity - min_intensity, 5),
        "avg_pitch_variation_hz": round(float(np.mean(all_pitch_ranges)), 1),
        "intensity_curve": intensity_curve,
        "repetitive_intensification": repetitive_analysis,
        "emotional_shifts": emotional_shifts,
        "shifts_summary": {
            "sudden_shifts": sudden_count,
            "gradual_shifts": gradual_count,
            "total_shifts": len(emotional_shifts)
        },
        "sections_analyzed": len(emotion_sections),
        "pitch_backend": "parselmouth_praat" if HAS_PARSELMOUTH else "librosa_pyin",
    }


# ─── Music generation hints ─────────────────────────────────────

# ─── Vocal speed / syllable elongation detection ────────────────

def estimate_syllable_count_from_onsets(y, sr, hop_length=512):
    """Estimate syllable-level onsets using spectral flux onset detection.

    Returns onset times in seconds, which approximate syllable/phone boundaries
    for vocal-dominated audio.
    """
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        y=y, sr=sr, onset_envelope=onset_env,
        hop_length=hop_length, backtrack=True
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    return onset_times


def detect_pitch_bends(f0, sr, hop_length=512, min_duration_sec=0.3):
    """Detect pitch bends / slides at phrase endings.

    A pitch bend is a sustained monotonic pitch movement (rising or falling)
    over at least min_duration_sec. These are hallmarks of emotional elongation:
    the vocalist holds a note and bends the pitch for expressiveness.

    Returns list of {start, end, direction, range_hz, duration_sec}.
    """
    bends = []
    voiced_idx = np.where(f0 > 0)[0]
    if len(voiced_idx) < 10:
        return bends

    # Work in contiguous voiced segments
    breaks = np.where(np.diff(voiced_idx) > 3)[0]  # gap > 3 frames = break
    segments = np.split(voiced_idx, breaks + 1)

    for seg in segments:
        if len(seg) < int(min_duration_sec * sr / hop_length):
            continue

        pitches = f0[seg]
        # Smooth for bend detection
        if len(pitches) > 5:
            smooth = uniform_filter1d(pitches.astype(float), size=5)
        else:
            smooth = pitches.astype(float)

        # Check last 30% of segment for monotonic slide
        tail_start = int(len(smooth) * 0.7)
        tail = smooth[tail_start:]

        if len(tail) < 3:
            continue

        diffs = np.diff(tail)
        # If >70% of diffs are same sign → monotonic slide
        pos = np.sum(diffs > 0)
        neg = np.sum(diffs < 0)
        total = len(diffs)

        if pos / total > 0.7:
            direction = "rising"
        elif neg / total > 0.7:
            direction = "falling"
        else:
            continue

        pitch_range = float(np.max(tail) - np.min(tail))
        if pitch_range < 20:  # minimum 20Hz slide to count
            continue

        start_sec = float(seg[tail_start] * hop_length / sr)
        end_sec = float(seg[-1] * hop_length / sr)
        duration = end_sec - start_sec

        bends.append({
            "start_seconds": round(start_sec, 2),
            "end_seconds": round(end_sec, 2),
            "direction": direction,
            "pitch_range_hz": round(pitch_range, 1),
            "duration_seconds": round(duration, 2),
        })

    return bends


def detect_vocal_speed_patterns(rms, f0, onset_times, sr, hop_length, emotion_sections):
    """Detect vocal speed variations and syllable elongation patterns.

    Analyzes:
    - Per-section syllable density (syllables per second)
    - Tempo deviation: how much faster/slower each section is vs average
    - Elongation detection: sections with significantly lower syllable density
    - Speed classification: normal / slowed / accelerated per section

    Returns dict with per-section speed data and overall pattern.
    """
    if len(onset_times) < 5 or len(emotion_sections) < 2:
        return {
            "detected": False,
            "description": "Insufficient data for vocal speed analysis",
            "sections": [],
        }

    # Compute per-section syllable density
    section_speeds = []
    for sec in emotion_sections:
        start = sec['start_seconds']
        end = sec['end_seconds']
        duration = end - start
        if duration < 0.5:
            continue

        # Count onsets within this section
        mask = (onset_times >= start) & (onset_times < end)
        syllable_count = int(np.sum(mask))

        if syllable_count < 1:
            syllable_count = max(1, int(duration / 0.5))  # rough estimate

        syllables_per_sec = syllable_count / duration
        avg_syllable_duration = duration / syllable_count

        section_speeds.append({
            "section_index": sec.get('section_index', 0),
            "structural_label": sec.get('structural_label', 'section'),
            "start_seconds": round(start, 2),
            "end_seconds": round(end, 2),
            "duration_seconds": round(duration, 2),
            "estimated_syllables": syllable_count,
            "syllables_per_second": round(syllables_per_sec, 2),
            "avg_syllable_duration_sec": round(avg_syllable_duration, 3),
        })

    if len(section_speeds) < 2:
        return {
            "detected": False,
            "description": "Too few sections for speed analysis",
            "sections": section_speeds,
        }

    # Compute average syllable density across all sections
    all_densities = [s['syllables_per_second'] for s in section_speeds]
    avg_density = float(np.mean(all_densities))
    std_density = float(np.std(all_densities)) + 1e-6

    # Classify each section's speed
    for s in section_speeds:
        z = (s['syllables_per_second'] - avg_density) / std_density
        if z < -1.0:
            s["speed_classification"] = "slowed"
        elif z > 1.0:
            s["speed_classification"] = "accelerated"
        else:
            s["speed_classification"] = "normal"

        s["tempo_deviation"] = round(
            (s['syllables_per_second'] - avg_density) / avg_density, 3
        )

    # Detect overall speed pattern
    slowed_sections = [s for s in section_speeds if s['speed_classification'] == 'slowed']
    accelerated_sections = [s for s in section_speeds if s['speed_classification'] == 'accelerated']

    # Check if final section(s) are slowed → classic emotional elongation pattern
    last_two = section_speeds[-2:] if len(section_speeds) >= 2 else section_speeds
    final_slowed = any(s['speed_classification'] == 'slowed' for s in last_two)

    # Check for deceleration trend (sections getting progressively slower)
    if len(section_speeds) >= 3:
        densities = [s['syllables_per_second'] for s in section_speeds]
        x = np.arange(len(densities))
        speed_slope, _ = np.polyfit(x, densities, 1)
        deceleration_detected = bool(speed_slope < -0.1 * avg_density)
    else:
        speed_slope = 0.0
        deceleration_detected = False

    # Determine overall pattern
    if deceleration_detected and final_slowed:
        pattern = "decelerating"
        desc = "Vocals progressively slow down, especially at the end — emotional elongation pattern"
    elif final_slowed and len(slowed_sections) > 0:
        pattern = "late_elongation"
        desc = "Final sections feature elongated syllables — classic emotional climax delivery"
    elif deceleration_detected:
        pattern = "gradual_slowing"
        desc = "Vocal delivery gradually slows throughout the song"
    elif len(accelerated_sections) > len(slowed_sections):
        pattern = "accelerating"
        desc = "Vocal delivery tends faster than average — urgent, driving"
    else:
        pattern = "steady"
        desc = "Vocal speed remains relatively consistent"

    # Build elongation report
    elongation_report = {
        "pattern": pattern,
        "description": desc,
        "average_syllables_per_second": round(avg_density, 2),
        "speed_slope": round(float(speed_slope), 4),
        "deceleration_detected": bool(deceleration_detected),
        "final_sections_slowed": bool(final_slowed),
        "slowed_sections_count": len(slowed_sections),
        "accelerated_sections_count": len(accelerated_sections),
        "sections": section_speeds,
        "music_generation_note": _speed_pattern_to_music_note(
            pattern, slowed_sections, final_slowed, avg_density
        ),
    }

    return elongation_report


def _speed_pattern_to_music_note(pattern, slowed_sections, final_slowed, avg_density):
    """Convert detected vocal speed pattern to music generation instructions."""
    notes = []

    if pattern == "decelerating":
        notes.append(
            "Vocal delivery progressively slows — for each section, increase the space between words"
        )
        notes.append(
            "Final chorus/section should be sung with stretched, elongated syllables for emotional emphasis"
        )
    elif pattern == "late_elongation":
        notes.append(
            "Final sections feature significant syllable elongation — slow down delivery for emotional weight"
        )
    elif pattern == "gradual_slowing":
        notes.append(
            "Tempo gradually decreases throughout — start at normal speed, progressively stretch phrases"
        )
    elif pattern == "accelerating":
        notes.append(
            "Vocal delivery accelerates — urgent, driving pace throughout"
        )
        return " ".join(notes) if notes else "Maintain steady vocal pace"

    if final_slowed and slowed_sections:
        slowest = min(slowed_sections, key=lambda s: s['syllables_per_second'])
        ratio = round(slowest['syllables_per_second'] / avg_density, 2)
        notes.append(
            f"Slowest section ({slowest['structural_label']}) at {ratio}x average speed — "
            f"use {slowest['estimated_syllables']} syllables over {slowest['duration_seconds']}s "
            f"(stretch each syllable to ~{slowest['avg_syllable_duration_sec']}s)"
        )

    return " ".join(notes) if notes else "Maintain steady vocal pace"


# ─── Silence / pause gap detection ──────────────────────────────

def detect_silence_gaps(rms, sr, hop_length=512, min_silence_sec=1.0):
    """Detect silence gaps and pauses in the audio.

    Finds sections where energy drops below a threshold for at least min_silence_sec.
    These are natural pauses in the song — important for dramatic effect.

    Returns list of {start_seconds, end_seconds, duration_seconds, avg_energy}.
    """
    # Threshold: consider anything below 20% of median energy as "silent/pause"
    median_energy = float(np.median(rms))
    silence_threshold = median_energy * 0.15

    min_frames = int(min_silence_sec * sr / hop_length)

    # Find frames below threshold
    quiet_mask = rms < silence_threshold

    gaps = []
    in_gap = False
    gap_start = 0

    for i in range(len(quiet_mask)):
        if quiet_mask[i] and not in_gap:
            in_gap = True
            gap_start = i
        elif not quiet_mask[i] and in_gap:
            in_gap = False
            gap_length = i - gap_start
            if gap_length >= min_frames:
                start_sec = round(gap_start * hop_length / sr, 2)
                end_sec = round(i * hop_length / sr, 2)
                gap_energy = float(np.mean(rms[gap_start:i]))
                gaps.append({
                    "start_seconds": start_sec,
                    "end_seconds": end_sec,
                    "duration_seconds": round(end_sec - start_sec, 2),
                    "avg_energy": round(gap_energy, 6),
                    "relative_energy": round(gap_energy / median_energy, 3),
                })

    # Handle gap that extends to end of audio
    if in_gap and (len(quiet_mask) - gap_start) >= min_frames:
        start_sec = round(gap_start * hop_length / sr, 2)
        end_sec = round(len(quiet_mask) * hop_length / sr, 2)
        gap_energy = float(np.mean(rms[gap_start:]))
        gaps.append({
            "start_seconds": start_sec,
            "end_seconds": end_sec,
            "duration_seconds": round(end_sec - start_sec, 2),
            "avg_energy": round(gap_energy, 6),
            "relative_energy": round(gap_energy / median_energy, 3),
        })

    return gaps


# ─── Music generation hints ────────────────────────────────────────

def generate_music_hints(emotion_profile):
    """Generate specific music generation instructions from emotion analysis."""
    hints = []
    curve = emotion_profile.get('intensity_curve', {}).get('pattern', 'unknown')
    dynamic_range = emotion_profile.get('dynamic_range', 0)
    overall = emotion_profile.get('overall_emotion_type', '')

    # Intensity curve → arrangement strategy
    # CRITICAL: 'sparse' always means FEWER instruments, not NO instruments
    curve_hints = {
        'crescendo': "Start with reduced arrangement (2 instruments), progressively add layers, reach full orchestration at climax — instruments always present",
        'decrescendo': "Open with full arrangement, gradually reduce to fewer instruments — but never drop to silence or a cappella",
        'climax_late': "Keep arrangement restrained through first two-thirds (2-3 instruments), then explode into full power for climax",
        'climax_early': "Powerful opening with full arrangement, then settle into warmer arrangement with fewer instruments",
        'wave': "Vary arrangement density — fuller for peaks, reduced for valleys — but always keep at least 2 instruments active",
    }
    if curve in curve_hints:
        hints.append(curve_hints[curve])

    # Dynamic range → contrast
    if dynamic_range > 0.08:
        hints.append("Strong dynamic contrast: quiet passages contrasted with loud climaxes — use the full range, add 1-2s dramatic pauses between major sections")
    elif dynamic_range > 0.03:
        hints.append("Moderate dynamic variation — gentle swells but no extreme contrast")
    else:
        hints.append("Consistent dynamics throughout — intimate, even-keeled delivery")

    # Repetitive intensification
    rep = emotion_profile.get('repetitive_intensification', {})
    if rep.get('detected'):
        ratio = rep.get('increase_ratio', 1)
        hints.append(f"For repeated phrases: each repetition should be {ratio:.1f}x more intense — add instruments, raise volume, increase urgency")
        hints.append("Progressively add backing vocals or harmonies on repeated phrases")

    # Sudden shifts → add pause instructions
    shifts = emotion_profile.get('emotional_shifts', [])
    sudden_shifts = [s for s in shifts if s.get('type') == 'sudden']
    if sudden_shifts:
        positions = [f"{s['at_seconds']:.0f}s" for s in sudden_shifts[:3]]
        hints.append(f"Add 1-2 second dramatic pauses before intensity shifts at: {', '.join(positions)} — pauses should have reverb tail, not dead silence")

    # Overall emotion → mood keywords
    mood_map = {
        'intense_dramatic': "Passionate, urgent, theatrical delivery — think stage performance",
        'dynamic_passionate': "Alternating between tender and powerful moments",
        'calm_intimate': "Whispered, close-mic feel — like a private confession",
        'moderate_varied': "Balanced delivery with natural emotional ebb and flow",
    }
    if overall in mood_map:
        hints.append(mood_map[overall])

    # CRITICAL: anti-sparse-silence guard
    hints.append("IMPORTANT: 'sparse' or 'reduced' arrangement means FEWER instruments playing, NOT silence or a cappella — always keep at least accordion/piano + bass active")

    return hints


# ─── Main ───────────────────────────────────────────────────────

def main(return_dict=False):
    """Analyze vocal emotion dynamics from audio.

    If return_dict is True, the function returns the analysis dict instead of
    printing it to stdout. This is the preferred entry point for programmatic
    callers (e.g., analysis_orchestrator.py) since it avoids fragile stdout
    capture. When return_dict is False (default, CLI behavior), the function
    prints JSON to stdout (or to --output file).
    """
    parser = argparse.ArgumentParser(description='Analyze vocal emotion dynamics from audio')
    parser.add_argument('audio', help='Audio file path (WAV/MP3/FLAC)')
    parser.add_argument('--sections', type=int, default=None,
                        help='Number of sections (default: auto-detect from energy)')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--hop-length', type=int, default=512, help='Hop length for analysis')
    args = parser.parse_args()

    result = analyze_audio(args)

    if return_dict:
        return result

    _cli_output(result, args.output)


def analyze_audio(args):
    """Run the full vocal emotion analysis pipeline. Returns the result dict.

    This is the programmatic entry point that returns the analysis dict.
    Use main(return_dict=True) from other scripts; use main() from the CLI.
    """
    print(f"Loading: {args.audio}", file=sys.stderr)

    # Load audio — librosa handles many formats via soundfile/audioread
    y, sr = librosa.load(args.audio, sr=22050)
    duration = len(y) / sr
    hop = args.hop_length

    print(f"Duration: {duration:.1f}s | SR: {sr}Hz | Parselmouth: {HAS_PARSELMOUTH}", file=sys.stderr)

    # ── Feature extraction ──
    f0, voiced_flag, f0_clean, _ = extract_pitch_contour(y, sr)
    rms, rms_gradient = compute_intensity_envelope(y, sr, hop_length=hop)
    spectral = compute_spectral_features(y, sr, hop_length=hop)

    # ── HPSS: harmonic-percussive separation ──
    harmonic_y, percussive_y = librosa.effects.hpss(y)
    harmonic_energy = float(np.sum(harmonic_y ** 2))
    percussive_energy = float(np.sum(percussive_y ** 2))
    total_energy = harmonic_energy + percussive_energy + 1e-12
    harmonic_ratio = harmonic_energy / total_energy
    percussive_ratio = percussive_energy / total_energy
    hpss_classification = "smooth_melodic" if harmonic_ratio > 0.7 else "percussive_rhythmic" if harmonic_ratio < 0.4 else "balanced"

    # ── LUFS/LRA dynamic profiling (pyloudnorm) ──
    if HAS_PYLOUDNORM:
        meter = pyln.Meter(sr)
        loudness_lufs = meter.integrated_loudness(y.reshape(1, -1) if y.ndim == 1 else y)
        loudness_range = meter.loudness_range(y.reshape(1, -1) if y.ndim == 1 else y)
        # Classify dynamics
        if loudness_range > 15:
            dynamics_class = "wide_dynamic_range"
            dynamics_desc = "Highly dynamic — quiet passages and loud climaxes, minimal compression"
        elif loudness_range > 8:
            dynamics_class = "moderate_dynamics"
            dynamics_desc = "Moderate dynamic variation — some compression but natural swells"
        else:
            dynamics_class = "compressed_consistent"
            dynamics_desc = "Heavily compressed — wall-of-sound, consistent energy throughout"
        loudness_data = {
            "integrated_lufs": round(float(loudness_lufs), 1),
            "loudness_range_lra": round(float(loudness_range), 1),
            "dynamics_classification": dynamics_class,
            "dynamics_description": dynamics_desc,
        }
    else:
        loudness_data = {"note": "pyloudnorm not installed — install with: pip install pyloudnorm"}

    # ── Chord progression extraction (autochord) ──
    if HAS_AUTOCHORD:
        try:
            chords = autochord.recognize(args.audio)
            # chords is list of (start_time, end_time, chord_label)
            # Summarize: unique chords, progression
            chord_labels = [c[2] for c in chords]
            unique_chords = list(dict.fromkeys(chord_labels))  # preserve order
            # Get main progression (most common sequence of 4 chords)
            chord_progression = unique_chords[:8]  # first 8 unique chords
            chords_data = {
                "detected": True,
                "chord_timeline": [{"start": round(c[0], 2), "end": round(c[1], 2), "chord": c[2]} for c in chords],
                "unique_chords": unique_chords,
                "main_progression": chord_progression,
                "progression_string": " - ".join(chord_progression),
            }
        except Exception as e:
            chords_data = {"detected": False, "error": str(e)}
    else:
        chords_data = {"note": "autochord not installed — install with: pip install autochord"}

    # ── Song structure detection (allin1) ──
    if HAS_ALLIN1:
        try:
            struct = allin1.analyze(args.audio)
            # struct has: segments with labels and boundaries
            structure_data = {
                "detected": True,
                "segments": [],
                "segment_labels": [],
            }
            if hasattr(struct, 'segments') and struct.segments:
                for seg in struct.segments:
                    structure_data["segments"].append({
                        "label": seg.label if hasattr(seg, 'label') else str(seg),
                        "start_seconds": round(float(seg.start), 2) if hasattr(seg, 'start') else 0,
                        "end_seconds": round(float(seg.end), 2) if hasattr(seg, 'end') else 0,
                    })
                    if hasattr(seg, 'label'):
                        structure_data["segment_labels"].append(seg.label)
            else:
                # allin1 returns different structures depending on version
                # Try alternative access patterns
                if hasattr(struct, 'boundaries'):
                    structure_data["boundaries"] = [round(float(b), 2) for b in struct.boundaries]
                if hasattr(struct, 'labels'):
                    structure_data["segment_labels"] = struct.labels
        except Exception as e:
            structure_data = {"detected": False, "error": str(e)}
    else:
        structure_data = {"note": "allin1 not installed — install with: pip install allin1"}

    # ── Parselmouth vocal quality (formants, HNR, jitter, shimmer) ──
    vocal_quality = compute_parselmouth_vocal_quality(y, sr) if HAS_PARSELMOUTH else None
    if vocal_quality is not None:
        voiced_hnr = vocal_quality['hnr'][vocal_quality['hnr'] > 0]
        avg_hnr_overall = float(np.mean(voiced_hnr)) if len(voiced_hnr) > 0 else 0.0
        print(f"Vocal quality: HNR={avg_hnr_overall:.1f}dB, jitter={vocal_quality['jitter_local']:.2f}%, "
              f"shimmer={vocal_quality['shimmer_local']:.2f}%, harmonic_ratio={harmonic_ratio:.2f}",
              file=sys.stderr)

    # ── Section boundary detection ──
    boundaries = detect_section_boundaries(rms, sr, hop_length=hop)
    struct_sections = label_sections_by_energy(rms, boundaries, hop, sr)

    # If user specified a fixed number of sections, override
    if args.sections:
        n = args.sections
        section_dur = duration / n
        fixed_sections = []
        for i in range(n):
            fixed_sections.append({
                'index': i,
                'start_seconds': round(i * section_dur, 2),
                'end_seconds': round((i + 1) * section_dur, 2),
                'structural_label': 'section',
                'avg_energy': 0,
            })
        struct_sections = fixed_sections
        # Re-compute energies for fixed sections
        for sec in struct_sections:
            si = max(0, int(sec['start_seconds'] * sr / hop))
            ei = min(len(rms), int(sec['end_seconds'] * sr / hop))
            if ei > si:
                sec['avg_energy'] = round(float(np.mean(rms[si:ei])), 5)

    print(f"Sections: {len(struct_sections)} ({'fixed' if args.sections else 'auto-detected'})", file=sys.stderr)

    # ── Per-section emotion analysis ──
    emotion_sections = []
    for sec in struct_sections:
        result = analyze_section_emotion(rms, f0, voiced_flag, spectral, sr,
            sec['start_seconds'], sec['end_seconds'], hop_length=hop, vocal_quality=vocal_quality)
        if result:
            result['section_index'] = sec['index']
            result['structural_label'] = sec.get('structural_label', 'section')
            result['emotion_classification'] = classify_emotion(result)
            emotion_sections.append(result)

    # ── Pattern detection ──
    intensity_curve = detect_intensity_curve(emotion_sections)
    repetitive = detect_repetitive_intensification(rms, sr, hop_length=hop)
    emotional_shifts = detect_emotional_shifts(emotion_sections)

    # ── Overall profile ──
    emotion_profile = generate_emotion_profile(
        emotion_sections, intensity_curve, repetitive, emotional_shifts
    )
    music_hints = generate_music_hints(emotion_profile)

    # ── Vocal speed / syllable elongation analysis ──
    onset_times = estimate_syllable_count_from_onsets(y, sr, hop_length=hop)
    pitch_bends = detect_pitch_bends(f0, sr, hop_length=hop)
    vocal_speed = detect_vocal_speed_patterns(
        rms, f0, onset_times, sr, hop, emotion_sections
    )

    # ── Silence / pause detection ──
    silence_gaps = detect_silence_gaps(rms, sr, hop, min_silence_sec=1.0)

    print(f"Vocal speed pattern: {vocal_speed.get('pattern', 'unknown')} | "
          f"Pitch bends: {len(pitch_bends)} | "
          f"Avg syll/sec: {vocal_speed.get('average_syllables_per_second', 'N/A')} | "
          f"Silence gaps: {len(silence_gaps)}", file=sys.stderr)

    # ── Compile result ──
    # Overall parselmouth vocal quality summary
    if vocal_quality is not None:
        voiced_hnr = vocal_quality['hnr'][vocal_quality['hnr'] > 0]
        avg_hnr = float(np.mean(voiced_hnr)) if len(voiced_hnr) > 0 else 0.0
        hnr_calibrated = len(voiced_hnr) > 0
        hnr_classification = "clean_resonant" if avg_hnr > 20 else "slightly_breathy" if avg_hnr > 10 else "very_breathy_noisy"
        jitter, shimmer = vocal_quality['jitter_local'], vocal_quality['shimmer_local']
        perturbation_calibrated = bool(vocal_quality.get('jitter_available')) and (jitter > 0 or shimmer > 0)
        voice_quality = "pressed_strained" if jitter > 1.0 else "smooth_clean" if jitter < 0.5 else "natural"
        overall_vocal_quality = {
            "avg_hnr_db": round(avg_hnr, 2), "hnr_classification": hnr_classification,
            "jitter_local_pct": round(jitter, 3), "shimmer_local_pct": round(shimmer, 3),
            "voice_quality": voice_quality, "formant_tracks_available": True,
            "hnr_calibrated": hnr_calibrated,
            "jitter_shimmer_calibrated": perturbation_calibrated,
            "note": "HNR/jitter/shimmer are uncalibrated when they remain zero across a whole track; prefer harmonic_ratio, pitch_bends, and vocal_speed_patterns in that case."
            if not (hnr_calibrated and perturbation_calibrated) else None,
        }
    else:
        overall_vocal_quality = {
            "formant_tracks_available": False,
            "note": "parselmouth not installed — install praat-parselmouth for formants, HNR, jitter, shimmer",
        }

    output = {
        "audio_info": {
            "file": args.audio, "duration_seconds": round(duration, 1), "sample_rate": sr,
            "pitch_backend": "parselmouth_praat" if HAS_PARSELMOUTH else "librosa_pyin",
            "sections_total": len(emotion_sections),
            "sections_method": "fixed" if args.sections else "auto_detected",
        },
        "harmonic_percussive": {
            "harmonic_ratio": round(harmonic_ratio, 3),
            "percussive_ratio": round(percussive_ratio, 3),
            "classification": hpss_classification,
        },
        "loudness_profile": loudness_data,
        "chord_progression": chords_data,
        "song_structure": structure_data,
        "vocal_quality": overall_vocal_quality,
        "emotion_sections": emotion_sections,
        "emotion_profile": emotion_profile,
        "vocal_speed_patterns": vocal_speed,
        "pitch_bends": pitch_bends[:20],
        "silence_gaps": silence_gaps,
        "music_generation_hints": music_hints,
    }

    if cached_or_compute:
        cached = cached_or_compute(args.audio, 'vocal_emotion_full', lambda: output)
        if cached.get('_cache') == 'hit':
            print("(loaded from cache)", file=sys.stderr)
        output = cached

    return output


def _cli_output(result, output_path):
    """Helper: serialize result for the CLI case (main without return_dict)."""
    json_out = json.dumps(result, indent=2, ensure_ascii=False)
    if output_path:
        with open(output_path, 'w') as f:
            f.write(json_out)
        print(f"Written: {output_path}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
