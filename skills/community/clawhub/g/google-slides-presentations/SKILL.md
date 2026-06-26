---
name: google-slides-presentations
description: Google Slides API integration with managed OAuth. Inspect presentations, create or update slide content, manage layouts, and coordinate presentation workflows. Use this skill when users want to work with Google Slides decks programmatically.
---

# Google Slides

![Google Slides](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-slides.svg?v=2)

Access Google Slides via the Google Slides API with managed OAuth authentication. Inspect presentations, create or update slide content, manage layouts, and coordinate deck workflows.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-slides-presentations) for hosted connection flows and credentials so you do not need to configure Google Slides API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Slides |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Slides |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Slides  │
│   (User Chat)   │     │   (OAuth)    │     │   (Slides API)   │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Slides     │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Slides  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Slides again."

## Quick Start

```bash
# Search for presentations
clawlink_call_tool --tool "googleslides_search_presentations" --params '{"query": "sales deck"}'

# Get presentation details
clawlink_call_tool --tool "googleslides_get_presentation" --params '{"presentation_id": "YOUR_PRESENTATION_ID"}'

# List slides
clawlink_call_tool --tool "googleslides_list_slides" --params '{"presentation_id": "YOUR_PRESENTATION_ID"}'
```

## Authentication

All Google Slides tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Slides API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-slides and connect Google Slides.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-slides` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-slides
```

**Response:** Returns the live tool catalog for Google Slides.

### Reconnect

If Google Slides tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-slides
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-slides`

## Security & Permissions

- Access is scoped to presentations within the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete slides, delete elements) are marked as high-impact and must be confirmed.
- Presentation sharing permissions should be reviewed before making changes.

## Tool Reference

### Presentation Discovery & Reading

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_search_presentations` | Search for presentations by name or query | Read |
| `googleslides_get_presentation` | Get a presentation's metadata and slide list | Read |
| `googleslides_get_presentation_thumbnail` | Get thumbnail images of slides | Read |
| `googleslides_list_slides` | List all slides in a presentation | Read |
| `googleslides_get_slide` | Get a specific slide's metadata and element list | Read |
| `googleslides_get_page_thumbnail` | Get a thumbnail for a specific slide | Read |

### Presentation Creation

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_create_presentation` | Create a new empty presentation | Write |
| `googleslides_create_slide` | Add a new slide to an existing presentation | Write |
| `googleslides_copy_presentation` | Create a copy of an existing presentation | Write |

### Text Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_insert_text` | Insert text into a text box or shape | Write |
| `googleslides_replace_all_text` | Replace text throughout a presentation | Write |
| `googleslides_update_text_style` | Update text formatting (font, size, color, bold, etc.) | Write |

### Shape & Element Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_create_shape` | Create a shape on a slide | Write |
| `googleslides_create_image` | Insert an image onto a slide | Write |
| `googleslides_create_line` | Create a line or connector on a slide | Write |
| `googleslides_update_shape_properties` | Update shape fill, stroke, and shadow | Write |
| `googleslides_delete_object` | Delete an element (shape, image, table, etc.) from a slide | Write |

### Table Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_create_table` | Insert a table onto a slide | Write |
| `googleslides_update_table_row_height` | Update a table row's height | Write |
| `googleslides_update_table_column_width` | Update a table column's width | Write |
| `googleslides_insert_table_rows` | Insert rows into a table | Write |
| `googleslides_delete_table_row` | Delete a row from a table | Write |

### Layout & Theme

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_list_page_layouts` | List available page layouts | Read |
| `googleslides_update_page_element_transform` | Move, resize, or rotate an element | Write |
| `googleslides_update_slide_position` | Reorder slides within a presentation | Write |
| `googleslides_update_theme` | Update the presentation theme or color scheme | Write |

### Presentation-Level Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_update_presentation_title` | Rename a presentation | Write |
| `googleslides_batch_update_presentation` | Execute multiple operations in a single request | Write |
| `googleslides_export_presentation` | Export a presentation as PDF or other format | Read |

### Copy Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googleslides_copy_slide` | Duplicate a slide within or across presentations | Write |
| `googleslides_duplicate_object` | Duplicate any presentation object | Write |

## Code Examples

### Search for presentations

```bash
clawlink_call_tool --tool "googleslides_search_presentations" \
  --params '{
    "query": "Q4 sales deck"
  }'
```

### Get presentation and list slides

```bash
clawlink_call_tool --tool "googleslides_get_presentation" \
  --params '{
    "presentation_id": "YOUR_PRESENTATION_ID"
  }'
```

### Create a new presentation

```bash
clawlink_call_tool --tool "googleslides_create_presentation" \
  --params '{
    "title": "Product Launch Deck"
  }'
```

### Insert text into a placeholder

```bash
clawlink_call_tool --tool "googleslides_insert_text" \
  --params '{
    "presentation_id": "YOUR_PRESENTATION_ID",
    "page_id": "SLIDE_PAGE_ID",
    "text": "Welcome to our presentation!",
    "element_id": "YOUR_ELEMENT_ID"
  }'
```

### Replace text throughout a presentation

```bash
clawlink_call_tool --tool "googleslides_replace_all_text" \
  --params '{
    "presentation_id": "YOUR_PRESENTATION_ID",
    "replace_text": "New Company Name",
    "search_text": "Old Company Name"
  }'
```

### Create a new slide

```bash
clawlink_call_tool --tool "googleslides_create_slide" \
  --params '{
    "presentation_id": "YOUR_PRESENTATION_ID",
    "layout_index": 1
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Slides is connected.
2. Call `clawlink_list_tools --integration google-slides` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-slides`.
5. If no Google Slides tools appear, direct the user to https://claw-link.dev/dashboard?add=google-slides.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  search → get → list → call                                │
│                                                             │
│  Example: List slides → Get details → Show results         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Presentation IDs are the long ID string in the presentation URL.
- Slide IDs and element IDs can be obtained from `get_presentation` or `get_slide` responses.
- `batch_update_presentation` allows combining multiple operations into a single API call for efficiency.
- Text insertion requires knowing the target element ID (text box or shape).
- Layouts control the placement and styling of placeholders on new slides.
- Thumbnail operations return image data useful for previews.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-slides`. |
| Missing connection | Google Slides is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-slides. |
| `RESOURCE_NOT_FOUND` | Presentation or slide does not exist. Check the ID. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
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

1. Ensure the integration slug is exactly `google-slides`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Slides API Overview](https://developers.google.com/slides)
- [Presentations Reference](https://developers.google.com/slides/reference/rest/v1/presentations)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-slides-presentations
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Docs](https://clawhub.ai/hith3sh/google-docs-documents) — For document reading and editing
- [Google Drive](https://clawhub.ai/hith3sh/google-drive-files) — For file management and Drive-level operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-slides-presentations)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)