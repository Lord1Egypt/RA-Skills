## Iteration & Refinement

### Continue suggestions

After generating a screen, Stitch suggests one-click follow-up edits (e.g., "Add a buy/sell button for quick trades"). Check these before writing your own follow-up prompt — they're often useful and faster than crafting a custom edit.

### Variants

Variants let you generate multiple takes on a design and scope the exploration.

**Creativity levels:**

| Level | Behavior | When to use |
|-------|----------|-------------|
| **Refine** | Small tweaks, close to original | Polishing an accepted direction |
| **Explore** | Balanced creativity — the sweet spot | Finding layout and imagery options |
| **Reimagine** ("YOLO" in Stitch UI) | Wild reinterpretation | Breaking out of a rut, early exploration |

**Scoping:** Scope variants to specific aspects: **layout**, **color scheme**, **images**, **text**, or **font**. This prevents unwanted changes in areas you've already accepted.

**Best practices:**

1. Generate 3-5 variants (adjustable count in the UI)
2. **Expect artistic flops** — not every variant will be usable. This is normal.
3. **Expect complete failures** — some variants may produce blank, broken, or empty results. Don't analyze failures; just regenerate.
4. Don't pick one winner — pick elements from multiple screens and compose
5. Everything in Stitch is a component; you can mix and match across variants
6. Use scoped prompts to refine specific aspects without breaking what works
7. Use the **custom instructions** field in the variant dialog for specific guidance

Note: `generate_variants` through MCP may still have reliability limitations (see capability boundaries). Variants are most reliable through the browser UI.

### Annotate: visual targeted editing

The **Annotate** feature lets you drag-select a region of a generated screen and describe changes for just that area. This is a visual alternative to text-based element targeting — useful when you can see what needs to change but don't want to re-describe the full context.

Best for: layout tweaks in a specific section, repositioning elements, adjusting spacing in one area without affecting the rest.

### Direct inline editing

You don't always need the prompt box. Click any element on a generated screen to:

- **Edit text directly** — click and type, no regeneration needed
- **Use AI on a specific element** — targeted changes without affecting the whole screen

This is the fastest path for small copy changes, label fixes, or tweaking a single button. Use it before reaching for a full prompt-based edit.

### Quick style adjustments

Select a screen → **Edit → Edit Theme** to open a right panel with color and corner radius controls. Faster than re-prompting for small style changes. You can also right-click any screen for quick access to editing features and keyboard shortcuts.

### Multi-screen hub-first pattern

For multi-screen projects, the critical rule: **generate a hub screen first, then derive all other screens via edit — never fresh generate siblings.**

Why: `generate` invents everything from scratch (layout, colors, spacing, typography). `edit` takes the source screen as the visual basis and changes only what you describe. Navigation, typography, and color palette stay consistent.

Recommended flow:
1. Generate the hub screen → review carefully
2. All further screens of the same concept → `edit` from the hub
3. Max 1-2 changes per edit prompt — too many changes = unpredictable results
4. Even elements you did NOT mention can change in an edit. Fewer changes = more stable output.

During the concept phase, 3-4 consistent core screens are enough. Full screen coverage only after the concept is approved.

### Screen review loop

After each generate or edit, categorize issues systematically:

| Category | Examples | Action |
|----------|----------|--------|
| **Stitch-fixable** | Missing section, wrong layout order, major color error, wrong navigation | Edit prompt (max 1-2 changes) |
| **Post-export fix** | Exact pixel spacing, icon details, typography fine-tuning, persistent content hallucinations | Note it, move on |

**Decision tree:**
- Stitch didn't fix it after 2 edits → note as post-export fix, move on
- Detail work (shadows, exact radii, pixel spacing) → directly note as post-export fix, don't waste edit budget
- Structural issue (section missing, navigation wrong) → Stitch edit

The user decides which tool to use for post-export fixes (Figma, code, etc.). Do not prescribe a tool.

### Acceptance checklist before handoff

Before calling a screen "approved" or ready for implementation, write a short checklist from the product source and verify it against the actual screenshot:

1. required brand/product name is visible
2. primary user task is visible without scrolling or ambiguity
3. required entities, rows, tabs, or actions are present in the visible screen
4. forbidden entities or out-of-scope features are absent
5. navigation matches the real app shell, not a generic generated shell
6. ad, legal, privacy, or monetization areas are placed away from the primary task
7. generated assets are robust enough for the target platform, or explicitly replaced by typographic/vector-safe UI

For dense mobile screens, put hard content requirements near the top of the prompt:

```text
Must visibly include exactly these rows in the screen: [A, B, C].
Do not add hamburger menus, side drawers, account controls, or features outside the current product phase.
Use text chips, local icons, or symbols only; do not rely on generated remote images for repeated row avatars.
```

This avoids a common failure mode: a visually attractive screen that misses required content or adds generic app chrome.

### Asset robustness for app handoff

For mobile/native-app targets, prefer UI elements that translate cleanly into local widgets:

- use typographic chips, initials, currency codes, or simple vector-like symbols for repeated row avatars when exact imagery is not essential
- avoid relying on generated or remote flag/avatar images for core app UI unless those assets are part of the real product
- if Stitch produces broken, inconsistent, or overly branded icons, fix that in Stitch before handoff or mark it as an intentional native implementation change

This is especially important for Flutter: local text/icon tokens are easier to implement, theme, test, and keep accessible than arbitrary generated image assets.

### Sequential wizard / multi-step pattern

Generate each step individually, using the previous step as base:

> "Use the existing Step 2 screen as the base. The following elements must stay exactly identical: [header, sidebar, progress indicator, page title]. Change ONLY these elements: [form content, step number, CTA label]."

Without explicit constraints, Stitch will change headers, titles, and layout between steps.

### Copywriting as a design step

Generic placeholder text makes even a beautiful layout feel like a template. Real copy makes the design feel real.

**When:** After the creative direction and design system are stable, but **before** the final design pass. Copy is not a finishing touch — it's a structural element.

**How:**

1. Use an LLM or agent skill with your DESIGN.md as context
2. Include the app description, community aspects, and emotional goals
3. Get multiple options for headlines, subheadlines, CTAs
4. Review and revise before feeding back into Stitch
5. Paste the copy into a variant prompt scoped to text content

The copy should match the creative brief. If your direction is "prestigious journal," the copy should sound like one.

Treat generated copy as design material, not verified facts. Check claims, prices, legal language, medical/financial wording, and user-visible promises before implementation.

### Multi-page expansion

After generating a page with navigation (sidenav, tab bar, etc.), rapidly scaffold the rest of the app:

> "Build me a page for each of the items in the left hand navigation"

Stitch generates all sub-pages in one shot, carrying the design system forward. Some pages may introduce inconsistencies (e.g., a top nav on one page when the rest use a sidenav) — expect minor cleanup.

**Brand consistency:** When adding pages, you don't need to re-specify the brand or design language. A minimal prompt like "design a second page for pricing" is enough — Stitch carries the color scheme, typography, and brand name forward.

### Mobile-from-web conversion

After designing a web/desktop screen, use **Generate → "build a mobile app version"** to have Stitch adapt the layout for mobile. This produces a separate mobile screen based on the same design system.

Expect some inconsistencies (chart types, minor layout differences) — treat it as a starting point, not a pixel-perfect responsive version.

### Sketch-to-design workflow

Upload a sketch or wireframe in the Stitch Web UI, then tell the agent:

> "I uploaded a sketch called [title]. Edit it to [desired changes]."

The agent finds the screen by title via `list_screens` and applies edits via the API.

Use Pro + Thinking for sketch/wireframe uploads — Flash produces noticeably weaker results with drawn inputs.

### Live mode: voice-driven design exploration

Stitch's **Live mode** lets you talk to the AI in real-time while it sees your screen. It can suggest design changes, adjust layouts, and generate new versions — all through conversation.

Good for:
- quick exploratory direction changes ("make the text more luminous")
- getting the AI's opinion on readability or layout issues
- hands-free iteration when you're reacting visually

Not good for:
- precise, scoped edits (use text prompts or direct inline editing instead)
- complex multi-step instructions (the AI may drift)

**Rule of thumb:** Live mode is for creative exploration. Text prompts are for precise control. Direct editing is for surgical changes.

### Redesign as style guide, not copy

Stitch 2.0's redesign feature does **not** replicate the source screenshot. It uses it as a **style guide**: pulling patterns, component placement, and design language, then applying them to your original content.

When the reference is a third-party product, preserve the intent and pattern language, not exact brand identity, proprietary assets, or unique copy.

**Tip:** Use a full-page screenshot tool (e.g., GoFullPage) instead of capturing section-by-section. One full-page reference gives Stitch the complete design context in a single shot.

### Cross-device preview

Before exporting, click the **Preview** button to see your design on phone, tablet, and desktop form factors. This catches responsive issues early. Make this a mandatory step before any export to AI Studio or code translation.

### Heat map (attention audit)

Select a generated screen → **Generate → Predicted Heat Map** to see where users' eyes will land first. Use this as a quality gate: if key elements (CTAs, primary info) aren't in high-attention zones, iterate before moving to code.

Heuristic: "If your buy button isn't glowing on the heat map, fix the design before you code it."

**Known issue:** The heat map may generate for the wrong page or create a new page instead of analyzing the selected one. Verify which screen it actually analyzed before trusting the results.

### Prototype mode tips

After generating pages, select 2+ screens and click **Prototype** to get an interactive click-through:

- Stitch auto-connects screens based on navigation elements
- Turn on **hotspots** to see clickable areas
- Switch between mobile/tablet/desktop to verify responsive behavior
- Select a specific element → "Change with AI" for targeted edits (e.g., add animation) without regenerating the whole screen
- Edit text directly on elements without re-generation
- **"Imagine a new screen"** suggests new pages based on your existing design context
- After adding new screens manually, use **connect to screen** to wire up navigation

This is a browser-only feature but invaluable for validating user flow before coding.

---
