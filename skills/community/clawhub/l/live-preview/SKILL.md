---
name: live-preview
version: 1.0.6
description: Share a live preview of a website under development via aitun tunnel, with hot-reload support so users see changes in real time as you edit. Perfect for AI agents that iteratively build or modify websites and need user feedback.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "👀"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/live-preview
---

# Live Preview - Share Real-Time Website Preview via Aitun Tunnel

## When to Use

Use this skill when:
- You are iteratively building or modifying a website and want the user to see live changes
- You need user feedback on a design while you continue editing
- You are prototyping a UI and want to share each iteration instantly
- You are debugging a web application and need the user to confirm fixes in real time
- You want to demo a development workflow where changes appear live

Do NOT use this skill when:
- The website is already deployed to a public server
- You only need a one-time share (use aitun-tunnel instead)
- The content is a static file that does not change (use sendfile instead)

## Instructions

### Step 1: Install aitun

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Or verify it is already installed:

```bash
which aitun
```

### Step 2: Start the development server

Start the local dev server with hot-reload enabled. The command depends on your framework:

```bash
# For a static HTML directory (use a live-reload tool)
pip install livereload
python3 -c "
from livereload import Server, shell
server = Server()
server.watch('/path/to/html/dir')
server.serve(root='/path/to/html/dir', port=8080)
" &
DEV_PID=$!
sleep 2

# For Next.js
npm run dev -- -p 8080 &

# For Vite
npx vite --port 8080 --host &

# For Flask
flask run --port 8080 --host 0.0.0.0 &

# For any HTTP server (no auto-reload)
python3 -m http.server 8080 --directory /path/to/html/dir &
```

### Step 3: Create a tunnel

Expose the dev server to the internet:

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123`

### Step 4: Share the preview link with the user

```
Your live preview is ready: https://aitun.cc/abc123

I'm still working on it — just refresh the page to see my latest changes.
This preview link will remain active while I'm editing.
```

### Step 5: Iterate and update

Continue editing files in your project directory. As you save changes:
- If using a hot-reload dev server: the user's browser will auto-refresh
- If using a basic HTTP server: tell the user to refresh the page manually

After each significant change, notify the user:

```
I've updated the navigation bar — refresh the page to see it.
```

### Step 6: Clean up

When the preview session is complete, stop the servers:

```bash
kill $AITUN_PID 2>/dev/null
kill $DEV_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- For a permanent preview subdomain, register at https://aitun.cc
- Hot-reload works best with frameworks that support it natively (Vite, Next.js, etc.)
- For static files, use Python's `livereload` package to enable auto-refresh
- The tunnel stays active as long as the aitun process is running — no need to restart the tunnel when files change
- All traffic is encrypted end-to-end
