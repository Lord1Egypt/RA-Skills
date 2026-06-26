# Server setup runbook

## Assumptions

- OS is Ubuntu 22.04 or close equivalent
- agent has root access
- repo path is `/Proxima`
- runtime user is `proxima`
- desired desktop display is `:2`

## 1. Install OS packages

```bash
apt-get update
apt-get install -y \
  xvfb \
  xfce4 \
  xfce4-goodies \
  x11vnc \
  novnc \
  websockify \
  xterm \
  dbus-x11
apt-get remove -y xfce4-screensaver || true
```

## 2. Clone repo and fix ownership

```bash
git clone https://github.com/alkindivv/Proxima /Proxima
id proxima >/dev/null 2>&1 || useradd -m -s /bin/bash proxima
chown -R proxima:proxima /Proxima
```

If the repo already exists, skip the clone and keep ownership correct.

## 3. Make Node global for non-root runtime

If Node exists only under root's nvm tree, copy or expose it globally. Example:

```bash
cp -a /root/.nvm/versions/node/v22.22.2 /opt/node-v22.22.2
ln -sf /opt/node-v22.22.2/bin/node /usr/local/bin/node
ln -sf /opt/node-v22.22.2/bin/npm /usr/local/bin/npm
ln -sf /opt/node-v22.22.2/bin/npx /usr/local/bin/npx
```

Verify:

```bash
runuser -u proxima -- node -v
runuser -u proxima -- npm -v
```

## 4. Install npm dependencies

```bash
runuser -u proxima -- bash -lc 'cd /Proxima && npm install'
```

## 5. Create Proxima config

Create directories:

```bash
runuser -u proxima -- mkdir -p /home/proxima/.config/proxima
runuser -u proxima -- mkdir -p /home/proxima/.config/autostart
```

Write `/home/proxima/.config/proxima/settings.json`:

```json
{
  "restApiEnabled": true,
  "chatgptEnabled": true,
  "claudeEnabled": true,
  "geminiEnabled": true,
  "perplexityEnabled": true
}
```

Write `/home/proxima/.config/autostart/xfce4-screensaver.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Disable XFCE Screensaver
Exec=/bin/true
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=false
```

## 6. Create launcher files

`/home/proxima/start-proxima.sh`:

```bash
#!/usr/bin/env bash
set -e
export DISPLAY=:2
export HOME=/home/proxima
export XDG_RUNTIME_DIR=/run/user/$(id -u)
cd /Proxima
exec /usr/local/bin/npm start
```

Then:

```bash
chmod +x /home/proxima/start-proxima.sh
chown proxima:proxima /home/proxima/start-proxima.sh
```

Optional desktop launcher `/home/proxima/Desktop/Start-Proxima.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Start Proxima
Exec=/home/proxima/start-proxima.sh
Terminal=false
```

## 7. Create GUI services

Get UID:

```bash
id -u proxima
```

Replace `<UID>` below.

### `/etc/systemd/system/proxima-user-xvfb.service`

```ini
[Unit]
Description=Proxima virtual X display
After=network.target

[Service]
User=proxima
Environment=HOME=/home/proxima
ExecStart=/usr/bin/Xvfb :2 -screen 0 1440x900x24 -nolisten tcp
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

### `/etc/systemd/system/proxima-user-xfce.service`

```ini
[Unit]
Description=Proxima XFCE desktop session
After=proxima-user-xvfb.service
Requires=proxima-user-xvfb.service

[Service]
User=proxima
Environment=DISPLAY=:2
Environment=HOME=/home/proxima
Environment=XDG_RUNTIME_DIR=/run/user/<UID>
ExecStartPre=/bin/mkdir -p /run/user/<UID>
ExecStartPre=/bin/chown proxima:proxima /run/user/<UID>
ExecStartPre=/bin/chmod 700 /run/user/<UID>
ExecStart=/usr/bin/startxfce4
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

### VNC password

Before x11vnc service, create password as user `proxima`:

```bash
runuser -u proxima -- x11vnc -storepasswd
```

### `/etc/systemd/system/proxima-user-x11vnc.service`

```ini
[Unit]
Description=Proxima x11vnc server
After=proxima-user-xfce.service
Requires=proxima-user-xfce.service

[Service]
User=proxima
Environment=DISPLAY=:2
Environment=HOME=/home/proxima
ExecStart=/usr/bin/x11vnc -display :2 -forever -shared -rfbauth /home/proxima/.vnc/passwd -rfbport 5902 -localhost
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

### `/etc/systemd/system/proxima-user-novnc.service`

```ini
[Unit]
Description=Proxima noVNC server
After=proxima-user-x11vnc.service
Requires=proxima-user-x11vnc.service

[Service]
User=root
ExecStart=/usr/share/novnc/utils/novnc_proxy --listen 127.0.0.1:6081 --vnc 127.0.0.1:5902
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

Enable services:

```bash
systemctl daemon-reload
systemctl enable --now proxima-user-xvfb.service
systemctl enable --now proxima-user-xfce.service
systemctl enable --now proxima-user-x11vnc.service
systemctl enable --now proxima-user-novnc.service
```

## 8. Create app service

`/etc/systemd/system/proxima-app.service`:

```ini
[Unit]
Description=Proxima Electron App
After=proxima-user-xfce.service
Requires=proxima-user-xfce.service

[Service]
User=proxima
WorkingDirectory=/Proxima
Environment=DISPLAY=:2
Environment=HOME=/home/proxima
Environment=XDG_RUNTIME_DIR=/run/user/<UID>
ExecStart=/usr/local/bin/npm start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
systemctl daemon-reload
systemctl enable --now proxima-app.service
```

If the app is started as root and fails with:

```text
Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
```

Fix it by running as `proxima`, not by loosening sandbox policy.

## 9. Create MCP wrapper

`/usr/local/bin/proxima-mcp`:

```bash
#!/usr/bin/env bash
exec /usr/sbin/runuser -u proxima -- /usr/local/bin/node /Proxima/src/mcp-server-v3.js
```

Then:

```bash
chmod +x /usr/local/bin/proxima-mcp
```

## 10. Validate on the server

Service status:

```bash
systemctl status proxima-user-xvfb.service --no-pager
systemctl status proxima-user-xfce.service --no-pager
systemctl status proxima-user-x11vnc.service --no-pager
systemctl status proxima-user-novnc.service --no-pager
systemctl status proxima-app.service --no-pager
```

Port check:

```bash
ss -ltnp | grep -E '(:5902|:6081|:3210|:19222)'
```

REST health:

```bash
curl http://127.0.0.1:3210/v1/models
```

MCP wrapper check:

```bash
/usr/local/bin/proxima-mcp
```

Expected early logs include:

```text
[MCP] Agent Hub MCP Server v3.0 starting...
[MCP] Connecting to Agent Hub on port 19222
[MCP] Connected to Agent Hub successfully
[MCP] MCP Server running
```
