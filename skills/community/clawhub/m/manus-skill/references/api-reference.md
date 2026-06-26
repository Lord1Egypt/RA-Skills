# Manus API — Complete Reference

Base URL: `https://api.manus.ai`
Auth header: `API_KEY: <your-key>` (on every request)

---

## Table of Contents

1. [Projects](#projects)
2. [Tasks](#tasks)
3. [Files](#files)
4. [Webhooks API](#webhooks-api)
5. [Webhook Events & Payloads](#webhook-events)
6. [Attachment Formats](#attachment-formats)

---

## Projects

### POST /v1/projects — Create Project

Creates a project to organize tasks under shared instructions.

**Request Body:**

| Field         | Type   | Required | Description                                          |
|--------------|--------|----------|------------------------------------------------------|
| `name`        | string | Yes      | Project name                                         |
| `instruction` | string | No       | Default instruction applied to all tasks in project  |

**Response (200):**
```json
{
  "id": "proj_abc123",
  "name": "Research Project",
  "instruction": "Always cite sources",
  "created_at": 1699900000
}
```

### GET /v1/projects — List Projects

**Query Parameters:**

| Param  | Type    | Default | Description                      |
|--------|---------|---------|----------------------------------|
| `limit` | integer | 100     | Max projects to return (1-1000)  |

**Response (200):**
```json
{
  "data": [
    {
      "id": "proj_abc123",
      "name": "My Research Project",
      "instruction": "Always cite sources",
      "created_at": 1699900000
    }
  ]
}
```

---

## Tasks

### POST /v1/tasks — Create Task

Creates a new task OR continues an existing one (if `taskId` provided).

**Request Body:**

| Field                | Type      | Required | Description                                                       |
|---------------------|-----------|----------|-------------------------------------------------------------------|
| `prompt`             | string    | Yes      | Task instruction/prompt for the agent                             |
| `agentProfile`       | enum      | Yes      | `manus-1.6`, `manus-1.6-lite`, `manus-1.6-max` (default: `manus-1.6`) |
| `taskMode`           | enum      | No       | `chat`, `adaptive`, `agent`                                       |
| `taskId`             | string    | No       | **Pass to continue an existing task** (multi-turn). Omit for new. |
| `projectId`          | string    | No       | Associate with a project (applies project instruction)            |
| `attachments`        | array     | No       | File/image attachments (see Attachment Formats below)             |
| `connectors`         | string[]  | No       | Connector UUIDs to enable (Gmail, Notion, Calendar)               |
| `hideInTaskList`     | boolean   | No       | Hide from Manus webapp task list                                  |
| `createShareableLink`| boolean   | No       | Make chat publicly accessible                                     |
| `locale`             | string    | No       | Locale setting (e.g., `"en-US"`, `"zh-CN"`)                      |
| `interactiveMode`    | boolean   | No       | Allow Manus to ask follow-up questions (default: false)           |

**Response (200):**
```json
{
  "task_id": "TeBim6FDQf9peS52xHtAyh",
  "task_title": "Analyze Q2 Revenue",
  "task_url": "https://manus.im/app/TeBim6FDQf9peS52xHtAyh",
  "share_url": "https://manus.im/share/..."
}
```

`share_url` only present when `createShareableLink: true`.

### GET /v1/tasks — List Tasks

**Query Parameters:**

| Param          | Type      | Default      | Description                                             |
|---------------|-----------|--------------|--------------------------------------------------------|
| `after`        | string    | —            | Cursor: ID of last task from previous page              |
| `limit`        | integer   | 100          | Max tasks to return (1-1000)                            |
| `order`        | enum      | `desc`       | Sort direction: `asc` or `desc`                         |
| `orderBy`      | enum      | `created_at` | Sort field: `created_at` or `updated_at`                |
| `query`        | string    | —            | Free-text search on title and body                      |
| `status`       | string[]  | —            | Filter: `pending`, `running`, `completed`, `failed`     |
| `createdAfter` | integer   | —            | Unix timestamp — tasks created after this time          |
| `createdBefore`| integer   | —            | Unix timestamp — tasks created before this time         |
| `project_id`   | string    | —            | Filter by project ID                                    |

**Response (200):**
```json
{
  "object": "list",
  "data": [
    {
      "id": "task_abc",
      "object": "response",
      "created_at": 1699900000,
      "updated_at": 1699900100,
      "status": "completed",
      "error": null,
      "incomplete_details": null,
      "instructions": "...",
      "max_output_tokens": 4096,
      "model": "manus-1.6",
      "metadata": {
        "task_title": "My Task",
        "task_url": "https://manus.im/app/task_abc"
      },
      "output": [
        {
          "id": "msg_001",
          "status": "completed",
          "role": "assistant",
          "type": "message",
          "content": [
            {
              "type": "output_text",
              "text": "Here is the analysis...",
              "fileUrl": null,
              "fileName": null,
              "mimeType": null
            }
          ]
        }
      ],
      "locale": "en-US",
      "credit_usage": 150
    }
  ],
  "first_id": "task_first",
  "last_id": "task_last",
  "has_more": false
}
```

### GET /v1/tasks/{task_id} — Get Task

Retrieves full detail including output, status, credit usage, and metadata.

**Query Parameters:**

| Param     | Type   | Description                                          |
|----------|--------|------------------------------------------------------|
| `convert` | string | Convert output files (currently only for pptx)       |

**Response:** Same shape as individual items in the List Tasks `data` array.

### PUT /v1/tasks/{task_id} — Update Task

**Request Body (all optional):**

| Field                        | Type    | Description                          |
|-----------------------------|---------|--------------------------------------|
| `title`                      | string  | Rename the task                      |
| `enable_shared`              | boolean | Enable/disable public sharing        |
| `enable_visible_in_task_list`| boolean | Show/hide in Manus webapp task list  |

### DELETE /v1/tasks/{task_id} — Delete Task

Permanently deletes a task. Cannot be undone.

**Response (200):**
```json
{
  "id": "task_abc",
  "object": "task.deleted",
  "deleted": true
}
```

---

## Files

Files are uploaded via a two-step process: create a record to get a presigned S3 URL, then PUT the file content to that URL. Files auto-delete after 48 hours.

### POST /v1/files — Create File

**Request Body:**

| Field      | Type   | Required | Description    |
|-----------|--------|----------|----------------|
| `filename` | string | Yes      | Name of file   |

**Response (200):**
```json
{
  "id": "file-abc123xyz",
  "object": "file",
  "filename": "report.pdf",
  "status": "pending",
  "upload_url": "https://s3.amazonaws.com/...",
  "upload_expires_at": "2025-01-15T10:00:00Z",
  "created_at": "2025-01-15T09:00:00Z"
}
```

Then upload:
```bash
curl -X PUT "<upload_url>" \
  -H "Content-Type: application/pdf" \
  --data-binary @report.pdf
```

### GET /v1/files — List Files

Returns all uploaded files with status and metadata.

### GET /v1/files/{file_id} — Get File

Returns details of a specific file by ID.

### DELETE /v1/files/{file_id} — Delete File

Marks file as deleted. Can no longer be used in tasks.

---

## Webhooks API

### POST /v1/webhooks — Create Webhook

Registers a URL to receive task lifecycle events. Manus sends a test request to verify before activating.

**Request Body:**

| Field | Type   | Required | Description            |
|-------|--------|----------|------------------------|
| `url`  | string | Yes      | Your webhook endpoint  |

### DELETE /v1/webhooks/{webhook_id} — Delete Webhook

Removes a webhook subscription.

### GET /v1/webhook/public_key — Get Public Key

Returns RSA public key for verifying webhook signatures.

```json
{
  "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
  "algorithm": "RSA-SHA256",
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

## Webhook Events

Three event types per task lifecycle:

### task_created (sent once)
```json
{
  "event_id": "task_created_TASKID_TIMESTAMP",
  "event_type": "task_created",
  "task_detail": {
    "task_id": "TeBim6FDQf9peS52xHtAyh",
    "task_title": "Hello World Function",
    "task_url": "https://manus.im/app/TeBim6FDQf9peS52xHtAyh"
  }
}
```

### task_progress (sent multiple times)
```json
{
  "event_id": "task_progress_TASKID_TIMESTAMP",
  "event_type": "task_progress",
  "progress_detail": {
    "task_id": "TeBim6FDQf9peS52xHtAyh",
    "progress_type": "plan_update",
    "message": "Generating the TypeScript code."
  }
}
```

### task_stopped (sent once — completed or needs input)

**stop_reason values:**
- `"finish"` — completed; output and attachments available
- `"ask"` — needs user input; continue via multi-turn with `taskId`

```json
{
  "event_id": "task_stopped_TASKID_TIMESTAMP",
  "event_type": "task_stopped",
  "task_detail": {
    "task_id": "task_abc123",
    "task_title": "Generate Report",
    "task_url": "https://manus.im/app/task_abc123",
    "message": "Report complete.",
    "attachments": [
      {
        "file_name": "report.pdf",
        "url": "https://s3.amazonaws.com/.../report.pdf",
        "size_bytes": 2048576
      }
    ],
    "stop_reason": "finish"
  }
}
```

### Webhook Signature Verification

Headers on every webhook request:
- `X-Webhook-Signature` — Base64-encoded RSA-SHA256 signature
- `X-Webhook-Timestamp` — Unix timestamp

Signature content: `{timestamp}.{url}.{body_sha256_hex}`

Verify: SHA256 the concatenated string → verify with RSA public key from `/v1/webhook/public_key`. Reject requests >5 minutes old to prevent replay attacks.

---

## Attachment Formats

Three ways to attach files to tasks:

### By File ID (recommended)
```json
{ "attachments": [{ "fileId": "file-abc123xyz", "filename": "report.pdf" }] }
```

### By URL
```json
{ "attachments": [{ "url": "https://example.com/doc.pdf", "filename": "doc.pdf" }] }
```

### By Base64 Data
```json
{ "attachments": [{ "data": "base64...", "filename": "image.png", "mimeType": "image/png" }] }
```

---

## Task Status Lifecycle

```
POST /v1/tasks (new)
       |
       v
    running ---------> failed (check "error" field)
       |
       v
    pending (needs input) --> POST /v1/tasks with taskId to continue
       |
       v
   completed (output available, credit_usage populated)
```

## OpenAI SDK Compatibility

Manus supports the OpenAI Responses API. Use the OpenAI Python SDK:

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.manus.ai/v1", api_key="your-key")

response = client.responses.create(
    input="Analyze this data",
    model="manus-1.6",
    extra_body={"task_mode": "agent", "agent_profile": "manus-1.6"}
)

# Multi-turn
followup = client.responses.create(
    input="Break it down by quarter",
    model="manus-1.6",
    previous_response_id=response.id,
    extra_body={"task_mode": "agent", "agent_profile": "manus-1.6"}
)
```
