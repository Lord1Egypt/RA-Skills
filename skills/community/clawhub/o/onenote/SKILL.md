---
name: onenote-notes
description: Manage OneNote notebooks, sections, pages, and page content via Microsoft Graph API. Use this skill when users want to read, create, or update OneNote pages, manage sections and notebooks, and work with page content as HTML via the OneNote API.
---

# OneNote Notes

![OneNote Notes](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/onenote.svg)

Access OneNote via Microsoft Graph API with managed OAuth authentication. Manage notebooks, sections, and pages; read and update page content as HTML; and navigate the OneNote hierarchy.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onenote-notes) for hosted connection flows and credentials so you do not need to configure OneNote API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect OneNote |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect OneNote |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Microsoft Graph  │
│   (User Chat)   │     │   (OAuth)    │     │  (OneNote API)   │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect OneNote   │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ OneNote  │
    │  File    │           │ Auth     │           │ Notebooks│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for OneNote again."

## Quick Start

```bash
# List user's notebooks
clawlink_call_tool --tool "onenote_list_user_notebooks" --params '{"user_id": "me"}'

# List sections in a notebook
clawlink_call_tool --tool "onenote_list_user_notebook_sections" --params '{"user_id": "me", "notebook_id": "NOTEBOOK_ID"}'

# Get page content
clawlink_call_tool --tool "onenote_get_me_section_page_content" --params '{"section_id": "SECTION_ID", "page_id": "PAGE_ID"}'
```

## Authentication

All OneNote tool calls are authenticated automatically by ClawLink using the user's connected Microsoft account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Microsoft Graph request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=onenote and connect OneNote.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `onenote` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration onenote
```

**Response:** Returns the live tool catalog for OneNote.

### Reconnect

If OneNote tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=onenote
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration onenote`

## Security & Permissions

- Access is scoped to notebooks, sections, and pages within the connected Microsoft account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete page content, delete section) must be confirmed.
- Copy operations are asynchronous — poll the operation status endpoint until complete.

## Tool Reference

### Notebook Operations

| Tool | Description | Mode |
|------|-------------|------|
| `onenote_list_user_notebooks` | List all notebooks for a user | Read |
| `onenote_get_user_notebook` | Get notebook properties by ID | Read |
| `onenote_get_notebook_from_web_url` | Get notebook from SharePoint or OneNote URL | Read |
| `onenote_create_me_notebooks` | Create a new notebook for the signed-in user | Write |
| `onenote_copy_onenote_site_notebook` | Copy a SharePoint site notebook | Write |
| `onenote_copy_onenote_group_notebook` | Copy a Microsoft 365 group notebook | Write |

### Section Operations

| Tool | Description | Mode |
|------|-------------|------|
| `onenote_list_user_notebook_sections` | List sections in a user's notebook | Read |
| `onenote_get_site_sections` | Get a SharePoint site section by ID | Read |
| `onenote_get_group_sections` | Get a Microsoft 365 group section by ID | Read |
| `onenote_create_site_notebooks_sections` | Create a section in a SharePoint notebook | Write |
| `onenote_create_me_sections_pages` | Create a page in a user's section | Write |
| `onenote_create_user_notebooks_sections` | Create a section in a user's notebook | Write |
| `onenote_update_me_sections` | Rename a section | Write |
| `onenote_update_site_notebooks_sections` | Update a SharePoint section | Write |
| `onenote_update_user_notebooks_sections` | Update a user's section | Write |
| `onenote_copy_section_to_notebook2` | Copy a section to another notebook | Write |
| `onenote_copy_section_to_notebook_for_user2` | Copy a section to a user's notebook | Write |

### Page Operations

| Tool | Description | Mode |
|------|-------------|------|
| `onenote_list_me_onenote_sections_pages4` | List pages in a user's section | Read |
| `onenote_get_me_section_page_content` | Get HTML content of a user's page | Read |
| `onenote_get_onenote_user_page_content` | Get HTML content of a user's page by ID | Read |
| `onenote_list_site_pages_content` | Get HTML content of a SharePoint site page | Read |
| `onenote_get_site_pages_preview` | Get text preview of a SharePoint page | Read |
| `onenote_create_me_sections_pages` | Create a new page in a section | Write |
| `onenote_create_site_notebooks_sections` | Create a page in a SharePoint site section | Write |
| `onenote_update_me_page_content` | Update page content via HTML patch commands | Write |
| `onenote_update_onenote_page_content` | Update a group page's content | Write |
| `onenote_update_site_pages_content` | Update a SharePoint page's content | Write |
| `onenote_delete_onenote_group_sections_pages2` | Delete a page from a group notebook | Write |
| `onenote_delete_site_pages` | Delete a SharePoint site page | Write |
| `onenote_delete_user_onenote_sections_pages` | Delete a page from a user's section | Write |
| `onenote_delete_user_pages` | Delete a user's OneNote page | Write |
| `onenote_delete_onenote_group_section_group_page_content` | Delete page content from a section group | Write |

### Section Group Operations

| Tool | Description | Mode |
|------|-------------|------|
| `onenote_list_group_notebook_section_groups` | List section groups in a group notebook | Read |
| `onenote_get_notebook_section_group` | Get a section group from a group notebook | Read |
| `onenote_list_onenote_group_section_groups_section_groups2` | List nested section groups | Read |
| `onenote_list_group_section_groups_sections` | List sections in a section group | Read |
| `onenote_count_notebooks_section_groups_sections` | Count sections in a section group | Read |
| `onenote_create_onenote_group_notebooks_section_groups` | Create a section group in a group notebook | Write |
| `onenote_create_group_section_groups_sections` | Create a section in a section group | Write |
| `onenote_update_site_section_groups_sections` | Update a section in a section group | Write |

### Async Operation Status

| Tool | Description | Mode |
|------|-------------|------|
| `onenote_get_onenote_group_operations` | Check status of a group async operation | Read |
| `onenote_get_onenote_site_operations` | Check status of a SharePoint async operation | Read |

## Code Examples

### List notebooks

```bash
clawlink_call_tool --tool "onenote_list_user_notebooks" \
  --params '{
    "user_id": "me"
  }'
```

### Get page content

```bash
clawlink_call_tool --tool "onenote_get_me_section_page_content" \
  --params '{
    "section_id": "SECTION_ID",
    "page_id": "PAGE_ID"
  }'
```

### Create a new page

```bash
clawlink_call_tool --tool "onenote_create_me_sections_pages" \
  --params '{
    "section_id": "SECTION_ID",
    "html": "<html><head><title>New Page</title></head><body><p>Page content here.</p></body></html>"
  }'
```

### Update page content

```bash
clawlink_call_tool --tool "onenote_update_me_page_content" \
  --params '{
    "page_id": "PAGE_ID",
    "commands": [
      {
        "action": "append",
        "target": "body",
        "content": "<p>New paragraph added via API.</p>"
      }
    ]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm OneNote is connected.
2. Call `clawlink_list_tools --integration onenote` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `onenote`.
5. If no OneNote tools appear, direct the user to https://claw-link.dev/dashboard?add=onenote.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List notebooks → Read sections → Show results    │
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

- Page content must be provided as valid HTML with proper `html`, `head`, and `body` tags.
- Asynchronous copy operations return a 202 Accepted with an Operation-Location header — poll this endpoint to check completion.
- Section names must be 50 characters or fewer and cannot contain: `?*/:<>|&#''%~`.
- Notebook names must be 128 characters or fewer and cannot contain: `?*\/:<>|&'"`.
- Only the `displayName` property can be updated on sections — other properties are read-only.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration onenote`. |
| Missing connection | OneNote is not connected. Direct the user to https://claw-link.dev/dashboard?add=onenote. |
| `notFound` | Notebook, section, or page does not exist. Check the ID. |
| `InvalidArgument` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Operation pending | Async operation still in progress. Poll the Operation-Location endpoint. |
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

1. Ensure the integration slug is exactly `onenote`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Microsoft Graph OneNote API Overview](https://learn.microsoft.com/en-us/graph/api/resources/onenote)
- [OneNote Notebook Resource](https://learn.microsoft.com/en-us/graph/api/resources/notebook)
- [OneNote Page Resource](https://learn.microsoft.com/en-us/graph/api/resources/page)
- [OneNote Section Resource](https://learn.microsoft.com/en-us/graph/api/resources/section)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onenote-notes
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [OneDrive Files](https://clawhub.ai/hith3sh/onedrive-files) — For general OneDrive file management
- [Microsoft Excel](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) — For Excel workbook operations
- [Outlook Inbox](https://clawhub.ai/hith3sh/outlook-inbox) — For Outlook email and calendar

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onenote-notes)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
