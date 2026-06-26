<!--
Windows-specific install notes. v2.6 originally documented uv-based
in-process install; v4.x is dockerized so most of these notes apply to
the Docker Desktop + WSL2 path now. Key v4.x adaptations: replace any
"investorclaw" CLI references with calls through the MCP server at
localhost:18090; replace "~/portfolios" with the bind-mounted
"./portfolios" under your compose project.
-->

# Windows Setup Guide for InvestorClaw

## Overview

This guide covers InvestorClaw setup on Windows systems, including OpenClaw, Claude Code, WSL, and local inference engines (LMStudio, Ollama, llama-server).

## Network Architecture Patterns

### Pattern 1: Local Machine (Native Windows)
```
OpenClaw/Claude Code (Windows)
        ↓
   LMStudio (Windows port 8000)
```
- Endpoint: `http://localhost:8000`
- Requirements: API Server enabled, no special networking

### Pattern 2: WSL + Windows LMStudio
```
OpenClaw/Claude Code (WSL)
        ↓ (remote network)
   LMStudio (Windows port 8000, bind 0.0.0.0)
```
- Endpoint: `http://172.31.x.x:8000` (WSL → Windows host IP)
- Requirements: 0.0.0.0 binding, CORS, firewall rules

### Pattern 3: Separate Windows Machines
```
OpenClaw (Windows Machine A)
        ↓ (network)
   LMStudio (Windows Machine B port 8000, bind 0.0.0.0)
```
- Endpoint: `http://192.168.x.x:8000` (Machine B IP)
- Requirements: 0.0.0.0 binding, CORS, firewall rules, network connectivity

## LMStudio Configuration for Remote Access

### Step 1: Enable API Server (Required for All)

1. Open **LMStudio**
2. Go to **Settings** (gear icon)
3. Navigate to **Developer** tab
4. Toggle **"Enable API Server"** to ON
5. Go to **Developer** → **Local Server**
6. Verify port (default 8000)
7. Click "Start Local Server"

### Step 2: Configure Network Binding (Windows/WSL Only)

For access from WSL or other machines:

1. In LMStudio: **Settings** → **Developer** → **Local Server Settings**
2. Change "Network" dropdown from `127.0.0.1` to `0.0.0.0`
3. This allows connections from any network interface
4. **Important:** Restart the local server after changing binding

**What does each binding mean:**
- `127.0.0.1` — localhost only (same machine)
- `0.0.0.0` — all interfaces (accept connections from anywhere)

### Step 3: Enable CORS (Windows/WSL Only)

For cross-origin requests:

1. In LMStudio: **Settings** → **Developer**
2. Toggle **"CORS"** to ON
3. This allows requests from different origins (e.g., WSL container)

### Step 4: Windows Firewall Rules

Add exception for LMStudio port using **PowerShell (as Administrator)**:

```powershell
# Add LMStudio to Windows Firewall (port 8000)
New-NetFirewallRule -DisplayName "LMStudio API" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 8000

# Verify it was added
Get-NetFirewallRule -DisplayName "LMStudio API" | Format-List

# To remove later:
Remove-NetFirewallRule -DisplayName "LMStudio API"
```

**Or via GUI:**
1. Open **Windows Defender Firewall** (search in Windows)
2. Click **"Allow an app through firewall"**
3. Click **"Change settings"** button
4. Click **"Allow another app"**
5. Browse to LMStudio executable
6. Click **"Add"**
7. Verify port 8000 is listed

### Step 5: InvestorClaw Configuration

**For local machine:**
```bash
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://localhost:8000
export INVESTORCLAW_CONSULTATION_MODEL=gemma-4-9b-instruct
```

**For WSL (connecting to Windows LMStudio):**
```bash
# Find Windows host IP
cat /etc/resolv.conf
# Look for line like: nameserver 172.31.x.x

# Set endpoint to Windows host IP
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://172.31.x.x:8000
export INVESTORCLAW_CONSULTATION_MODEL=gemma-4-9b-instruct
```

**For remote machine:**
```bash
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://192.168.x.x:8000
export INVESTORCLAW_CONSULTATION_MODEL=gemma-4-9b-instruct
```

## WSL-Specific Configuration

### Finding Windows Host IP from WSL

```bash
# Method 1: From /etc/resolv.conf
cat /etc/resolv.conf | grep nameserver
# Output: nameserver 172.31.x.x (this is Windows host IP)

# Method 2: Using ip command
ip route show | grep default | awk '{print $3}'
# Output: 172.31.x.x (this is Windows host IP)

# Test connectivity to Windows host
ping 172.31.x.x  # Should work if WSL can reach Windows
```

### WSL Firewall Considerations

Windows Firewall applies to WSL containers. If connections fail:

1. Verify firewall rule exists (see PowerShell commands above)
2. Ensure LMStudio binding is `0.0.0.0` (not `127.0.0.1`)
3. Test from WSL: `curl http://172.31.x.x:8000/health`
4. Should return HTTP 200 if working

## Troubleshooting

### "Connection refused" / "No route to host"

| Cause | Check | Fix |
|-------|-------|-----|
| LMStudio not running | Task Manager → look for LMStudio | Start LMStudio |
| API Server not enabled | LMStudio > Settings > Developer | Toggle "Enable API Server" ON |
| Wrong network binding | LMStudio > Settings > Developer > Local Server | Change to `0.0.0.0` |
| Firewall blocking | Windows Firewall settings | Add exception for port 8000 |
| WSL using wrong IP | `cat /etc/resolv.conf` | Use correct Windows host IP |

### "HTTP 400" / "HTTP 422"

| Cause | Check | Fix |
|-------|-------|-----|
| CORS not enabled | LMStudio > Settings > Developer | Toggle "CORS" ON |
| Wrong model name | LMStudio UI (loaded model name) | Use exact model name from UI |
| Invalid request format | API request payload | Check for syntax errors |

### "HTTP 500" / "CORS error"

| Cause | Check | Fix |
|-------|-------|-----|
| Model not loaded | LMStudio main UI | Load a model before API calls |
| CORS not enabled | LMStudio > Settings > Developer | Toggle "CORS" ON |
| GPU memory full | System GPU usage | Reduce max_tokens or restart LMStudio |

### No response or timeout

| Cause | Check | Fix |
|-------|-------|-----|
| Network unreachable | `ping 172.31.x.x` (WSL) or `ping 192.168.x.x` | Check network connectivity |
| Firewall blocking | Windows Firewall rules | Add port 8000 exception |
| LMStudio overloaded | LMStudio UI → System Resources | Restart LMStudio or reduce load |

## Command Line Verification

Test your setup before configuring InvestorClaw:

```powershell
# From Windows (native) or WSL

# Test connection
curl http://localhost:8000/health      # Local machine
curl http://172.31.x.x:8000/health     # From WSL to Windows
curl http://192.168.x.x:8000/health    # From remote machine

# Check available models
curl http://localhost:8000/v1/models

# Test chat completions (manual API call)
curl -X POST http://localhost:8000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -d @- << 'EOF'
{
  "model": "gemma-4-9b-instruct",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}
EOF
```

## Performance Notes

### Windows vs WSL Performance

- **Native Windows**: Full GPU access, best performance
- **WSL2**: Good GPU access via Direct3D, slightly slower than native
- **WSL1**: No GPU support, uses CPU only (slow)

### Optimize for Windows

1. Use WSL2 (not WSL1) if possible
2. Allocate GPU memory in LMStudio settings
3. Monitor Task Manager > Performance > GPU utilization
4. Consider quantized models (Q6_K, Q8_0) for better VRAM usage

## Security Considerations

### ⚠️ WARNING: 0.0.0.0 Binding

Setting network binding to `0.0.0.0` exposes your LLM to any device that can reach your machine on the network.

**Security implications:**
- Any device on your network can use your LMStudio GPU
- Potential for resource exhaustion or abuse
- No authentication by default

**Recommendations:**
- Use only on **trusted networks** (home network with family devices)
- Do NOT expose to the internet (no port forwarding from router)
- Consider firewall rules to restrict access to specific IPs
- Use VPN if accessing from untrusted networks

**Restrict firewall rule to specific IP:**
```powershell
# Allow only from specific machine (198.51.100.100)
New-NetFirewallRule -DisplayName "LMStudio API (Restricted)" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 8000 `
  -RemoteAddress 198.51.100.100
```

## Ollama on Windows

Ollama also works on Windows with similar requirements:

```bash
# Port: 11434 (default)
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://localhost:11434
export INVESTORCLAW_CONSULTATION_MODEL=gemma:7b

# For remote access: set binding to 0.0.0.0 in Ollama settings
# For WSL: use Windows host IP like WSL pattern above
```

## llama-server on Windows

Not officially supported on Windows, but can work via WSL:

```bash
# In WSL:
brew install llama.cpp  # (if on WSL Ubuntu)
llama-server -m ~/models/gemma-4.gguf --port 8080

# From Windows/WSL:
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://localhost:8080  # (native WSL)
export INVESTORCLAW_CONSULTATION_ENDPOINT=http://172.31.x.x:8080  # (from Windows)
```

## Summary Checklist

For Windows + LMStudio + WSL setup:

- [ ] LMStudio installed and running
- [ ] Settings > Developer > Enable API Server = ON
- [ ] Settings > Developer > Local Server Network = 0.0.0.0
- [ ] Settings > Developer > CORS = ON
- [ ] Windows Firewall rule added for port 8000
- [ ] Windows host IP identified from WSL (`cat /etc/resolv.conf`)
- [ ] InvestorClaw endpoint set to `http://172.31.x.x:8000`
- [ ] Model name matches exactly what LMStudio shows
- [ ] Test: `curl http://172.31.x.x:8000/health` returns 200

---

**Last Updated:** 2026-04-18  
**Status:** Production Ready

For additional help, see `docs/LOCAL_INFERENCE_GUIDE.md` for other inference engines and advanced configurations.
