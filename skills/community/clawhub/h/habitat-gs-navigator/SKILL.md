---
name: habitat-gs-navigator
description: "Navigate and interact with photo-realistic 3DGS environments via the Habitat-GS Bridge. Use when: user asks to explore a 3D scene, perform embodied navigation, do Embodied QA tasks, run navigation episodes in Habitat-GS, or interact with the Habitat-GS simulator. Triggers on: 'navigate', 'habitat', '3DGS scene', 'embodied', 'load scene', 'explore room', 'EQA'. Requires the Habitat-GS Bridge server (pip install habitat-gs-bridge) running at localhost:8890."
---

# Habitat-GS Navigator

Control an embodied agent inside photo-realistic 3D Gaussian Splatting environments through the Habitat-GS Bridge.

## Installation


```bash
git clone https://github.com/The0xKa1/habitat-gs-bridge.git
cd habitat-gs-bridge
pip install -e .
```

This provides two commands:
- `hab-cli` — CLI for controlling the simulator (used by this skill)
- `habitat-gs-bridge` — starts the bridge server

For full API details, read [references/api-reference.md](references/api-reference.md).
For setup instructions, read [references/setup.md](references/setup.md).

## Quick Workflow

```bash
# 1. Start the bridge server (in a separate terminal)
habitat-gs-bridge

# 2. Verify it's running
hab-cli status

# 3. Load scene (by scene-id + dataset, or by direct path)
hab-cli load_scene --scene-id gs_scene --dataset /path/to/config.json
hab-cli load_scene --scene /path/to/scene.gs.ply

# 4. Reset episode with start/goal
hab-cli reset --start "5.18,-3.57,-2.86" --goal "-3.62,-3.61,3.18"

# 5. Navigate: observe → decide → act → repeat
hab-cli step move_forward
hab-cli step turn_left
hab-cli step turn_right
hab-cli step stop          # when goal reached

# 6. Utilities
hab-cli observe             # current observation without stepping
hab-cli path --goal "x,y,z" # shortest-path info
hab-cli random_point        # sample navigable point
```

## Navigation Loop

1. **Observe**: read `agent_state.position`, `distance_to_goal`, `collided`
2. **Decide**: use the philosophical-three-questions skill (Goal/State/Future tree)
3. **Act**: pick one of `move_forward`, `turn_left`, `turn_right`, `stop`
4. **Check**: verify distance decreased; if collided, turn to find open path
5. **Repeat** until `done` is true or `distance_to_goal` < `goal_radius`

## Decision Heuristics

- `collided` after `move_forward` → turn (try left, then right) to find open path
- `distance_to_goal` decreasing → keep current heading
- `distance_to_goal` stagnant/increasing → change direction, use `hab-cli path` to check geodesic distance
- `distance_to_goal` < 0.5m → call `stop`
- Near `max_steps` → consider `stop` if reasonably close

## Configuration

The bridge server URL defaults to `http://127.0.0.1:8890`. Override with:
- `--url` flag: `hab-cli --url http://host:port status`
- Environment variable: `export HABITAT_GS_BRIDGE_URL=http://host:port`

## Experience Logging

After each episode, record to `~/.openclaw/workspace/memory/YYYY-MM-DD.md`:

```markdown
## [NAV] Episode <id> in <scene>
- Result: success/fail (N steps, optimal: M steps)
- Key decisions: <turning points>
- Lesson: <what to do differently>
```

After 5+ episodes, review memory and extract recurring patterns into new skills or update this skill's heuristics.
