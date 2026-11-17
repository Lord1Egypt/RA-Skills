#!/usr/bin/env python3
"""Validate a paper-collage Remotion script manifest and its public assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROLES = {"primary", "secondary", "tertiary", "foreground"}
DIRECTIONS = {"left", "right", "bottom"}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("public_dir", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read manifest: {error}")

    composition = data.get("composition", {})
    width, height, fps = (composition.get(key) for key in ("width", "height", "fps"))
    if not all(isinstance(value, int) and value > 0 for value in (width, height, fps)):
        fail("composition needs positive integer width, height, and fps")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        fail("scenes must be a non-empty list")

    duration = 0
    warnings = []
    for scene_index, scene in enumerate(scenes, 1):
        scene_name = scene.get("id", f"scene-{scene_index}")
        scene_duration = scene.get("durationInFrames")
        if not isinstance(scene_duration, int) or scene_duration <= 0:
            fail(f"{scene_name}: durationInFrames must be a positive integer")
        duration += scene_duration
        asset_paths = [scene.get("background")]
        layers = scene.get("layers")
        if not isinstance(layers, list) or not layers:
            fail(f"{scene_name}: layers must be a non-empty list")
        for layer_index, layer in enumerate(layers, 1):
            for key in ("src", "x", "y", "width", "delay", "z", "role", "from"):
                if key not in layer:
                    fail(f"{scene_name} layer {layer_index}: missing {key}")
            if layer["role"] not in ROLES or layer["from"] not in DIRECTIONS:
                fail(f"{scene_name} layer {layer_index}: invalid role or entrance direction")
            if not all(isinstance(layer[key], (int, float)) for key in ("x", "y", "width", "delay", "z")) or layer["width"] <= 0:
                fail(f"{scene_name} layer {layer_index}: numeric values are invalid")
            if layer["x"] < -layer["width"] or layer["x"] > width or layer["y"] < -height or layer["y"] > height:
                warnings.append(f"{scene_name} layer {layer_index}: final position is outside the frame")
            asset_paths.append(layer["src"])
        for relative_path in asset_paths:
            if not isinstance(relative_path, str):
                fail(f"{scene_name}: background and layer src values must be paths")
            asset = args.public_dir / relative_path
            if not asset.is_file():
                fail(f"{scene_name}: missing asset {asset}")
            if asset.suffix.lower() == ".png":
                with Image.open(asset) as image:
                    if "A" not in image.getbands() and relative_path != scene.get("background"):
                        warnings.append(f"{scene_name}: {relative_path} has no alpha channel")

    print(f"OK: {len(scenes)} scenes, {duration} frames ({duration / fps:.2f}s), {width}x{height}@{fps}")
    for warning in warnings:
        print(f"WARNING: {warning}")


if __name__ == "__main__":
    main()
