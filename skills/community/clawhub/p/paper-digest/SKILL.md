---
name: paper-digest
description: "Given an arXiv ID or URL, fetch the paper, spawn sub-agents to read its key citations, and write an executive summary under."
user-invocable: true
author: Damoon
version: 0.0.1
---
# Paper Digest

## Input

- `arxiv_id`: bare ID like `2305.11206` or full `https://arxiv.org/abs/2305.11206` (Normalise: strip the URL prefix, extract bare ID.)

## Step 1 — Fetch the main paper

Try HTML first: web.fetch https://arxiv.org/html/<arxiv_id>
- If HTTP 200 → use this as `paper_text`.
- If Falis: add v1 at the end, and try again: web.fetch https://arxiv.org/html/<arxiv_id>v1
- else if all fails skip and ABORT!

If the `paper_text` is retrieved then write the summary to `~/.openclaw/workspace/papers/<arxiv-id>.md`.

## Step 2 — Extract citations

Note: DO NOT DO THIS STEP INSIDE sub-agents

Within the `main agent` and from `paper_text`, identify **at most 5 citations** the paper most directly builds on. Prioritize:
- Papers that are **explicitly extended** or improved upon
- Papers used as the **primary baseline** for comparison
- Papers that **provide the core architecture** this work adopts
- Papers **referred to repeatedly** (not just mentioned once) or that provide essential context

For each citation, extract either the `arXiv ID` or the **title**. Then resolve to an arXiv URL:
- If an arXiv ID is in the reference → `https://arxiv.org/html/<id>`
- Otherwise search `https://arxiv.org/search/?query=<title>&searchtype=all` and take the first match.

## Step 3 — Spawn sub-agents for citations

***Note***: Ensure that the sub-agent related task is precise and concise so the sub-agent does not have to re-read the previously read SKILLs and files.

For each resolved citation:
- Check if the file for citation exists: `~/.openclaw/workspace/papers/<arxiv-id>.md`, if it does then skip and consider the sub-agent concluded.
- If the previous step fails then spawn a sub-agent with this EXACT instruction in VERBATIM: 
  - Fetch https://arxiv.org/html/<citation_id> (or add v1 at the end, and try again: web.fetch https://arxiv.org/html/<arxiv_id>v1). If unavailable, SKIP. If retrieved then Write the summary to `~/.openclaw/workspace/papers/<arxiv-id>.md`.


## Step 4 — Write the executive summary

Check the citation summaries within `~/.openclaw/workspace/papers/` then utilize the main paper we are summarising with citation summaries and write a single **markdown document in flowing prose** (no bullet lists) to `~/.openclaw/workspace/digest/report_<arxiv-id>`. Use this structure:

```markdown
# <Title>

<What problem this solves and why it matters. Context and related references summary>

<What prior work missed and how this paper addresses that gap. Cite inline as [Author et al., YEAR](<arxiv_link>).

<Core method in plain terms>

<Headline result. How it differs from previous work.

<One limitation and one future direction>

<Detailed Ablations, benchmarks if present in this paper or cited references>
```

## Rules

- Every citation must be a markdown link: `[Author et al., YEAR](<arxiv_or_url>)`
- No bullet lists in the output — **prose only**.
- If a section is absent from the paper (e.g., no ablations), skip it silently.
- Do not fabricate results, metrics, or author claims.
- **Citation resolution retry**: If a citation URL cannot be resolved after one retry, write the citation as plain text without a link: `[Author et al., YEAR]`.
