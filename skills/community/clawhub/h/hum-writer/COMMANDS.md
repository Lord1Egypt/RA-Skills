# Hum Commands

Commands for a user's content writing workflow. These are handled by the main session.

## Data Directory

All data lives in `<data_dir>` (set via `HUM_DATA_DIR` env var, defaults to `~/Documents/hum`). In the command docs below, `<data_dir>` means this directory.

---

## /hum init

**What it does:**
Sets up the hum data directory with template files and required folders. Safe to run multiple times — skips anything that already exists.

```bash
python3 skills/hum/scripts/init.py
```

**Creates:**
- `VOICE.md` — tone, style rules, word preferences
- `CONTENT.md` — content pillars with keywords for feed classification
- `AUDIENCE.md` — target audience definition
- `CHANNELS.md` — publishing platforms (LinkedIn, X), frequency, and engage settings
- `knowledge/index.md` — knowledge source definitions (blogs, YouTube transcripts, podcasts)

**Folders:**
- `feed/`, `feed/raw/`, `feed/assets/`
- `content/`, `content-samples/`, `knowledge/`, `ideas/`, `learn/`

After running, edit each file to set up your profile. The content pillars in `CONTENT.md` drive feed classification and brainstorming.

---

## /hum loop

**What it does:**
Runs the full daily morning workflow. Read `LOOP.md` in the skill root and follow every step.

---

## /hum refresh-feed

**What it does:**
Fetches X home feed, X profiles, Hacker News, YouTube, and knowledge sources (RSS, sitemaps, YouTube transcripts, podcasts from `knowledge/index.md`) via direct APIs — ranks items, sends a formatted digest via Telegram, and saves aggregated data to `<data_dir>/feed/feeds.json`. No browser automation.

**This command is also triggered automatically by the "Morning Digest" cron job at 6:00am SGT daily.**

**Scrape sources:** See `<data_dir>/feed/sources.json` for social/ephemeral feed sources. See `<data_dir>/knowledge/index.md` for knowledge sources (blogs, newsletters, YouTube transcripts, podcasts). Manage social sources with `/hum sources`.

### Step 1 — Fetch all sources

Runs the full refresh pipeline in a single command:

```bash
python3 skills/hum/scripts/feed/refresh.py --type all
```

This fetches:
- **X home feed**: via Bird `filter:follows since:<last_crawled>` — returns tweets from accounts you follow without any browser.
- **X profiles**: per-handle `from:<handle> since:<last_crawled>` via Bird.
- **Hacker News**: via Algolia public API (merged into `feeds.json`).
- **Knowledge sources**: RSS, sitemaps, YouTube transcripts, and podcasts from `knowledge/index.md` — saves full articles to `knowledge/<source>/` and generates feed items into `feeds.json`.

Requires `AUTH_TOKEN` and `CT0` session cookies in `~/.hum/credentials/x.json` (or the `HUM_X_AUTH_TOKEN` / `HUM_X_CT0` env vars). Extract them once from your browser devtools on x.com. If credentials are missing, the X fetch is skipped with a log message and the rest of the pipeline still runs.

All items are merged into `feeds.json` with `source: "x" | "hn" | "knowledge"`, `topics: [...]`, and engagement counts:
```json
[{"source": "x", "author": "@handle", "text": "...", "likes": 123, "url": "https://x.com/...", "topics": ["AI"]}]
```

You can also crawl knowledge sources independently:
```bash
python3 skills/hum/scripts/feed/refresh.py --type knowledge
```

### Step 2 — Pull YouTube creator updates (optional, for sources.json YouTube only)

Only needed for YouTube channels defined in `sources.json` (short digest summaries via yt-dlp). YouTube channels in `knowledge/index.md` are crawled as full transcripts in Step 1.

```bash
python3 skills/hum/scripts/feed/source/youtube.py \
  --file <data_dir>/feed/sources.json \
  --days 7 \
  --output <data_dir>/feed/raw/youtube_feed.json
```

### Step 3 — Rank and aggregate

```bash
python3 skills/hum/scripts/feed/ranker.py \
  --input <data_dir>/feed/feeds.json \
  --output <data_dir>/feed/raw/feed_ranked.json
```

Merge all source outputs (X, YouTube, HN, knowledge) into `feed/feeds.json` — a single aggregated JSON file that other commands (like `/hum brainstorm`) read from.

### Step 4 — Format & send digest

```bash
python3 skills/hum/scripts/feed/digest.py \
  --input <data_dir>/feed/feeds.json \
  --youtube-input <data_dir>/feed/raw/youtube_feed.json \
  --max-posts 12
```

Send the output via Telegram. Use:
```
message(action="send", channel="telegram", target="<user>", message="<digest>")
```

Target: **up to 4 posts per category** (AI / Startups / Crypto). Skip any section with 0 matches.

### Step 5 — Archive

Append today's digest to `<data_dir>/feed/feeds.json` for historical reference. Insert new entries at the top, before previous entries.

**Telegram output format:**
```
🗞 Morning Feed — [date]

💰 AI Monetization
1. @handle: [text]
   [url]

🤖 AI
2. @handle: [text]
   [url]

🚀 Startups
3. @handle: [text]
   [url]

🪙 Crypto
4. @handle: [text]
   [url]

YouTube items are prefixed with ▶:
5. ▶ [Channel]: [video title] ([date])
   [summary]
   [url]

📌 General
6. @handle: [text]
   [url]
```

Posts are grouped by content pillar topic (up to 3 per topic). Items not matching any topic appear in the General section. HN stories and knowledge items are mixed into topic sections based on their classified topics.

---

## /hum crawl [source_key | --all | --list]

**What it does:**
Crawls knowledge sources (blogs, newsletters, YouTube transcripts, podcasts) defined in `<data_dir>/knowledge/index.md`. Saves full articles as markdown files in `<data_dir>/knowledge/<source_key>/`. Also generates feed items for newly crawled articles.

This is the same crawl that runs as part of `/hum refresh-feed`, but can be invoked independently for one-off crawls or testing.

```bash
# List all knowledge sources with file counts
python3 -m feed.source.knowledge --list

# Crawl a single source
python3 -m feed.source.knowledge <source_key>

# Crawl every source in index.md
python3 -m feed.source.knowledge --all

# Limit articles per source (useful for testing)
python3 -m feed.source.knowledge <source_key> --max 5

# Re-fetch everything, overwriting existing files
python3 -m feed.source.knowledge <source_key> --recrawl
```

Run from `skills/hum/scripts/` directory. Sources are defined as markdown tables in `knowledge/index.md` with columns: Key, Handler (rss/sitemap/youtube/podcast), Feed URL.

**Requirements:**
```bash
pip3 install trafilatura feedparser python-slugify requests lxml_html_clean youtube-transcript-api
```

---

## /hum sources

**What it does:**
Manage feed sources — list, add, or remove X accounts, YouTube creators, and websites.

```bash
# List all sources
python3 skills/hum/scripts/feed/sources.py list

# Add an X account
python3 skills/hum/scripts/feed/sources.py add x <handle> [category]

# Add a YouTube creator
python3 skills/hum/scripts/feed/sources.py add youtube <url> [name]

# Add a website
python3 skills/hum/scripts/feed/sources.py add website <name> <url>

# Remove a source
python3 skills/hum/scripts/feed/sources.py remove <handle_or_name>
```

Sources are stored in `<data_dir>/feed/sources.json`.

---

## /hum config

**What it does:**
Show current hum config.

Display current configuration:
```
Hum Config
  data_dir: ~/Documents/hum
  image_model: gemini
```

To change, set environment variables or edit `openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "hum": {
        "enabled": true,
        "config": {
          "hum_data_dir": "~/Documents/hum",
          "image_model": "gemini"
        }
      }
    }
  }
}
```

Or run `python3 skills/hum/scripts/config.py` to verify resolved paths.

---

## /hum brainstorm

**What it does:**
Researches trending content across multiple platforms for each of the user's content pillars, then generates and saves content ideas to `ideas/ideas.json`.

**Sources searched (per pillar):**
- YouTube — trending videos, popular creators, transcript insights
- X (Twitter) — posts, threads, engagement signals
- Reddit — threads, top comments, community sentiment
- Hacker News — stories, technical discussions, points/comments
- Polymarket — prediction markets, real-money signals on outcomes
- Web search — blogs, news, tutorials, industry publications

### Step 1 — Load context

1. Read `<data_dir>/CONTENT.md` to extract the content pillars
2. Read `<data_dir>/VOICE.md` and `<data_dir>/AUDIENCE.md` for voice and audience context
3. Read `<data_dir>/content-samples/` for voice reference
4. Read `<data_dir>/ideas/ideas.json` to know what ideas already exist (avoid duplicates)
5. Read `feed/feeds.json` for recent feed context (what's trending in the user's sources)
6. Read `<data_dir>/knowledge/` for any user-curated reference material

### Step 2 — Research each pillar

For each content pillar in CONTENT.md, research using WebSearch queries:
- `{pillar topic} trends 2026`
- `{pillar topic} discussion opinions`
- Exclude reddit.com, x.com, twitter.com (covered by script)

### Step 3 — Synthesize and generate ideas

For each pillar's research results:
1. Read the full output — it contains Reddit, X, YouTube, Hacker News, Polymarket, and web data
2. Identify the highest-signal findings: cross-platform mentions, high-engagement posts, strong opinions, surprising data
3. Cross-reference with existing ideas in `ideas.json` to find gaps
4. Generate 3–5 content ideas per pillar, each grounded in specific research findings

### Step 4 — Save ideas

Append each idea to `<data_dir>/ideas/ideas.json`. Each idea is an object:

```json
{
  "id": "I042",
  "title": "CFOs Replacing Headcount with AI Agents",
  "pillar": "AI in Finance",
  "status": "pending",
  "date": "2026-04-03",
  "post_type": "LinkedIn Post",
  "hook": "The opening line or tension — one sentence",
  "angle": "The specific POV or contrarian take — 1-2 sentences",
  "evidence": [
    "Source 1: specific data point with platform attribution — e.g. per @handle on X",
    "Source 2",
    "Source 3"
  ],
  "why_now": "Why this is timely — what triggered it in the research",
  "notes": "Optional: format suggestions, media ideas, related ideas"
}
```

**ID assignment:** Increment from the highest existing ID in `ideas.json` (e.g. I001, I002...).

### Step 5 — Present summary

Show the user a summary grouped by pillar:

```
📋 Brainstorm Results

Researched [N] pillars across YouTube, X, Reddit, HN, Polymarket, and web.

**[Pillar 1]**
  I042 · CFOs Replacing Headcount with AI Agents (LinkedIn Post)
  I043 · The Real Cost of Manual Reconciliation (X Thread)
  I044 · Why FP&A Teams Are Shrinking (LinkedIn Post)

**[Pillar 2]**
  I045 · ...

[N] new ideas saved to ideas.json
```

Ask: "Want to refine any of these, change post types, or discard some?"

### Rules

- Research takes 5–15 minutes depending on the number of pillars — tell the user upfront
- Always ground ideas in specific research findings, not generic knowledge
- Each idea must cite at least one real source from the research
- Avoid duplicating ideas already in `ideas.json`
- Prefer ideas where the same signal appears across multiple platforms (strongest evidence)

---

## /hum learn

**What it does:**
Weekly strategy audit. Analyzes your own post engagement, studies how successful niche influencers write (formats, hooks, angles — not topics), and researches platform algorithm mechanics. Synthesizes into strategy-level recommendations and proposes context file updates.

**Not a brainstorm.** Topic and idea generation is handled by `/hum brainstorm` (run daily), which already reads `knowledge/` and `feeds.json` for trending topics. Learn reads the same sources differently — for writing patterns, not topics — so there is no duplication.

**When to use it:**
- Weekly strategy refresh, especially on Saturdays
- After a meaningful batch of new posts has been published
- When content performance feels flat

---

### Phase 1 — Load context

Read: `<data_dir>/VOICE.md`, `<data_dir>/AUDIENCE.md`, `<data_dir>/CHANNELS.md`, `<data_dir>/CONTENT.md`

---

### Phase 2 — Own engagement analysis

Scrape post performance via browser for each platform in `CHANNELS.md`:

```bash
python3 -m act.analyze --platform all --account <account>
```

This returns browser instructions — follow them to scrape your X and LinkedIn profiles.

**Engagement table**
Build a table per platform: post type (tweet / thread / LinkedIn post / article) → total posts scraped → avg. reactions → avg. reposts → avg. comments. Rank by avg. engagement.

**Underperformers**
Flag posts with below-average engagement. Note likely cause: weak hook, format mismatch, or pure product promo.

If no posts are found or data is thin, note it clearly — do not fabricate.

---

### Phase 3 — Influencer format and pattern analysis

**Goal:** Understand *how* successful niche influencers write — not what topics they cover (brainstorm handles that). Extract writing patterns, formats, and hooks from the already-crawled knowledge base.

**Phase 3a — Knowledge: influencer format analysis**

Read the most recent files (last 60 days, filter by `date` frontmatter) from `<data_dir>/knowledge/` subdirectories. Use `knowledge/index.md` to identify which sources are relevant to the user's content pillars (Finance, Fintech, AI, AI Monetization — cross-reference with `CONTENT.md` keywords).

For each relevant source with recent content, extract:
- **Format**: How is the piece structured? (essay, numbered list, how-to, data breakdown, contrarian argument, case study, Q&A)
- **Hook style**: How does it open? (question, stat/number, bold claim, personal story, observation)
- **Angle**: What POV does it take? (neutral, contrarian, practical, historical, predictive)
- **Length/density**: Long-form with depth, or short and punchy?
- **CTA pattern**: Does it end with a question, link, poll, or nothing?

Group by source. Produce a compact profile per source:
```
[Source name] — [author] — [niche]
Recent format: [list / essay / data breakdown / ...]
Hook style: [question / stat / bold claim / ...]
Angle: [contrarian / practical / predictive / ...]
CTA: [question / link / none]
```

Then identify across sources:
- **Formats that appear in 2+ niche sources** — these are the formats working in the niche
- **Formats not represented in your `content-samples/`** — these are format gaps

Do NOT extract topics — that's brainstorm's job.

**Phase 3b — Feed: engagement signals (pillar-scoped)**

Read `<data_dir>/feed/feeds.json`. Extract the top 10 items where `topics` matches your content pillars. Note:
- Which X accounts from `sources.json` are generating the highest-engagement posts
- Any cross-platform convergence: same topic appearing in both X feed and knowledge/ (signals elevated relevance)

Do NOT cluster topics or generate ideas — that belongs in brainstorm.

---

### Phase 4 — Platform algorithm mechanics

Run one web search per active platform in `CHANNELS.md`:
- Search: `"[platform] algorithm" [current year] reach distribution`
- Focus on actionable signals: timing, engagement velocity, format weighting, link penalties, reply behavior
- Note any algorithm changes in the last 30–60 days

---

### Phase 5 — Synthesis

Connect the data from Phases 2–4. Produce:

**Format gap map**
Formats that niche influencers use consistently (Phase 3a) that are absent from your `content-samples/`. Name the influencer and format: "OnlyCFO uses numbered data breakdowns with a bold claim opener — not in your samples." These are the format experiments worth running.

**Strength map**
Your highest-performing post type and engagement pattern from Phase 2. Identify 1–2 formats to double down on.

**Opportunity matrix**
Where format gap + your pillar + algorithm signal align. Example: "Contrarian essay format (Phase 3a: used by 3 niche sources) + AI Monetization pillar + LinkedIn algorithm rewards long comments = highest priority experiment." List 2–3 combinations.

**Next 2 weeks**
2–3 format experiments to try — not topic ideas. Brainstorm generates topics; Learn generates format direction. Example: "Try one contrarian thesis post on LinkedIn. Try one data-breakdown post with a question CTA."

---

### Phase 6 — Output and context updates

**Save learning report**

Save a dated report to `<data_dir>/learn/YYYY-MM-DD.md` with these sections:
```
# Learn Report — [date]

## Engagement Summary
[Per-platform tables from Phase 2]

## Influencer Format Patterns
[Source profiles from Phase 3a — format, hook style, angle, CTA per source]

## Feed Signals
[Top pillar-scoped items and cross-platform convergence from Phase 3b]

## Platform Algorithm Mechanics
[Algorithm signals from Phase 4]

## Synthesis
[Format gap map, strength map, opportunity matrix from Phase 5]

## Recommendations
[Next 2 weeks: 2–3 format experiments]
```

**Propose context file edits**

List proposed changes to `VOICE.md`, `CHANNELS.md`, and `CONTENT.md` with the evidence that supports each. Do not edit the files yet. Show:

```
Proposed changes:

CHANNELS.md — [what to change] — because [evidence]
CONTENT.md — [what to change] — because [evidence]
VOICE.md — [what to change] — because [evidence]
```

Ask: "Should I apply these changes?"

Apply only on confirmation. Only make changes backed by evidence — do not speculate.

**Present summary**

After saving the report, show a brief summary (not a repeat of the full report):
- Your top-performing format and what makes it work
- 2–3 format patterns from niche influencers worth experimenting with
- 1–2 platform algorithm signals to act on
- The 2–3 format experiments to try in the next 2 weeks

---

**Rules:**
- Phase 3 reads existing knowledge/ and feeds.json — no new scraping or web searches in this phase
- Phase 4 uses web search for algorithm mechanics only — not content trends (brainstorm handles that)
- Be specific: name the influencer source when citing a format pattern
- Never edit context files without user approval
- If knowledge/ has no recent files for a niche, note it clearly and reduce confidence on format claims for that niche

---

## /hum ideas

**What it does:**
Displays the full idea list from `<data_dir>/ideas/ideas.json`.

**Output format:**
```
📋 Ideas

✅ Approved (ready to draft)
I001 · The K-shaped VC market
I002 · AI agents as headcount
...

📝 Drafted (awaiting publish)
I006 · [idea]

🟡 Pending (not yet approved)
(none)

✔️ Published
(none)
```

Always show count per status. End with: "Use `/hum create [platform] [post type] [idea ID]` to draft — e.g. `/hum create LinkedIn Post I001`"

---

## /hum content

**What it does:**
Lists drafts and assets across the content pipeline.

**Steps:**
1. Read files in `<data_dir>/content/drafts/` (unPublished drafts)
2. Read files in `<data_dir>/content/published/` (sent posts)
3. Read files in `<data_dir>/content/images/` (generated images)
4. Show them grouped by status and platform
5. Include draft status metadata if present in the file header
6. If no drafts exist, say so plainly

**Output format:**
```
🗂 Drafts

LinkedIn
- LinkedIn - The Finance Team of 2028.md · outline — 2026-03-24

X
- X - AI Agents as Headcount.md · ready — 2026-03-25

✅ Published
- X - OpEx Structure with AI.md — published 2026-04-07

🖼 Images
- ai-math-trap-2026-04-08.png
```

End with: "Use `/hum publish [draft file]` to publish or `/hum create [platform] [post type] [idea ID]` to draft something new."

---

## /hum create [platform] [post type] [idea ID or keyword]

**What it does:**
Researches an idea, proposes an outline for approval, then drafts content in the user's voice.

**Full command spec:** [`scripts/create/CREATE.md`](scripts/create/CREATE.md)

**Flow:** Load context → Deep research (3-5 web searches) → Propose outline → User approval → Write draft → Save & track

### Image generation

When drafting, set the `image_prompt` field on the post. The `validate()` call automatically generates the image using the configured provider (default: Gemini).

To include an image with a draft:
- Add `image_prompt: "your image description"` when creating the post
- `validate(post)` ��� generates image → sets `media_path`
- `format_preview(post)` → shows `(run validate() to generate the image)` until generated
- If `VOICE.md` has a `## Visual Style` section, it is appended to the prompt automatically

Providers:
1. `gemini` — gemini-2.5-flash-image (default)
2. `openai` — gpt-image-1
3. `grok` — grok-2-image (xAI API)
4. `minimax` — image-01

Set the active provider in `openclaw.json` → `skills.entries.hum.config.image_model` or via the `HUM_IMAGE_MODEL` env var.

---

## /hum publish [draft file or idea ID]

**What it does:**
Publishes an approved draft to X or LinkedIn via platform connectors (API-based).

**⚠️ Always confirm with the user before posting. Show the final text and ask "Ready to publish?" before running any publish script.**

### Shared steps

**Steps:**
1. Read the draft from `<data_dir>/content/drafts/`
2. Read connector docstrings in `skills/hum/scripts/act/connectors/` for credential shape and connector details
3. Show the exact final text and ask: "Ready to publish to [platform]?"
4. Run a preview first:
   `python3 skills/hum/scripts/act/publish.py --draft "[draft path]"`
5. On confirmation, publish using:
   `python3 skills/hum/scripts/act/publish.py --draft "[draft path]" --account "[account]" --publish --update-draft`
6. If a LinkedIn image or X first-post image exists, include:
   `--image "/absolute/path/to/image.png"`
7. Confirm success from the returned URL / ID
8. Update `ideas.json`: status → `published`, add date and URL

### Account selection
- Use the account mappings defined by the current user's `CHANNELS.md`.
- If the target API account is missing credentials, stop and tell the user which account file entry is missing

### Rules
- Never publish without explicit "yes" / "publish" / "post it" confirmation
- Always show the exact text that will be posted before running the script
- If posting fails (missing token, scope issue, rate limit, validation error, etc.) — report the error, do not retry silently
- After publishing, save the post URL to the draft file

### Platform constraints

- **X:** Supports single posts and numbered threads through the script. First-post image attachment is supported via `--image`.
- **LinkedIn:** Supports feed posts and single-image feed posts through API.
- **Other channels:** If `CHANNELS.md` lists additional platforms, follow those channel-specific workflows instead of `publish.py`.
- **LinkedIn native long-form articles:** do not assume they are API-publishable. If the draft is a real long-form article, follow the LinkedIn Article workflow below.

---

### LinkedIn Article Publish Workflow

When publishing a LinkedIn article (long-form, `_Format: LinkedIn Article_` in the draft), follow these steps in order:

#### Step 1 — Generate cover image

Use an image generation API (Gemini or MiniMax) to create a cover image for the article.

- **API key:** uses the configured image provider (see `/hum config`)
- **Prompt:** generate a LinkedIn article cover image for the article title, matching the user's style preferences
- **Save to:** `<data_dir>/content/images/LinkedIn Cover - [article title].png`
- Show the image to the user and ask for approval before proceeding

#### Step 2 — Draft the intro feed post

Write a short LinkedIn feed post (100–150 words) to introduce the article:
- Opens with the article's core tension or hook (not "I wrote an article")
- 2–3 sentences of substance — what the reader will get
- Ends with: "Full article 👇" or "Link in comments." (choose based on `CHANNELS.md` rules)
- Save to: `<data_dir>/content/drafts/LinkedIn Post - [article title].md`
- Show to user for approval before publishing

#### Step 3 — Publish the article (browser)

LinkedIn articles must be published via the LinkedIn article editor — not API.

1. Open `https://www.linkedin.com/article/new/` via the browser tool
2. Paste the article content from the draft file
3. Upload the cover image from Step 1
4. Set the article title
5. Click Publish
6. Capture the published article URL

#### Step 4 — Publish the intro feed post

Once the article URL is known:
1. Append the URL to the intro feed post draft
2. Publish via:
```bash
cd skills/hum/scripts && python3 -m act.connectors.linkedin \
  --account <account> \
  --text "<intro post text>\n\n<article URL>"
```

#### Step 5 — Update tracking

- Update `ideas.json`: status → `published`, add date and article URL
- Update the draft file with publish metadata

---

## /hum engage [linkedin | x | all]

**What it does:**
Three things in one command:
1. **Follow** 5–10 relevant accounts on X (finance, CFO, AI, fintech)
2. **Suggest replies** to posts from accounts the user's active X account follows — insightful engagement to build visibility
3. **Draft responses** to replies/comments on the user's own posts

Default: `all` (both platforms). Specify `x` or `linkedin` to scope.

**Before running:** Read `<data_dir>/CHANNELS.md` → "Engage Command Settings" to get the per-platform config (follows, engagement plays, response count).

**⚠️ Never post anything without the user's explicit approval.**

---

### Part 1 — Follow relevant accounts (X only)

1. Open https://x.com in the OpenClaw browser using the user's active X account
2. Search for 5–10 accounts in categories that match the user's niche and audience, using `<data_dir>/AUDIENCE.md` and `<data_dir>/CHANNELS.md` as the source of truth. Derive the relevant topics, industries, and account types from those files — do not assume a specific niche.
3. For each: navigate to their profile, click Follow if not already following
4. Skip accounts already followed (check before clicking)
5. Report: "Followed X new accounts: [list]"

**Prioritise accounts that:**
- Have 10K+ followers in finance/CFO/AI space
- Post regularly (active in last 7 days)
- Are not already followed

---

### Part 2 — Suggest outbound replies (engagement plays)

**Goal:** Reply to recent posts from niche accounts in a way that feels authentic, adds real value, and builds visibility in the right circles.

**Step 1 — Identify target accounts**

Pull target accounts from two sources:
1. `<data_dir>/feed/sources.json` — entries with `type: x_profile`
2. `<data_dir>/knowledge/index.md` — the "Influencers & Thought Leaders" tables (Name + Platform columns)

Combine into a single candidate list. Prioritise accounts that appear in both sources — these are most relevant to the user's niche.

**Step 2 — Find recent posts worth replying to**

For each candidate account (work through 8–12 to find 3–5 good matches):
1. Navigate to their profile in the browser
2. Find their most recent post from the **last 48 hours** — skip if nothing recent
3. Read the full post text carefully

A post is worth replying to if it:
- Makes a specific claim, shares data, or argues a position
- Is in the user's niche (check against `<data_dir>/CONTENT.md` content pillars)
- Has some engagement already — signals the conversation is active
- Is not a repost or share of someone else's content

**Step 3 — Draft replies**

Before drafting, read `<data_dir>/VOICE.md` for tone and style.

For each selected post, draft a reply that:
- **Anchors to something specific** in the post — a stat, a claim, a specific phrase. Never summarise generically.
- **Does one of:** adds a related data point, offers a contrarian take with a concrete reason, or extends the argument with a specific example
- **Feels like a person wrote it** — no filler openers ("Great point!", "Love this", "So true", "This is spot on"). Start with the substance.
- **Is concise** — 1–2 sentences for X (under 280 chars), 2–3 sentences for LinkedIn
- **Matches the user's voice** per VOICE.md — calm, direct, grounded in specifics

**Step 4 — Present for approval**

```
💬 Engagement Plays — suggested replies

1. @[account] on [platform] — "[exact quote or key claim from their post]"
   → [drafted reply]

2. @[account] on [platform] — "[exact quote or key claim from their post]"
   → [drafted reply]
```

Ask: "Which should I post? Any edits?"

---

### Part 3 — Gather posts and inbound comments

**LinkedIn:**
1. Open the user's recent LinkedIn activity page in the OpenClaw browser
2. If not logged in, stop and ask the user to log in first
3. Scan the 5 most recent posts
4. For each post, click into it and read the comments section
5. Collect comments that haven't been replied to by the user yet
6. Skip: generic congratulations ("Great post!"), spam, and comments with no substance worth engaging

**X (Twitter):**
1. Open the user's relevant X account
2. Check the 5 most recent tweets/threads from the relevant configured account
3. For each, click into it and read the replies
4. Collect replies that haven't been responded to yet
5. Skip: bots, spam, generic "nice" replies, and trolls not worth engaging

### Part 4 — Draft inbound responses

1. Read `<data_dir>/VOICE.md` for tone and style
2. For each comment worth responding to, draft a reply that:
   - Matches the user's voice — calm, direct, no fluff if that is what `VOICE.md` specifies
   - Adds value — extends the point, shares a specific insight, asks a follow-up
   - Is concise — 1–3 sentences max for LinkedIn, under 280 chars for X
   - Feels human — not templated, not sycophantic
   - Engages thoughtfully with the commenter's specific point
3. Present all drafts in a numbered table:

```
💬 Responses Ready

LinkedIn — [Post title / first line]
  1. @[commenter]: "[their comment summary]"
     → [your drafted response]

  2. @[commenter]: "[their comment summary]"
     → [your drafted response]

X — [Tweet text summary]
  3. @[replier]: "[their reply summary]"
     → [your drafted response]

  (no replies needing response)
```

4. Ask: "Which responses should I post? (numbers, 'all', or 'none')"

### Part 5 — Post approved responses

**On approval (numbers or "all"):**

**LinkedIn:**
1. Navigate to the specific post
2. Find the comment being replied to
3. Click "Reply" under that comment
4. Type the approved response text
5. Click the reply/submit button
6. Screenshot to confirm

**X:**
1. Navigate to the specific tweet/reply
2. Click "Reply"
3. Type the approved response text
4. Click "Reply" to post
5. Screenshot to confirm

**After posting all approved responses:**
- Report: "Posted X/Y responses. [list which ones]"
- If any failed (not logged in, rate limit, element not found), report the error per response

### Response style guidelines

- **Don't be a bot.** Vary sentence structure. Don't start every reply the same way.
- **Add, don't echo.** Never just agree — extend the thought with a new angle or specific example.
- **Match energy.** Short casual comment → short casual reply. Thoughtful paragraph → thoughtful reply.
- **Use names** when they're visible — "Good point, [Name]" feels more human than "Good point."
- **Disagree respectfully** when it's warranted — the user may have opinions and shouldn't dodge them.
- **Skip the gratitude performance.** Don't say "Thanks for sharing!" or "Great question!" — just answer.

---

## /hum samples

**What it does:**
Collects real writing samples from the user's social media profiles into `<data_dir>/content-samples/` using the browser.

**Steps:**
1. Read `<data_dir>/CHANNELS.md` to find the user's social media profile URLs
2. Open each profile URL in the browser
3. Scroll through recent posts — aim for 10–20 representative samples across platforms
4. For each post, extract:
   - Full text content (preserve exactly, do not edit)
   - Platform (X, LinkedIn, etc.)
   - Post type (tweet, thread, post, article)
   - Date posted (if visible)
   - Engagement metrics (likes, reposts, comments — if visible)
5. Save each sample as a separate file in `<data_dir>/content-samples/`:
   - Filename: `<platform> - <short-title-or-date>.md`
   - Format:
     ```
     ---
     platform: LinkedIn
     type: post
     date: 2026-03-15
     likes: 142
     comments: 23
     reposts: 8
     ---

     [exact post text]
     ```
6. Summarize: samples collected per platform, date range, top performers by engagement

**When to run:**
- First setup of a new profile
- User asks to refresh (`/hum samples`)
- Before drafting if `<data_dir>/content-samples/` is empty — prompt the user

**Rules:**
- Only collect public posts from the user's own accounts
- Preserve original text exactly
- Include engagement numbers to identify what resonates
- Overwrite stale samples on refresh — keep the folder current

---

## /hum feedback

**What it does:**
Log upvote/downvote on digest items and update feed preferences.

```bash
python3 skills/hum/scripts/feed/feedback.py log --item 3 --vote up
python3 skills/hum/scripts/feed/feedback.py log --item 1 --vote down
python3 skills/hum/scripts/feed/feedback.py show     # show current preferences
python3 skills/hum/scripts/feed/feedback.py history   # show recent votes
```

Preferences are stored in `feed/assets/preferences.json` and used by the ranker to score future feed items.

---

## Notes for the agent

- Always read VOICE.md, `<data_dir>/content-samples/`, and `<data_dir>/knowledge/` before drafting — do not rely on memory
- `ideas.json` is the source of truth for all idea state
- Never auto-post to any platform — drafts are always reviewed first
- When brainstorming, avoid ideas already in `ideas.json`
- IDs are permanent — never reuse a retired ID
- Drafts are named `[channel] - [title].md` in the `content/` folder
