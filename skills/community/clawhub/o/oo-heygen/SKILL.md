---
name: oo-heygen
description: "HeyGen (heygen.com). Use this skill for ANY HeyGen request — reading, creating, updating, and deleting data. Whenever a task involves HeyGen, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HeyGen"
  author: "OOMOL"
  version: "1.0.1"
  services: ["heygen"]
  icon: "https://static.oomol.com/logo/third-party/HeyGen.svg"
---

# HeyGen

Operate **HeyGen** through your OOMOL-connected account. This skill calls the `heygen` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HeyGen. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "heygen" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "heygen" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_asset` — Delete a HeyGen asset that is no longer needed. [destructive]
- `delete_video` — Delete a generated or translated HeyGen video that is no longer needed. [destructive]
- `generate_template_video` — Start an asynchronous HeyGen template video generation job with explicit template variables.
- `generate_video` — Start an asynchronous HeyGen avatar video generation job and return the generated video ID.
- `get_avatar` — Retrieve details for a single HeyGen avatar by avatar ID.
- `get_current_user` — Retrieve profile information for the HeyGen account associated with the API key.
- `get_remaining_quota` — Retrieve the remaining generation quota for the authenticated HeyGen account.
- `get_shareable_video_url` — Retrieve a public share URL for a rendered HeyGen video by video ID.
- `get_template` — Retrieve variable definitions and metadata for a single HeyGen template.
- `get_video_status` — Retrieve processing status and download URLs for a HeyGen video by video ID.
- `list_assets` — List uploaded HeyGen image, video, and audio assets so they can be reused in video generation.
- `list_avatars` — List HeyGen avatars and talking photos available for video generation.
- `list_folders` — List HeyGen folders and folder IDs that can be used with HeyGen video generation inputs.
- `list_templates` — List HeyGen templates created under the authenticated account.
- `list_videos` — List generated HeyGen videos for historical result management.
- `list_voices` — List HeyGen voices available for video narration.
- `upload_asset` — Upload an image, video, or audio file to HeyGen and return an asset ID usable in video generation. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HeyGen state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HeyGen is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=heygen
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- HeyGen homepage: https://www.heygen.com
