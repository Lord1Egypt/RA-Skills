---
name: desktop-pet
description: Deploy a pixel-art desktop pet (桌面宠物) with four explorable scenes, care mechanics, and walk animations. Use when user asks to create a desktop pet, virtual pet, pixel pet, tamagotchi-like app, or says "桌面宠物", "桌宠", "desktop pet". Requires Python 3.11+ with Tkinter and Pillow.
---

# Desktop Pet — 南波万の小家园

A pixel-art desktop pet built with Python + Tkinter. Features a mini floating character on the desktop and a full home-garden mode with four explorable scenes.

## Features

- **Mini mode**: Transparent floating pixel character with walk animation (128px, white oval background)
- **Garden mode**: 850×560 window with four scenes connected by doorways
  - 🏠 Indoor (1F) — cozy room with furniture
  - 🪜 Upstairs (2F) — mirrored warm-tone layout
  - 🌿 Outdoor — front yard with fence
  - 🌳 Forest — large woodland area
- **Care system**: Hunger / Mood / Cleanliness / Health with decay and recovery
- **Controls**: Arrow keys or WASD to walk, E to interact with doorways, T for debug mode
- **Right-click menu**: Feed 🍔 / Bathe 🛁 / Play 🎮 / Medicine 💊

## Deployment

1. Copy `scripts/desktop_pet.py` to target directory
2. Copy all files from `assets/` into an `assets/` subdirectory next to `desktop_pet.py`
3. Run:

```bash
cd <target-dir>
pip install Pillow
TK_SILENCE_DEPRECATION=1 python3 desktop_pet.py
```

### File structure after deployment

```
target-dir/
├── desktop_pet.py
└── assets/
    ├── room_bg.png        # Indoor scene (1F)
    ├── upstairs_bg.png    # Upstairs scene (2F, mirrored + warm)
    ├── exterior_bg.png    # Outdoor scene
    ├── forest_bg.png      # Forest scene
    ├── walk_right.gif     # Character walk right (8 frames, 32×32)
    └── walk_left.gif      # Character walk left (8 frames, 32×32)
```

### macOS notes

- Uses `overrideredirect(True)` + `systemTransparent` for floating mini window
- PhotoImage doesn't render on transparent canvas → white oval workaround
- Set `TK_SILENCE_DEPRECATION=1` to suppress Tk warnings

## Scene transitions

| From | Trigger | To |
|---|---|---|
| Indoor 1F | Walk to staircase (top-left) + E | Upstairs 2F |
| Indoor 1F | Walk to carpet (bottom-right) + E | Outdoor |
| Upstairs 2F | Walk to staircase (top-right) + E | Indoor 1F |
| Outdoor | Walk to left edge + E | Forest |
| Outdoor | Walk to door + E | Indoor 1F |
| Forest | Walk to right edge + E | Outdoor |

## Customization

- **Backgrounds**: Replace PNG files in `assets/` (850×526px recommended)
- **Character**: Replace GIF files (32×32 per frame, 8 frames)
- **Care decay rate**: Search `frame%600` in code (higher = slower decay)
- **Collision walls**: Edit `_INDOOR_WALLS` / `_OUTDOOR_WALLS` arrays
- **Window sizes**: `W_M, H_M` for mini mode, `W_G, H_G` for garden mode

## Credits

- Character sprites: [Cozy People](https://pixelfight.itch.io/) (free pixel art)
- Background tiles: [CraftPix](https://craftpix.net/freebies/) (free top-down pixel art)
