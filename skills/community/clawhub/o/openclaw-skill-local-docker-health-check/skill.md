---
name: Docker Medic
description: Inspects container health and suggests fixes for common errors
version: 1.0.0-openclaw-skill-local-docker-health-check
commands:
  - name: check_containers
    description: Check the health of Docker containers and suggest fixes for any issues detected
    parameters:
      - name: name
        type: string
        required: false
        description: Optional container name to check. If omitted, all containers are inspected.
---

# Docker Medic

Docker Medic inspects the health of your Docker containers and suggests fixes for common errors.

## Usage

```
/docker_medic check_containers [--name <container_name>]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name`    | No       | Specific container name to inspect. Defaults to all containers. |

## What It Does

1. Lists running and stopped containers (or targets the named container).
2. Checks container health status, restart counts, and exit codes.
3. Inspects container logs for common error patterns (OOM kills, port conflicts, missing configs, crash loops).
4. Returns a summary of findings and suggested fixes.
