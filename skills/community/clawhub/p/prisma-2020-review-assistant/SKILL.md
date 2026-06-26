---
name: prisma-2020-review-assistant
description: Review, audit, coach, and extract PRISMA 2020 reporting compliance for systematic reviews, meta-analyses, protocols, reviewer comments, and draft manuscript sections. Use when checking a draft against PRISMA 2020, building a PRISMA checklist table, locating evidence for checklist items, explaining what a PRISMA item requires, or revising a review section to improve reporting completeness.
---

# PRISMA 2020 Review Assistant

Assess systematic review reporting against PRISMA 2020 and help authors close reporting gaps.

## Choose a mode

Pick the mode that best matches the request:

- **Reviewer**: check a draft and flag missing or weak PRISMA items.
- **Coach**: help the user draft or revise one section at a time.
- **Audit assistant**: produce a structured PRISMA comparison table.
- **Extractor**: build an evidence map showing where each item is addressed.

If the request is broad, start with an **audit** and then switch into **coach** mode for the missing items.

## Operating rules

- Treat PRISMA as a **reporting guideline**, not proof that the methods were good.
- Judge only from the text available. Do not assume an item is satisfied unless the manuscript states it.
- Distinguish clearly between:
  - **Reported adequately**
  - **Partially reported / unclear**
  - **Missing or not findable**
- Quote or point to the manuscript language supporting each judgment whenever possible.
- Prioritize high-impact missing items first: objectives, eligibility criteria, information sources, search strategy, selection process, data collection, risk of bias, synthesis methods, study selection results, synthesis results, limitations, registration/protocol, funding/conflicts, and data/code availability.

## Minimum inputs

Use whatever is available:

- Full manuscript draft, pasted text, or excerpts
- Supplementary files if available
- Target journal if known
- Whether the review includes meta-analysis, narrative synthesis only, or mixed methods
- Whether the user wants strict compliance, coaching help, reviewer-style critique, or a checklist table

If the user supplies only an abstract or outline, say the assessment is provisional.

## Reference files

Load these only as needed:

- `references/prisma-2020-map.md` for the practical item-by-item review map
- `references/prisma-2020-checklist-source.md` for the checklist wording extracted from the official DOCX
- `references/prisma-2020-expanded-checklist-source.md` for text extracted from the official expanded checklist PDF
- `assets/source-docs/PRISMA_2020_checklist.docx` for the original checklist source file
- `assets/source-docs/PRISMA_2020_expanded_checklist.pdf` for the original expanded checklist source file

Use `prisma-2020-map.md` first for normal reviews. Read the source extraction files when you need closer wording from the official materials.

## Reviewer mode

Use this mode for requests like:

- "Check this draft systematic review for PRISMA gaps"
- "Act like a reviewer on PRISMA reporting"
- "What am I missing before submission?"

### Procedure

1. Identify which manuscript parts are available.
2. Map visible content to PRISMA sections: Title, Abstract, Introduction, Methods, Results, Discussion, Other Information.
3. Review each relevant PRISMA item and sub-item.
4. Produce a prioritized findings list:
   - critical missing items
   - important but fixable weaknesses
   - minor completeness improvements
5. For each flagged item, include:
   - item number and short label
   - status
   - why it matters
   - evidence found or note that none was found
   - a concrete fix suggestion
6. End with a short submission-readiness summary.

### Output pattern

- **Overall PRISMA status:** strong / moderate / weak
- **Critical gaps:**
- **Section-by-section findings:**
- **Fastest fixes before submission:**

## Coach mode

Use this mode for requests like:

- "Help me structure my systematic review"
- "Walk me through the methods section"
- "What should I include under PRISMA item 13?"

### Procedure

1. Ask which section the user is drafting, unless obvious.
2. Narrow to the relevant PRISMA items.
3. For each item, explain:
   - what the section must report
   - common omissions
   - what details the author should gather
   - a simple fill-in scaffold
4. If the user shares draft text, revise it toward PRISMA-complete reporting.

### Output pattern

For each item, use:

- **What to report**
- **Questions to answer**
- **Common misses**
- **Draftable template language**

## Audit assistant mode

Use this mode for requests like:

- "Compare this manuscript against PRISMA"
- "Make an audit table"
- "Flag checklist gaps"

### Procedure

1. Build an item-by-item table.
2. Include at minimum:
   - PRISMA item
   - requirement summary
   - manuscript evidence
   - status
   - gap / action needed
3. Use sub-items separately where needed: 10a/10b, 13a-13f, 16a/16b, 20a-20d, 23a-23d, 24a-24c.
4. If location information is available, include section, page, or heading references.
5. Sort the action list by importance, not only checklist order.

### Status labels

Use one of:

- **Met**
- **Partly met**
- **Not met**
- **Not assessable from provided text**
- **Not applicable**

## Extractor mode

Use this mode for requests like:

- "Generate a reporting completeness table"
- "Extract where each PRISMA item is addressed"
- "Turn this draft into a checklist matrix"

### Procedure

1. Scan the manuscript for explicit evidence tied to each item.
2. Build a matrix with concise evidence snippets.
3. Preserve the author's wording where possible.
4. Mark unresolved items clearly instead of guessing.
5. Produce either a submission-ready checklist table or an internal candid working table, depending on the request.

## Prioritization heuristics

If time is short, check these first:

1. **Methods transparency**: items 5-15
2. **Results traceability**: items 16-22
3. **Other information / trust signals**: items 24-27
4. **Framing clarity**: items 1-4 and abstract

If the manuscript claims a meta-analysis, pay special attention to items 12, 13d-13f, 20b-20d, 21, and 22.

## Important distinctions

- Separate **information sources** (item 6) from **full search strategies** (item 7).
- Separate **selection process** (item 8) from **data collection process** (item 9).
- Separate **study risk of bias** (item 11/18) from **reporting bias due to missing results in syntheses** (item 14/21).
- Separate **results of individual studies** (item 19) from **results of syntheses** (item 20a-20d).
- Separate **limitations of the evidence** (23b) from **limitations of the review processes** (23c).
- Keep registration, protocol access, and amendments under item 24.

## Default deliverables

Unless the user asks for something else, return:

1. A short overall assessment
2. A prioritized list of missing or weak items
3. A section-by-section PRISMA view
4. A small next-step plan for revision

If the user explicitly wants a table, provide the audit/extractor matrix first and the narrative summary second.
