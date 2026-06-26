---
name: openclaw-vln-planner
description: Plan the next high-level navigation step for a robot from a user navigation instruction, one current image, and a sequence of historical images. Use when the task is vision-language navigation, closed-loop replanning, multimodal next-action prediction, or converting visual observations into a single structured JSON navigation action for an OpenAI-compatible multimodal gateway and a separate execution bridge.
---

# OpenClaw VLN Planner

Use this skill when the user wants a robot to follow a natural-language navigation instruction from visual observations.

This skill is a **high-level navigation planner**. It does **not** produce motor, joint, torque, or trajectory control. It only produces one structured **mid-level navigation action** at a time.

## When this skill triggers

Trigger this skill when the task includes one or more of the following:
- Vision-language navigation (VLN)
- Robot next-step planning from camera images
- Closed-loop navigation with replanning after each observation
- Converting a current frame plus historical frames into a single next navigation action
- Sending current + history images to an OpenAI-compatible multimodal gateway for action prediction

## Required inputs

The planner expects:
- `user_instruction`: natural-language navigation instruction
- `current_frame`: exactly one current image
- `history_frames`: zero or more previous images in temporal order

Optional inputs:
- `robot_state`: heading, speed, pose estimate, execution feedback, etc.
- `safety_flags`: blocked, collision_risk, lost, target_reached, low_visibility, etc.
- `config_path`: path to the runtime config file

## Output contract

Output must be **pure JSON only**. Do not prepend or append prose.

Allowed action types only:
- `MOVE_FORWARD`
- `TURN_LEFT`
- `TURN_RIGHT`
- `STOP`

Expected JSON shape:

```json
{
  "next_action": {
    "type": "MOVE_FORWARD",
    "value": 75,
    "unit": "cm"
  },
  "task_status": "in_progress",
  "confidence": 0.87,
  "notes": "continue along the hallway"
}
```

Completion example:

```json
{
  "next_action": {
    "type": "STOP"
  },
  "task_status": "completed",
  "confidence": 0.93,
  "notes": "goal reached"
}
```

## Core rules

1. Plan **only the next action**.
2. Never output a full route.
3. Replan after each execution step.
4. If uncertain, unsafe, blocked, unable to parse, or visually ambiguous, output `STOP`.
5. Enforce action bounds:
   - `MOVE_FORWARD`: 10-150 cm
   - `TURN_LEFT`: 5-90 deg
   - `TURN_RIGHT`: 5-90 deg
   - `STOP`: no value/unit required
6. If `safety_flags.target_reached == true`, output `STOP` with `task_status = completed`.
7. If `blocked`, `collision_risk`, `lost`, or severe uncertainty is present, prefer `STOP`.

## Runtime configuration

Before running, load a YAML config file such as `config/vln-config.yaml`.

The config should define:
- subscribed or logical input topics / channels for current frame and history frame collection
- optional robot state and safety flag sources
- OpenAI-compatible multimodal gateway settings: `base_url`, `api_key`, `model_id`
- planner behavior such as confidence threshold and safety fallback
- executor bridge mode (default: Python function bridge)

Read `references/navigation-schema.md` for the expected config structure.

## Internal module design

### 1) context builder
Build a model input payload from:
- user instruction
- historical observations
- current observation
- optional robot state
- optional safety flags

The prompt must explicitly separate:
- historical observations
- current observation
- user instruction

### 2) action planner
Call an **OpenAI-compatible multimodal gateway** with:
- one current image
- historical images
- planner prompt
- optional structured context

The model should be asked to return pure JSON for exactly one next action.

### 3) action parser
Parse the model result as JSON.

If parsing fails:
- try safe extraction of the first JSON object
- if still invalid, fall back to `STOP`

### 4) action validator
Validate:
- action type is one of the four allowed values
- distance and angle ranges are legal
- unit matches action type
- confidence is numeric if present
- task_status is one of `in_progress`, `completed`, `failed`

Any invalid output falls back to `STOP`.

### 5) executor bridge
Forward the validated mid-level action to a separate execution layer.

Reserved Python bridge interface:
- `execute_move_forward(distance_cm)`
- `execute_turn_left(angle_deg)`
- `execute_turn_right(angle_deg)`
- `execute_stop()`
- `get_robot_state()`
- `get_safety_flags()`

Do not hardcode a robot SDK into the planner logic.

### 6) replanning loop
Use the planner in a closed loop:
1. gather current frame + history frames
2. gather optional robot state / safety flags
3. call multimodal planner
4. parse and validate JSON action
5. execute through bridge
6. observe again
7. repeat until `task_status = completed` or forced stop

### 7) safety fallback
Always stop on:
- parse failure
- invalid action
- confidence below threshold
- blocked / collision risk / lost / target reached
- missing visual evidence for safe motion

## Prompt template

Use this prompt pattern:

```text
You are a robot navigation planner.
You will receive:
1. historical observations
2. current observation
3. a user instruction
4. optional robot state and safety flags

Your job is to decide the robot's next single mid-level navigation action.
You may output only one of these actions:
- MOVE_FORWARD with distance in cm
- TURN_LEFT with angle in deg
- TURN_RIGHT with angle in deg
- STOP

Rules:
- Plan only the next step, not the whole route.
- If the goal has been reached, output STOP.
- If you are uncertain, the scene is unclear, or there is any safety risk, output STOP.
- MOVE_FORWARD must be 10-150 cm.
- TURN_LEFT and TURN_RIGHT must be 5-90 deg.
- Output pure JSON only, with no extra explanation.
```

## Example user requests

- "Go down the hallway and stop at the blue door."
- "Move to the kitchen entrance."
- "Find the end of the corridor and stop."
- "Turn right at the next intersection and continue."

## Failure handling

If anything is wrong with the output, return:

```json
{
  "next_action": {
    "type": "STOP"
  },
  "task_status": "failed",
  "confidence": 0.0,
  "notes": "fallback_stop"
}
```

## Bundled resources

- `references/navigation-schema.md`: schema, bounds, safety fallback, examples, config contract
- `scripts/vln_bridge.py`: example OpenAI-compatible multimodal planner + Python executor bridge
- `scripts/requirements.txt`: Python dependencies
- `config/vln-config.yaml`: runtime config template
