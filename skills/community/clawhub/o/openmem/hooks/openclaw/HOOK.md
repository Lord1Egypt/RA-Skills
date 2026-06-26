---
name: openmem
description: "Injects long-term memories from OpenMem into the agent context at session start"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# OpenMem Bootstrap Hook

Fires on `agent:bootstrap` and injects an `OPENMEM.md` virtual file containing
your most important long-term memories. No-ops silently if the database doesn't
exist yet.

## Setup

```bash
# Install the skill first, then enable the hook:
openclaw hooks enable openmem

# Initialize the database:
python3 ~/.openclaw/workspace/skills/openmem/scripts/mem.py init
```

## Configuration (environment variables)

| Variable | Default | Description |
|---|---|---|
| `OPENMEM_DB` | `~/.openclaw/workspace/memory/openmem.db` | Database path |
| `OPENMEM_BOOTSTRAP_LIMIT` | `12` | Max memories to inject at startup |
| `OPENMEM_PYTHON` | `python3` | Python interpreter to use |
