---
name: docker-manager
description: "Docker container lifecycle management. Use when: user asks to list containers, start/stop containers, view logs, check stats, prune unused containers or images. Requires Docker CLI installed."
metadata:
  openclaw:
    emoji: "🐳"
    requires:
      bins:
        - docker
---

# Docker Manager Skill

Manage Docker containers, images, and system resources.

## Triggers

- "docker containers", "list containers"
- "start container", "stop container"  
- "docker logs", "container logs"
- "docker stats", "container stats"
- "docker prune", "cleanup containers"
- "docker images", "list images"

## Commands

### List Running Containers
```bash
docker ps
```

### List All Containers (including stopped)
```bash
docker ps -a
```

### Start a Container
```bash
docker start <container_id_or_name>
```

### Stop a Container
```bash
docker stop <container_id_or_name>
```

### Restart a Container
```bash
docker restart <container_id_or_name>
```

### View Container Logs
```bash
# Tail last 100 lines
docker logs --tail 100 <container_id_or_name>

# Follow logs in real-time
docker logs -f <container_id_or_name>
```

### Container Stats (CPU, Memory, Network)
```bash
# Stream stats for all running containers
docker stats

# Stats for specific container
docker stats <container_id_or_name>

# Non-streaming (one-time)
docker stats --no-stream <container_id_or_name>
```

### List Docker Images
```bash
docker images
```

### Prune Unused Containers
```bash
# Remove all stopped containers
docker container prune -f
```

### Prune Unused Images
```bash
# Remove dangling images
docker image prune -f

# Remove all unused images
docker image prune -a -f
```

### Docker System DF (Disk Usage)
```bash
docker system df
```

## Bundled Scripts

### docker-stats.sh
Script for formatted container stats output.

```bash
#!/bin/bash
# Docker container stats with formatted output

echo "Container Stats"
echo "==============="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

## Usage Examples

| Intent | Command |
|--------|---------|
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| Start nginx container | `docker start nginx` |
| Stop nginx container | `docker stop nginx` |
| View webapp logs | `docker logs --tail 50 webapp` |
| Monitor stats | `docker stats` |
| List images | `docker images` |
| Cleanup unused containers | `docker container prune -f` |
| Cleanup unused images | `docker image prune -a -f` |
| Check disk usage | `docker system df` |
