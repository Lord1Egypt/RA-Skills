# Architecture

## Goal

Generate custom Aavegotchi 3D renders for arbitrary valid trait combinations using the official Aavegotchi Unity SDK.

## Layers

### 1. Skill interface layer

Files:
- `SKILL.md`
- `scripts/render-custom-gotchi.sh`
- `scripts/render_custom_payload.py`
- `scripts/validate-custom-config.py`

Responsibilities:
- accept natural-language or structured requests
- normalize requests into canonical JSON
- validate field presence and slot values
- choose output paths in `/tmp/openclaw`
- call the Unity worker

### 2. Unity worker layer

Files:
- `scripts/launch-unity-batch.sh`
- Unity project under `unity/GotchiCustomRenderer/`

Responsibilities:
- load the Unity SDK package
- instantiate the Aavegotchi prefab
- create an `Aavegotchi_Data` object
- call `Aavegotchi_Base.UpdateForData(...)`
- wait for addressables and wearables to load
- frame and capture PNGs
- optionally export turntable frames later

### 3. Artifact layer

Output files:
- `custom-gotchi-<slug>-full.png`
- `custom-gotchi-<slug>-headshot.png`
- `custom-gotchi-<slug>-manifest.json`

Artifacts are written to `/tmp/openclaw` so AAi can send them safely.

## Contract between shell and Unity

Input:
- normalized JSON manifest path

Output:
- JSON result written to stdout and mirrored to a manifest file
- full and headshot image paths
- worker metadata such as render duration and Unity version

## Why separate skill

The current `aavegotchi-3d-renderer` depends on Aavegotchi-hosted renderer APIs and canonical onchain data.
This skill owns the full composition path locally through Unity, which is what makes synthetic loadouts possible.
