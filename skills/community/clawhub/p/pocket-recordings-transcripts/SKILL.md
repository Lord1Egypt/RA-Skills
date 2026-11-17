---
name: pocket-recordings-transcripts
description: "Pocket: Search, list, and read the user's Pocket recordings including transcripts and AI summaries; create audio download links; save recording audio to file storage; upload new audio recordings; list tags. Use when an agent needs pocket, pocket recordings transcripts, search recordings by topic, pull meeting transcripts, get ai summaries of conversations, upload audio files for transcription, get audio download url, recording id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/pocket-recordings-transcripts
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/pocket-recordings-transcripts"}}
---
# Pocket

## Freshness
Last updated: `2026-08-01`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Bring your Pocket recordings into every tool you already use. Pocket captures your conversations, meetings, and calls as recordings, transcripts, and AI summaries — and this makes all of it searchable and workflow-ready for your AI assistant. Search by keyword or meaning, pull full transcripts and summaries, upload new audio for transcription, generate shareable audio links, and organize by tag — then build automations and workflows that turn what was said into follow-up emails, CRM notes, tasks, and shared documents.

## Product Instructions
### Pocket Recordings

Use these actions for a member's recordings, transcripts, summaries, audio files, uploads, and tags.

#### Actions

##### `search_recordings`
Required: `query`
Optional: `limit`, `filters`
`{"action":"search_recordings","query":"weekly planning","limit":8}`

##### `list_recordings`
Optional: `start_date`, `end_date`, `tag_ids`, `page`, `limit`
`{"action":"list_recordings","start_date":"2026-07-01","end_date":"2026-07-31","limit":20}`

##### `get_recording`
Required: `recording_id`
Optional: `include_transcript`, `include_summarizations`, `summarization_id`
`{"action":"get_recording","recording_id":"rec_123","include_transcript":true,"include_summarizations":true}`

##### `get_audio_download_url`
Required: `recording_id`
Optional: `expires_in`
`{"action":"get_audio_download_url","recording_id":"rec_123","expires_in":3600}`

##### `save_audio_to_files`
Required: `recording_id`
Optional: `expires_in`
`{"action":"save_audio_to_files","recording_id":"rec_123"}`

##### `upload_recording`
Required: `file_id`
Optional: `title`, `recording_at`, `duration_seconds`
`{"action":"upload_recording","file_id":"file_123","title":"Design review","duration_seconds":1842}`

##### `list_tags`
`{"action":"list_tags"}`

#### Pagination

List and search actions can return `pagination` with page, limit, totals, and continuation details when available.

#### Notes

`filters` is an advanced passthrough object for search. Audio save and upload actions have a 100 MiB limit; use `get_audio_download_url` for larger audio.

## When To Use
- Use this skill for `Pocket` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: pocket, pocket recordings transcripts, search recordings by topic, pull meeting transcripts, get ai summaries of conversations, upload audio files for transcription, get audio download url, recording id.
- Supported action names: `get_audio_download_url`, `get_recording`, `list_recordings`, `list_tags`, `save_audio_to_files`, `search_recordings`, `upload_recording`.

## Use Cases
- Search recordings by topic
- Pull meeting transcripts
- Get AI summaries of conversations
- Upload audio files for transcription
- Download recording audio
- Browse recordings by date or tag
- Feed meeting notes into automations

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `7`.
x402 availability: not enabled for this product.

- `get_audio_download_url` (action slug: `get-audio-download-url`): Create a temporary audio download link for one recording. Use this for large audio instead of saving the file. Price: `5` credits. Parameters: `expires_in`, `recording_id`.
- `get_recording` (action slug: `get-recording`): Get one Pocket recording, optionally including transcript and summarization data. Price: `5` credits. Parameters: `include_summarizations`, `include_transcript`, `recording_id`, `summarization_id`.
- `list_recordings` (action slug: `list-recordings`): List the user's Pocket recordings with optional date, tag, and pagination filters. Price: `5` credits. Parameters: `end_date`, `limit`, `page`, `start_date`, `tag_ids`.
- `list_tags` (action slug: `list-tags`): List tags available in the user's Pocket recording library. Price: `5` credits. Parameters: none.
- `save_audio_to_files` (action slug: `save-audio-to-files`): Download one recording's audio and save it to File Manager. Audio over 100 MiB is rejected. Price: `5` credits. Parameters: `expires_in`, `recording_id`.
- `search_recordings` (action slug: `search-recordings`): Search Pocket recordings by query. Requires query. Optional limit must be 20 or fewer; filters is an advanced passthrough object. Price: `5` credits. Parameters: `filters`, `limit`, `query`.
- `upload_recording` (action slug: `upload-recording`): Upload a File Manager audio file to Pocket for transcription. Requires a valid file_id owned by this budget, rejects files over 100 MiB, and never returns the temporary upload URL. Price: `5` credits. Parameters: `duration_seconds`, `file_id`, `recording_at`, `title`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "pocket-recordings-transcripts"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "pocket-recordings-transcripts"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "pocket-recordings-transcripts"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "pocket-recordings-transcripts"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "pocket-recordings-transcripts"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "pocket-recordings-transcripts"
  }
}
```

## Call This Tool
Product slug: `pocket-recordings-transcripts`

Marketplace page: https://www.agentpmt.com/marketplace/pocket-recordings-transcripts

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Pocket",
    "arguments": {
      "action": "get_audio_download_url",
      "expires_in": 60,
      "recording_id": "example recording id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "pocket-recordings-transcripts",
  "parameters": {
    "action": "get_audio_download_url",
    "expires_in": 60,
    "recording_id": "example recording id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_audio_download_url` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/pocket-recordings-transcripts
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
