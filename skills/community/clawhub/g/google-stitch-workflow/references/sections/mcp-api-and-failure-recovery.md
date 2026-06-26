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

### Context menu → MCP mapping (based on current Stitch MCP surface)

Use this mapping to decide whether to attempt an action via MCP or ask for browser execution.
If an item is not listed here and not in `tools list`, treat it as browser-only.

| Browser action (common labels) | MCP status | Notes / tool |
|---|---|---|
| **Edit** | MCP | `edit_screens` |
| **Variants** | MCP (weak/unstable) | `generate_variants` (expect reliability variance) |
| **Regenerate** | MCP (approx) | Prefer `edit_screens` with a tight prompt; variants can branch unpredictably |
| **Design system** | MCP | `list_design_systems`, `create_design_system`, `update_design_system`, `apply_design_system` |
| **View code** | MCP (read) | `get_screen` (look for `htmlCode` fields / downloadUrl when present) |
| **List projects/screens** | MCP (read) | `list_projects`, `list_screens`, `get_project`, `get_screen` |
| **Instant prototype** | Browser-only (usually) | Not represented in current MCP tool list; run in browser and then continue via artifacts |
| **Predictive heat map** | Browser-only | Run in browser |
| **Missing states** | Browser-only | Run in browser; manually encode states into the transfer contract/checklist |
| **Preview sizes / QR / connections** | Browser-only | Use browser preview to capture reference screenshots for the Fidelity Pack |
| **Export / Download** | Browser-only in most setups | If you need zip/code, do it in browser and store artifacts next to the screen family |
| **Duplicate / Delete / Favourite / Focus** | Browser-only (unless surfaced) | Not in current MCP tool list; treat as browser-only |

### Capability boundaries

**Verified MCP capabilities** (default safe surface):

- `list_projects`
- `get_project`
- `list_screens`
- `get_screen`
- `create_project`
- `generate_screen_from_text`
- `edit_screens`

**Optional wrapper capabilities** (use when present, never assume):

- `fetch_screen_image` (preview retrieval)
- `fetch_screen_code` (post-approval code retrieval)
- `generation_status` (long-run status polling)
- `list_generations` (generation tracking)

**Known weak or unverified areas** — treat as unstable until revalidated:

- `generate_variants` — reliable through browser UI (see Variants section), less predictable via MCP
- screenshot-driven redesign through MCP
- prototype creation through MCP
- browser-style canvas operations beyond basic project and screen inspection

**Browser-only product features** — do not infer MCP can perform these:

- image or screenshot redesign
- prototype-oriented workflows
- broader canvas interactions
- newer browser-facing product features

### Parameter discipline

The MCP surface is parameter-sensitive. Incorrect casing or identifier shape can produce generic invalid-argument failures.

**`deviceType`:** Use uppercase enum values when explicitly setting a device: `"MOBILE"`, `"DESKTOP"`. If uncertain, omit the parameter instead of guessing. For `edit_screens` in particular, **omit deviceType entirely** — including it can cause invalid-argument errors.

**`modelId`:** Use only identifiers exposed by the active MCP tool schema. Typical values include `"GEMINI_3_FLASH"`, `"GEMINI_3_PRO"`, and `"GEMINI_3_1_PRO"`. Treat browser labels such as "Flash" or "Pro Thinking" as product labels that must be mapped to MCP enum values before calling tools.

**`selectedScreenIds`:** For `edit_screens`, pass bare screen IDs as an array — no `"projects/xxx/screens/"` prefix. Wrong: `["projects/xxx/screens/abc123"]`. Right: `["abc123"]`.

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

**Rule:** After receiving any timeout error on `generate_screen_from_text`, do NOT retry immediately. Set up a 60-second polling interval via `list_screens` and wait. Desktop screens regularly take 5-10 minutes to appear after the HTTP timeout.

**Additional reality:**
- Stitch can generate multiple screens (variants) from a single prompt — do not assume exactly one new screen per generate call
- **The screenshot `downloadUrl` may be empty even after the screen entry appears in `list_screens`.** Poll for the screenshot file to become available before downloading. This typically resolves within seconds to a few minutes.
- **Parallel generation across device types is safe.** If you need mobile and desktop, kick off both simultaneously. They generate independently and poll each on its own timeline.
- Mobile generation is significantly faster and more reliable than desktop; prefer mobile-first even when desktop is the target, then derive the desktop from the mobile screen via `edit_screens`
- If desktop generation fails after 2 attempts via MCP, open Stitch in browser directly and generate desktop there

### Failure handling

**`Request contains an invalid argument.`** — Check in this order:

1. `deviceType` — for `edit_screens`, omit it entirely; for `generate_screen_from_text`, verify uppercase
2. `modelId` spelling — check against known identifiers
3. `selectedScreenIds` shape — bare IDs only, no resource name prefix
4. whether the screen is genuinely editable generated output (`htmlCode` present = likely safe to edit)
5. whether the prompt is trying to change too much at once

**Generation timeout — the canonical recovery path:**

Long-running operations may complete even when the client sees a timeout. The screen appears in `list_screens` moments later.

```
1. Record: T=0 at HTTP timeout
2. Wait 60s, then call: list_screens with projectId
3. Inspect result for new screen matching your deviceType
4. If found → download screenshot + htmlCode → done
5. If not found → repeat step 2 every 60s
6. After 3min (mobile) or 10min (desktop) with no result → declare failed
7. Only then retry with adjusted prompt or device type
```

**Never retry with the same prompt during the polling window.** Stitch queues generations; a retry before the first one lands creates duplicate work and does not speed up the original.

**If optional tracking tools ARE available**, use them as a first signal before polling:
```
1. query generation_status for the active generation
2. inspect list_generations to detect completion artifacts
3. only retry when status confirms failure or no artifact landed
```

**Bail condition:** After 2 failed desktop generation attempts via MCP, switch to Stitch browser UI for desktop and continue MCP polling for mobile.

**Incomplete or lagging screen lists:** `list_screens` may lag behind a successful operation. If the originating call indicated success, re-check before retrying. Do not assume immediate list lag means failure.

**HTTP-level errors:**

| Error | Likely cause | Action |
|-------|-------------|--------|
| `401 Unauthorized` | Token/API key expired | Refresh auth, retry once |
| `400 Bad Request` | Invalid payload or vague prompt | Check parameters, refine prompt |
| `429 Too Many Requests` | Rate limit | Wait 60s, retry with backoff |

---
