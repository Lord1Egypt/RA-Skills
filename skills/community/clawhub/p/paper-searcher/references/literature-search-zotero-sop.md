# Literature Search + Zotero Import SOP

This SOP describes a disciplined workflow for academic literature search, evidence-based shortlisting, and Zotero import.

## Table of Contents

1. Pre-search assessment
2. Search planning
3. Source strategy
4. Keyword strategy
5. Search depth
6. Time window
7. Deduplication
8. Report-before-report filtering
9. Candidate field verification
10. Pre-import review list
11. Zotero import
12. Required final report

## 1. Pre-search assessment

Before searching, decide whether the user has provided enough information.

### Sufficient information: execute directly

Proceed without extra questions when the user provides most of:

- topic/direction;
- keywords or key concepts;
- year range;
- literature type;
- desired quantity;
- output goal, such as shortlist, review, Zotero import, or PDF collection.

Briefly restate the plan and start.

### Insufficient information: ask focused questions

Ask only 2–4 questions when the request is broad or likely to go off-target. Cover:

- direction/subfield;
- time range;
- literature type;
- whether to import to Zotero.

## 2. Search planning

A search plan must include:

- understood goal;
- keyword matrix;
- source list;
- source coverage limits;
- depth per keyword/source;
- time window;
- filtering criteria;
- Zotero strategy.

## 3. Source strategy

Platform bundles are starting points only. Formal execution should search individual sources where possible and record source-specific counts and errors.

### Common source groups

| Field | Useful sources | Common gaps |
|---|---|---|
| Medicine/clinical | PubMed, PMC, Europe PMC, OpenAlex, Crossref | clinical trial registries, guidelines, publisher full text |
| Biology/biomedicine | PubMed, Europe PMC, bioRxiv, medRxiv, OpenAlex, Crossref | paywalled publisher pages |
| Engineering/materials/physics | Crossref, OpenAlex, Semantic Scholar, arXiv, Google Scholar | patents, standards, publisher platforms |
| Top journals | Crossref, OpenAlex, Google Scholar, publisher/DOI pages | journal-site search may be needed |
| Chinese journals | Google Scholar, Crossref/OpenAlex if indexed, web search | CNKI, Wanfang, VIP, journal sites |
| Humanities/education | OpenAlex, Crossref, Google Scholar, ERIC/JSTOR if available | CNKI/Wanfang/VIP and local journals |

### Direct vs indirect coverage

`paper-search` public sources do not directly replace Web of Science, SpringerLink, ScienceDirect/Elsevier, CNKI, Wanfang, VIP, JSTOR, or ERIC.

Springer/Elsevier articles may appear indirectly through DOI metadata in Crossref/OpenAlex/Google Scholar, but that is not a full SpringerLink/ScienceDirect search.

Always report this distinction when relevant.

## 4. Keyword strategy

Use a keyword matrix instead of a single query.

Minimum dimensions:

1. core term;
2. abbreviation/synonym;
3. subfield/application term;
4. method/material/device term;
5. population/disease/object term when relevant;
6. review/progress/status terms when the user asks for state of the art.

Example pattern:

```text
<core term>
<abbreviation>
<core term> review
<core term> clinical trial
<method/device term> <core term>
<application term> <core term>
```

## 5. Search depth

Default formal search:

- each keyword × each source Top 10.

Expand to Top 20 when:

- deduplicated candidates are too few;
- the topic is broad;
- key subdirections are missing;
- the user asks for research progress/status.

Use Top 5 only for tool tests or quick probes. Use Top 50+ only for systematic-review-like tasks and explicitly tell the user it will take longer.

## 6. Time window

Default formal time window: recent 5 years.

Prioritize current and previous year.

Older papers should not enter the main list unless they are:

- foundational;
- highly cited;
- from a leading team/institution;
- a guideline/consensus;
- unusually aligned with the user's specific question.

When keeping older work, state the reason.

## 7. Deduplication

Deduplicate in this order:

1. DOI;
2. PMID/PMCID;
3. normalized title;
4. title + first author + year.

Prefer the most formal and metadata-complete version over preprints or duplicates.

## 8. Report-before-report filtering

Search broadly, report narrowly.

Filter out before the user-facing shortlist:

- wrong field;
- wrong scenario;
- wrong target object;
- staff/operator-focused papers when user wants patient-focused work;
- diagnostic imaging results when user wants treatment literature;
- editorials, corrections, peer-review records, news, weak conference abstracts;
- insufficient metadata;
- duplicates or near-duplicates;
- low relevance tail results.

Output tiers:

1. recommended for close reading/import;
2. relevant but secondary/temporary;
3. filtered out summary, with counts and reasons.

## 9. Candidate field verification

For each shortlist candidate, verify fields from DOI landing page, PubMed, Europe PMC/PMC, publisher page, PDF first page, or other reliable metadata sources.

Fields:

- title;
- publication/online/accepted date;
- journal/conference;
- authors;
- country/region;
- institutions/affiliations;
- DOI/PMID/PMCID/URL;
- abstract;
- literature type;
- open access/PDF availability if relevant.

If a field cannot be verified, write `not reliably identified` or `metadata unavailable`. Do not infer beyond evidence.

## 10. Pre-import review list

Before Zotero import, present a readable review list.

For each item:

```markdown
### N. Title
- Date:
- Journal:
- Authors:
- Country/region:
- Institutions:
- DOI / PMID / PMCID / URL:
- Summary:
- My judgment:
- Suggested action:
```

Include why the item is useful, whether it matches the user's direction, and whether it is worth close reading.

## 11. Zotero import

Import only after the user confirms specific items.

Before import:

1. check duplicates by DOI;
2. if no DOI, check title;
3. confirm target collection;
4. decide tags;
5. decide whether PDF upload is authorized and legal/open.

Create a `journalArticle` or other appropriate item type with:

- title;
- creators;
- abstractNote;
- DOI;
- URL;
- date;
- collections;
- tags;
- extra import note.

After import, report:

- status;
- item key;
- item version;
- collection;
- tags;
- duplicate status;
- PDF status.

## 12. Required final report

A complete final report should contain:

```markdown
## Search Plan / Actual Search
## Search Counts
## Coverage Gaps
## Filtered-out Summary
## Pre-import Review List
## Zotero Status
## Evidence Files / Commands
```

Do not overclaim. If important databases were not directly searched, say so.
