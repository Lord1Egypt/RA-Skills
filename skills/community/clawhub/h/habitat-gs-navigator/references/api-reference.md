# Habitat-GS Bridge API Reference

## Commands

### status
```bash
hab-cli status
```
Returns: loaded, scene, step_count, episode_done, goal_position, max_steps.

### load_scene

**By file path:**
```bash
hab-cli load_scene --scene /path/to/scene.gs.ply [--dataset /path/to/config.json] [--physics]
```

**By scene ID (recommended for 3DGS with navmesh):**
```bash
hab-cli load_scene --scene-id gs_scene --dataset /path/to/config.json
```

Options:
- `--scene`: direct path to asset (`.gs.ply`, `.3dgs.ply`, `.glb`)
- `--scene-id`: scene handle from `scene_dataset_config.json` (mutually exclusive with `--scene`)
- `--dataset`: scene dataset config JSON — required for `--scene-id`, auto-loads navmesh
- `--physics`: enable Bullet physics
- `--width`, `--height`: sensor resolution (default 480x360)

When `--dataset` is provided, the bridge auto-loads the `.navmesh` from `navmesh_instances` and disables automatic navmesh recomputation (which crashes on render-only 3DGS assets).

### reset
```bash
hab-cli reset [--start x,y,z] [--goal x,y,z] [--goal-radius 0.5] [--max-steps 500]
```
Sets start/goal positions, returns initial observation. Coordinates are comma-separated x,y,z floats.

### step
```bash
hab-cli step <action>
```
Actions: `move_forward` (+0.25m), `turn_left` (+10°), `turn_right` (+10°), `stop` (end episode).

### observe
```bash
hab-cli observe
```
Get current observation without executing an action.

### path
```bash
hab-cli path [--goal x,y,z]
```
Returns geodesic distance, euclidean distance, path_found, path_points. Uses episode goal if `--goal` omitted.

### random_point
```bash
hab-cli random_point
```
Sample a random navigable point from the navmesh.

### close
```bash
hab-cli close
```

## Response Fields

Each step/observe/reset returns:
| Field | Description |
|-------|-------------|
| `agent_state.position` | [x, y, z] current position |
| `agent_state.rotation` | [qx, qy, qz, qw] quaternion |
| `observations.rgb` | base64-encoded PNG (first-person view) |
| `observations.depth_min/max` | depth range in meters |
| `collided` | hit a wall/obstacle on this step |
| `info.distance_to_goal` | euclidean distance to goal (m) |
| `info.goal_reached` | within goal_radius |
| `done` | episode ended (goal reached, max steps, or stop) |
| `step_count` | total steps so far |

## Global Options

```bash
hab-cli --url http://other-host:8890 status
```

Or set the environment variable:
```bash
export HABITAT_GS_BRIDGE_URL=http://other-host:8890
```
