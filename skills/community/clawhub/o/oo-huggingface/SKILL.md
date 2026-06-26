---
name: oo-huggingface
description: "Hugging Face (huggingface.co). Use this skill for ANY Hugging Face request — searching and reading data. Whenever a task involves Hugging Face, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Hugging Face"
  author: "OOMOL"
  version: "1.0.1"
  services: ["huggingface"]
  icon: "https://static.oomol.com/logo/third-party/Hugging%20Face.svg"
---

# Hugging Face

Operate **Hugging Face** through your OOMOL-connected account. This skill calls the `huggingface` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Hugging Face. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "huggingface" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "huggingface" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `generate_chat_completion` — Generate a chat completion with Hugging Face Inference Providers.
- `generate_embeddings` — Generate text embeddings with Hugging Face inference.
- `get_current_user` — Get the current authenticated Hugging Face user profile.
- `get_dataset_first_rows` — Preview the first rows of a dataset split from the Hugging Face Dataset Viewer.
- `get_dataset_info` — Get detailed metadata for a Hugging Face dataset by dataset id.
- `get_dataset_statistics` — Get column statistics for a dataset split from the Hugging Face Dataset Viewer.
- `get_model_info` — Get detailed metadata for a Hugging Face model by modelId.
- `get_space_info` — Get detailed metadata for a Hugging Face Space by repo id.
- `get_trending` — Get trending Hugging Face repositories across models, datasets, and Spaces.
- `list_datasets` — List Hugging Face datasets using user-friendly search filters.
- `list_endpoints` — List Hugging Face Inference Endpoints for a namespace.
- `list_models` — List Hugging Face models using user-friendly search filters.
- `list_repo_files` — List files in a Hugging Face repository tree.
- `list_spaces` — List Hugging Face Spaces using user-friendly discovery filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Hugging Face state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Hugging Face is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=huggingface
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Hugging Face homepage: https://huggingface.co
