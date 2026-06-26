---

name: local-qwen3-asr-aipc
description: >
   Local offline ASR on Windows — no cloud, no API cost, full privacy.
   Qwen3-ASR 0.6B + Intel OpenVINO, GPU-accelerated inference.
   NETWORK: required for first-time setup (install deps + download 2 GB model); NOT required for inference.
   Auto-extracts audio from video files (mp4, mkv, webm, mov, avi) — just pass the video path.
   Also supports audio: mp3, wav, flac, m4a, ogg, aac, wma, opus.
   Single file, batch folder, or watch-mode continuous transcription with automatic txt/json archive.
   30 languages + 22 Chinese dialects, auto language detection.
   One-line LLM API: from acoustic_pipeline import AcousticPipeline
   Local speech to text, transcribe audio, voice recognition, transcribe video, transcribe recording,
   convert speech to text, audio transcription, local ASR, offline speech recognition, dictation on Windows.
   本地离线语音识别，零云端，支持视频音轨自动提取，支持批量转录和文件夹监听，自动保存转写文档。
   网络说明：仅首次安装环境和下载模型时需要网络，推理转录完全离线。
os: windows
requires:
   - python>=3.10
   - git
network:
   setup: required
   inference: offline
user-invocable: true
allowed-tools: Bash(python \*), Bash(powershell \*), Read, Write, message

---

# Local Speech Recognition (Windows · Qwen3-ASR · OpenVINO)

**Model**: `snake7gun/Qwen3-ASR-0.6B-fp16-ov` (ModelScope FP16)  
**SKILL_VERSION**: 'v1.0.3'

> **First time?** Before using this skill, run these two scripts once in a terminal:
> ```
> python setup.py          # [SYSTEM PYTHON OK] creates venv, installs deps (~5 min)
> python download_model.py # [SYSTEM PYTHON OK] downloads the model (~2 GB, resumable)
> ```
> Both scripts are in the skill directory alongside this SKILL.md.

---

## Agent Routing

Always use `acoustic_pipeline.py` as the entry point, called with **VENV_PY** (obtained from `check_env.py` output). It handles all cases:

```powershell
# VENV_PY = value from check_env.py output, e.g. C:\intel_openvino\venv\Scripts\python.exe

# Single file
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --file "<FILE_PATH>" --language auto

# Single file + save transcript
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --file "<FILE_PATH>" --language auto --archive json

# Watch folder
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --watch "<DIR_PATH>" --language auto --archive both

# Batch folder
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --batch "<DIR_PATH>" --language auto --archive json
```

> **Never run `acoustic_pipeline.py` with system `python`.** It imports model packages (`openvino`, `qwen_asr`) that are only installed in the venv.

Use `transcribe.py` directly only when called internally by `acoustic_pipeline.py` — do not invoke it as a standalone entry point.

---

## Skill Contract (Input / Output)

### Accepted Inputs

Any agent should treat this skill as a local audio/video transcription skill.

1. Single file path
* Audio: .wav, .mp3, .flac, .m4a, .ogg, .aac, .wma, .opus
* Video: .mp4, .mkv, .webm, .flv, .mov, .avi, .mts, .m2ts, .ts, .m3u8
2. Folder path
* Watch mode: continuously process new files in folder
* Batch mode: process existing files in folder recursively
3. Runtime options
* language: auto or explicit language name
* archive: none | txt | json | both
* archive_dir: optional output folder for transcript files
* auto_bootstrap: initialize ASR automatically when environment is missing

### Output On Success

The result should be returned as a JSON object (or equivalent dictionary) with:

* text: transcription content
* language: detected or requested language
* source_file: original input path
* source_format: source extension
* confidence: optional confidence value (if available)
* archive_files: optional object containing txt/json output paths

Example shape:

```json
{
    "text": "...",
    "language": "Chinese",
    "source_file": "C:\\demo\\meeting.mp4",
    "source_format": ".mp4",
    "confidence": null,
    "archive_files": {
        "json": "C:\\demo\\transcripts\\meeting_20260326_120000.json"
    }
}
```

### Output On Failure

The agent should return a short structured error summary including:

* error: human-readable failure reason
* stage: bootstrap | extract_audio | transcribe | archive
* source_file: input path (if known)
* recoverable: true if retry is reasonable

---

## ⚠️ Agent instructions

1. **Windows / PowerShell only.** Never use Linux commands (`ls`, `rm`, `cat`). Never use `&&` or `call`.
2. **Every step reads `state.json` itself** — do not pass paths between steps manually.
3. **Use `VENV_PY` from state.json for inference calls** — never use system python for inference. `check_env.py` and `setup.py` are the only scripts intentionally run with system python (they create or validate the venv, so they must not depend on it). `check_env.py` validates the *venv's* packages, not system Python's — `PACKAGES_MISSING` from check_env.py means the venv is incomplete, not the system installation.
4. `transcribe.py` is automatically deployed to `ASR_DIR` when `setup.py` runs. If it is missing, re-run `setup.py`.
5. **If `transcribe.py` fails at runtime**, do NOT edit it manually. Re-run `setup.py` to redeploy the original from the repository.
6. **Never diagnose "model issues" without running Step 1's check script first.** The model layout may use a `thinker/` subdirectory — the scripts handle this automatically.
7. **Do not generate helper scripts in agent workspace directories.** Use repository-managed `check_env.py` instead.
8. **Goal**: transcribe the audio file and send the result to the conversation.

**Auto-recovery policy — try before asking user:**
⚠️ Network handling (proxy-aware)

When running setup.py or download_model.py:

1. Try to read system proxy settings:

   * Environment variables: HTTP_PROXY / HTTPS_PROXY
   * Windows WinHTTP proxy (netsh winhttp show proxy)
2. If proxy is detected:

   * Automatically apply it
   * Continue installation / download
3. If no proxy is detected:

   * Continue normally (direct connection)
4. If download/setup fails:

   * Inform the user whether a proxy was detected
   * If no proxy was detected, suggest configuring one
   * Then retry
IMPORTANT:
* Many networks (corporate / China mainland / campus) require proxy
* Download supports resume — safe to retry after fixing network
* If `STATE=MISSING`, `VENV_PY=BROKEN`, or `PACKAGES_MISSING`: automatically run `setup.py` (up to 3 attempts). Only ask user to run it manually if all 3 attempts fail. `setup.py` is idempotent — it skips any step already completed (venv, packages, repo clone, asr_engine.py, transcribe.py). Re-running a working environment is safe and fast.
* If `MODEL_STATUS=MISSING`: automatically run `download_model.py` (up to 3 attempts). Only ask user to run it manually if all 3 attempts fail or if a single attempt runs longer than 8 minutes without completing (likely a slow connection — download_model.py supports resume so partial progress is not lost). `download_model.py` exits immediately if the model is already complete — re-running the script on an already-downloaded model is safe.
* Always announce what you are doing before each attempt: "⚙️ Automatically setting up the environment (attempt N/3)…"


## Pre-flight: Verify Runtime Requirements (Required on First Use)

> 🔍 Pre-flight: Checking Python and git...

### Check Python Version

```powershell
python --version
```

**Interpretation:**

| Output | Action |
|--------|--------|
| `Python 3.10.x` or higher | `PYTHON_OK` — set `PYTHON_EXE=python`, continue to git check |
| `Python 3.8 / 3.9` | Version too low; upgrade required (see below) |
| `'python' is not recognized...` | Python missing; install required (see below) |
| `Python was not found; run without arguments...` | **Windows Store alias** — run `py --version` instead (see below) |

**If output contains "run without arguments to install from the Microsoft Store"**, the Windows Store App Execution Alias is shadowing the real Python. Do NOT ask the user to change settings, and do NOT write helper scripts. Use `where.exe` (native Windows tool, works in both PowerShell and cmd) to find the real Python:

> ⚠️ **Do NOT write any helper .ps1 scripts. Run the command below directly in the terminal.**

```powershell
where.exe python 2>$null | Where-Object { $_ -notlike "*WindowsApps*" } | Select-Object -First 1
```

* A path is printed → **record this literal string as `SYSTEM_PYTHON`** (this is the system-level Python, used only to run `setup.py`, `check_env.py`, and `download_model.py`). For every command marked `[SYSTEM PYTHON]`, substitute the full literal path for `python`. Example: `python "<skill_dir>\check_env.py"` becomes `"C:\Users\intel\AppData\Local\Programs\Python\Python312\python.exe" "<skill_dir>\check_env.py"`. Do NOT use this path for inference — inference must always use `VENV_PY` (the venv Python path printed by `check_env.py`). Do NOT rely on a `$variable` across tool calls — each call is a new shell process; always embed the literal path directly.
* Nothing printed → Python is not installed — install it (see below).
**If Python is missing or outdated**, run this one-command silent installer in PowerShell (recommended, no admin required):

**```powershell
$f = "$env:TEMP\\python-installer.exe"
Invoke-WebRequest "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe" -OutFile $f
Start-Process $f -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1" -Wait
Remove-Item $f
```

> `PrependPath=1` adds Python to PATH automatically; `Include_pip=1` installs pip; `InstallAllUsers=0` avoids requiring administrator privileges.

After installation, **restart the terminal**, then run `python --version` and confirm it reports `Python 3.12.x`.

If you prefer manual installation: download **https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe** and make sure to check **"Add python.exe to PATH"** during setup.

### Check git

```bat
git --version
```

**Interpretation:**

**| Output | Action |**
**|------|------|**
| `git version 2.x.x` | ✅ `GIT_OK`, Pre-flight passed |
| `'git' is not recognized as an internal or external command` |  git is not installed; install is required (see below) |

**If git is missing**, run this one-command silent installer in PowerShell:

```powershell
$f = "$env:TEMP\\git-installer.exe"
Invoke-WebRequest "https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe" -OutFile $f
Start-Process $f -ArgumentList "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=icons,ext\\reg\\shellhere,assoc,assoc_sh" -Wait
Remove-Item $f
```

After installation, **restart the terminal**, then run `git --version` to confirm.

If you prefer manual installation: open **https://git-scm.com/download/win**, download the installer, and proceed with default options.

> git is required for the `git+https://` dependency in `requirements_imagegen.txt`; without git, `pip install` will fail with `git: command not found`.

**Pre-flight pass criteria**: `python --version` is >= 3.10 and `git --version` returns a valid version string.

Status message: `✅ Python and git are ready. Starting main workflow.`

**Pipeline — follow exactly in order, no skipping:**

```
Step 0: parse request       → AUDIO_PATH, LANGUAGE, TOPIC
Step 1: verify environment  → run check_env.py → record VENV_PY and ASR_DIR
         ↳ if STATE=MISSING or VENV_BROKEN or PACKAGES_MISSING: auto-run setup.py (3 attempts)
         ↳ if SCRIPTS_STALE=...: auto-run setup.py to redeploy runtime scripts
         ↳ if MODEL_STATUS=MISSING: auto-run download_model.py (3 attempts)
Step 2: transcribe + send   → run acoustic_pipeline.py using VENV_PY from Step 1
         ↳ fallback: run transcribe.py directly using VENV_PY and ASR_DIR from Step 1
```

\---

## Step 0: parse request (LLM only — no tools)

Extract from the user's message:

|Field|Default|Notes|
|-|-|-|
|`AUDIO_PATH`|required|Absolute path to audio/video file (wav/mp3/flac/m4a/ogg/aac/wma/opus/mp4/mkv/webm/flv/mov/avi/mts/m2ts/ts/m3u8)|
|`LANGUAGE`|auto-detect|Optional: `Chinese`, `English`, `Japanese`, etc.|
|`TOPIC`|English snake_case from context|Used for output filename|

If no audio file provided, ask the user before continuing.

---

## Step 1: verify environment and model

> Step 1/3: checking environment and model...

```powershell
# [SYSTEM PYTHON] check_env.py creates/validates the venv — must NOT use venv python here
python "<skill_dir>\check_env.py"
```

> `check_env.py` and `setup.py` intentionally run with system Python — they create and validate the venv, so they cannot depend on it.

**On success**: record `VENV_PY` and `ASR_DIR` from output, proceed to Step 2.

> `check_env.py` also prints `SCRIPTS_STALE=<old>-><new>` when the deployed `transcribe.py` is outdated.
> If this line appears, treat it as a mandatory **auto-update** — run `setup.py` before Step 2 (see below).

**On failure — auto-recovery (try before asking user):**

### If SCRIPTS_STALE=... → auto-run setup.py to redeploy runtime scripts

`SCRIPTS_STALE` means the venv and model are both OK, but the deployed `transcribe.py` (and/or `asr_engine.py`) in `ASR_DIR` is an older version. `setup.py` is idempotent — it skips the venv, package, and model steps and only redeploys the outdated files.

```
⚙️ Runtime scripts are outdated. Redeploying (attempt 1/3)...
```

```powershell
# [SYSTEM PYTHON] — redeploys transcribe.py and asr_engine.py to ASR_DIR
python "<skill_dir>\setup.py"
```
After running, re-run `check_env.py` to confirm `SCRIPTS_STALE` no longer appears, then proceed to Step 2.

### If STATE=MISSING or VENV_PY=BROKEN or PACKAGES_MISSING → auto-run setup.py

`PACKAGES_MISSING` means the venv exists but required packages (e.g. `openvino`, `qwen_asr`) are not installed. Re-running `setup.py` re-installs only what is missing; it does not recreate the venv or re-clone the repo.

Announce and run (up to 3 attempts):

```
⚙️ Environment is not initialized. Running automatic setup (attempt 1/3)...
```

```powershell
# [SYSTEM PYTHON] setup.py creates the venv — must NOT use venv python here
python "<skill_dir>\setup.py"
```
After each attempt, re-run `check_env.py` to verify. If all 3 attempts fail, show manual fallback below.

### If MODEL_STATUS=MISSING → auto-run download_model.py

Announce and run (up to 3 attempts, stop if a single attempt exceeds 8 minutes):

```
📥 Model not found. Starting automatic download (attempt 1/3)...
   Estimated time: ~3 minutes at 100 Mbps, ~5 minutes at 50 Mbps
   Download supports resume; rerun safely after interruption.
```

```powershell
# [SYSTEM PYTHON] download_model.py runs before venv — must NOT use venv python here
python "<skill_dir>\download_model.py"
```
After each attempt, re-run `check_env.py` to verify. If all 3 attempts fail, show manual fallback below.

### Manual fallback (only if all 3 auto-attempts fail)

Show user this message:

```
⚠️ Automatic setup failed. Manual steps are required.

Open a Windows terminal (PowerShell or Command Prompt) and run the following in order:

1) Install environment (if not installed yet):
   python "<skill_dir>\setup.py"          # [SYSTEM PYTHON OK]
   Expected duration: about 5 minutes, fully automated.

2) Download model (about 2 GB):
   python "<skill_dir>\download_model.py" # [SYSTEM PYTHON OK]
   Download supports resume; rerun safely after interruption.
   Estimated time: ~3 minutes at 100 Mbps, ~5 minutes at 50 Mbps.

After completion, return here and resend your request.
```

---

## Step 2: transcribe and send result

> Step 2/2: transcribing...

**Preferred path** — run `acoustic_pipeline.py` with the **venv Python** obtained from Step 1:

```powershell
# [VENV PYTHON] VENV_PY = value printed by check_env.py, e.g. C:\intel_openvino\venv\Scripts\python.exe
# Never use system python here — openvino/qwen_asr are only in the venv
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --file "AUDIO_PATH" --language auto --archive json
```

If the user specified a language:

```powershell
# [VENV PYTHON]
& "<VENV_PY>" "<skill_dir>\acoustic_pipeline.py" --file "AUDIO_PATH" --language "LANGUAGE" --archive json
```

Return the JSON result directly to the conversation and include any `archive_files` paths.

**Fallback** — only if `acoustic_pipeline.py` exits with a non-zero code:

```powershell
# [VENV PYTHON] fallback — both VENV_PY and ASR_DIR come from check_env.py (Step 1)
& "<VENV_PY>" "<ASR_DIR>\transcribe.py" --audio "AUDIO_PATH" --language "LANGUAGE"
```

> Never use system python here.

**Pass**: `$LASTEXITCODE -eq 0`. Stdout is a single line of JSON with this shape:

```json
{"text": "...", "language": "Chinese", "time_elapsed": 12.3, "audio_path": "C:\\audio\\file.wav"}
```

Parse with `$result = $stdout | ConvertFrom-Json`. Record `TRANSCRIPT` from `$result.text` and `LANG` from `$result.language`.

**Fail**: if `$LASTEXITCODE -ne 0`, do not attempt to parse stdout. Show the stderr output to the user.

Send via `message` tool:

```
action: "send"  message: "✅ LANG\n\nTRANSCRIPT"
```

---

## Troubleshooting

|Error|Fix|
|-|-|
|`Python was not found; run without arguments...`|Windows Store alias blocking `python`. Run: `where.exe python 2>$null | Where-Object { $_ -notlike "*WindowsApps*" } | Select-Object -First 1`. Record the printed literal path and substitute it for `python` in every subsequent command (do NOT use a `$variable` — each tool call is a new shell).|
|`STATE=MISSING`|Run `python "<skill_dir>\setup.py"`|
|`VENV_PY=BROKEN`|Re-run `python "<skill_dir>\setup.py"` — it will rebuild the venv|
|`PACKAGES_MISSING: ...`|Re-run `python "<skill_dir>\setup.py"` — re-installs missing venv packages only; skips steps already done|
|`MODEL_STATUS=MISSING`|Run `python "<skill_dir>\download_model.py"` — exits immediately if model is already complete|
|`[ERROR] Audio not found`|Verify the file path is correct and the file exists|
|`[ERROR] Model incomplete`|Re-run `python "<skill_dir>\download_model.py"` — supports resume|
|`[ERROR] state.json not found`|Re-run Step 1 (`check_env.py`)|
|`SCRIPTS_STALE=v1.0.1->v1.0.2`|Deployed runtime scripts are outdated. Run `python "<skill_dir>\setup.py"` — it redeploys only the changed files, skipping venv/packages/model (fast).|
|`RuntimeError` on GPU|Run `check_env.py` first to confirm model is READY. If model is OK, try adding `--language auto` to remove language mismatch. If still failing, re-run `setup.py` to upgrade OpenVINO and redeploy runtime files.|

---

## LLM API Usage

For agents that prefer a Python import interface over shell commands, run this inside a subprocess using **VENV_PY**:

```powershell
# Must be run with VENV_PY, not system python
& "<VENV_PY>" -c "
import sys; sys.path.insert(0, r'<skill_dir>')
from acoustic_pipeline import AcousticPipeline
pipeline = AcousticPipeline()
result = pipeline.transcribe(r'C:\\meeting.mp4', language='auto', archive_mode='json')
print(result['text'])
"
```

Or if your agent framework already runs inside the venv Python process:

```python
from acoustic_pipeline import AcousticPipeline

pipeline = AcousticPipeline()
result = pipeline.transcribe("C:\\meeting.mp4", language="auto", archive_mode="json")
print(result["text"])
print(result.get("archive_files"))
```

---

## Workspace Hygiene

* Use repository-managed `check_env.py` — it is versioned, auditable, and repeatable.
* If the execution environment forces a temporary file, treat it as disposable and remove it after the command completes.



