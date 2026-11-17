# One-Shot Research Mode (v3)

Research ANY topic across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web. Surface what people are actually discussing, recommending, betting on, and debating right now.

---

## 1. Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about
2. **TARGET TOOL** (if specified): Where they'll use the prompts
3. **QUERY TYPE**:
   - **PROMPTING** - "X prompts", "prompting for X" -> copy-paste prompts
   - **RECOMMENDATIONS** - "best X", "top X" -> list of specific things
   - **NEWS** - "what's happening with X" -> current events
   - **COMPARISON** - "X vs Y", "X versus Y", "compare X and Y" -> side-by-side comparison
   - **GENERAL** - anything else -> broad understanding

Common patterns:
- `[topic] for [tool]` -> TOOL IS SPECIFIED
- `[topic] prompts for [tool]` -> TOOL IS SPECIFIED
- Just `[topic]` -> TOOL NOT SPECIFIED, that's OK
- "best [topic]" or "top [topic]" -> QUERY_TYPE = RECOMMENDATIONS
- "X vs Y" or "X versus Y" -> QUERY_TYPE = COMPARISON, TOPIC_A = X, TOPIC_B = Y

**Do NOT ask about target tool before research.** Run research first, ask after.

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown" if not specified]`
- `QUERY_TYPE = [PROMPTING | RECOMMENDATIONS | NEWS | COMPARISON | GENERAL]`
- `TOPIC_A = [first item]` (only if COMPARISON)
- `TOPIC_B = [second item]` (only if COMPARISON)

---

## 2. Confirm Topic

Display a branded one-liner before starting research. Build ACTIVE_SOURCES_LIST by checking what's configured in .env (Reddit, HN, Polymarket are always active; add X, YouTube, TikTok, Instagram, GitHub, Perplexity based on configured keys/tools).

For GENERAL / NEWS / RECOMMENDATIONS / PROMPTING queries:
```
/last30days - searching {ACTIVE_SOURCES_LIST} for what people are saying about {TOPIC}.
```

For COMPARISON queries:
```
/last30days - comparing {TOPIC_A} vs {TOPIC_B} across {ACTIVE_SOURCES_LIST}.
```

Do NOT show a multi-line "Parsed intent" block with TOPIC=, TARGET_TOOL=, QUERY_TYPE= variables. Do NOT promise a specific time. Do NOT list sources that aren't configured.

Then proceed immediately to research execution.

---

## 3. Handle / GitHub Resolution

**OpenClaw does not have WebSearch.** Skip manual handle resolution (Steps 0.5, 0.55, 0.75 from the main skill). Instead, add `--auto-resolve` to the research command. The engine will use configured web search backends (Brave, Exa, Serper) to discover subreddits, X handles, and context before planning.

If the user manually provides handles or community names, pass them through as CLI flags (see the flags list in Research Execution below). But do NOT attempt WebSearch-based resolution yourself.

---

## 4. Agent Mode (--agent flag)

If `--agent` appears in ARGUMENTS (e.g., `/last30days plaud granola --agent`):

1. **Skip** the intro display block
2. **Skip** any `AskUserQuestion` calls - use `TARGET_TOOL = "unknown"` if not specified
3. **Run** the research script exactly as normal
4. **Skip** the follow-up invitation
5. **Output** the complete research report and stop - do not wait for further input

Agent mode saves raw research data to `~/Documents/Last30Days/` automatically via `--save-dir`.

Agent mode report format:

```
## Research Report: {TOPIC}
Generated: {date} | Sources: Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket, Web

### Key Findings
[3-5 bullet points, highest-signal insights with citations]

### What I learned
{The full "What I learned" synthesis from normal output}

### Stats
{The standard stats block}
```

---

## 5. Comparison Mode (QUERY_TYPE = COMPARISON)

When the user asks "X vs Y", run ONE research pass with a comparison-optimized query that covers both entities AND their rivalry.

**Single pass with entity-aware subqueries:**
```bash
python3 "${SKILL_ROOT}/scripts/last30days.py" "{TOPIC_A} vs {TOPIC_B}" --auto-resolve --emit=compact --save-dir=~/Documents/Last30Days --save-suffix=v3 --store 2>&1
```

If the user provided manual handles or subreddits, include those flags too.

Then skip the normal Research Execution below - go directly to the comparison synthesis format (see Synthesis section).

**Comparison output format:**

```
# {TOPIC_A} vs {TOPIC_B}: What the Community Says (Last 30 Days)

## Quick Verdict
[1-2 sentence data-driven summary: which one the community prefers and why, with source counts]

## {TOPIC_A}
Community Sentiment: [Positive/Mixed/Negative] ({N} mentions across {sources})

Strengths (what people love)
- [Point 1 with source attribution]
- [Point 2]

Weaknesses (common complaints)
- [Point 1 with source attribution]
- [Point 2]

## {TOPIC_B}
Community Sentiment: [Positive/Mixed/Negative] ({N} mentions across {sources})

Strengths (what people love)
- [Point 1 with source attribution]
- [Point 2]

Weaknesses (common complaints)
- [Point 1 with source attribution]
- [Point 2]

## Head-to-Head
[Synthesis from the combined search - what people say when directly comparing]

| Dimension | {TOPIC_A} | {TOPIC_B} |
|-----------|-----------|-----------|
| [Key dimension 1] | [A's position] | [B's position] |
| [Key dimension 2] | [A's position] | [B's position] |
| [Key dimension 3] | [A's position] | [B's position] |

## The Bottom Line
Choose {TOPIC_A} if... Choose {TOPIC_B} if... (based on actual community data, not assumptions)
```

Then show combined stats and the standard invitation section.

---

## 6. Research Execution

**Run the research script in the FOREGROUND with a 5-minute timeout.**

```bash
python3 "${SKILL_ROOT}/scripts/last30days.py" $ARGUMENTS --auto-resolve --emit=compact --save-dir=~/Documents/Last30Days --save-suffix=v3 --store 2>&1
```

Use a **timeout of 300000** (5 minutes). The `--store` flag persists findings for watchlist/briefing integration.

**Always include `--auto-resolve`** since OpenClaw has no WebSearch. The engine will use configured web search backends (Brave, Exa, Serper) to discover subreddits, X handles, and current events context before planning.

**Available flags** (pass through if the user provides them manually):
- `--x-handle={handle}` - primary X/Twitter handle (without @)
- `--x-related={handle1},{handle2}` - related X handles (comma-separated, without @)
- `--subreddits={sub1},{sub2}` - target subreddits (comma-separated, no r/ prefix)
- `--tiktok-hashtags={tag1},{tag2}` - TikTok hashtags to search
- `--tiktok-creators={creator1},{creator2}` - TikTok creator handles
- `--ig-creators={creator1},{creator2}` - Instagram creator handles
- `--github-user={username}` - GitHub username for person-mode search
- `--github-repo={owner/repo}` - GitHub repo for project-mode search (comma-separated for multiple)
- `--deep-research` - Perplexity Deep Research mode (exhaustive 50+ citation reports, ~$0.90/query, requires OPENROUTER_API_KEY + `INCLUDE_SOURCES=perplexity`)
- `--days=N` - look back N days instead of 30
- `--quick` - faster, fewer sources (8-12 each)
- `--deep` - comprehensive (50-70 Reddit, 40-60 X)

**Read the ENTIRE output.** It contains data sections for: Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and Web. If you miss sections, you will produce incomplete stats.

---

## 7. WebSearch Supplemental

**If your platform supports WebSearch**, use it after the script finishes to supplement with blogs, tutorials, and news.

Choose search queries based on QUERY_TYPE:

- **RECOMMENDATIONS**: `best {TOPIC} recommendations`, `{TOPIC} list examples`
- **NEWS**: `{TOPIC} news 2026`, `{TOPIC} announcement update`
- **PROMPTING**: `{TOPIC} prompts examples 2026`, `{TOPIC} techniques tips`
- **GENERAL**: `{TOPIC} 2026`, `{TOPIC} discussion`

Rules:
- **USE THE USER'S EXACT TERMINOLOGY**
- EXCLUDE reddit.com, x.com, twitter.com (covered by script)
- Do NOT output a separate "Sources:" block

**If your platform does NOT support WebSearch**, the `--auto-resolve` flag already provides web context via the engine's configured backends. Skip this step.

---

## 8. Synthesis / Judge Agent

### v3 Cluster-First Output

v3 returns results grouped by STORY/THEME (clusters), not by source. Each cluster represents one narrative thread found across multiple platforms.

**How to read v3 output:**
- `### 1. Cluster Title (score N, M items, sources: X, Reddit, TikTok)` - a story found across multiple platforms
- `Uncertainty: single-source` - only one platform found this story (lower confidence)
- `Uncertainty: thin-evidence` - all items scored below 55 (unconfirmed)
- Items within a cluster show: source label, title, date, score, URL, and evidence snippet

**Synthesis strategy for cluster-first output:**
1. **Synthesize per-cluster first.** Each cluster = one story. Summarize what each story is about.
2. **Multi-source clusters are highest confidence.** A cluster with items from Reddit + X + YouTube is much stronger than single-source.
3. **Check uncertainty tags.** "single-source" means treat with caution. "thin-evidence" means mention but caveat.
4. **Cross-cluster synthesis second.** After covering individual stories, identify themes that span clusters.
5. **Engagement signals still matter.** Items with high likes/upvotes/views within a cluster are the strongest evidence points.
6. **Quote directly from evidence snippets.** The snippets are pre-extracted best passages - use them.
7. Extract the top 3-5 actionable insights across all clusters.
8. **Disambiguation: trust your resolved entity.** When auto-resolve identified a specific entity, prioritize content about THAT entity. If results contain a different entity with the same name, lead with the one auto-resolve identified.

### Source-Specific Guidance (applies within clusters)

The Judge Agent must:
1. Weight Reddit/X sources HIGHER (they have engagement signals: upvotes, likes)
2. Weight YouTube sources HIGH (they have views, likes, and transcript content)
3. Weight TikTok sources HIGH (they have views, likes, and caption content - viral signal)
4. Weight Instagram sources HIGH (influencer/creator perspective)
5. Weight WebSearch sources LOWER (no engagement data)
6. **For Reddit: Pay special attention to top comments** - they often contain the wittiest, most insightful, or funniest take. Quote them directly.
7. **For X: Reply clusters are gold.** When you see a cluster of replies to a recommendation-request tweet (someone asking "what's the best X?" and getting multiple independent responses), call this out prominently. This is the strongest form of community endorsement.
8. **For YouTube: Quote transcript highlights directly.** Attribute to the channel name.
9. **For TikTok: Note view counts and caption content.** Viral TikToks are strong cultural signal.
10. **For Instagram: Weight alongside TikTok.** Instagram provides unique creator/influencer perspective.
11. **For HN: Developer community signal.** Cite as "per HN" or "per hn/username."
12. **For GitHub person-mode data:** When the output includes "GitHub Person Profile" items, these contain PR velocity, top repos with star counts, release notes, README summaries, and top issues. Lead with the velocity headline ("X PRs merged across Y repos"), then highlight the most impressive repos by star count. Weave release notes into the narrative to show what actually shipped.
13. Identify patterns that appear across ALL sources (strongest signals)
14. Note any contradictions between sources
15. **Multi-source clusters (items from 3+ platforms) are the strongest signals.** Lead with these.

### Prediction Markets (Polymarket)

When Polymarket returns relevant markets, prediction market odds are among the highest-signal data points. Real money on outcomes cuts through opinion.

**6-point synthesis strategy:**

1. **Prefer structural/long-term markets over near-term deadlines.** Championship odds > regular season. Regime change > near-term strike deadline. IPO/major milestone > incremental update. When multiple markets exist, the bigger question is more interesting.

2. **When the topic is an outcome in a multi-outcome market, call out that specific outcome's odds and movement.** Don't just say "Polymarket has a market" - say "Arizona has a 28% chance, up 10% this month."

3. **Weave odds into the narrative as supporting evidence.** Don't isolate Polymarket data in its own paragraph. Instead: "Final Four buzz is building - Polymarket gives Arizona a 12% chance to win the championship (up 3% this week)."

4. **Citation format: show ONLY % odds. NEVER mention dollar volumes, liquidity, or betting amounts.** The % odds are the magic - the dollar figures are internal metrics that add zero value.

5. **When multiple relevant markets exist, highlight 3-5 of the most interesting ones** in your synthesis, ordered by importance (structural > near-term).

6. **Polymarket odds with real money behind them are STRONGER signals than opinions.** Always include specific percentages when markets are confirmed relevant.

### X Reply Cluster Weighting

When you see a cluster of replies to a recommendation-request tweet (someone asking "what's the best X?" and getting multiple independent responses), call this out prominently. This is the strongest form of community endorsement - real people independently making the same recommendation without coordination. Example: "In a thread where @ecom_cork asked for Loom alternatives, every reply said Tella."

### Fun Content

**If the research output includes a "## Best Takes" section or items tagged with `fun:` scores, weave at least 2-3 of the funniest/cleverest quotes into your synthesis.** Reddit comments and X posts with high fun scores are the voice of the people. A 1,338-upvote comment that says "Where's the limewire link" tells you more about the cultural moment than a news article. Quote the actual text. Don't put fun content in a separate section - mix it into the narrative where it fits naturally.

### ELI5 Mode

**If ELI5_MODE is true for this run, apply these writing guidelines to your ENTIRE synthesis. If false, skip this block and write normally.**

- Assume I know nothing about this topic. Zero context.
- No jargon without a quick explanation in parentheses
- Short sentences. One idea per sentence.
- Start with the single most important thing that happened, in one line
- Use analogies when they help ("think of it like...")
- Keep the same structure: narrative, key patterns, stats, invitation
- Still quote real people and cite sources - don't lose the grounding
- Don't be condescending. Simple is not stupid. ELI5 means accessible, not childish.

### Citation Priority Hierarchy

Most to least preferred:

1. @handles from X - "per @handle" (these prove the tool's unique value)
2. r/subreddits from Reddit - "per r/subreddit" (prefer quoting top comments over thread titles)
3. YouTube channels - "per [channel name] on YouTube" (transcript-backed insights)
4. TikTok creators - "per @creator on TikTok" (viral/trending signal)
5. Instagram creators - "per @creator on Instagram" (influencer/creator signal)
6. HN discussions - "per HN" or "per hn/username" (developer community signal)
7. Polymarket - "Polymarket has X at Y% (up/down Z%)" with specific odds and movement
8. Web sources - ONLY when other sources don't cover that specific fact

The tool's value is surfacing what PEOPLE are saying, not what journalists wrote. When both a web article and an X post cover the same fact, cite the X post.

### URL Formatting

NEVER paste raw URLs anywhere in the output - not in synthesis, not in stats, not in sources.
- **BAD:** "per https://www.rollingstone.com/music/..."
- **GOOD:** "per Rolling Stone"
- **BAD stats line:** `Web: 10 pages - https://later.com/blog/...`
- **GOOD stats line:** `Web: 10 pages - Later, Buffer, CNN, SocialBee`

Use the publication/site name, not the URL.

### Disambiguation

When auto-resolve or the research identified a specific entity (handles, subreddits, location context), prioritize content about THAT entity. If search results contain a different entity with the same name, lead with the entity your resolution identified. Mention the other only briefly, or not at all if the user clearly meant the resolved one.

### Anti-Pattern Warning

**Ground your synthesis in the ACTUAL research content, not your pre-existing knowledge.**

Read the research output carefully. Pay attention to:
- **Exact product/tool names** mentioned - don't conflate similar-sounding products
- **Specific quotes and insights** from the sources - use THESE, not generic knowledge
- **What the sources actually say**, not what you assume the topic is about

**SELF-CHECK before displaying**: Re-read your "What I learned" section. Does it match what the research ACTUALLY says? If you catch yourself projecting your own knowledge instead of the research, rewrite it.

---

## 9. Display Results

### "What I learned" (format depends on QUERY_TYPE)

**If RECOMMENDATIONS** - show specific items with sources:
```
Most mentioned:

[Name] - {n}x mentions
Use Case: [what it does]
Sources: @handle1, r/sub, blog.com
```

**If PROMPTING/NEWS/GENERAL** - show synthesis:

Cite sparingly: 1-2 sources per topic in the intro, 1 source per pattern. Do NOT chain multiple citations.

```
What I learned:

{Topic 1} - [1-2 sentences about what people are saying, per @handle or r/sub]

{Topic 2} - [1-2 sentences, per @handle or r/sub]

KEY PATTERNS from the research:
1. [Pattern] - per @handle
2. [Pattern] - per r/sub
3. [Pattern] - per @handle
```

**If COMPARISON** - use the comparison output format from section 5 above.

### Stats Block

**Calculate actual totals from the research output.** Count posts/threads from each section. Sum engagement: parse likes, upvotes, views from each item. Identify top voices.

**Copy this EXACTLY, replacing only the {placeholders}:**

```
---
✅ All agents reported back!
├─ 🟠 Reddit: {N} threads │ {N} upvotes │ {N} comments
├─ 🔵 X: {N} posts │ {N} likes │ {N} reposts
├─ 🔴 YouTube: {N} videos │ {N} views │ {N} with transcripts
├─ 🎵 TikTok: {N} videos │ {N} views │ {N} likes │ {N} with captions
├─ 📸 Instagram: {N} reels │ {N} views │ {N} likes │ {N} with captions
├─ 🧵 Threads: {N} posts │ {N} likes │ {N} replies
├─ 📌 Pinterest: {N} pins │ {N} saves │ {N} comments
├─ 🟡 HN: {N} stories │ {N} points │ {N} comments
├─ 🦋 Bluesky: {N} posts │ {N} likes │ {N} reposts
├─ 🇺🇸 Truth Social: {N} posts │ {N} likes │ {N} reposts
├─ 🐙 GitHub: {N} items │ {N} reactions │ {N} comments
├─ 📊 Polymarket: {N} markets │ {exact % odds}
├─ 🔮 Perplexity: {N} insights │ {N} citations
├─ 🌐 Web: {N} pages — Source Name, Source Name
├─ 🗣️ Top voices: @{handle1} ({N} likes), @{handle2} │ r/{sub1}, r/{sub2}
└─ 📎 Raw results saved to ~/Documents/Last30Days/{slug}-raw.md
---
```

**CRITICAL: Omit any line with 0 results.** Do NOT show "0 threads", "0 stories", "0 markets", or "(no results this cycle)". If a source found nothing, DELETE that line entirely.

**Web line - how to extract site names from URLs:** Strip the protocol, path, and `www.` - use the recognizable publication name. List as comma-separated plain names.

---

## 10. Invitation

Adapt to QUERY_TYPE. Every invitation MUST include 2-3 specific example suggestions based on what you ACTUALLY learned from the research.

**If QUERY_TYPE = PROMPTING:**
```
---
I'm now an expert on {TOPIC} for {TARGET_TOOL}. What do you want to make? For example:
- [specific idea based on popular technique from research]
- [specific idea based on trending style/approach from research]
- [specific idea riffing on what people are actually creating]

Just describe your vision and I'll write a prompt you can paste straight into {TARGET_TOOL}.
```

**If QUERY_TYPE = RECOMMENDATIONS:**
```
---
I'm now an expert on {TOPIC}. Want me to go deeper? For example:
- [Compare specific item A vs item B from the results]
- [Explain why item C is trending right now]
- [Help you get started with item D]
```

**If QUERY_TYPE = NEWS:**
```
---
I'm now an expert on {TOPIC}. Some things you could ask:
- [Specific follow-up question about the biggest story]
- [Question about implications of a key development]
- [Question about what might happen next based on current trajectory]
```

**If QUERY_TYPE = COMPARISON:**
```
---
I've compared {TOPIC_A} vs {TOPIC_B} using the latest community data. Some things you could ask:
- [Deep dive into {TOPIC_A} alone with /last30days {TOPIC_A}]
- [Deep dive into {TOPIC_B} alone with /last30days {TOPIC_B}]
- [Focus on a specific dimension from the comparison table]
- [Look at a different time period with --days=7 or --days=90]
```

**If QUERY_TYPE = GENERAL:**
```
---
I'm now an expert on {TOPIC}. Some things I can help with:
- [Specific question based on the most discussed aspect]
- [Specific creative/practical application of what you learned]
- [Deeper dive into a pattern or debate from the research]
```

Context-aware: Only list sources that returned results in the closing line. Build the source list from your stats.

---

## 11. Follow-Up

After research, you are an **EXPERT** on this topic.

When the user responds, match their intent:

- **QUESTION** about the topic -> Answer from research (no new searches)
- **GO DEEPER** on a subtopic -> Elaborate from findings
- **CREATE/PROMPT** -> Write ONE prompt using research insights
- **Different topic** -> Run new research

### Mode Toggles

- **"eli5 on"** / **"eli5 mode"** / **"explain simpler"** -> Write `ELI5_MODE=true` to `~/.config/last30days/.env`. Confirm: "ELI5 mode on. All future runs will explain things like you're 5."
- **"eli5 off"** / **"normal mode"** / **"full detail"** -> Write `ELI5_MODE=false` to `~/.config/last30days/.env`. Confirm: "ELI5 mode off. Back to full detail."
- **"more fun"** / **"too serious"** -> Write `FUN_LEVEL=high` to `~/.config/last30days/.env`. Confirm: "Fun level set to high. Next run will surface more witty and viral content."
- **"less fun"** / **"too many jokes"** -> Write `FUN_LEVEL=low` to `~/.config/last30days/.env`. Confirm: "Fun level set to low. Next run will focus on the news."

### Writing Prompts

When the user wants a prompt, write a single, highly-tailored prompt using your research expertise.

**CRITICAL: Match the FORMAT the research recommends.** If research says to use JSON prompts with device specs, your prompt MUST be JSON. If research says structured params, use structured params.

Quality Checklist (run before delivering):
- FORMAT MATCHES RESEARCH - if research said JSON/structured/etc, prompt IS that format
- Directly addresses what the user said they want to create
- Uses specific patterns/keywords discovered in research
- Ready to paste with zero edits (or minimal [PLACEHOLDERS] clearly marked)
- Appropriate length and style for TARGET_TOOL

### Output Summary Footer (After Each Prompt)

```
---
Expert in: {TOPIC} for {TARGET_TOOL}
Based on: {n} Reddit threads ({sum} upvotes) + {n} X posts ({sum} likes) + {n} YouTube videos ({sum} views) + {n} TikTok videos ({sum} views) + {n} Instagram reels ({sum} views) + {n} HN stories ({sum} points) + {n} web pages

Want another prompt? Just tell me what you're creating next.
```

Only include sources with non-zero results in the footer.
