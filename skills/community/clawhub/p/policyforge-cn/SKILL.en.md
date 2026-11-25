---
name: policyforge-cn
display_name: PolicyForge — Policy Brief Intelligence
display_name_en: PolicyForge — Policy Brief Intelligence
description: A six-stage pipeline that turns a one-line assignment into a submission-ready Chinese policy brief, from source retrieval through framing, drafting, official-format Word rendering, and page-by-page visual verification.
description_en: >-
  A six-stage pipeline for policy analysts and government-affairs writers: source and verify original policy texts, build a four-tier policy framing, draft the outline, write the body, render a GB/T 9704-compliant Word file, and visually verify every page.
version: 1.0.0
category: professional
sub_categories:
  - key: pro-gov
    name: Government Documents
tags: [policy brief, official document, policy research, policy framing, Word formatting]
tags_en: [policy brief, official document, policy research, Word formatting, government affairs]
icon: 🏛️
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [write a policy brief, policy brief, official document, situation report, policy framing, source register, official Word format, policy retrieval, citation check]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "2.99"
---

# PolicyForge — Policy Brief Intelligence

A six-stage pipeline that turns a one-line assignment into a submission-ready policy brief: source and verify the original texts, stack the policy framing, fix the outline, write the body, render a Chinese official-format Word file, and inspect the rendered pages before delivery.

## What It Is

- **The problem it solves.** Assignments usually arrive as one sentence: write a brief on a business line, for a superior body. There is no outline, no named source document, and no agreed length. Most rework is not a writing problem; it is a sequencing problem. Drafting the outline first and hunting for citations afterwards leaves every section unable to hang on a real document, and the whole draft gets rebuilt. This skill inverts the order: sources decide the framing, the framing decides the structure, and the structure decides the length.
- **What you get.** One official-format `.docx` main file (A4, FangSong at 16pt, fixed line spacing, page numbers, appendix table) plus three companions: a Policy Source Register, a Placeholder Register, and a Verification Record.
- **How it differs from asking a general model.** Every citation must resolve to a four-part tuple of document number, issue date, issuing body, and official link, or it goes on a pending-verification list instead of being smoothed into a plausible-sounding sentence. The structure is derived from the framing rather than from a map. Business figures are always red placeholders with a note on where to collect them. And no `.docx` counts as delivered until its pages have been rendered and inspected.
- **Why a fixed pipeline pays off.** These documents recur across business lines: the same framing and skeleton rerun with a different subject. Fixing the retrieval rules, structural tests, typographic parameters, and acceptance list once is far cheaper than rediscovering them each time.
- **Who it is for.** Office writing staff in government and public institutions, research and general-affairs roles in state-owned enterprises and financial institutions, policy analysts, and business-line staff who draft on behalf of a principal.

## When to Use

1. I have to write a progress brief on a business line and the only input is a subject line, with no instruction on sections or ordering.
2. I need to attach the material to a policy frame but cannot tell which tier of document to cite, or how many are enough for one tier.
3. I want verbatim excerpts I can paste straight into the body, not a paraphrase saying the document stressed the importance of the work.
4. I want sections organized by business line rather than by region, but the only data I was given is regional.
5. I need a Word file whose fonts, sizes, spacing, and page numbers are correct enough to print and submit as-is.
6. I want a pre-submission self-check: which citations still lack a document number, which figures are still blank.
7. I have to convert an existing report into brief structure, keeping the facts and rebuilding the skeleton.
8. I want a procedure a new colleague can follow, rather than knowledge passed along by word of mouth.

What these scenarios share: **the input is incomplete and the output must be formal**. The pipeline therefore runs sources first and figures second, and any missing piece lands visibly as a placeholder or a pending-verification entry instead of a guess.

## When NOT to Use

- You have no first-hand material and just want the model to "sound authoritative" — build a retrieval checklist with `references/policy-retrieval.md` first.
- You need an officially stamped document number: this skill produces content and layout skeletons only.
- The material is classified or contains unredacted personal data: stop and escalate.
- You need a forecast of when a policy will land: only signals to watch, no dates.

## Quick Reference

| Situation | Use |
|---|---|
| Scattered source material | `references/policy-retrieval.md` |
| Framing level does not match the audience | `references/hat-framework.md` |
| You only want the skeleton | `references/brief-template.md` |
| Need a formatted `.docx` | `references/gongwen-format.md` + `scripts/make_gongwen_docx.py` |
| Pre-delivery self-check | `references/quality-checklist.md` |

## Inputs and Outputs

### Input fields

| Field | Required | Notes |
|---|---|---|
| Subject | Yes | One sentence on the business and the addressee; if vague, pin down both |
| Document type | Yes | Brief, report, situation report, study, or work priorities; sets skeleton and length |
| Reporting level | Yes | To a superior body, to internal leadership, or peer exchange; sets framing height |
| Your role in the chain | Yes | Underwriter, co-organizer, agent channel, administrator, or supervised party |
| Available data | No | By year, business line, or institution; anything missing becomes a placeholder |
| Length preference | No | Default 6,000-8,000 characters (10-13 pages); a 4,000-character short form is available |
| Citation and search limits | No | Default: prioritize documents from the last quarter; 10-15 keywords, 3-4 fallback queries |
| Phrases to avoid | No | Wording or definitions that must not appear in the body or the appendices |

### Output files

Four files in one named folder. Preview PDFs and PNGs go into `_preview/` inside it and are deleted before delivery.

- `policy-brief.docx` - official-format main file, six chapters plus appendix, 6,000-8,000 characters, roughly 10-13 pages at 600 characters per page; the rendered page count is authoritative.
- `policy-source-register.md` - source table (number, title, document number, issue date, issuing body, link, citation value), verbatim excerpts grouped by document, a pending-verification list (what is missing and which channel normally holds it), and a search trail (channel, query, hit count).
- `placeholder-register.md` - every `[FILL: ...]` and `[DRAFTING NOTE: ...]` grouped by chapter, each with the line that owns the figure.
- `verification-record.md` - forecast versus rendered page count, page-sample findings, font fallbacks, and open items with their resolution.

### Chapter allocation (default 6,000-8,000 characters; about 600 characters per page)

| Chapter | Share | Characters | Content |
|---|---|---|---|
| 1. Policy background | 15%-20% | 1,000-1,500 | The framing zone, highest tier first, opening lands on the top tier |
| 2. Progress | 55%-60% | 3,500-4,500 | Split by business line; each section runs requirement, situation, gap |
| 3. Compliance and risk control | 10%-15% | 700-1,100 | Direct constraints from documents in force; its own chapter |
| 4. Problems | 8%-10% | 500-750 | Shortfalls stated up front, with definitions and structural causes |
| 5. Next steps | 8%-10% | 500-750 | One measure per problem, executable and assessable |
| 6. Support requested | 3%-5% | 200-350 | What is needed and who acts |
| Appendix: source register | Not counted | 1-3 pages | Table on a new page, header row repeating |

## Workflow

Six steps, each with five fields. The order is not optional, and step 1 cannot be deferred. Steps 5 and 6 need Python 3.9 or later and `python-docx`; visual verification additionally needs Microsoft Word on Windows, `pywin32`, and `PyMuPDF`, and degrades to parameter-only self-check if any of the three is missing.

### Step 1 - Retrieve and verify the original texts (sources before structure)

- **Do**: search in the order given in `references/policy-retrieval.md` - the gov.cn policy library through `scripts/gov_doc_search.py`, then provincial portals and departmental columns, then municipal re-postings for full text, then a search engine as fallback. For each retained document record the four-part tuple and lift one to three verbatim sentences that can be cited directly.
- **Keyword matrix**: search short terms, never a full sentence. One term pulls a whole cluster, so about a dozen rounds cover two years of a field. Rotate across four dimensions - sector and business line, business object, policy theme, action or instrument - using terms such as implementation plan, guiding opinion, administrative measures, pilot, special campaign.
- **Produce**: a first draft of the source register with the table, verbatim excerpts, pending list, and search trail.
- **Pass test**: every planned chapter maps to at least one citable passage; at least three of the four framing tiers hold a real document; anything available only as a re-posting sits on the pending list.
- **If it fails**: a zero result usually means a bad parameter, so switch to a valid library type and drop the field restriction for full-text search. If that still returns nothing, locate the URL through a fallback search, fetch the body, and confirm the page title. If three rounds produce nothing, mark the chapter pending; a paraphrase never substitutes for a quotation.
- **Common errors**: citing a municipal re-posting as the original; concluding a document does not exist because a parameter was wrong; searching with a long sentence instead of short terms.

### Step 2 - Fix the policy framing

- **Do**: stack five tiers from high to low as described in `references/hat-framework.md` - overarching document, main framework (including the 1+N closure check), domain-specific documents, local implementation, and compliance floor. The opening paragraph must land on the highest tier and quote its core formulation and time horizon.
- **Produce**: a one-page framing map: tier, document and usable sentence, planned chapter.
- **Pass test**: the opening names a specific document; domain documents map one-to-one onto body sections; local implementation prefers a government work report or equally authoritative text; a compliance floor, if one exists, gets its own chapter rather than a line under next steps.
- **If it fails**: when a tier genuinely has no document, merge it with a neighbouring tier and record the gap in the register. Never invent a document number or a formulation to fill the tier.
- **Common errors**: stacking three or more citations in one paragraph; framing tiers that do not match the chapters; presenting an industry commonplace as quoted text.

### Step 3 - Fix the outline and the length split

- **Do**: build the main axis from the policy or business dimension - business line, insurance line, or domain - and let region appear only as a closing example or a single comparison. Allocate by tier: each must-cover domain gets a section, emerging documents get half a section, local distinctives merge into one or two sections, and compliance stands alone.
- **Produce**: a chapter outline carrying character counts and, after each section heading, the source IDs it draws on.
- **Pass test**: no administrative division appears in a first-level heading; every heading maps to a policy requirement; the problems chapter states shortfalls; compliance has its own chapter.
- **If it fails**: when only regional data exists, keep the business-line axis and demote the regional figures to a closing comparison, recording the missing dimension in the placeholder register.
- **Common errors**: organizing by map so that every section reads as a travelogue; burying compliance requirements inside next steps.

### Step 4 - Write the body with placeholders

- **Do**: run each section through requirement, situation, gap. One conclusion takes one strongest citation. Business figures become `[FILL: ...]`; missing data becomes `[DRAFTING NOTE: ...]`. Confirm your organization's role in the chain before writing a single verb.
- **Produce**: the full marked-up body plus the placeholder register.
- **Pass test**: no invented figures; every judgment traces to a citation; placeholders are greppable and match the register line for line; no status markers in the body.
- **If it fails**: keep the placeholder and the drafting note rather than deleting the paragraph or estimating a number; downgrade unsupported conclusions to pending or drop them.
- **Common errors**: writing a co-organizer as an underwriter; mixing reference years across scale and structure metrics; padding length by restating source text.

### Step 5 - Render the official-format Word file

- **Do**: write the body in the markup the script expects and run `python scripts/make_gongwen_docx.py source.md output.docx`. The script prints the font choices and the character/page forecast before rendering; parameters are in `references/gongwen-format.md`.
- **Produce**: `policy-brief.docx` with a page-number field and an appendix that starts on its own page.
- **Pass test**: A4 with correct margins; the four text levels match the parameter table; line spacing is exact; page numbers read as an en dash, the number, and an en dash; the appendix header repeats across pages; placeholders render in red.
- **If it fails**: fall back along the font chain and record the substitution; on a script error, first check for mixed heading markers in the source; if the rendered page count misses the forecast by more than three pages, adjust length rather than squeezing the font.
- **Common errors**: setting only `run.font.name` so Chinese still renders in the default Song face; leaving the page at Letter; setting exact spacing without a point value.

### Step 6 - Verify visually and deliver

- **Do**: run `python scripts/verify_docx_render.py output.docx` to produce a PDF and per-page PNGs. Sample five representative pages - title page, table-heavy page, placeholder page, appendix page, final page - walk the list in `references/quality-checklist.md`, then delete `_preview/`.
- **Produce**: `verification-record.md` plus the four cleaned deliverable files.
- **Pass test**: all five page samples pass; no tofu boxes or mojibake from font fallback; tables stay inside the margins; page numbers are present; Word's own count is within two pages of the forecast.
- **If it fails**: return to step 5, change the parameter, re-render. Never deliver a `.docx` nobody has looked at. Without Word available, degrade to parameter-only self-check and state plainly in the record that visual verification was not performed.
- **Common errors**: reviewing Word without reviewing the PDF; sampling only the title page; shipping the preview folder.

## Output Format

```
Title (a claim, not "Report on ...")
Lead: one-line conclusion + scope
1. Situation (upper-level requirement / local reality / trend)
2. Problems and causes (symptom -> data -> cause)
3. Recommendations (action -> owner -> deadline -> acceptance)
Risks and assumptions
Sources (traceable; never "it is understood that ...")
```

## Quality Gates

Tick every line before delivery. Any failure blocks submission, and the bracketed action is what to do on the spot.

- [ ] **Citations traceable**: each has document number, issue date, issuing body, and official link, or sits on the pending list with what is missing and which channel holds it. *If not:* downgrade to pending wording and drop the number; no half-citations.
- [ ] **No invented figures**: all business data are `[FILL: ...]`, matching the placeholder register, with no estimates. *If not:* replace each with a placeholder and add the collection owner to the register.
- [ ] **Framing complete**: at least three of four tiers hold real documents and gaps are recorded; the opening lands on the top tier. *If not:* run one more check for recent documents, then merge tiers and record the gap rather than inventing a file.
- [ ] **Structure compliant**: no administrative division in first-level headings; compliance has its own chapter; problems are stated. *If not:* demote regional material to closing examples and lift compliance out of next steps.
- [ ] **Single strongest source**: no more than three citations under one conclusion. *If not:* keep the strongest, move the rest to the appendix table.
- [ ] **Role accurate**: your position in the chain is confirmed and used consistently, and no co-organizer is written as an underwriter. *If not:* re-confirm the input field and replace the affected verbs and subjects throughout.
- [ ] **Clean body and clean folder**: no status markers or source notes in the body; no temporary files or machine-specific absolute paths in the deliverable folder. *If not:* move status notes into the register or the record, delete temporary files.
- [ ] **Typography on spec**: A4, margins, four text levels, exact spacing, page-number field, appendix on a new page, repeating header row. *If not:* return to step 5 and re-render with a note on the difference.
- [ ] **Visual check done**: five page samples pass with no overflow, mojibake, or boxes; page count within two pages. *If not:* isolate the page and element, fix, and rerun the check rather than skipping pages.
- [ ] **Version confirmed**: the current edition numbers of the document-handling regulation and the format standard have been checked by a human, with the conclusion and date in the record. *If not:* mark the version as pending and use wording that carries no edition number.

## Scope and Limits

- **No privileged retrieval.** It does not connect to internal document systems and does not read unpublished transmittals or classified files; it works from publicly available text and puts the rest on a pending list.
- **No fabrication.** When verbatim text is unavailable it writes no plausible-looking clause or document number, and it does not rule on whether a policy remains in force; it supplies the verification path instead.
- **No invented business data.** It does not estimate volumes, institution counts, or ratios; it leaves a placeholder and a collection note.
- **No outcome guarantee.** It does not promise approval or adoption; it promises a reproducible process, checkable gates, and traceable sources.
- **No sensitive material.** Classified content or third-party personal information should move offline; the skill neither accepts nor retains it.
- **No other formats.** Slide decks, social-media layout, and chart styling are out of scope; you get the body text and the skeleton.

The bias behind all six: a visible gap is safer than a convincing sentence nobody can trace back.

## Common Traps

- **Framing above the evidence**: grand directives with no local data get rejected on first read.
- **Retelling instead of judging**: end every section with "so what we should do".
- **Numbers without a statistical basis**: give the basis or mark as "to be verified".
- **Writing advice as a decision**: use "recommend / consider", state preconditions.

## Delivery Example

**Input (three lines)**

- Subject: annual progress on one business line, addressed to a superior body.
- Type: brief, about 6,000 characters.
- Data: regional completion figures only; no breakdown by business line.

**Output skeleton (excerpt)**

```text
Title: Report on progress in [FILL: XX] business
Subtitle: [FILL: submitting unit]   [FILL: date]

1. Policy background
   (a) National tier: top document, quote the core formulation [S01]
   (b) Main framework: is the 1+N set closed? cite by tier [S02-S03]
   (c) Local implementation: government work report wording [S04]
   (d) Compliance floor: direct constraints in force [S05]
2. Progress (by business line; one regional comparison closes each section)
   (a) [Business line A]: requirement -> [FILL: volume A] -> gap
   (b) [Business line B]: requirement -> [FILL: volume B] -> gap
3. Compliance and risk control
4. Problems (shortfalls stated, including scale-versus-structure definitions)
5. Next steps
6. Support requested
Appendix: source register (table, new page)
```

**Three companions.** The source register carries five tuples, one flagged pending with the channel to check, plus a four-line search trail; a work report in that table carries no document number, which is normal, so the year and session are recorded instead. The placeholder register lists twelve `[FILL: ...]` and three `[DRAFTING NOTE: ...]` entries by chapter with the owning line. The verification record notes a forecast of 11 pages against 11 rendered, five page samples passed, and one font substitution.

## Related Skills

- **SkillForge (paid)**: turn this method into your own reusable skill set.
- **ChartAtelier (paid)**: produce the figures a policy brief needs.

## Reference Files

- `references/policy-retrieval.md` - channel order, query forms, body extraction, and the verification trail.
- `references/hat-framework.md` - the four-tier framing, selection tests, opening patterns, and four anti-patterns.
- `references/brief-template.md` - skeletons for three document types, the three-part paragraph, placeholder rules, and language discipline.
- `references/gongwen-format.md` - typographic parameters, python-docx pitfalls, and the five-step render check.
- `references/quality-checklist.md` - the tickable acceptance list with an action for every failed line.
- `scripts/gov_doc_search.py` - library search, body fetch, sentence extraction, fallback search (standard library only).
- `scripts/make_gongwen_docx.py` - renders markup into an official-format `.docx` (requires `python-docx`).
- `scripts/verify_docx_render.py` - Word to PDF to PNG page sampling (requires `pywin32`, `PyMuPDF`, and Word).
