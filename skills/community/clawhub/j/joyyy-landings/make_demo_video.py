#!/usr/bin/env python3
"""
Build a ~30s demo video from screenshots for ClawHub.
Run after capture_screenshots.py. Output: demo_30s.mp4

  cd skills/joyyy-landings && pip install -r requirements-screenshots.txt
  python3 make_demo_video.py
"""

import sys
from pathlib import Path

try:
    from moviepy.editor import ImageClip, concatenate_videoclips
    from moviepy.video.fx.all import fadein, fadeout
except ImportError:
    print("❌ pip install moviepy")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = SCRIPT_DIR / "screenshots"
OUTPUT_PATH = SCRIPT_DIR / "demo_30s.mp4"

# Order and duration (seconds) per slide
SLIDES = [
    "01_landing.png",
    "02_crash_engine.png",
    "03_crash_probability_explorer.png",
    "04_mmo_map.png",
    "05_dice_room.png",
]
SEC_PER_SLIDE = 6
FADE_DURATION = 1.0


def main():
    if not SCREENSHOTS_DIR.exists():
        print(f"❌ Run capture_screenshots.py first. Expected: {SCREENSHOTS_DIR}")
        sys.exit(1)

    clips = []
    for name in SLIDES:
        path = SCREENSHOTS_DIR / name
        if not path.exists():
            print(f"⚠ Skip (missing): {name}")
            continue
        clip = ImageClip(str(path), duration=SEC_PER_SLIDE)
        clip = fadein(clip, FADE_DURATION)
        clip = fadeout(clip, FADE_DURATION)
        clips.append(clip)

    if not clips:
        print("❌ No images found.")
        sys.exit(1)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        str(OUTPUT_PATH),
        fps=24,
        codec="libx264",
        audio=False,
        logger=None,
    )
    print(f"✅ {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
