---
name: oo-apple-notary
description: "Apple Notary (developer.apple.com). Use this skill for ANY Apple Notary request — reading, creating, and updating data. Whenever a task involves Apple Notary, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Apple Notary"
  author: "OOMOL"
  version: "1.0.4"
  services: ["apple_notary"]
  icon: "https://static.oomol.com/logo/third-party/apple_notary.svg"
---

# Apple Notary

Operate **Apple Notary** through your OOMOL-connected account. This skill calls the `apple_notary` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Apple Notary. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "apple_notary" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "apple_notary" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_submission_log` — Get a download URL for the notarization log of one submission. The log is a JSON file listing everything the notary service found, including warnings on a submission it accepted, so it is worth reading even after a successful notarization. This action returns the URL only and downloads nothing; the URL expires after a few hours, and calling this action again issues a fresh one.
- `get_submission_status` — Read the state of one notarization submission. In Progress means the notary service has not finished yet, or that the software was never uploaded to Amazon S3; Accepted, Invalid and Rejected are final. Read get_submission_log afterwards in every case, because an accepted submission can still carry warnings.
- `list_submissions` — List the notarization submissions of the team behind the connected key. The notary service returns at most the 100 most recent ones and offers no pagination and no filtering, so this is the way to recover a submission identifier that was lost, not a full history.
- `submit_software` — Register a new notarization submission and get the temporary Amazon S3 credentials that upload the software. This action uploads nothing: it reserves the submission and returns the bucket, the object key and short-lived AWS credentials, and you then upload the exact file whose SHA-256 you passed here yourself. The credentials expire 12 hours after this call. The notary service only starts notarizing once that upload finishes, so a submission whose file was never uploaded stays In Progress; after uploading, poll get_submission_status until the status leaves In Progress. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Apple Notary state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Apple Notary is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/apple_notary
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Apple Notary homepage: https://developer.apple.com/documentation/notaryapi
- API documentation: https://developer.apple.com/documentation/notaryapi
