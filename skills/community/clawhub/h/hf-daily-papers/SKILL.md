---
name: hf-daily-papers
description: "Fetch and digest HuggingFace Daily Papers. Use when user asks for today's HF papers, daily paper digest, wants a paper report, or says 论文精选/今日论文/HF daily papers. Fetches from hf.co/papers via HF API, reads results, scores and generates a formatted digest with commentary."
---

# HF Daily Papers

Fetch papers from HuggingFace Daily Papers feed and generate a digest with analysis.

## Setup: Get Your HF Token

1. Go to **https://huggingface.co/settings/tokens**
2. Create a Read token (any name)
3. Set the token as an environment variable:

```powershell
# Windows PowerShell
$env:HF_TOKEN = "hf_xxxxxxxxxxxxx"

# macOS / Linux / Git Bash
export HF_TOKEN="hf_xxxxxxxxxxxxx"
```

> The script reads `HF_TOKEN` from `os.environ`. If not set, it exits with a clear error message.

## Step 1: Run the fetcher

```bash
cd <skill-path>/scripts && python hf_papers.py [date YYYY-MM-DD]
```

- No date arg = yesterday
- Output: `hf_results.json` (saved in the working directory)

## Step 2: Read results

Read `hf_results.json`. Fields:

| Field | Description |
|-------|-------------|
| `paperId` | arXiv ID |
| `title` | Paper title |
| `votes` | Community upvotes |
| `submittedBy` | Submitter name |
| `organization` | Research institution |
| `summary` | Full abstract (cleaned, up to 2000 chars) |
| `aiSummary` | AI-generated summary (200-300 chars, from HF blue box) |
| `githubRepo` | GitHub repo URL if available |
| `keywords` | AI-extracted keywords (up to 10) |
| `link` | HF paper page |
| `arxivLink` | arXiv abstract page |

## Step 3: Score and write digest

Scoring reference (10-point scale, intuition-based):

| Dimension | Weight | Bonus signals |
|-----------|--------|---------------|
| Innovation | 0-3 | New benchmark/dataset, novel direction, first-of-its-kind |
| Practicality | 0-3 | Has GitHub code, clear real-world application, big tech/academia |
| Technical depth | 0-2 | Summary >200 chars, contains RL/MCTS/evolutionary methods |
| Interestingness | 0-2 | Provocative thesis, cross-discipline, counterintuitive |

**High vote count (>10) is a bonus** — reflects community heat.

## Step 4: Output format

```
📄 HF Daily Papers · [date]  N papers total

## 🔴 Must Read (score 8-10)
[Title | ID | Organization
 Xiaolongxia comment: ...]
## 🟡 Worth Noting (score 6-7)
[Compact list + one-line evaluation]
## 🟢 Skim If Interested
[Ultra brief list]

## 🦞 Summary
Top 3 + today's main theme observations
```

Commentary guidelines:
- Every "Must Read" paper needs a "Xiaolongxia comment" — explain the core insight in your own words
- Say why it's worth reading and what makes it special
- Can connect to other papers or industry trends
- Tone: casual, witty, friendly — like chatting with a friend
- "Worth Noting" entries: one sentence max
