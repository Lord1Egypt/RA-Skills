---
name: jpeng-state-machine
description: "Manage state machines"
version: "1.0.0"
author: "jpeng"
tags: ["state", "machine", "automation"]
---

# State Machine

Manage state machines

## When to Use

- User needs state related functionality
- Automating machine tasks
- Automation operations

## Usage

```bash
python3 scripts/state_machine.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export MACHINE_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
