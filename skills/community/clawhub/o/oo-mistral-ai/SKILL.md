---
name: oo-mistral-ai
description: "Mistral AI (mistral.ai). Use this skill for ANY Mistral AI request — reading, creating, updating, and deleting data. Whenever a task involves Mistral AI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mistral AI"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mistral_ai"]
  icon: "https://static.oomol.com/logo/third-party/Mistral%20AI.svg"
---

# Mistral AI

Operate **Mistral AI** through your OOMOL-connected account. This skill calls the `mistral_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mistral AI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mistral_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mistral_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `append_to_conversation` — Appends a new message to an existing session and triggers a new completion.
- `create_agent` — Create a new Mistral Agent. [write]
- `create_agents_completion` — Call the Mistral agents completions interface to generate Agent responses. [write]
- `create_audio_transcription` — Upload the audio file and call the Mistral transcoding interface. [write]
- `create_chat_completion` — Call the Mistral chat completions interface to generate chat responses. [write]
- `create_chat_moderation` — Call the Mistral chat moderations interface to detect chat message security risks. [write]
- `create_embeddings` — Call the Mistral embeddings interface to generate vectors. [write]
- `create_fim_completion` — Call the Mistral FIM completions interface to generate completion results. [write]
- `create_library` — Create a new Mistral library. [write]
- `create_library_share` — Creates or updates the shared access level for the specified library. [write]
- `create_moderation` — Call the Mistral moderations interface to detect text security risks. [write]
- `create_ocr` — Call the Mistral OCR interface to identify text and layout in the document. [write]
- `create_or_update_agent_alias` — Create or update an Agent version alias. [write]
- `delete_agent` — Delete the specified Agent. [destructive]
- `delete_conversation` — Delete the specified session. [destructive]
- `delete_file` — Delete the specified file. [destructive]
- `delete_library` — Delete the specified library. [destructive]
- `delete_library_document` — Delete the specified library document. [destructive]
- `delete_library_share` — Removes the shared access level for the specified library. [destructive]
- `download_file` — Download the file contents and return the accessible download address via fileTransit.
- `get_agent` — Get a single Agent by Agent ID, optionally specifying agent_version.
- `get_agent_version` — Get version details of the specified Agent.
- `get_conversation` — Get metadata for a single session by session ID.
- `get_conversation_history` — Get all history entries in the session.
- `get_conversation_messages` — Get all message entries in the session.
- `get_document_extracted_text_url` — Get a temporary signed link to a text file extracted from library document.
- `get_document_signed_url` — Get a temporary signed link to the library document's original file.
- `get_document_status` — Get the processing status of library document.
- `get_document_text_content` — Get the extracted text content of the library document.
- `get_file_signed_url` — Get the temporary signature download link for the file.
- `get_fine_tuning_jobs` — List fine-tuning jobs, with paging and filtering conditions.
- `get_library` — Get individual library details by library ID.
- `get_library_document` — Get details of a single library document.
- `get_model` — Get details of a single Mistral model by model ID.
- `list_agent_aliases` — Lists all version aliases for the specified Agent.
- `list_agent_versions` — Lists all versions of the specified Agent.
- `list_agents` — List all Agents, optionally with pagination, name, source or metadata filtering parameters.
- `list_batch_jobs` — List batch jobs, with paging and filtering conditions.
- `list_conversations` — List sessions under the current organization, with pagination and metadata filtering parameters.
- `list_files` — List all files under the current organization.
- `list_libraries` — List all libraries under the current organization.
- `list_library_documents` — List all documents under the specified library.
- `list_library_shares` — List shared access records for the specified library.
- `list_models` — List all Mistral models accessible by the current API Key.
- `reprocess_document` — Reprocess the specified library document.
- `restart_conversation` — Restarts the session from some historical point in the session and generates a new subsequent response. [write]
- `retrieve_file` — Get file metadata by file ID.
- `start_conversation` — Create a new session and immediately append the message or tool call context. [write]
- `update_agent` — Update the Agent configuration and create a new version. [write]
- `update_agent_version` — Switch the current version of the Agent. [write]
- `update_library` — Updates the properties of the specified library. [write]
- `update_library_document` — Updates the properties of the specified library document. [write]
- `upload_file` — Upload files to Mistral for fine-tuning, batch or OCR. [write]
- `upload_library_document` — Uploads a new document to the specified library. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mistral AI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mistral AI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mistral_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mistral AI homepage: https://mistral.ai
