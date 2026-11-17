---
name: oo-karakeep
description: "Karakeep (karakeep.app). Use this skill for ANY Karakeep request — reading, creating, updating, and deleting data. Whenever a task involves Karakeep, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Karakeep"
  author: "OOMOL"
  version: "1.0.5"
  services: ["karakeep"]
  icon: "https://static.oomol.com/logo/third-party/karakeep.svg"
---

# Karakeep

Operate **Karakeep** through your OOMOL-connected account. This skill calls the `karakeep` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Karakeep. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "karakeep" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "karakeep" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_bookmark_to_list` — Add a bookmark to a manual Karakeep list. The operation is idempotent, so adding a bookmark that is already in the list succeeds and changes nothing. [write]
- `admin_trigger_inference` — Trigger AI inference, either tagging or summarization, on bookmarks across the whole Karakeep instance. Filter by inference status and by how recently the bookmarks were modified. The inference jobs are queued and run asynchronously. Requires an API key owned by a Karakeep admin user; any other key fails with a 403 provider_error carrying the upstream message Forbidden - Admin access required. [write]
- `admin_trigger_recrawl` — Trigger a recrawl of link bookmarks across the whole Karakeep instance. Filter by crawl status to target specific bookmarks, for example only the failed ones, and by how recently they were modified. The crawls are queued and run asynchronously. Requires an API key owned by a Karakeep admin user; any other key fails with a 403 provider_error carrying the upstream message Forbidden - Admin access required. [write]
- `admin_trigger_reindex` — Trigger a reindex of bookmarks in the Karakeep search engine. Without modifiedWithinSeconds Karakeep clears the whole search index first and then re-queues every bookmark, so search results across the instance stay incomplete until the queue drains; with it only the bookmarks modified inside that window are re-queued and the existing index is preserved. The reindex runs asynchronously. Requires an API key owned by a Karakeep admin user; any other key fails with a 403 provider_error carrying the upstream message Forbidden - Admin access required. [destructive]
- `admin_update_user` — Update another Karakeep user's role, bookmark quota, storage quota or browser crawling setting. Only the provided fields are changed, and at least one of them must be present. Karakeep rejects updating the user that owns the API key with a 400. Requires an API key owned by a Karakeep admin user; any other key fails with a 403 provider_error carrying the upstream message Forbidden - Admin access required. [destructive]
- `attach_asset_to_bookmark` — Attach an already uploaded asset to a bookmark, for example a screenshot or a PDF. Upload the file first to obtain an asset id. Only the screenshot, pdf, assetScreenshot, precrawledArchive, bannerImage, video and userUploaded roles can be attached; linkHtmlContent, bookmarkAsset, fullPageArchive, avatar and unknown assets are maintained by Karakeep itself and are rejected with a 400. [write]
- `attach_tags_to_bookmark` — Attach tags to a bookmark. Reference each tag by tagId, or by tagName to let Karakeep create the tag when it does not exist yet. [write]
- `check_bookmark_url` — Check whether a URL is already bookmarked and return the id of the existing bookmark, or null when it is not. Useful before calling create_bookmark.
- `create_backup` — Trigger a new full account backup for the connected Karakeep user. Karakeep records the request and answers immediately with a backup whose status is pending; the archive itself is produced asynchronously by the instance backup worker, and assetId, size and bookmarkCount stay empty until it finishes. Poll get_backup until status becomes success or failure. When the backup worker is disabled on that instance the record stays pending forever, so always give the polling loop a timeout of its own. Karakeep rate limits this to five backups per hour. [write]
- `create_bookmark` — Create a bookmark from a link, a text note or an already uploaded asset. Set type to link and provide url, set type to text and provide text, or set type to asset and provide assetType and assetId. When the same URL is already bookmarked Karakeep does not create a duplicate: it returns the existing bookmark with alreadyExists set to true and re-saves it, which bumps createdAt to now, resets archived to false, and overwrites title, favourited, note and summary with whatever you supplied. Only source rss and source import skip that re-save. Call check_bookmark_url first when the existing bookmark must not be touched. [write]
- `create_feed` — Create a new RSS feed subscription. Karakeep periodically fetches the feed and imports matching items as bookmarks. Karakeep answers with 400 when the per user feed limit has already been reached. [write]
- `create_highlight` — Create a text highlight on a Karakeep bookmark. A highlight is defined by the character offsets it covers in the readable content of the bookmark and can carry a color and a note. [write]
- `create_list` — Create a new bookmark list. Manual lists receive bookmarks that are added explicitly, while smart lists are populated automatically by a saved search query. [write]
- `create_tag` — Create a new Karakeep tag. The name is trimmed and normalized into the tag style configured for the account. [write]
- `delete_backup` — Permanently delete a Karakeep backup record together with the archive file it produced. Karakeep answers with an empty body, so the action reports the deleted backup id instead. [destructive]
- `delete_bookmark` — Permanently delete a bookmark together with its tags, highlights and attached assets. [destructive]
- `delete_feed` — Delete an RSS feed subscription. Bookmarks that the feed already imported are not affected. [destructive]
- `delete_highlight` — Delete a Karakeep highlight and return the record that was removed. The bookmark the highlight belonged to is kept. [destructive]
- `delete_list` — Delete a Karakeep list. Only the list itself is removed; the bookmarks it contained are kept. [destructive]
- `delete_tag` — Delete a Karakeep tag. The tag is detached from every bookmark that carried it; the bookmarks themselves are kept. [destructive]
- `detach_asset_from_bookmark` — Detach an asset from a bookmark. Karakeep deletes the asset record together with the stored file, so the asset id becomes unusable afterwards and the bytes are gone; the bookmark keeps its other assets. Only screenshot, pdf, assetScreenshot, fullPageArchive, precrawledArchive, bannerImage, video and userUploaded assets can be detached; linkHtmlContent, bookmarkAsset, avatar and unknown assets are maintained by Karakeep itself and are rejected with a 400. [destructive]
- `detach_tags_from_bookmark` — Detach tags from a bookmark. Reference each tag by tagId or by tagName. The tags themselves are kept, only the attachment to this bookmark is removed. [destructive]
- `download_backup` — Download the archive of a finished Karakeep backup and hand it back as a temporary connector file URL. The action reads the backup record first: while the status is still pending it fails with an invalid input error asking you to poll get_backup, on a failed backup it fails with an invalid input error carrying the upstream failure message because that state is terminal and polling will not help, and a success record without an archive asset fails as a provider error. Only then does it stream the archive out of Karakeep into file transit. Karakeep's own download endpoint answers with a redirect to an authenticated relative path that most HTTP clients cannot follow, so the connector resolves the archive asset id itself instead of following the redirect.
- `fetch_feed_now` — Trigger an immediate fetch of an RSS feed subscription. The fetch is only enqueued and runs asynchronously, so newly imported bookmarks appear later; poll get_feed and watch lastFetchedAt to see when it finished. [write]
- `get_asset` — Download the binary content of a Karakeep asset and hand it back as a temporary connector file URL. The connector streams the bytes from Karakeep into file transit instead of returning them inline, so the action also works for large images, videos, PDFs and archives. Karakeep sends no Content-Disposition header, so the file name falls back to the asset id plus an extension guessed from the content type.
- `get_asset_signed_url` — Create a short lived signed download URL for a Karakeep asset. The URL carries its own token, so anyone holding it can fetch the asset without an API key, and it expires between 15 and 75 minutes after it was issued. Karakeep builds the URL from the public URL configured on the instance itself rather than from the instance URL stored on this connection, so a misconfigured self-hosted instance can return a host that is unreachable from the outside.
- `get_backup` — Get one Karakeep backup by id, including its current status, archive size, bookmark count and failure message. This is the polling target for create_backup: keep reading it until status is success or failure, and treat a record that stays pending as a backup worker that is not running on that instance.
- `get_bookmark` — Get a single bookmark with its tags, content and attached assets. Keep includeContent false unless the extracted page content is really needed, because it can make the response very large; text bookmarks always carry content.text. Use get_bookmark_content to read long article text in chunks.
- `get_bookmark_content` — Read the readable content of a bookmark in chunks as markdown or plain text. This is the safe way to read long articles: pass nextCursor back to fetch the following chunk instead of asking for the whole content with includeContent. Karakeep rejects a cursor with CONTENT_CHANGED when the bookmark content changed while paging, in which case restart from the first chunk.
- `get_bookmark_highlights` — List the highlights stored on a bookmark.
- `get_bookmark_lists` — List the Karakeep lists that contain a bookmark.
- `get_current_user` — Get the profile of the Karakeep user that owns the connected API key, including name, email and avatar.
- `get_current_user_stats` — Get usage statistics for the Karakeep user that owns the connected API key, including bookmark, tag, list and asset counts.
- `get_feed` — Retrieve a single RSS feed subscription by its id.
- `get_highlight` — Retrieve a single Karakeep highlight by its id.
- `get_list` — Retrieve a single Karakeep list by its id.
- `get_list_bookmarks` — Retrieve one page of the bookmarks inside a Karakeep list. For smart lists the bookmarks are computed from the saved query of the list.
- `get_tag` — Retrieve a single Karakeep tag by its id, including how many bookmarks carry it and who attached it.
- `get_tag_bookmarks` — Retrieve one page of the bookmarks that carry a given Karakeep tag.
- `list_backups` — List every account backup recorded for the connected Karakeep user, including the ones that are still pending and the ones that failed.
- `list_bookmarks` — List the bookmarks of the connected Karakeep user, optionally filtered by archived or favourited status, sorted by creation date and paged with a cursor. Keep includeContent false unless the extracted page content is really needed, because it can make the response very large; text bookmarks always carry content.text.
- `list_feeds` — Retrieve all RSS feed subscriptions for the authenticated Karakeep user. The response is not paginated and returns every feed at once.
- `list_highlights` — Retrieve one page of the highlights the authenticated Karakeep user has made across all bookmarks.
- `list_lists` — Retrieve all bookmark lists for the authenticated Karakeep user, including both manual and smart lists. This endpoint is not paginated and returns every list in one response.
- `list_tags` — Retrieve one page of Karakeep tags. Tags can be filtered by name fragment and by who attached them, and sorted by name, usage count or relevance. Pagination is only active when limit is given: omit limit and Karakeep returns every tag in one response with no cursor.
- `remove_bookmark_from_list` — Remove a bookmark from a manual Karakeep list. The bookmark itself is kept. Karakeep rejects the request when the bookmark is not a member of the list. [destructive]
- `replace_asset_on_bookmark` — Replace an asset that is attached to a bookmark with another already uploaded asset. The replaced asset is deleted and the new asset takes over its role. The asset being replaced must hold an attachable role, meaning screenshot, pdf, assetScreenshot, precrawledArchive, bannerImage, video or userUploaded; assets Karakeep maintains itself, including linkHtmlContent, bookmarkAsset, fullPageArchive, avatar and unknown, are rejected with a 400. [destructive]
- `search_bookmarks` — Search the bookmarks of the connected Karakeep user with full text, semantic or hybrid search. Paging uses a search specific cursor that cannot be shared with list_bookmarks. Keep includeContent false unless the extracted page content is really needed, because it can make the response very large; text bookmarks always carry content.text.
- `summarize_bookmark` — Generate an AI summary for a link bookmark and return it. Karakeep saves the generated summary on the bookmark, replacing any summary it already had, and re-indexes the bookmark for search, so this is not a read-only preview. The call blocks while the configured model runs, so it can take a while, and it fails with an invalid input error when the Karakeep instance has no inference provider configured. The current server writes the summary before answering and returns it synchronously, so summary normally carries the finished text. The published OpenAPI spec instead documents the whole bookmark record, so an instance following that shape can answer with summary null; in that case read the bookmark again with get_bookmark until summarizationStatus is success and take the summary from there. [destructive]
- `update_bookmark` — Update a bookmark. Only the fields you send are changed, and sending null clears a nullable field, so existing values are overwritten. Fields that do not belong to the bookmark variant are not ignored: Karakeep rejects the whole request with a 400 such as Attempting to set link attributes for non-link type bookmark and writes nothing, so send only the fields that match the bookmark type. [destructive]
- `update_feed` — Update an RSS feed subscription. Only the fields present in the input are changed; every omitted field keeps its current value. [destructive]
- `update_highlight` — Partially update a Karakeep highlight. Only the color and the note can be changed, and sending null for the note clears it. [write]
- `update_list` — Partially update a Karakeep list. Only the fields present in the input are changed, and sending null for description or parentId clears the stored value. [write]
- `update_tag` — Rename a Karakeep tag. The name is the only field this endpoint can change, so it is required. The new name is trimmed and normalized, and every bookmark carrying the tag sees the new name. [write]
- `upload_asset` — Upload a file to Karakeep as a new standalone asset. The connector downloads fileUrl server side and posts the bytes as multipart/form-data under the form field file. Karakeep accepts only image/gif, image/jpeg, image/png, image/webp, video/mp4, video/webm, video/x-matroska, text/html and application/pdf. It sniffs binary types from the bytes themselves and ignores the declared type for them, but HTML carries no signature, so an HTML upload is accepted only when the declared content type is exactly text/html. Anything above the instance asset size limit is rejected with an Asset is too big error; that limit is MAX_ASSET_SIZE_MB multiplied by 1024 * 1024, so it is 50 MiB by default. The asset is created detached from any bookmark, so follow up with attach_asset_to_bookmark when it belongs to one. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Karakeep state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Karakeep is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/karakeep
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Karakeep homepage: https://karakeep.app
- API documentation: https://docs.karakeep.app/api/karakeep-api
