# Platform Guide: Windows, Mac, and Linux

Project Trident runs on any platform that supports OpenClaw. This guide covers platform-specific paths, commands, and gotchas.

---

## Path Reference

| Platform | OpenClaw Workspace | LCM Database | Skills Directory |
|---|---|---|---|
| Linux | `~/.openclaw/workspace` | `~/.openclaw/lcm.db` | `~/.openclaw/skills/` |
| Mac (Homebrew) | `~/.openclaw/workspace` | `~/.openclaw/lcm.db` | `~/.openclaw/skills/` |
| Windows | `%USERPROFILE%\.openclaw\workspace` | `%USERPROFILE%\.openclaw\lcm.db` | `%USERPROFILE%\.openclaw\skills\` |
| VPS (root user) | `/root/.openclaw/workspace` | `/root/.openclaw/lcm.db` | `/root/.openclaw/skills/` |
| Docker container | `/home/node/.openclaw/workspace` | `/home/node/.openclaw/lcm.db` | `/home/node/.openclaw/skills/` |

**Important:** The `AGENT-PROMPT.md` template must use the absolute path for your platform. Hardcoded paths like `/data/.openclaw/workspace` (Shiva's VPS) will break on other systems.

**Always use the `OPENCLAW_WORKSPACE` environment variable when available:**
```bash
echo $OPENCLAW_WORKSPACE  # Check if set
```
If not set, use the absolute path for your platform.

---

## Linux

### Prerequisites
- Node.js ≥ 22.14.0
- npm ≥ 10.x
- OpenClaw installed globally: `npm install -g openclaw`

### Workspace Setup
```bash
# Create Layer 1 structure
cd ~/.openclaw/workspace
mkdir -p memory/{daily,semantic,self,lessons,projects,reflections,layer0}
touch MEMORY.md SESSION-STATE.md

# Copy Layer 0.5 template
cp ~/.openclaw/skills/project-trident/scripts/layer0-agent-prompt-template.md \
   ~/.openclaw/workspace/memory/layer0/AGENT-PROMPT.md

# Set workspace path in template
WORKSPACE=$(realpath ~/.openclaw/workspace)
sed -i "s|WORKSPACE_PATH|$WORKSPACE|g" \
    ~/.openclaw/workspace/memory/layer0/AGENT-PROMPT.md
```

### Docker (Optional — Semantic Recall Only)
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### Ollama (Optional — Zero-Cost Layer 0.5)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
```

### Git Backup (Optional)
```bash
cd ~/.openclaw/workspace
git init
git remote add origin git@github.com:yourusername/yourrepo.git
```

---

## Mac (macOS)

### Prerequisites
- Node.js ≥ 22.14.0 (recommended: install via `nvm` or `mise`)
- OpenClaw: `npm install -g openclaw`

### Install Node.js (if needed)
```bash
# Option A: nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 22
nvm use 22

# Option B: Homebrew
brew install node@22
```

### Workspace Setup
```bash
# Create Layer 1 structure
cd ~/.openclaw/workspace
mkdir -p memory/{daily,semantic,self,lessons,projects,reflections,layer0}
touch MEMORY.md SESSION-STATE.md

# Copy Layer 0.5 template
cp ~/.openclaw/skills/project-trident/scripts/layer0-agent-prompt-template.md \
   ~/.openclaw/workspace/memory/layer0/AGENT-PROMPT.md

# Set workspace path in template
WORKSPACE=$(realpath ~/.openclaw/workspace)
sed -i '' "s|WORKSPACE_PATH|$WORKSPACE|g" \
    ~/.openclaw/workspace/memory/layer0/AGENT-PROMPT.md
```

Note: Mac `sed` requires the empty string argument (`''`) after `-i`.

### Docker Desktop (Optional — Semantic Recall Only)
Download from: https://www.docker.com/products/docker-desktop/

After installation:
```bash
docker --version  # verify
```

### Ollama (Optional — Zero-Cost Layer 0.5)
Download from: https://ollama.com/download/mac
```bash
ollama pull qwen2.5:7b
```

---

## Windows

### Prerequisites
- Node.js ≥ 22.14.0 (download from https://nodejs.org)
- npm ≥ 10.x (bundled with Node.js installer)
- Git for Windows (recommended): https://git-scm.com/download/win
- PowerShell 7+ (recommended): https://aka.ms/powershell

### Install OpenClaw
```powershell
# In PowerShell (as Administrator)
npm install -g openclaw
```

### Workspace Setup (PowerShell)
```powershell
$ws = "$env:USERPROFILE\.openclaw\workspace"

# Create Layer 1 structure
New-Item -ItemType Directory -Force -Path "$ws\memory\daily"
New-Item -ItemType Directory -Force -Path "$ws\memory\semantic"
New-Item -ItemType Directory -Force -Path "$ws\memory\self"
New-Item -ItemType Directory -Force -Path "$ws\memory\lessons"
New-Item -ItemType Directory -Force -Path "$ws\memory\projects"
New-Item -ItemType Directory -Force -Path "$ws\memory\reflections"
New-Item -ItemType Directory -Force -Path "$ws\memory\layer0"
New-Item -ItemType File -Force -Path "$ws\MEMORY.md"
New-Item -ItemType File -Force -Path "$ws\SESSION-STATE.md"

# Copy Layer 0.5 template
$skillsPath = "$env:USERPROFILE\.openclaw\skills\project-trident\scripts\layer0-agent-prompt-template.md"
$dest = "$ws\memory\layer0\AGENT-PROMPT.md"
Copy-Item $skillsPath $dest

# Set workspace path in template (Windows-style path)
(Get-Content $dest) -replace 'WORKSPACE_PATH', $ws | Set-Content $dest
```

### Windows Path Note for AGENT-PROMPT.md

Windows uses backslashes in paths. When the Layer 0.5 agent reads its prompt, ensure paths use the correct format:

```
# In AGENT-PROMPT.md on Windows:
WORKSPACE_PATH = C:\Users\username\.openclaw\workspace
```

However, many tools (including OpenClaw internals) accept forward slashes on Windows. When in doubt, use forward slashes:
```
C:/Users/username/.openclaw/workspace
```

### Docker Desktop (Optional — Semantic Recall Only)
Download from: https://www.docker.com/products/docker-desktop/

Note: Docker Desktop requires WSL2 on Windows 10/11. Enable in PowerShell (as Admin):
```powershell
wsl --install
```

Then restart and install Docker Desktop.

### Ollama (Optional — Zero-Cost Layer 0.5)
Download from: https://ollama.com/download/windows
```powershell
ollama pull qwen2.5:7b
```

### Windows-Specific Gotchas

**Line endings (CRLF):** Windows uses `\r\n` by default. This can break shell scripts or `.md` files read by agents expecting Unix line endings. Configure Git to normalize:
```powershell
git config --global core.autocrlf input
```

**Long paths:** Windows has a 260-character path limit by default. Enable long paths:
```powershell
# As Administrator
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
```

**Firewall:** If running Qdrant locally (Port 6333), allow it through Windows Firewall:
```powershell
New-NetFirewallRule -DisplayName "Qdrant" -Direction Inbound -Protocol TCP -LocalPort 6333 -Action Allow
```

---

## VPS (Cloud Servers)

Most VPS providers (Hostinger, DigitalOcean, Linode, AWS EC2, etc.) run Ubuntu or Debian. Follow the Linux guide above with these additions:

### Fresh VPS Bootstrap
```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Verify
node --version  # should be ≥ 22.14.0

# Install OpenClaw
npm install -g openclaw

# Initialize
openclaw setup
```

### Root vs. Non-Root Users

Running as root (`/root/.openclaw/`) is common on VPS but carries security risks. Consider creating a dedicated user:

```bash
useradd -m -s /bin/bash openclaw
su - openclaw
npm install -g openclaw  # installs in user context
```

### Docker on VPS
```bash
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER
systemctl enable docker
systemctl start docker
```

### Persistent Layer 0.5 on VPS

OpenClaw cron jobs persist as long as the gateway daemon is running. Ensure it restarts on reboot:

```bash
# Create systemd service (if not already configured by OpenClaw setup)
openclaw gateway status  # check current status
```

---

## Qdrant Without Docker (All Platforms)

If Docker isn't available, run Qdrant as a standalone binary:

**Linux / Mac:**
```bash
# Download binary
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-musl.tar.gz | tar -xz
chmod +x qdrant

# Start with persistent storage
./qdrant --storage-path ~/.qdrant-storage
```

**Windows (PowerShell):**
```powershell
# Download binary
Invoke-WebRequest -Uri "https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-pc-windows-msvc.zip" -OutFile qdrant.zip
Expand-Archive qdrant.zip -DestinationPath .

# Start
.\qdrant.exe --storage-path "$env:USERPROFILE\.qdrant-storage"
```

**Or use Qdrant Cloud (no installation required):**
1. Create free account at https://qdrant.tech
2. Get API key + cluster URL
3. Configure in Trident (see `deployment-guide.md`)

---

## FalkorDB Without Docker (All Platforms)

FalkorDB runs as a Redis module. If Docker isn't available:

**Option A: Redis + FalkorDB module (Linux/Mac):**
```bash
# Install Redis
apt install redis-server  # Debian/Ubuntu
brew install redis         # Mac

# Download FalkorDB module
curl -L https://github.com/FalkorDB/FalkorDB/releases/latest/download/falkordb-linux-x64.so -o falkordb.so

# Start Redis with FalkorDB
redis-server --loadmodule ./falkordb.so
```

**Option B: FalkorDB Cloud:**
- Available at https://falkordb.com
- Free tier available

---

## Platform Compatibility Matrix

| Feature | Linux | Mac | Windows | VPS |
|---|---|---|---|---|
| Trident Lite (Layers 0, 0.5, 1) | ✅ | ✅ | ✅ | ✅ |
| Qdrant (Docker) | ✅ | ✅ | ✅* | ✅ |
| Qdrant (binary) | ✅ | ✅ | ✅ | ✅ |
| Qdrant Cloud | ✅ | ✅ | ✅ | ✅ |
| FalkorDB (Docker) | ✅ | ✅ | ✅* | ✅ |
| FalkorDB (Redis module) | ✅ | ✅ | ⚠️** | ✅ |
| FalkorDB Cloud | ✅ | ✅ | ✅ | ✅ |
| Ollama (local LLM) | ✅ | ✅ | ✅ | ✅*** |
| Git backup | ✅ | ✅ | ✅ | ✅ |

*Requires Docker Desktop + WSL2
**Redis native Windows build is experimental
***VPS Ollama requires sufficient RAM (8GB+ recommended)
