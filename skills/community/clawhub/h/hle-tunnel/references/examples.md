# HLE Tunnel Examples

## Agent UI — remote access

```bash
# Access your agent's Control UI from anywhere
hle expose --service http://localhost:18789 --label my-agent

# Share with a collaborator via SSO
hle expose --service http://localhost:18789 --label my-agent \
  --allow colleague@company.com

# Allow multiple users
hle expose --service http://localhost:18789 --label my-agent \
  --allow dev1@company.com --allow dev2@company.com
```

## Homelab services

```bash
# Home Assistant — allow yourself remotely
hle expose --service http://localhost:8123 --label ha \
  --allow you@gmail.com

# Grafana — share dashboard with your team
hle expose --service http://localhost:3000 --label grafana \
  --allow dev1@company.com --allow dev2@company.com

# Jellyfin media server — share with family
hle expose --service http://localhost:8096 --label media \
  --allow family@gmail.com

# Node-RED
hle expose --service http://localhost:1880 --label nodered \
  --allow you@gmail.com

# Pi-hole admin
hle expose --service http://localhost:80 --label pihole \
  --allow you@gmail.com

# Portainer
hle expose --service https://localhost:9443 --label portainer \
  --allow you@gmail.com
```

## Development

```bash
# Next.js / React dev server — share with a client
hle expose --service http://localhost:3000 --label dev \
  --allow client@company.com

# API server — share with a teammate
hle expose --service http://localhost:8000 --label api \
  --allow teammate@company.com

# Jupyter notebook — share with a colleague
hle expose --service http://localhost:8888 --label notebook \
  --allow colleague@company.com

# MCP server — share with a teammate
hle expose --service http://localhost:8080 --label mcp-server \
  --allow teammate@company.com
```

## Docker

```bash
# Run HLE container (headless, no UI)
docker run -d --name hle -e HLE_API_KEY=your_key \
  -v hle-data:/data ghcr.io/hle-world/hle-docker:headless

# Expose the agent's Control UI running on the Docker host
docker exec hle hle expose \
  --service http://host.docker.internal:18789 \
  --label my-agent \
  --allow you@gmail.com

# Expose a service running in another container (use container name or Docker network IP)
docker exec hle hle expose \
  --service http://my-other-container:8080 \
  --label backend \
  --allow colleague@company.com
```

## Background tunnel with process manager

```bash
# Using nohup
nohup hle expose --service http://localhost:18789 --label my-agent > /dev/null 2>&1 &

# Using systemd (create a service file)
# /etc/systemd/system/hle-tunnel.service
# [Unit]
# Description=HLE Tunnel
# After=network.target
# [Service]
# ExecStart=hle expose --service http://localhost:18789 --label my-agent
# Restart=always
# Environment=HLE_API_KEY=hle_your_key_here
# [Install]
# WantedBy=multi-user.target
```

## Access control examples

```bash
# Grant SSO access to a user (they log in via Google/GitHub)
hle access add my-agent-x7k dev@company.com

# Create a share link that expires in 2 hours, max 3 uses
hle share create my-agent-x7k --duration 2h --max-uses 3 --label "client demo"

# Set a PIN for quick mobile access
hle pin set my-agent-x7k
# Enter: 1234

# List all access rules
hle access list my-agent-x7k

# Revoke a share link
hle share revoke my-agent-x7k 42
```
