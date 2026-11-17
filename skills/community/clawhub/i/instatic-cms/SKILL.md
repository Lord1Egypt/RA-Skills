---
name: "instatic-cms"
description: "Install, build, design, publish with Instatic (self-hosted visual CMS): canvas, collections, templates, tokens, agent, MCP. Trigger: instatic."
---

# Instatic Self-Hosted CMS

Build and run Instatic sites: one Bun container holds the visual canvas, content engine, media, auth, forms, plugins, and publisher; published pages ship as plain HTML with hashed CSS bundles. This skill manages a self-hosted Instatic deployment and everything you can do with it. Knowledge was compiled against v0.0.20 and sharpened by live operation; later versions can drift, re-verify before trusting behavior.

## Quick Reference

| Topic | File |
|-------|------|
| Install, compose modes, image, platform notes | `instatic-cms/install.md` |
| Stack, database dialects, migrations, health | `instatic-cms/database.md` |
| Tables, rows, fields, templates, components, layouts, loops | `instatic-cms/content-model.md` |
| Full endpoint surface, auth rules, capabilities, env vars | `instatic-cms/api.md` |
| Design tokens, class registry, CSS bundles | `instatic-cms/styling.md` |
| Publish pipeline, holes, scheduler, export bundle, imports, TLS | `instatic-cms/publishing.md` |
| Admin UI: workspaces, canvas modes, spotlight | `instatic-cms/workspaces.md` |
| AI agent, MCP server, plugin automation | `instatic-cms/automation.md` |
| Verification rules and evidence bar | `instatic-cms/verification.md` |

Read the file for the area you are working in BEFORE touching the instance. The master file stays lean on purpose; detail lives in the per-area files.

## Where things live

This skill is generic to any self-hosted Instatic deployment. Replace the placeholders with your own values before relying on them:

- Deployment: compose files + `.env` in your install directory (every env knob listed in `instatic-cms/api.md`)
- Upstream documentation: the `docs/` tree in the pinned version checkout (about 55 files at v0.0.20). Handler source under `server/handlers/cms/` beats prose docs when they disagree
- Live-instance specifics (port, URLs, volumes, proven commands, backups): your deployment notes, not this skill

## Critical Rules

1. **Verify against the pinned checkout before claiming behavior.** Upstream prose drifts from source: their docs say 38 capabilities, the source array has 40. When live behavior disagrees with this skill, fix the skill the same session.
2. **Session cookie is HttpOnly, Path=/admin.** Scripted clients keep one cookie jar across login and calls, under `/admin/api/cms/*`, with an Origin header matching the base URL.
3. **State-changing calls need a matching Origin header** (canonical origin from `PUBLIC_ORIGIN` or the request Host). Set `PUBLIC_ORIGIN` whenever a proxy or domain fronts the container.
4. **Step-up gates more than you expect:** publish, data-table create/patch/delete, user create/patch/delete, branch merge/update, plugin install/lifecycle, token creation. The 401 body says `step_up_required`; open the window with `POST /auth/step-up {password}`, retry once inside it (15 min default), and if it 401s again check `/auth/activity` before anything else. The handler source marks gates per route; a missing body is not proof of no gate.
5. **Five failed logins locks the account,** exponential backoff up to 24h, shared counter with MFA misses. Check `/auth/activity` before retrying anything.
6. **Never hand-write page-tree payloads into `/site-document`.** The seq-conflict body (baseSeqs/shellBaseSeq) belongs to the editor SPA. Use the UI, the AI agent, or the row APIs.
7. **Export bundles move sites between instances. They are not deploy output.** Loop-bearing pages publish as `<instatic-hole>` placeholders this server fills at view time; a pure static-host deploy only works on hole-free pages or pre-resolved output.
8. **Field truth (v0.0.20): 16 field types.** markdown/html are richText formats, image/video/any are media kind values, currency/percent are number formats; none are separate types. No icon-picker field exists.
9. **Computed flags are not in create responses.** After creating or patching a table, read back `/data/tables/:id` or `/data/_meta` to confirm routable/versioned and the stored field set; the 201 body alone proves nothing.
10. **Verify with DOM measurements and fetched HTML, never eyeballs or image files.** Operator confirmation from his own browser gates interactive flows; an HTTP 200 never marks work done.
11. **Pin image tags; migrations run at boot and a failed migration exits the process.** Keep the previous tag locally until the operator confirms the upgrade.

## Standard Workflow

1. Read the matching topic file, plus `instatic-cms/verification.md`.
2. Take a live DB snapshot before risky writes (pattern in `instatic-cms/database.md`).
3. Make one logical change to one table or page; expect `step_up_required` on schema writes and open the window first when planning a batch.
4. Verify per `instatic-cms/verification.md` (readback, not trust), then check in.

## Memory

Operator preferences and live-instance specifics are not part of this published skill. The skill is generic; any local customization lives in your own deployment notes, not here.
