# Bower on the MCP google_workspace Drive tools

The Bower SKILL.md was written against a generic Drive API and references tool names like `GOOGLEDRIVE_FIND_FILE`. In this deployment the live interface is the `mcp__google_workspace` MCP server. This file maps Bower's prescribed scan steps onto the real tools so a future session does not rediscover them.

## Tool mapping

| Bower step | Real tool | Call shape |
|------------|-----------|------------|
| Root-level baseline query (`pageSize=10`) | `mcp__google_workspace__list_drive_items` | `folder_id: "root"`, `page_size: 10`, `include_items_from_all_drives: false`, `user_google_email: "<owner>"`. Absent `nextPageToken` ⇒ root has <100 items. |
| modifiedTime arrival query | `mcp__google_workspace__search_drive_files` | `query: "modifiedTime > 'YYYY-MM-DDTHH:MM:SSZ'"`, `corpora: "user"`, `include_items_from_all_drives: false`, `order_by: "modifiedTime desc"`, `user_google_email: "<owner>"`. |
| Enumerate a known folder | `mcp__google_workspace__list_drive_items` | `folder_id` = folder ID; `page_size` up to 200 for one-shot full listing of a single folder. |

## Owner account

The Drive owner email is required on every call. For <operator>'s Drive it is `<user-google-email>`.

## Detecting shared vs owned files in arrival results

The MCP search results do NOT expose a literal `ownedByMe` boolean or `parents` array. Infer ownership from the result fields:

- **Owned by user**: result shows `"Last Edited By: <Owner Name> <<owner email>>>"` (e.g., `Last Edited By: <user> <<user-google-email>>`).
- **Externally shared / not actionable**: result shows a different editor (`Last Edited By: a.editor <someone@example.com>`) OR a sharing badge with no owner edit such as `"Anyone with link: writer"`. These correspond to the `parents: null` / `ownedByMe: False` items the skill's gotcha warns about — exclude them from proposals.

Group arrivals by `Last Edited By` to split the two classes quickly: count non-owner editors and exclude those files.

## Cutoff convention

After a founding deep scan, use the founding scan's completion timestamp (`scan_progress.json` `last_checkpoint_at`, or the deep-scan `completed_at` in `scan_events.jsonl`) as the `modifiedTime` cutoff for the next light scan. The light scan is "since last full scan," not "since last light scan." Note the founding `scan_events.jsonl` entry may carry the same `started_at` and `completed_at` timestamp (instant completion) — the `drive_digest.json` `last_updated` field is the reliable cutoff.
