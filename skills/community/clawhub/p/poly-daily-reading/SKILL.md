---
name: poly-daily-reading
description: >
  Generate Guillaume's daily reading list by searching curated sources across AI, LLMs,
  full-stack dev, anime, horror games, and metal music. Use when asked to "generate reading list",
  "daily reading", "find articles to read", or when running Poly's daily cron task.
  Handles dedup against past readings, Obsidian file output, Mission Control ingestion,
  and weekly/yearly archiving.
---

# Poly Daily Reading List (Optimized)

Generate and deliver a curated daily reading list for Guillaume.

## Paths

- **Obsidian vault:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Guillaume Maka/`
- **Daily reading dir:** `<vault>/Daily Reading/`
- **Output file:** `<vault>/Daily Reading/daily-YYYY-MM-DD.md`
- **Read-status cache:** `~/.openclaw/workspace-poly/reading-lists/read-status.json`
- **Mission Control CLI:** `~/.openclaw/workspace/mission-control/apps/cli`

## Workflow

### 1. Collect Past Read URLs (Optimized)

Before searching, gather URLs Guillaume already read from recent history:

1. Glob `daily-*.md` files from last 30 days only in Daily Reading dir
2. Extract URLs from lines matching `[x]` (checked/read items)
3. Load `read-status.json` if it exists for additional cached read URLs
4. Combine into a deduplicated exclusion set

Helper script (updated):
```bash
scripts/collect-read-urls.py <daily-reading-dir> --days 30
```
Outputs a JSON array of read URLs to stdout.

### 2. Search (Optimized)

Search across all topics with explicit limits:

**Priority order:**
1. Primary AI sources (OpenAI Blog, Anthropic Blog, Kilo.ai Blog, DeepLearning.AI, arxiv)
   - Fetch only latest 5 items per source (not full blog)
   - Use source-specific feeds/APIs when available
2. Web search for other topics (full-stack, anime, horror games, metal)
   - Limit to 3 results per category with `count: 3`
   - Add 10-second timeout per search operation

**Quality focus**: Still aim for 2-5 strong picks per category max, but with bounded search space.

### 3. Filter (Unchanged)

Remove any URL matching the exclusion set from Step 1.

### 4. Write Daily File (Unchanged)

Create `<vault>/Daily Reading/daily-YYYY-MM-DD.md`:

```markdown
# Daily Reading List — May 8, 2026

## AI & Agentic
- [ ] [Title](url) — One-line summary

## Full Stack Dev
- [ ] [Title](url) — One-line summary

## Anime
- [ ] [Title](url) — One-line summary

## Horror Games
- [ ] [Title](url) — One-line summary

## Metal Music
- [ ] [Title](url) — One-line summary
```

Categories with no items should still appear (empty section) so Guillaume knows they were checked.

### 5. Update Read-Status Cache (Optimized)

Append today's new URLs to SINGLE read-status file:
`~/.openclaw/workspace-poly/reading-lists/read-status.json`

Remove duplicate update to agent directory to reduce write operations.

```json
{
  "lastUpdated": "YYYY-MM-DD",
  "readUrls": ["url1", "url2"]
}
```

### 6. Notify (Unchanged)

Deliver a brief summary with the link to the Obsidian file.

## Mission Control Integration

After saving the daily file, ingest into Mission Control:

```bash
cd ~/.openclaw/workspace/mission-control/apps/cli
npx tsx src/index.ts ingest reading-list --data '<JSON>'
```

JSON format:
```json
{
  "agentId": "poly",
  "date": "YYYY-MM-DD",
  "articles": [
    {"title": "...", "url": "...", "category": "ai"}
  ],
  "delivered": true,
  "deliveryChannel": "telegram"
}
```

Valid categories: `ai`, `llms`, `safety`, `prompting`, `fullstack`, `anime`, `horror`, `metal`

Then update agent status:
```bash
npx tsx src/index.ts ingest status --agent-id poly --status online --activity-message "Reading list delivered"
```

## Weekly Archiving (Mondays)

Before generating today's list, on Mondays:

1. Query Mission Control for last week's data:
   ```bash
   npx tsx src/index.ts query reading-lists --dateFrom <mon> --dateTo <sun> --agentId poly --format json
   ```
2. Collect all `daily-*.md` files from Mon–Sun of last week
3. Group items by source/topic
4. Write to `<vault>/Daily Reading/Archives/Month YYYY.md` (e.g., "May 2026.md") with header:
   ```markdown
   # Week of May 4-10, 2026

   ## Collected Unread Items
   - [ ] [Title](url) — Summary
   ```
5. Delete the individual daily files after archiving
6. Ingest archive task:
   ```bash
   npx tsx src/index.ts ingest task --agentId poly --title "Daily Reading Weekly Archive" --description "Archived last week's reading lists" --status completed --category maintenance
   ```

## Yearly Archiving (January 1st)

Before generating today's list, on Jan 1:

1. Collect all daily readings from the past year
2. Group by month within a single file
3. Write to `<vault>/Daily Reading/YYYY.md` (e.g., "2025.md")
4. Delete monthly archive files after creating yearly
5. Ingest archive task as above
