#!/usr/bin/env python3
"""
LYGO Profile Generator v0.3
Image → Musical DNA + Lyrical Framework

Extracts visual mathematics from an image and translates it into
structured creative direction for music production and AI-assisted lyric writing.
Full source from https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
"""

import cv2
import numpy as np
import json
import math
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

__version__ = "0.3.0"


class LYGOProfileGenerator:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Extract rich mathematical features from the image."""
        img = cv2.imread(str(image_path))
        if img is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        h, w, _ = img.shape
        total_pixels = h * w

        # === Color Analysis (HSV) ===
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        avg_hue = float(np.mean(hsv[:, :, 0]) * 2)          # 0-360
        avg_sat = float(np.mean(hsv[:, :, 1]) / 255.0)
        avg_val = float(np.mean(hsv[:, :, 2]) / 255.0)
        sat_std = float(np.std(hsv[:, :, 1]) / 255.0)       # colorfulness

        # === Luminance & Contrast ===
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray) / 255.0)
        contrast = float(np.std(gray) / 255.0)

        # === Structural Analysis ===
        edges = cv2.Canny(gray, 50, 150)
        edge_density = float(np.count_nonzero(edges) / total_pixels)

        # Contours for structural complexity
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        structure_index = min(len(contours) / 80.0, 1.0)

        # Micro-chaos (FAST corners)
        fast = cv2.FastFeatureDetector_create(threshold=38)
        keypoints = fast.detect(gray, None)
        chaos_index = len(keypoints)

        features = {
            "source_image": str(Path(image_path).name),
            "dimensions": {"width": w, "height": h},
            "color": {
                "average_hue": round(avg_hue, 2),
                "average_saturation": round(avg_sat, 4),
                "average_brightness": round(brightness, 4),
                "colorfulness": round(sat_std, 4),
            },
            "structure": {
                "edge_density": round(edge_density, 4),
                "contrast": round(contrast, 4),
                "structure_index": round(structure_index, 4),
                "chaos_keypoints": chaos_index,
            },
        }
        return features

    def _get_musical_key(self, hue: float, brightness: float) -> str:
        keys = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
        key_index = int(hue / 30) % 12
        mode = "Minor" if brightness < 0.48 else "Major"
        return f"{keys[key_index]} {mode}"

    def _calculate_bpm(self, edge_density: float, chaos: int, brightness: float) -> int:
        base = 82 + (edge_density * 920)
        chaos_mod = min(chaos / 1800, 0.6)
        brightness_mod = (brightness - 0.5) * 12
        bpm = int(base + (chaos_mod * 25) + brightness_mod)
        return max(78, min(178, bpm))

    def _generate_genre_texture(self, features: Dict) -> Dict[str, str]:
        e = features["structure"]["edge_density"]
        c = features["structure"]["chaos_keypoints"]
        b = features["color"]["average_brightness"]
        contrast = features["structure"]["contrast"]

        if c > 650 and b < 0.38:
            genre = "Industrial Dubstep / Dark Phonk"
            texture = "Heavy distortion, aggressive stutters, deep sub-bass, metallic textures"
            energy = "High-aggression"
        elif e > 0.065 and contrast > 0.18:
            genre = "Emo Rap / Modern Trap"
            texture = "Crisp hi-hats, melancholic melodies, heavy 808s, emotional vocal layers"
            energy = "Mid-High emotional"
        elif c > 420 and b > 0.55:
            genre = "Experimental / Glitch Hop"
            texture = "Glitchy percussion, chopped vocals, atmospheric synths, rhythmic complexity"
            energy = "High chaotic"
        elif e < 0.035 and b > 0.6:
            genre = "West Coast G-Funk / Smooth Instrumental"
            texture = "Laid-back grooves, warm analog bass, melodic leads, nostalgic atmosphere"
            energy = "Mid relaxed"
        else:
            genre = "Dark Alternative / Cinematic Rap"
            texture = "Atmospheric pads, punchy drums, moody synths, introspective energy"
            energy = "Mid cinematic"

        return {"genre": genre, "texture": texture, "energy": energy}

    def translate_to_lygo(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Convert visual features into musical and lyrical creative direction."""
        hue = features["color"]["average_hue"]
        brightness = features["color"]["average_brightness"]
        edge_density = features["structure"]["edge_density"]
        chaos = features["structure"]["chaos_keypoints"]
        contrast = features["structure"]["contrast"]

        musical_key = self._get_musical_key(hue, brightness)
        bpm = self._calculate_bpm(edge_density, chaos, brightness)
        genre_data = self._generate_genre_texture(features)

        # === Lyrical Theme Engine ===
        if brightness < 0.42 and edge_density > 0.055:
            core_theme = "Survival, betrayal, lone wolf resilience, moving in silence"
            lyric_prompt = (
                "Write raw, introspective lyrics about being the last one standing after betrayal. "
                "Focus on trust issues, a very small circle of ride-or-die people, and the cold satisfaction of outlasting everyone who counted you out."
            )
            vocal_style = "Raspy melodic rap or gritty sung-rap hybrid"
        elif chaos > 550:
            core_theme = "Breaking chains, system resistance, unchained personal power"
            lyric_prompt = (
                "Write aggressive yet intelligent lyrics about breaking free from systems that tried to define you. "
                "Emphasize resilience, moving in silence, and turning pain into unstoppable momentum."
            )
            vocal_style = "Assertive rap with melodic moments or distorted vocal processing"
        else:
            core_theme = "Observation, loyalty, navigating a cold modern world with quiet edge"
            lyric_prompt = (
                "Write clever, slightly dark observational lyrics with dry humor about modern life, loyalty, "
                "and staying true to your own code while everything around you feels artificial."
            )
            vocal_style = "Deadpan to melodic rap delivery, slightly introspective"

        # === Final Structured Output ===
        lygo_profile = {
            "LYGO_PROFILE": {
                "version": __version__,
                "generated_at": datetime.now().isoformat(),
                "source": features["source_image"],
                "mathematics": features,
                "musical_dna": {
                    "root_key": musical_key,
                    "bpm": bpm,
                    "energy_level": genre_data["energy"],
                    "suggested_genre": genre_data["genre"],
                    "texture_description": genre_data["texture"],
                    "vocal_style": vocal_style,
                },
                "lyrical_framework": {
                    "core_theme": core_theme,
                    "ai_lyric_prompt": lyric_prompt,
                },
                "ai_music_prompt": (
                    f"Create a {genre_data['genre']} track at {bpm} BPM in the key of {musical_key}. "
                    f"The overall energy should feel {genre_data['energy'].lower()}. "
                    f"Sound design and texture: {genre_data['texture']}. "
                    f"Lyrical themes should center around {core_theme}."
                ),
                "production_notes": (
                    f"High contrast and structural complexity suggest strong dynamic range. "
                    f"Consider heavy low-end support and atmospheric layers to match the visual weight."
                ),
            }
        }
        return lygo_profile

    def generate(self, image_path: str, output_json: str = "lygo_profile.json", create_brief: bool = False):
        self._log(f"\n╔════════════════════════════════════════════╗")
        self._log(f"║           LYGO Profile Generator v{__version__}      ║")
        self._log(f"║     Image → Musical DNA + Lyrical Framework║")
        self._log(f"╚════════════════════════════════════════════╝\n")

        features = self.analyze_image(image_path)
        profile = self.translate_to_lygo(features)

        # Save JSON
        with open(output_json, "w") as f:
            json.dump(profile, f, indent=2)

        self._log(json.dumps(profile, indent=2))
        self._log(f"\n[+] LYGO Profile saved → {output_json}")

        if create_brief:
            brief_path = Path(output_json).with_suffix(".brief.txt")
            self._create_creative_brief(profile, brief_path)
            self._log(f"[+] Creative Brief saved → {brief_path}")

    def _create_creative_brief(self, profile: Dict, path: Path):
        data = profile["LYGO_PROFILE"]
        brief = f"""LYGO CREATIVE BRIEF
Generated: {data['generated_at']}
Source Image: {data['source']}

══════════════════════════════════════════════
MUSICAL DNA
══════════════════════════════════════════════
Key: {data['musical_dna']['root_key']}
BPM: {data['musical_dna']['bpm']}
Energy: {data['musical_dna']['energy_level']}
Genre Direction: {data['musical_dna']['suggested_genre']}

Texture & Vibe:
{data['musical_dna']['texture_description']}

Vocal Approach: {data['musical_dna']['vocal_style']}

══════════════════════════════════════════════
LYRICAL DIRECTION
══════════════════════════════════════════════
Core Theme: {data['lyrical_framework']['core_theme']}

AI Prompt:
{data['lyrical_framework']['ai_lyric_prompt']}

══════════════════════════════════════════════
FULL AI MUSIC PROMPT (Copy-Paste Ready)
══════════════════════════════════════════════
{data['ai_music_prompt']}

Production Notes:
{data['production_notes']}
"""
        path.write_text(brief, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(
        description="LYGO Profile Generator — Turn any image into structured musical + lyrical creative direction"
    )
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("-o", "--output", default="lygo_profile.json", help="Output JSON file")
    parser.add_argument("--brief", action="store_true", help="Also generate a human-readable .brief.txt file")
    parser.add_argument("--batch", action="store_true", help="Process all images in a folder")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    generator = LYGOProfileGenerator(verbose=not args.quiet)

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
            out_json = f"lygo_profile_{img.stem}.json"
            generator.generate(str(img), out_json, create_brief=args.brief)
        return

    generator.generate(args.image, args.output, create_brief=args.brief)


if __name__ == "__main__":
    main()