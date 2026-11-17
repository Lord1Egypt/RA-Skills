# Common Usage

Split out of `SKILL.md` to keep it within the 100-line budget.

## Common Usage

**Generate a secure token:**
```bash
openssl rand -hex 32
```

**View container logs:**
```bash
docker-compose logs -f openclaw
```

**Run CLI commands inside container:**
```bash
docker-compose run --rm openclaw-cli COMMAND_HERE
```

**Fix volume permissions (Linux):**
```bash
# Verify the uid first - 1000 is not your uid on every machine.
id -u; id -g
# Then use YOUR actual ids (shown above), not a guessed 1000:
sudo chown -R "$(id -u):$(id -g)" ~/.openclaw ~/openclaw
```

**Approve Telegram pairing:**
```bash
docker-compose run --rm openclaw-cli pairing approve telegram YOUR_CODE
```

**Access via Tailscale (recommended — HTTPS):**
```bash
sudo apt install tailscale
sudo tailscale up
./docker-setup.sh tailscale  # Starts tailscale serve on port 18789
```
Then visit `https://YOUR_MACHINE_NAME.YOUR_TAILNET.ts.net?token=YOUR_TOKEN` from any device on your tailnet. Use MagicDNS hostname over raw IP — it's HTTPS by default and more stable.
