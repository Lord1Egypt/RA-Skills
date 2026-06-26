## Creative Direction

### Creative direction framework

The single biggest lever for better Stitch results is **direction before description**. A generic prompt gives a generic screen. A directed prompt gives something you can actually iterate on.

Direction includes structure, not only style. A screen can have good color and
still feel generic if it uses the same centered heading, repeated cards, and
bottom CTA as every other generated mockup. Choose the composition first, then
style it.

#### 1. Start with empathy

Before touching color, typography, or layout, answer two questions:

- Who is the user?
- What should they feel when they arrive?

Everything else flows from these answers.

#### 2. Replace abstract words with concrete vocabulary

Bad: "make it look high-end", "patriotic", "sporty", "modern"  
Good: "architectural limestone", "neoclassical", "ink on paper", "clay of an old track"

Concrete aesthetic words give Stitch something to build from. Abstract words give you the same generic output as everyone else.

**Tip:** Use an LLM (Gemini works well) to help craft prompts with specific design concepts and aesthetic descriptions. Feed it your empathy answers and ask it to return design vocabulary you wouldn't have thought of.

#### 3. Use metaphors to find layouts

When stuck on layout, ask: "If my site were a physical object, what would it be?"

- A coffee table book → lookbook editorial layout with full-page imagery
- A newspaper → dense typographic grid
- A luxury travel magazine → large headings over cinematic photography

This bridges the gap between "I know what I want" and "I don't know what to prompt."

#### 4. Protect content truth

Do not make the design feel credible by inventing proof. Metrics, testimonials,
customer logos, prices, legal claims, and case-study numbers must come from the
user, from the real product, or remain clearly labelled placeholders.

If the concept does not have proof yet, choose a structure that does not depend
on proof.

#### 5. Avoid decorative chrome

Fake browser bars, phone shells, IDE title bars, traffic-light dots, and code
window frames are usually generated-design tells. Use them only when that chrome
is the actual object being reviewed. Otherwise prefer the product surface
itself, a plain figure, or typography.

### Design system as DNA

Stitch auto-generates a design system for every project. Treat it as the DNA of your design, not decoration. It covers colors, fonts, components, and — critically — a structured creative brief.

#### DESIGN.md

Stitch generates a **DESIGN.md** tab covering creative direction, color hierarchy with roles, typography rationale, elevation, components, and dos/don'ts. This is what drives the design system.

Treat `DESIGN.md` as a two-layer artifact:

- a token layer with the concrete values the system depends on
- a prose layer with the reasoning for what those values are supposed to do

Keep those two layers aligned. If the rationale and the token values drift apart, the design system stops being reliable for both Stitch and coding agents.

Think of tokens as **named design decisions**, not loose variables. `primary` is not just a hex slot; it is the role for the main ink of the product. `body-main` is not just a size; it is the role for default reading copy. The current value fills that role, but the role is the durable part.

**What you can do with DESIGN.md:**

- edit it directly in Stitch to course-correct
- have an LLM generate an improved one
- copy it to new projects for consistency (paste it into a new prompt and Stitch builds from it)
- copy it into your coding agent (VS Code, Cursor, etc.) as a rule set that maintains design consistency when translating Stitch output to real code

**DESIGN.md portability pattern:**

1. Generate a design in Stitch and let it create the DESIGN.md
2. Review and refine the DESIGN.md inside Stitch
3. Copy the DESIGN.md content
4. Paste it into your coding agent's context (system prompt, rules file, or inline)
5. Use it as the style authority when translating Stitch exports to production code

This bridges the gap between Stitch's design environment and your coding environment, ensuring the coding agent respects the same typography, color hierarchy, spacing rules, and component decisions.

This is the single most portable artifact in your Stitch workflow. Invest time in getting it right.

**Creating a custom DESIGN.md outside Stitch:**

1. Write a minimal design-system brief first: visual posture, intended mood, main user job, and 3-5 things the UI must not resemble.
2. Turn that brief into a compact `DESIGN.md` with:
   - YAML front matter for the durable tokens: color roles, typography, radius, spacing, and only the stable component rules
   - markdown sections for the why: overview, colors, typography, layout, components, and do's/don'ts
3. Keep the token layer concrete. Keep the prose layer directional. Do not mix them.
4. Define the baseline role anchors clearly:
   - `primary` for the main ink and core text emphasis
   - `neutral` for the canvas and emotionally neutral surfaces
5. In component rules, prefer references to roles over hardcoded raw values. A button should usually point at `primary`, `tertiary`, `on-primary`, or another named role instead of embedding a literal color directly.
6. Keep the Components section conservative. Encode the stable reusable rules, not every temporary visual exception.
7. In Stitch: Design Systems → Create New → paste the finished `DESIGN.md` → Save
8. Stitch visualizes the design system immediately — colors, fonts, spacing all rendered
9. Generate screens using this custom design system as the base

This pattern is useful when you've already brainstormed design direction with a coding agent and want to transfer that direction into Stitch.

If the copied `DESIGN.md` will become a real project artifact outside Stitch,
validate it before treating it as authoritative:

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md diff DESIGN-before.md DESIGN-after.md
```

Use `lint` as part of the normal edit loop, not just as a final gate: read the current design system, make the change, lint it, fix the findings, then re-check. Use `diff` before and after meaningful revisions to catch token drift or accidental regressions in the design system itself.

**Importing from an existing website:**

Beyond pasting a URL for style hints in a prompt, you can import a website's design as a formal design.md file via the design systems panel: provide the URL and Stitch crawls the site, extracting style and typography into a structured design system. This gives you an editable, portable design foundation rather than a one-off style hint.

#### Color hierarchy (not just a palette)

Colors have jobs based on visual weight and importance. Reach for the role first, then the value that currently fills it. That keeps the design system semantic instead of turning it into a bag of swatches.

`Primary` and `neutral` are the anchor roles. In practice, `primary` usually carries the reading ink and strong emphasis, while `neutral` carries the background and surface system.

Colors have jobs based on visual weight and importance:

| Role | Usage | Visual weight |
|------|-------|---------------|
| **Neutral** | 80-90% of the canvas — the background | Lightest |
| **Primary** | Headings, body text, core content | Dark, high contrast |
| **Secondary** | Subdued support text | Softer than primary |
| **Tertiary** | Accent, CTAs, hover states | Loudest, but used the least |

The tertiary color is third in volume but first in visual pull. Choose it deliberately.

#### Font hierarchy

Stitch sets up three font slots: headline, body, and label.

Opinionated guidance:
- Choose fonts that match your creative direction, not just "what looks nice"
- **Space Grotesk is great for labels and timestamps. It does not belong in headlines.** (Stitch will put it there — override it.)
- A font like Public Sans works for both headline and body when you want official-but-approachable
- Match the font personality to the emotional goal

#### Corner radius as a design decision

Corner radius is not neutral — it communicates:
- **More rounded** → friendly, approachable, casual
- **Sharp edges** → editorial, serious, stationary-like

Decide based on the feeling you want, not a default.

---
