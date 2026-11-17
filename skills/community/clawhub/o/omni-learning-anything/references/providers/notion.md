# Notion

Default new connection: official `ntn` CLI API transport, or an already authorized writable official API connector with create/media/readback support. See [onboarding](../onboarding.md). The learner supplies the confirmed course parent-page link; the agent extracts its ID and runs `connect --platform notion --location LINK`. It returns read-only readiness or a specific setup step.

If needed, the agent installs official `ntn`, checks current help, initiates `ntn login --no-browser`, and forwards the generated official URL and verification code. The learner opens it, checks matching code/account/workspace and approves. After confirmation the agent runs `ntn login poll`, then repeats `connect`. CLI login requires full workspace membership; guests/restricted members must resolve their role or use an explicitly supported authorized API alternative. Tokens stay in the official CLI's OS keychain. Do not call token-export commands or silently turn off keychain storage. Existing `NOTION_API_TOKEN` overrides keychain authorization, so check the resulting identity; never print its value. For multiple workspaces use the confirmed `--workspace-id` instead of switching defaults.

The returned delivery uses `platform: notion`, `mode: cli`, verified `account_id` and `destination.parent_page_id`; optional `destination.workspace_id`. The adapter checks the same identity before any write. Existing `mode: api` with `credential_env.token` stays supported for privately configured tokens; share the confirmed parent with that integration and grant only necessary read/insert capabilities. A browser session alone supplies neither route's API grant.

The bundled adapter pins `Notion-Version: 2026-03-11`, uploads a PNG/JPEG (<=20 MB) through `/v1/file_uploads` and `/send`, creates a Markdown page through `/v1/pages`, and attaches a file-upload image block. It removes local image paths before cloud creation. It reads page parent/title, all root image blocks and Markdown sections/source links before verifying. A page returned from create is not by itself verified.

Grant only the needed insert/read capabilities to the chosen parent. Keep the token outside course/repository in the named environment variable. Published content lives under the course parent; page IDs and upload IDs are saved for recovery. No key is requested when the host connector supplies equivalent access.

If Markdown API rejects a lesson size/format, preserve the existing pending page and use authorized host/block tools to complete it; do not create another page blindly. Uploaded unattached files expire after one hour: if a pending upload expires, reconcile the known page or start a explicitly confirmed new course version; never conceal missing media. Free account upload limits may be lower than the API's 20 MB maximum.

For UI import, `mode: import` now defaults to embedded DOCX plus Markdown; `publish` points to the DOCX. Existing reviewed Markdown-only imports remain resumable and require their referenced image. In the Word importer, explicitly select the confirmed course parent. The importer may use the filename as the page title and omit the Word title: inspect and rename the actual page to the intended plan/lesson title. Reopen it from the parent and inspect the full text, rendered figure/caption and all five exact source URLs before recording a receipt. An import-complete dialog alone does not verify content. Reuse the same page on repeat publish. Login/UI availability cannot guarantee unattended daily delivery.

Real-account acceptance on 2026-10-18: plan and Day01 Word imports, bilingual content, image/credit, five URL destinations per page, parent placement, reopen and verified-receipt reuse passed. This historical result does not validate the direct API route.

Real-account API acceptance on 2026-10-25: official `ntn 0.23.25` login, selected parent access, actual plan and Day01 Markdown-page creation/image uploads, title/parent/content readback, full native browser visual checks and five links per page passed. Saved connection reuse, identical receipt reuse and exactly two documents in the isolated API QA parent passed. Browser UI was used for inspection; all writes used the official API transport. Unattended scheduling/keychain access was not tested. The live API returned official `app.notion.com` URLs and escaped Markdown punctuation; the adapter accepts that host and normalizes punctuation for content checks.

CLI login links expire quickly. Finish local tool setup before generating a timed link; show the fresh URL/code immediately and hand control back for login. If an old link returns HTTP400, confirm session expiry from official polling before issuing a new flow. Do not repeatedly resend stale codes.

Official sources (CLI authorization/installation checked 2026-10-25; content API references checked 2026-10-14):
- https://developers.notion.com/cli/get-started/installation
- https://developers.notion.com/cli/get-started/authentication
- https://developers.notion.com/cli/guides/api-requests
- https://developers.notion.com/cli/guides/file-uploads
- https://developers.notion.com/guides/data-apis/working-with-markdown-content
- https://developers.notion.com/guides/data-apis/uploading-small-files
- https://developers.notion.com/reference/patch-block-children
