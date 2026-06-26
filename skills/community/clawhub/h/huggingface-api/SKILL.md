---
name: huggingface-skill
description: "Full Hugging Face Hub skill — CLI and Python API for downloading models/datasets, uploading files, managing repos and Spaces, searching the Hub, and handling cache. Reads HF_TOKEN from environment for private repos, gated models, and write operations. Use for: model inference prep, dataset pipelines, Hub automation, and Space deployment."
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
      env:
        - HF_TOKEN
    install:
      - kind: pip
        package: huggingface_hub
        bins: [huggingface-cli]
    primaryEnv: "HF_TOKEN"
    emoji: "🤗"
    homepage: https://huggingface.co/docs/huggingface_hub
    os:
      - linux
      - macos
      - windows
---

# Hugging Face Skill

This skill exposes the full **Hugging Face Hub** surface — both the `huggingface-cli` command-line tool and the `huggingface_hub` Python library — to every assistant interaction. It reads `HF_TOKEN` from the environment for authenticated operations; public read-only operations work without a token.

> **Token scope:** `HF_TOKEN` is only required for private/gated model downloads, any upload, repo creation/deletion, and Space management. All public model/dataset browsing and downloads work without one.

---

## Security Notice

- Set `HF_TOKEN` in your shell environment or `.env` file — never hard-code it in scripts.
- Use **fine-grained tokens** (read-only or repo-scoped) over full write tokens where possible. Create them at https://huggingface.co/settings/tokens
- Gated models (Llama, Gemma, etc.) require both a token and accepted model terms on the Hub web UI.
- `HF_HUB_OFFLINE=1` prevents all network calls — safe for air-gapped or CI environments where the cache is pre-populated.

---

## Installation

### Minimum install
```bash
pip install huggingface_hub
```

### Recommended install with all extras
```bash
pip install "huggingface_hub[cli,torch,tensorflow,fastai,dev]"
```

| Extra | Adds |
|-------|------|
| `cli` | `huggingface-cli` command |
| `hf_transfer` | Fast Rust-based multi-part downloads (`pip install hf_transfer`) |
| `torch` | PyTorch model helpers |
| `tensorflow` | TF model helpers |
| `fastai` | fastai helpers |

### Enable fast downloads (optional)
```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
```

### Verify install
```bash
huggingface-cli version
huggingface-cli whoami       # requires HF_TOKEN
```

---

## Authentication

### Login (writes token to ~/.cache/huggingface/token)
```bash
huggingface-cli login
# or non-interactively:
huggingface-cli login --token $HF_TOKEN
```

### Logout
```bash
huggingface-cli logout
```

### Check current identity
```bash
huggingface-cli whoami
```

### Environment variable (preferred for CI/scripts)
```bash
export HF_TOKEN=hf_...
```
The library reads `HF_TOKEN` automatically — no explicit login needed when this var is set.

---

## Downloading Models and Datasets

### Download an entire model repo
```bash
huggingface-cli download <org/model>
# Example:
huggingface-cli download google/gemma-2b
```

### Download a single file
```bash
huggingface-cli download <org/model> <filename>
huggingface-cli download openai/whisper-large-v3 config.json
```

### Download to a specific directory
```bash
huggingface-cli download <org/model> --local-dir ./models/mymodel
```

### Download a dataset repo
```bash
huggingface-cli download <org/dataset> --repo-type dataset
```

### Download a specific revision (branch, tag, or commit SHA)
```bash
huggingface-cli download <org/model> --revision v1.0
huggingface-cli download <org/model> --revision abc1234
```

### Download specific file patterns (glob)
```bash
huggingface-cli download <org/model> --include "*.safetensors"
huggingface-cli download <org/model> --exclude "*.bin" --include "*.safetensors"
```

### Download gated model (requires token + accepted terms)
```bash
HF_TOKEN=hf_... huggingface-cli download meta-llama/Llama-3-8B
```

---

## Uploading to the Hub

### Upload a single file
```bash
huggingface-cli upload <org/repo> <local_file> <path_in_repo>
huggingface-cli upload myorg/mymodel weights.safetensors model/weights.safetensors
```

### Upload an entire folder
```bash
huggingface-cli upload <org/repo> <local_folder> <path_in_repo>
huggingface-cli upload myorg/mymodel ./model_dir .
```

### Upload to a dataset repo
```bash
huggingface-cli upload myorg/mydataset ./data . --repo-type dataset
```

### Upload to a Space
```bash
huggingface-cli upload myorg/myspace ./app . --repo-type space
```

### Upload with commit message
```bash
huggingface-cli upload myorg/mymodel ./weights . --commit-message "Add fp16 weights"
```

### Upload large folder (multi-part, resumable)
```bash
huggingface-cli upload-large-folder myorg/mymodel --repo-type model ./large_model_dir
```

---

## Repository Management

### Create a repo
```bash
huggingface-cli repo create <repo-name>
huggingface-cli repo create my-model --type model
huggingface-cli repo create my-dataset --type dataset
huggingface-cli repo create my-space --type space
```

### Delete a repo
```bash
huggingface-cli repo delete <org/repo>
```

### Get repo info
```bash
huggingface-cli repo info <org/repo>
huggingface-cli repo info google/gemma-2b
```

---

## Tags

```bash
huggingface-cli tag create  <org/repo> <tag>      --message "Release v1.0"
huggingface-cli tag list    <org/repo>
huggingface-cli tag delete  <org/repo> <tag>
```

---

## Cache Management

### Scan cache (see what's stored locally)
```bash
huggingface-cli scan-cache
```

### Delete unused cache entries interactively
```bash
huggingface-cli delete-cache
```

### Show cache size summary
```bash
huggingface-cli scan-cache --verbose
```

---

## Python API — Quick Patterns

See `templates/python_patterns.txt` for full copy-paste code. Core entry point:

```python
import os
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
```

Use `scripts/hf_helper.py` as a CLI wrapper over the Python API for search, info, and cache operations without a browser.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | — | Access token; required for private/gated/write operations |
| `HF_HOME` | `~/.cache/huggingface` | Root cache directory |
| `HF_HUB_CACHE` | `$HF_HOME/hub` | Model/dataset cache |
| `HF_DATASETS_CACHE` | `$HF_HOME/datasets` | Datasets library cache |
| `HF_HUB_OFFLINE` | `0` | Set `1` to disable all network calls |
| `HF_HUB_ENABLE_HF_TRANSFER` | `0` | Set `1` to enable fast Rust downloader |
| `HF_ENDPOINT` | `https://huggingface.co` | Override for enterprise/mirror deployments |
| `HF_HUB_DISABLE_PROGRESS_BARS` | `0` | Set `1` to suppress tqdm bars (good for CI logs) |
| `HF_HUB_VERBOSITY` | `warning` | Log level: `debug`, `info`, `warning`, `error` |
| `HUGGINGFACE_HUB_VERBOSITY` | — | Legacy alias for `HF_HUB_VERBOSITY` |

---

## Best Practices

### 1. Prefer `--local-dir` over default cache for reproducible paths
The default cache uses content-addressed symlinks. Use `--local-dir ./models/name` when you need a stable, self-contained directory for an application.

### 2. Pin revisions in production
Always pass `--revision <commit-sha>` in production downloads. Branches like `main` are mutable and can silently update between runs.

### 3. Use `--include`/`--exclude` to skip unnecessary weights
Large models ship both `.bin` and `.safetensors` formats. Download only what your framework uses:
```bash
huggingface-cli download <model> --include "*.safetensors" --exclude "*.bin"
```

### 4. Pre-populate cache before going offline
```bash
huggingface-cli download <model>        # fills cache
export HF_HUB_OFFLINE=1                 # subsequent loads use cache only
```

### 5. Use fine-grained tokens with minimal scope
Create per-project tokens at https://huggingface.co/settings/tokens — read-only tokens cannot accidentally delete or overwrite repos.

### 6. Commit model cards alongside weights
Every upload is a git commit. Include a `README.md` (model card) in the upload folder so the repo is immediately browseable on the Hub.

### 7. Use `upload-large-folder` for models over ~50 GB
`upload-large-folder` uses multi-part upload with automatic retry and deduplication — far more reliable than `upload` for very large checkpoints.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `401 Unauthorized` | Set `HF_TOKEN` or run `huggingface-cli login` |
| `403 Forbidden` on gated model | Accept model terms on huggingface.co, then retry |
| `huggingface-cli: command not found` | `pip install "huggingface_hub[cli]"` and ensure pip bin is on PATH |
| Slow downloads | `pip install hf_transfer` and set `HF_HUB_ENABLE_HF_TRANSFER=1` |
| `OSError: [Errno 28] No space left` | Run `huggingface-cli delete-cache` to free cache space |
| Download resumes from wrong offset | Use `--local-dir` — the default cache can have stale partial blobs |
| `RepositoryNotFoundError` | Check repo name spelling and that your token has access |
| `RevisionNotFoundError` | Verify the branch/tag/SHA exists on the Hub |
| `EntryNotFoundError` | File not in this revision; check `huggingface-cli repo info` |
| Enterprise behind firewall | Set `HF_ENDPOINT=https://your-mirror.internal` |
