---
name: local-image-gen-aipc
#displayName: Local Image Generation (Windows · Z-Image-Turbo · OpenVINO)


description: >
generate an image, create a picture, draw something, make an image of, text to image,
paint a picture, illustrate, visualize, local image generation, AI art, image synthesis,
offline image generation, no API key, local inference, generate art, create artwork,
produce an image, render an image, AI drawing, image from text.
Runs Z-Image-Turbo on-device on Windows via Intel OpenVINO. Prioritizes Intel iGPU
(Xe / Arc), falls back to CPU. Bilingual prompts (English + Chinese) supported.
SETUP requires network: downloads pip dependencies from GitHub and the model (\~10 GB)
from modelscope.cn. INFERENCE is fully offline after setup — no cloud API calls.
os: windows
requires:

* python>=3.10
* git
network:
setup: required    # github.com (pip deps), modelscope.cn (\~10 GB model)
inference: offline
user-invocable: true
allowed-tools: Bash(python *), Bash(powershell *), Bash(git *), Read, Glob, Write, message
---


**Model**: `snake7gun/Z-Image-Turbo-int4-ov` (ModelScope INT4)  
**SKILL_VERSION**: `v1.0.3`

> **Network usage**: Setup downloads pip dependencies (some pinned to git+https commits)
> from `github.com`, and the model (~10 GB, resume supported) from `modelscope.cn`.
> Inference is fully offline — no network calls once setup is complete.

**First time?** Before using this skill, run these two scripts once in a terminal:

```
python setup.py          # creates venv, installs dependencies (~5 min)
python download_model.py # downloads the model (~10 GB, resumable)
```

Both scripts are in the skill directory alongside this SKILL.md.

## Directory layout (all auto-created)

```
{USERNAME}_openvino\
├── venv\                          ← shared venv (created by setup.py)
└── imagegen\
    ├── state.json                 ← written by setup.py
    ├── generate_image.py          ← deployed by setup.py (versioned)
    ├── Z-Image-Turbo-int4-ov\    ← downloaded by download_model.py (~10 GB)
    └── outputs\YYYYMMDD_HHMMSS_topic.png
```

---

##  Agent instructions

1. **Windows / PowerShell only.** Never use Linux commands (`ls`, `rm`, `cat`). Never use `&&` or `call`.
2. **Every step reads `state.json` itself** — do not pass paths between steps manually.
3. **Use `VENV_PY` from state.json for all inference and package-import calls** — never use system Python for inference or Step 2 DEP_CHECK. Exception: `setup.py`, `check_env.py`, `download_model.py`, and the Step 2 script-write command intentionally run with system Python (they only use stdlib or create/validate the venv, so they must not depend on it).
4. **CRITICAL — Never modify `generate_image.py` manually.** It is deployed and versioned by `setup.py`. If it fails or is missing, re-run `setup.py`.
5. **Goal**: generate an image and send the preview to the conversation.

**Auto-recovery policy — try before asking user:**

* If `STATE=MISSING`, `VENV_PY=BROKEN`, `PACKAGES_MISSING`, or `SCRIPTS_STALE`: automatically run `setup.py` (up to 3 attempts). Only ask user if all 3 fail.
* If `MODEL_STATUS=MISSING`: automatically run `download_model.py` (up to 3 attempts). Stop if a single attempt exceeds 20 minutes — download supports resume, partial progress is not lost.
* Always announce before each attempt: `[INFO] Auto-installing environment (attempt N/3)…`

**[WARNING] Network / proxy handling** — when running `setup.py` or `download_model.py`:
1. Check for proxy: read `$env:HTTPS_PROXY` / `$env:HTTP_PROXY`; if unset, run `netsh winhttp show proxy`.
2. If proxy detected: apply automatically and continue.
3. If no proxy and download/setup fails: inform the user, suggest configuring one, then retry.

Many networks (corporate / China mainland / campus) require a proxy. Download supports resume — safe to retry after fixing network.

**Pipeline — follow exactly in order, no skipping:**

```
Step 0: expand prompt       → EXPANDED_PROMPT, TOPIC
Step 1: verify environment  → VENV_PY, IMAGE_GEN_DIR confirmed ready
         ↳ if STATE=MISSING or VENV_BROKEN or PACKAGES_MISSING: auto-run setup.py (3 attempts)
         ↳ if MODEL_STATUS=MISSING: auto-run download_model.py (3 attempts)
Step 2: verify deps         → DEP_CHECK=PASS
Step 3: generate + send     → [SUCCESS] + image preview
```
## Pre-flight: Verify Runtime Requirements (Required on First Use)

> Pre-flight: Checking Python and git...

### Check Python Version

```powershell
python --version
```

**Interpretation:**

| Output | Action |
|------|------|
| `Python 3.10.x` or higher | [OK] `PYTHON_OK`, continue to git check |
| `Python 3.8 / 3.9` | Version too low; upgrade is required (see below) |
| `'python' is not recognized as an internal or external command` | Python is not installed; install is required (see below) |
| `Python was not found; run without arguments...` | **Windows Store alias** — see below |

**If output contains "run without arguments to install from the Microsoft Store"**, the Windows Store App Execution Alias is shadowing the real Python. Do NOT ask the user to change settings, and do NOT write helper scripts. Run this command to find the real Python:

```powershell
where.exe python 2>$null | Where-Object { $_ -notlike "*WindowsApps*" } | Select-Object -First 1
```

* A path is printed → **record this literal string as `SYSTEM_PYTHON`** (system-level Python, used only for `setup.py`, `check_env.py`, `download_model.py`). For every command marked `[SYSTEM PYTHON]`, substitute the full literal path for `python`. Do NOT use this path for inference — inference must always use `VENV_PY`. Do NOT use a `$variable` across tool calls — each call is a new shell; always embed the literal path directly.
* Nothing printed → Python is not installed — install it (see below).

**If Python is missing or outdated**, run this one-command silent installer in PowerShell (recommended, no admin required):

```powershell
$f = "$env:TEMP\python-installer.exe"
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

| Output | Action |
|------|------|
| `git version 2.x.x` | [OK] `GIT_OK`, Pre-flight passed |
| `'git' is not recognized as an internal or external command` |  git is not installed; install is required (see below) |

**If git is missing**, run this one-command silent installer in PowerShell:

```powershell
$f = "$env:TEMP\git-installer.exe"
Invoke-WebRequest "https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe" -OutFile $f
Start-Process $f -ArgumentList "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=icons,ext\\reg\\shellhere,assoc,assoc_sh" -Wait
Remove-Item $f
```

After installation, **restart the terminal**, then run `git --version` to confirm.

If you prefer manual installation: open **https://git-scm.com/download/win**, download the installer, and proceed with default options.

> git is required for the `git+https://` dependency in `requirements_imagegen.txt`; without git, `pip install` will fail with `git: command not found`.

**Pre-flight pass criteria**: `python --version` is >= 3.10 and `git --version` returns a valid version string.

Status message: `[OK] Python and git are ready. Starting main workflow.`

---

## Skill Contract (Input / Output)

### Accepted Inputs

1. **Text description** (required) — English or Chinese prompt describing the image to generate.
2. **Optional parameters:**
   * `steps`: inference steps, default 9 (higher = more detail)
   * `size`: `512×512` | `768×768` | `1024×1024`, default `512×512`
   * `seed`: integer (default 42) or `-1` for random
   * `output`: custom absolute output path for the PNG file

### Output on Success

Returns the PNG file path in stdout as `[SUCCESS] <path>`, and sends a preview via the `message` tool.

```json
{
    "image_path": "C:\\...\\outputs\\20260412_153000_panda_bamboo.png",
    "topic": "panda_bamboo",
    "prompt": "A giant panda sitting in a lush bamboo forest...",
    "steps": 9,
    "size": "512x512",
    "seed": 42,
    "device": "GPU.0"
}
```

### Output on Failure

```json
{
    "error": "human-readable description",
    "stage": "environment | model | inference",
    "recoverable": true
}
```

---

## Step 0: expand prompt (LLM only — no tools)

Do two things simultaneously: **① expand the prompt** and **② extract a topic slug** (English snake_case, used for the filename).

Expansion structure: `[subject] [action/pose] [environment] [lighting/mood] [style] [quality tags]`

Prompts can be English or Chinese — no translation needed. Topic slug must always be English to avoid path encoding issues.

Quality tags: `photorealistic`, `8K resolution`, `cinematic lighting`, `masterpiece`

|Input|Topic slug|Expanded prompt|
|-|-|-|
|a panda|`panda_bamboo`|A giant panda sitting in a lush bamboo forest, sunlight filtering through leaves, photorealistic, 8K, wildlife photography|
|赛博朋克城市|`cyberpunk_city`|未来感都市夜景，霓虹灯倒映在湿漉漉的街道，赛博朋克风，电影级，8K|

Show the result before proceeding:

```
Input:    {user description}
   Expanded: {full prompt}
   Topic:    {topic_slug}
```

---

## Step 1: verify environment and model

> Step 1/3: checking environment and model…

```powershell
# [SYSTEM PYTHON] check_env.py validates the venv — must NOT use venv python here
python "<skill_dir>\check_env.py"
```

**Output interpretation:**

| Output | Meaning | Action |
|---|---|---|
| `MODEL_STATUS=READY` + `VENV_PY=...` | OK | Proceed to Step 2 |
| `SCRIPTS_STALE=old->new` | `generate_image.py` outdated | Auto-run setup.py (see below) |
| `STATE=MISSING` | setup.py never run | Auto-run setup.py (see below) |
| `VENV_PY=BROKEN` | venv corrupted | Auto-run setup.py (see below) |
| `PACKAGES_MISSING: ...` | packages missing from venv | Auto-run setup.py (see below) |
| `MODEL_STATUS=MISSING  missing=[...]` | download incomplete | Auto-run download_model.py (see below) |

**On success**: record `VENV_PY` and `IMAGE_GEN_DIR` from stdout, proceed to Step 2.

> If `SCRIPTS_STALE` also appears alongside `MODEL_STATUS=READY`, auto-run setup.py before Step 2 (see below).

---

### If SCRIPTS_STALE or STATE=MISSING or VENV_PY=BROKEN or PACKAGES_MISSING → auto-run setup.py

`SCRIPTS_STALE` means the venv and model are both OK but `generate_image.py` in `IMAGE_GEN_DIR` is an older version. `setup.py` is idempotent — it skips venv/packages if already healthy and only redeploys the script.

`PACKAGES_MISSING` means the venv exists but required packages (`openvino`, `torch`, `optimum.intel`) are not installed. Re-running `setup.py` re-installs only what is missing.

Announce and run (up to 3 attempts):

```
[INFO] Environment not initialized — auto-installing (attempt 1/3)…
```

```powershell
# [SYSTEM PYTHON] setup.py creates the venv — must NOT use venv python here
python "<skill_dir>\setup.py"
```

Re-run `python "<skill_dir>\check_env.py"` after each attempt. If all 3 fail, show manual fallback below.

---

### If MODEL_STATUS=MISSING → auto-run download_model.py

Announce to user and ask how to proceed:

```
Model not found — download required (~10 GB)
   Estimated time:
   • 100 Mbps → ~15 min
   •  50 Mbps → ~30 min
   •  10 Mbps → ~2 hr
   Download supports resume — safe to interrupt and retry.

   [Y] Start auto-download
   [N] I'll download manually — show me the link
```

**Auto-download** (up to 3 attempts, stop if a single attempt exceeds 20 minutes):

```powershell
# [SYSTEM PYTHON] download_model.py uses stdlib only — must NOT use venv python here
python "<skill_dir>\download_model.py"
```

Re-run `python "<skill_dir>\check_env.py"` after each attempt.

**Manual download fallback:**

ModelScope page: **https://modelscope.cn/models/snake7gun/Z-Image-Turbo-int4-ov/files**

Place all files under `<IMAGE_GEN_DIR>\Z-Image-Turbo-int4-ov\`. Required subdirs:

```
Z-Image-Turbo-int4-ov\
├── transformer\
├── vae_decoder\
└── text_encoder\
```

Then re-run `python "<skill_dir>\check_env.py"` to verify.

---

### Manual fallback (only if all 3 setup auto-attempts fail)

Show user:

```
[WARN] Auto-install failed. Please run manually in a terminal:

1) Install environment:
   python "<skill_dir>\setup.py"
   Takes ~5 min, fully automated.

2) Download model (~10 GB):
   python "<skill_dir>\download_model.py"
   Resumable — safe to interrupt and retry.

Come back here when done.
```

---

## Step 2: verify dependencies

> Step 2/3: verifying dependencies…

**Verify dependencies** (run via VENV_PY):

```
$env:PYTHONUTF8 = "1"
& "<VENV_PY>" -c "
import json, site
from pathlib import Path

EXPECTED_COMMITS = {
    'optimum_intel': '2f62e5ae',
    'diffusers':     'a1f36ee3',
}

def get_git_commit(pkg_name):
    dirs = site.getsitepackages()
    try: dirs += [site.getusersitepackages()]
    except Exception: pass
    for d in dirs:
        for dist in Path(d).glob(f'{pkg_name}*.dist-info'):
            url_file = dist / 'direct_url.json'
            if url_file.exists():
                data = json.loads(url_file.read_text(encoding='utf-8'))
                return data.get('vcs_info', {}).get('commit_id', 'no_vcs_info')
    return 'not_found'

results = {}
for pkg, imp in [('openvino','openvino'),('torch','torch'),('Pillow','PIL'),('modelscope','modelscope')]:
    try:
        ver = getattr(__import__(imp), '__version__', 'OK')
        results[pkg] = ('OK', ver)
    except ImportError as e:
        results[pkg] = ('MISSING', str(e))

try:
    from optimum.intel import OVZImagePipeline
    results['OVZImagePipeline'] = ('OK', 'importable')
except ImportError as e:
    results['OVZImagePipeline'] = ('MISSING', str(e))

for pkg_name, exp in EXPECTED_COMMITS.items():
    actual = get_git_commit(pkg_name)
    if actual == 'not_found':
        results[f'{pkg_name}@commit'] = ('MISSING', 'not installed via git+https')
    elif actual.startswith(exp):
        results[f'{pkg_name}@commit'] = ('OK', actual[:16])
    else:
        results[f'{pkg_name}@commit'] = ('WRONG', f'got {actual[:16]} want {exp}...')

all_ok = all(v[0] == 'OK' for v in results.values())
for k, (status, detail) in results.items():
    icon = '[OK]' if status == 'OK' else ('[WARN]' if status == 'WRONG' else '[MISSING]')
    print(f'  {icon} {k}: {detail}')
print('DEP_CHECK=PASS' if all_ok else 'DEP_CHECK=FAIL')
"
```

|Output|Action|
|-|-|
|`DEP_CHECK=PASS`|[PASS] Proceed to Step 3|
|`DEP_CHECK=FAIL` (MISSING)|[FAIL] Re-run `setup.py` and retry|
|`DEP_CHECK=FAIL` (`@commit` WRONG)|[FAIL] Force reinstall: `& "<VENV_PY>" -m pip uninstall optimum-intel diffusers -y` then `& "<VENV_PY>" -m pip install -r "<skill_dir>\requirements_imagegen.txt" --no-cache-dir`|

---

## Step 3: generate image and send preview

> Step 3/3: running inference…

Run these two commands separately:

```
$env:PYTHONUTF8 = "1"
```

```
& "<VENV_PY>" "<IMAGE_GEN_DIR>\generate_image.py" --prompt "EXPANDED_PROMPT" --topic "TOPIC" --steps 9 --seed 42
```

**Pass**: stdout contains `[SUCCESS]`. Record `OUTPUT_PATH` from the `[SUCCESS]` line.

Send preview via `message` tool:

```
action: "send"  filePath: "OUTPUT_PATH"  message: "[OK] TOPIC"
```

**Final announcement:**

```
[OK] Done! Path: <OUTPUT_PATH>
Prompt: {expanded prompt}
steps=9, 512×512, seed=42 | device: {CPU/GPU}
```
---

## Parameters

|Param|Default|Notes|
|-|-|-|
|`--prompt`|required|English or Chinese|
|`--topic`|empty|English snake_case slug for filename|
|`--steps`|9|Higher = more detail; no hard limit|
|`--width--height`|512|512 | 768|768  1024|1024 recommended|
|`--seed`|42|-1 = random|
|`--output`|auto|Custom absolute output path|

> `guidance_scale` is fixed at `0.0` and not exposed as a parameter.

---

## Troubleshooting

|Error|Cause|Fix|
|-|-|-|
|`STATE=MISSING`|setup.py never run|Run `python "<skill_dir>\setup.py"`|
|`VENV_PY=BROKEN`|venv corrupted|Re-run `python "<skill_dir>\setup.py"` — rebuilds venv automatically|
|`PACKAGES_MISSING: ...`|venv ok but packages missing|Re-run `python "<skill_dir>\setup.py"` — reinstalls missing packages; skips steps already done|
|`MODEL_STATUS=MISSING`|download never run or interrupted|Run `python "<skill_dir>\download_model.py"` — resumes automatically|
|`DEP_CHECK=FAIL` (MISSING)|packages not installed in venv|Re-run `setup.py`|
|`DEP_CHECK=FAIL` (`@commit` WRONG)|PyPI release installed instead of pinned commit|Uninstall optimum-intel + diffusers, reinstall with `--no-cache-dir`|
|`@commit` shows `not installed via git+https`|git was missing when pip ran|Confirm git is installed, re-run `setup.py`|
|`[ERROR] Model incomplete`|Download interrupted mid-file|Re-run `download_model.py` — resumes automatically|
|`[ERROR] state.json not found`|state.json missing|Re-run Step 1|
|`SCRIPTS_STALE=old->new`|`generate_image.py` in `IMAGE_GEN_DIR` is outdated|Auto-run `setup.py` — it redeploys only the script, skips venv/packages/model (fast)|
|`RuntimeError` on GPU|Insufficient VRAM|Lower resolution or hardcode `return "CPU"` in `get_device()`|
|Black  noisy output|Too few steps|Use `--steps` ≥ 4; 9 recommended|
|Download timeout|Network issue or proxy needed|Configure proxy and retry — download supports resume|
|`RuntimeError: stack expects each tensor to be equal size`|openvino 2026.1.0 breaks `OVZImagePipeline.forward` — `pooled_projections` tensors have mismatched sequence lengths|Downgrade: `& "<VENV_PY>" -m pip install openvino==2026.0.0 --force-reinstall`. Then re-run Step 2 and Step 3. If re-running `setup.py`, it will now install the pinned version automatically.|



