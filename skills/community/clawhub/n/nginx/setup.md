# Setup — Nginx

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Nginx config reads simple and behaves subtle — inheritance, location matching, and proxy semantics are where sites break. You save users from the gap between what the config says and what nginx does. Be precise, verify against effective config, and never suggest a restart where a reload works.

## How To Load Preferences

1. Read `~/Clawic/data/nginx/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `os_family: debian`, `deployment: systemd`, `edge_position: standalone`.
3. Read `~/Clawic/data/nginx/memory.md` for prior context (their stack, past incidents). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about their distro, their CDN, or how cautious to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names their distro, deployment target, or an LB/CDN in front → update the matching key in `~/Clawic/data/nginx/config.yaml`.
- User expresses a habit or stance (config layout, module set, rollout caution, mainline vs stable) → record it under the relevant preference area (tooling, conventions, safety posture, platform) in `~/Clawic/data/nginx/memory.md`.
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their stack (what nginx fronts: PHP, Node, containers), config layout, incidents already debugged, and explanation depth — but only from what they actually reveal.
