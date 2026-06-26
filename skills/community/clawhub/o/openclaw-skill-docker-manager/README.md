# docker-manager

Docker container lifecycle management skill for OpenClaw.

## Description

Manage Docker containers, images, and system resources. List, start, stop, restart containers, view logs, check stats, and prune unused resources.

## Features

- List running and all containers
- Start, stop, restart containers
- View container logs
- Monitor container stats (CPU, memory, network)
- List Docker images
- Prune unused containers and images
- Check disk usage

## Installation

### Via ClawHub
```bash
clawhub install ppopen/openclaw-skill-docker-manager
```

### Manual
```bash
git clone https://github.com/ppopen/openclaw-skill-docker-manager.git
```

## Usage

Trigger phrases:
- "List docker containers"
- "Start container"
- "Stop container"
- "View container logs"
- "Docker stats"
- "Cleanup docker"

## Requirements

- Docker CLI installed
- Docker daemon running

## License

MIT
