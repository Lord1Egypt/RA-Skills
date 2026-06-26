# Odoo Hosting Surfaces

Use this file to pick the right operating surface before suggesting commands, debugging steps, or automation.

| Surface | Usually available | Usually restricted | Best use |
|---------|-------------------|--------------------|----------|
| Odoo Online | UI, exports, imports, limited app/admin settings, supported APIs | shell access, direct server logs, custom server packages, direct database work | business operations, controlled imports, standard automation |
| Odoo.sh | UI, APIs, staging branches, logs, deploy pipeline, custom modules | casual production hacks, uncontrolled shell changes | module work, upgrade rehearsal, safe deploy/debug loop |
| Self-hosted | UI, APIs, server access, logs, workers, database tooling | nothing by default except what the user's infra forbids | deep ops, integration ownership, controlled backend diagnosis |

## Surface Rules

- Say the surface out loud before proposing a tool.
- Do not recommend shell, direct logs, or database debugging if the instance is Odoo Online.
- On Odoo.sh, prefer branch and staging rehearsal before production changes.
- On self-hosted systems, SQL may help diagnosis but should not be the first write path for business logic.
- If the surface is unknown, default to UI-safe guidance and ask the one question that unlocks the safer route.

## Decision Hints

- If the user talks about apps, forms, imports, and daily operations, start from the UI lane.
- If the user mentions deployments, modules, branches, or failed upgrades, treat it as Odoo.sh or self-hosted until clarified.
- If the user mentions psql, Docker, workers, or nginx, it is almost certainly self-hosted.
- If the user wants a repeatable integration, check whether APIs are enough before inventing backend access.
