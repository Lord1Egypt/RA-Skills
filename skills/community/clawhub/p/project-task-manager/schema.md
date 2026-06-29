# Project Task Manager Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `project-task-manager`

x402 availability: not enabled for this product.

## `decompose`

Action slug: `decompose`

Price: `20` credits

Break a single task description into smaller, actionable subtasks. Standalone operation that does not require an existing task tree.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `level_of_detail` | `string` | no | How detailed the breakdown should be. 'basic' (3-5 steps), 'standard' (5-10 steps, default), 'detailed' (10-15 steps). |
| `task` | `string` | yes | The task to break into smaller steps. Be specific. Example: 'Implement user login with session management'. |

Sample parameters:

```json
{
  "level_of_detail": "basic",
  "task": "example task"
}
```

Generated JSON parameter schema:

```json
{
  "level_of_detail": {
    "description": "How detailed the breakdown should be. 'basic' (3-5 steps), 'standard' (5-10 steps, default), 'detailed' (10-15 steps).",
    "enum": [
      "basic",
      "standard",
      "detailed"
    ],
    "required": false,
    "type": "string"
  },
  "task": {
    "description": "The task to break into smaller steps. Be specific. Example: 'Implement user login with session management'.",
    "required": true,
    "type": "string"
  }
}
```

## `generate`

Action slug: `generate`

Price: `20` credits

Create a hierarchical task breakdown from a high-level objective. An AI model analyzes the objective and produces a structured tree of tasks with dependencies, time estimates, and priorities.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `object` | no | Technologies or constraints. Example: {"tech": ["python", "postgresql"], "constraints": ["must use docker", "deploy to AWS"]}. |
| `max_depth` | `integer` | no | How many levels deep to break down tasks. 2 = simple, 3 = standard (default), 4 = very detailed. |
| `objective` | `string` | yes | What you want to accomplish. Be specific about the end goal. Max 2000 characters. Example: 'Build a REST API for user management with JWT authentication'. |

Sample parameters:

```json
{
  "context": {},
  "max_depth": 1,
  "objective": "example objective"
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "Technologies or constraints. Example: {\"tech\": [\"python\", \"postgresql\"], \"constraints\": [\"must use docker\", \"deploy to AWS\"]}.",
    "properties": {},
    "required": false,
    "type": "object"
  },
  "max_depth": {
    "description": "How many levels deep to break down tasks. 2 = simple, 3 = standard (default), 4 = very detailed.",
    "required": false,
    "type": "integer"
  },
  "objective": {
    "description": "What you want to accomplish. Be specific about the end goal. Max 2000 characters. Example: 'Build a REST API for user management with JWT authentication'.",
    "required": true,
    "type": "string"
  }
}
```

## `list`

Action slug: `list`

Price: `20` credits

Show all your task trees sorted by most recently updated. Returns up to 50 trees with their IDs, objectives, task counts, and progress.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `status`

Action slug: `status`

Price: `20` credits

Check the current progress and status of a task tree. Returns overall progress, completed/remaining tasks, blocked items, and estimated completion time.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tree_id` | `string` | yes | The tree_id returned from the generate action. |

Sample parameters:

```json
{
  "tree_id": "example tree id"
}
```

Generated JSON parameter schema:

```json
{
  "tree_id": {
    "description": "The tree_id returned from the generate action.",
    "required": true,
    "type": "string"
  }
}
```

## `update`

Action slug: `update`

Price: `20` credits

Mark progress on a specific task within a task tree. Update status, completion percentage, and add notes about what happened.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `notes` | `string` | no | What you learned or what happened while working on this task. Keep it brief. Max 500 characters. |
| `progress` | `number` | no | How complete is this task. 0 = not started, 50 = halfway done, 100 = finished. |
| `task_id` | `string` | yes | The specific task_id to update. Use one of the task_ids from the generate response. |
| `task_status` | `string` | no | New status for the task. Use 'in_progress' when you start, 'completed' when done, 'failed' if you cannot do it, 'blocked' if you are stuck. |
| `tree_id` | `string` | yes | The tree_id returned from the generate action. Identifies which project you are working on. |

Sample parameters:

```json
{
  "notes": "example notes",
  "progress": 1,
  "task_id": "example task id",
  "task_status": "pending",
  "tree_id": "example tree id"
}
```

Generated JSON parameter schema:

```json
{
  "notes": {
    "description": "What you learned or what happened while working on this task. Keep it brief. Max 500 characters.",
    "required": false,
    "type": "string"
  },
  "progress": {
    "description": "How complete is this task. 0 = not started, 50 = halfway done, 100 = finished.",
    "required": false,
    "type": "number"
  },
  "task_id": {
    "description": "The specific task_id to update. Use one of the task_ids from the generate response.",
    "required": true,
    "type": "string"
  },
  "task_status": {
    "description": "New status for the task. Use 'in_progress' when you start, 'completed' when done, 'failed' if you cannot do it, 'blocked' if you are stuck.",
    "enum": [
      "pending",
      "in_progress",
      "completed",
      "failed",
      "blocked"
    ],
    "required": false,
    "type": "string"
  },
  "tree_id": {
    "description": "The tree_id returned from the generate action. Identifies which project you are working on.",
    "required": true,
    "type": "string"
  }
}
```
