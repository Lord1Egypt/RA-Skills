---
name: pandadoc-documents
description: Create and manage PandaDoc documents, templates, folders, and contacts via the PandaDoc API. Use this skill when users want to create documents from templates, manage document workflows, track signature status, and coordinate document signing via PandaDoc.
---

# PandaDoc Documents

![PandaDoc Documents](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/pandadoc.svg)

Access PandaDoc's document platform via the PandaDoc API. Create documents from templates or file uploads, manage folders, track document status, and coordinate signature workflows.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pandadoc-documents) for hosted connection flows and credentials so you do not need to configure PandaDoc API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect PandaDoc |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect PandaDoc |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  PandaDoc API │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │ 3. Connect PandaDoc │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼ ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ PandaDoc │
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

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for PandaDoc again."

## Quick Start

```bash
# List documents
clawlink_call_tool --tool "pandadoc_list_documents" --params '{"status": "document.draft"}'

# Get document details
clawlink_call_tool --tool "pandadoc_get_document_details" --params '{"document_id": "DOCUMENT_ID"}'

# List templates
clawlink_call_tool --tool "pandadoc_list_templates" --params '{}'
```

## Authentication

All PandaDoc tool calls are authenticated automatically by ClawLink using the user's connected PandaDoc account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every PandaDoc API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=pandadoc and connect PandaDoc.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `pandadoc` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration pandadoc
```

**Response:** Returns the live tool catalog for PandaDoc.

### Reconnect

If PandaDoc tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=pandadoc
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration pandadoc`

## Security& Permissions

- Access is scoped to documents, templates, folders, and contacts within the connected PandaDoc account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete template, delete contact) must be confirmed.
- Document sending and workflow triggers affect external parties — confirm before executing.

## Tool Reference

### Document Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pandadoc_list_documents` | List documents with optional status filter | Read |
| `pandadoc_get_document_details` | Get document metadata, recipients, fields, and status | Read |
| `pandadoc_create_document_from_file` | Create a document by uploading PDF, DOCX, or RTF | Write |
| `pandadoc_create_document_from_template` | Create a document from an existing template | Write |
| `pandadoc_move_document_to_folder` | Move a draft document to a folder | Write |
| `pandadoc_create_document_attachment` | Add an attachment to a draft document | Write |
| `pandadoc_send_document` | Send a document for signature | Write |

### Template Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pandadoc_list_templates` | List templates with optional filters | Read |
| `pandadoc_get_template_details` | Get template metadata and content details | Read |
| `pandadoc_create_template` | Create a template from PDF or scratch | Write |
| `pandadoc_delete_template` | Delete a template permanently | Write |

### Folder Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pandadoc_list_document_folders` | List all document folders | Read |
| `pandadoc_create_folder` | Create a new folder | Write |

### Contact Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pandadoc_list_contacts` | List all contacts | Read |
| `pandadoc_create_or_update_contact` | Create or update a contact by email | Write |
| `pandadoc_delete_contact` | Delete a contact permanently | Write |

### Webhook Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pandadoc_create_webhook` | Create a webhook subscription | Write |

## Code Examples

### List documents

```bash
clawlink_call_tool --tool "pandadoc_list_documents" \
  --params '{
    "status": "document.sent",
    "limit": 50
  }'
```

### Get document details

```bash
clawlink_call_tool --tool "pandadoc_get_document_details" \
  --params '{
    "document_id": "DOCUMENT_ID"
  }'
```

### Create a document from template

```bash
clawlink_call_tool --tool "pandadoc_create_document_from_template" \
  --params '{
    "template_id": "TEMPLATE_ID",
    "recipients": [
      {
        "email": "client@example.com",
        "name": "Jane Client",
        "role": "Signer"
      }
    ],
    "data": {
      "company_name": "Acme Corp",
      "contract_value": "$50,000"
    }
  }'
```

### Create or update a contact

```bash
clawlink_call_tool --tool "pandadoc_create_or_update_contact" \
  --params '{
    "email": "newcontact@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "company": "Acme Corp"
  }'
```

## Notes

- Documents can only be moved when in `document.draft` status.
- Templates can be filtered by name, shared status, and deleted status.
- File uploads for document creation accept PDF, DOCX, and RTF formats.
- Attachments are limited to 10 files per document, max 50 MB each.
- Contacts are matched by email — creating with an existing email updates that contact.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration pandadoc`. |
| Missing connection | PandaDoc is not connected. Direct the user to https://claw-link.dev/dashboard?add=pandadoc. |
| `not_found` | Document, template, or contact does not exist. Check the ID. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `state_error` | Document is not in the required state (e.g., moving a non-draft document). |
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

1. Ensure the integration slug is exactly `pandadoc`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [PandaDoc API Documentation](https://developers.pandadoc.com/)
- [Document API](https://developers.pandadoc.com/reference/documents)
- [Template API](https://developers.pandadoc.com/reference/templates)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pandadoc-documents
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [PandaDoc](https://clawhub.ai/hith3sh/pandadoc-documents) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pandadoc-documents)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
