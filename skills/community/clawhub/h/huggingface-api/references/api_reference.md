# Hugging Face Hub API Reference

Complete reference for `huggingface-cli` (v0.20+) and the `huggingface_hub` Python library.

---

## CLI Overview

```
huggingface-cli login                         Authenticate with the Hub
huggingface-cli logout                        Remove stored token
huggingface-cli whoami                        Print current user
huggingface-cli download <repo> [file]        Download model/dataset/space files
huggingface-cli upload <repo> <src> <dest>    Upload file or folder
huggingface-cli upload-large-folder <repo>    Multi-part upload for large folders
huggingface-cli repo create <name>            Create a new repo
huggingface-cli repo delete <repo>            Delete a repo
huggingface-cli repo info <repo>              Show repo metadata
huggingface-cli tag create <repo> <tag>       Create a git tag
huggingface-cli tag list <repo>               List tags
huggingface-cli tag delete <repo> <tag>       Delete a tag
huggingface-cli scan-cache                    Inspect local cache
huggingface-cli delete-cache                  Interactively free cache space
huggingface-cli env                           Print environment / debug info
huggingface-cli version                       Print library version
```

---

## `huggingface-cli login`

```bash
huggingface-cli login [--token TOKEN] [--add-to-git-credential]
```

| Flag | Description |
|------|-------------|
| `--token TOKEN` | Pass token non-interactively (use `$HF_TOKEN` in scripts) |
| `--add-to-git-credential` | Store token in git credential store for HTTPS git operations |

Token is written to `~/.cache/huggingface/token`.  
**In CI/scripts** prefer `export HF_TOKEN=hf_...` over running login.

---

## `huggingface-cli download`

```bash
huggingface-cli download <repo_id> [filename ...] [flags]
```

| Flag | Description |
|------|-------------|
| `--repo-type` | `model` (default), `dataset`, `space` |
| `--revision` | Branch, tag, or commit SHA (default: `main`) |
| `--include PATTERN` | Glob pattern — only download matching files |
| `--exclude PATTERN` | Glob pattern — skip matching files |
| `--local-dir PATH` | Save to a plain directory instead of the cache |
| `--local-dir-use-symlinks` | `auto` (default), `True`, `False` — control symlink behavior with `--local-dir` |
| `--cache-dir PATH` | Override `HF_HUB_CACHE` for this download |
| `--token TOKEN` | Override `HF_TOKEN` |
| `--quiet` | Suppress progress bars |
| `--force-download` | Re-download even if already cached |

**Examples:**
```bash
# Entire model repo
huggingface-cli download google/gemma-2b

# Single file
huggingface-cli download openai/whisper-large-v3 config.json

# Safetensors only
huggingface-cli download meta-llama/Llama-3-8B \
  --include "*.safetensors" --exclude "*.bin"

# Specific commit, to a local dir
huggingface-cli download google/gemma-2b --revision abc1234 --local-dir ./gemma
```

---

## `huggingface-cli upload`

```bash
huggingface-cli upload <repo_id> <local_path> [path_in_repo] [flags]
```

| Flag | Description |
|------|-------------|
| `--repo-type` | `model` (default), `dataset`, `space` |
| `--revision` | Target branch (default: `main`) |
| `--commit-message` | Git commit message |
| `--commit-description` | Extended commit description |
| `--create-pr` | Open a Pull Request instead of committing directly |
| `--every N` | Auto-upload every N minutes (watch mode) |
| `--include PATTERN` | Only upload matching files |
| `--exclude PATTERN` | Skip matching files |
| `--delete PATTERN` | Delete remote files matching pattern as part of the commit |
| `--token TOKEN` | Override `HF_TOKEN` |
| `--quiet` | Suppress output |

**Examples:**
```bash
# Upload single file
huggingface-cli upload myorg/mymodel weights.safetensors weights.safetensors

# Upload folder to repo root
huggingface-cli upload myorg/mymodel ./model_dir .

# Upload only JSON files
huggingface-cli upload myorg/mymodel ./configs . --include "*.json"

# Upload as PR
huggingface-cli upload myorg/mymodel ./update . --create-pr --commit-message "Add fp16"
```

---

## `huggingface-cli upload-large-folder`

```bash
huggingface-cli upload-large-folder <repo_id> [flags] <local_folder>
```

Uses multi-part upload with automatic retry and deduplication. Required for repos > ~50 GB.

| Flag | Description |
|------|-------------|
| `--repo-type` | `model` (default), `dataset`, `space` |
| `--revision` | Target branch |
| `--num-workers N` | Parallel upload workers (default: 5) |
| `--token TOKEN` | Override `HF_TOKEN` |

---

## `huggingface-cli repo`

```bash
huggingface-cli repo create <name> [--type model|dataset|space] [--private] [--exist-ok]
huggingface-cli repo delete <org/repo>  [--repo-type model|dataset|space] [--yes]
huggingface-cli repo info   <org/repo>  [--repo-type model|dataset|space]
```

| Flag | Description |
|------|-------------|
| `--type` | `model`, `dataset`, or `space` |
| `--private` | Create as private repo |
| `--exist-ok` | Don't error if repo already exists |
| `--yes` | Skip confirmation prompt on delete |

---

## `huggingface-cli tag`

```bash
huggingface-cli tag create <repo_id> <tag>  [--message MSG] [--revision REV]
huggingface-cli tag list   <repo_id>
huggingface-cli tag delete <repo_id> <tag>  [--yes]
```

---

## `huggingface-cli scan-cache` / `delete-cache`

```bash
huggingface-cli scan-cache [--dir PATH] [--verbose]
huggingface-cli delete-cache [--dir PATH]
```

`scan-cache` prints a table of cached repos, revisions, sizes, and last-accessed dates.  
`delete-cache` launches an interactive TUI to select and delete revisions.

---

## Python API — `HfApi`

```python
from huggingface_hub import HfApi
import os

api = HfApi(token=os.environ.get("HF_TOKEN"))
```

### Repo operations

```python
# Create repo
api.create_repo(repo_id="myorg/mymodel", repo_type="model", private=True, exist_ok=True)

# Delete repo
api.delete_repo(repo_id="myorg/mymodel", repo_type="model")

# Repo info
info = api.repo_info(repo_id="google/gemma-2b", repo_type="model")
print(info.id, info.sha, info.private)

# List repo files
files = api.list_repo_files(repo_id="google/gemma-2b")
for f in files:
    print(f)

# List repo tree (with metadata)
for item in api.list_repo_tree(repo_id="google/gemma-2b"):
    print(item.path, item.size)
```

### Upload operations

```python
# Upload single file
api.upload_file(
    path_or_fileobj="local_weights.safetensors",
    path_in_repo="weights.safetensors",
    repo_id="myorg/mymodel",
    commit_message="Add weights",
)

# Upload folder
api.upload_folder(
    folder_path="./model_dir",
    repo_id="myorg/mymodel",
    repo_type="model",
    commit_message="Initial upload",
    ignore_patterns=["*.pyc", "__pycache__/"],
)

# Delete file
api.delete_file(
    path_in_repo="old_weights.bin",
    repo_id="myorg/mymodel",
    commit_message="Remove old bin weights",
)
```

### Download operations

```python
from huggingface_hub import snapshot_download, hf_hub_download

# Download single file → returns local path
local_path = hf_hub_download(
    repo_id="openai/whisper-large-v3",
    filename="config.json",
    token=os.environ.get("HF_TOKEN"),
)

# Download entire repo snapshot → returns local dir path
local_dir = snapshot_download(
    repo_id="google/gemma-2b",
    repo_type="model",
    ignore_patterns=["*.msgpack", "*.h5"],
    token=os.environ.get("HF_TOKEN"),
)
```

### Search and listing

```python
# List models
models = api.list_models(
    filter="text-generation",
    sort="downloads",
    direction=-1,
    limit=10,
)
for m in models:
    print(m.id, m.downloads)

# List datasets
datasets = api.list_datasets(search="squad", limit=5)

# List Spaces
spaces = api.list_spaces(author="huggingface", limit=10)

# Search by tag/library/pipeline
models = api.list_models(
    tags=["pytorch"],
    pipeline_tag="text-classification",
    library="transformers",
)
```

### Model/Dataset card operations

```python
from huggingface_hub import ModelCard, DatasetCard

# Read card
card = ModelCard.load("google/gemma-2b")
print(card.text)

# Create and push card
card = ModelCard("# My Model\n\nDescription here.")
card.push_to_hub("myorg/mymodel")
```

### Space management

```python
# Get Space runtime info
runtime = api.get_space_runtime(repo_id="myorg/myspace")
print(runtime.stage, runtime.hardware)

# Restart a Space
api.restart_space(repo_id="myorg/myspace")

# Pause / resume Space
api.pause_space(repo_id="myorg/myspace")
api.resume_space(repo_id="myorg/myspace")

# Duplicate a Space
api.duplicate_space(
    from_id="gradio/chatbot-streaming",
    to_id="myorg/my-chatbot",
    private=True,
)
```

### Commit API (atomic multi-file commits)

```python
from huggingface_hub import CommitOperationAdd, CommitOperationDelete

operations = [
    CommitOperationAdd(path_in_repo="new_file.txt", path_or_fileobj=b"content"),
    CommitOperationDelete(path_in_repo="old_file.txt"),
]

api.create_commit(
    repo_id="myorg/mymodel",
    operations=operations,
    commit_message="Atomic update",
)
```

### Cache management (Python)

```python
from huggingface_hub import scan_cache_dir, delete_cache_dir

# Inspect
cache_info = scan_cache_dir()
print(f"Total size: {cache_info.size_on_disk_str}")
for repo in cache_info.repos:
    print(repo.repo_id, repo.size_on_disk_str)

# Delete specific revisions
delete_strategy = cache_info.delete_revisions("abc123sha", "def456sha")
print(f"Will free: {delete_strategy.expected_freed_size_str}")
delete_strategy.execute()
```

---

## Inference API

```python
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ.get("HF_TOKEN"))

# Text generation
result = client.text_generation("The capital of France is", model="gpt2", max_new_tokens=50)

# Chat (OpenAI-compatible)
response = client.chat_completion(
    model="meta-llama/Llama-3-8B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)

# Image classification
result = client.image_classification("photo.jpg", model="google/vit-base-patch16-224")

# Automatic speech recognition
result = client.automatic_speech_recognition("audio.flac")

# Text to image
image = client.text_to_image("A cat on the moon", model="stabilityai/stable-diffusion-xl-base-1.0")
image.save("output.png")
```

---

## Hugging Face Filesystem (`HfFileSystem`)

Acts like a standard Python `fsspec` filesystem over the Hub:

```python
from huggingface_hub import HfFileSystem

fs = HfFileSystem(token=os.environ.get("HF_TOKEN"))

# List files
fs.ls("google/gemma-2b", detail=False)

# Read a file
with fs.open("google/gemma-2b/config.json") as f:
    import json
    config = json.load(f)

# Write a file (requires write token)
with fs.open("myorg/mymodel/notes.txt", "w") as f:
    f.write("My notes")

# Works with pandas, datasets, etc.
import pandas as pd
df = pd.read_parquet("hf://datasets/myorg/mydataset/data.parquet")
```

---

## Repository Types

| Type | `--repo-type` | URL pattern |
|------|--------------|-------------|
| Model | `model` | `huggingface.co/<org>/<name>` |
| Dataset | `dataset` | `huggingface.co/datasets/<org>/<name>` |
| Space | `space` | `huggingface.co/spaces/<org>/<name>` |

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `401 Unauthorized` | No token or expired token | `export HF_TOKEN=hf_...` or `huggingface-cli login` |
| `403 Forbidden` on gated model | Model terms not accepted | Visit model page on huggingface.co and accept terms |
| `RepositoryNotFoundError` | Typo in repo ID or insufficient permissions | Check spelling; ensure token has read access |
| `RevisionNotFoundError` | Branch/tag/SHA doesn't exist | Run `huggingface-cli repo info` to see available refs |
| `EntryNotFoundError` | File absent in this revision | Check exact filename and revision |
| Downloads very slow | Default Python downloader | `pip install hf_transfer` + `export HF_HUB_ENABLE_HF_TRANSFER=1` |
| `No space left on device` | Cache full | `huggingface-cli delete-cache` |
| `OSError: symbolic link privilege not held` (Windows) | Symlinks disabled | Add `--local-dir-use-symlinks False` to download command |
| Progress bars clutter CI logs | tqdm default | `export HF_HUB_DISABLE_PROGRESS_BARS=1` |
| Need to work offline | Network unavailable | Pre-download, then `export HF_HUB_OFFLINE=1` |
