---
name: interactive-doc-mapper
description: Create JSON-driven single-page interactive HTML documentation for app workflows between packages, services, and components. Use when a user asks for clickable architecture docs, action flow maps such as invite-user or desktop-build flows, package/component handoff diagrams, or a reusable workflow JSON that renders to an inspectable HTML page.
---

# Interactive Doc Mapper

## Goal

Turn an app's package/component workflows into a portable, self-contained HTML
page where every package stays visible and clicking an action highlights the
handoff path, payloads, and annotations.

Use the JSON file as the source of truth. The generated HTML is a review
artifact, not the place to hand-edit flows.

## Quick Start

1. Inventory the app.
   - Identify packages, components, services, queues, build systems, databases,
     and external adapters that matter to the requested workflows.
   - Group them by natural boundary such as `frontend`, `backend`, `data`,
     `build`, or `external`.

2. Create or update the flow JSON.
   - Follow `references/flow-schema.md`.
   - Include every visible node in `nodes`.
   - Include each clickable action in `actions`.
   - Put ordered handoffs in `actions[].steps` with `from`, `to`, `label`,
     `payload`, and `notes`.

3. Validate before rendering.
   - Run `python3 {baseDir}/scripts/validate_flow_doc.py --input <flows.json> --out <validation.json>`.
   - Fix unknown node references, duplicate IDs, missing action steps, or vague
     labels before generating the page.

4. Generate the page.
   - Run `python3 {baseDir}/scripts/generate_interactive_doc.py --input <flows.json> --out <workflow-map.html>`.
   - Use `--print-summary` when you want a short terminal summary for the user.

5. Verify interactively.
   - Open the HTML page in a browser or use Playwright.
   - Click at least two action buttons.
   - Confirm the active nodes, arrow path, step list, and payload annotations
     change together.

## Flow Authoring Rules

- Keep action IDs stable and human-readable: `invite-new-user`,
  `todesktop-build`, `checkout-payment`, `daily-sync`.
- Prefer concrete package/component names from the repo over generic names like
  `frontend` or `backend` unless those are actual packages.
- Document what crosses each boundary: request body, event name, database row,
  artifact path, token claim, cache key, or build output.
- Add `risk` only when there is a real review concern such as auth, secrets,
  irreversible side effects, or flaky build state.
- Do not put credentials, raw tokens, cookies, customer data, private URLs, or
  secret environment values in the JSON or generated HTML.
- If the user did not provide JSON, derive a first draft from repo inspection
  and clearly state the assumptions in the JSON `description` or action
  summaries.

## Quality Bar

- The output must be one HTML file that works from `file://` without a build
  step or external CDN.
- All nodes must stay visible even when a selected action uses only a subset.
- The selected action must highlight both source/target nodes and ordered
  arrows.
- The right-side annotation panel must explain the handoff sequence without
  requiring the user to read code.
- Generated pages should be dense and work-focused, not a landing page.

## Bundled Scripts

- `scripts/validate_flow_doc.py`
  - Validate JSON structure, duplicate IDs, action references, and weak labels.
- `scripts/generate_interactive_doc.py`
  - Validate and render a self-contained interactive HTML workflow map.

## References

- `references/flow-schema.md`
  - JSON fields, examples, and authoring checklist.
