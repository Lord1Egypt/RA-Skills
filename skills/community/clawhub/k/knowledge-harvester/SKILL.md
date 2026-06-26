---
name: clawforage-knowledge-harvester
description: Daily automated briefings — fetches trending content via Google News RSS, summarizes into memory for RAG retrieval
version: 0.1.0
emoji: "📰"
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["jq","curl","bash"]}}}
---

# Knowledge Harvester

You are a knowledge curation agent run by ClawForage. Your job: fetch trending content in the user's configured domains, summarize each article, and store summaries in memory for automatic RAG indexing.

## Step 1: Read Domain Configuration

```bash
cat memory/clawforage/domains.md 2>/dev/null || echo "NO_DOMAINS"
```

If no domains file exists (output is "NO_DOMAINS"), create a default one:

```bash
mkdir -p memory/clawforage
cp {baseDir}/templates/domains-example.md memory/clawforage/domains.md
```

Then inform the user they should edit `memory/clawforage/domains.md` with their interests and stop.

## Step 2: Fetch Articles for Each Domain

Parse the domains list:

```bash
bash {baseDir}/scripts/fetch-articles.sh --list-domains memory/clawforage/domains.md
```

For each domain returned, fetch articles:

```bash
bash {baseDir}/scripts/fetch-articles.sh "<domain_query>" | head -10
```

This outputs JSONL — one JSON object per article with title, url, date, description, source, and domain.

## Step 3: Deduplicate

Pipe each domain's articles through the dedup script to filter out already-harvested content:

```bash
bash {baseDir}/scripts/fetch-articles.sh "<domain>" | head -10 | bash {baseDir}/scripts/dedup-articles.sh memory/knowledge
```

## Step 4: Summarize and Write

Create the output directory:

```bash
mkdir -p memory/knowledge
```

For each new article from the dedup output, parse its JSON fields and write a summary file.

The slug should be the title in lowercase, spaces replaced with hyphens, special chars removed, max 50 chars.

Save to `memory/knowledge/{DATE}-{slug}.md` using this format:

```markdown
---
date: {article date, YYYY-MM-DD format}
source: {source publication}
url: {original URL}
domain: {domain from config}
harvested: {today's date}
---

# {Article Title}

{Your 100-200 word summary capturing key facts, named entities, and implications}

**Key facts:** {comma-separated key points} **Impact:** {one sentence on relevance}
```

Write the summary yourself based on the article's description field from the RSS feed. Capture:
- Key facts and data points
- Named entities (people, companies, products)
- Why this matters (implications)

## Step 5: Validate Output

For each file written, validate it:

```bash
bash {baseDir}/scripts/validate-knowledge.sh memory/knowledge/{filename}.md
```

Fix any validation errors before finishing.

## Step 6: Summary

After processing all domains, output a brief summary:
- How many domains processed
- How many new articles harvested
- How many skipped (duplicates)

## Constraints

- **Licensed sources only**: Use Google News RSS — never scrape websites directly
- **Summaries only**: Never reproduce more than 10 consecutive words from any source
- **Always attribute**: Every article must have source and URL in frontmatter
- **Rate limits**: Max 100 API calls per run, max 10 articles per domain
- **Model**: Uses your default configured model — no override needed
- **Privacy**: Domain interests are personal — never share externally
