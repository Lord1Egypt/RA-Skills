---
name: oo-feishu-app-bot
description: "Feishu App Bot (open.feishu.cn). Use this skill for ANY Feishu App Bot request — reading, creating, updating, and deleting data. Whenever a task involves Feishu App Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Feishu App Bot"
  author: "OOMOL"
  version: "1.0.11"
  services: ["feishu_app_bot"]
  icon: "https://static.oomol.com/logo/third-party/feishu_app_bot.svg"
---

# Feishu App Bot

Operate **Feishu App Bot** through your OOMOL-connected account. This skill calls the `feishu_app_bot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Feishu App Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "feishu_app_bot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "feishu_app_bot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_chat_members` — Add users or bots to a Feishu chat. [write]
- `add_drive_permission` — Grant a collaborator permission on a Feishu Drive resource. [write]
- `add_message_reaction` — Add one emoji reaction to a Feishu/Lark message. [write]
- `add_task_comment` — Add a text comment to a Feishu task. [write]
- `add_task_to_tasklist` — Add a Feishu task to a tasklist. [write]
- `add_wiki_member` — Add a member to a Feishu Wiki space. [write]
- `arrange_base_dashboard` — Ask Feishu to automatically arrange dashboard blocks. [write]
- `batch_create_base_records` — Create up to 200 records in one Feishu Base request. [write]
- `batch_create_okrs` — Create objectives and their key results sequentially, with optional rollback on failure. [write]
- `batch_delete_base_records` — Delete up to 200 records in one Feishu Base request. [destructive]
- `batch_get_messages` — Fetch up to 50 Feishu messages by message ID in one request.
- `batch_update_base_records` — Update up to 200 records with record-specific fields in one Feishu Base request. [write]
- `batch_update_sheet` — Execute multiple Sheet AI write tools in one batch request. [destructive]
- `clear_cells` — Clear cell contents, formats, or both from an A1 range. [destructive]
- `complete_task` — Mark a Feishu task as completed. [write]
- `copy_base` — Copy a Feishu Base, optionally changing its name, destination folder, content inclusion, or time zone. [write]
- `copy_drive_file` — Copy a Feishu Drive file or online document into another folder. [write]
- `copy_sheet_range` — Copy a cell range. [write]
- `copy_wiki_node` — Copy a Feishu Wiki node into another space or below another parent. [write]
- `create_app_slash_command` — Register a slash command, optionally updating the existing command when its name already exists. [write]
- `create_base` — Create a Feishu Base, optionally replacing its default table with a custom initial schema. [write]
- `create_base_block` — Create a folder, table, document, dashboard, or workflow block. [write]
- `create_base_dashboard` — Create a dashboard in a Base. [write]
- `create_base_dashboard_block` — Create a chart, metric, or text block in a Base dashboard. [write]
- `create_base_field` — Create one field in a Feishu Base table. [write]
- `create_base_form` — Create a form in a Base table. [write]
- `create_base_form_questions` — Create up to ten questions in a Base form. [write]
- `create_base_record` — Create one record in a Feishu Base table. [write]
- `create_base_record_share_links` — Generate share links for up to 100 Base records. [write]
- `create_base_role` — Create a custom Base role from a complete permission configuration. [write]
- `create_base_table` — Create a table with an optional initial field schema in a Feishu Base. [write]
- `create_base_views` — Create one or more views sequentially in a Feishu Base table. [write]
- `create_base_workflow` — Create a disabled Base workflow from a complete definition. [write]
- `create_calendar_event` — Create a Feishu calendar event and add attendees, rolling back the event if attendee creation fails. [write]
- `create_chat` — Create a Feishu group or topic chat with initial users and bots. [write]
- `create_document` — Create a Feishu document from Docx XML or Markdown content, optionally inside a folder or Wiki node. [write]
- `create_drive_comment` — Create a full-resource or anchored rich-text comment on a Feishu Drive document or supported file. [write]
- `create_drive_comment_reply` — Add a rich-text reply to a Feishu Drive comment. [write]
- `create_drive_folder` — Create a folder in Feishu Drive. [write]
- `create_drive_shortcut` — Create a Feishu Drive shortcut to an existing file in another folder. [write]
- `create_mail_template` — Create a personal Feishu mail template from JSON content and existing Drive-backed attachments. [write]
- `create_markdown_file` — Create a Markdown file from a JSON string in Feishu Drive root, a Drive folder, or a Wiki node. [write]
- `create_okr` — Create one Feishu objective or key result from plain text. [write]
- `create_okr_alignment` — Align one Feishu OKR objective to another objective. [write]
- `create_okr_progress` — Create a progress record for an objective or key result. [write]
- `create_sheet` — Create an empty sub-sheet with optional position and dimensions. [write]
- `create_sheet_chart` — Create a chart object. [write]
- `create_sheet_conditional_format` — Create a conditional format object. [write]
- `create_sheet_filter` — Create a filter object. [write]
- `create_sheet_filter_view` — Create a filter view object. [write]
- `create_sheet_float_image` — Create a float image object. [write]
- `create_sheet_pivot_table` — Create a pivot table object. [write]
- `create_sheet_sparkline` — Create a sparkline object. [write]
- `create_slide` — Create a page in an existing Feishu Slides presentation. [write]
- `create_slides_presentation` — Create a Feishu Slides presentation and optionally add up to ten initial pages. [write]
- `create_task` — Create a Feishu task with members, dates, reminders, and tasklist membership. [write]
- `create_tasklist` — Create a Feishu tasklist. [write]
- `create_whiteboard_diagram` — Create a Mermaid, PlantUML, or SVG diagram node in a Feishu whiteboard. [write]
- `create_whiteboard_nodes` — Create raw OpenAPI nodes in a Feishu whiteboard, optionally replacing all existing content. [write]
- `create_wiki_node` — Create a document node in a Feishu Wiki space. [write]
- `create_workbook` — Create a Feishu spreadsheet workbook. [write]
- `delete_app_slash_command` — Permanently delete a slash command selected by command ID or exact command name. [destructive]
- `delete_base_block` — Delete a Base resource block. [destructive]
- `delete_base_dashboard` — Delete a Base dashboard and its blocks. [destructive]
- `delete_base_dashboard_block` — Delete a block from a Base dashboard. [destructive]
- `delete_base_field` — Delete one field from a Feishu Base table. [destructive]
- `delete_base_form` — Delete a form from a Base table. [destructive]
- `delete_base_form_questions` — Delete up to ten questions from a Base form. By default this also deletes the underlying fields and record data; set keepFields to preserve them. [destructive]
- `delete_base_record` — Delete one record from a Feishu Base table. [destructive]
- `delete_base_role` — Delete a custom Base role; system roles cannot be deleted. [destructive]
- `delete_base_table` — Delete a table from a Feishu Base. [destructive]
- `delete_base_view` — Delete one view from a Feishu Base table by ID or accepted view name. [destructive]
- `delete_calendar_event` — Delete a Feishu calendar event. [destructive]
- `delete_document_cover` — Idempotently clear the cover of a Feishu docx document. [write]
- `delete_drive_comment` — Delete a Feishu Drive comment. [destructive]
- `delete_drive_comment_reply` — Delete a reply from a Feishu Drive comment. [destructive]
- `delete_drive_item` — Delete a Feishu Drive file or folder and return a task ID when Feishu processes the deletion asynchronously. [destructive]
- `delete_drive_version` — Permanently delete a specific historical version of a Feishu Drive file. [destructive]
- `delete_okr_alignment` — Delete a Feishu OKR objective alignment. [destructive]
- `delete_okr_progress` — Delete a Feishu OKR progress record. [destructive]
- `delete_sheet` — Delete one sub-sheet from a workbook. [destructive]
- `delete_sheet_chart` — Delete a chart object. [destructive]
- `delete_sheet_conditional_format` — Delete a conditional format object. [destructive]
- `delete_sheet_dimension` — Delete rows or columns in a sub-sheet. [destructive]
- `delete_sheet_dropdowns` — Remove dropdown validation from multiple sheet-prefixed ranges. [write]
- `delete_sheet_filter` — Delete a filter object. [destructive]
- `delete_sheet_filter_view` — Delete a filter view object. [destructive]
- `delete_sheet_float_image` — Delete a float image object. [destructive]
- `delete_sheet_pivot_table` — Delete a pivot table object. [destructive]
- `delete_sheet_sparkline` — Delete a sparkline object. [destructive]
- `delete_slide` — Delete a page from a Feishu Slides presentation. [destructive]
- `delete_wiki_node` — Delete a Feishu Wiki node and optionally its descendants. [destructive]
- `delete_wiki_space` — Delete a Feishu Wiki space and return either synchronous completion or an asynchronous task ID. [destructive]
- `diff_markdown_file` — Compute a unified line diff between Drive versions or between a Drive version and a JSON Markdown string.
- `disable_base_advanced_permissions` — Disable advanced permissions for a Base. [destructive]
- `disable_base_workflow` — Disable a Base workflow without changing its steps. [destructive]
- `download_base_attachments` — Read Base attachment metadata and download selected or all record attachments into connector transit storage.
- `download_docs_media` — Download Feishu document media or a whiteboard image into connector transit storage.
- `download_document_cover` — Read a Feishu docx document cover and download its image into connector transit storage.
- `download_drive_cover` — Download a stable Drive cover preset into connector transit storage.
- `download_drive_export` — Download a generated Drive export file into connector transit storage.
- `download_drive_file` — Download a Feishu Drive file into connector transit storage.
- `download_drive_preview` — Resolve a requested Drive preview type and download the ready artifact into connector transit storage.
- `download_file` — Download one Feishu/Lark file by file key and upload it to transit storage.
- `download_image` — Download one Feishu/Lark image by image key and upload it to transit storage.
- `download_message_resource` — Download one image or file resource attached to a Feishu message into connector transit storage.
- `download_minutes_media` — Resolve and stream a Feishu Minutes audio or video recording into connector transit storage.
- `edit_message` — Edit a Feishu/Lark text or post message sent by the app bot. [write]
- `enable_base_advanced_permissions` — Enable advanced permissions for a Base. [write]
- `enable_base_workflow` — Enable a Base workflow without changing its steps. [write]
- `export_whiteboard_svg` — Export a Feishu whiteboard as SVG and return the API's Base64 payload without writing a local file.
- `fetch_document` — Fetch a Feishu document as Docx XML or Markdown, with optional structural detail and partial-read selection.
- `fetch_markdown_file` — Fetch the latest or a specific version of a Markdown file from Feishu Drive.
- `fill_sheet_range` — Fill a destination range from a source pattern. [write]
- `find_calendar_rooms` — Find meeting rooms available for the specified event time slots.
- `freeze_sheet_dimension` — Freeze or unfreeze the leading rows or columns. [write]
- `get_app_info` — Get the Feishu custom app profile and configured scopes for this connection.
- `get_app_permissions` — Get the currently published Feishu app version, tenant scopes, and subscribed events.
- `get_base` — Get the metadata of a Feishu Base.
- `get_base_dashboard` — Get a Base dashboard.
- `get_base_dashboard_block` — Get a Base dashboard block and its data configuration.
- `get_base_dashboard_block_data` — Get the computed chart data for a Base dashboard block.
- `get_base_field` — Get one field from a Feishu Base table.
- `get_base_form` — Get a form configured for a Base table.
- `get_base_form_detail` — Get public form questions and submission metadata by share token.
- `get_base_record` — Get one record from a Feishu Base table.
- `get_base_role` — Get a Base role and its complete permission configuration.
- `get_base_table` — Get one table in a Feishu Base.
- `get_base_view` — Get one view from a Feishu Base table.
- `get_base_view_card` — Get the card configuration of a Base view.
- `get_base_view_filter` — Get the filter configuration of a Base view.
- `get_base_view_group` — Get the grouping configuration of a Base view.
- `get_base_view_sort` — Get the sorting configuration of a Base view.
- `get_base_view_timebar` — Get the timeline configuration of a Base view.
- `get_base_view_visible_fields` — Get the visible field IDs of a Base view.
- `get_base_workflow` — Get a Base workflow including its steps.
- `get_calendar_event` — Get the complete details of one Feishu calendar event.
- `get_cells` — Read one or more A1 ranges with values, formulas, and optional styles.
- `get_chat` — Fetch one Feishu/Lark chat by `chat_id`.
- `get_document_creation` — Get a document creation task status and its completed document. Do not repeat creation while the task is processing.
- `get_document_revert_status` — Get the status of a Feishu document history revert task.
- `get_drive_export` — Get the normalized status and generated file token of a Drive export task.
- `get_drive_import` — Get the normalized status and created document token of a Drive import task.
- `get_drive_permission_settings` — Get public access, sharing, collaborator management, security, and comment permission settings for a Feishu Drive resource. Download restrictions can only be determined when the corresponding fields are returned; this does not test a user's effective download permission.
- `get_drive_task_status` — Get the current state of an asynchronous Drive move, copy, or delete task.
- `get_drive_version` — Download one specific Feishu Drive file version into connector transit storage.
- `get_mail_message` — Read one Feishu mail message with body and attachment metadata.
- `get_mail_recall_detail` — Get asynchronous recall progress and per-recipient results for one Feishu mail message.
- `get_mail_thread` — Read every message in a Feishu mail thread in chronological order.
- `get_message` — Fetch one Feishu/Lark message by `message_id`.
- `get_message_read_users` — List users who have read a Feishu message.
- `get_okr_comment` — Get one Feishu OKR comment by ID.
- `get_okr_cycle_detail` — List every objective in an OKR cycle and fetch the key results below each objective.
- `get_okr_progress` — Get one Feishu OKR progress record.
- `get_sheet` — Get one sub-sheet from a workbook structure.
- `get_sheet_changeset` — Get the raw spreadsheet edit actions between two revisions for reviewing applied changes.
- `get_sheet_dropdown` — Read dropdown validation metadata for a range.
- `get_sheet_history_revert_status` — Poll the status of a spreadsheet history revert.
- `get_slide` — Get one Feishu Slides page as SML 2.0 XML by stable ID or page number.
- `get_slides_presentation` — Get the complete SML 2.0 XML of a Feishu Slides presentation.
- `get_slides_revert_status` — Get the status of a Slides history revert task.
- `get_slides_screenshots` — Render up to ten existing Slides pages and store the decoded screenshots in connector transit storage.
- `get_task` — Get one Feishu task by GUID.
- `get_typed_table` — Read a sub-sheet range into a DataFrame-friendly typed table with inferred dtypes.
- `get_user` — Get a Feishu user profile. User identity may omit userId to return the authenticated user.
- `get_wiki_node` — Resolve a Feishu Wiki node by node token or document token; the server detects the token type.
- `get_wiki_space` — Get one Feishu Wiki space by ID.
- `get_wiki_task` — Get a normalized Wiki asynchronous task status.
- `get_workbook` — Get workbook structure and metadata, including all sub-sheets.
- `group_sheet_dimension` — Group rows or columns in a sub-sheet. [write]
- `hide_sheet_dimension` — Hide rows or columns in a sub-sheet. [write]
- `insert_docs_media` — Append an image or file to a Feishu docx document by creating a block, uploading media, and binding the file token with rollback on failure. [write]
- `insert_sheet_dimension` — Insert blank rows or columns into a sub-sheet. [write]
- `inspect_drive_item` — Inspect a Feishu Drive token to resolve its canonical type, title, URL, and underlying document for Wiki nodes.
- `join_vc_meeting` — Join a Feishu video meeting with the app's meeting bot. [write]
- `leave_vc_meeting` — Leave a Feishu video meeting previously joined by the app's meeting bot. [destructive]
- `list_active_vc_meetings` — List active Feishu video meetings for the current user or a tenant user.
- `list_app_slash_commands` — List every slash command registered on the currently connected Feishu app.
- `list_base_blocks` — List folders, tables, documents, dashboards, and workflows in a Base.
- `list_base_dashboard_blocks` — List blocks in a Base dashboard.
- `list_base_dashboards` — List dashboards in a Base.
- `list_base_fields` — List the fields in a Feishu Base table.
- `list_base_form_questions` — List questions configured for a Base form.
- `list_base_forms` — List forms configured for a Base table.
- `list_base_record_history` — List the change history for one Base record.
- `list_base_records` — List records in a Feishu Base table with optional projection, filter, and sort.
- `list_base_roles` — List roles configured for Base advanced permissions.
- `list_base_tables` — List tables in a Feishu Base.
- `list_base_views` — List the views in a Feishu Base table.
- `list_base_workflows` — List and optionally filter workflows in a Base.
- `list_calendar_agenda` — List event instances in a Feishu calendar over a bounded time range.
- `list_chat_members` — List visible members in one Feishu/Lark chat.
- `list_chats` — List chats that the Feishu/Lark app bot currently belongs to.
- `list_department_users` — List users in a Feishu department visible to the app.
- `list_departments` — List child departments below a Feishu department visible to the app.
- `list_document_history` — List historical versions of a Feishu docx document.
- `list_drive_comments` — List comments on a Feishu Drive document or supported file.
- `list_drive_files` — List files, folders, and online documents inside a Feishu Drive folder.
- `list_drive_permissions` — List collaborators and permission roles on a Feishu Drive resource.
- `list_drive_previews` — List available preview artifacts and generation states for a Feishu Drive file.
- `list_drive_versions` — List one page of tagged version history for a Feishu Drive file.
- `list_mail_messages` — List message IDs in a Feishu mailbox folder or label.
- `list_message_reactions` — List emoji reactions on one Feishu/Lark message.
- `list_messages` — List Feishu/Lark history messages from a chat or thread.
- `list_okr_alignments` — List the objectives aligned from or to a Feishu OKR objective.
- `list_okr_categories` — List enabled and disabled Feishu OKR categories configured by the tenant.
- `list_okr_comments` — List one page of comments attached to a Feishu OKR entity.
- `list_okr_cycles` — List Feishu OKR cycles visible to a user.
- `list_okr_progress` — List progress records for an objective or key result.
- `list_pins` — List pin records in one Feishu/Lark chat and time window.
- `list_sheet_charts` — List charts on a sub-sheet.
- `list_sheet_conditional_formats` — List conditional formats on a sub-sheet.
- `list_sheet_filter_views` — List filter views on a sub-sheet.
- `list_sheet_filters` — List filters on a sub-sheet.
- `list_sheet_float_images` — List float images on a sub-sheet.
- `list_sheet_history` — List spreadsheet edit history versions.
- `list_sheet_pivot_tables` — List pivot tables on a sub-sheet.
- `list_sheet_sparklines` — List sparklines on a sub-sheet.
- `list_slides_history` — List historical versions of a Feishu Slides presentation.
- `list_thread_messages` — List messages inside a Feishu message thread.
- `list_vc_meeting_events` — List participant and lifecycle events from one Feishu video meeting.
- `list_whiteboard_nodes` — List the raw nodes in a Feishu whiteboard, including Mermaid or PlantUML source metadata.
- `list_wiki_members` — List members of a Feishu Wiki space.
- `list_wiki_nodes` — List nodes in a Feishu Wiki space or below one parent node.
- `list_wiki_spaces` — List Feishu Wiki spaces accessible to the caller.
- `manage_task_assignees` — Add or remove assignees on a Feishu task. [write]
- `manage_task_followers` — Add or remove followers on a Feishu task. [write]
- `manage_task_reminders` — List, add, or remove reminders on a Feishu task. [write]
- `manage_tasklist_members` — Add or remove members on a Feishu tasklist. [destructive]
- `merge_sheet_range` — Merge cells in a range. [write]
- `move_base_block` — Move and order a Base resource block. [write]
- `move_drive_item` — Move a Feishu Drive file or folder and return a task ID when Feishu processes the move asynchronously. [write]
- `move_sheet_dimension` — Move a contiguous row or column range to a new position. [write]
- `move_sheet_range` — Move a cell range. [write]
- `move_wiki_node` — Move a Feishu Wiki node to another space or parent node. [write]
- `overwrite_markdown_file` — Overwrite an existing Feishu Drive Markdown file with a complete JSON Markdown string. [write]
- `patch_markdown_file` — Fetch a Markdown file, replace literal text or a JavaScript regular expression locally, and overwrite only when matches exist. [write]
- `patch_okr` — Update content, notes, score, or deadline on an objective or key result. [write]
- `pin_message` — Pin one Feishu/Lark message inside its chat. [write]
- `preview_docs_media` — Download the source-file preview of Feishu document media into connector transit storage.
- `put_typed_table` — Write a DataFrame-friendly typed table while preserving numbers, booleans, and real dates. [write]
- `query_base_data` — Run the Base data-query DSL for server-side grouping, aggregation, filtering, sorting, and Top N analysis.
- `query_calendar_freebusy` — Query a Feishu user's free/busy periods and RSVP status.
- `recall_message` — Recall one Feishu/Lark message that the app bot sent. [destructive]
- `recall_sent_mail` — Request asynchronous recall of one delivered Feishu mail message within its recall window. [destructive]
- `remove_base_attachments` — Validate a Base attachment field and remove selected file tokens from one record cell. [write]
- `remove_chat_members` — Remove users or bots from a Feishu chat. [destructive]
- `remove_drive_permission` — Remove a collaborator permission from a Feishu Drive resource. [destructive]
- `remove_message_reaction` — Remove one Feishu/Lark message reaction by `reaction_id`. [destructive]
- `remove_pin` — Remove the pin state from one Feishu/Lark message. [destructive]
- `remove_wiki_member` — Remove a member from a Feishu Wiki space. [destructive]
- `rename_base_block` — Rename a Base resource block. [write]
- `rename_base_view` — Rename a Base view. [write]
- `render_slide_screenshot` — Render one SML 2.0 slide XML fragment and store the decoded screenshot in connector transit storage.
- `reopen_task` — Reopen a completed Feishu task. [write]
- `reorder_okrs` — Replace the objective or key-result order with an explicit ID sequence. [write]
- `replace_cells` — Find and replace matching text in a sub-sheet. [write]
- `replace_slide_elements` — Replace or insert structural elements on one Slides page, with SML boilerplate added for common shape replacements. [write]
- `replace_slides` — Replace multiple Slides pages by creating each replacement before its old page and then deleting the old page. [destructive]
- `reply_calendar_event` — Accept, decline, or tentatively accept a Feishu calendar event invitation. [write]
- `reply_message` — Reply to an existing Feishu/Lark message as the app bot. [write]
- `resize_sheet_range` — Resize rows or columns using pixels, standard size, or row auto-fit. [write]
- `revert_document` — Revert a Feishu docx document to a historical version and return the background task state. [destructive]
- `revert_drive_version` — Revert a Feishu Drive file to a specific historical version. [destructive]
- `revert_sheet_history` — Start an asynchronous revert to a spreadsheet history version. [destructive]
- `revert_slides_history` — Revert a Feishu Slides presentation to a historical version and return its task metadata. [destructive]
- `search_base_field_options` — Search the options of a single-select or multi-select field in a Feishu Base.
- `search_base_records` — Search records by keyword within selected fields of a Feishu Base table.
- `search_cells` — Find cell coordinates matching text or a regular expression.
- `search_chats` — Search chats visible to the Feishu/Lark app bot by keyword.
- `search_drive_items` — Search Feishu Drive documents, Wiki nodes, spreadsheets, Base apps, files, folders, and slides.
- `send_message` — Send a Feishu/Lark app bot message to a user or chat. [write]
- `send_rich_message` — Send text, Markdown, image, file, audio, video, or raw Feishu content, uploading URL media before sending. [write]
- `send_vc_meeting_message` — Send a text message or reaction through the app's in-meeting bot. [write]
- `set_base_view_card` — Replace the card configuration of a Base view. [write]
- `set_base_view_filter` — Replace the filter configuration of a Base view. [write]
- `set_base_view_group` — Replace the grouping configuration of a Base view. [write]
- `set_base_view_sort` — Replace the sorting configuration of a Base view. [write]
- `set_base_view_timebar` — Replace the timeline configuration of a Base view. [write]
- `set_base_view_visible_fields` — Replace the visible field configuration of a Base view. [write]
- `set_cells` — Write values, formulas, styles, comments, or validation to an A1 range. [write]
- `set_sheet_cell_image` — Fetch an image from a public URL, upload it to a Feishu spreadsheet, and embed it into one cell. [write]
- `set_sheet_dropdown` — Set dropdown validation across every cell in a range. [write]
- `set_task_ancestor` — Set or clear the ancestor of a Feishu task. [write]
- `sort_sheet_range` — Sort a cell range by one or more columns. [write]
- `submit_base_form` — Submit JSON field values to a shared Base form. [write]
- `submit_drive_export` — Submit an asynchronous Feishu Drive document export and return a handle for status polling. [write]
- `submit_drive_import` — Fetch a source file, upload it as Feishu import media, and submit an asynchronous Drive import task. [write]
- `submit_wiki_move_to_drive` — Move a Wiki node out of its knowledge space into Drive and return an asynchronous task handle. [write]
- `suggest_calendar_times` — Suggest available meeting times for Feishu users and chats.
- `triage_mail_messages` — Auto-paginate compact mailbox summaries through list or search APIs with a stable continuation token.
- `ungroup_sheet_dimension` — Ungroup rows or columns in a sub-sheet. [write]
- `unhide_sheet_dimension` — Unhide rows or columns in a sub-sheet. [write]
- `unmerge_sheet_range` — Unmerge cells in a range. [write]
- `update_app_slash_command` — Update the description, localized descriptions, or icon of a slash command selected by ID or name. [write]
- `update_base_dashboard` — Update a Base dashboard name or theme. [write]
- `update_base_dashboard_block` — Update a Base dashboard block name or data configuration. [write]
- `update_base_field` — Replace one field definition in a Feishu Base table. Read the field first and include all writable configuration to preserve; this is a full PUT replacement, not a partial update. [write]
- `update_base_form` — Update the name or description of a Base form. [write]
- `update_base_form_questions` — Update up to ten Base form questions by question ID. [write]
- `update_base_record` — Update one record in a Feishu Base table. [write]
- `update_base_role` — Delta-merge changes into a Base role configuration. [write]
- `update_base_table` — Rename a table in a Feishu Base. [write]
- `update_base_workflow` — Replace a Base workflow definition while preserving its enabled state. [write]
- `update_calendar_event` — Update Feishu calendar event fields and incrementally add or remove attendees. [destructive]
- `update_chat` — Update a Feishu chat's name or description. [write]
- `update_document` — Update a Feishu document with a high-level text or block operation instead of manually orchestrating docx block APIs. [destructive]
- `update_document_cover` — Upload an image from a public URL and set it as a Feishu docx document cover. [write]
- `update_drive_comment` — Mark a Feishu Drive comment as solved or unresolved. [write]
- `update_drive_permission` — Change a collaborator's permission role on a Feishu Drive resource. [write]
- `update_mail_template` — Fetch and fully replace a mail template after merging provided JSON fields; concurrent writes are last-write-wins. [write]
- `update_okr_indicator` — Find the first indicator for an objective or key result and update its current value. [write]
- `update_okr_progress` — Update the content or rate of an OKR progress record. [write]
- `update_okr_weights` — Replace objective or key-result weights with explicit ID and weight pairs. [write]
- `update_sheet` — Rename, move, hide, show, or recolor one sub-sheet. [write]
- `update_sheet_chart` — Update a chart object. [write]
- `update_sheet_conditional_format` — Update a conditional format object. [write]
- `update_sheet_dropdowns` — Apply one dropdown configuration to multiple sheet-prefixed ranges. [write]
- `update_sheet_filter` — Update a filter object. [write]
- `update_sheet_filter_view` — Update a filter view object. [write]
- `update_sheet_float_image` — Update a float image object. [write]
- `update_sheet_pivot_table` — Update a pivot table object. [write]
- `update_sheet_sparkline` — Update a sparkline object. [write]
- `update_task` — Update the editable attributes of a Feishu task. [write]
- `update_wiki_node_title` — Update a Feishu Wiki node title. Supports doc, docx, and shortcut nodes. [write]
- `upload_base_attachments` — Validate a Base attachment field, upload one or more files from public URLs, and append them to one record cell. [write]
- `upload_docs_media` — Upload an image or attachment from a public URL to a Feishu document block, using multipart upload above 20 MB. [write]
- `upload_drive_file` — Upload a file from a public URL to Feishu Drive, automatically using the three-step multipart protocol above 20 MB. [write]
- `upload_file` — Upload one public file URL to Feishu/Lark and return the file key for message sending. [write]
- `upload_image` — Upload one public image URL to Feishu/Lark and return the image key for message sending. [write]
- `upload_okr_image` — Upload an image from a public URL for use in Feishu OKR progress rich text. [write]
- `upload_slides_media` — Upload an image of at most 20 MB to a Slides presentation for use as an XML `<img>` file token. [write]
- `upload_task_attachment` — Upload a file from a public URL as an attachment to a Feishu Task resource. [write]
- `upsert_base_record` — Create a Base record when recordId is omitted, or update that record when recordId is provided. [write]
- `verify_sheet_formulas` — Scan formulas for errors across selected sheets or ranges.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Feishu App Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Feishu App Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/feishu_app_bot
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Feishu App Bot homepage: https://open.feishu.cn
- API documentation: https://open.feishu.cn/document/server-docs/im-v1/message/create
