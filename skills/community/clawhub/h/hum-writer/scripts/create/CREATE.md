# /hum create [platform] [post type] [idea ID or keyword]

Drafts content for a specific platform and post type using the user's voice and channels.

## Arguments

| Argument | Required | Values |
|----------|----------|--------|
| platform | yes | `X`, `LinkedIn` |
| post type | yes | Platform-specific (see below) |
| idea ID or keyword | yes | Idea ID (e.g. `I042`) or freeform keyword |

## Post Types by Platform

**X:**
| Post Type | Format |
|-----------|--------|
| `Tweet` | Single tweet, under 280 chars, hook-driven. Optional media (image/video). |
| `Thread` | Multiple numbered tweets, each under 280 chars. Hook in tweet 1. Media can attach to any tweet. |
| `Article` | Long-form post, up to 25,000 chars. Premium subscribers only. Rich text formatting (H2 section headers, bold, italic, lists). Cover image required. Draft in full prose with 3-6 H2 sections. Each section is a natural reading chunk. Open with a strong hook paragraph, close with a reflection or question. Write a 1-2 sentence intro post to accompany the article. |

**LinkedIn:**
| Post Type | Format |
|-----------|--------|
| `Post` | Under 200 words. Short paragraphs, no bullet lists in body. Opens with observation (not "I"), ends with reflection/question. Optional media. |
| `Article` | Long-form, 600-1000 words. Section headers allowed. Requires cover image and a short intro feed post to promote it. |

**Examples:**
- `/hum create X Tweet I042`
- `/hum create LinkedIn Article I015`

If platform or post type is missing, ask the user.

---

## Step 1 — Load Context

1. Read `<data_dir>/VOICE.md`, `<data_dir>/CHANNELS.md`, and content samples from `<data_dir>/content-samples/` for voice reference
2. Read `scripts/create/STYLES.md` for available writing styles and their techniques
3. Read `<data_dir>/knowledge/` for any user-curated reference material relevant to the topic
4. Read the idea from `<data_dir>/ideas/ideas.json`
5. If the idea status is not `pending` or `approved`, flag it and ask for confirmation

---

## Step 2 — Deep Research

Research the topic thoroughly before proposing any outline. The goal is to build a fact base the user can evaluate, not to start writing.

### 2a — Web search (3-5 queries)

Run multiple `web_search` queries to cover different angles:

1. **Core topic query** — the topic itself, recent coverage
   - e.g. `"CFOs replacing headcount with AI agents" 2026`
2. **Data / stats query** — quantitative evidence
   - e.g. `"AI automation finance teams" statistics survey 2025 2026`
3. **Contrarian / debate query** — opposing views, criticism, nuance
   - e.g. `"AI replacing finance jobs" criticism risks overhyped`
4. **Example / case study query** — real companies, named examples
   - e.g. `"company replaced finance team AI" case study`
5. **Adjacent angle query** (optional) — related trend that could strengthen the piece
   - e.g. `"FP&A automation tools" trend adoption`

### 2b — Collect and organize findings

For each search, extract and note:
- **Hard data**: stats, percentages, survey results, market sizes (with source attribution)
- **Named examples**: companies, people, products doing/saying something specific
- **Strong quotes**: memorable lines from articles, tweets, or reports
- **Contrarian takes**: dissenting views, risks, or caveats worth addressing
- **Recency signal**: anything that makes this topic timely *right now*

Discard generic filler. Only keep findings that are specific enough to cite in a post.

### 2c — Cross-reference with existing material

- Check `<data_dir>/knowledge/` for anything the user has already curated on this topic
- Check `<data_dir>/feed/feeds.json` for recent feed items on the topic

---

## Step 3 — Propose Outline

Present the research findings, a recommended writing style, and a structured outline for the user's approval. **Do NOT write prose yet.**

Select the best style from STYLES.md using the Style Selection Guide. Consider the content goal, platform, and post type. Styles can be blended (e.g. "Technical Storyteller + Contrarian Debater").

The outline **must** include:

### Style Selection (required)
- **Style:** [Name from STYLES.md, e.g. "Technical Storyteller"]
- **Why this style:** [1-line explanation of why this style fits the content goal and audience]
- **Hook type:** [Which hook strategy from the style, e.g. "The Reframe"]

### Research Summary (required)
- [Key finding 1 — stat or fact with source]
- [Key finding 2 — named example or quote]
- [Key finding 3 — contrarian view or caveat]
- [Key finding 4 — timeliness signal]

### Proposed Outline (required)
```
**Platform:** [X / LinkedIn]
**Post Type:** [Tweet / Thread / Post / Article]
**Style:** [Style name] — [1-line reason this style fits]
**Hook type:** [Which hook strategy from the style]

**Hook:** [Opening line or tension — what stops the scroll]
**Angle:** [The specific POV or contrarian take — why YOUR post is different]

**Tweet 1:** [Hook — what stops the scroll]
**Tweet 2:** [Build — deepen or pivot from hook]
**Tweet 3:** [Evidence or tension — the data or reframe]
**Tweet 4:** [Payoff — what it means in practice]
**Tweet 5:** [Close — reflection or question]

**Named concept (if any):** [Optional framework or label that makes the idea sticky]
**Supporting evidence:** [Which research findings make the cut]
**Excluded:** [Angles deliberately left out and why]
```

**Ask:** "Does this outline work? Want to change the style, angle, hook, or structure?"

**Only proceed to Step 4 after the user approves or adjusts the outline.**

---

## Step 4 — Full Draft

After the outline is approved:

1. Re-read content samples from `<data_dir>/content-samples/` to match the user's voice
2. Write the full piece applying two layers:
   - **Voice layer** (from VOICE.md + content-samples/) — tone, vocabulary, personality. This is the foundation and always takes priority.
   - **Style layer** (from the approved style in STYLES.md) — hook patterns, sentence structures, templates. This provides the structural scaffolding.
3. Follow the approved outline structure and the post type format constraints defined above
4. If the style suggests language that conflicts with VOICE.md (e.g. hype language vs. "no fluff"), VOICE.md wins
5. Present the full draft clearly
6. Ask: "Want to revise, approve, or scrap this?"

---

## Step 5 — Save & Track

**On approval:**
- Update the idea status in `ideas.json` -> `drafted`
- Save draft to `<data_dir>/content/drafts/[Platform] [Post Type] - [title].md`
  - Example: `X Tweet - AI Agents as Headcount.md`, `LinkedIn Article - The Finance Team of 2028.md`
- Save any related generated images to `<data_dir>/content/images/`
  - Examples: diagrams, thumbnails, cover images, or supporting media

**On publish confirmation** ("publish this" / "post it"):
- Update idea/topic status -> `published`, add date
- Use `/publish` to post instead of asking the user to copy/paste

**On revision:**
- Apply feedback and re-draft. Iterate until approved.
