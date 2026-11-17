# Organizing monitors

## Contents
- Tags and folders
- Editing, pausing and removing monitors
- Templates and page discovery
- Workspaces
- Showing monitors visually

## Tags and folders

Tags (labels) and folders are separate. A monitor sits in at most one folder but can carry many tags. Use folders for structure (a client, a competitor, a project) and tags for cross-cutting themes (pricing, legal, urgent).

Folders (`manage-folders`):

- Start with `manage-folders(action="list")` to see the tree before changing it.
- `manage-folders(action="create", name="Competitors", parent="Research")` nests a folder; omit `parent` for the top level.
- `manage-folders(action="move", folder="Competitors", monitor_ids=[...])` moves up to 50 monitors. A destination that does not exist is created at the top level. An empty `folder` removes monitors from any folder.
- `rename` and `reparent` change a folder. `manage-folders(action="reparent", folder="Competitors", target_workspace_id=...)` moves the folder, its subfolders and every monitor in them to another workspace of the same team.
- `delete` removes a folder and its subfolders, and the monitors inside stay but lose their folder. Confirm before deleting.
- `list-monitors(folder="Competitors")` includes monitors in subfolders.

Tags (`manage-tags`):

- `manage-tags(action="list")` shows the current workspace's tags, or another workspace's with `workspace_id`.
- `manage-tags(action="add", monitor_ids=[...], tags=["pricing"])` tags up to 50 monitors in one call, and `action="remove"` untags them. Use `monitor_id` for a single monitor. The monitors can be in different workspaces: each one gets the tag of its own workspace, created there when missing.

## Editing, pausing and removing monitors

- `manage-monitors(action="update", monitor_id="...", frequency=60)` changes the name, URL, frequency, notifications, screenshots, `ai_page_focus`, folder or enabled state. It cannot change what the monitor tracks; for that, create a corrected monitor.
- `set-monitor-status(monitor_ids=[...], enabled=false)` stops checks on up to 50 monitors (`monitor_id` for one) and keeps them with their history, freeing slots in the plan's active monitor count. Each monitor comes back with its own result. Turning monitors back on counts against that limit again, and enabling stops when the limit is reached.
- `manage-monitors(action="clear-history", monitor_id="...")` erases stored checks and values but keeps the monitor. `manage-monitors(action="delete", monitor_ids=[...])` removes monitors with all their history, screenshots and values. Both are permanent and accept up to 50 monitors: confirm first, naming the monitors.

## Templates and page discovery

A template holds shared settings for many monitors and can discover pages on a website.

1. `list-templates` shows existing templates.
2. `manage-templates(action="create", name="Example blog", url="https://example.com/blog", autoimport_enabled=true)` creates one with discovery on. `autoimport_mode` chooses how pages are found (for example `sitemap` or `combined`); some modes depend on the plan.
3. `manage-templates(action="add-filter", template="...", filter_type="url", filter_action="include", filter_pattern="/blog/*", filter_match_type="wildcard")` limits which discovered pages qualify.
4. `manage-templates(action="run-discovery", template="...")` queues a discovery crawl. It returns once queued, not when pages are found.
5. Later, `manage-discovered-pages(action="list", template_id=..., status="matches_filters")` shows candidates, and `manage-discovered-pages(action="import", ids=[...])` turns up to 50 of them into monitors. Pages imported past the plan's active monitor allowance are created paused.

`pause` and `resume` stop and restart monitors created from discovered pages. `stop` deletes those monitors but keeps the discovered records; `delete` removes the records. Confirm both. Deleting a template removes its discovered-page records and keeps monitors already created.

Help: https://pagecrawl.io/help/features/article/page-discovery

## Workspaces

- `list-workspaces` shows teams and workspaces with their IDs and monitor counts. Read and action tools work across all of them; `add-page-monitor` and moving monitors take a `workspace_id`.
- `manage-monitors(action="move", monitor_ids=[...], workspace_id=..., folder="Clients")` moves up to 50 monitors to another workspace, including one in another of the user's teams; omit `folder` to place them at the top level. Their history, review status and tags go with them, while alert channels, AI settings and reports come from the new workspace, so confirm with the user first. Monitors made from a template move together with their template: select all of them, or move their folder with `manage-folders` reparent and `target_workspace_id`.
- `manage-workspaces(action="create", name="Client: Example")` adds one; `manage-workspaces(action="update", timezone="Europe/London")` changes the timezone that schedules and report dates use.
- `manage-workspaces(action="delete", workspace_id=..., confirm=true)` permanently deletes every monitor in it with their history. Check what it contains and confirm with the user first. The last workspace in a team cannot be deleted.
- Creating and deleting workspaces needs the team owner or manager role.

## Showing monitors visually

In clients that display interactive results, call `list-monitors` first and then `render-monitors-dashboard(monitor_ids=[...], title="...")` with 1 to 50 IDs from that result. It is for showing, not for reading data.
