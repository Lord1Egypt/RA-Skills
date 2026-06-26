---
name: openai-ai
description: Manage OpenAI files, assistants, vector stores, batches, fine-tuning jobs, and model resources via the OpenAI API. Use this skill when users want to create or manage assistants, upload files, run batch jobs, fine-tune models, generate images or audio, and work with the Assistants API via OpenAI.
---

# OpenAI

![OpenAI](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/openai-dark.svg)

Access OpenAI's platform API with API key authentication. Manage files, assistants, vector stores, batches, fine-tuning jobs, and model resources. Generate chat completions, images, audio, and video.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=openai-ai) for hosted connection flows and credentials so you do not need to configure OpenAI API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect OpenAI |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect OpenAI |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   OpenAI API     │
│   (User Chat)   │     │   (API Key)  │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │3. Connect OpenAI   │                       │
          │                      │  4. Secure Proxy      │
          │                      │  5. API Requests      │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  OpenAI  │
    │  File    │           │ Auth     │           │ Platform │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for OpenAI again."

## Quick Start

```bash
# List assistants
clawlink_call_tool --tool "openai_list_assistants" --params '{"limit": 10}'

# Create a chat completion
clawlink_call_tool --tool "openai_create_chat_completion" --params '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}'

# List files
clawlink_call_tool --tool "openai_list_files" --params '{"purpose": "batch"}'
```

## Authentication

All OpenAI tool calls are authenticated automatically by ClawLink using the user's OpenAI API key.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every OpenAI API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=openai and connect OpenAI.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `openai` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration openai
```

**Response:** Returns the live tool catalog for OpenAI.

### Reconnect

If OpenAI tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=openai
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration openai`

## Security& Permissions

- Access is scoped to resources within the connected OpenAI organization and account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete file, delete assistant, cancel batch) must be confirmed.
- Fine-tuning, batch jobs, and video generation are asynchronous — poll for completion.

## Tool Reference

### Assistants & Threads

| Tool | Description | Mode |
|------|-------------|------|
| `openai_list_assistants` | List assistants to discover by name or metadata | Read |
| `openai_create_assistant` | Create a new assistant with model and tools | Write |
| `openai_modify_assistant` | Update an existing assistant | Write |
| `openai_delete_assistant` | Delete an assistant permanently | Write |
| `openai_create_thread` | Create a new conversation thread | Write |
| `openai_create_message` | Add a message to a thread | Write |
| `openai_create_run` | Execute an assistant on a thread | Write |
| `openai_list_messages` | List messages in a thread | Read |
| `openai_list_runs` | List runs for a thread | Read |
| `openai_cancel_run` | Cancel an in-progress run | Write |
| `openai_list_run_steps` | List steps in a run | Read |
| `openai_get_run_step` | Get details of a specific run step | Read |

### Files & Vector Stores

| Tool | Description | Mode |
|------|-------------|------|
| `openai_list_files` | List uploaded files | Read |
| `openai_upload_file` | Upload a file to OpenAI | Write |
| `openai_delete_file` | Delete an uploaded file | Write |
| `openai_download_file` | Download file content | Read |
| `openai_create_vector_store` | Create a vector store | Write |
| `openai_list_vector_stores` | List vector stores | Read |
| `openai_get_vector_store` | Get vector store details | Read |
| `openai_delete_vector_store` | Delete a vector store | Write |
| `openai_create_vector_store_file` | Add a file to a vector store | Write |
| `openai_list_vector_store_files` | List files in a vector store | Read |
| `openai_delete_vector_store_file` | Remove a file from a vector store | Write |

### Batches & Fine-Tuning

| Tool | Description | Mode |
|------|-------------|------|
| `openai_list_batches` | List batch jobs | Read |
| `openai_create_batch` | Create a batch from a JSONL file | Write |
| `openai_cancel_batch` | Cancel an in-progress batch | Write |
| `openai_list_fine_tunes` | List fine-tuning jobs | Read |
| `openai_create_fine_tuning_job` | Start a fine-tuning job | Write |
| `openai_list_fine_tuning_events` | Get events for a fine-tuning job | Read |
| `openai_list_fine_tuning_job_checkpoints` | List checkpoints from a fine-tuning job | Read |

### Generations & Completions

| Tool | Description | Mode |
|------|-------------|------|
| `openai_create_chat_completion` | Create a chat completion | Read |
| `openai_create_completion` | Create a text completion (legacy) | Read |
| `openai_create_response` | Create a response via Responses API | Write |
| `openai_create_embeddings` | Generate text embeddings | Read |
| `openai_create_image` | Generate an image | Write |
| `openai_create_image_edit` | Edit an existing image | Write |
| `openai_create_image_variation` | Create an image variation | Write |
| `openai_create_speech` | Generate text-to-speech audio | Read |
| `openai_create_audio_transcription` | Transcribe audio to text | Read |
| `openai_create_audio_translation` | Translate audio to English | Read |
| `openai_create_video` | Generate a video | Write |
| `openai_list_videos` | List video generation jobs | Read |
| `openai_get_video` | Get video generation status | Read |
| `openai_download_video` | Download video content | Read |
| `openai_create_moderation` | Classify content for policy violations | Read |

### Evaluations

| Tool | Description | Mode |
|------|-------------|------|
| `openai_list_evals` | List evaluations | Read |
| `openai_get_eval` | Get evaluation details | Read |
| `openai_create_eval` | Create an evaluation | Write |
| `openai_delete_eval` | Delete an evaluation | Write |
| `openai_create_eval_run` | Start an evaluation run | Write |
| `openai_get_eval_run` | Get evaluation run status | Read |
| `openai_list_eval_runs` | List evaluation runs | Read |
| `openai_cancel_eval_run` | Cancel an evaluation run | Write |

### Other Resources

| Tool | Description | Mode |
|------|-------------|------|
| `openai_list_models` | List available models | Read |
| `openai_list_engines` | List available engines | Read |
| `openai_get_input_token_counts` | Calculate token counts for a request | Read |
| `openai_create_skill` | Create a skill from files | Write |
| `openai_list_skills` | List skills | Read |
| `openai_delete_skill` | Delete a skill | Write |
| `openai_create_container` | Create an isolated execution container | Write |
| `openai_list_containers` | List containers | Read |
| `openai_delete_container` | Delete a container | Write |

## Code Examples

### Create a chat completion

```bash
clawlink_call_tool --tool "openai_create_chat_completion" \
  --params '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "max_tokens": 500
  }'
```

### Create an assistant

```bash
clawlink_call_tool --tool "openai_create_assistant" \
  --params '{
    "name": "Code Reviewer",
    "model": "gpt-4o",
    "instructions": "You review code and suggest improvements.",
    "tools": [{"type": "code_interpreter"}]
  }'
```

### Upload a file and create a vector store

```bash
clawlink_call_tool --tool "openai_upload_file" \
  --params '{
    "file": "@./knowledge.pdf",
    "purpose": "assistants"
  }'

clawlink_call_tool --tool "openai_create_vector_store_file" \
  --params '{
    "vector_store_id": "VS_ID",
    "file_id": "FILE_ID"
  }'
```

### Create a batch job

```bash
clawlink_call_tool --tool "openai_create_batch" \
  --params '{
    "input_file_id": "FILE_ID",
    "endpoint": "chat/completions",
    "model": "gpt-4o-mini",
    "completion_window": "24h"
  }'
```

### Generate an image

```bash
clawlink_call_tool --tool "openai_create_image" \
  --params '{
    "model": "dall-e-3",
    "prompt": "A minimalist diagram showing the OpenClaw to ClawLink to Provider flow",
    "size": "1024x1024",
    "n": 1
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm OpenAI is connected.
2. Call `clawlink_list_tools --integration openai` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `openai`.
5. If no OpenAI tools appear, direct the user to https://claw-link.dev/dashboard?add=openai.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List models → Create completion → Return result   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Use model IDs exactly as returned by `openai_list_models` — misspelled or unsupported IDs cause validation errors.
- Asynchronous operations (batch, fine-tune, video) return a job ID — poll `get` endpoints to check completion.
- Thread IDs must be persisted after creation and passed to all subsequent calls.
- Files uploaded for batch processing must have `purpose: "batch"`; files for assistants must have `purpose: "assistants"`.
- Video generation is asynchronous — poll `openai_get_video` until status is `completed`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration openai`. |
| Missing connection | OpenAI is not connected. Direct the user to https://claw-link.dev/dashboard?add=openai. |
| `invalid_request_error` | Invalid parameter or model not available. Verify model ID with `openai_list_models`. |
| `RateLimitError` | Too many requests. Wait and retry with exponential backoff. |
| `authentication_error` | Invalid API key. Reconnect OpenAI at the dashboard. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `openai`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Assistants API Overview](https://platform.openai.com/docs/assistants/overview)
- [Fine-tuning Documentation](https://platform.openai.com/docs/guides/fine-tuning)
- [Batch API](https://platform.openai.com/docs/guides/batch)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=openai-ai
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [OpenAI](https://clawhub.ai/hith3sh/openai-ai) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=openai-ai)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
