# Instatic Admin API Reference

Compiled from route tables and handler doc-headers in `server/handlers/cms` at v0.0.20, plus live-verified behavior. Paths sit under `/admin/api/cms` unless noted. Session cookie `instatic_admin_session` (HttpOnly, Path=/admin). State-changing calls require a matching Origin header (CSRF). Capability gates in parentheses; step-up notes mark routes verified or read as gated in handler source. System roles: owner, admin (39 of 40 capabilities, everything but roles.manage), client, member; custom roles are capability sets, and owner-only capabilities are stripped from non-owner roles at read time.

Scripted flow that works: one cookie jar across login plus every call (`curl -b jar -c jar`), Origin header equal to the base URL, and a step-up call when a route answers 401 `step_up_required`.

## Setup and first run (public, one-shot)
- GET /setup/status -> {hasSite,hasAdmin,hasOwner,needsSetup}
- POST /setup {siteName,email,password,displayName?} creates site + owner + starter homepage, then 409s forever
- GET /public-site -> {name,faviconUrl} (unauthenticated branding for login screen)

## Auth and account
- POST /login {email,password}; POST /logout; POST /auth/logout-all
- GET /me; PATCH /me (displayName,email); PATCH /me/password
- POST /auth/step-up {password} (opens window, default 15 min; PATCH /me/security/step-up sets 5/15/30/60)
- GET /auth/sessions; DELETE /auth/sessions/:id
- POST /auth/mfa/verify; POST /me/mfa/totp/start; POST /me/mfa/totp/enable; DELETE /me/mfa/totp; POST /me/mfa/recovery-codes
- GET /auth/activity (login attempts; lockout diagnosis)
- /me/preferences/:key (catalog-driven editor prefs); POST /me/avatar; DELETE /me/avatar

## Users and roles (users.manage / roles.manage; mutations step-up-gated per handler source)
- GET /users; POST /users {email,password,displayName?,roleId,status?} (create rejects role=owner; guards stop you removing the last active owner)
- PATCH /users/:id (email/displayName/password/roleId/status); DELETE /users/:id (soft)
- GET|POST /roles; PATCH|DELETE /roles/:id (custom roles only; built-ins resync at boot)

## Data: tables and rows
Tables (writes content.manage; create/patch/delete additionally step-up-gated, live-verified on create):
- GET /data/tables (list with row counts, optional query + limit); POST /data/tables -> 201 {table}
- Create semantics: kind coerces to postType|data (system tables are not creatable); slug from pluralLabel, pluralLabel from name, singularLabel from name minus trailing s; supplied fields win on id collision; omitting fields entirely gets the canonical six postType built-ins; mandatory title+slug are auto-prepended when missing; non-empty routeBase gives published rows public URLs
- GET /data/tables/:id -> {table} (full stored schema; the readback for computed flags); PATCH/DELETE /data/tables/:id (system tables frozen; step-up)
- GET /data/tables/:id/rows; POST /data/tables/:id/rows (draft row); GET /data/tables/:id/loop-preview
Rows:
- GET|PATCH|DELETE /data/rows/:id (PATCH saves draft cells; DELETE soft)
- POST /data/rows/:id/publish (content.publish.own / .any); PATCH /data/rows/:id/status (draft<->unpublished)
- POST|DELETE /data/rows/:id/schedule (scheduled publish); PATCH /data/rows/:id/author; PATCH /data/rows/:id/table (data.rows.move)
- POST /data/rows/:id/preview; GET /data/rows/:id/versions; POST /data/rows/:id/versions/:versionId/restore
- GET /data/authors; GET /data/search?query=&limit=
- GET /data/_meta -> {meta:{tables:[{id,slug,name,kind,singularLabel,pluralLabel,primaryFieldId,routable,versioned,fields}]}} (nested under `meta`; the compact schema view)

## Site and editor (site.read; writes site.structure.edit / site.content.edit / site.style.edit)
- GET /site (draft shell: breakpoints, classes, files, deps)
- PUT /site-document (whole-draft save; mode incremental|replace; conflict fields baseSeqs/shellBaseSeq 409 on stale writes). Built by the editor SPA; do not hand-craft page trees
- GET /pages?id=; GET /components?id=; GET /layouts?id= (each is data_rows in the matching system table)
- POST /runtime/dependencies/resolve; POST /runtime/validate; POST /runtime/preview (runtime.dependencies)

## Publish
- POST /publish (pages.publish + step-up) -> {publishedPages:n}; serialized under a publish lock; 422 on script build error
- GET /publish/status (site.read; draft-vs-published freshness)
- Unauthenticated public surface: baked HTML at site origin; GET /_instatic/hole/<nodeId>?v=<publishVersion>&u=<pageUrl>; assets /_instatic/assets/, /_instatic/css/, /_instatic/media/, /_instatic/module-js/, /_instatic/preview/; form endpoints /_instatic/form/submit + /challenge; GET /health

## Media
- GET /media (list); POST /media (multipart `file` part + metadata; size + magic-byte validation; image variants generated) (media.write)
- PATCH|DELETE /media/:id (metadata / soft delete); POST /media/:id/restore; POST /media/:id/replace (media.replace); POST /media/:id/folders
- GET|POST /media/folders; PATCH|DELETE /media/folders/:id (cascade children + assets)
- Storage adapters: GET /media/storage; POST /media/storage/elect | /delegate | /verify/:id | /migrate (storage.elect / storage.migrate)

## Fonts
- GET /fonts/google (bundled directory, no CDN hit); POST /fonts/estimate; POST /fonts/install (woff2 download); POST /fonts/custom (from uploaded media); DELETE /fonts/family/:family

## Branches (site.branches.create / .manage)
- GET|POST /branches (list / fork); PATCH|DELETE /branches/:id (rename / delete)
- GET|POST|DELETE /branches/:id/preview (active link / issue / revoke)
- GET /branches/:id/merge then POST (plan then execute, manage + step-up); POST /branches/:id/merge/undo; same pair for update
- GET /branches/:id/review; POST .../review/request|withdraw|decline; POST .../review/comments; GET .../review/render (page as main vs branch). Main is the live site and never a source to merge from

## Export and import (data.export / data.import)
- GET|POST /export -> site-bundle zip (`.instatic/site-bundle.json` + media/); POST /export/estimate; GET /export/summary
- POST /import?strategy=replace|merge-add|merge-overwrite; POST /import/archive?strategy=... (streamed media ZIP); POST /import/preview
- Static-site Super Import runs through the admin modal pipeline (plan -> commit, single undo), not a bare API call

## Plugins (plugins.read/install/configure/lifecycle)
- GET|POST /plugins (list / manifest JSON install); POST /plugins/inspect-package; POST /plugins/package (zip install/upgrade)
- PATCH|DELETE /plugins/:id (enable/disable; uninstall with ?force=true deletes assets); POST /plugins/:id/restart; POST /plugins/:id/pack/install
- GET|PUT /plugins/:id/settings (schema + masked values)
- GET|POST /plugins/:id/resources/:rid/records; PATCH|DELETE .../records/:recId
- GET /plugins/:id/schedules; POST .../schedules/:sid/run-now|pause|resume; GET /plugins/events (SSE)

## npm registry proxy (runtime.dependencies)
- GET /registry; GET /registry/search?q=&sort=&from=&size=&deprecated=; GET /registry/packages/:name with subpaths /latest /downloads /advisories

## AI agent (ai.chat; writes ai.tools.write; providers ai.providers.manage)
- POST /admin/api/ai/chat/site|content opens an NDJSON stream; browser-bridged tool results relay to POST /admin/api/ai/tool-result; /admin/api/ai/oauth/authorize for OAuth providers

## MCP
- Endpoint /_instatic/mcp; OAuth aux /_instatic/oauth/register + /_instatic/oauth/token; personal access tokens use the imcp_pat_ prefix (server/ai/mcp/connectors/token.ts)

## Audit and dashboard (audit.read / dashboard.read)
- GET /audit (latest events, reverse-chronological; publish, user/role/plugin/data mutations recorded)
- GET /dashboard/pages|posts|media|plugins|storage|publish-lineup|activity

## Server env vars (server/config.ts)
PORT (3001); HOST (0.0.0.0); DATABASE_URL (default sqlite:./.tmp/dev.db); UPLOADS_DIR (./uploads); STATIC_DIR (./dist); INSTATIC_SECRET_KEY; TRUSTED_PROXY_CIDRS (CSV); PUBLIC_ORIGIN (CSV canonical origins, unset derives from Host); INSTATIC_SHUTDOWN_TOKEN; INSTATIC_FORM_SECRET; RUNTIME_CACHE_DIR; IMAGE_VARIANT_WORKER_POOL_SIZE; RENDER_CACHE_MAX_ENTRIES; NPM_REGISTRY_URL; NODE_ENV; INSTATIC_VERSION; RENDER_EXTERNAL_URL and RAILWAY_PUBLIC_DOMAIN (origin fallbacks); dev/test: VITE_PORT, VITE_ALLOWED_ORIGIN, E2E_CMS_PORT, E2E_VITE_PORT.

## Capabilities (40, verified unique in src/core/capabilities.ts; upstream prose says 38 and is stale)
ai.audit.read, ai.chat, ai.providers.manage, ai.tools.write, audit.read, content.create, content.edit.any, content.edit.own, content.manage, content.publish.any, content.publish.own, dashboard.read, data.custom.tables.manage, data.custom.tables.read, data.export, data.import, data.rows.move, data.system.tables.manage, data.system.tables.read, media.delete, media.read, media.replace, media.write, pages.edit, pages.publish, plugins.configure, plugins.install, plugins.lifecycle, plugins.read, roles.manage, runtime.dependencies, site.branches.create, site.branches.manage, site.content.edit, site.read, site.structure.edit, site.style.edit, storage.elect, storage.migrate, users.manage
