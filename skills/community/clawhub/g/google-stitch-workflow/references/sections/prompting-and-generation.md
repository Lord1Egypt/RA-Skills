## Prompting & Generation

### App vs Web toggle

Before generating, switch between **App** (mobile/narrow) and **Web** (wide/horizontal) in the Stitch UI. This fundamentally changes the output — Stitch composes a proper layout rather than stretching a design. Don't forget this toggle when switching between mobile and desktop targets.

### Model selection & thinking mode

Stitch offers multiple generation modes. Pick based on where you are in the process:

| Mode | When to use |
|------|------------|
| **Gemini Flash** (`GEMINI_3_FLASH`) | Fast exploratory passes, cheap/small edits, density and copy adjustments |
| **Gemini 3.1 Pro Thinking** (`GEMINI_3_1_PRO`) | First canonical screen, complex structure, native-app handoff targets, fixes where Flash keeps missing constraints |
| **Gemini Pro** (`GEMINI_3_PRO`) | Use only when this is the available Pro identifier in the active MCP surface |
| **Redesign** | You have a screenshot or existing site to work from |
| **ID8** | You only have a vague problem statement; Stitch helps you construct a plan |
| **Live** | Real-time conversational editing; changes appear as you chat (voice-based, AI sees your screen) |

**Thinking mode:** Stitch 2.0 exposes a **Thinking** toggle alongside model selection. Thinking mode takes a few seconds longer but follows complex instructions significantly better than fast mode. Use it when:
- the prompt specifies detailed section-by-section layout
- the design has complex multi-region composition
- you need the output to match a specific structure, not just a general vibe

**Usage budget rule:** Default to Flash for inexpensive exploration and small preservation edits. Spend Pro/Thinking on the first canonical screen, difficult constraint-following, or a final consolidation pass after the direction is clear.

**MCP mapping:** In direct MCP calls, set `modelId` explicitly when model choice matters. The current direct identifiers may include `GEMINI_3_FLASH`, `GEMINI_3_PRO`, and `GEMINI_3_1_PRO`; verify against the active tool schema because names can change over time.

### Component isolation

Stitch's strongest tendency is to generate **full application layouts** — sidebar, header, navigation, content — even when you only asked for a button. To counteract this, include this incantation when generating individual components:

> "Design a single standalone UI component — do NOT generate a full application screen or layout. Show it isolated on a neutral background, like a component in a design system."

Also add: "Make sure all text is fully visible — do not truncate any labels or text with ellipsis."

This produces dramatically better results for component work.

### First prompt: don't start blank

A common pattern from other AI design tools is to start with a blank page and build the design system manually first. **This does not work well in Stitch.** Starting with "build me a blank page with no design system" produces noticeably worse results than letting Stitch generate its own design system from a descriptive initial prompt.

Instead, include your theme and color choices directly in the first prompt:

> "Build me a crypto dashboard with purple as the primary color in dark mode"

Stitch generates the design system (primary/secondary/tertiary/neutral colors, fonts, components) alongside the first screen. You can adjust everything afterward, but you get a much stronger starting point than starting from nothing.

**Also:** mobile designs currently tend to be higher quality than web. If output quality matters more than platform, consider generating mobile first.

### Prompt construction: incremental enrichment

Don't write the final prompt in one shot. Build it up:

1. Start with the app description (1-2 sentences)
2. List the specific screens by name (e.g., "mission overview, trajectory, weather, mission log, system status")
3. Add core functionality per screen
4. Set the vibe with concrete adjectives
5. Optionally: use another AI tool (Gemini works well) to iteratively refine the prompt before pasting into Stitch — this produces significantly better results than writing the prompt directly in Stitch

Simple prompts work for simple apps. Complex dashboards benefit from upfront enrichment.

### PRD + reference image pattern

The most reliable way to get a strong first generation is to combine a **PRD** (Product Requirements Document) with a **reference screenshot**:

1. Find a design you like on the web
2. Capture a full-page screenshot (use a browser extension like GoFullPage — wait for all animations/lazy loads to finish first)
3. Paste the screenshot into ChatGPT or Gemini with a prompt like: *"I want to reference the design in the attached image to create a detailed PRD for a [type of app]. Include design principles, layout system, typography, color palette, components, and page structure."*
4. Review and tweak the generated PRD
5. In Stitch: paste the PRD + attach the reference image together as your first prompt

This produces significantly better results than typing a design description from scratch. The PRD gives Stitch structural guidance (layout system, component hierarchy, color roles) while the reference image anchors the visual direction.

Use references for layout logic, visual vocabulary, and interaction patterns. Do not copy protected brand assets, logos, exact copy, or proprietary product structure unless the user owns the source or explicitly confirms permission.

**Tip:** The PRD doesn't need to be long. Even a bullet-point outline covering layout, typography, and color intent is better than a vague one-liner. Stitch will generate its own design system from the PRD, so focus on *what* and *why*, not on exact pixel values.

### Prompt structure template

Every good Stitch prompt has four layers. Omit one and Stitch fills the gap with generic defaults — that's where "AI slop" comes from:

1. **Context** — who and what: industry, audience, app reference ("Like Linear's dashboard")
2. **Structure** — layout and components: sidebar navigation, card grid, hero section, KPI cards with sparklines
3. **Aesthetic** — visual tone using precise keywords (see style keyword table below)
4. **Constraints** — device, format, what must NOT change

### Style keyword reference

Stitch relies on precise design vocabulary. Use these keywords deliberately:

| Keyword | What Stitch generates |
|---------|---------------------|
| `minimal` / `clean` | Lots of whitespace, restrained palette, simple geometry |
| `editorial` / `magazine-style` | Large typography, dramatic whitespace, museum-curatorial feel |
| `brutalist` / `neobrutalist` | Thick black borders, clashing colors, hard shadows, monospaced type |
| `glassmorphism` | Frosted translucent cards over colorful backgrounds, blur effects |
| `dark mode` | Dark backgrounds with light text, often paired with accent colors |
| `premium` / `luxury` | Restrained palette, serif typography, generous spacing |
| `playful` / `consumer` | Rounded shapes, bright colors, friendly illustrations |
| `vintage` | Texture, paper grain, serif type, aged feel |
| `retro` | Modern homage to past era (80s synthwave, pixel art, neon) |

**Vintage ≠ retro.** Vintage gives you a 19th-century cookbook. Retro gives you 80s neon. Be specific.

**Color directions:** monochromatic, neutral with accent, vibrant on dark, pastel, muted/earthy — or specific: "indigo accent", "emerald green", "warm amber"

### Section-by-section prompt pattern

For best results with complex layouts, structure the prompt as:

1. **Context line** — device and app type: "A mobile dashboard for a crypto tracking app"
2. **Aesthetic line** — visual direction: "dark mode aesthetics with neon purple and green accents"
3. **Section-by-section layout** — each section gets its own sentence: "Top section shows total portfolio value, below that a graph showing a 7-day trend"

Example (web): "A modern clean landing page for a SaaS productivity tool called Flowstate. Wide hero section with a headline 'focus faster' subtext and primary blue CTA button. Below, a three-column feature grid with icons, minimalist aesthetics with lots of white space."

This pattern works better than listing features without spatial context.

### Adjective-driven mood language

Stitch relies on **adjectives to identify mood** rather than exact structural descriptions. "Warm, inviting, premium" works better than "rounded corners, 16px padding, serif font." When prompting, prefer mood and intent language first, then add structure afterward.

### URL-based style extraction

Two approaches, depending on depth:

**Quick (paste in prompt):** Paste an existing website URL into Stitch's prompt area. Stitch extracts the color scheme, typography, and general visual vibe as a starting point. This avoids reinventing a design language that already exists.

**Structured (import as design.md):** Via the design systems panel, provide a URL and Stitch crawls the site, extracting style and typography into a structured design system file. This gives you an editable, portable design foundation rather than a one-off style hint.

### Wireframe-to-design from photos

Upload a photo of a paper sketch and use this prompt pattern:

> "Turn this wireframe into a [fidelity level] [platform] [screen type], [aesthetic direction]"

Example: "Turn this wireframe into a high fidelity iOS login screen, clean white background." Stitch converts scribbles into proper UI elements.

**Use Pro + Thinking for wireframe uploads.** Flash produces noticeably weaker results with sketch/wireframe inputs — the output tends to look flat and generic. Pro + Thinking interprets spatial relationships from drawings significantly better.

Expect variable quality from hand-drawn input. Results depend heavily on sketch clarity and prompt specificity. The impressive examples on social media often come from clean, well-structured sketches combined with detailed prompts.

---
