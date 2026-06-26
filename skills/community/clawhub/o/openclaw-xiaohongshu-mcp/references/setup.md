# Setup

## 1. Start the local MCP service

From the repository root, use:

```bash
docker compose -f assets/docker-compose.xiaohongshu-mcp.yml up -d
```

## 2. Check service and login

```bash
mcporter --config assets/config/mcporter.json list --json
mcporter --config assets/config/mcporter.json call xiaohongshu.check_login_status
```

## 3. Local image convention

Recommended host directory:

```text
./data/xiaohongshu-mcp/images
```

Publish using container-visible paths, for example:

```json
"images": ["/images/demo.png"]
```

## 4. Persistence notes

Persist at least these paths through Docker volumes:

- `/app/cookies.json`
- `/root/.config/google-chrome`
- `/root/.pki`
- `/tmp/rod/user-data`

That usually preserves login state across restarts.
