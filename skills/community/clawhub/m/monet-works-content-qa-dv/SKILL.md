---
id: 'monet-works-content-qa'
name: 'Monet Works Content QA Pipeline'
description: 'QA remediation auto-fix pipeline for Monet Works content. Detects and repairs common content issues: banned phrases, missing disclaimers, missing CTAs, and excessive length. Outputs fixed content to stdout and a structured change-report JSON to stderr.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Monet Works Content QA Pipeline

**Goal Chain**: L0 Medici Enterprises → L1 Monet Works → L2 Content Quality

## Purpose

This skill is an automated QA and remediation pipeline for all content produced by Monet Works. It detects and automatically fixes common content issues, ensuring brand consistency and quality before publication.

## How It Works

The `content-qa` CLI tool takes a markdown file as input and processes it through a series of checks and fixes. It outputs the remediated content to `stdout` and a structured JSON report of all changes to `stderr`.

### Checks and Fixes

1.  **Banned Phrases:**
    *   *Detects:* A list of 37+ banned phrases (e.g., "in conclusion," "game-changer," "level up").
    *   *Fix:* Automatically removes or rephrases them.

2.  **Missing Disclaimers:**
    *   *Detects:* If the content discusses investments, finance, or taxes without the standard legal disclaimer.
    *   *Fix:* Appends the required disclaimer to the end of the document.

3.  **Missing Call-to-Action (CTA):**
    *   *Detects:* If the content does not end with a clear CTA (e.g., a link to a product, a request to subscribe).
    *   *Fix:* Appends a default, context-aware CTA based on the content's topic.

4.  **Excessive Length:**
    *   *Detects:* If the word count exceeds platform-specific limits (e.g., >600 words for LinkedIn).
    *   *Fix:* Uses an AI model to generate a concise summary and offers it as an alternative.

5.  **AI Writing Patterns:**
    *   *Detects:* Integrates with the `ogilvy-humanizer` skill to detect and fix common AI writing tics.
    *   *Fix:* Applies the humanizer's transformations.

## Usage

### CLI

```bash
# Run the QA pipeline on a draft file
content-qa fix path/to/draft.md > path/to/fixed-draft.md 2> path/to/report.json

# Example report.json
{
  "changes": [
    {
      "type": "banned_phrase",
      "action": "removed",
      "original": "In conclusion, this is a great product.",
      "remediated": "This is a great product.",
      "line": 42
    },
    {
      "type": "missing_disclaimer",
      "action": "appended",
      "details": "Appended standard investment disclaimer."
    }
  ],
  "word_count": {
    "original": 750,
    "remediated": 738
  },
  "humanizer_score": {
    "before": 0.68,
    "after": 0.95
  }
}
```

## Integration

This is the final step in the Monet Works content generation pipeline, run just before scheduling a post.

```bash
# Part of the main content pipeline script
cat $DRAFT_FILE | content-qa fix > $FINAL_FILE 2> $QA_REPORT_FILE
```

## Configuration

-   **Banned Phrases:** Managed in `references/banned_phrases.txt`.
-   **Disclaimers:** Templates in `references/disclaimers/`.
-   **CTAs:** Default CTAs in `references/ctas.json`.

This automated QA process saves hours of manual editing and ensures every piece of content meets our quality standards.
