---
name: journal-matcher
description: Find and rank suitable academic journals for a manuscript using multi-source semantic matching, metrics, OA options, indexing, and predatory-risk checks. Use when the user provides a title/abstract or asks for journal recommendations / where to submit.
version: 0.1.0
author: comeingwind
license: MIT
metadata:
  hermes:
    tags: [research, academic-publishing, journal-selection, manuscript]
    category: research
    requires_toolsets: [web]   # or whatever toolsets you need
---

# Journal Matcher

## When to Use
- User pastes title + abstract (or keywords) and asks for journal suggestions
- "Where should I submit this paper?", "Find journals matching my manuscript", "Compare journal options"
- After a rejection when the user wants alternatives

## Prerequisites / Inputs
Collect (or ask for):
- Title and abstract (preferred)
- Field / keywords
- Preferences: OA required? Target quartile/IF range? Max APC? Preferred speed? Geographic focus? Article type?
- Any prior rejections or must-avoid journals

Privacy note: Prefer not storing full manuscripts long-term; process ephemerally where possible.

## Procedure
1. Normalize input (clean abstract, extract key terms).
2. Query multiple independent sources in parallel where possible:
   - JANE (jane.biosemantics.org) for biomedical
   - Publisher finders: Elsevier Journal Finder, Springer Nature Journal Suggester, Wiley, Taylor & Francis, MDPI, etc.
   - Broader tools / indexes: Paperpile-style, Web of Science / Clarivate if accessible, SCImago, Scopus sources, DOAJ
   - Semantic search / recent similar papers via web or available APIs
3. Aggregate candidates and enrich each with:
   - Scope fit / similarity rationale + example similar papers
   - Indexing (Scopus, WoS, PubMed, DOAJ…)
   - Metrics (SJR, CiteScore, JIF if relevant — present DORA-aware)
   - Reported or estimated review/acceptance timelines, acceptance rates if available
   - OA model + APC / waivers
   - Predatory-risk signals (Think.Check.Submit checklist items, known lists, red flags)
4. Filter and rank according to user preferences + quality signals.
5. Produce a clear shortlist (3–8 journals) with:
   - Ranked table or cards
   - "Why this one" explanations
   - Risks / caveats
   - Direct links to guidelines / submission
   - Suggested next actions (e.g., check special issues, prepare cover letter points)
6. Optionally offer deeper checks or a human-style "expert shortlist" rationale.

## Pitfalls & Guardrails
- Publisher tools are biased — always cross-check with independent sources.
- Acceptance rates and real timelines are often incomplete or outdated.
- Interdisciplinary work needs broader search + manual scope reading.
- Never recommend journals that fail basic legitimacy checks.
- Be transparent about data gaps.

## Verification / Acceptance
- Shortlist contains at least 3 plausible options with explicit fit reasoning.
- User can act immediately (links + clear next steps).
- Quality flags are visible.

## References / Further
- Link to key sites and Think.Check.Submit.
- (Add any local templates or example reports in references/ or templates/)
