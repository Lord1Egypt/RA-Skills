---
name: local-image-ocr-aipc
version: 2.0.0
description: >
  Image OCR, text recognition, extract text from image, scan document, read image text,
  invoice OCR, receipt OCR, contract recognition, table extraction, business card OCR,
  ID recognition, screenshot text extraction, document digitization.
  Runs locally on Windows using the GLM-OCR model, supports mixed Chinese/English text,
  prioritizes Intel iGPU inference, no cloud API calls.
user-invocable: true
allowed-tools: Bash(powershell *), Bash(python *), Bash(llama-server *), Read, Write, message
---

# Image OCR — Local AI PC (Windows · GLM-OCR · llama.cpp Vulkan)

**Model**: `ggml-org/GLM-OCR-GGUF` (Q8_0, HuggingFace / hf-mirror)  
**Inference**: `llama-server` (llama.cpp Vulkan prebuilt, HTTP API)  
**SKILL_VERSION**: `2.0.0`

## Directory Structure (auto-created or user-specified)

```
<OCR_DIR>\                        ← auto-selected drive or user-specified (e.g. C:\image-ocr or D:\image-ocr)
├── llama.cpp\                    ← llama-server.exe and related binaries
└── models\
    └── GLM-OCR-GGUF\
        ├── GLM-OCR-Q8_0.gguf        ← main model (~950 MB)
        └── mmproj-GLM-OCR-Q8_0.gguf ← vision projection layer (~484 MB, required)
```

Python helper scripts (located alongside this SKILL.md):

| File | Purpose |
|------|---------|
| `_ocr_cfg.py` | Shared helper: resolves OCR_DIR from env var or `.ocr_dir` config file |
| `ocr_setup.py` | All-in-one setup: preflight checks, llama.cpp install, model download & verify |
| `ocr_run.py` | Run GLM-OCR inference on an image (via llama-server HTTP API) |

> ## ⚠️ Before You Install — Security & Compliance Disclosure
>
> This skill will perform the following actions on your system. **Review carefully before granting autonomous execution.**
>
> | Action | Source | Risk level |
> |--------|--------|------------|
> | Download and extract `llama-server.exe` and related binaries | `github.com/ggml-org/llama.cpp` releases | Medium — executes downloaded binary |
> | Download model files (~1.5 GB total) | HuggingFace (`huggingface.co`) or ModelScope (`modelscope.cn`) | Low — large file download |
> | Automatically install **Miniforge** (if Python not found) | `github.com/conda-forge/miniforge` | Medium — silently installs Python to `%USERPROFILE%\miniforge3` |
> | Create directories and write files to disk | Local filesystem only | Low |
>
> **Credentials**: The GLM-OCR model (`ggml-org/GLM-OCR-GGUF`) is publicly available and does not
> require authentication. If you use a private or gated HuggingFace model, you may need to set
> `$env:HUGGINGFACE_TOKEN` before running the download commands — this skill does not request or
> store any tokens automatically.
>
> **Trust**: Verify you trust the following sources before proceeding:
> - `https://github.com/ggml-org/llama.cpp/releases`
> - `https://huggingface.co/ggml-org/GLM-OCR-GGUF`
> - `https://github.com/conda-forge/miniforge` (only if Miniforge auto-install is triggered)
>
> If you prefer to control each step manually rather than granting autonomous execution,
> run the commands in this SKILL.md one by one yourself.

---

## Cached Installation

> **AI Assistant**: After a successful first-time setup, fill in this section with the resolved paths.
> On every subsequent invocation, read this section first and attempt the Fast Path before running setup.

```
OCR_DIR       =
LLAMA_EXE     =
MODEL_GGUF    =
MMPROJ_GGUF   =
LAST_VERIFIED =
```

*(Leave blank until first install. AI fills these in after `INSTALL_DONE=1` is printed by `ocr_setup.py`.)*

---

## ⚠️ AI Assistant Instructions

### 0. Fast Path (try this first on every invocation)

**Before running any setup steps**, check the `## Cached Installation` section above.

- If `OCR_DIR` is filled in → attempt the fast path:
  ```
  python ocr_run.py "<image_path>"
  ```
- **Fast path succeeds** (stdout contains recognized text) → return the result immediately. No setup steps needed.
- **Fast path fails** (file not found, server error, model missing, etc.) → fall through to the full setup flow below and then retry inference.

---

### Full Setup Flow (run only when Fast Path fails or on first use)

1. Execute one command at a time; wait for output before proceeding.
2. Stop immediately on error; refer to the Troubleshooting table at the end.
3. Wrap all paths in double quotes.
4. `<OCR_DIR>` is the absolute working directory path, determined after Pre-flight.
5. **Single goal**: Recognize image content and return text results.

**Execution flow (do not skip steps)**:
```
Pre-flight: python ocr_setup.py --check     → LLAMA_STATUS + MODEL_STATUS
Step 1:     python ocr_setup.py --llama     → only if LLAMA_STATUS=MISSING/OUTDATED
            (Check Python first — see Step 1 below)
Step 2:     python ocr_setup.py --download  → only if MODEL_STATUS=MISSING
Step 3:     python ocr_run.py <image>       → inference → return result
Post-setup: Update "Cached Installation" section above with resolved paths
```

**Progress reporting**: Announce each step before starting, e.g.: `🔍 Pre-flight: Checking environment…`

**After successful setup**: Update the `## Cached Installation` section in this SKILL.md with:
- `OCR_DIR` (from `ocr_setup.py` output line `OCR_DIR=...`)
- `LLAMA_EXE` = `<OCR_DIR>\llama.cpp\llama-server.exe`
- `MODEL_GGUF` = `<OCR_DIR>\models\GLM-OCR-GGUF\GLM-OCR-Q8_0.gguf`
- `MMPROJ_GGUF` = `<OCR_DIR>\models\GLM-OCR-GGUF\mmproj-GLM-OCR-Q8_0.gguf`
- `LAST_VERIFIED` = today's date

---

## ⚠️ Using Bash.exe on Windows (Git Bash / WSL)

If the AI assistant's terminal is **bash.exe** rather than PowerShell or CMD, environment variables
set via `$env:OCR_DIR` (PowerShell) or `set OCR_DIR=` (CMD) will **not** be visible to Python scripts
launched from bash. This was the most common cause of "cannot find llama.cpp / models" errors.

### How it's solved now

All scripts use `_ocr_cfg.py` which resolves `OCR_DIR` via two methods (in order):

1. **Environment variable** `OCR_DIR` — works if properly `export`-ed in bash
2. **`.ocr_dir` config file** — written automatically by `ocr_setup.py --workdir` alongside the scripts

**As long as `ocr_setup.py` has been run once (from any shell), all subsequent scripts
will find the OCR directory automatically**, regardless of which shell is used.

### Shell compatibility summary

| Shell | Needs `export OCR_DIR=...`? | Works after first run of `ocr_setup.py`? |
|-------|----------------------------|------------------------------------------|
| PowerShell / CMD | No (auto-resolved) | ✅ Yes |
| Git Bash | No (reads `.ocr_dir` file) | ✅ Yes |
| WSL bash | No (reads `.ocr_dir` file) | ✅ Yes |

> **Note**: If running from WSL, `subprocess.Popen` does not support `creationflags`.
> `ocr_run.py` handles this automatically (`_CREATE_NO_WINDOW` is `0` when `sys.platform != "win32"`).

---

## Pre-flight: Check Environment

> 🔍 Pre-flight: Checking working directory, llama.cpp, and model files…

```
python ocr_setup.py --check
```

| Output | Action |
|--------|--------|
| Both `READY` | ✅ Skip to Step 3 |
| `LLAMA_STATUS=MISSING/OUTDATED` | ⬇️ Execute Step 1 |
| `MODEL_STATUS=MISSING` | ⬇️ Execute Step 2 |

Announce: `✅ Environment check complete. Execute steps as needed.`

---

## Step 1: Check Python + Install / Update llama.cpp Vulkan

> 🐍 Step 1a: Checking Python availability…

### Check Python

> Note: This step requires an existing Python to run scripts. Use the snippet below to locate Python,
> record the path as `PYTHON_EXE`, and use that Python for all subsequent steps.

**Option A — PowerShell (Windows default)**

```powershell
$customPythonExe = ""  # Optional: specify a path manually, e.g. "C:\Python311\python.exe"
$found = $null
if ($customPythonExe -and (Test-Path $customPythonExe)) { $found = $customPythonExe }
if (-not $found) {
    foreach ($cmd in @("python","python3","py")) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) { $found = (Get-Command $cmd).Source; break }
    }
}
if (-not $found) {
    foreach ($p in @(
        "$env:USERPROFILE\miniforge3\python.exe","$env:USERPROFILE\miniconda3\python.exe",
        "$env:USERPROFILE\anaconda3\python.exe")) {
        if (Test-Path $p) { $found = $p; break }
    }
}
if ($found) { $env:PYTHON_EXE = $found; Write-Host "PYTHON_STATUS=OK"; Write-Host "PYTHON_EXE=$found" }
else { Write-Host "PYTHON_STATUS=MISSING" }
```

**Option B — Bash / Git Bash / WSL (fallback if PowerShell is unavailable)**

```bash
CUSTOM_PYTHON_EXE=""  # Optional: e.g. "/c/Python311/python.exe"
found=""
if [ -n "$CUSTOM_PYTHON_EXE" ] && [ -x "$CUSTOM_PYTHON_EXE" ]; then found="$CUSTOM_PYTHON_EXE"; fi
if [ -z "$found" ]; then
    for cmd in python python3 py; do
        if command -v "$cmd" >/dev/null 2>&1; then found=$(command -v "$cmd"); break; fi
    done
fi
if [ -z "$found" ]; then
    for p in "$HOME/miniforge3/bin/python" "$HOME/miniconda3/bin/python" "$HOME/anaconda3/bin/python"; do
        if [ -x "$p" ]; then found="$p"; break; fi
    done
fi
if [ -n "$found" ]; then
    export PYTHON_EXE="$found"
    echo "PYTHON_STATUS=OK"
    echo "PYTHON_EXE=$found"
else
    echo "PYTHON_STATUS=MISSING"
fi
```

**If Python is not found (`PYTHON_STATUS=MISSING`)**, install Miniforge:

> **Consent required**: Miniforge will be silently installed to `%USERPROFILE%\miniforge3`.
> This installs a Python runtime and conda/pip toolchain. No admin rights are needed.
> Source: `github.com/conda-forge/miniforge`. Confirm with the user before proceeding.

**Option A — PowerShell**

```powershell
$mf = "$env:TEMP\Miniforge3-Windows-x86_64.exe"
Invoke-WebRequest -Uri "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe" -OutFile $mf
Start-Process $mf -ArgumentList "/S /D=$env:USERPROFILE\miniforge3" -Wait
Remove-Item $mf
$env:PYTHON_EXE = "$env:USERPROFILE\miniforge3\python.exe"
& $env:PYTHON_EXE --version
Write-Host "PYTHON_STATUS=OK"
```

**Option B — Bash / Git Bash / WSL**

```bash
MF_URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
MF_INSTALLER="/tmp/Miniforge3-install.sh"
curl -fsSL "$MF_URL" -o "$MF_INSTALLER"
bash "$MF_INSTALLER" -b -p "$HOME/miniforge3"
rm -f "$MF_INSTALLER"
export PYTHON_EXE="$HOME/miniforge3/bin/python"
"$PYTHON_EXE" --version
echo "PYTHON_STATUS=OK"
```

| Output | Action |
|--------|--------|
| `PYTHON_STATUS=OK` | ✅ Continue to Step 1b |
| `PYTHON_STATUS=MISSING` → Miniforge installed | ✅ Continue to Step 1b |
| Miniforge download error | ⛔ Check network, or install Python manually |

Announce: `✅ Python ready. Checking llama.cpp…`

---

> ⬇️ Step 1b: Installing / updating llama.cpp Vulkan… (only when `LLAMA_STATUS=MISSING/OUTDATED`)

> **Consent required**: Before proceeding, inform the user:
> - A ZIP (~50–100 MB) will be downloaded from `github.com/ggml-org/llama.cpp/releases`
> - It will be extracted to `<OCR_DIR>\llama.cpp\` and the original ZIP will be deleted
> - `llama-server.exe` will be placed on disk and launched as a local HTTP server by `ocr_run.py`
>
> Ask the user to confirm before running the download command.

Edit the `LLAMA_TAG` variable at the top of `ocr_setup.py` if a newer release is available.

```
python ocr_setup.py --llama
```

To install a specific tag:
```
python ocr_setup.py --llama --tag b9000
```

| Output | Action |
|--------|--------|
| `LLAMA_INSTALL=DONE` | ✅ Continue to Step 2 |
| Download error | ⛔ Check network, or manually download from browser and extract to `<OCR_DIR>\llama.cpp\` |

Announce: `✅ llama.cpp installed. Continue to Step 2 to download models.`

---

## Step 2: Download GLM-OCR Models

> 📦 Step 2: Downloading GLM-OCR models… (only when `MODEL_STATUS=MISSING`)

### First-time Download Notice (required reading when MODEL_STATUS=MISSING)

Announce the following to the user, then ask whether to proceed:

```
📥 First-time model download is approximately 1.5 GB
   (GLM-OCR-Q8_0.gguf ~950 MB + mmproj ~484 MB).
   Estimated download time:
   • 100 Mbps connection: ~2 minutes
   •  50 Mbps connection: ~4 minutes
   •  10 Mbps connection: ~20 minutes

   Downloads support resumption — if interrupted, re-running this step
   will automatically continue from where it left off.

   ✅ Ready — start automatic download
   📂 I prefer to download manually — skip automatic download
```

- User chooses **automatic download** → continue with download commands below
- User chooses **manual download** → jump to the "Manual Download Fallback" section

---

### Check Disk Space

```
python ocr_setup.py --disk
```

| Output | Action |
|--------|--------|
| `DISK_STATUS=OK` | ✅ Continue to Download Models |
| `DISK_STATUS=LOW` | ⚠️ Ask user to free space before continuing |

### Download Models

**Option A: HuggingFace (recommended)**

To use the HF mirror (China), uncomment the `HF_ENDPOINT` line inside `ocr_setup.py`.

```
python ocr_setup.py --download hf
```

**Option B: ModelScope (alternative for users in China)**

```
python ocr_setup.py --download ms
```

**Verify:**

```
python ocr_setup.py --verify
```

| Output | Action |
|--------|--------|
| `MODEL_DOWNLOAD=DONE` | ✅ Continue to Step 3 |
| Timeout / repeated failure | ⚠️ Direct user to "Manual Download Fallback", or switch Option A / B and retry |

Announce: `✅ Model download complete.`

---

### Manual Download Fallback

If automatic download repeatedly fails, guide the user to download manually:

```
⚠️ Automatic download failed. Please manually download the following two files:

1. GLM-OCR-Q8_0.gguf (~950 MB)
   HuggingFace: https://huggingface.co/ggml-org/GLM-OCR-GGUF/resolve/main/GLM-OCR-Q8_0.gguf
   HF Mirror:   https://hf-mirror.com/ggml-org/GLM-OCR-GGUF/resolve/main/GLM-OCR-Q8_0.gguf
   ModelScope:  https://modelscope.cn/models/ggml-org/GLM-OCR-GGUF/resolve/master/GLM-OCR-Q8_0.gguf

2. mmproj-GLM-OCR-Q8_0.gguf (~484 MB)
   HuggingFace: https://huggingface.co/ggml-org/GLM-OCR-GGUF/resolve/main/mmproj-GLM-OCR-Q8_0.gguf
   HF Mirror:   https://hf-mirror.com/ggml-org/GLM-OCR-GGUF/resolve/main/mmproj-GLM-OCR-Q8_0.gguf
   ModelScope:  https://modelscope.cn/models/ggml-org/GLM-OCR-GGUF/resolve/master/mmproj-GLM-OCR-Q8_0.gguf

Once downloaded, place both files into:
   <OCR_DIR>\models\GLM-OCR-GGUF\

Then run: python ocr_setup.py --verify
```

---

## Step 3: Run Inference

> 🔍 Step 3: Running GLM-OCR recognition…

### Determine Input Source

| Situation | Action |
|-----------|--------|
| User message contains a local file path (e.g. `C:\Users\...\xxx.png`) | ⬇️ Case A |
| User uploaded an image via the interface; AI tool provides a temp path | ⬇️ Case B |
| Neither | ⛔ Ask user to provide a local file path or upload an image |

### Case A: User Provides a Local File Path

```
python ocr_run.py "<file path extracted from user message>"
```

### Case B: User Uploaded an Image via the Interface

```
python ocr_run.py "<temporary image path provided by the AI tool>"
```

**Success criteria**: stdout contains the recognized text content.

---

### Format Output

Once the recognized text is obtained, process it according to the user's intent:

| Scenario | Handling |
|----------|----------|
| General text extraction | Output the recognized text as-is, preserving original layout |
| Invoice / receipt | Extract structured fields from the text; output as JSON + human-readable format |
| Table | Reformat the recognized text as a Markdown table |
| Business card | Extract name, title, company, phone, email, address; output as JSON |
| ID / certificate | Output structured by original layout |
| Screenshot / document | Organize output by paragraph |
| User-defined | Process according to the user's stated requirements |

**Completion announcement**:

```
✅ Recognition complete!
Let me know if you'd like to re-process, change the output format, or export to a file.
```

| Situation | Handling |
|-----------|----------|
| `ERROR: File not found` | File path does not exist — ask user to verify the path |
| Empty / garbled output | Low image quality — ask user to retake or rescan |
| Blurry / low-resolution image | Ask user to retake or zoom in before retrying |
| No text detected | Inform user that no recognizable text was found in the image |

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `PYTHON_STATUS=MISSING` | Python not installed | Step 1 auto-installs Miniforge; confirm consent and retry |
| `llama-server` not found | llama-server.exe path not set correctly | Run `python ocr_setup.py --check` to verify path |
| Server failed to start | Wrong binary version, Vulkan error, or port conflict | Run `python ocr_setup.py --llama` to reinstall latest llama.cpp; check Vulkan drivers |
| `ggml_vulkan: no devices found` | Vulkan driver not installed | Update GPU driver |
| `error: unable to open model` | Incorrect model path | Run `python ocr_setup.py --check` to verify path |
| `MODEL_DOWNLOAD=` no output | Download interrupted | Switch between `--download hf` / `--download ms`, or configure proxy |
| Garbled / blank output | Low image quality | Improve image quality |
| VRAM insufficient / crash | Not enough GPU memory | Lower `-ngl` value, or use `--device none` |
| Fast path fails unexpectedly | Stale cached paths in SKILL.md | Clear the `## Cached Installation` block, re-run full setup flow |

---

## References

- llama.cpp Releases: https://github.com/ggml-org/llama.cpp/releases
- GLM-OCR GGUF: https://huggingface.co/ggml-org/GLM-OCR-GGUF
