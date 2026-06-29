# Setup and Pre-Flight

Full pre-flight protocol for music-craft: dependency consent, platform
detection, user and hardware setup, required and optional dependencies,
and install details. Load this before the first generation in a session,
or when any dependency or hardware question comes up.

## Dependency Consent Protocol

Some setups (local models, audio analysis) need installs, large downloads, or
certificate/proxy configuration. Apply this protocol every time:

- Label every dependency as **REQUIRED** (the chosen path will not work without it) or
  **OPTIONAL** (it works without, quality improves with it). Say which when you ask.
- **Stop and ask before any install or multi-GB download.** Show the exact command and its
  rough size/impact. Never auto-install; never silently fall back to a degraded path.
- If the user declines a REQUIRED item, stop and say plainly that the chosen path cannot
  proceed, then offer an alternative (for example cloud vs local).
- **Ask once, up front, where to save output** (`OUTPUT_DIR`) and use a per-song subfolder.
  Do not invent an output path silently.
- For local models on Windows, follow [`windows-wsl-setup.md`](windows-wsl-setup.md),
  which encodes these gates for the WSL2 path.

## Platform Detection (run first)

Identify the host OS so the install commands later use the right package manager.

```bash
# POSIX (Linux, macOS, WSL, Git Bash)
uname -s    # "Linux" or "Darwin"

# Windows PowerShell
$env:OS     # "Windows_NT"

# Windows cmd
ver
```

Then identify the available package manager (in priority order):

| OS | Package managers (in priority order) |
|---|---|
| Ubuntu / Debian / Mint | `apt` |
| Fedora / RHEL / Rocky | `dnf` (legacy: `yum`) |
| Arch / Manjaro | `pacman` |
| Alpine | `apk` |
| macOS | `brew` (install from [brew.sh](https://brew.sh) if missing) |
| Windows | `winget` (built into Windows 10 2004+), then `choco` (Chocolatey), then `scoop` |

A useful one-liner to detect the active manager:

```bash
# POSIX
command -v apt dnf pacman apk brew 2>/dev/null | head -1

# Windows PowerShell
Get-Command winget, choco, scoop -ErrorAction SilentlyContinue | Select-Object -First 1
```

If the agent is running inside WSL, treat it as Linux (use `apt`). If it is running inside a non-standard environment (container, Codespace, dev container), ask the user which base image they are on before proposing install commands.

## User & Hardware Setup (ask once per session)

Before installing any backend, gather the user's preferences and confirm hardware. The skill works on **any** modern machine — not just Apple Silicon MacBooks. Auto-detect first, then confirm critical values with the user.

### Hardware Probe (run first)

Run this on the user's machine to detect platform, RAM, disk, and existing installs:

```bash
echo "=== Platform ==="
uname -srm

echo ""
echo "=== RAM ==="
case "$(uname -s)" in
  Darwin) sysctl -n hw.memsize | awk '{printf "%.0f GB\n", $1/1024/1024/1024}' ;;
  Linux)  awk '/MemTotal/{printf "%.0f GB\n", $2/1024/1024}' /proc/meminfo ;;
  *)      echo "unknown (Windows: run systeminfo | findstr Memory)" ;;
esac

echo ""
echo "=== CPU chip ==="
case "$(uname -s)" in
  Darwin) sysctl -n machdep.cpu.brand_string 2>/dev/null ;;
  Linux)  grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs ;;
  *)      echo "unknown" ;;
esac

echo ""
echo "=== GPU ==="
if [ "$(uname -m)" = "arm64" ] && [ "$(uname -s)" = "Darwin" ]; then
  echo "Apple Silicon (MPS available for MLX)"
elif command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null
else
  echo "No GPU detected (CPU only)"
fi

echo ""
echo "=== Disk free in \$HOME ==="
df -h "$HOME" | tail -1

echo ""
echo "=== Python managers ==="
command -v uv    >/dev/null 2>&1 && echo "uv:     $(which uv)" || echo "uv:     not found"
command -v conda >/dev/null 2>&1 && echo "conda:  $(which conda)" || echo "conda:  not found"
command -v python3 >/dev/null 2>&1 && echo "python3: $(python3 --version 2>&1)" || echo "python3: not found"

echo ""
echo "=== Existing ACE-Step install? ==="
ls ~/ACE-Step-1.5 2>/dev/null >/dev/null && echo "✓ Found at ~/ACE-Step-1.5" || echo "✗ Not found in ~/ACE-Step-1.5"
```

**Windows note:** the probe above is bash (POSIX) and cannot run on native Windows
before WSL exists. Run this PowerShell probe first (full walkthrough in
[`windows-wsl-setup.md`](windows-wsl-setup.md)):

```powershell
(Get-CimInstance Win32_OperatingSystem).Caption
[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)  # RAM GB
(Get-CimInstance Win32_Processor).Name
(Get-CimInstance Win32_VideoController).Name                                      # GPUs
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) { 'nvidia-smi present' }
wsl --list --verbose; wsl --version                                              # WSL state
Get-PSDrive C | Select-Object @{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}}
```
Once inside a WSL distro, the bash probe applies (WSL is treated as Linux).

### Ask the user (4 questions, in order)

After running the probe, present the detected values to the user and ask 4 questions. These answers stay in the session context and are reused for every backend install in this session.

**Question 1 — Platform confirmation:**

> I see: `{platform}, {ram} GB RAM, {cpu}, {gpu}`. Is that right?
> - ✅ Yes, continue
> - ❌ No, let me correct it (RAM/GPU/etc.)

If the user says no, ask which value is wrong and re-detect with corrections.

**Question 2 — Clone location for ACE-Step (and any other large model repo):**

> Where should I clone ACE-Step? Common choices:
> - `~/ACE-Step-1.5` (default, simple, no path collision)
> - `~/projects/ace-step` (if you keep projects in a subfolder)
> - `~/ml/ace-step` (if you have a dedicated ML directory)
> - A custom path: ___________
>
> If ACE-Step is already cloned somewhere, I detected it at: `{detected_path}`. Use that? Or pick a different path?

Use the user's answer as `ACE_STEP_PATH` for the rest of the session. Never hardcode absolute user-specific paths.

**Question 3 — Output directory for generated songs:**

> Where should I save generated songs and project files?
> - `~/Music mix/` (default)
> - A custom path: ___________
>
> I'll create the directory if it doesn't exist.

Use the user's answer as `OUTPUT_DIR` for the rest of the session.

**Question 4 — Cloud backends (optional, for backup or speed):**

> Do you have any of these set up? (Just for backup if ACE-Step fails)
> - MiniMax API key (set `MINIMAX_API_KEY` in your shell)
> - Stability AI API key (set `STABILITY_API_KEY`)
> - No, just use local backends
>
> You can always set these later.

### Hardware-specific notes (referenced later)

After the user answers Question 1, the skill knows the hardware. Save these flags for the rest of the session:

- `IS_APPLE_SILICON` = true if `uname -m` = `arm64` AND `uname -s` = `Darwin`
- `IS_INTEL_MAC` = true if `uname -m` = `x86_64` AND `uname -s` = `Darwin`
- `IS_LINUX_NVIDIA` = true if `nvidia-smi` works
- `IS_LINUX_AMD` = true if `rocm-smi` works (not yet handled)
- `IS_CPU_ONLY` = true if no GPU
- `RAM_GB` = total system RAM (24, 16, 32, 64, etc.)
- `MEMORY_ARCH` = "unified" (Apple Silicon, integrated graphics, AMD APU) OR "dedicated" (NVIDIA/AMD discrete GPU)
- `ML_BUDGET_GB` = how much memory is actually available for ML models (= free RAM minus 2 GB safety margin, or the smaller of free system + free VRAM for dedicated GPUs)
- `GPU_VRAM_GB` = total VRAM if dedicated GPU detected
- `GPU_FREE_GB` = free VRAM right now if dedicated GPU detected

These flags affect:
- **Backend selection** — Apple Silicon gets ACE-Step (MLX). Intel Mac / NVIDIA Linux get ACE-Step (CUDA, slower on consumer GPUs). CPU-only gets ACE-Step (CPU, very slow) or cloud backends.
- **Tier availability** — see the ML-budget tier table in the **ACE-Step Quality Tiers** section of [`acestep-generation.md`](acestep-generation.md).
- **Install commands** — see the per-OS install blocks in **Required** below.

**Apple Silicon note:** M1/M2/M3/M4 all work with ACE-Step MLX backend. M3 Pro/Max/Ultra and M4 are faster but otherwise identical. No code changes needed across chips. **Memory architecture: unified** — your 24 GB is shared between the OS, your apps, and the ML model. A 24 GB MacBook with 4 GB of open apps has ~20 GB ML budget, not 24 GB. This is why xl-mixed (which needs ~25-30 GB peak) hits swap-thrashing on 24 GB Macs. On a 32 GB Mac Mini or 64 GB Mac Studio, the same model fits comfortably.

**Intel Mac note:** ACE-Step MLX backend requires Apple Silicon. On Intel Macs, ACE-Step runs on CPU only (very slow, ~10x slower than MLX) or PyTorch with MPS (which is also limited on Intel). Recommend **cloud backends** (MiniMax, Stable Audio) for Intel Mac users who want reasonable speed. MusicGen still works fine on Intel Mac. **Memory architecture: unified** (Intel iGPU shares system RAM, same caveat as Apple Silicon).

**Linux + NVIDIA note:** ACE-Step on Linux uses CUDA. Needs NVIDIA driver + CUDA toolkit. Generation is faster than Apple Silicon MLX for high-end GPUs (RTX 4090, A100), slower for low-end (RTX 3050, GTX 1660). **Memory architecture: dedicated** — VRAM is separate from system RAM, so a 12 GB GPU + 16 GB system can still run a 10 GB model (VRAM is the bottleneck, not system RAM). The probe script detects this and uses the smaller pool as the ML budget.

**Windows note:** Run local ACE-Step via **WSL2** (treated as Linux, with CUDA passthrough to your NVIDIA GPU), not native Windows. On managed or proxied networks, model downloads may need certificate/proxy configuration — see [`windows-wsl-setup.md`](windows-wsl-setup.md). Cloud backends are the no-WSL alternative.

## Required

Before starting, detect **any** available music backend. Check in this priority order — use the first one that succeeds:

| Priority | Backend | Detection command | What it needs |
|---|---|---|---|
| 1 | Native tool | Inspect runtime's tool list for `music_generate` or similar | None — built into runtime |
| 2 | ACE-Step local (free, best quality) | `curl -s http://127.0.0.1:8001/health 2>/dev/null` returns `{"status":"ok"}` | `git clone` + `uv sync` + `uv run acestep-api` (REST API on port 8001) |
| 3 | MusicGen local (free, instrumental only) | `python3 -c "import audiocraft" 2>/dev/null && echo OK` | Conda or pip env with audiocraft + torch + xformers |
| 4 | mmx CLI (MiniMax) | `which mmx 2>/dev/null` | MiniMax API key in environment |
| 5 | Stable Audio REST | `[ -n "$STABILITY_API_KEY" ] && echo OK` | `STABILITY_API_KEY` env var |
| 6 | Any other CLI | `which mmx 2>/dev/null`, etc. | Provider-specific setup |

Run all detection checks. You only need **one** working backend. The skill adapts to whatever it finds.

If **no** backend is found after checking all paths, **branch on detected hardware** and present the right install path. Use the `ACE_STEP_PATH` and `OUTPUT_DIR` from the User & Hardware Setup answers.

### Apple Silicon (`IS_APPLE_SILICON = true`)

> No music generation backend detected. The quickest free path is ACE-Step local — it supports vocals, lyrics, and up to 10-minute songs with no API key and no quota limits.
>
> **Install ACE-Step (Apple Silicon, MLX native):**
> ```bash
> git clone https://github.com/ace-step/ACE-Step-1.5.git "${ACE_STEP_PATH}"
> cd "${ACE_STEP_PATH}" && uv sync
> uv run acestep-api --port 8001
> ```
> On first launch, the API server starts in "no models loaded" state. The skill will ask before downloading any models (see the **Model download consent flow** in the ACE-Step Quality Tiers section of [`acestep-generation.md`](acestep-generation.md)). REST API runs on `http://127.0.0.1:8001`.
>
> **Alternative — MusicGen (instrumental only):**
> ```bash
> brew install miniforge
> conda create -n musicgen -c conda-forge python=3.11 audiocraft torch torchaudio xformers
> conda activate musicgen
> ```

### Intel Mac (`IS_INTEL_MAC = true`)

> No music generation backend detected. ACE-Step MLX is **not supported** on Intel Macs. Your options:
>
> **Option A — Cloud backends (recommended for speed):**
> - MiniMax: set `MINIMAX_API_KEY` in your shell, install `mmx` CLI
> - Stable Audio: set `STABILITY_API_KEY` in your shell
>
> **Option B — ACE-Step on CPU (slow, ~10x slower than MLX):**
> ```bash
> git clone https://github.com/ace-step/ACE-Step-1.5.git "${ACE_STEP_PATH}"
> cd "${ACE_STEP_PATH}" && uv sync
> uv run acestep-api --port 8001
> # No MLX backend on Intel — generation will use CPU, expect ~60 min/track
> ```
>
> **Option C — MusicGen (instrumental only, fine on Intel):**
> ```bash
> brew install miniconda
> conda create -n musicgen -c conda-forge python=3.11 audiocraft torch torchaudio xformers
> conda activate musicgen
> ```

### Linux + NVIDIA GPU (`IS_LINUX_NVIDIA = true`)

> No music generation backend detected. The quickest free path is ACE-Step with CUDA.
>
> **Install ACE-Step (CUDA):**
> ```bash
> git clone https://github.com/ace-step/ACE-Step-1.5.git "${ACE_STEP_PATH}"
> cd "${ACE_STEP_PATH}" && uv sync
> uv run acestep-api --port 8001
> ```
> Requires NVIDIA driver + CUDA toolkit. Generation speed depends on GPU tier (see Linux + NVIDIA note above).
>
> **Alternative — MusicGen (instrumental only):**
> ```bash
> # Conda (preferred):
> conda create -n musicgen -c conda-forge python=3.11 audiocraft torch torchaudio xformers
> conda activate musicgen
> # Or venv + pip (CUDA required):
> python3 -m venv ~/musicgen-env
> source ~/musicgen-env/bin/activate
> pip install audiocraft torch torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```

### Linux (CPU only or AMD GPU)

> No NVIDIA GPU detected. ACE-Step will run on CPU (very slow, expect ~60-90 min/track). For better performance, consider:
> - **Cloud backends** (MiniMax, Stable Audio) — fast, paid
> - **MusicGen** — CPU-capable for shorter instrumentals
> - **Buy a GPU** 😄 (or borrow a cloud instance with NVIDIA)

### Windows

> Local ACE-Step on **native** Windows is not recommended (bash setup scripts; the
> LM backend path is built for Linux). The supported local path is **WSL2**, which
> gives a real Linux with CUDA passthrough to your NVIDIA GPU. The full, verified
> walkthrough — including certificate/proxy troubleshooting for managed
> networks — is in [`windows-wsl-setup.md`](windows-wsl-setup.md).
>
> **Option A — WSL2 (recommended for local generation):**
> 1. Probe with PowerShell (see the Windows note under Hardware Probe) and read `wsl --list --verbose`.
> 2. Create a **dedicated, isolated** distro. Never reuse or modify an existing
>    managed distro, and never edit the global `%USERPROFILE%\.wslconfig`:
> ```powershell
> wsl --install Ubuntu-24.04 --name acestep --no-launch
> ```
> 3. Verify GPU passthrough: `wsl -d acestep -u root -- nvidia-smi`. Then follow the
>    Linux + NVIDIA install steps inside the distro.
> 4. On a managed or proxied machine, do the CA-install and proxy-bypass steps in
>    `windows-wsl-setup.md` **before** downloading models.
>
> **Option B — Cloud backends (fast, paid):**
> - MiniMax: set `MINIMAX_API_KEY` and install `mmx`
> - Stable Audio: set `STABILITY_API_KEY`
>
> **Option C — MusicGen (instrumental only):**
> ```powershell
> winget install Anaconda.Miniconda3
> conda create -n musicgen -c conda-forge python=3.11 audiocraft torch torchaudio xformers
> conda activate musicgen
> ```

After any install method, verify: `python3 -c "import audiocraft; print('MusicGen ready')"` (for MusicGen) or `curl -s http://127.0.0.1:8001/health` (for ACE-Step).

Other options: install `mmx` CLI, or set `STABILITY_API_KEY` for Stable Audio API.

Do not start the workflow loop without a backend.

## MusicGen Installation Details

MusicGen's dependency chain has a known blocker: **`xformers` cannot build from source on macOS without conda** (it requires CUDA build tools that don't exist outside Linux/nvidia). This is why conda/miniforge is the recommended path on macOS.

**Why not plain `pip install audiocraft torch`?**

```
audiocraft → requires xformers
xformers   → requires CUDA build tools
macOS      → no CUDA → build fails
conda      → ships pre-built xformers wheels for all platforms ✓
```

**If conda is NOT available and the user refuses to install it**, fall back to any cloud backend (mmx, Stable Audio). Do not attempt a broken pip install chain.

**Verification (run after any install method):**

```bash
python3 -c "
import audiocraft
import torch
print(f'MusicGen {audiocraft.__version__} OK')
print(f'torch {torch.__version__}, CUDA: {torch.cuda.is_available()}')
print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU only\"}')
"
```

If this prints without error, MusicGen is ready. The agent should cache the activation command (e.g., `conda activate musicgen`) and use it for every MusicGen generation call in the session.

## Optional improvements

This skill does not require any optional tool, but the user may benefit from any of these. Ask once at the start of the workflow, before generating anything. Propose the install command for the **detected platform** using the table below.

| Tool | What it unlocks | Linux (apt/dnf/pacman/apk) | macOS (brew) | Windows (winget / choco) | Pip fallback (any OS) |
|---|---|---|---|---|---|
| `ffmpeg` | Audio format conversion, trimming, re-encoding | `apt install ffmpeg` (Debian/Ubuntu) · `dnf install ffmpeg` (Fedora) · `pacman -S ffmpeg` (Arch) · `apk add ffmpeg` (Alpine) | `brew install ffmpeg` | `winget install Gyan.FFmpeg` (or `choco install ffmpeg`) | — |
| `yt-dlp` | YouTube download for cover or mashup inputs | `apt install yt-dlp` (or pip) | `brew install yt-dlp` (or pip) | `winget install yt-dlp` (or `choco install yt-dlp` or pip) | `pip install -U yt-dlp` |
| `demucs` | Local stem separation for arranger experiments via `scripts/extract_stems.py` | pip | pip | pip | `pip install demucs` |
| `audiocraft` | **MusicGen local generation (free, no API key, no quota)** | conda (preferred) or pip | **conda (preferred):** `brew install miniforge` then `conda create -n musicgen -c conda-forge python=3.11 audiocraft torch torchaudio xformers` | Same as Linux | — | `pip install audiocraft torch` (may fail on macOS without conda — xformers build issue) |
| `librosa` | Audio analysis (BPM, key, energy, structure) | pip | pip | pip | `pip install librosa numpy scipy` |
| `parselmouth` | Better pitch tracking (optional, Praat under the hood) | pip | pip | pip | `pip install praat-parselmouth` |
| `mmx` CLI | Per-flag control (`--avoid`, `--bpm`, `--key`, `--structure`) with MiniMax | follow the MiniMax install guide for Linux | follow the MiniMax install guide for macOS | follow the MiniMax install guide for Windows (PowerShell) | — |
| `python3` | Required for `audiocraft`, `librosa`, and `parselmouth` | `apt install python3 python3-pip` · `dnf install python3 python3-pip` · `pacman -S python python-pip` · `apk add python3 py3-pip` | `brew install python` (ships pip) | `winget install Python.Python.3.12` | — |

### Python interpreter quirk

On Linux and macOS, the interpreter is usually `python3`. On Windows, it is usually `python` (no `3`). When verifying, check both names so Windows users are not falsely reported as missing Python:

```bash
# POSIX
command -v python3 || command -v python

# Windows PowerShell
Get-Command python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1
```

## The "ask the user" pattern

For each missing optional tool, present three options:

1. **Install** — propose the exact command **for the detected platform**, let the user approve through the agent's approval flow. The LLM does not auto-install.
2. **Skip** — proceed without it, use the simple prompt-only path.
3. **Cancel** — stop the workflow. Do not generate anything until the tools are sorted.

Do not auto-install. Do not silently fall through to a degraded path without confirmation. The user is in control of their machine.

For local arranger experiments, `scripts/extract_stems.py` requires Demucs and
`scripts/remix_stems.py` requires `ffmpeg`. Both are optional. If either is
missing, keep the workflow in planning/analysis mode or switch to
`music-craft-minimax` rather than pretending a stem workflow ran.

If the active platform is not recognized (unknown base image, restricted shell, no package manager available), say so explicitly and ask the user to either name their environment or install the tools manually before continuing.
