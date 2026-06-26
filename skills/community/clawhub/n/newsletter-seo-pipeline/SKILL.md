---
name: newsletter-seo-pipeline
description: >
  8-step SEO content production workflow for newsletters and blogs.
  Runs SERP analysis, builds an optimized outline, writes in your newsletter's
  voice, screens for AI patterns, applies quality gates, validates SEO metadata,
  formats, and generates a paste-ready publish doc — all in one pipeline.
  Use when writing a newsletter issue, an evergreen SEO post, or any
  long-form article that needs to rank in search.
  Triggers on: 'write issue', 'write newsletter', 'write evergreen post',
  'write SEO post', 'run the pipeline', 'produce issue', 'newsletter pipeline',
  'write article', 'write blog post'.
  Pairs with newsletter-launch for full automation.
  NOT for: social posts, email subject lines, short-form copy, keyword research only.
  Requires: serp-analysis, seo-content-engine, article-writing, markdown-formatter.
  Optional: de-ai-ify (auto-installed by newsletter-launch).
---

# Newsletter SEO Pipeline

## Article Header Block (required in every output file)

Every article must start with this block — scripts depend on it:

```
Meta Title: <50–60 chars, includes primary keyword>
Meta Description: <150–160 chars, includes keyword + value prop>
URL Slug: <keyword-rich-hyphenated-slug>
Primary Keyword: <exact keyword phrase>
```

## Production Workflow (run in order — do not skip steps)

### Step 1 — SERP Analysis
Run `serp-analysis` skill on the primary keyword.
Goal: identify content gaps, SERP features, search intent, and top-ranking structure.

### Step 2 — SEO Outline
Run `seo-content-engine` skill.
Goal: keyword variants, H2/H3 structure, target word count, internal link opportunities.

### Step 3 — Write
Run `article-writing` skill using the outline from Step 2.
Include the Article Header Block at the top of the output file.

Voice reference: `projects/<slug>/writing-style.md` — where `<slug>` is the project slug from the project memory file.
This file lives in the newsletter's project folder and was generated during `newsletter-launch` setup.

If missing:
- Check the project folder at `projects/<slug>/` — it should be there
- If the whole project folder is missing, re-run `newsletter-launch` for this newsletter
- If only writing-style.md is missing, recreate it by running `newsletter-launch` and choosing 'update style guide' when prompted

### Step 4 — AI Pattern Pre-Screen
The skill directory = the folder containing this SKILL.md file. Use its absolute path throughout.
Run the pre-screen script:
```
python3 <skill_dir>/scripts/score_ai_patterns.py <article_file>
```
- Score ≥ 8: proceed to Step 5
- Score < 8 and `de-ai-ify` skill is installed: run it, then re-run the script to confirm ≥ 8
- Score < 8 and `de-ai-ify` is NOT installed: manually rewrite flagged patterns (script lists them by line), then re-run the script until score ≥ 8 before continuing

### Step 5 — Quality Gate (built-in QVP)
Check all 5 gates. Each must pass before continuing:
1. **Completeness** — does the article fully address the target keyword and search intent? No gaps, no unanswered questions a reader would have.
2. **Accuracy** — are all facts, stats, dollar figures, and claims verifiable? No fabricated sources. Flag any uncertain claims explicitly.
3. **Source integrity** — every stat or claim must trace to a real, named source (publication, study, company report). No "experts say" or vague attributions.
4. **Action clarity** — every H2 section must end with a clear action the reader can take. No insight without a takeaway. Ownership must be clear.
5. **Format check** — Article Header Block is present and complete. Meta title 50–60 chars. Meta description 150–160 chars. Exactly one H1. At least 3 H2s. No placeholder text remaining.

If any gate fails: fix the specific issue, then re-check that gate before continuing. Do not proceed with a failed gate.

### Step 6 — SEO Validation
Run the validator script. Resolve path relative to this skill's directory:
```
python3 <skill_dir>/scripts/validate_seo.py <article_file> "<primary keyword>"
```
Fix all ❌ ISSUES before continuing. ⚠️ WARNINGS should be fixed but are not blocking.

### Step 7 — Markdown Format
Run `markdown-formatter` skill for a final clean formatting pass.

### Step 8 — Build Paste Doc
Generate the beehiiv-ready publish doc. Resolve path relative to this skill's directory:
```
python3 <skill_dir>/scripts/build_paste_doc.py <article_file> <YYYY-MM-DD>
```
This produces `<article_file_stem>-PASTE.md` — the file the user copies into beehiiv.

## Output

Alert the user with:
- Path to the final article file
- Path to the `-PASTE.md` file
- Confirm all gates passed: QVP ✅, SEO validation ✅, AI score ✅
- Include the AI score (e.g. 9/10), so the user knows the quality level

## Context Required

Before running the pipeline, the calling context (cron, user message, or issue template) must supply:
- **Project slug** — to locate `projects/<slug>/writing-style.md` and output files to the correct folder
- **Primary keyword** — for SERP analysis and SEO validation
- **Publish date** — for the paste doc (YYYY-MM-DD)

These are always present in the cron payloads generated by `newsletter-launch`.
If running manually, read the project memory file at `projects/<slug>/project.md` first.
