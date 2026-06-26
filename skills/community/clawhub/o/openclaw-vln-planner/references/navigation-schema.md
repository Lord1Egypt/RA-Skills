# Navigation Schema Reference

## 1. Action schema

Planner output must be valid JSON:

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

### Allowed action types
- `MOVE_FORWARD`
- `TURN_LEFT`
- `TURN_RIGHT`
- `STOP`

### task_status values
- `in_progress`
- `completed`
- `failed`

## 2. Parameter bounds

### MOVE_FORWARD
- required fields: `type`, `value`, `unit`
- `type = MOVE_FORWARD`
- `value`: integer or float in `[10, 150]`
- `unit = cm`

### TURN_LEFT
- required fields: `type`, `value`, `unit`
- `type = TURN_LEFT`
- `value`: integer or float in `[5, 90]`
- `unit = deg`

### TURN_RIGHT
- required fields: `type`, `value`, `unit`
- `type = TURN_RIGHT`
- `value`: integer or float in `[5, 90]`
- `unit = deg`

### STOP
- required fields: `type`
- `type = STOP`
- `value` and `unit` should be omitted

## 3. Safety fallback strategy

Fallback to:

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

Fallback conditions:
- model output is not parseable JSON
- unsupported action type
- out-of-range angle or distance
- wrong unit for action type
- missing required fields
- confidence below configured threshold
- blocked / collision_risk / lost / low_visibility
- executor bridge rejects the action

## 4. Prompt template

```text
You are a robot navigation planner.
You will receive historical observations, a current observation, and a user instruction.
Based on them, determine the robot's next single action.

Actions are limited to:
- MOVE_FORWARD with distance in cm
- TURN_LEFT with angle in deg
- TURN_RIGHT with angle in deg
- STOP

Rules:
- Output exactly one next action.
- Do not output a full path.
- If the task is complete, output STOP.
- If uncertain or risky, output STOP.
- MOVE_FORWARD must be 10-150 cm.
- TURN_LEFT and TURN_RIGHT must be 5-90 deg.
- Output pure JSON only.

Historical observations:
{history_summary}

Current observation:
{current_summary}

User instruction:
{user_instruction}

Optional robot state:
{robot_state}

Optional safety flags:
{safety_flags}
```

## 5. Typical inputs

### Planner request object

```json
{
  "user_instruction": "Go down the hallway and stop at the blue door.",
  "current_frame": "frames/current.jpg",
  "history_frames": [
    "frames/h1.jpg",
    "frames/h2.jpg",
    "frames/h3.jpg"
  ],
  "robot_state": {
    "heading_deg": 90,
    "speed_mps": 0.0
  },
  "safety_flags": {
    "blocked": false,
    "collision_risk": false,
    "lost": false,
    "target_reached": false
  }
}
```

## 6. Typical outputs

### Forward motion

```json
{
  "next_action": {
    "type": "MOVE_FORWARD",
    "value": 60,
    "unit": "cm"
  },
  "task_status": "in_progress",
  "confidence": 0.88,
  "notes": "continue straight toward the door"
}
```

### Turn right

```json
{
  "next_action": {
    "type": "TURN_RIGHT",
    "value": 30,
    "unit": "deg"
  },
  "task_status": "in_progress",
  "confidence": 0.8,
  "notes": "turn at the visible opening"
}
```

### Completion

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

## 7. Runtime config schema

Example YAML:

```yaml
planner:
  confidence_threshold: 0.55
  fallback_on_parse_error: true
  fallback_on_invalid_action: true
  max_history_frames: 5

model:
  provider: openai_compatible
  base_url: https://your-gateway.example.com/v1
  api_key: YOUR_API_KEY
  model_id: your-model-id
  timeout_seconds: 60

input:
  source_type: single_image_sequence
  current_frame_key: current_frame
  history_frames_key: history_frames
  instruction_key: user_instruction
  robot_state_key: robot_state
  safety_flags_key: safety_flags

subscriptions:
  current_frame_topic: /camera/current_frame
  history_frames_topic: /camera/history_frames
  robot_state_topic: /robot/state
  safety_flags_topic: /robot/safety

executor:
  type: python_function
  dry_run: true
```

Notes:
- The planner consumes one current image plus historical images each round.
- `subscriptions.*` provides the logical source names / topics required by the surrounding runtime.
- The planner itself stays decoupled from the transport layer.
