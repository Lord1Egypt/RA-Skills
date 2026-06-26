---
name: project-cog
description: "AI project management powered by CellCog. Knowledge workspaces, document upload, AI-processed context trees, signed URL retrieval. Works standalone or as CellCog chat context."
author: CellCog
homepage: https://cellcog.ai
metadata:
  openclaw:
    emoji: "📂"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
dependencies: [cellcog]
---
# Project Cog — Knowledge Workspaces for Agents

CellCog Projects are knowledge workspaces where documents are organized into AI-processed **Context Trees** — structured, hierarchical summaries that agents can read, search, and reason about.

## Two Ways to Use Projects

**1. With CellCog Chats** — Upload documents to a project, then pass `project_id` to `create_chat()`. CellCog agents automatically have access to all project documents and instructions.

**2. Standalone** — Use projects purely as a knowledge management layer. Upload documents, retrieve context tree summaries, get signed URLs for sharing — no CellCog chat required. Any agent can use CellCog's proprietary Context Tree data structures for its own workflows.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## Quick Start

```python
from cellcog import CellCogClient

client = CellCogClient(agent_provider="openclaw")

# 1. Create a project
project = client.create_project(
    name="Q4 Financial Analysis",
    instructions="Focus on quantitative analysis. Use conservative estimates."
)
project_id = project["id"]
ct_id = project["context_tree_id"]

# 2. Upload documents
client.upload_document(ct_id, "/data/earnings_report.pdf", "Q4 2025 earnings report")
client.upload_document(ct_id, "/data/market_analysis.xlsx", "Competitor market share data")

# 3. Wait for processing (poll until all documents are ready)
import time
while True:
    docs = client.list_documents(ct_id)
    pending = [d for d in docs["documents"]
               if d["status"] in ("PENDING_PROCESSING", "PROCESSING")]
    if not pending:
        break
    time.sleep(10)

# 4. Read the context tree — structured summary of all documents
tree = client.get_context_tree_markdown(ct_id)
print(tree["markdown"])

# 5. Use with CellCog chat

# OpenClaw agents (fire-and-forget):
result = client.create_chat(
    prompt="Based on our project documents, create a board presentation",
    project_id=project_id,
    notify_session_key="agent:main:main",  # OpenClaw only
    task_label="board-deck",
)

# All other agents (blocks until done):
result = client.create_chat(
    prompt="Based on our project documents, create a board presentation",
    project_id=project_id,
    task_label="board-deck",
)
```

---

## Project Lifecycle

### Creating Projects

```python
project = client.create_project(
    name="My Research Project",
    instructions="Optional instructions for CellCog agents working in this project"
)
# Returns: {"id": "...", "name": "...", "context_tree_id": "...", "created_at": "..."}
```

The creator is automatically an admin. Instructions are optional but help CellCog agents understand the project's purpose and work style.

### Listing Projects

```python
projects = client.list_projects()
# Returns: {"projects": [{"id", "name", "is_admin", "context_tree_id", "files_count", "created_at"}, ...]}
```

Every project in the list includes its `context_tree_id` — no need to call `get_project()` separately just to get it.

### Getting Project Details

```python
project = client.get_project(project_id)
# Returns: {"id", "name", "project_instructions", "context_tree_id", "is_admin", "created_at", ...}
```

Use `get_project()` when you need `project_instructions` or other details not included in the list.

### Updating Projects

```python
client.update_project(project_id, name="New Name", instructions="Updated instructions")
```

Admin access required.

### Deleting Projects

```python
client.delete_project(project_id)
```

Admin access required. Soft delete — contact support@cellcog.ai to recover.

---

## Document Management

All document operations use `context_tree_id`, not `project_id`. Get it from `list_projects()`, `create_project()`, or `get_project()` response.

### Uploading Documents

```python
result = client.upload_document(
    context_tree_id=ct_id,
    file_path="/path/to/document.pdf",
    brief_context="Q4 2025 earnings report with revenue breakdown"
)
# Returns: {"file_id": "...", "status": "processing", "message": "..."}
```

**Admin access required.** The project creator is automatically an admin.

**`brief_context` matters.** CellCog's AI uses it to generate better summaries in the context tree. A good brief context significantly improves the quality of the structured summary that agents will read later.

**Supported file types:** PDF, DOCX, XLSX, PPTX, CSV, TXT, MD, images (JPG/PNG/GIF/WebP/SVG), audio (MP3/WAV/AAC/FLAC), video (MP4/AVI/MOV), and code files (JS/PY/Java/Go/etc.).

**Max file size:** 100 MB per file.

**Credit usage:** Uploads are processed by a lightweight AI agent using credits, so agents can access structured summaries and decide which documents to pull into context. Credit cost varies by document size and complexity.

**Processing time:** After upload, CellCog processes the document (extracts text, generates summaries, updates the context tree). This takes 1-3 minutes for typical documents, longer for large files.

### Waiting for Document Processing

After uploading, poll until processing completes:

```python
import time
while True:
    docs = client.list_documents(ct_id)
    pending = [d for d in docs["documents"]
               if d["status"] in ("PENDING_PROCESSING", "PROCESSING")]
    if not pending:
        break
    time.sleep(10)
```

### Listing Documents

```python
docs = client.list_documents(ct_id)
# Returns: {"documents": [{"id", "original_filename", "file_type", "file_size", "status", ...}]}
```

Document status values:
- `PENDING_PROCESSING` — Queued for processing
- `PROCESSING` — Being processed
- `SUCCEEDED` — Ready and in context tree
- `ERRORED` — Processing failed (check `processing_error`)

### Deleting Documents

```python
client.delete_document(ct_id, file_id)

# Or bulk delete (up to 100 at once):
client.bulk_delete_documents(ct_id, [file_id_1, file_id_2, ...])
```

Admin access required.

---

## Context Trees — Your Knowledge Structure

After documents are processed, CellCog organizes them into a **Context Tree** — a hierarchical markdown representation with file descriptions, metadata, and content summaries. This is the same proprietary data structure that CellCog's internal agents use.

### Getting the Context Tree Markdown

```python
# Default: compact view with short summaries
tree = client.get_context_tree_markdown(ct_id)
print(tree["markdown"])

# Detailed view: includes long descriptions for each document
tree = client.get_context_tree_markdown(ct_id, include_long_description=True)
print(tree["markdown"])
```

Use `include_long_description=True` when you need full document details for deeper analysis. Default short descriptions are sufficient for most use cases and keep context windows efficient.

**Example output:**

```
## 📁 / (Q4 Financial Analysis Documents)
Document repository for Q4 Financial Analysis.

### 📁 /financials (Financial Reports)
Core financial documents and earnings data

#### 📄 /financials/earnings_report.pdf (Q4 2025 Earnings Report)
*Created: 2 hours ago*
**Type:** PDF (2.1 MB)

Comprehensive Q4 2025 earnings report with revenue breakdown by segment,
operating margins, and forward guidance. Revenue grew 15% YoY to $12.3B.

### 📁 /market (Market Data)
Competitive landscape and market research

#### 📄 /market/market_analysis.xlsx (Competitor Market Share Data)
*Created: 2 hours ago*
**Type:** XLSX (450.5 KB)

Market share analysis across 5 competitors. Includes quarterly trends,
geographic breakdown, and pricing comparison matrix.
```

### Why Context Trees Matter for Agents

1. **Understand before downloading.** Read the tree to know what's available without downloading every file.
2. **AI-processed summaries.** Each file has a description generated by CellCog's AI — not just a filename.
3. **Hierarchical organization.** Documents are organized into logical folders, making navigation intuitive.
4. **Same view as CellCog agents.** When you pass `project_id` to a CellCog chat, the agent sees this exact tree.

---

## Signed URLs — Share Your Documents

Generate time-limited, pre-authenticated download URLs for any documents in the context tree. These URLs work without CellCog authentication — pass them to other agents, tools, or humans.

### By File Path (Recommended)

Use paths directly from the context tree markdown — no file IDs needed:

```python
urls = client.get_document_signed_urls_by_path(
    context_tree_id=ct_id,
    file_paths=["/financials/earnings_report.pdf", "/market/analysis.xlsx"],
    expiration_hours=24  # Valid for 24 hours (default: 1 hour, max: 168 = 7 days)
)

# Returns:
# {
#     "urls": {"/financials/earnings_report.pdf": "https://storage.googleapis.com/...", ...},
#     "errors": {}
# }
```

### By File ID (Alternative)

Use file IDs from `list_documents()`:

```python
urls = client.get_document_signed_urls(
    context_tree_id=ct_id,
    file_ids=["file_id_1", "file_id_2"],
    expiration_hours=24
)
```

### Use Cases

- **Cross-agent sharing.** Pass URLs to other agents that need to read your documents.
- **Human sharing.** Send URLs to your human so they can download files directly.
- **External tool integration.** Pass URLs to APIs that accept file URLs (e.g., analysis services).
- **Temporary access.** Use short expiry (1 hour) for one-time access, long expiry (7 days) for ongoing workflows.

**Note:** Signed URLs remain valid for their full duration even if the user's project access is later revoked. New URLs cannot be generated after access is removed.

---

## Using Projects with CellCog Chats

Projects are first-class in CellCog. When you pass a `project_id`, CellCog agents automatically get:

- **All project documents** via the context tree
- **Project instructions** that guide agent behavior
- **Organization context** if the project belongs to an organization

**Quick start:**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",  # See cellcog skill for all modes
)
```

See https://cellcog.ai for complete SDK API reference — delivery modes, `send_message()`, timeouts, file handling, and more.

**Finding project and role IDs:**
```python
# List all projects
projects = client.list_projects()

# Get project details (includes context_tree_id)
project = client.get_project(project_id)

# List agent roles in a project
roles = client.list_agent_roles(project_id)
```

---

## API Reference

### Project Management

| Method | Description |
|--------|-------------|
| `client.list_projects()` | List all accessible projects |
| `client.create_project(name, instructions="")` | Create a new project (returns `id`, `context_tree_id`) |
| `client.get_project(project_id)` | Get project details including `context_tree_id` |
| `client.update_project(project_id, name=None, instructions=None)` | Update project (admin) |
| `client.delete_project(project_id)` | Soft delete project (admin) |

### Agent Roles (Read-Only)

| Method | Description |
|--------|-------------|
| `client.list_agent_roles(project_id)` | List active roles (for discovering `agent_role_id` values) |

### Document Management

| Method | Description |
|--------|-------------|
| `client.list_documents(context_tree_id)` | List all documents with status |
| `client.upload_document(context_tree_id, file_path, brief_context=None)` | Upload and process a document (admin) |
| `client.delete_document(context_tree_id, file_id)` | Delete a document (admin) |
| `client.bulk_delete_documents(context_tree_id, file_ids)` | Delete up to 100 documents (admin) |

### Context Tree

| Method | Description |
|--------|-------------|
| `client.get_context_tree_markdown(context_tree_id, include_long_description=False)` | Get AI-processed markdown view (set True for detailed descriptions) |
| `client.get_document_signed_urls_by_path(context_tree_id, file_paths, expiration_hours=1)` | Get download URLs by file path (recommended) |
| `client.get_document_signed_urls(context_tree_id, file_ids, expiration_hours=1)` | Get download URLs by file ID (alternative) |

---

## Human-Only Features

The following are managed by humans through the CellCog web UI at cellcog.ai:

| Feature | Why | Where |
|---------|-----|-------|
| **Member management** | Invitation flow requires email verification | cellcog.ai → Projects → Members |
| **Agent role creation/editing** | Prompt engineering best done interactively | cellcog.ai → Projects → Agent Roles |
| **Google Drive import** | OAuth requires browser interaction | cellcog.ai → Projects → Import |

Ask your human to configure these at https://cellcog.ai.

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `APIError(404)` | Project or context tree not found | Verify the ID with `list_projects()` |
| `APIError(403)` | Not a project member, or admin access required | Check membership; upload/delete require admin |
| `APIError(400)` | Invalid request (e.g., file too large, unsupported type) | Check file size (<100MB) and supported types |
| `FileUploadError` | Local file not found or upload failed | Verify file path exists and is readable |

All errors include descriptive messages. Check `error.message` for details.

---

## Tips

1. **`brief_context` is your best investment.** A one-sentence description like "Q4 2025 earnings with segment breakdown" dramatically improves the AI-generated summary in the context tree.

2. **Read the tree before downloading.** Use `get_context_tree_markdown()` to understand what's available. You often don't need to download files — the markdown summaries are sufficient for many decisions.

3. **Signed URLs enable cross-agent workflows.** Get a 24-hour URL and pass it to another agent or tool that needs the data. No CellCog auth needed on their end.

4. **Projects work without CellCog chats.** You can use projects purely as a document store with AI-processed summaries. Upload docs, read the context tree, get signed URLs — all without creating a single CellCog chat.

5. **Processing takes time.** After uploading, poll with `list_documents()` checking the `status` field. Don't use fixed sleeps — processing time varies by file size and type.

6. **Use the right `context_tree_id`.** Every project has its own context tree. Get it from `list_projects()`, `create_project()`, or `get_project()`. Don't mix context tree IDs from different projects or organizations.


---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
**Other agents:** `pip install cellcog` and set `CELLCOG_API_KEY`. See https://cellcog.ai for details.
