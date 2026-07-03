# Docker Manager

Docker container and image management with health monitoring and auto-cleanup.

## Features
- Container lifecycle management
- Image pruning and cleanup
- Resource monitoring (CPU, memory, disk)
- Log rotation and management
- Bulk operations across hosts
- Automated health checks

## Usage
```bash
clawdhub install king-docker-manager
python3 main.py ps
python3 main.py prune --all
python3 main.py monitor nginx
```
