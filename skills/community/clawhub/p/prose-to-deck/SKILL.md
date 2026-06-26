---
name: prose-to-deck
description: |
  Transform articles, essays, transcripts, and other long-form writing into polished single-file HTML presentations with editorial pacing and strong visual storytelling.
  Use when the user wants a scrollable slide-style deck for review, presentation, or sharing, especially when the output should feel designed rather than mechanically converted.
  Supports review and auto workflows, structured intermediate artifacts, optional author credit, and optional named style seeds.
  Not suitable for fixed-size screenshot cards, social image posts, batch PNG export, or generic PowerPoint cloning.
---

# Prose to Deck

Transform long-form writing into a polished, full-screen scrollable HTML presentation.
Output is a single self-contained `.html` file inside a dedicated project folder.

## Example requests

- Turn this article into a scrollable slide-style HTML presentation.
- Visualize this essay as a polished single-file presentation for review.
- Convert this transcript into an editorial HTML deck with `mode=auto`.

---

## Execution Modes

| Mode                    | Behavior                                                                                        |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| `mode=review` (default) | Pause at each HITL checkpoint, write the stage file, notify the user, and wait for confirmation |
| `mode=auto`             | Skip all pauses — write all stage files and continue immediately                                |

In both modes, every stage produces a file. The difference is only whether execution pauses for approval.

**HITL response rules (applies to all checkpoints):**

- User replies "go" → update `progress.md` status to `approved`, continue to next phase
- User replies with change instructions → apply changes, re-notify
- `mode=auto` → log decision to Decisions Log, continue immediately

---

## Project Folder

Every execution creates a dedicated working directory. By default it lives under `./projects/` in the current working directory. All intermediate work and the final output live there unless you intentionally pass a different project root to the init script.

```text
projects/<slug>-<timestamp>/
  progress.md              ← created by init script; tracks stage status throughout execution
  01-analysis.md           ← Phase 1 output: content analysis
  02-slide-plan.md         ← Phase 2 output: slide sequence plan  [HITL-1]
  03-visual-direction.md   ← Phase 3 output: visual direction decision  [HITL-2]
  04-build-notes.md        ← Phase 4 output: per-slide layout notes
  index.html               ← Phase 4 output: final presentation
```

**Artifact formats** are defined in individual reference files:

- `progress.md` format → `references/artifact-progress.md`
- `01-analysis.md` format → `references/artifact-analysis.md`
- `02-slide-plan.md` format → `references/artifact-slide-plan.md`
- `03-visual-direction.md` format → `references/artifact-visual-direction.md`
- `04-build-notes.md` format → `references/artifact-build-notes.md`

**Resuming interrupted execution:** read `progress.md` to determine where to resume. Do not re-run stages already marked `done` or `approved`. Use this table:

| Status value                 | Action on resume                                    |
| ---------------------------- | --------------------------------------------------- |
| `pending`                    | Run the phase normally                              |
| `in-progress`                | Re-run the phase (it was interrupted mid-execution) |
| `done`                       | Skip — output already exists                        |
| `awaiting-approval`          | Re-surface the HITL message to the user and wait    |
| `approved` / `approved-auto` | Skip — already approved, proceed to next phase      |

When resuming from Phase 3 or later, re-read the references for that phase before continuing — do not assume prior context is still loaded.

---

## Phase 1 — Content Analysis

**Goal:** Understand the source material. No design decisions yet.

Read: `references/artifact-analysis.md`

### Steps

1. Parse invocation parameters: `source`, `author`, `mode`, `style`. If `source` is missing, ask the user to provide it before proceeding.
2. If `source` is a file path, read the file. Do not proceed until full content is read.
3. Derive the base slug from the article title (lowercase, hyphens, max 40 chars). Then run the bundled Python init script to create the project folder and all artifact files:

   ```bash
   python scripts/init_project.py "<base-slug>" "<author>" "<mode>" "$(pwd)/projects"
   ```

   If the environment exposes `python3` instead of `python`, use `python3` with the same arguments.
   The fourth argument is the project root. Use `$(pwd)/projects` by default, or pass a different absolute path only when the user explicitly wants another location.

   The script appends a timestamp with second-level precision to the slug (for example `career-guide-20260401-143022`) and adds a numeric suffix if needed to avoid collisions. It then creates the project directory, writes the initial `progress.md`, and touches all artifact files.
   Capture the final slug from the script's stdout and combine it with the project root to get the actual directory path for all subsequent file paths.
   Do not create any project files manually.

4. Update `progress.md`: `phase1: in-progress`. Then immediately update the `Source` field in `progress.md` with the actual file path provided (or `"inline text"` if the content was given directly in the message). The init script cannot know the source — this is your responsibility to fill in.
5. Answer these three questions:

**How many distinct ideas are here?**
Count ideas, not words. A 2000-word essay built around one central claim is still one idea.
Five short paragraphs each making a separate argument are five ideas.

**What is the logical structure?**

Don't force the content into a named category. Instead, ask:

- What does the author want the reader to _feel_ by the end — convinced, equipped, reframed, or moved?
- Where does the tension live? Is it between old and new, between two opposing views, between a problem and its fix, or between what people believe and what's actually true?
- How does the argument move? Does it build (each idea requires the previous), branch (parallel threads that converge), or spiral (returning to the same core from new angles)?
- Is there a moment of surprise or reversal? Where does it land in the sequence?
- What would be lost if you removed the first slide? The last? That tells you what's load-bearing.

Name the structure in your own words — something like "builds from misconception to correction" or "three parallel lenses on one problem" is more useful than a generic label. The name should predict the slide sequence.

**What is the single most important thing?**
If this presentation had only one slide, what would it say?

6. Write `01-analysis.md` (format: `references/artifact-analysis.md`).
7. Update `progress.md`: `phase1: done`.

Proceed to Phase 2 immediately. No HITL here.

---

## Phase 2 — Slide Plan

**Goal:** Decide how to map the content into a slide sequence. This is a creative decision.

Read: `references/artifact-slide-plan.md`, `references/headline-system.md`

### Steps

Update `progress.md`: `phase2: in-progress`.

For each slide, determine:

- **Job** — one phrase, 5 words max. If you can't name it, split the slide.
- **Main claim** — the one thing it must communicate. This is the full judgment, not automatically the on-screen title.
- **Display headline** — the title language the reader sees first. By default this should be shorter, sharper, and more visual than the full claim.
- **Support line** — optional, but strongly encouraged whenever the headline is compressed. Use it to recover nuance instead of forcing the headline to carry the entire argument.
- **Content shape** — what is the natural form of this information?

Content shape questions to ask:

- A single powerful statement — how much space does this idea need to land?
- Two things in tension — how should their visual weight relate?
- Parallel items with no ranking — what holds them together without implying order?
- Items with a clear hierarchy — how does size, position, or weight express the levels?
- A progression over time — what connects the steps, and what separates them?
- A quantitative claim — does a visual encoding make the magnitude more immediate?
- Relationships between concepts — are the connections as important as the nodes?
- A quote or moment of emphasis — what does this need around it to land with force?

**Sequence rules:**

- Always open with a cover (title + core thesis + @author if provided)
- Always close with a conclusion (key takeaway, not a summary of summaries)
- Every slide earns the next — the sequence should have momentum
- **Never** pad to hit a number.
- **Never** compress two distinct ideas to save space.
- **Hard limit: maximum 15 slides total.** If the content analysis yields more than 13 distinct ideas, make merging decisions here — combine closely related ideas into one slide rather than deferring the problem to Phase 4. A presentation that can't be told in 15 slides hasn't been edited yet.

**Headline rules:**

Use `references/headline-system.md`.
In Phase 2, explicitly choose `Display headline` and `Support line` instead of assuming the `Main claim` becomes the title.
Record only genuine poster-style exceptions in the `Headline exceptions` section of `02-slide-plan.md`.

Write `02-slide-plan.md` (format: `references/artifact-slide-plan.md`).

### HITL-1 Checkpoint

Update `progress.md`: `phase2: awaiting-approval` (review) or `phase2: approved-auto` (auto).

**If `mode=review`:** notify the user and stop. Use the actual project directory path, not the placeholder:

```
✋ HITL-1 — Slide plan ready

Wrote `[project-dir]/02-slide-plan.md`.
This is the most important checkpoint; the plan drives all downstream work.

Reply: go / change requests
```

**If `mode=auto`:** log to `progress.md` decisions log and continue:

```
[AUTO] HITL-1: <N> slides
  Core thesis: "<thesis>"
  Slide jobs: Cover | <job2> | <job3> | ... | Conclusion
```

---

## Phase 3 — Visual Direction

**Goal:** Establish the visual identity of this presentation. This is a design judgment, not a form to fill.

Read: `references/design-system.md`, `references/artifact-visual-direction.md`

`design-system.md` contains design principles — how to think about color, typography, layout, motion,
and consistency. Read it to inform your judgment, not to find ready-made answers.
`materials.md` (loaded in Phase 4) contains the actual implementation tools — CDN links, libraries,
CSS patterns. Don't pre-read it now.

### Steps

Update `progress.md`: `phase3: in-progress`.

**Seed check (always run, regardless of whether `style` was passed):** Read `references/style-seeds.md` now. Scan the available seeds and identify whether the content clearly matches one by background and tone. Record your finding in `03-visual-direction.md` under a `Seed match` field — even if no `style` parameter was passed. This makes the design decision reproducible and surfaces the seed system to future runs.

**If `style=<name>` was passed at invocation:** find the matching seed and treat its `background`, `tone`, and `avoid` fields as hard constraints for this phase. Everything else — specific palette values, typefaces, motifs, atmosphere — is still decided by content analysis. The seed narrows the search space; it does not replace the design judgment.

**If no `style` parameter was provided:** let the content lead entirely. If a seed matches well, note it but do not treat it as a constraint — it is informational only. Ask yourself:

**What does this content feel like?**
Not what category it belongs to — what is its texture? A technical argument has different weight than
a personal essay. A call to action has different energy than a retrospective. The visual direction
should make that texture visible.

**Who encounters this, and where?**
A presentation shared on social media needs to pop at thumbnail size. A focused reading session
rewards quieter, more typographic choices. A live screen presentation benefits from high contrast
and generous scale. The same content can be right for different contexts — pick one and commit.

**What should the reader feel on the first slide?**
Intrigued? Challenged? Welcomed? Impressed? That emotional entry point shapes everything:
background darkness, type weight, accent intensity, whether atmosphere effects add drama or distraction.

**What visual idea could make this memorable?**
Beyond palette and fonts — is there a structural visual motif that could run through the presentation?
A recurring geometric element, a consistent use of negative space, a typographic treatment that
becomes a signature? The best presentations have a visual idea, not just a visual style.

From these answers, make decisions and commit to them. Write `03-visual-direction.md`
(format: `references/artifact-visual-direction.md`) — but treat the format as a minimum record,
not a ceiling. If your direction has nuances the format doesn't capture, add them.

### HITL-2 Checkpoint

Update `progress.md`: `phase3: awaiting-approval` (review) or `phase3: approved-auto` (auto).

**If `mode=review`:** notify the user and stop. Use the actual project directory path, not the placeholder:

```
✋ HITL-2 — Visual direction ready

Wrote `[project-dir]/03-visual-direction.md`.

Reply: go / change requests
```

**If `mode=auto`:** log and continue:
`[AUTO] HITL-2: <direction name> — <one-sentence reason>`

---

## Phase 4 — Design and Build

**Goal:** Build the HTML. Phase 2 gives you the content structure; Phase 3 gives you the visual identity.
Use both as your brief. Every slide will still require concrete layout decisions — that's expected.
Make them in the spirit of the plan, not against it.

Read: `references/materials.md`, `references/headline-system.md`, `references/artifact-build-notes.md`, `references/qa-checklist.md`

`materials.md` is the implementation toolkit — icon libraries, chart/diagram tools, animation utilities,
CDN links, and CSS patterns with exactly one correct form. Use what the content needs; ignore the rest.

**Before starting, re-read `02-slide-plan.md` in full.** The `Content shape` column is your primary brief for each slide's layout decision. Do not rely on memory of Phase 2 — the plan is the source of truth.

Update `progress.md`: `phase4: in-progress`.

### 4.1 Output context

This skill produces a **full-viewport scroll-snap presentation**, not a fixed-pixel screenshot card.
Sizing uses `vw`/`vh` units and `clamp()` — not fixed `px` dimensions. The layout must be
usable at any screen size. Do not apply fixed-width card constraints from other skills.

### 4.2 Global setup

Single `.html` file. All CSS and JS inline.
External resources: Google Fonts for the roles actually used + libraries from `references/materials.md` only when content requires them.

If the output uses CDN fonts or libraries, the presentation must still preserve readable core text and structure when those resources fail to load.

- Define CSS custom properties from `03-visual-direction.md` in `:root`
- Load Display and Body fonts, plus Mono only if the chosen direction uses it (see font loading notes in `references/materials.md`)
- Apply atmosphere effects per visual direction
- Set up navigation and reveal system — see `references/materials.md` for correct implementation patterns

**CSS discipline:** Only define CSS classes that you will actually use in the HTML of this presentation. Do not pre-define component classes speculatively. If you define a class and then decide not to use it, remove it before moving to the next slide. Every class in `<style>` must have at least one corresponding element in the HTML body. Inline styles are acceptable for one-off overrides, but if the same inline style pattern appears on more than two elements, extract it into a class.

### 4.3 Headline system before layout

Read `references/headline-system.md` before deciding how the title stack works for a slide.
Do **not** jump straight from `Main claim` to a giant headline.

In Phase 4, decide only these things:

- whether the slide needs a `Support line`
- which headline tier it belongs to
- whether it is using a genuine poster-style exception

### 4.4 Build each slide

Work through slides one at a time. **Do not batch-write all build notes first and then write HTML.** The note and the HTML for each slide are written together before moving to the next.

For each slide N (from 1 to total):

**Step A — Write the build note first.**
Append the layout note for slide N to `04-build-notes.md` (format: `references/artifact-build-notes.md`):

> **Layout:** [one sentence] — **Because:** [content shape from `02-slide-plan.md`]
> **Headline strategy (only if non-default / noteworthy):** [display headline] — Tier: [hero-xl | hero-lg | section-md | compact-md] — Support line: [text or none]

If you cannot write the Layout sentence in one clear line, the slide's job isn't resolved — go back to the plan before writing any HTML.

**Step B — Write the HTML for this slide.**
Append the `<section>` for slide N to the output file.

**Step C — Per-slide check before advancing.**
Before moving to slide N+1, verify:

- [ ] This slide has exactly one job matching the build note
- [ ] Headline tier is appropriate for this slide's role
- [ ] If this slide uses a multi-column layout: is there a named CSS class (not just inline styles) with a corresponding rule in `@media (max-width: 768px)`? If inline styles were used instead, flag it and add the responsive rule now.
- [ ] No new CSS classes were defined for this slide that aren't used in its HTML

**Do not proceed to slide N+1 until Steps A, B, and C are all complete for slide N.**

For each slide, ask: **what is the most direct visual expression of this idea?**
Sometimes that's a large headline and nothing else. Sometimes it's a diagram. Sometimes it's
a number so big it fills the slide. The layout should feel inevitable for the content, not assembled
from available parts.

Available materials when you need them — all in `references/materials.md`:

- Icons → Lucide or Phosphor
- Charts → Chart.js, ECharts, or pure CSS
- Diagrams → Mermaid or hand-coded SVG
- Animation → CSS + IntersectionObserver, or GSAP
- Atmosphere → blobs, grid lines, noise texture
- CSS patterns → gradient text, scroll-snap container, responsive clamp

### 4.5 Principles — not rules, but hard-won truths

**One job per slide.** If a slide is trying to do two things, it is doing neither well.

**Density is editorial.** One large headline + two lines of body is not empty — it gives the idea
room to land. Eight bullets is refusing to make a decision.

**Not every slide is a poster.** Let structure, contrast, comparison, or evidence carry the page when that is truer to the content than oversized type.

**Size contrast creates hierarchy.** Large headline (48px+) paired with small mono metadata (11–12px).
Similar sizes feel flat.

**One accent owns each slide.** Use it for gradient text, borders, chart fills, icon color.
Cover and conclusion may use 2–3.

**Spacing is substance.** Padding: 28–36px minimum inside cards. Line-height: 1.75–1.8 for body.
Borders: ≤7% opacity.

**Surprise is a tool.** If every slide uses the same layout pattern, the presentation becomes
predictable. One slide that breaks the rhythm — a full-bleed image, a single word, an unexpected
color — can make the whole thing more memorable. Use it deliberately.

### 4.6 QA and wrap-up

Run `references/qa-checklist.md` in full. This checklist covers **global and structural concerns** — per-slide checks were already handled in the 4.4 loop. Fix issues silently — only surface to the user if a fix requires a design decision that changes the intent of the plan.

**Shareable test:** pick the one slide you'd post standalone — the one that communicates something
valuable even without the surrounding context. Does it have a strong visual hook? Does it make one
clear point? Would someone who hasn't read the article understand why it matters?

If you can't identify a strong candidate, that's a signal — strengthen the weakest slides before
finishing, not after.

Update `progress.md`: `phase4: done`. Record in the Decisions Log:
`Most shareable: Slide N — [reason]`

**Final delivery to user.** Use the actual project directory path and full slug — do not output placeholder text.

Default completion text:

```
✅ Done. Presentation saved to [project-dir]/index.html

Artifacts: progress.md · 01-analysis.md · 02-slide-plan.md · 03-visual-direction.md · 04-build-notes.md · index.html

Most shareable: Slide N — [reason]
```

If `mode=auto`, append: `(auto mode — checkpoints logged in progress.md)`

**Then send the HTML file itself to the user whenever the environment supports file delivery.**
Use the generated `[project-dir]/index.html` as an attachment/document in the current conversation instead of only listing its path.
Prefer a single concise completion flow:

- if the environment has a first-class messaging/file-send tool, send the completion text plus the HTML file to the current user
- avoid duplicate plain-text replies after sending the file
- if file delivery is unavailable in the current environment, fall back to the text summary above
