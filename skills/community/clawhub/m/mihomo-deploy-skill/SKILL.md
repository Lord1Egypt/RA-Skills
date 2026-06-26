---
name: mihomo-deploy
description: Deploy mihomo proxy kernel + Metacubexd web UI on a Linux server (no sudo required, uses systemd --user). Use this skill whenever the user wants to set up mihomo, clash-meta, or a proxy service on a remote/local Linux server, or mentions deploying a proxy with a subscription config file, even if they don't explicitly say "mihomo deploy".
---

# Mihomo Server Deployment

Deploy mihomo (Clash.Meta kernel) + Metacubexd web UI on a Linux server.
✔ Supports:
- dynamically get latest version of mihomo
- systemd --user (preferred)
- no sudo required (except optional linger)

## Step 0: Gather Required Information

Before doing anything on the server, collect the following from the user. Ask for all missing items up front — don't proceed until you have them.

**Required:**
- **config.yaml** — the proxy subscription config file from their provider. Ask for the file path or have them paste the path.

**With defaults (ask if they want to change):**
- **mixed-port** — the port mihomo listens on for HTTP/SOCKS traffic. Default: `7890`
- **external-controller mode** — whether the web UI controller binds to:
  - `127.0.0.1` (local loopback, accessible only via SSH tunnel) — **default**
  - `0.0.0.0` (global, accessible from any IP — less secure)
- **external-controller port** — port for the web UI API. Default: `9090`
- **secret** — password for the web UI. Required if using global (0.0.0.0) mode; optional but recommended for loopback mode. If the user doesn't specify, generate a short random string (e.g. `openssl rand -hex 8`) or ask them to provide one.

Confirm the final configuration with the user before proceeding, e.g.:
```
mixed-port: 7890
external-controller: 127.0.0.1:9090
secret: (user-provided or generated)
```

## Step 1: Detect Server Architecture

Run on the target server:

```bash
uname -m
```

Map the output to the mihomo binary suffix:
| `uname -m` output | Binary suffix |
| ----------------- | ------------- |
| `x86_64`          | `amd64`       |
| `aarch64`         | `arm64`       |
| `armv7l`          | `armv7`       |

If the architecture is anything else, stop and tell the user — unsupported architectures need manual handling.

## Step 2: Create Directory Structure

```bash
mkdir -p ~/bin
mkdir -p ~/.config/mihomo
mkdir -p ~/.config/systemd/user/
```

## Step 3: Download Mihomo Binary

Check the latest stable release at https://github.com/MetaCubeX/mihomo/releases. Use the `compatible` variant for amd64 (broader glibc compatibility). Download to `~/bin`:

```bash
cd ~/bin

# Example for amd64 (substitute version and arch as needed):
MIHOMO_VERSION=$(curl -s https://api.github.com/repos/MetaCubeX/mihomo/releases/latest | grep tag_name | cut -d '"' -f 4)
ARCH="amd64"  # change to arm64 or armv7 as detected

curl -L -O "https://github.com/MetaCubeX/mihomo/releases/download/${MIHOMO_VERSION}/mihomo-linux-${ARCH}-compatible-${MIHOMO_VERSION}.gz"

gunzip mihomo-linux-${ARCH}-compatible-${MIHOMO_VERSION}.gz
mv mihomo-linux-${ARCH}-compatible-${MIHOMO_VERSION} mihomo
chmod +x mihomo

# Verify it runs:
~/bin/mihomo -v
```

For arm64/armv7, the filename does not include "compatible" — use `mihomo-linux-arm64-${MIHOMO_VERSION}.gz` instead.

## Step 4: Download Geo Database

```bash
cd ~/.config/mihomo
curl -L -o Country.mmdb "https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb"
```

## Step 5: Deploy Metacubexd Web UI

```bash
cd ~/.config/mihomo
git clone -b gh-pages https://github.com/MetaCubeX/Metacubexd.git ui
```

If `git` is unavailable, download the zip instead:
```bash
cd ~/.config/mihomo
curl -L -o metacubexd.zip https://github.com/MetaCubeX/Metacubexd/archive/refs/heads/gh-pages.zip
unzip metacubexd.zip
mv Metacubexd-gh-pages ui
rm metacubexd.zip
```

## Step 6: Patch config.yaml

Upload the user's original config.yaml to `~/.config/mihomo/config.yaml` (via scp, sftp, or by pasting contents with `cat > ~/.config/mihomo/config.yaml`).

Then use `scripts/patch_config.py` from this skill to apply the user's settings:

```bash
python3 /path/to/skill/scripts/patch_config.py \
  --config ~/.config/mihomo/config.yaml \
  --mixed-port 7890 \
  --controller-addr 127.0.0.1 \
  --controller-port 9090 \
  --secret "your-secret-here"
```

The script modifies the config in-place, setting or replacing:
- `mixed-port`
- `external-controller`
- `external-ui: ui`
- `secret` (omit `--secret` to leave it unset or remove it)

If Python 3 is not available on the server, use `sed` as a fallback (see below), but prefer the script — YAML sed-patching is fragile.

**sed fallback** (only if Python unavailable):
```bash
CONFIG=~/.config/mihomo/config.yaml
sed -i "s/^mixed-port:.*/mixed-port: 7890/" "$CONFIG"
sed -i "s/^external-controller:.*/external-controller: '127.0.0.1:9090'/" "$CONFIG"
# Add external-ui if missing:
grep -q "^external-ui:" "$CONFIG" || echo "external-ui: ui" >> "$CONFIG"
# Add/replace secret:
grep -q "^secret:" "$CONFIG" && sed -i "s/^secret:.*/secret: 'your-secret'/" "$CONFIG" || echo "secret: 'your-secret'" >> "$CONFIG"
```

## Step 7: Create systemd User Service

Create `~/.config/systemd/user/mihomo.service`:

```bash
cat > ~/.config/systemd/user/mihomo.service << 'EOF'
[Unit]
Description=Mihomo Daemon (User Level)
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.config/mihomo
ExecStart=%h/bin/mihomo -d %h/.config/mihomo
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
```

> `%h` is systemd's specifier for the user's home directory — no need to hardcode the path.

## Step 8: (Optional) Enable Linger for Persistence After SSH Logout

By default, user services stop when you disconnect from SSH. To keep mihomo running after logout:

```bash
sudo loginctl enable-linger $USER
```

If the user doesn't have sudo, they should ask a sysadmin to run this for them, or accept that mihomo will only run during active SSH sessions.

Verify:
```bash
loginctl show-user $USER --property=Linger
# Expected: Linger=yes
```

## Step 9: Enable and Start the Service

```bash
systemctl --user daemon-reload
systemctl --user enable mihomo
systemctl --user start mihomo
```

## Step 10: Verify

```bash
systemctl --user status mihomo
```

Check logs if there are errors:
```bash
journalctl --user -u mihomo -n 30 --no-pager
```

Common issues:
- Port already in use → change `mixed-port` or `external-controller` port
- Binary not found → verify `~/bin/mihomo` exists and is executable
- Config parse error → check YAML syntax in `config.yaml`

## Step 11: Finishing Up — SSH Tunnel and Proxy Setup

Tell the user to add LocalForward entries to their SSH config (`~/.ssh/config` on their **local machine**):

```
Host your-server
  ...existing settings...
  LocalForward 127.0.0.1:<controller-port> 127.0.0.1:<controller-port>
  LocalForward 127.0.0.1:<mixed-port>      127.0.0.1:<mixed-port>
```

Replace `<controller-port>` and `<mixed-port>` with the actual values. After reconnecting, the web UI will be accessible at `http://127.0.0.1:<controller-port>/ui` in their local browser.

**Proxy environment variables** (add to `~/.bashrc` or `~/.zshrc` on the server):

```bash
# === Mihomo Proxy ===
export MY_PROXY_ADDR="127.0.0.1:<mixed-port>"
export MY_NO_PROXY='localhost,127.0.0.1,::1,mirrors.tuna.tsinghua.edu.cn,pypi.tuna.tsinghua.edu.cn,hf-mirror.com,*.hf-mirror.com,*.tuna.tsinghua.edu.cn,repo.anaconda.com,*.anaconda.com,conda.anaconda.org'

alias proxy_on="
    export http_proxy=\"http://\$MY_PROXY_ADDR\";
    export https_proxy=\"http://\$MY_PROXY_ADDR\";
    export all_proxy=\"socks5h://\$MY_PROXY_ADDR\";
    export ALL_PROXY=\"socks5h://\$MY_PROXY_ADDR\";
    export no_proxy=\"\$MY_NO_PROXY\";
    export NO_PROXY=\"\$MY_NO_PROXY\";
    echo 'Proxy set to '\$MY_PROXY_ADDR
"
alias proxy_off="
    unset http_proxy https_proxy all_proxy;
    echo 'Proxy restored to original state'
"

proxy_on
```

Verify the proxy is working:
```bash
curl ip-api.com
```

The response should show the IP/location of one of the proxy nodes, not the server's own IP.

## Updating / Restarting After Config Changes

If the user modifies `config.yaml` later:
```bash
systemctl --user daemon-reload
systemctl --user restart mihomo
journalctl --user -u mihomo -n 20 --no-pager
```
