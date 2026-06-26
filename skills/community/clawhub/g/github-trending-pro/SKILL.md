---
name: github-trending
description: Use when the user asks for GitHub Trending, GitHub hot repositories, daily/weekly/monthly trending repos, trending projects by programming language, spoken-language filtered GitHub trends, or trend analysis of popular GitHub projects.
---

# GitHub Trending

Use this skill as a GitHub Trending intelligence report: fetch the live榜单, preserve verifiable facts, then explain what matters, why it is trending, and what technical direction it signals.

## Workflow

1. Infer filters from the user request.
   - Programming language: use the mentioned language, otherwise leave blank for the default all-language Trending page.
   - Date range: map "today/current/daily" to `daily`, "this week/weekly" to `weekly`, and "this month/monthly" to `monthly`. Default to `daily`.
   - Spoken language: use `--spoken-language` only when the user requests a natural-language filter such as Chinese/English repositories.
   - Output language: answer in Chinese when the user asks in Chinese; otherwise answer in English.
2. Run `scripts/fetch_trending.py` with the inferred filters. Use JSON for analysis; use Markdown only when the user asks for a raw table/export.
3. Use the JSON output to write the report. Do not invent stars, languages, descriptions, repository URLs, author names, or avatar URLs.
4. If the script returns no repositories, say that GitHub Trending returned no matching projects and include the filters used.

## Script

Run from the skill directory:

```bash
python3 scripts/fetch_trending.py --since daily --limit 10
python3 scripts/fetch_trending.py --language python --since weekly --limit 10 --format json
python3 scripts/fetch_trending.py --language rust --since monthly --spoken-language zh --limit 10
python3 scripts/fetch_trending.py --language javascript --since daily --format markdown
```

The script outputs JSON with:

- Report metadata: `date`, `since`, `language`, `spoken_language`, `url`, `updated_at`
- Compatibility fields: `rank`, `repo`, `url`, `description`, `language`, `total_stars`, `forks`, `current_period_stars`
- Intelligence fields: `full_name`, `author`, `author_avatar`, `name`, `title`, `title_en`, `summary`, `summary_en`, `primary_lang`, `lang_color`, `updated_at`

`title/title_en/summary_en` are deterministic text fields derived from the GitHub Trending description when possible. If a richer translated title or summary is needed, generate it in the final report and keep it clearly separate from raw GitHub facts.

## Differentiation

This skill should not behave like a simple leaderboard copier. Treat the table as the scan layer and the analysis as the value layer:

- Identify the main project category: AI agent, developer tooling, framework, infrastructure, data, security, UI, media, education, or other.
- Explain the user-facing capability, not just the repository description.
- Infer implementation only from available evidence such as language, description, and public repository context.
- Explain "Why Trending" as a grounded hypothesis using current-period stars, category momentum, and the project's positioning.
- End with a concise trend synthesis that helps the user decide what to inspect next.

## Report Format

Start every report with title, date, range, programming language, and spoken language. Then include an `Overview` table before project details.

Use this table header exactly:

```markdown
| # | Repo | Total Stars | Today | Lang | Description |
|---|------|-------------|-------|------|-------------|
```

For weekly/monthly reports, keep the column name `Today` only if the user explicitly asked for that header; otherwise rename it to `This Week` or `This Month`.

Use this detail structure for each repository:

```markdown
### 1. owner/repo
- URL: https://github.com/owner/repo
- Stars: 12,345
- Today: +321
- Lang: Python
- Description: Short repository description.

**Feature**: What the project provides.
**Functionality**: What users can do with it.
**Implementation**: Likely implementation approach based on language, description, and repository context.
**Why Trending**: Why it is plausibly popular in this date range.
```

End with a trend summary. Highlight repeated themes such as AI agents, developer tooling, infrastructure, frameworks, data systems, security, UI libraries, or language-specific momentum.

## Analysis Rules

- Base factual fields on the script output.
- Keep inferred sections clearly grounded in the repository description and public context.
- When information is missing, say "not specified" or omit that field instead of guessing.
- Prefer the top 10 repositories unless the user requests a different count.
- Keep reports scannable: brief overview rows, concise per-project paragraphs, and a short final trend analysis.
- If the user asks for JSON, return the script JSON or a strict subset of it; do not mix prose into JSON.
- If the user asks for a human report, answer in the user's language and include the Overview table first.
