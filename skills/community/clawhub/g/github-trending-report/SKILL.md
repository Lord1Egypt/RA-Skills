# GitHub Trending Report

Use the `github-discover` CLI to fetch real-time GitHub data and generate structured trending reports — discover fast-rising repositories, newly popular projects, and hot topic tags.

## Installation

```bash
npm install -g github-discover
```

> Requires Node.js 18+. Check with `node --version`.

## Prerequisites

- Node.js ≥ 18
- `github-discover` installed globally (see Installation above)

## Commands

### trending — Fastest-growing repositories

Ranked by daily average stars with a 30-day smoothing factor, removing age bias to surface genuinely fast-rising projects.

```bash
github-discover trending [options]
```

| Option | Description | Default |
|---|---|---|
| `-p` | Period: daily / weekly / monthly / yearly | daily |
| `-n` | Number of results (1–100) | 50 |
| `-l` | Filter by programming language (e.g. python, typescript) | all |
| `-s` | Minimum star threshold | auto by period |
| `--json` | Output as JSON | — |

### popular — New high-star repositories

Sorted by raw star count descending, focused on recently created high-popularity projects.

```bash
github-discover popular [options]
```

Same options as `trending`.

### topic — Hot topic tags

Scored by `repoCount × log10(starSum)` to surface trending technology topics.

```bash
github-discover topic [options]
```

| Option | Description | Default |
|---|---|---|
| `-p` | Period: daily / weekly / monthly / yearly | daily |
| `-n` | Number of results (1–100) | 30 |
| `--json` | Output as JSON | — |

## Data Windows (trending command)

| Period | Repository creation range |
|---|---|
| daily | Created within last 7 days |
| weekly | Created within last 28 days |
| monthly | Created within last 90 days |
| yearly | Created within last 730 days |

## Standard Workflow for Generating a Report

When a user requests a GitHub trending report, follow these steps:

**Step 1: Verify the tool is available**

```bash
github-discover --version
```

If the command is not found, prompt the user to run `npm install -g github-discover`, then stop.

**Step 2: Determine the time period**

Infer the period from the user's request:
- "today" / "latest" / "right now" → `daily`
- "this week" / "weekly" → `weekly`
- "this month" / "monthly" → `monthly`
- "this year" / "annual" → `yearly`
- Not specified → default to `daily`

**Step 3: Fetch all three data sets in parallel**

```bash
github-discover trending -p <period> -n 10 --json
github-discover popular  -p <period> -n 10 --json
github-discover topic    -p <period> -n 10 --json
```

If the user specified a language (e.g. Python, TypeScript), append `-l <language>` to the `trending` and `popular` commands.

**Step 4: Generate the structured report**

Combine the JSON output from all three commands and produce a report in the following format:

---

## 📈 GitHub <Period> Trending Report

### 1. Fastest-Growing Projects
> Source: `trending` — reflects real growth velocity, age bias removed

List Top 5–10 entries, each with:
- Repository name (with link)
- Short description
- Star count / daily average growth
- Primary language

### 2. Newly Popular Repositories
> Source: `popular` — recently created projects gaining rapid traction

List Top 5–10 entries, same format as above.

### 3. Hot Topics
> Source: `topic` — scored by repository count × star magnitude

List Top 10 topic tags with a brief description of each technology area.

### 4. AI Insights
Based on the data above, provide:
- A 2–3 sentence summary of the key technical trends this period
- Projects or movements worth watching closely
- If a language filter was applied, a brief analysis of that ecosystem's current state

---

## Limitations

- Data is sourced from the GitHub Search API; freshness depends on GitHub's indexing lag
- The `trending` growth score is estimated from creation time and star count, and it is **not** GitHub's official Trending page data
- The `-l` language filter matches only the repository's primary language; multi-language projects may be excluded
