# Scout Brief Template

## Format

Briefs are Markdown documents with the following structure.

## Required Sections

### Executive Summary

2-4 sentences. What was researched, key conclusion, and confidence level.

### Identity Resolution Notes

How the subject was identified. Aliases considered. Ambiguities noted. State clearly if resolution is incomplete.

### Findings

Organized by category (professional background, organizational affiliations, public activity, notable events). Each finding includes the claim, confidence level, and source citation.

### Public Records

When public-records investigation was run, include a dedicated section with sub-sections for each source that returned results:
- **Corporate Filings** (SEC EDGAR) — key filings, material events, insider transactions
- **Government Contracts** (USAspending) — contracts awarded, amounts, agencies
- **Lobbying Disclosures** (Senate LD-1/LD-2) — clients, registrants, issues lobbied, income/expenses
- **Sanctions** (OFAC SDN) — whether subject appears on sanctions lists
- **Offshore Leaks** (ICIJ) — offshore entities, beneficial ownership connections
- **Property Records** (NYC ACRIS) — deeds, mortgages, liens matching subject
- **Corporate Registry** (OpenCorporates) — incorporation details, officers, filings
- **Litigation** (CourtListener) — court opinions, dockets involving subject
- **Web Archives** (Wayback Machine) — historical captures of subject's web presence
- **Knowledge Base** (Wikipedia/Wikidata) — structured facts, corporate hierarchies
- **News Monitoring** (GDELT) — global news coverage, sentiment trends

Each public-records finding includes the specific record (with date, amount, or other key data), source URL, and normalized entity name used for matching. For entity resolution cross-links, state the match tier (exact/fuzzy/token_overlap) and confidence.

If timing correlation was run, include the permutation test results with p-value and interpretation. Clearly state that statistical significance does not establish wrongdoing.

### Risk and Uncertainty

What could not be confirmed. Where confidence is low. What the brief does not cover.

### Source Log

Complete list of sources consulted with URLs and retrieval timestamps. Organized by tier.

## Tone

Concise, executive-useful. State facts directly. Flag uncertainty explicitly. No narrative padding. No speculation presented as fact.

## Length

Target: 300-800 words for a standard brief. Longer for complex multi-entity investigations.
