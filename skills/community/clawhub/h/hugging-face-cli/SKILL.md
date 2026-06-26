---
name: hugging-face-cli
description: "Manage Hugging Face Hub via hf CLI. Use when working with HF AI models, datasets, spaces, or repos."
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F917"
    version: 1.1.0
    homepage: https://huggingface.co
    primaryEnv: HF_TOKEN
    requires:
      env: [HF_TOKEN]
      bins: [hf]
---

# Hugging Face CLI

Hugging Face (https://huggingface.co) is the leading platform for sharing and collaborating on AI models, datasets, and spaces. This skill enables interaction with the Hub through the official `hf` CLI.

# Installation

Check if `hf` is available by running `hf version`. If not installed:

```bash
pip install -U "huggingface_hub[cli]"
# or
brew install hf
```

If the options above do not work, follow the [official installation guide](https://huggingface.co/docs/huggingface_hub/guides/cli#getting-started).

After installation, run `hf version` to verify. If the command is not found, run `source ~/.bashrc` (or `source ~/.zshrc` for zsh) to reload the PATH, then try again.

# Authentication

A Hugging Face User Access Token is required. The token is provided via the `HF_TOKEN` environment variable.

If authentication fails or the token is missing, instruct the user to:
1. Go to https://huggingface.co/settings/tokens
2. Create a new token — there are two permission levels:
   - **Read** (safer): sufficient for searching, downloading models/datasets, listing repos, browsing papers, and most read-only operations. Choose this if you only need to explore and download.
   - **Write** (less safe, broader access): required for creating/deleting repos, uploading files, managing discussions, deploying endpoints, and running jobs. Example 3 (create a repo and upload weights) requires a write token.
3. Set it as an environment variable: `export HF_TOKEN="hf_..."` (add to shell profile for persistence)

**Important:** Do NOT run `hf auth login` interactively — it requires terminal input. Instead, use the environment variable directly. The `hf` CLI automatically picks up `HF_TOKEN` from the environment for all commands. To verify authentication, run:
```bash
hf auth whoami
```

# Key Commands

| Task | Command |
|---|---|
| Check current user | `hf auth whoami` |
| Download files | `hf download <repo_id> [files...] [--local-dir <path>]` |
| Download specific revision | `hf download <repo_id> --revision <branch\|tag\|commit>` |
| Download with filters | `hf download <repo_id> --include "*.safetensors" --exclude "*.bin"` |
| Upload files | `hf upload <repo_id> <local_path> [path_in_repo]` |
| Upload as PR | `hf upload <repo_id> <local_path> [path_in_repo] --create-pr` |
| Upload (private repo) | `hf upload <repo_id> <local_path> [path_in_repo] --private` |
| Upload large folder | `hf upload-large-folder <repo_id> <local_path>` |
| Create a repo | `hf repos create <name> [--repo-type model\|dataset\|space] [--private]` |
| Delete a repo | `hf repos delete <repo_id>` |
| Delete files from repo | `hf repos delete-files <repo_id> <path>...` |
| Duplicate a repo | `hf repos duplicate <repo_id> [--type model\|dataset\|space]` |
| Repo settings | `hf repos settings <repo_id> [--private\|--public]` |
| Manage branches | `hf repos branch create\|delete <repo_id> <branch>` |
| Manage tags | `hf repos tag create\|delete <repo_id> <tag>` |
| List models | `hf models ls [--search <query>] [--sort downloads] [--limit N]` |
| Model info | `hf models info <repo_id>` |
| List datasets | `hf datasets ls [--search <query>]` |
| Dataset info | `hf datasets info <repo_id>` |
| Run SQL on data | `hf datasets sql "<SQL>"` |
| List spaces | `hf spaces ls [--search <query>]` |
| Space info | `hf spaces info <repo_id>` |
| Space dev mode | `hf spaces dev-mode <repo_id>` |
| List papers | `hf papers ls [--limit N]` |
| List collections | `hf collections ls [--owner <user>] [--sort trending]` |
| Create collection | `hf collections create "<title>"` |
| Collection info | `hf collections info <collection_slug>` |
| Add to collection | `hf collections add-item <collection_slug> <repo_id> <type>` |
| Delete collection | `hf collections delete <collection_slug>` |
| Run a cloud job | `hf jobs run <docker_image> <command>` |
| List jobs | `hf jobs ps` |
| Job logs | `hf jobs logs <job_id>` |
| Cancel a job | `hf jobs cancel <job_id>` |
| Job hardware | `hf jobs hardware` |
| Deploy endpoint | `hf endpoints deploy <name> --repo <repo_id> --framework <fw> --accelerator <hw> ...` |
| List endpoints | `hf endpoints ls` |
| Endpoint info | `hf endpoints describe <name>` |
| Pause/resume endpoint | `hf endpoints pause\|resume <name>` |
| Delete endpoint | `hf endpoints delete <name>` |
| List discussions | `hf discussions ls <repo_id>` |
| Create discussion | `hf discussions create <repo_id> --title "<title>"` |
| Comment on discussion | `hf discussions comment <repo_id> <num> --body "<text>"` |
| Close discussion | `hf discussions close <repo_id> <num>` |
| Merge PR | `hf discussions merge <repo_id> <num>` |
| Manage cache | `hf cache ls`, `hf cache rm <id>`, `hf cache prune` |
| Delete bucket / files | `hf buckets delete <user>/<bucket>`, `hf buckets rm <user>/<bucket>/<path>` |
| Sync to bucket | `hf sync <local_path> hf://buckets/<user>/<bucket>` |
| Print environment | `hf env` |

# End-to-End Examples

**Example 1: Explore trending models, pick one, and preview a download**
```bash
hf models ls --sort trending_score --limit 5
hf models info openai-community/gpt2
hf download --dry-run openai-community/gpt2 config.json tokenizer.json
hf download openai-community/gpt2 config.json tokenizer.json --local-dir ./gpt2
```

**Example 2: Browse today's papers and find related datasets**
```bash
hf papers ls --limit 5
hf datasets ls --search "code" --sort downloads --limit 5
hf datasets info bigcode/the-stack
```

**Example 3: Create a private model repo and upload weights**
```bash
hf repos create my-fine-tuned-model --private
# create returns <your-username>/my-fine-tuned-model — use that full ID below
hf upload <username>/my-fine-tuned-model ./output --commit-message "Add fine-tuned weights"
hf repos tag create <username>/my-fine-tuned-model v1.0 -m "Initial release"
```

# Further Reference

Reference version: `hf` CLI v1.x

For the full list of commands and options, use built-in help:
```bash
hf --help
hf <command> --help
```

- **Full documentation:** https://huggingface.co/docs/huggingface_hub/guides/cli
- **CLI reference:** https://huggingface.co/docs/huggingface_hub/package_reference/cli

# Safety Rules

- **Destructive commands require explicit user confirmation.** Before running any of the following, describe what will happen and ask the user to confirm:
  - `hf repos delete` — permanently deletes a repository
  - `hf repos delete-files` — deletes files from a repository
  - `hf buckets delete` / `hf buckets rm` — deletes buckets or bucket files
  - `hf discussions close` / `hf discussions merge` — closes or merges PRs/discussions
  - `hf collections delete` — permanently deletes a collection
  - `hf endpoints delete` — permanently deletes an Inference Endpoint
  - `hf jobs cancel` — cancels a running compute job
  - Any command with `--delete` flag (e.g., sync with deletion)
  - `hf cache rm` / `hf cache prune` — removes cached data from disk (re-downloadable, but may waste bandwidth)
- Never expose or log the `HF_TOKEN` value. Do not include it in command output or commit it to files.
- When uploading, warn the user if the target repo is public and the upload may contain sensitive data.
