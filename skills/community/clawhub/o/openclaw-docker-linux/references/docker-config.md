
# Docker Configuration

Complete setup files for running OpenClaw in Docker.

## docker-compose.yml

```yaml
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:v1
    container_name: openclaw_agent
    restart: unless-stopped
    environment:
      # Required
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - HOME=/home/node
      - NODE_ENV=production
      - PATH=/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      # Optional — add whichever you need
      - BRAVE_API_KEY=${BRAVE_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ~/openclaw/workspace:/home/node/.openclaw/workspace
      # ⚠️  OPTIONAL host tool mounts — commented out by default.
      # Only uncomment what you actually need. These expose host credentials to the container:
      # - ~/.config/gh contains GitHub CLI auth tokens
      # - .npm-global may contain registry credentials
      # - /home/linuxbrew exposes your entire Homebrew installation
      # Uncomment selectively:
      # - /home/linuxbrew:/home/linuxbrew
      # - /home/YOUR_USERNAME/.npm-global:/home/YOUR_USERNAME/.npm-global
      # - /home/YOUR_USERNAME/.config/gh:/home/node/.config/gh
    ports:
      # Bind to localhost only for security; use Tailscale for remote access
      - "127.0.0.1:18789:18789"
    command: ["bash", "/home/node/.openclaw/workspace/scripts/start.sh"]

  openclaw-cli:
    image: ghcr.io/openclaw/openclaw:v1
    profiles: ["cli"]
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ~/openclaw/workspace:/home/node/.openclaw/workspace
      # - /home/linuxbrew:/home/linuxbrew  # Optional — only if needed
    environment:
      - HOME=/home/node
      - PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    entrypoint: ["node", "dist/index.js"]
```

> Replace `YOUR_USERNAME` with your actual Linux username throughout.
> Remove volume mounts you don't need (e.g. Linuxbrew, npm-global, gh config).

## .env Template

Create `.env` in the same directory as `docker-compose.yml`:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
OPENCLAW_GATEWAY_TOKEN=   # Generate with: openssl rand -hex 32

# Optional — messaging
TELEGRAM_BOT_TOKEN=

# Optional — other AI providers
GEMINI_API_KEY=

# Optional — tools
BRAVE_API_KEY=
ELEVENLABS_API_KEY=
GITHUB_TOKEN=
```

Generate a secure gateway token:
```bash
openssl rand -hex 32
```

> Never commit `.env` to git. Add it to `.gitignore`.

## openclaw.json — Critical Fields

Inside `~/.openclaw/openclaw.json`, ensure:

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "allowedOrigins": [
      "http://localhost:18789",
      "https://YOUR_MACHINE_NAME.YOUR_TAILNET.ts.net"
    ]
  }
}
```

> Use your Tailscale MagicDNS hostname (e.g. `https://my-machine.tailabcd1.ts.net`) — not the raw IP. It's HTTPS by default and stable across reboots.
> Get your hostname: `tailscale status | head -1`

Run `openclaw doctor --fix` after onboarding to auto-correct any config issues.

## Management Script

A `docker-setup.sh` helper script simplifies common operations. Place it alongside your `docker-compose.yml`:

```bash
chmod +x docker-setup.sh
```

**Available commands:**
```bash
./docker-setup.sh start          # Pull latest image, start container, auto-fix config
./docker-setup.sh stop           # Stop container
./docker-setup.sh restart        # Restart container
./docker-setup.sh logs           # Follow logs
./docker-setup.sh status         # Container + OpenClaw status
./docker-setup.sh doctor         # Run openclaw doctor --fix
./docker-setup.sh info           # Show access URLs with token
./docker-setup.sh approve_telagram  # Interactive Telegram pairing approval
./docker-setup.sh security_audit    # Run openclaw security audit --deep --fix
./docker-setup.sh tailscale      # Start Tailscale serve on port 18789
```

The `start` command automatically:
- Pulls the latest image
- Checks for missing `gateway.mode` and runs `doctor --fix` if needed
- Displays local and Tailscale access URLs with your token

---

## Volume Permissions (Linux)

If you see permission errors on mounted volumes, set ownership to UID 1000 (the `node` user inside the container):

```bash
sudo chown -R 1000:1000 ~/.openclaw ~/openclaw
```

On macOS, permissions usually work out of the box. If not:
```bash
chmod -R 755 ~/.openclaw ~/openclaw
```

---

## Telegram Pairing

After connecting your Telegram bot:
1. Message your bot from Telegram
2. You'll receive a pairing code
3. Approve it:
```bash
docker-compose run --rm openclaw-cli pairing approve telegram YOUR_CODE
```

Or use the management script:
```bash
./docker-setup.sh approve_telagram
```

---

## Tailscale Setup on Host

Tailscale runs on the Ubuntu host, not in the container.

```bash
# Install
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.noarmor.gpg | \
  sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null

curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/noble.tailscale-keyring.list | \
  sudo tee /etc/apt/sources.list.d/tailscale.list

sudo apt-get update && sudo apt-get install tailscale

# Connect
sudo tailscale up

# Get your IP
tailscale ip -4
```

**Preferred — use MagicDNS hostname (HTTPS, no port needed):**
```bash
./docker-setup.sh tailscale  # Starts tailscale serve proxy
```
Then access at: `https://YOUR_MACHINE_NAME.YOUR_TAILNET.ts.net?token=YOUR_TOKEN`

This is more secure than raw IP (HTTPS via Tailscale's TLS certs) and more stable (hostname doesn't change if your IP does).

**Raw IP fallback (HTTP):**
`http://YOUR_TAILSCALE_IP:18789?token=YOUR_TOKEN`
