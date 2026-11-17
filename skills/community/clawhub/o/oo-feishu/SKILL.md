---
name: oo-feishu
description: "Feishu (feishu.cn). Use this skill for ANY Feishu request — reading, creating, updating, and deleting data. Whenever a task involves Feishu, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Feishu"
  author: "OOMOL"
  version: "1.0.8"
  services: ["feishu"]
  icon: "https://static.oomol.com/logo/third-party/feishu.svg"
---

# Feishu

Operate **Feishu** through your OOMOL-connected account. This skill calls the `feishu` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Feishu. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "feishu" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "feishu" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_approval_cc` — Add CC recipients to an active approval instance. [write]
- `add_chat_members` — Add users or bots to a Feishu chat. [write]
- `add_drive_permission` — Grant a collaborator permission on a Feishu Drive resource. [write]
- `add_sign_approval_task` — Add users before, after, or alongside the current approval task. [write]
- `add_task_comment` — Add a text comment to a Feishu task. [write]
- `add_task_to_tasklist` — Add a Feishu task to a tasklist. [write]
- `add_wiki_member` — Add a member to a Feishu Wiki space. [write]
- `apply_drive_permission` — Apply to a Feishu document owner for view or edit permission on behalf of the current user. [write]
- `apply_minutes_permission` — Apply for view or edit permission on one Feishu Minutes record. [write]
- `approve_approval_task` — Approve a pending approval task with optional form controls. [write]
- `arrange_base_dashboard` — Ask Feishu to automatically arrange dashboard blocks. [write]
- `batch_create_base_records` — Create up to 200 records in one Feishu Base request. [write]
- `batch_create_okrs` — Create objectives and their key results sequentially, with optional rollback on failure. [write]
- `batch_delete_base_records` — Delete up to 200 records in one Feishu Base request. [destructive]
- `batch_get_messages` — Fetch up to 50 Feishu messages by message ID in one request.
- `batch_update_base_records` — Update up to 200 records with record-specific fields in one Feishu Base request. [write]
- `batch_update_sheet` — Execute multiple Sheet AI write tools in one batch request. [destructive]
- `cancel_approval_instance` — Recall an approval instance initiated by the connected user. [destructive]
- `cancel_message_flag` — Cancel a targeted message flag or best-effort cancel both message and feed layers. [destructive]
- `cancel_scheduled_send` — Cancel a Feishu mail message before its scheduled delivery time. [destructive]
- `clear_cells` — Clear cell contents, formats, or both from an A1 range. [destructive]
- `complete_task` — Mark a Feishu task as completed. [write]
- `copy_base` — Copy a Feishu Base, optionally changing its name, destination folder, content inclusion, or time zone. [write]
- `copy_drive_file` — Copy a Feishu Drive file or online document into another folder. [write]
- `copy_sheet_range` — Copy a cell range. [write]
- `copy_wiki_node` — Copy a Feishu Wiki node into another space or below another parent. [write]
- `create_app_slash_command` — Register a slash command, optionally updating the existing command when its name already exists. [write]
- `create_approval_instance` — Create an approval instance from structured form controls. [write]
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
- `create_feed_shortcuts` — Add up to 10 chats to the authorized user's feed shortcuts at the head or tail. [write]
- `create_mail_draft` — Compose and save a new Feishu mail draft without sending it. [write]
- `create_mail_template` — Create a personal Feishu mail template from JSON content and existing Drive-backed attachments. [write]
- `create_markdown_file` — Create a Markdown file from a JSON string in Feishu Drive root, a Drive folder, or a Wiki node. [write]
- `create_message_flag` — Bookmark a message in the message or feed layer, automatically detecting thread type when needed. [write]
- `create_okr` — Create one Feishu objective or key result from plain text. [write]
- `create_okr_alignment` — Align one Feishu OKR objective to another objective. [write]
- `create_okr_comment` — Create or reply to a Feishu OKR comment. [write]
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
- `create_wiki_space` — Create a Feishu Wiki space. [write]
- `create_workbook` — Create a Feishu spreadsheet workbook. [write]
- `decline_mail_read_receipt` — Dismiss a message's read-receipt request without sending mail, safely doing nothing when already cleared. [write]
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
- `delete_mail_draft` — Delete a Feishu mail draft. [destructive]
- `delete_okr_alignment` — Delete a Feishu OKR objective alignment. [destructive]
- `delete_okr_comment` — Permanently delete a Feishu OKR comment. [destructive]
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
- `download_message_resource` — Download one image or file resource attached to a Feishu message into connector transit storage.
- `download_minutes_media` — Resolve and stream a Feishu Minutes audio or video recording into connector transit storage.
- `download_vc_note_transcript` — Fetch every page of a unified meeting-note transcript and upload the complete text to connector transit storage.
- `enable_base_advanced_permissions` — Enable advanced permissions for a Base. [write]
- `enable_base_workflow` — Enable a Base workflow without changing its steps. [write]
- `export_whiteboard_svg` — Export a Feishu whiteboard as SVG and return the API's Base64 payload without writing a local file.
- `fetch_document` — Fetch a Feishu document as Docx XML or Markdown, with optional structural detail and partial-read selection.
- `fetch_markdown_file` — Fetch the latest or a specific version of a Markdown file from Feishu Drive.
- `fill_sheet_range` — Fill a destination range from a source pattern. [write]
- `find_calendar_rooms` — Find meeting rooms available for the specified event time slots.
- `forward_mail` — Forward a Feishu mail message to new recipients. [write]
- `freeze_sheet_dimension` — Freeze or unfreeze the leading rows or columns. [write]
- `get_approval` — Get an approval definition, form snapshot, and approval nodes.
- `get_approval_instance` — Get an approval instance with its nodes, tasks, form, and history.
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
- `get_calendar_meeting_info` — Get video meeting and meeting-note relations for calendar event instances.
- `get_cells` — Read one or more A1 ranges with values, formulas, and optional styles.
- `get_chat` — Get the metadata of one Feishu chat visible to the authorized user.
- `get_current_user` — Get the profile of the Feishu user who authorized this connection, using their user_access_token.
- `get_document` — Get a Feishu docx document's basic metadata (title and revision) that the authorized user can read.
- `get_document_content` — Read the full plain-text content of a Feishu docx document the authorized user can access.
- `get_document_creation` — Get a document creation task status and its completed document. Do not repeat creation while the task is processing.
- `get_document_revert_status` — Get the status of a Feishu document history revert task.
- `get_drive_export` — Get the normalized status and generated file token of a Drive export task.
- `get_drive_import` — Get the normalized status and created document token of a Drive import task.
- `get_drive_permission_settings` — Get public access, sharing, collaborator management, security, and comment permission settings for a Feishu Drive resource. Download restrictions can only be determined when the corresponding fields are returned; this does not test a user's effective download permission.
- `get_drive_task_status` — Get the current state of an asynchronous Drive move, copy, or delete task.
- `get_drive_version` — Download one specific Feishu Drive file version into connector transit storage.
- `get_mail_message` — Read one Feishu mail message with body and attachment metadata.
- `get_mail_recall_detail` — Get asynchronous recall progress and per-recipient results for one Feishu mail message.
- `get_mail_send_status` — Get the latest per-recipient delivery status for one sent Feishu mail message.
- `get_mail_signature_detail` — Fetch one complete mail signature and annotate whether it is the send or reply default.
- `get_mail_thread` — Read every message in a Feishu mail thread in chronological order.
- `get_minutes_detail` — Get the basic metadata of one Feishu Minutes record.
- `get_minutes_download_metadata` — Get the temporary media download URL for a Feishu Minutes record without downloading it.
- `get_minutes_summary` — Get the generated summary of a Feishu Minutes record.
- `get_minutes_todos` — List the generated todos of a Feishu Minutes record.
- `get_minutes_transcript` — Get the generated transcript text of a Feishu Minutes record.
- `get_okr_comment` — Get one Feishu OKR comment by ID.
- `get_okr_cycle_detail` — List every objective in an OKR cycle and fetch the key results below each objective.
- `get_okr_progress` — Get one Feishu OKR progress record.
- `get_related_tasks` — List tasks related to the authorized Feishu user, with optional bounded auto-pagination.
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
- `get_vc_meeting` — Get Feishu video meeting metadata and participant data.
- `get_vc_meeting_note` — Resolve a video meeting to its note ID and return normalized meeting-note details.
- `get_vc_note` — Get meeting-note metadata and its related document tokens.
- `get_vc_recording_metadata` — Get recording URL and duration metadata for a Feishu video meeting.
- `get_wiki_node` — Resolve a Feishu Wiki node by node token or document token; the server detects the token type.
- `get_wiki_space` — Get one Feishu Wiki space by ID.
- `get_wiki_task` — Get a normalized Wiki asynchronous task status.
- `get_workbook` — Get workbook structure and metadata, including all sub-sheets.
- `group_sheet_dimension` — Group rows or columns in a sub-sheet. [write]
- `hide_sheet_dimension` — Hide rows or columns in a sub-sheet. [write]
- `insert_docs_media` — Append an image or file to a Feishu docx document by creating a block, uploading media, and binding the file token with rollback on failure. [write]
- `insert_sheet_dimension` — Insert blank rows or columns into a sub-sheet. [write]
- `inspect_drive_item` — Inspect a Feishu Drive token to resolve its canonical type, title, URL, and underlying document for Wiki nodes.
- `list_active_vc_meetings` — List active Feishu video meetings for the current user or a tenant user.
- `list_app_slash_commands` — List every slash command registered on the currently connected Feishu app.
- `list_approval_tasks` — List approval tasks grouped by pending, completed, or CC status.
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
- `list_bitable_fields` — List the fields (columns) of a Feishu Bitable table, to understand its schema before reading rows.
- `list_bitable_tables` — List the data tables in a Feishu Bitable (multi-dimensional spreadsheet) the authorized user can access.
- `list_calendar_agenda` — List event instances in a Feishu calendar over a bounded time range.
- `list_chat_members` — List members of one Feishu chat visible to the authorized user.
- `list_chats` — List Feishu chats visible to the authorized user.
- `list_department_users` — List users in a Feishu department visible to the app.
- `list_departments` — List child departments below a Feishu department visible to the app.
- `list_document_blocks` — List a Feishu docx document's structured blocks (one page), for reading document structure and rich content.
- `list_document_history` — List historical versions of a Feishu docx document.
- `list_drive_comments` — List comments on a Feishu Drive document or supported file.
- `list_drive_files` — List files, folders, and online documents inside a Feishu Drive folder.
- `list_drive_permissions` — List collaborators and permission roles on a Feishu Drive resource.
- `list_drive_previews` — List available preview artifacts and generation states for a Feishu Drive file.
- `list_drive_secure_labels` — List secure labels available to the current Feishu user.
- `list_drive_versions` — List one page of tagged version history for a Feishu Drive file.
- `list_feed_group_items` — List active and deleted feed cards in one group, optionally resolving each chat.
- `list_feed_groups` — List user feed groups, preserving both active and soft-deleted groups across auto-pagination.
- `list_feed_shortcuts` — List one version-locked page of user feed shortcuts and optionally attach complete chat details.
- `list_initiated_approval_instances` — List approval instances initiated by the connected user.
- `list_mail_messages` — List message IDs in a Feishu mailbox folder or label.
- `list_mail_signatures` — List the authorized user's Feishu mail signatures and default usages.
- `list_message_flags` — List active and canceled user message flags, optionally auto-paginating and enriching feed flags with messages.
- `list_messages` — List messages from one Feishu chat or thread with user-identity history permissions.
- `list_okr_alignments` — List the objectives aligned from or to a Feishu OKR objective.
- `list_okr_categories` — List enabled and disabled Feishu OKR categories configured by the tenant.
- `list_okr_comments` — List one page of comments attached to a Feishu OKR entity.
- `list_okr_cycles` — List Feishu OKR cycles visible to a user.
- `list_okr_progress` — List progress records for an objective or key result.
- `list_sheet_charts` — List charts on a sub-sheet.
- `list_sheet_conditional_formats` — List conditional formats on a sub-sheet.
- `list_sheet_filter_views` — List filter views on a sub-sheet.
- `list_sheet_filters` — List filters on a sub-sheet.
- `list_sheet_float_images` — List float images on a sub-sheet.
- `list_sheet_history` — List spreadsheet edit history versions.
- `list_sheet_pivot_tables` — List pivot tables on a sub-sheet.
- `list_sheet_sparklines` — List sparklines on a sub-sheet.
- `list_slides_history` — List historical versions of a Feishu Slides presentation.
- `list_tasks` — List Feishu tasks related to the caller with server-side status filters.
- `list_thread_messages` — List messages inside a Feishu message thread.
- `list_vc_meeting_events` — List participant and lifecycle events from one Feishu video meeting.
- `list_whiteboard_nodes` — List the raw nodes in a Feishu whiteboard, including Mermaid or PlantUML source metadata.
- `list_wiki_members` — List members of a Feishu Wiki space.
- `list_wiki_nodes` — List nodes in a Feishu Wiki space or below one parent node.
- `list_wiki_spaces` — List Feishu Wiki spaces accessible to the caller.
- `manage_minutes_todos` — Add, update, or delete multiple todo items in one Feishu Minutes record. [write]
- `manage_task_assignees` — Add or remove assignees on a Feishu task. [write]
- `manage_task_followers` — Add or remove followers on a Feishu task. [write]
- `manage_task_reminders` — List, add, or remove reminders on a Feishu task. [write]
- `manage_tasklist_members` — Add or remove members on a Feishu tasklist. [destructive]
- `merge_sheet_range` — Merge cells in a range. [write]
- `modify_mail_messages` — Add or remove labels and move Feishu mail messages in batches of 20. [destructive]
- `move_base_block` — Move and order a Base resource block. [write]
- `move_drive_item` — Move a Feishu Drive file or folder and return a task ID when Feishu processes the move asynchronously. [write]
- `move_sheet_dimension` — Move a contiguous row or column range to a new position. [write]
- `move_sheet_range` — Move a cell range. [write]
- `move_wiki_node` — Move a Feishu Wiki node to another space or parent node. [write]
- `overwrite_markdown_file` — Overwrite an existing Feishu Drive Markdown file with a complete JSON Markdown string. [write]
- `patch_markdown_file` — Fetch a Markdown file, replace literal text or a JavaScript regular expression locally, and overwrite only when matches exist. [write]
- `patch_okr` — Update content, notes, score, or deadline on an objective or key result. [write]
- `preview_docs_media` — Download the source-file preview of Feishu document media into connector transit storage.
- `put_typed_table` — Write a DataFrame-friendly typed table while preserving numbers, booleans, and real dates. [write]
- `query_base_data` — Run the Base data-query DSL for server-side grouping, aggregation, filtering, sorting, and Top N analysis.
- `query_calendar_freebusy` — Query a Feishu user's free/busy periods and RSVP status.
- `query_feed_group_items` — Look up specific chat feed cards in one group and optionally attach complete chat details.
- `query_my_attendance_tasks` — Query the current authorized user's attendance tasks and clock-in records for a work-date range.
- `recall_sent_mail` — Request asynchronous recall of one delivered Feishu mail message within its recall window. [destructive]
- `reject_approval_task` — Reject a pending approval task. [destructive]
- `remind_approval_tasks` — Send reminders for one or more tasks in an approval instance. [write]
- `remove_base_attachments` — Validate a Base attachment field and remove selected file tokens from one record cell. [write]
- `remove_chat_members` — Remove users or bots from a Feishu chat. [destructive]
- `remove_drive_permission` — Remove a collaborator permission from a Feishu Drive resource. [destructive]
- `remove_feed_shortcuts` — Remove up to 10 chats from the authorized user's feed shortcuts. [destructive]
- `remove_wiki_member` — Remove a member from a Feishu Wiki space. [destructive]
- `rename_base_block` — Rename a Base resource block. [write]
- `rename_base_view` — Rename a Base view. [write]
- `render_slide_screenshot` — Render one SML 2.0 slide XML fragment and store the decoded screenshot in connector transit storage.
- `reopen_okr_comment` — Reopen a solved Feishu OKR comment or selection thread. [write]
- `reopen_task` — Reopen a completed Feishu task. [write]
- `reorder_okrs` — Replace the objective or key-result order with an explicit ID sequence. [write]
- `replace_cells` — Find and replace matching text in a sub-sheet. [write]
- `replace_minutes_speaker` — Replace a transcript speaker with another Feishu user in one Minutes record. [write]
- `replace_minutes_summary` — Replace the AI-generated summary of one Feishu Minutes record. [write]
- `replace_minutes_words` — Batch-replace words in the transcript of one Feishu Minutes record. [write]
- `replace_slide_elements` — Replace or insert structural elements on one Slides page, with SML boilerplate added for common shape replacements. [write]
- `replace_slides` — Replace multiple Slides pages by creating each replacement before its old page and then deleting the old page. [destructive]
- `reply_all_mail` — Reply to all participants of a Feishu mail message. [write]
- `reply_calendar_event` — Accept, decline, or tentatively accept a Feishu calendar event invitation. [write]
- `reply_mail` — Reply to a Feishu mail message, preserving conversation headers. [write]
- `reply_message` — Reply to a Feishu message as the authorized user, optionally inside the message thread. [write]
- `resize_sheet_range` — Resize rows or columns using pixels, standard size, or row auto-fit. [write]
- `revert_document` — Revert a Feishu docx document to a historical version and return the background task state. [destructive]
- `revert_drive_version` — Revert a Feishu Drive file to a specific historical version. [destructive]
- `revert_sheet_history` — Start an asynchronous revert to a spreadsheet history version. [destructive]
- `revert_slides_history` — Revert a Feishu Slides presentation to a historical version and return its task metadata. [destructive]
- `rollback_approval_task` — Roll back an approval task to one or more earlier nodes. [destructive]
- `search_approvals` — Search approval definitions the connected user can initiate.
- `search_base_field_options` — Search the options of a single-select or multi-select field in a Feishu Base.
- `search_base_records` — Search records by keyword within selected fields of a Feishu Base table.
- `search_bitable_records` — Read rows (records) from a Feishu Bitable table, with optional field selection, filter, and sort.
- `search_calendar_events` — Search Feishu calendar events by text, time range, and attendee identifiers.
- `search_cells` — Find cell coordinates matching text or a regular expression.
- `search_chats` — Search Feishu chats visible to the authorized user by name.
- `search_documents` — Search Feishu documents, Wiki nodes, spreadsheets, Base apps, files, folders, and slides.
- `search_drive_items` — Search Feishu Drive documents, Wiki nodes, spreadsheets, Base apps, files, folders, and slides.
- `search_mail_messages` — Search Feishu mail by text, addresses, subject, state, and creation time.
- `search_messages` — Search messages across Feishu chats with keyword, sender, chat, mention, attachment, and time filters.
- `search_minutes` — Search Feishu Minutes by text, owners, participants, and creation time.
- `search_tasklists` — Search Feishu tasklists by name and ownership.
- `search_tasks` — Search Feishu tasks by text, members, completion state, and due range.
- `search_users` — Search Feishu users by keyword, open_id list, or relationship filters using user identity.
- `search_vc_meetings` — Search Feishu video meetings by text, people, rooms, and time range.
- `send_mail` — Compose a new email, create a Feishu draft, and send it immediately. [write]
- `send_mail_draft` — Send an existing Feishu mail draft immediately or at a scheduled time. [write]
- `send_mail_read_receipt` — Send a system-generated RFC 3798-style read receipt for a message that requested one. [write]
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
- `share_mail_to_chat` — Create a Feishu mail share card for one message or thread and send it to an IM recipient. [write]
- `solve_okr_comment` — Mark a Feishu OKR comment or its selection thread as solved. [write]
- `sort_sheet_range` — Sort a cell range by one or more columns. [write]
- `submit_base_form` — Submit JSON field values to a shared Base form. [write]
- `submit_drive_export` — Submit an asynchronous Feishu Drive document export and return a handle for status polling. [write]
- `submit_drive_import` — Fetch a source file, upload it as Feishu import media, and submit an asynchronous Drive import task. [write]
- `submit_wiki_move_to_drive` — Move a Wiki node out of its knowledge space into Drive and return an asynchronous task handle. [write]
- `subscribe_mail_events` — Subscribe a user mailbox to Feishu message-received events before consuming the corresponding push event. [write]
- `suggest_calendar_times` — Suggest available meeting times for Feishu users and chats.
- `transfer_approval_task` — Transfer a pending approval task to another user. [write]
- `trash_mail_messages` — Move Feishu mail messages to trash in batches of 20. [destructive]
- `triage_mail_messages` — Auto-paginate compact mailbox summaries through list or search APIs with a stable continuation token.
- `ungroup_sheet_dimension` — Ungroup rows or columns in a sub-sheet. [write]
- `unhide_sheet_dimension` — Unhide rows or columns in a sub-sheet. [write]
- `unmerge_sheet_range` — Unmerge cells in a range. [write]
- `unsubscribe_mail_events` — Unsubscribe a user mailbox from Feishu message-received events. [destructive]
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
- `update_drive_secure_label` — Set the secure label of a Feishu Drive file or document. [write]
- `update_mail_draft` — Replace the complete content of an existing Feishu mail draft. [write]
- `update_mail_template` — Fetch and fully replace a mail template after merging provided JSON fields; concurrent writes are last-write-wins. [write]
- `update_minutes_title` — Update the title of one Feishu Minutes record. [write]
- `update_okr_comment` — Replace the content of a Feishu OKR comment. [write]
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
- `upload_minutes_media` — Upload audio or video from a public URL to Drive and create a Feishu Minutes recording from the resulting file token. [write]
- `upload_okr_image` — Upload an image from a public URL for use in Feishu OKR progress rich text. [write]
- `upload_slides_media` — Upload an image of at most 20 MB to a Slides presentation for use as an XML `<img>` file token. [write]
- `upload_task_attachment` — Upload a file from a public URL as an attachment to a Feishu Task resource. [write]
- `upsert_base_record` — Create a Base record when recordId is omitted, or update that record when recordId is provided. [write]
- `verify_sheet_formulas` — Scan formulas for errors across selected sheets or ranges.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Feishu state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Feishu is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/feishu
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Feishu homepage: https://www.feishu.cn
- API documentation: https://open.feishu.cn/document/home/index
