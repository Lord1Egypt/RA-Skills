# Supported Trace Shapes

`distill_logic.py` accepts either of these JSON shapes:

## Object Form

```json
{
  "task": "repair npm cache",
  "status": "success",
  "utility_score": 4,
  "events": [
    {
      "tool": "exec",
      "command": "npm cache verify",
      "status": "ok"
    }
  ]
}
```

## Array Form

```json
[
  {
    "tool": "exec",
    "command": "npm cache verify",
    "status": "ok"
  }
]
```

## Recognized Event Fields

- `tool`, `type`, or `kind`
- `command`
- `path`
- `url`
- `status`, `ok`, or `success`
- `error`
- `content`, `snippet`, `diff`, or `patch`
- `timestamp`

Unknown fields are preserved in memory metadata only when they are needed for diagnostics.
