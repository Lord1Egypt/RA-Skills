# Tencent Docs / 腾讯文档

Use the learner's authorized writable official API connector when it offers document creation, media and content readback. Otherwise prefer the bundled **official OAuth + MCP API** route (`mode: mcp`). This is Tencent Docs at docs.qq.com, not Enterprise WeChat. No browser cookies or community CLI are needed.

## Guided connection

Ask for a personal folder link (`https://docs.qq.com/desktop/mydoc/folder/ID`) or explicit confirmation of the home root (`https://docs.qq.com/desktop/`). If unknown, ask only this missing choice. Install `scripts/requirements-tencent-mcp.txt` in the selected isolated Python environment. Check existing named connections first.

Agent commands (`OMNI` is the installed `scripts/omni_learning.py`):

```sh
OMNI tencent-auth status --name personal-tencent
OMNI tencent-auth login --name personal-tencent
OMNI connect --platform tencent --location 'CONFIRMED_OFFICIAL_HOME_OR_FOLDER_LINK' --auth-profile personal-tencent --save-as my-tencent
```

Run `login` only when needed. It starts a loopback-only callback on a free local port, registers a public OAuth client and immediately prints the exact official authorization URL. Send that URL to the learner promptly; have them log in on the **same computer**, choose their own account and review `docs:read docs:write`. Keep the foreground login process running (up to ten minutes) until it reports success. A stale link requires a new login; do not repeatedly issue codes while a grant is pending. Public device authorization is advertised in the official metadata, but new dynamically registered clients were rejected by that endpoint during acceptance; the default supported flow is authorization code with PKCE.

Secrets are saved only by maintained `keyring` into an OS credential backend (macOS Keychain, Windows Credential Locker, Secret Service/libsecret). No plaintext fallback. An unavailable/locked keyring is a setup blocker: explain the exact local action, or reuse an already authorized official connector. Do not ask for a token in chat, read private browser stores, run a remote OAuth server or switch accounts silently. Callback state/PKCE is verified; bearer tokens go only to the official endpoint without redirects. Do not include authorization URLs, codes or private account IDs in public reports.

`connect` reads `get_user_info`, pins its user ID and checks the confirmed location. A saved profile contains only `auth_profile`, `account_id` and destination metadata. Copy returned `delivery` into the new course intake; later calls recheck identity. New documents use the course title (maximum 36 characters); agree a concise title before rendering.

## Publication and recovery

The selected MCP endpoint is `https://docs.qq.com/openapi/mcp`. Its live `tools/list` schemas are authoritative. The adapter uses `manage.pre_import`, sends the reviewed DOCX to the returned signed official upload URL with **no account headers**, then calls `manage.async_import`. It checkpoints the upload task, marks the document write uncertain before confirmation, and immediately saves the returned conversion task. The opaque upload key is not a folder/object ID.

Resume with `manage.import_progress`. Once a document ID is known, reuse that exact document. Confirm editable `doc` type and exact title with `manage.query_file_info`, and confirm membership in the requested folder through paginated `manage.folder_list`; move only this new course document if needed. Never change sharing permissions. The home root is an explicit `/`, not an inferred team space.

Readback uses `manage.export_file` → `manage.export_progress`, an allowlisted HTTPS download, and DOCX text, embedded-image and exact semantic hyperlink checks. Tencent may represent hyperlinks as Word `HYPERLINK` fields rather than relationship entries; both are checked, and plain URL text is insufficient. Export tasks can expire: recreate only the export, at most three times, preserving the existing document/import. An uncertain import confirmation without its returned task/document requires reconciliation before another write.

`publish` may return `pending`; retry that same command after the service makes progress. After `verified`, visual inspection of the actual native document remains required. Repeat publication reuses immutable receipts and creates no second course document. Background access to an interactive keychain still needs separate host verification.

The higher-level SmartCanvas creation tool was also probed: it appended content after a default tutorial. It is not the bundled course publishing route. Do not silently replace the reviewed document with a template or claim an image/link pass based solely on creation success. Missing VIP/account capabilities require specific guidance; never purchase or expand access automatically.

## Existing application API courses

Legacy `mode: api` retains its official COS SDK/application OAuth contract: `destination.folder_id`, environment references `client_id`, `open_id`, `token`, and the `Client-Id`, `Open-Id`, `Access-Token` headers. Install `requirements-tencent.txt` for that selected route. Temporary COS credentials remain in memory. Existing pending tasks and hashes are preserved; do not migrate an approved course to MCP automatically.

Official references inspected 2026-10-25:
- [Tencent Docs team MCP guide](https://developer.cloud.tencent.com/mcp/server/11803)
- [Official OAuth server metadata](https://docs.qq.com/.well-known/oauth-authorization-server)
- [Official MCP protected-resource metadata](https://docs.qq.com/openapi/mcp/.well-known/oauth-protected-resource)
- [Application OpenAPI](https://docs.qq.com/open/document/app/openapi/v2/)
- [Official COS SDK](https://github.com/tencentyun/cos-python-sdk-v5)

Real-account acceptance: official PKCE login, plan + Day01 DOCX import/export, same personal account and confirmed home root, exact five hyperlinks, synthetic embedded image, native page inspection and repeated receipt reuse passed on 2026-10-25. This does not establish unattended scheduling or every organization's entitlement.
