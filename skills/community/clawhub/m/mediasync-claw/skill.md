---
name: MediaSync-Claw
version: 1.0.1
description: A media file server that serves multimedia files with FRP support
author: OpenClaw User
type: workspace
language: python
entrypoint: media_server_flask.py
requires:
  bins:
    - python3
    - uv
  python:
    - "flask>=2.0.1"
    - "requests"
    - "jinja2"
    - "aiortc"
    - "flask-socketio"
triggers:
  - type: keyword
    values: ["playlist", "media list", "show videos", "list files", "media pocket", "my media", "video library", "media gallery"]
    url: "http://local.flask.service:8000/api/openclaw"
    method: "POST"

permissions:
  - filesystem:read
  - filesystem:write
  - network:listen
  - network:connect
  - process:execute
  - network:access:internal
  - network:access:internet
---

# MediaSync-Claw

## 💡 Gateway Mode Active
This skill operates entirely at the gateway level. When a user sends a matched keyword, OpenClaw bypasses the LLM and forwards the request directly to the Flask backend to achieve low latency (<50ms).

*Note: All response text formatting and custom error handling must be managed inside `media_server_flask.py`.*

## 🔒 Security & Network Disclosure

### ⚠️ Critical: FRP Tunnel Exposes Local Services to Public Internet
This skill **automatically** downloads and runs the **FRP (Fast Reverse Proxy) client (`frpc`)** upon startup. The `frpc` binary is fetched from GitHub Releases and establishes an outbound tunnel to a remote FRP server (`129.213.174.213:7000`), which in turn exposes your local media service (port 8000) to the **public internet** via a `*.yunfrp.net` subdomain.

**This materially expands your attack surface.** Anyone who knows or discovers the public subdomain can attempt to access your media files and the Flask service running on your machine.

### 1. Automatic Tunnel Behavior (No User Opt-in)
* **Automatic on Startup**: The FRP tunnel starts automatically when `media_server_flask.py` runs. There is no prompt, no confirmation, and no environment-variable gate.
* **Binary Download**: On first run, `frpc.exe` is downloaded silently from GitHub (`fatedier/frp` releases). Internet access is required.
* **No Inbound Firewall Changes**: The tunnel is outbound-only; no inbound ports need to be opened on your firewall.

### 2. Supply-Chain Risk: Downloaded Binary Execution
* The skill downloads and executes a native binary (`frpc.exe`) from GitHub Releases. Compromise of the GitHub repository, the release artifact, or the network transport (MITM) could result in **arbitrary code execution** on your host with the same privileges as the Python process.
* **Pinned SHA256 Verification**: The code includes hardcoded SHA256 checksums for both the zip archive and the extracted `frpc.exe` binary (version `0.65.0`). The download is rejected if either checksum does not match. This defends against transport tampering and corrupted downloads, but **does not protect against a compromise of the upstream GitHub repository or release**.
* **Version-Locked**: The FRP version is pinned at `0.65.0`. Upgrading requires a code change and SHA256 re-verification. This prevents silent upgrades to potentially compromised newer versions.

### 3. Authentication Status
* **No Authentication Implemented**: The Flask server currently has **no HTTP Basic Auth, no token mechanism, and no access control**. All API routes and media endpoints are publicly accessible to anyone who reaches the server — whether via LAN or the FRP tunnel.
* **Risk**: An unauthenticated third party who discovers the `*.yunfrp.net` subdomain can enumerate and download media files from your machine.

### 4. Remote Server Trust
* The FRP server at `129.213.174.213:7000` is a third-party relay. All traffic between the public internet and your local service passes through this server.
* The FRP tunnel operates in HTTP mode (no TLS termination by FRP server).
* You must trust that this FRP server operator will not inspect, log, or tamper with your traffic.

