#!/usr/bin/env python3
"""
LYGO Resonance Engine v0.3
Image → Living Stereo Soundscape
A spectral translator that gives voice to the hidden geometry, texture, and color of any image.
Full source from https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
"""

import cv2
import numpy as np
import soundfile as sf
import math
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import mido
from mido import MidiFile, MidiTrack, Message

__version__ = "0.3.0"

# Artistic Presets (from the site)
PRESETS = {
    "raw": {},
    "ambient": {
        "noise_vol": 0.055,
        "drone_vol": 0.095,
        "note_vol": 0.11,
        "glitch_vol": 0.012,
        "drone_attack": 5.5,
        "drone_decay": 5.5,
        "note_attack": 0.04,
        "note_decay": 0.35,
        "max_glitches": 10,
        "noise_lowpass_hz": 650,
    },
    "glitch": {
        "noise_vol": 0.16,
        "drone_vol": 0.06,
        "note_vol": 0.09,
        "glitch_vol": 0.07,
        "max_notes": 8,
        "max_glitches": 50,
        "note_decay": 0.10,
        "glitch_decay": 0.008,
        "noise_lowpass_hz": 2800,
    },
    "ethereal": {
        "noise_vol": 0.04,
        "drone_vol": 0.08,
        "note_vol": 0.14,
        "glitch_vol": 0.02,
        "root_freq_range": (35, 95),
        "theta_lock_range": (6, 14),
        "note_attack": 0.06,
        "note_decay": 0.45,
        "noise_lowpass_hz": 450,
    },
    "cinematic": {
        "noise_vol": 0.07,
        "drone_vol": 0.11,
        "note_vol": 0.13,
        "glitch_vol": 0.025,
        "drone_attack": 4.0,
        "drone_decay": 4.5,
        "max_drones": 5,
        "noise_lowpass_hz": 900,
    },
}

class ResonanceEngine:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = {
            "sr": 44100,
            "duration": 15.0,
            "global_fade": 0.7,
            "soft_clip": True,
            "soft_clip_amount": 1.7,
            "max_drones": 6,
            "max_notes": 12,
            "max_glitches": 30,
            "noise_vol": 0.095,
            "drone_vol": 0.075,
            "note_vol": 0.15,
            "glitch_vol": 0.032,
            "root_freq_range": (28, 72),
            "theta_lock_range": (4.5, 11),
            "drone_attack": 3.2,
            "drone_decay": 3.2,
            "note_attack": 0.022,
            "note_decay": 0.20,
            "glitch_attack": 0.003,
            "glitch_decay": 0.011,
            "noise_lowpass_hz": 0,
            "random_seed": None,
            "verbose": True,
            "export_stems": False,
            "export_midi": False,
        }
        if config:
            self.config.update(config)

    def _log(self, msg: str):
        if self.config.get("verbose", True):
            print(msg)

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        img = cv2.imread(str(image_path))
        if img is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        avg_blue, avg_green, avg_red, _ = cv2.mean(img)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (h * w)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=28, maxLineGap=12)
        fast = cv2.FastFeatureDetector_create(threshold=38)
        keypoints = fast.detect(gray, None)

        features = {
            "width": w, "height": h,
            "avg_red": avg_red, "avg_green": avg_green, "avg_blue": avg_blue,
            "edge_density": edge_density,
            "contours": contours,
            "lines": lines if lines is not None else [],
            "keypoints": keypoints,
        }
        return features

    def _generate_tone(self, freq: float, duration: float, wave_type: str = "sine") -> np.ndarray:
        sr = self.config["sr"]
        t = np.linspace(0, duration, int(sr * duration), False)
        if wave_type == "sine":
            return np.sin(freq * t * 2 * np.pi).astype(np.float32)
        elif wave_type == "sawtooth":
            return (2 * (t * freq - np.floor(0.5 + t * freq))).astype(np.float32)
        elif wave_type == "noise":
            return np.random.uniform(-1.0, 1.0, len(t)).astype(np.float32)
        return np.zeros(len(t), dtype=np.float32)

    def _apply_envelope(self, audio: np.ndarray, attack: float, decay: float) -> np.ndarray:
        sr = self.config["sr"]
        a = max(1, int(attack * sr))
        d = max(1, int(decay * sr))
        env = np.ones_like(audio, dtype=np.float32)
        if len(audio) > a + d:
            env[:a] = np.linspace(0, 1, a)
            env[-d:] = np.linspace(1, 0, d)
        return audio * env

    def _stereo_pan(self, mono: np.ndarray, pan: float) -> np.ndarray:
        pan = max(-1.0, min(1.0, pan))
        left = math.cos((pan + 1) * math.pi / 4)
        right = math.sin((pan + 1) * math.pi / 4)
        return np.column_stack((mono * left, mono * right)).astype(np.float32)

    def _fft_lowpass(self, audio: np.ndarray, cutoff_hz: float) -> np.ndarray:
        if cutoff_hz <= 0 or len(audio) < 32:
            return audio
        sr = self.config["sr"]
        n = len(audio)
        fft = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(n, 1.0 / sr)
        fft[freqs > cutoff_hz] = 0
        return np.fft.irfft(fft, n=n).real.astype(np.float32)

    def _soft_limit(self, audio: np.ndarray) -> np.ndarray:
        if self.config["soft_clip"]:
            amt = self.config["soft_clip_amount"]
            return np.tanh(audio * amt) / np.tanh(amt)
        return audio

    def _freq_to_midi(self, freq: float) -> int:
        if freq <= 0:
            return 0
        return max(0, min(127, int(12 * math.log2(freq / 440) + 69)))

    def synthesize(self, features: Dict[str, Any], output_path: str):
        cfg = self.config
        if cfg["random_seed"] is not None:
            np.random.seed(cfg["random_seed"])

        sr = cfg["sr"]
        duration = cfg["duration"]
        audio = np.zeros((int(sr * duration), 2), dtype=np.float32)

        root = np.interp(features["avg_red"], [0, 255], cfg["root_freq_range"])
        theta = np.interp(features["avg_green"], [0, 255], cfg["theta_lock_range"])
        w, h = features["width"], features["height"]

        # Initialize stem collections
        audio_noise = np.zeros((int(sr * duration), 2), dtype=np.float32)
        audio_drone = np.zeros((int(sr * duration), 2), dtype=np.float32)
        audio_melody = np.zeros((int(sr * duration), 2), dtype=np.float32)
        audio_glitch = np.zeros((int(sr * duration), 2), dtype=np.float32)
        melody_events = []

        # Layer 1: Texture Floor
        if features["edge_density"] > 0.007:
            noise = self._generate_tone(0, duration, "noise")
            if cfg["noise_lowpass_hz"] > 0:
                noise = self._fft_lowpass(noise, cfg["noise_lowpass_hz"])
            noise = self._apply_envelope(noise, cfg["drone_attack"], cfg["drone_decay"])
            vol = min(features["edge_density"] * 1.6, cfg["noise_vol"])
            stereo_noise = self._stereo_pan(noise, 0.0) * vol
            audio += stereo_noise
            audio_noise += stereo_noise

        # Layer 2: Drones
        for i, line in enumerate(features["lines"][:cfg["max_drones"]]):
            x1, _, x2, _ = line[0]
            length = math.hypot(x2 - x1, 0)
            detune = (i * 0.7) if cfg["random_seed"] is not None else 0
            freq = root + (max(1, int(length / 48)) * theta * 0.55) + detune
            tone = self._generate_tone(freq, duration, "sawtooth")
            tone = self._apply_envelope(tone, cfg["drone_attack"], cfg["drone_decay"])
            pan = (x1 / w) * 2 - 1
            stereo_drone = self._stereo_pan(tone, pan) * cfg["drone_vol"]
            audio += stereo_drone
            audio_drone += stereo_drone

        # Layer 3: Contours → Melody
        valid = [c for c in features["contours"] if 90 < cv2.contourArea(c) < (w * h * 0.6)]
        valid.sort(key=lambda c: cv2.boundingRect(c)[0])

        for i, cnt in enumerate(valid[:cfg["max_notes"]]):
            area = cv2.contourArea(cnt)
            verts = len(cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True))
            freq = (root * 3.7) + (verts * theta * 1.6)
            dur = min(2.6, 0.22 + (area / 13500))
            tone = self._generate_tone(freq, dur, "sine")
            tone = self._apply_envelope(tone, cfg["note_attack"], cfg["note_decay"])

            M = cv2.moments(cnt)
            cx = int(M["m10"] / M["m00"]) if M["m00"] != 0 else cv2.boundingRect(cnt)[0]
            start = (cx / w) * (duration - dur)
            idx = int(start * sr)
            end = min(idx + len(tone), len(audio))
            pan = (cx / w) * 2 - 1
            stereo_note = self._stereo_pan(tone[:end-idx], pan) * cfg["note_vol"]
            audio[idx:end] += stereo_note
            audio_melody[idx:end] += stereo_note
            melody_events.append((freq, dur, start))

        # Layer 4: Glitch / Micro events
        for i, kp in enumerate(features["keypoints"][:cfg["max_glitches"]]):
            x, y = kp.pt
            freq = root * 13.5 + (y % 85) * 1.4
            tone = self._generate_tone(freq, 0.042, "sine")
            tone = self._apply_envelope(tone, cfg["glitch_attack"], cfg["glitch_decay"])
            start = (y / h) * (duration - 0.05)
            idx = int(start * sr)
            end = min(idx + len(tone), len(audio))
            pan = (x / w) * 2 - 1
            stereo_glitch = self._stereo_pan(tone[:end-idx], pan) * cfg["glitch_vol"]
            audio[idx:end] += stereo_glitch
            audio_glitch[idx:end] += stereo_glitch

        # Final polish
        audio = self._soft_limit(audio)
        fade = int(cfg["global_fade"] * sr)
        if fade > 0 and len(audio) > fade * 2:
            audio[:fade] *= np.linspace(0, 1, fade)[:, None]
            audio[-fade:] *= np.linspace(1, 0, fade)[:, None]

        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.97

        sf.write(output_path, audio, sr)
        self._log(f"✓ Saved: {output_path}  |  Peak: {peak:.3f}")

        # Export Stems
        if cfg.get("export_stems"):
            base = output_path.replace(".wav", "")
            for stem, name in [(audio_noise, "noise"), (audio_drone, "drone"),
                               (audio_melody, "melody"), (audio_glitch, "glitch")]:
                max_val = np.max(np.abs(stem))
                if max_val > 0:
                    stem = stem / max_val * 0.97
                sf.write(f"{base}_{name}.wav", stem, sr)
                self._log(f"✓ Stem saved: {base}_{name}.wav")

        # Export MIDI
        if cfg.get("export_midi") and melody_events:
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)
            ticks_per_beat = 480
            tempo = 120
            tick_offset = 0
            for freq, dur, start in melody_events:
                midi_note = self._freq_to_midi(freq)
                duration_ticks = int(dur * ticks_per_beat * (tempo / 60))
                start_ticks = int(start * ticks_per_beat * (tempo / 60))
                track.append(Message('note_on', note=midi_note, velocity=64, time=start_ticks - tick_offset))
                track.append(Message('note_off', note=midi_note, velocity=64, time=duration_ticks))
                tick_offset = start_ticks + duration_ticks
            mid_path = output_path.replace(".wav", ".mid")
            mid.save(mid_path)
            self._log(f"✓ MIDI saved: {mid_path}")

    def process(self, image_path: str, output_path: str):
        self._log(f"\n╔════════════════════════════════════════════╗")
        self._log(f"║           LYGO Resonance Engine v{__version__}      ║")
        self._log(f"║     Image → Living Stereo Soundscape       ║")
        self._log(f"╚════════════════════════════════════════════╝\n")
        self._log(f"Analyzing: {image_path}")
        features = self.analyze_image(image_path)
        self.synthesize(features, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="LYGO Resonance Engine — Turn any image into a rich stereo soundscape"
    )
    parser.add_argument("image", help="Input image path")
    parser.add_argument("-o", "--output", default=None, help="Output .wav path")
    parser.add_argument("--duration", type=float, default=15.0)
    parser.add_argument("--style", choices=list(PRESETS.keys()), default="cinematic",
                        help="Artistic preset")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--noise-filter", type=float, default=None,
                        help="Lowpass cutoff Hz for noise layer (0 = off)")
    parser.add_argument("--stems", action="store_true", help="Export individual stems (noise, drone, melody, glitch)")
    parser.add_argument("--midi", action="store_true", help="Export MIDI file from melody events")
    parser.add_argument("--batch", action="store_true", help="Process all images in a folder")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    config = {
        "duration": args.duration,
        "random_seed": args.seed,
        "verbose": not args.quiet,
        "export_stems": args.stems,
        "export_midi": args.midi,
    }
    if args.noise_filter is not None:
        config["noise_lowpass_hz"] = args.noise_filter

    preset = PRESETS.get(args.style, {})
    config.update(preset)

    if args.batch:
        folder = Path(args.image)
        if not folder.is_dir():
            print("Error: --batch requires a folder path")
            return
        images = sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.png")) + sorted(folder.glob("*.jpeg"))
        if not images:
            print("No images found in folder")
            return
        for img in images:
            print(f"\nProcessing: {img.name}")
            out_path = f"resonance_{img.stem}.wav"
            engine = ResonanceEngine(config)
            engine.process(str(img), out_path)
        return

    out_path = args.output or f"resonance_{Path(args.image).stem}.wav"
    engine = ResonanceEngine(config)
    engine.process(args.image, out_path)


if __name__ == "__main__":
    main()