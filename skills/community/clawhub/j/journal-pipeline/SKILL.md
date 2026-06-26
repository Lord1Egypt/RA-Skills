---
name: journal-pipeline
version: 1.0.0
description: Autonomous journal content pipeline for UniqueStaysUSA. Researches keywords, writes editorial content, publishes to Payload CMS, and tracks results. Use when creating journal posts, writing blog content, planning content strategy, or the user says "next post", "write an article", "journal", "content sprint", "publish", or anything about creating travel editorial content. Also triggers on "content calendar", "what should we write next", or "run the pipeline".
---

# Journal Pipeline

Autonomous content machine for UniqueStaysUSA. Combines SEO research, editorial writing, quality enforcement, and Payload CMS publishing into one pipeline. Runs as a PRD-driven loop — pick next article, execute 7 phases, commit, repeat.

## Default Behavior: Autonomous Mode

**When invoked without arguments, this skill runs automatically:**

1. Read the content calendar (`KEYWORD_RESEARCH_AND_CONTENT_CALENDAR.md`)
2. Identify the next uncompleted entry
3. Execute all 7 phases without stopping
4. Only pause if quality gate fails (score below 8.0/10) or user asks

**User overrides:**
- Specific topic: `/journal-pipeline best cabins near Yellowstone`
- Research only: `/journal-pipeline --research-only`
- Draft only: `/journal-pipeline --draft-only`
- Pause point: "stop after the brief"

**If no override is given, assume autonomous mode and execute the full pipeline.**

## The 7-Phase Pipeline

Each phase maps to a PRD story type. The pipeline reads and updates `scripts/ralph/prd.json` for sprint state persistence.

---

### Phase 1: STRATEGY (PLAN-xxx)

Research what to write before writing a single word.

**Read these files:**
1. `KEYWORD_RESEARCH_AND_CONTENT_CALENDAR.md` — content pillars, keyword clusters, monthly schedule
2. `docs/uniquestays-gtm-strategy.md` — distribution channels, KPIs, content goals
3. `scripts/ralph/progress.txt` — what's been done, learned patterns

**If no topic specified — auto-select from calendar:**
1. Parse the current month's table entries
2. For each journal post entry, check if a matching published post exists:
   ```bash
   GET ${NEXT_PUBLIC_SERVER_URL}/api/blog-posts?where[status][equals]=published&depth=0&limit=50
   ```
3. Select the first uncompleted entry
4. Announce: "Starting autonomous creation of [topic] — next in calendar queue"
5. Proceed directly to Phase 2

**Keyword research (always run):**
1. Use WebSearch to check keyword volumes and difficulty for the target keyword
2. Search for the top 3 ranking articles for the target keyword — note their angles, gaps, word counts
3. Check AI citation patterns — search for the topic on Perplexity/ChatGPT to see what sources get cited
4. Identify the competitive gap: what angle is no one covering?

**Article type selection:**
| Signal | Type | Template |
|---|---|---|
| Topic names a specific city/region | Destination Dispatch | 3-5 stays, 1,400-2,000 words |
| Topic names a stay category | Curated Roundup | 8-12 stays, 1,800-2,500 words |
| Topic names a season/month | Seasonal Guide | 5-8 stays, 1,500-2,200 words |
| Topic names an activity | Activity-Based Guide | 4-7 stays, 1,400-2,000 words |
| Topic focuses on one property | Stay Spotlight | 1 stay, 1,000-1,500 words |

**Stay selection:**
```bash
# For destination dispatches
GET /api/stays?where[state][equals]={State}&where[rating][greater_than_equal]=4.7&limit=20&depth=1&sort=-rating

# For roundups
GET /api/stays?where[category][equals]={categoryId}&limit=50&depth=1&sort=-rating

# For activity-based (search by tags)
GET /api/stays?where[tags.tag][contains]={activity}&limit=20&depth=1
```

Select stays ensuring:
- Geographic diversity (for roundups, at least 4+ states)
- Quality floor: `rating >= 4.7`, `reviewCount >= 30`
- Valid `affiliateUrl` (starts with `https://`)
- Hero image exists (`imageUrl` or `image` relationship)

**Auto-proceed unless:** No clear strategic gap exists — only then stop and propose alternatives.

**Output:** Sprint plan with target keyword, article type, selected stays, competitive angle. Update `scripts/ralph/prd.json` with 7 stories for this sprint.

---

### Phase 2: RESEARCH (RESEARCH-xxx)

Collect the raw material.

**For each selected stay, collect from Payload (depth=1):**
- `title`, `subtitle`, `location`, `state`, `region`
- `price`, `rating`, `reviewCount`, `platform`
- `description`, `tags` (array of tag objects)
- `affiliateUrl`, `imageUrl`
- `sleeps`, `bedrooms`

**Identify the "specific detail" for each stay:**
Find at least one concrete detail that could not apply to any other property. Sources:
- The stay name itself (e.g., "Redwood Treehouse" → built into a specific redwood)
- `tags` array (e.g., "Wood-Burning Stove", "Stargazing Deck")
- `description` field (look for named landmarks, distances, species, history)
- Geographic context (elevation, nearest town, driving time)

**External source research:**
1. Search for 2-3 authoritative sources to cite (official tourism, NPS, established publications)
2. Verify any statistics planned for the article
3. Note seasonal information, booking trends, or recent news about the destination

**Verify:**
- All stays have valid `affiliateUrl`
- All stays have images
- No two stays have identical descriptions (if they do, note for differentiation in writing)

**Output:** Stay data collection with specific details identified per stay. Mark RESEARCH as passed in `prd.json`.

---

### Phase 3: WRITE (WRITE-xxx)

Write the full editorial draft.

**Invoke `/elite-copywriter`** with:
- The content brief (topic, keyword, article type, competitive angle)
- The brand voice profile (reference `docs/uniquestays-brand-guidelines.md`)
- The stay data from Phase 2
- The article type template from `references/article-templates.md`

**Writing rules:**
- Open with the reader's experience, not the property's features
- Lead with feeling, follow with fact — every paragraph
- One idea per paragraph. Short sentences for impact. Long sentences for atmosphere.
- Use "you" for direct address, "we" for editorial observations
- Specific numbers over vague claims ("$285/night" not "affordable")
- Weave price and rating into prose naturally, not as separate callouts
- Include `[EMBED: stay-slug]` placeholders where each stay should appear
- Never write meta-commentary sections ("Why this matters", "The takeaway")
- No banned words (see `references/quality-checklist.md`)
- No exclamation marks

**File location:** `content/drafts/{slug}.md`

**Frontmatter format:**
```yaml
---
title: ""
subtitle: ""
slug: ""
excerpt: ""
city: ""
state: ""
latitude: ""
longitude: ""
metaTitle: ""
metaDescription: ""
publishedAt: ""
status: "draft"
heroImage: "[description or source URL]"
linkedStays:
  - stay-slug-1
  - stay-slug-2
---
```

**Output:** First draft saved. Mark WRITE as passed in `prd.json`.

---

### Phase 4: SEO (SEO-xxx)

Optimize for search and AI citation. Read `references/seo-requirements.md` for the full checklist.

**Keyword placement:**
1. Verify primary keyword in: title, metaTitle, first 100 words, at least one H2, metaDescription, excerpt
2. Weave 2-3 long-tail variations into body paragraphs naturally
3. Check keyword never feels forced

**AI citation blocks:**
1. Add 1-2 definition sentences early in the article (clear, self-contained, extractable)
2. Add an FAQ section with 3-5 questions matching common queries
3. Verify 2-3 sourced statistics with real attribution
4. Add structured comparison table if applicable

**Internal linking:**
1. Query Payload for related posts:
   ```bash
   GET /api/blog-posts?where[status][equals]=published&where[state][equals]={state}&depth=0&limit=10
   ```
2. Add 2+ contextual inline links to other journal posts
3. Link to relevant spoke pages where topic overlaps

**Meta verification:**
- `metaTitle` under 60 chars, includes keyword, reads like editorial
- `metaDescription` under 160 chars, includes keyword + specific detail
- `slug` is kebab-case, no dates in path

**Cannibalization check:**
1. List all published posts from Payload
2. Verify no existing post targets the same primary keyword
3. If overlap exists, differentiate the angle

**Output:** SEO-optimized draft. Mark SEO as passed in `prd.json`.

---

### Phase 5: REVIEW (REVIEW-xxx)

Quality gate. Score against the rubric in `references/quality-checklist.md`.

**Scoring:** Rate each of the 8 criteria (voice match, specificity, feeling-first, banned words, SEO, embeds, practical value, cut test) on a 1-10 scale with weighted average.

| Score | Action |
|---|---|
| 8.0+ | **AUTO-PROCEED** to Phase 6 |
| 7.0-7.9 | One more edit pass targeting failing criteria, then re-score |
| Below 7.0 | **STOP** — identify what's missing, may need partial rewrite |

**Quality scans:**
1. **Banned word scan** — zero tolerance. Search for: stunning, breathtaking, magical, life-changing, perfect, amazing, incredible, unforgettable, cozy, hidden gem, wanderlust, bucket list, must-see, nestled, escape the everyday, "whether you're", "perfect for"
2. **Exclamation mark scan** — zero tolerance in journal posts
3. **20% cut test** — identify the weakest 20% of paragraphs. Cut or rewrite them
4. **Feeling-first check** — verify no stay section opens with features instead of feeling
5. **Irish Storytelling Test** — verify at least one specific detail per stay that could only apply to that place
6. **Distinct voice check** — verify no two stay descriptions sound alike

**Save v2** to `content/drafts/{slug}-v2.md`.

**Output:** Quality score, specific improvements made. Mark REVIEW as passed in `prd.json`.

---

### Phase 6: PUBLISH (PUBLISH-xxx)

Publish directly to Payload CMS. No intermediate scripts needed.

**Step 1: Resolve stay IDs**
```bash
# For each stay slug in linkedStays
GET /api/stays?where[slug][equals]={stay-slug}&depth=0&limit=1
# Collect: docs[0].id
```

**Step 2: Upload hero image** (if external URL, not already in media collection)
```bash
# Fetch image, then upload to Payload media
# Use the two-step pattern from existing scripts
```

**Step 3: Check for existing post**
```bash
GET /api/blog-posts?where[slug][equals]={slug}&depth=0&limit=1
```
- If `totalDocs === 0` → `POST /api/blog-posts`
- If `totalDocs === 1` → `PATCH /api/blog-posts/{id}`

**Step 4: Construct Lexical JSON**

Use these helper functions to build the content:

```typescript
function text(content: string) {
  return { type: 'text', format: 0, style: '', mode: 'normal', text: content, detail: 0, version: 1 }
}

function para(content: string) {
  return {
    type: 'paragraph', format: '', indent: 0, version: 1, direction: 'ltr',
    textFormat: 0, textStyle: '',
    children: [text(content)],
  }
}

function h2(content: string) {
  return {
    type: 'heading', tag: 'h2', format: '', indent: 0, version: 1, direction: 'ltr',
    children: [text(content)],
  }
}

function embedBlock(stayId: number) {
  return {
    type: 'block', version: 2,
    fields: { id: crypto.randomUUID(), blockType: 'stayEmbed', stay: stayId },
  }
}

function hr() {
  return { type: 'horizontalrule', version: 1 }
}
```

**Step 5: Two-step update** (follows the pattern in `scripts/update-treehouse-article.ts`)

First call — update heroImage + linkedStays + editorial fields:
```bash
PATCH /api/blog-posts/{id}
{
  "title": "...",
  "subtitle": "...",
  "excerpt": "...",
  "heroImage": <media_id>,
  "linkedStays": [<stay_id_1>, <stay_id_2>, ...],
  "city": "...",
  "state": "...",
  "latitude": "...",
  "longitude": "...",
  "metaTitle": "...",
  "metaDescription": "...",
  "status": "published",
  "publishedAt": "<ISO datetime>"
}
```

Second call — update content with Lexical JSON:
```bash
PATCH /api/blog-posts/{id}
{
  "content": { "root": { ... } }
}
```

**Step 6: Verify**
```bash
# Check the API record
GET /api/blog-posts?where[slug][equals]={slug}&depth=1&limit=1

# Check the public page loads
GET https://uniquestaysusa.com/journal/{slug}
```

**Step 7: Save final version** to `content/published/{slug}.md`

**Authentication:** `Authorization: users API-Key {key}` — read from environment, never hardcode.

**ISR revalidation:** Automatic via Payload's `afterChange` hook in `src/collections/BlogPosts.ts`. No manual revalidation needed.

**Output:** Post live at `/journal/{slug}`. Mark PUBLISH as passed in `prd.json`.

---

### Phase 7: SYNC (SYNC-xxx)

Update tracking documents. Mandatory — never skip.

**Update `scripts/ralph/progress.txt`:**
Append a sprint summary:
```markdown
### Sprint {N}: {Article Title}

**PLAN-{N}** ✓ — {keyword}, {article type}, {N} stays selected

**RESEARCH-{N}** ✓ — Stay data collected, {N} specific details identified

**WRITE-{N}** ✓ — First draft: content/drafts/{slug}.md

**SEO-{N}** ✓ — Keyword optimized, {N} internal links, FAQ added

**REVIEW-{N}** ✓ — Quality score: {X}/10, {N} edits

**PUBLISH-{N}** ✓ — content/published/{slug}.md
- Published at: /journal/{slug}
- Target keyword: {keyword}
- Word count: {N}
- Quality score: {X}/10
```

**Record learned patterns** in the progress file (what worked, what to do differently next sprint).

**Verify sitemap inclusion:**
```bash
GET https://uniquestaysusa.com/sitemap.xml
# Check that /journal/{slug} appears
```

**Update `scripts/ralph/prd.json`:**
- All sprint stories set to `passes: true`
- Increment `sprintNumber`
- Clear `currentStory` for next sprint

**Git commit:**
```bash
git add content/published/{slug}.md scripts/ralph/prd.json scripts/ralph/progress.txt
git commit -m "journal: publish \"{title}\" (sprint {N})"
```

**Output:** All tracking docs updated and committed. Mark SYNC as passed. Loop continues to next sprint.

---

## Loop Control

### State persistence

The loop state lives in three files:

| File | Purpose |
|---|---|
| `scripts/ralph/prd.json` | Sprint stories, pass/fail status, sprint number |
| `scripts/ralph/progress.txt` | Running log of completed work and learned patterns |
| `.claude/ralph-loop.local.md` | Ralph stop hook state (active, iteration count, completion promise) |

### Start of each iteration

1. Read `.claude/ralph-loop.local.md` — is a Ralph loop active?
2. Read `scripts/ralph/prd.json` — what's the current sprint and story?
3. Read `scripts/ralph/progress.txt` — what patterns have been learned?
4. Find the highest-priority story where `passes: false`
5. Execute that story's phase
6. Update `prd.json` with `passes: true`
7. If all stories pass, start a new sprint (return to Phase 1)

### Stop conditions

- All calendar entries for the current month are completed
- Quality gate fails 3 times on the same article (escalate to user)
- User explicitly cancels (`/ralph-cancel` or removes `active: true` from loop state)
- User says "stop", "pause", or "that's enough for now"

### Ralph stop hook integration

The existing Ralph stop hook at `.claude/ralph-loop.local.md` controls loop persistence across context windows. The skill reads this file at the start of each iteration. When a context window closes, the stop hook re-feeds the journal-pipeline prompt to continue where it left off.

---

## Content Calendar Integration

### Reading the calendar

The calendar lives at `KEYWORD_RESEARCH_AND_CONTENT_CALENDAR.md`. Parse the monthly tables:

| Column | Use |
|---|---|
| Week | Scheduling |
| Content Type | Journal Post vs Lead Magnet vs Programmatic |
| Title/Topic | The article topic |
| Target Keywords | Primary + secondary keywords |
| Goal | The strategic purpose |

### Auto-select logic

1. Find the current month's section
2. Filter for "Journal Post" content type entries
3. For each entry, check if a published post exists in Payload with matching topic
4. Select the first entry with no published match
5. If the current month has no remaining entries, advance to the next month
6. If no entries remain, report "calendar complete" and suggest planning next quarter

### Article type inference

| Calendar signal | Article type |
|---|---|
| Topic mentions a city/state/region | Destination Dispatch |
| Topic mentions a stay category (treehouses, cabins, domes) | Curated Roundup |
| Topic mentions a season or month | Seasonal Guide |
| Topic mentions an activity (stargazing, fishing, hiking) | Activity-Based Guide |
| Topic mentions a specific property by name | Stay Spotlight |

---

## When NOT to Use This Skill

- Updating existing published posts (use `elite-copywriter` for polish passes)
- Creating listing pages (that's programmatic SEO, a separate system)
- Social media content (future extension)
- Newsletter content (future extension)
- Technical documentation or code changes
