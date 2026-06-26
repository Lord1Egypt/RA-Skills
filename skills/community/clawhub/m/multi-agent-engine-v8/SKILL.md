---
name: multi-agent-engine-v8
description: "Multi-Agent Orchestrator v8.2.1 - Enhanced stability (Node.js v24 compatibility, lazy environment detection, third-party environment adaptation). Supports goal-driven research, task decomposition, parallel execution, validation review, and smart decisions."
---

# Multi-Agent Orchestrator v8.2.1

Goal-driven deep research and project collaboration system with multi-agent parallel execution.

## Key Features

- **Lazy environment detection** - No blocking on module load
- **Node.js v24 compatibility** - Warnings for compatibility issues
- **openclaw.json size protection** - 5MB limit
- **Simplified model pool** - No hardcoded model IDs

## Commands

```bash
# Environment check
multi-agent check_env

# Start workflow
multi-agent run --goal "Research topic"

# Generate plan
multi-agent plan --goal "Research topic"

# View help
multi-agent help
```

## Requirements

- OpenClaw: 2026.3.x+
- Node.js: 20.5+ (recommended: 20 LTS or 22 LTS)

## Changelog

- v8.2.1: No hardcoded model IDs (adapts to third-party environments)
- v8.2.0: Node.js v24 compatibility + environment detection optimization
- v8.1.0: Active polling monitor + timeout degradation
- v8.0.0: Token optimization + JSON constraint output