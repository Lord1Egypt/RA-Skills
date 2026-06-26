
# OpenClaw Docker - Simple Setup (Using Official Image)

This is the SIMPLE way to run OpenClaw using the official pre-built Docker image.
**No building required!** Just pull and run.

## Quick Start (5 Minutes)

### 1. Create your setup directory

```bash
mkdir openclaw-docker
cd openclaw-docker
```

### 2. Create `.env` file

```bash
cat > .env << 'EOF'
# AI Model API Key (REQUIRED - at least one)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
# OPENAI_API_KEY=sk-your-key-here
# GOOGLE_API_KEY=your-key-here

# Gateway Auth Token (generate with: openssl rand -hex 32)
OPENCLAW_GATEWAY_TOKEN=your-secure-random-token-here

# Messaging Platforms (Optional)
# TELEGRAM_BOT_TOKEN=
# DISCORD_BOT_TOKEN=
# SLACK_BOT_TOKEN=
EOF
```

### 3. Create `docker-compose.yml`

See `references/docker-config.md` for the full template.

### 4. Fix permissions (IMPORTANT on Linux)

```bash
# Create directories with proper ownership
mkdir -p ~/.openclaw ~/openclaw/workspace

# On Linux, set ownership to UID 1000 (the 'node' user in the container)
sudo chown -R 1000:1000 ~/.openclaw ~/openclaw

# On Mac, the default user is already compatible
```

### 5. Pull the image and start

```bash
docker-compose pull
docker-compose up -d
docker-compose logs -f
```

### 6. Run initial setup (REQUIRED - first time only)

```bash
docker-compose run --rm openclaw-cli onboard
```

Follow the prompts to select your AI model, configure messaging channels, and set up security preferences.

### 7. Access the dashboard

```bash
docker-compose run --rm openclaw-cli dashboard --no-open
# Copy the URL and open it in your browser
# Example: http://localhost:18789?token=your-token-here
```

## Common Commands

```bash
docker-compose logs -f openclaw          # View logs
docker-compose down                      # Stop
docker-compose restart openclaw          # Restart
docker-compose pull && docker-compose up -d  # Update to latest

# CLI commands
docker-compose run --rm openclaw-cli status
docker-compose run --rm openclaw-cli doctor
docker-compose run --rm openclaw-cli devices list
docker-compose run --rm openclaw-cli pairing list
```

## Setting Up Telegram (Optional)

1. Message @BotFather on Telegram, send `/newbot`
2. Copy the token to `.env` as `TELEGRAM_BOT_TOKEN`
3. Restart: `docker-compose restart openclaw`
4. Message your bot — you'll get a pairing code
5. Approve it:
   ```bash
   docker-compose run --rm openclaw-cli pairing approve telegram YOUR_CODE
   ```

## Backup Your Data

```bash
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw
```

## Security Notes

1. Use a strong random `OPENCLAW_GATEWAY_TOKEN` — generate with `openssl rand -hex 32`
2. Don't expose port 18789 to the internet without HTTPS
3. Use DM pairing mode for unknown senders
4. Never commit `.env` to git
