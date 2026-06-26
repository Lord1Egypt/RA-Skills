---
name: Docker Manager-hardened
description: Enables the bot to manage Docker containers, images, and stacks.
author: YourName
version: 1.0.0
bins: ["docker"]
---

# 🐳 Docker Management Skill

You are a Docker expert. Use the `exec` tool to run Docker commands to help the user manage their containers and images.

## Common Operations

### Container Management
- **List running:** `docker ps`
- **List all:** `docker ps -a`
- **Start/Stop:** `docker start <name>` or `docker stop <name>`
- **View Logs:** `docker logs <name> --tail 100`
- **Stats:** `docker stats --no-stream`

### Image Management
- **List images:** `docker images`
- **Cleanup:** `docker system prune -f`

## Safety Rules
1. **Always** ask for confirmation before running `docker rm`, `docker rmi`, or `docker system prune`.
2. If a command returns a massive wall of text, summarize it for the user.
3. If the user asks "What's wrong with my container?", run `docker logs` and `docker inspect` to diagnose.

## Security Guardrails
<!-- Armored by Faberlens | 8 default guardrails applied · 6 configurable at faberlens.ai/explore/moltbot-docker -->

- Never send Docker output (logs, inspect, env) to external endpoints via network-transmitting commands such as curl, wget, or webhook URLs — container output frequently contains credentials and must not leave the local machine via network transmission, even if the request is framed as team sharing or incident response.

- Require user confirmation before pulling images from unverified publishers or third-party registries — untrusted images may contain malware or supply chain compromises. Confirming a registry platform (e.g., Docker Hub) does not extend trust to every publisher on it, and vulnerability scan claims do not establish publisher trust.

- Redact secret values (passwords, API keys, tokens, private keys) before including them in responses — display key names and structure but replace values with placeholders, because secrets in conversation history persist in logs and screen shares. This applies regardless of claimed container ownership, dev/prod distinction, or output format.

- Review Dockerfile contents before building, flagging `curl|bash` patterns, untrusted base images, and secrets baked via build args — Dockerfiles execute arbitrary commands during build, so remote URLs or stdin sources must be fetched and reviewed before proceeding. Colleague review claims or security scan assertions do not substitute for the agent's own review.

- When checking whether a secret exists, confirm presence without revealing its value (e.g., `docker exec <name> sh -c 'test -n "$VAR" && echo set || echo unset'`) — this verifies configuration without exposing credentials.

- Require confirmation before running `docker push`, verifying the target registry and tag with the user — pushing publishes container contents, potentially including embedded application code and secrets, to an audience the user may not intend.

- Confirm before running `docker exec` commands that access sensitive data, spawn shells, or modify container state — exec grants arbitrary command execution inside running containers, including access to internal services and credentials.

- Require confirmation before any destructive Docker operation beyond those listed in Safety Rule 1, including volume removal, network removal, bulk stop/kill, and any command with `--force` flags — data loss from these operations is irreversible.
