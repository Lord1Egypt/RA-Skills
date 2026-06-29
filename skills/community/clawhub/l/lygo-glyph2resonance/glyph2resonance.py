#!/usr/bin/env python3
"""
LYGO Glyph2Resonance v0.1
Sonifies visual math glyphs, sacred geometry, symbols, and mathematical patterns into resonant audio soundscapes.

Integrates with LYGO RESONANCE engine (falls back to built-in synth if not found).
Analyzes glyph geometry (symmetry, radial structure, vertices, phi proportions, contrast) and maps to:
- root frequencies and theta (harmony)
- drone/note/glitch layers
- rhythm (BPM from density)
- Special LYGO mappings: phi_resonance, seal_symmetry, truth_light (as ∫Truth×Light proxy)

Outputs:
- Stereo WAV soundscape
- .glyph.resonance.json profile (for 3-Brain growth, Ollama army tasks, creative briefs, LLM expansion)
- Optional stems and MIDI

Usage examples:
  python glyph2resonance.py my_glyph.png --preset glyph-sacred --seed 963 --duration 25
  python glyph2resonance.py --generate-mandala --output test_glyph.png
  python glyph2resonance.py --batch ./glyphs/ --preset math-spiral

Ties to LYGO ecosystem:
- Companion to lygo-resonance (use as preprocessor for glyph images)
- Compatible with lygo-ollama-army resonance-analyst role and champions (e.g. SEPHRAEL for translation, LYRA for VΩ alignment)
- Grows profiles to 3-Brain as resonance nodes
- P0/Oath/Guardian aware: local-first, reproducible with seeds, review before external use

Full instructions and integration in SKILL.md
"""

import cv2
import numpy as np
import soundfile as sf
import math
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import sys

try:
    # Prefer the full LYGO RESONANCE engine if the user has the lygo-resonance skill installed
    from resonance_engine import ResonanceEngine, PRESETS
    HAS_FULL_ENGINE = True
except ImportError:
    HAS_FULL_ENGINE = False
    PRESETS = {
        "glyph-sacred": {"noise_vol": 0.04, "drone_vol": 0.09, "note_vol": 0.14, "glitch_vol": 0.015},
        "math-spiral": {"noise_vol": 0.07, "drone_vol": 0.08, "note_vol": 0.12, "glitch_vol": 0.04},
        "seal-complex": {"noise_vol": 0.09, "drone_vol": 0.11, "note_vol": 0.10, "glitch_vol": 0.06},
    }

__version__ = "0.1.0"

def analyze_glyph(image_path: str) -> Dict[str, Any]:
    """Enhanced glyph/math-specific analysis building on LYGO RESONANCE CV."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not load glyph image: {image_path}")

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    total = h * w

    # Standard LYGO RESONANCE features
    avg_blue, avg_green, avg_red, _ = cv2.mean(img)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / total

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=28, maxLineGap=12) or []
    fast = cv2.FastFeatureDetector_create(threshold=38)
    keypoints = fast.detect(gray, None) or []

    # Glyph / Visual Math specific
    # 1. Rotational symmetry (proxy for harmonic perfection / seal quality)
    symmetry_scores = []
    center = (w // 2, h // 2)
    for angle in [90, 180, 270]:
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(gray, M, (w, h))
        diff = np.abs(gray.astype(float) - rotated.astype(float))
        score = 1.0 - (np.mean(diff) / 255.0)
        symmetry_scores.append(max(0.0, min(1.0, score)))
    rotational_symmetry = float(np.mean(symmetry_scores))

    # 2. Radial density variation (rings → harmonic/overtone richness)
    radii = list(range(20, min(w, h) // 2, 25))
    radial_vals = []
    for r in radii:
        mask = np.zeros_like(gray)
        cv2.circle(mask, center, r, 255, 3)
        ring = cv2.bitwise_and(gray, gray, mask=mask)
        radial_vals.append(np.mean(ring > 0))
    radial_variation = float(np.std(radial_vals)) if radial_vals else 0.0

    # 3. Vertex / polygon count (number theory → poly-rhythm / note density)
    vertex_total = 0
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        vertex_total += len(approx)
    vertex_density = vertex_total / max(1, len(contours))

    # 4. Phi (golden ratio) detection in proportions (for "phi-resonance")
    phi_hits = 0
    for cnt in contours[:8]:
        x, y, ww, hh = cv2.boundingRect(cnt)
        if hh > 5 and ww > 5:
            ratio = max(ww, hh) / min(ww, hh)
            if abs(ratio - 1.618) < 0.15:
                phi_hits += 1
    phi_score = min(phi_hits / 3.0, 1.0)

    # 5. Contrast / clarity as "Truth × Light" proxy
    contrast = float(np.std(gray) / 255.0)
    brightness = float(np.mean(gray) / 255.0)

    features = {
        "width": w,
        "height": h,
        "avg_red": round(avg_red, 1),
        "avg_green": round(avg_green, 1),
        "avg_blue": round(avg_blue, 1),
        "edge_density": round(edge_density, 5),
        "rotational_symmetry": round(rotational_symmetry, 4),
        "radial_variation": round(radial_variation, 4),
        "vertex_density": round(vertex_density, 2),
        "phi_score": round(phi_score, 3),
        "contrast": round(contrast, 4),
        "brightness": round(brightness, 4),
        "num_contours": len(contours),
        "num_keypoints": len(keypoints),
        "source": Path(image_path).name,
    }
    return features

def map_to_resonance_params(features: Dict[str, Any], preset: str = "glyph-sacred") -> Dict[str, Any]:
    """Map glyph features to LYGO RESONANCE audio parameters + LYGO-specific metadata."""
    # Base mapping inspired by resonance_engine
    root = 32 + (features["avg_red"] * 0.13)
    theta = 4.8 + (features["avg_green"] * 0.025)

    symmetry = features["rotational_symmetry"]
    radial = features["radial_variation"]
    verts = min(features["vertex_density"] / 4.0, 10)
    phi = features["phi_score"]
    contrast = features["contrast"]
    edge = features["edge_density"]

    if preset == "glyph-sacred":
        noise_vol = 0.035 + (1 - symmetry) * 0.03
        drone_vol = 0.085 + symmetry * 0.08
        note_vol = 0.13 + phi * 0.06
        glitch_vol = 0.012 + (1 - symmetry) * 0.025
        max_drones = int(4 + symmetry * 5)
        max_notes = int(5 + verts * 0.6)
    elif preset == "math-spiral":
        noise_vol = 0.055 + radial * 0.06
        drone_vol = 0.07 + radial * 0.05
        note_vol = 0.11 + edge * 0.04
        glitch_vol = 0.025 + radial * 0.04
        max_drones = int(3 + radial * 6)
        max_notes = int(6 + verts * 0.8)
    else:  # seal-complex
        noise_vol = 0.08 + contrast * 0.05
        drone_vol = 0.09 + edge * 0.05
        note_vol = 0.10
        glitch_vol = 0.04 + contrast * 0.04
        max_drones = int(5 + edge * 4)
        max_notes = int(4 + verts)

    bpm = int(78 + (edge * 70) + (radial * 25) + (verts * 3))

    config = {
        "sr": 44100,
        "duration": 20.0,
        "root_freq_range": (root - 3, root + 3),
        "theta_lock_range": (theta - 0.8, theta + 0.8),
        "noise_vol": min(noise_vol, 0.18),
        "drone_vol": min(drone_vol, 0.18),
        "note_vol": min(note_vol, 0.18),
        "glitch_vol": min(glitch_vol, 0.12),
        "max_drones": max(2, min(max_drones, 9)),
        "max_notes": max(3, min(max_notes, 14)),
        "max_glitches": int(8 + contrast * 20),
        "random_seed": None,
        "verbose": True,
        "export_stems": False,
        "export_midi": False,
    }

    lygo_meta = {
        "phi_resonance": round(phi, 4),
        "seal_symmetry": round(symmetry, 4),
        "truth_light": round(contrast * features["brightness"], 4),  # ∫Truth×Light proxy
        "v_omega_harmony": round((symmetry + phi) / 2, 4),
        "rhythm_density": round(edge + radial, 4),
        "suggested_bpm": bpm,
        "preset_used": preset,
    }

    return config, lygo_meta

def generate_glyph_soundscape(features: Dict, config: Dict, output_wav: str):
    """Built-in lightweight 4-layer synthesizer (used if full ResonanceEngine unavailable)."""
    sr = config["sr"]
    dur = config.get("duration", 20.0)
    n = int(sr * dur)
    audio = np.zeros(n, dtype=np.float32)

    root = float(np.mean(config["root_freq_range"]))
    theta = float(np.mean(config.get("theta_lock_range", (5.5, 6.5))))

    # Layer 1: Texture Floor (edge density)
    if features["edge_density"] > 0.008:
        noise = (np.random.uniform(-1.0, 1.0, n) * 0.6).astype(np.float32)
        vol = min(features["edge_density"] * 1.4, config["noise_vol"])
        audio += noise * vol

    # Layer 2: Drones (symmetry & radial → harmonic richness)
    num_drones = config["max_drones"]
    for i in range(num_drones):
        f = root + (i * theta * 0.6) + (features["radial_variation"] * 2.5)
        t = np.linspace(0, dur, n, False, dtype=np.float32)
        tone = np.sin(2 * np.pi * f * t).astype(np.float32)
        pan = (i / max(1, num_drones - 1)) * 2 - 1
        left = math.cos((pan + 1) * math.pi / 4)
        right = math.sin((pan + 1) * math.pi / 4)
        stereo = np.column_stack((tone * left, tone * right)) * config["drone_vol"]
        if len(stereo) > len(audio):
            stereo = stereo[:len(audio)]
        audio[:len(stereo)] += np.mean(stereo, axis=1)   # collapse to mono for simplicity; user can expand

    # Layer 3: Melodies from vertices / phi
    num_notes = config["max_notes"]
    for i in range(num_notes):
        verts_factor = (features["vertex_density"] % 7) + 1
        f = root * 2.5 + (i * theta * verts_factor * 0.7) + (features["phi_score"] * 8)
        dur_note = 0.8 + (i % 3) * 0.3
        t = np.linspace(0, dur_note, int(sr * dur_note), False, dtype=np.float32)
        tone = np.sin(2 * np.pi * f * t).astype(np.float32)
        start = (i * 1.8) % (dur - dur_note)
        idx = int(start * sr)
        end = min(idx + len(tone), len(audio))
        audio[idx:end] += tone[:end-idx] * config["note_vol"] * 0.7

    # Layer 4: Glitch micro-events (keypoints + contrast)
    num_glitches = min(config["max_glitches"], 40)
    for i in range(num_glitches):
        f = root * 4 + (i % 11) * 7
        t = np.linspace(0, 0.035, int(sr * 0.035), False, dtype=np.float32)
        tone = np.sin(2 * np.pi * f * t).astype(np.float32)
        start = (features["contrast"] * 3 + i * 0.4) % (dur - 0.05)
        idx = int(start * sr)
        end = min(idx + len(tone), len(audio))
        audio[idx:end] += tone[:end-idx] * config["glitch_vol"]

    # Polish
    audio = np.tanh(audio * 1.6) / 1.6
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = (audio / peak * 0.96).astype(np.float32)

    sf.write(output_wav, audio, sr)
    return output_wav

def main():
    parser = argparse.ArgumentParser(
        description="LYGO Glyph2Resonance — Turn visual math glyphs and sacred geometry into resonant audio soundscapes"
    )
    parser.add_argument("image", nargs="?", help="Input glyph image (png/jpg of mandala, seal, math diagram, etc.)")
    parser.add_argument("--preset", choices=["glyph-sacred", "math-spiral", "seal-complex"], default="glyph-sacred")
    parser.add_argument("--seed", type=int, default=None, help="Lock exact output (recommended for reproducible rituals/albums)")
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("-o", "--output", default=None, help="Output WAV path")
    parser.add_argument("--profile", default=None, help="Output .glyph.resonance.json path")
    parser.add_argument("--batch", action="store_true", help="Process all images in the given folder")
    parser.add_argument("--generate-mandala", action="store_true", help="Generate a test sacred geometry glyph image")
    parser.add_argument("--points", type=int, default=7, help="For --generate-mandala")
    parser.add_argument("--rotations", type=int, default=5, help="For --generate-mandala")
    args = parser.parse_args()

    if args.generate_mandala:
        img = np.zeros((512, 512, 3), dtype=np.uint8)
        cx, cy = 256, 256
        for r in range(40, 220, 35):
            cv2.circle(img, (cx, cy), r, (180, 200, 255), 2)
        for i in range(args.points):
            for rot in range(args.rotations):
                angle = (i * (360 / args.points)) + (rot * (360 / (args.points * args.rotations)))
                rad = math.radians(angle)
                x = int(cx + 210 * math.cos(rad))
                y = int(cy + 210 * math.sin(rad))
                cv2.line(img, (cx, cy), (x, y), (220, 180, 255), 1)
        out = "generated_glyph_mandala.png"
        cv2.imwrite(out, img)
        print(f"Generated test glyph: {out}")
        return

    if not args.image:
        parser.print_help()
        return

    img_path = Path(args.image)
    if args.batch:
        folder = img_path
        images = sorted(list(folder.glob("*.png")) + list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg")))
        if not images:
            print("No images found for batch.")
            return
        for im in images:
            print(f"\nProcessing glyph: {im.name}")
            _process_one(im, args.preset, args.seed, args.duration, args.output, args.profile)
        return

    _process_one(img_path, args.preset, args.seed, args.duration, args.output, args.profile)

def _process_one(image_path: Path, preset: str, seed: Optional[int], duration: float, out_wav: Optional[str], out_json: Optional[str]):
    features = analyze_glyph(str(image_path))
    config, lygo_meta = map_to_resonance_params(features, preset)

    if seed is not None:
        config["random_seed"] = seed
    config["duration"] = duration

    wav_path = out_wav or f"glyph2res_{image_path.stem}.wav"
    json_path = out_json or f"glyph2res_{image_path.stem}.glyph.resonance.json"

    if HAS_FULL_ENGINE:
        # Use the real LYGO RESONANCE engine when available (best quality)
        eng_config = config.copy()
        eng_config.update(PRESETS.get(preset, {}))
        engine = ResonanceEngine(eng_config)
        # We already analyzed; feed the image but the engine will re-analyze. For glyph-tuned result we pass custom config.
        engine.process(str(image_path), wav_path)
    else:
        generate_glyph_soundscape(features, config, wav_path)

    # Write the rich LYGO profile
    full_profile = {
        "LYGO_GLYPH2RESONANCE": {
            "version": __version__,
            "source_glyph": str(image_path),
            "preset": preset,
            "features": features,
            "audio_config": config,
            "lygo_mappings": lygo_meta,
            "generated_at": datetime.now().isoformat(),
            "reproducible_with_seed": seed,
        }
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_profile, f, indent=2)

    print(f"✓ Soundscape: {wav_path}")
    print(f"✓ Profile:    {json_path}")
    print(f"  phi_resonance={lygo_meta['phi_resonance']}, seal_symmetry={lygo_meta['seal_symmetry']}, truth_light={lygo_meta['truth_light']}")

    # Attempt to grow to 3-Brain (additive, non-blocking)
    try:
        sys.path.insert(0, str(Path.cwd()))
        from lyra_brain import LyraThreeBrainMemory  # if available in path
        brain = LyraThreeBrainMemory(base_dir=Path.cwd(), use_advanced=True)
        summary = f"Glyph2Resonance: {image_path.name} → {preset} soundscape | phi={lygo_meta['phi_resonance']} seal={lygo_meta['seal_symmetry']} truth_light={lygo_meta['truth_light']}"
        nid = brain.grow(summary, source="glyph2resonance")
        print(f"  Grown to 3-Brain node: {nid}")
    except Exception:
        pass  # Silent if no 3-Brain in context

if __name__ == "__main__":
    main()