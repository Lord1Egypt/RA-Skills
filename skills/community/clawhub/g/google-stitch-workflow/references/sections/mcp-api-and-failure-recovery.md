## Autonomous Agent Pipeline

Some agent-connected Stitch workflows split the work into three specialized skill phases:

1. **Enhanced Prompt skill** — transforms vague prompts into Stitch-optimized prompts using adjective-based mood language and Stitch-specific keywords
2. **Stitch Loop skill** — autonomous iterative building using Chrome DevTools; maintains prompt tracking across stages
3. **React Component skill** — converts Stitch's monolithic HTML export into modular React components with validation scripts

**Recommended pipeline order for coding agents:**

1. Enhanced Prompt → convert your vague prompt into a Stitch-specific one
2. Stitch Loop → build the design via MCP (generates design system first, then actual design)
3. React Component skill → break the monolithic export into modular components

Add these steps to your coding agent's config file only when those skills exist in the active environment and match the target stack.

---

## MCP API Reference

### Browser context menu reality check (do not over-assume MCP)

Stitch's browser UI (including the right-click context menu) exposes features that are often **not** available
through the MCP surface.

Operational rule:
- Treat every context-menu action as **browser-only until proven** by MCP tool discovery (`tools list` in your agent environment).
- If a matching MCP tool does not exist, do not try to "prompt your way into it". Ask the human to run the action
  in the browser, then continue from artifacts (screenshots/zip/code).

Typical browser-only items include (non-exhaustive): instant prototype flows, predictive heat maps, missing-states
helpers, and newer preview/export affordances.

### Context menu → MCP mapping (official Stitch MCP server, checked 2026-11-08)

Use this mapping to decide whether to attempt an action via MCP or ask for browser execution.
If an item is not listed here and not in your runtime's tool list, treat it as browser-only.

| Browser action (common labels) | MCP status | Notes / tool |
|---|---|---|
| **List projects/screens** | MCP (read) | `list_projects` (huge output, summarize it), `get_project`, `list_screens`, `get_screen` |
| **Edit** | MCP | `edit_screens`: structural changes usually return new screen IDs; a small text edit can come back as a `DomOperationEvent` on the same screen and not be saved. Verify with `download_file` |
| **Variants** | MCP | `generate_variants` with `variantOptions` (`variantCount` 1-5, `creativeRange` REFINE/EXPLORE/REIMAGINE, `aspects`) |
| **Regenerate** | MCP (approx) | Prefer `edit_screens` with a tight prompt, or `generate_variants` with `creativeRange: "REFINE"` |
| **Design system** | MCP | `list_design_systems`, `create_design_system` (then `update_design_system`), `update_design_system`, `apply_design_system` |
| **Import DESIGN.md** | MCP | `upload_design_md` then `create_design_system_from_design_md` |
| **View code / Download screenshot** | MCP (read) | `download_file` with `htmlCode.name` or `screenshot.name` from `get_screen` / `list_screens` |
| **Delete project** | MCP (destructive) | `delete_project`; cannot be undone, confirm the exact project with the user first |
| **Instant prototype** | Browser-only | Not in the MCP tool list; run in browser and continue from artifacts |
| **Predictive heat map** | Browser-only | Run in browser |
| **Missing states** | Browser-only | Run in browser; encode states into the transfer contract/checklist |
| **Preview sizes / QR / connections** | Browser-only | Use browser preview to capture reference screenshots for the Fidelity Pack |
| **Export zip / Figma** | Browser-only | Use `download_file` for single-screen HTML and images; zip and Figma export stay in the browser |
| **Duplicate / Delete screen / Favourite / Focus** | Browser-only | No screen-level duplicate or delete tool in the MCP list |

### Capability boundaries

**Official MCP tools** (seen in the live schema on 2026-11-08):

- read: `list_projects`, `get_project`, `list_screens`, `get_screen`, `list_design_systems`, `download_file`
- generate/edit: `create_project`, `generate_screen_from_text`, `edit_screens`, `generate_variants`
- design system: `create_design_system`, `update_design_system`, `apply_design_system`, `upload_design_md`, `create_design_system_from_design_md`
- destructive: `delete_project`

Read calls were exercised live on that date. Write, generate and design-system calls were checked against the schema only; re-verify behavior in your environment before relying on them in an unattended flow.

**Not in the official server (unverified; older wrapper tools):**

- `fetch_screen_image`, `get_screen_image` → use `download_file` with `screenshot.name`
- `fetch_screen_code`, `get_screen_code` → use `download_file` with `htmlCode.name`
- `generation_status`, `list_generations` → poll `get_screen` / `list_screens`
- `build_site` → no equivalent

Use one only if your own tool list shows it.

**Tool-reported behavior worth knowing:**

- `create_design_system` should be followed by `update_design_system` so the design system is applied and shown in the project.
- `upload_design_md` should be followed by `create_design_system_from_design_md`; the upload creates the screen instance that call needs.
- `apply_design_system` takes screen instances (`{id, sourceScreen}`) from `get_project` → `screenInstances`, not screen IDs.
- `generate_screen_from_text` may return `output_components` with text or suggestions; show them to the user, and if the user accepts a suggestion, send it as the next prompt.

**Browser-only product features** — do not infer MCP can perform these:

- image or screenshot redesign
- prototype-oriented workflows
- broader canvas interactions
- newer browser-facing product features

### Parameter discipline

The MCP surface is parameter-sensitive. Incorrect casing or identifier shape can produce generic invalid-argument failures. Read the loaded tool schema before the first call of each tool.

**IDs vs resource names:** `projectId` and `selectedScreenIds` take bare IDs. `get_project`, `get_screen`, `delete_project` and `download_file` take resource names (`projects/{p}`, `projects/{p}/screens/{s}`, `projects/{p}/files/{f}`). Wrong: `selectedScreenIds: ["projects/xxx/screens/abc123"]`. Right: `["abc123"]`.

**`deviceType`:** Uppercase enum: `"MOBILE"`, `"DESKTOP"`, `"TABLET"`, `"AGNOSTIC"`. Optional on `edit_screens` and `generate_variants`; omit it there unless you need to change the device. Lowercase values fail.

**`modelId`:** Optional enum. Current schema values: `"GEMINI_3_8_FLASH"`, `"GEMINI_3_5_FLASH_LITE"`. The older `"GEMINI_3_FLASH"`, `"GEMINI_3_PRO"` and `"GEMINI_3_1_PRO"` are gone. Browser labels ("Flash", "Pro Thinking") are product labels, not MCP values. Omit `modelId` when unsure.

**`designSystem`** (generation): asset name such as `assets/15996705518239280238`. **`assetId`** (`apply_design_system`): the same ID without the `assets/` prefix.

**`upload_design_md`:** `designMdBase64` must decode to valid UTF-8.

**Prompt length:** Keep prompts under ~500 characters. Longer prompts get silently truncated by Stitch. Iterate with short, focused prompts rather than dumping all constraints in one call.

Example:
```json
{
  "projectId": "8675077932533356979",
  "selectedScreenIds": ["69b3228b6c5f4b9f9efceea4b6a30168"],
  "prompt": "Make the primary button darker. Keep everything else identical."
}
```

### Time budgets — by device type

These are verified from real sessions. **The HTTP timeout is NOT the generation time.** Stitch drops the TCP connection at ~60s while the generation continues server-side.

| Device   | HTTP timeout | Safe wait before declaring failure | Keep polling until |
|----------|-------------|----------------------------------|-------------------|
| MOBILE   | ~20-60s     | +60s after timeout               | 3 min total       |
| DESKTOP  | ~20-60s     | +5 min after timeout            | 10 min total      |

**Rule:** After receiving any timeout error on `generate_screen_from_text`, do NOT retry immediately. The tool's own instructions say: poll `get_screen` every 30 seconds up to 10 times when you know the screen; otherwise poll `list_screens` every 30-60 seconds and wait. Desktop screens regularly take 5-10 minutes to appear after the HTTP timeout.

**Additional reality:**
- Stitch can generate multiple screens (variants) from a single prompt — do not assume exactly one new screen per generate call
- **Screenshots via `download_file` are base64 and often too large for the context.** Some clients save the result to a file; decode it to PNG with a short script rather than reading it. HTML returns inline.
- **The screenshot may not be ready even after the screen entry appears in `list_screens`.** If `download_file` on `screenshot.name` fails or the field is missing, wait and retry. This typically resolves within seconds to a few minutes.
- **Parallel generation across device types is safe.** If you need mobile and desktop, kick off both simultaneously. They generate independently and poll each on its own timeline.
- Mobile generation is significantly faster and more reliable than desktop; prefer mobile-first even when desktop is the target, then derive the desktop from the mobile screen via `edit_screens`
- If desktop generation fails after 2 attempts via MCP, open Stitch in browser directly and generate desktop there

### Failure handling

**`Request contains an invalid argument.`** — Check in this order:

1. `deviceType` — for `edit_screens`, omit it entirely; for `generate_screen_from_text`, verify uppercase
2. `modelId` spelling — check against known identifiers
3. `selectedScreenIds` shape — bare IDs only, no resource name prefix
4. whether the screen is genuinely editable generated output (`htmlCode` present = likely safe to edit)
5. `modelId` is a current enum value (`GEMINI_3_8_FLASH`, `GEMINI_3_5_FLASH_LITE`), or omitted
6. `apply_design_system` got screen instances from `get_project`, not screen IDs
7. whether the prompt is trying to change too much at once

**Generation timeout — the canonical recovery path:**

Long-running operations may complete even when the client sees a timeout. The screen appears in `list_screens` moments later.

```
1. Record: T=0 at HTTP timeout
2. Wait 60s, then call: list_screens with projectId
3. Inspect result for new screen matching your deviceType
4. If found → `download_file` for screenshot + htmlCode → done
5. If not found → repeat step 2 every 60s
6. After 3min (mobile) or 10min (desktop) with no result → declare failed
7. Only then retry with adjusted prompt or device type
```

**Never retry with the same prompt during the polling window.** Stitch queues generations; a retry before the first one lands creates duplicate work and does not speed up the original.

The official server has no `generation_status` or `list_generations`; polling is the tracking path. If a wrapper in your environment does expose them, use them as a first signal before polling.

**Bail condition:** After 2 failed desktop generation attempts via MCP, switch to Stitch browser UI for desktop and continue MCP polling for mobile.

**Incomplete or lagging screen lists:** `list_screens` and `get_project` can lag far behind. On 2026-11-08, screens that `edit_screens` had created successfully were still missing from both minutes later while the web UI showed them. Keep the screen ID from each response; it is the only reliable handle. Do not assume list lag means failure.

**Timed out with no ID:** a timed-out call can still finish 10-20 minutes later (two generations and one edit did on 2026-11-08). Before generating again, ask the user to check the project in the web UI; if needed, ask for a zip export, unpack it into a new empty folder as untrusted data, and compare file hashes with what you already have.

**Small text edits:** a text-only `edit_screens` on an existing screen may report success as DOM operations on the same screen without saving. Verify with `download_file` (HTML); if the target is code, fix the text there instead of spending generations.

**HTTP-level errors:**

| Error | Likely cause | Action |
|-------|-------------|--------|
| `401 Unauthorized` | Credential expired or missing | Ask the user to refresh the MCP credential in their runtime config; never print or paste the key |
| `400 Bad Request` | Invalid payload or vague prompt | Check parameters, refine prompt |
| `429 Too Many Requests` | Rate limit | Wait 60s, retry with backoff |

---
