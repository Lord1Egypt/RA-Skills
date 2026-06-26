# Paper Impact Analyzer

Multi-source, fault-tolerant academic paper impact analysis for Claude Code / OpenClaw.

> Tired of Semantic Scholar rate limits killing your research workflow? This tool still works when S2 is down, using GitHub + OpenAlex + arXiv as fallbacks.

## Features

- **Zero API keys required** — all data sources are free and keyless
- **Graceful degradation** — each source fails independently, you always get a report
- **Age-aware scoring** — new papers scored by GitHub + venue + team; older papers scored by citations
- **Single file, zero dependencies** — Python stdlib only

## Data Sources

| Priority | Source | What it provides | Reliability |
|----------|--------|-----------------|-------------|
| 1 | arXiv API | Title, authors, date, venue detection | Always available |
| 2 | GitHub API | Stars, forks, issues, repo age | ~90% success |
| 3 | OpenAlex API | Citation count (free, no key) | ~80% success |
| 4 | Semantic Scholar | Citations, influential citations, author h-index | ~50% (rate limited) |

## Usage

### As a Claude Code skill

```
Analyze the impact of arxiv paper 2603.04948
```

### Command line

```bash
# Single paper
python scripts/analyze.py 2603.04948

# Multiple papers
python scripts/analyze.py 2603.04948 2602.15922 2603.05488 2602.22661
```

### Sample Output

```
## Impact: dLLM: Simple Diffusion Language Modeling

- arXiv: 2602.22661
- Published: 2026-02-26 (27 days ago)
- Authors: Zhanhui Zhou, Lingjie Chen, Hanghang Tong, Dawn Song

| Dimension | Data                          | Signal |
|-----------|-------------------------------|--------|
| Venue     | Preprint / Unknown            | --     |
| GitHub    | 2268 stars / 214 forks        | +++++ |
| Citations | OpenAlex: 0                   | too new|
| Author    | Data unavailable              | --     |

Rating: S
Confidence: medium
Data completeness: 3/4 sources available
```

## Install from ClawHub

```bash
clawhub install paper-impact-analyzer
```

## How It Works

1. Fetches paper metadata from arXiv API (title, authors, abstract, comment field)
2. Detects venue acceptance from the arXiv comment field (e.g., "Accepted at ICLR 2026")
3. Extracts GitHub URL from abstract/comments, or searches GitHub API by title
4. Queries OpenAlex for citation count using the arXiv DOI
5. Queries Semantic Scholar for citations + first author h-index (with rate limiting)
6. Synthesizes a weighted rating based on paper age:
   - < 3 months: venue (3x) + GitHub (3x) + author (2x) + citations (0.5x)
   - 3-12 months: venue (2x) + GitHub (2x) + citations (2.5x) + author (1.5x)
   - > 1 year: citations (3.5x) + venue (1.5x) + GitHub (1x) + author (1x)

## Rating Scale

| Rating | Meaning |
|--------|---------|
| S | Exceptional impact signals |
| A | Strong impact |
| B | Moderate impact |
| C | Limited signals available |
| D | Minimal impact or insufficient data |

## License

MIT-0

## Author

[@haataa](https://github.com/haataa)
