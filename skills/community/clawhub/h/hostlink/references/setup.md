# HostLink Setup Guide

## Host-side installation (run these on your host machine)

### 1. Clone and build

```bash
git clone https://github.com/jebadiahgreenwood/hostlink ~/hostlink
cd ~/hostlink
make
sudo make install
# Installs: /usr/local/bin/hostlinkd, /usr/local/bin/hostlink-cli
# Creates:  /etc/hostlink/, /run/hostlink/, /var/log/hostlink/
```

Or manually:
```bash
gcc -std=c11 -O2 -o hostlinkd \
    src/common/cjson/cJSON.c src/common/log.c src/common/util.c \
    src/common/protocol.c src/common/config.c \
    src/daemon/executor.c src/daemon/server.c src/daemon/main.c \
    -I src/common -I src/common/cjson
sudo cp hostlinkd /usr/local/bin/
```

### 2. Create config

```bash
sudo mkdir -p /etc/hostlink /run/hostlink /var/log/hostlink
sudo tee /etc/hostlink/hostlink.conf << 'EOF'
node_name = host
auth_token = CHANGE_THIS_TO_A_STRONG_SECRET
unix_enabled = 1
unix_path = /run/hostlink/hostlink.sock
unix_mode = 0660
tcp_enabled = 0
max_concurrent = 8
default_timeout_ms = 30000
max_timeout_ms = 300000
shell = /bin/bash
default_max_output_bytes = 4194304
max_output_bytes = 67108864
output_tmpdir = /tmp/hostlink_output
log_target = file
log_file = /var/log/hostlink/hostlinkd.log
log_level = info
EOF
sudo chmod 640 /etc/hostlink/hostlink.conf
```

**Important:** Change `auth_token` to a strong random secret:
```bash
openssl rand -hex 32
```

### 3. Start the daemon

**Option A — systemd (recommended):**
```bash
sudo cp ~/hostlink/hostlink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hostlinkd
sudo systemctl start hostlinkd
sudo systemctl status hostlinkd
```

**Option B — manual foreground (testing):**
```bash
sudo hostlinkd -f -c /etc/hostlink/hostlink.conf
```

### 4. Verify socket exists

```bash
ls -la /run/hostlink/hostlink.sock
# srw-rw---- 1 root hostlink 0 ... /run/hostlink/hostlink.sock
```

---

## Docker Compose configuration

Add to your `docker-compose.yml` for the openclaw-gateway service:

```yaml
services:
  openclaw-gateway:
    volumes:
      - /run/hostlink/hostlink.sock:/run/hostlink/hostlink.sock
    environment:
      - HOSTLINK_SOCKET=/run/hostlink/hostlink.sock
      - HOSTLINK_TOKEN=SAME_TOKEN_AS_IN_HOSTLINK_CONF
```

Then restart the container:
```bash
docker compose down && docker compose up -d
```

---

## OpenClaw config (add auth token as env var)

In `~/.openclaw/openclaw.json`, add to the `env.vars` section:

```json
{
  "env": {
    "vars": {
      "HOSTLINK_TOKEN": "your_auth_token_here",
      "HOSTLINK_SOCKET": "/run/hostlink/hostlink.sock"
    }
  }
}
```

Or set it in your host's `.env` file if using docker-compose env file loading.

---

## Test the connection

From inside the OpenClaw container:
```bash
hostlink ping
# Expected: [host] pong - uptime Xs
```

If that works, HostLink is fully operational.

---

## Security notes

- The auth token is the only secret. Keep it out of git.
- The Unix socket is accessible to anyone who can read the socket file.
  The `unix_mode = 0660` + `hostlink` group membership restricts access.
- All commands run as the user hostlinkd is started as (typically root if using systemd).
  Consider running as a dedicated less-privileged user for production use.
- TCP transport (for remote access) requires WireGuard — do not expose hostlinkd directly to the internet.
