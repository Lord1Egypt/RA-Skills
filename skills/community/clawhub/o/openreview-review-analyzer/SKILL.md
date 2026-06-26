---
name: openreview-review-analyzer
description: Fetch and analyze peer reviews from OpenReview for any academic paper. Use this skill when the user mentions OpenReview, asks about reviews for a paper, wants a review summary or synthesis, provides an openreview.net URL, mentions a paper forum ID, asks about reviewer opinions or scores for a conference submission (ICLR, NeurIPS, ICML, AAAI, etc.), or wants to understand what reviewers think about a specific paper. Also trigger when the user says things like 'what did reviewers say about this paper', 'summarize the reviews', 'get reviews for this submission', or 'analyze reviewer feedback'. Even if the user just pastes an OpenReview link, this skill should trigger.
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# OpenReview Review Analyzer

Fetch all public peer reviews for any paper on OpenReview and generate a structured synthesis report.

## When to Use

- User provides an OpenReview URL (e.g., `https://openreview.net/forum?id=XXXXX`)
- User asks to analyze or summarize reviews for a conference paper
- User mentions a paper's OpenReview forum ID
- User wants to understand reviewer consensus, disagreements, or key concerns
- User asks about scores, ratings, or review content for any venue on OpenReview

## Workflow

### Step 1: Extract Forum ID

Parse the OpenReview URL or forum ID from user input. The forum ID is the `id` parameter in the URL:
- `https://openreview.net/forum?id=xxxxxxx` → forum ID = `xxxxxxx`

### Step 2: Fetch Reviews via Script

Run the Python script to fetch all reviews and metadata:

```bash
python3 {baseDir}/scripts/fetch_reviews.py <forum_id>
```

The script has **zero external dependencies** — it uses Python's built-in `urllib`. If `requests` is installed it will use that instead, but it's not required.

The script outputs a JSON file at `/tmp/openreview_<forum_id>.json` containing:
- Paper metadata (title, authors, abstract, venue, keywords)
- All official reviews with ratings, confidence, strengths, weaknesses, questions, and full review text
- All official comments (author responses, reviewer discussions)
- Meta-review if available

If the script fails (e.g., network restrictions, reviews not public, paper withdrawn), use these fallback methods in order:

**Fallback 1 — web_fetch the API directly:**
```
web_fetch https://api2.openreview.net/notes?forum=<forum_id>
```
Parse the JSON response to get the submission, then:
```
web_fetch https://api2.openreview.net/notes?forum=<forum_id>&trash=true
```
to get all replies including reviews. Filter replies where `invitations` contains `Official_Review`.

**Fallback 2 — web_search for review content:**
Search for `"<forum_id>" review site:openreview.net` or `"<paper_title>" review <venue>` to find discussions, blog posts, or cached review content.

**Fallback 3 — inform the user:**
If no review data is accessible, explain that reviews may not be public yet, or suggest the user check the OpenReview page directly.

### Step 3: Generate Synthesis Report

Read the JSON output and produce a structured report following `{baseDir}/references/report-template.md`.

Key analysis points:
1. **Score Distribution** — list each reviewer's rating and confidence, compute average
2. **Consensus Points** — identify strengths/weaknesses mentioned by multiple reviewers
3. **Key Disagreements** — where reviewers diverge in opinion
4. **Critical Issues** — weaknesses flagged as major by any reviewer
5. **Questions Raised** — important unresolved questions
6. **Author Responses** — summarize rebuttal if available, and whether reviewers updated scores
7. **Meta-Review** — include AC recommendation if available
8. **Overall Assessment** — synthesize into a clear verdict

## Important Notes

- OpenReview content is public for completed review cycles. Some venues keep reviews private until decisions are made.
- For withdrawn papers, reviews may or may not be visible depending on venue policy.
- Always attribute opinions to specific reviewers (e.g., "Reviewer 1 (rating: 5)") when citing specific claims.
- The script uses the OpenReview API v2 by default (for venues from 2024+) and falls back to API v1 for older venues.
- No authentication is needed for reading public reviews.

## Output Language

Match the user's language. If the user writes in Chinese, output the report in Chinese. If in English, output in English.
