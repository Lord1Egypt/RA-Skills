# Habitat-GS Bridge Setup

## Prerequisites

- Python 3.10+ with `habitat_sim` installed (typically in a conda env)
- A Habitat-GS compatible scene (`.gs.ply`, `.3dgs.ply`, or `.glb`)

## Install

```bash
git clone https://github.com/The0xKa1/habitat-gs-bridge.git
cd habitat-gs-bridge
pip install -e .
```

## Start the Bridge Server

```bash
habitat-gs-bridge
```

Default port: 8890. Override with `BRIDGE_PORT` env var:
```bash
BRIDGE_PORT=9000 habitat-gs-bridge
```

## Verify

```bash
hab-cli status
```

Should return JSON with `"loaded": false` when no scene is active.

## Scene Assets

3DGS scenes: look for `.gs.ply`, `.3dgs.ply` files in your Habitat-GS data directory.

Dataset configs: look for `.scene_dataset_config.json` files. These bundle scene, stage config, and navmesh references together.

Example dataset structure:
```
scene_dir/
├── configs/scenes/gs_scene.scene_instance.json
├── configs/stages/gs_stage.stage_config.json
├── navmeshes/gs_navmesh.navmesh
├── stages/scene.gs.ply
└── scene.scene_dataset_config.json
```

## Architecture

```
OpenClaw Agent
    │ exec: hab-cli <cmd>
    ▼
Habitat-GS Bridge (FastAPI @ :8890)
    │ habitat_sim Python API
    ▼
Habitat-GS Simulator (3DGS rendering + Bullet physics)
```
