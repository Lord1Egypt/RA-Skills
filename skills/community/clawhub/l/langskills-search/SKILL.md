---
name: langskills-search
version: 0.1.0
description: Search 119K evidence-backed skills from 95K+ papers & 24K+ tech sources
author: LabRAI
tags: [research, skills, knowledge-base, search, evidence]
requires:
  bins: ["python3"]
metadata: {"source": "https://github.com/LabRAI/LangSkills", "license": "MIT", "min_python": "3.10"}
---

# LangSkills Search

Search 119,608 evidence-backed skills covering 62K+ research papers and 23K+ coding/tech sources — all offline via FTS5 SQLite.

## When to Use

- User asks for best practices, how-tos, or techniques on a technical topic
- You need evidence-backed knowledge (not LLM-generated guesses)
- Research tasks that benefit from academic or real-world source citations

## First-Time Setup

```bash
pip install langskills-rai
# Install matching bundles for the current project or pick a domain:
langskills-rai bundle-install --auto
```

## Search Command

```bash
langskills-rai skill-search "<query>" [options]
```

### Parameters

| Flag | Description | Default |
|:---|:---|:---|
| `--top N` | Number of results | 5 |
| `--domain <d>` | Filter by domain | all |
| `--min-score N` | Minimum quality score (0-5) | 0 |
| `--content` | Include full skill body | off |
| `--format markdown` | Output as Markdown | text |

### Example

```bash
langskills-rai skill-search "CRISPR gene editing" --domain research --top 3 --content --format markdown
```

## Reading Results

Each result includes: **title**, **domain**, **quality score** (0-5), **source URL**, and optionally the full skill body. Higher scores indicate stronger evidence chains.

## Available Domains

`linux` · `web` · `programming` · `devtools` · `security` · `cloud` · `data` · `ml` · `llm` · `observability` · `research-arxiv` · `research-plos-*` · `research-elife` · `research-other`

## Tips

- Use `--content --format markdown` to get copy-paste-ready skill text
- Combine `--domain` with `--min-score 4.0` for high-quality results
- Run `bundle-install --auto` in a project directory to install only relevant domains
