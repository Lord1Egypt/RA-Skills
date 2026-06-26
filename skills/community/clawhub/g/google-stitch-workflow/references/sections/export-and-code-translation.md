## Export & Code Translation

### Choose the transfer strategy first

After a visual direction is approved, do not assume the next step is "copy the code".
The agent must choose a transfer strategy based on the user's actual destination:

| Destination | Best strategy | What to preserve | What not to do |
|-------------|---------------|------------------|----------------|
| **Flutter / React Native / SwiftUI / Compose** | Native translation from Fidelity Pack | tokens, hierarchy, spacing rhythm, component roles, screenshots | do not port DOM/CSS 1:1 |
| **React / Vue / Svelte / web app** | Use Stitch HTML/CSS as a structural seed, then refactor into app components | CSS variables, layout structure, reusable sections | do not paste monolithic generated code as final app architecture |
| **Figma/design handoff** | Export to Figma or ask user to do browser export if MCP lacks it | frames, autolayout clues, typography, spacing, design comments | do not treat Figma export as production code |
| **AI Studio/prototype** | Export/build as a prototype, then validate behavior and code quality | visual direction, page flow, quick interaction demo | do not ship without review and production hardening |
| **No-code/site builder** | Use screenshots + copy + tokens as implementation reference | section order, content, style roles | do not assume Stitch assets map cleanly to the builder |
| **Unknown stack** | Ask the user before exporting or coding | target platform, desired fidelity, who will implement | do not choose a path silently |

If the user has not specified enough context, ask a short routing question before implementation:

```text
What is the target for this Stitch design?
1. Implement directly in an existing app/codebase
2. Export to Figma/design handoff
3. Build a quick web prototype

If it is an app/codebase, tell me the stack and whether I should modify files now.
```

Once the route is chosen, create the smallest artifact set that supports that route. Do not collect Figma exports, zip files, AI Studio builds, and code artifacts all at once unless the user explicitly needs them.

### Export paths

| Export path | Direction | Best for |
|------------|-----------|----------|
| **Google AI Studio** | One-way push | Simple apps (1-2 pages), quick prototyping |
| **MCP connection** | Bidirectional | Ongoing projects, multi-page apps, iterative development |
| **Download zip** | One-time | Offline work, custom build pipelines |
| **Copy code** | One-time | Quick paste into existing project |
| **Figma** | One-time | Design handoff to designers |
| **Project brief** | One-time | Requirements document for stakeholders |

### Picking the right export for fidelity (practical rule)

If your goal is "the implemented UI feels meaningfully close to Stitch", do not treat the export step as optional.
Pick an export format intentionally based on what you need downstream:

- **You want ongoing iteration with Stitch as the source of truth**: use **MCP connection**
  - Use MCP to pull current screens (and code artifacts if available) whenever the design changes.
  - Use MCP when you want to avoid repeated manual exports and keep the agent in sync.
- **You want the highest-fidelity one-time handoff**: use **Download zip**
  - Zip export is the safest way to capture a consistent snapshot: HTML/CSS, assets, and any bundled artifacts Stitch provides.
  - Prefer zip when the implementation target is not HTML/CSS-native, or when you need offline traceability.
- **You want a quick seed and will refactor immediately**: use **Copy code**
  - Use this only for quick prototypes; it is easy to lose assets and drift without noticing.

Important nuance:
- **MCP is not "export"**. MCP is the bidirectional control plane. You still need a repeatable way to capture an accepted reference snapshot (zip or code artifact) for parity checks and later diffs.
- **Figma is a handoff surface, not a universal bridge**. Use it when humans need design inspection or when the workflow already depends on Figma; it is not required for agent-driven Flutter/native implementation.

### Fidelity Pack (recommended for non-HTML targets and/or non-multimodal agents)

When the implementation target isn't "paste this HTML into a web app", the common failure mode is:
the agent re-creates the UI from memory or vague text, and fidelity collapses.

To prevent that, create a "Fidelity Pack" per accepted screen family before implementing:

1. **Accepted reference screenshots**
   - Capture at least two widths (phone + desktop/tablet) from Stitch Preview.
   - If you only capture one: capture phone. Most drift is visible on dense layouts.
2. **Export snapshot**
   - Prefer **Download zip** for a stable snapshot.
   - If a direct code artifact exists via MCP/tooling, keep it alongside the zip.
3. **Design token map**
   - Extract token intent from `DESIGN.md` into a short table:
     - typography scale (H1/H2/body/caption)
     - spacing scale (xs/s/m/l)
     - radii, shadows, surfaces, elevation intent
     - primary/secondary/accent roles and contrast intent
4. **Structure map (text-only)**
   - Write a compact outline of the screen's hierarchy (landmarks + primary components).
   - This is what a text-only coding agent can follow without "seeing" the screen.
5. **Drift checklist baseline**
   - Start a `missing/mismatched/intentional` list before coding.
   - Anything not backed by the pack is "not guaranteed"; do not invent details.

Implementation rule:
- The coding agent must translate from the **Fidelity Pack artifacts**, not from the prompt that produced the design.
- The Fidelity Pack should be route-specific: native apps need tokens/screenshots/structure; web apps also need exported HTML/CSS; Figma workflows need frames and comments; prototypes need flow/state notes.

### Browser export requirement for Fidelity Packs (when MCP cannot snapshot)

In many environments, Stitch MCP enables iteration (generate/edit/inspect) but does **not** expose the full
export/download surface (zip export, AI Studio export, Figma export, prototype tooling).

Rule:
- If the Fidelity Pack requires **zip/assets** or an export snapshot not available via MCP tools,
  the agent must explicitly request the human to perform the **browser export/download** step.
- Do not pretend MCP can do it. Do not proceed with "best-effort" reconstruction when the artifact is required.

Required request format (copy/paste):

```text
Please do this in the Stitch browser UI for the accepted screen family:
1) Preview at Mobile + Desktop, take 2 reference screenshots
2) Export/Download a zip snapshot (includes assets)
3) Tell me where you saved it (path), or drag it into the workspace
Then I will continue with token extraction + parity checks.
```

### Parity verification (how to stop "looks kinda similar" regressions)

If you care about fidelity, you need a check that fails when drift grows.
After implementing a screen, do at least one of:

- **Screenshot parity check** (preferred)
  - Produce implementation screenshots at the same breakpoints as the Stitch reference.
  - Include the real app shell and platform chrome when those affect available space.
  - Compare manually, or with a pixel-diff/golden workflow available in the target stack.
- **Token parity check** (always)
  - Verify typography scale, spacing scale, and radii match the token map.
  - Fix tokens first; layout fixes are harder when tokens are drifting.

Do not declare a screen "done" without one parity check pass.

### Token extraction from exported code (the missing bridge)

Most "Stitch looks great but the real app looks generic" failures come from skipping token transfer.
Do not eyeball colors/spacing/typography. Extract them.

When you have an export snapshot (zip or code artifact):

1. **Find the token carriers**
   - CSS variables, repeated hex values, repeated radii, repeated shadow values
   - font families + font sizes + font weights
   - spacing constants that recur (8/12/16/20/24...)
2. **Build a token map (small, explicit)**
   - colors: background/surface/text/muted/primary/accent/border
   - typography: display/title/body/caption sizes + weights + line-heights
   - shape: card radius, button radius, input radius
   - elevation: 1-2 shadow styles (not a full shadow zoo)
   - spacing scale: xs/s/m/l/xl
3. **Bind tokens into the target UI system**
   - Replace ad-hoc per-component styling with theme-level tokens first.
   - Only then do layout/structure tweaks.
4. **Lock drift**
   - If tokens drift, everything drifts. Fix tokens before arguing about pixels.

Non-goals:
- Do not attempt a full 1:1 component conversion from monolithic export on day 1.
- Do not recreate layout from screenshots when export artifacts exist.

### First translation pass recipe (make the result "feel like Stitch" fast)

For most implementation targets, the biggest fidelity gains come from replicating a small set of UI primitives
that Stitch outputs consistently, rather than trying to port the entire screen in one go.

Do this in order (per screen family):

1. **Surface system**
   - background color, card color, shadow/elevation style
   - consistent card radius (one number) and padding (one scale)
2. **Typography hierarchy**
   - title weight/size
   - large numeric display style (the "hero number" pattern)
   - muted label style (small caps/label-like weight)
3. **Primary action shape**
   - button height + radius + weight
   - disabled/loading visuals (must not collapse to default)
4. **Choice controls**
   - "pill" selector styling (border, radius, padding) instead of default dropdown styling
   - bottom-sheet selector for long lists when the platform supports it
5. **Entity rows**
   - rows that carry an icon/flag/avatar + name + code on the right
   - keep: alignment, truncation rules, chevron affordance
6. **Highlight card**
   - gradient/solid primary surface for the result card
   - keep: hierarchy + spacing + rounding; do not shrink the hero number
7. **Preset grid**
   - uniform tiles with consistent radius and spacing (avoid default chips)

Only after these primitives exist should you spend time on micro-spacing or exact pixel drift.

### Common drift checklist (seen in real Stitch → implementation ports)

If the result looks "generic" compared to Stitch, it is usually one of these:

- tokens not mapped (colors/spacing/typography/radii are ad-hoc per widget/component)
- default controls leaking through (native dropdowns/chips) instead of pill/tile styling
- missing "entity row" pattern (flag/avatar + name + code alignment)
- highlight card downgraded (no gradient, wrong radius, weak number hierarchy)
- inconsistent padding scale between cards/sections

Fix these before asking Stitch for more edits. This is implementation drift, not design drift.

### AI Studio pipeline

The simplest end-to-end path for getting a working website from a Stitch design:

1. **Design in Stitch** — finalize the direction, verify via cross-device preview
2. **Export → Build with AI Studio** — Stitch automatically uploads images, a markdown file, and a prompt. No manual copying needed.
3. **Press Build** in AI Studio — generates a functional website matching the design
4. **Verify** — check mobile/desktop views in AI Studio, test interactions
5. **Publish** — create a cloud project (may require billing), get a live URL
6. **Customize** — set up custom domain if needed

This is the "Vibe Design → Vibe Coding" pipeline: useful for fast prototypes, but still requires review before treating the output as product code.

**AI Studio as a faster iteration surface:** Once you export to AI Studio, it can be faster than Stitch itself for code-level refinements:
- Timing varies by project and current product behavior; re-check before making workflow promises
- **Screenshot-anchored editing**: paste a screenshot of the specific section to change, describe the edit. The image pins context so the AI knows exactly what to modify.
- AI Studio preserves your full HTML/CSS, so every edit updates the actual code

**Practical flow:** Design direction in Stitch → export to AI Studio → refine details there → publish or copy code.

**AI Studio export gotchas:**
- **Select all screens before exporting.** By default, AI Studio may only receive the active screen.
- **Export page-by-page for complex apps.** Sending 5+ complex screens at once can overload AI Studio (12+ minute builds with missing content).
- AI Studio export is **one-way**. Changes in Stitch after export don't sync back.

### Bidirectional MCP workflow

MCP creates a two-way connection between Stitch and your coding agent:

1. In Stitch: Export → Set up MCP → Choose your tool → Create API key
2. In coding agent: Add MCP server → Search "Stitch" → Install → Paste API key
3. Available tools: create/list/get projects, get/generate screens, pull design files, sync updates
4. **Key benefit:** edit in Stitch → pull changes in coding agent → edit code → push back. No re-export needed.

Recommended hybrid flow for larger projects:
1. Design in Stitch
2. Initial export to AI Studio for the first working prototype
3. Push to GitHub
4. Open in coding agent (Antigravity, Claude Code, Cursor)
5. Connect MCP for ongoing bidirectional iteration

### Figma export

Export to Figma: **Export → Figma → Convert → Copy frame → Paste in Figma.** The resulting auto layout is usable — better than most AI design tool exports — though some elements may be hidden or not fully responsive. Good enough for design handoff and developer inspection.

### Review gate before code translation

Do not port a Stitch output into code until these conditions are true:

- required elements are still present
- the primary user task is clearer than before
- mobile density and hierarchy are acceptable
- the screen fits the rest of the project direction
- the design can be implemented coherently in the current application architecture

If the answer is not clearly yes, keep iterating in Stitch.

### Artifact-first transfer protocol (recommended)

To improve handoff quality from Stitch to implementation in any stack:

1. build a compact PRD first (user task, key screens, layout intent, component/state requirements)
2. add one strong visual reference (screenshot or URL-derived style direction)
3. generate one canonical screen family, not all pages at once
4. approve visually before any code pull/export
5. transfer with artifacts, not memory:
   - accepted screen output
   - `DESIGN.md`
   - export/code artifact
6. integrate screen-by-screen for complex apps instead of bulk export/import
7. run drift checklist (`missing`, `mismatched`, `intentional`) after each integration pass

This protocol reduces the common failure mode: pretty Stitch output + weak implementation fidelity.

### Transfer contract (required before coding)

Before pulling/exporting code for implementation, create this compact contract:

```text
Target screen:
Primary user task:
Required states: loading, empty, error, disabled, success
Must keep: (layout landmarks, component hierarchy, token roles)
Can change: (implementation details only)
Exit criteria: (what must be true to call this screen done)
```

Do not start integration without this contract.

### Per-screen integration checklist

Run this checklist for each screen (not just once for the whole project):

1. structure and hierarchy match accepted design direction
2. `DESIGN.md` token intent is preserved in implementation theme/tokens
3. required states exist and are testable
4. dependencies used by exported code are installed/resolved
5. drift log is updated (`missing`/`mismatched`/`intentional`)
6. any intentional divergence is documented with reason

### Fidelity reality check

For most stacks, "identical to Stitch pixels in every state" is not a realistic default outcome.
The practical target is controlled fidelity:

- preserve structure and hierarchy from accepted Stitch output
- preserve token intent from `DESIGN.md`
- explicitly track drift as `missing`, `mismatched`, or `intentional`
- close high-impact drift first (layout, typography scale, interaction states)

Treat exact pixel parity as an optimization step, not the first integration goal.

### Variant and edit failure handling

If variants or edits produce low-delta or broken outputs:

1. keep the best current candidate as the canonical base
2. restate constraints in tighter language (`keep`, `change`, `do not touch`)
3. switch to smaller edit scopes (one section/component at a time)
4. stop after two low-value retries and mark remaining items as post-export fixes

Do not burn iteration budget on repeated low-signal variant retries.

For greenfield translation from exported Stitch code, also check:

- the exported code represents the accepted direction, not an older candidate
- the layout system is coherent enough to preserve rather than rewrite immediately
- the token layer can be mapped into the target project's theme system
- there is a plan to replace placeholders and hardcoded demo content with real data
- the team will translate deliberately instead of pasting large exports blindly
- all required npm dependencies are installed before integration
- hardcoded colors/sizes have been replaced with project theme tokens

### Design system file injection

When the SDK doesn't support `design_system_id` in generate/edit calls, use this workaround: load a design system markdown file and append its content to the prompt. This carries design tokens (colors, typography, spacing rules) into each generation without relying on Stitch's built-in design system panel.

### Dependency check during integration

When integrating Stitch output into a codebase, check whether the generated code uses libraries not yet installed (e.g. `recharts`, `framer-motion`, `lucide-react`). Run `npm install <pkg>` before integration to prevent build failures.

Also check whether the generated code uses hardcoded colors or sizes that conflict with the project's existing theme — replace them with CSS variables or design tokens before saving.

### Architecture-aware component placement

When integrating components, respect the project's architecture:
- Standard: `src/components/<ComponentName>.tsx`
- Hexagonal/modular: `src/modules/<domain>/components/<ComponentName>.tsx`
- Feature-based: `src/features/<feature>/components/<ComponentName>.tsx`

Don't blindly place everything in `src/components/` — detect the project's convention first.

### Shadcn UI integration

For converting Stitch designs into component-based apps:

1. Set up the **Shadcn MCP** before building (provides tool calls for component operations)
2. Install Google's **Shadcn UI skill** — a detailed guide for converting Stitch output to Shadcn components
3. Add instructions to your agent's config so Stitch MCP output automatically flows through the Shadcn skill
4. Specify additional registries for premium components (e.g., glassmorphism, motion primitives)
5. Workflow: specify the Stitch project name → agent fetches the project → loads Shadcn skill → implements with MCP tool calls + registries

This can produce a more structured component implementation from Stitch designs than static HTML alone. Still run the parity gates and production hardening checks before shipping.

---
