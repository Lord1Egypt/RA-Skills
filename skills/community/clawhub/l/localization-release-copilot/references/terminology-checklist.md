# Localization Release Copilot — Terminology & Release Checklist

Use this as the LLM step's working checklist when reviewing a source → target pair.

## A. Pre-flight (before diffing)
- [ ] Confirm the target is a true translation/adaptation of the source (same document, two languages), not two related-but-different docs.
- [ ] Identify source language and target language.
- [ ] Load any supplied glossary; if none, infer locked terms from the source (product names, framework names, branded metrics, units).

## B. Number integrity (locale-aware)
- [ ] Extract every number + unit from source and target.
- [ ] Normalize: 亿→×1e8, 万→×1e4, B/billion→×1e9, M/million→×1e6, K/thousand→×1e3.
- [ ] Equivalent pairs are MATCHES, not errors: `8.3亿`≈`830M`, `117亿`≈`€11.7B`, `1.5亿`≈`€150M`.
- [ ] Any source number with NO locale-equivalent in the target → P0 (missing data).

## C. Proper-noun & entity integrity
- [ ] Product names, org names, person names, framework names present in source must appear in target.
- [ ] Acronyms: if source uses "AI Native", target must not silently become "AI-native" inconsistently across files (track, P2 unless branded).

## D. Source attribution preservation
- [ ] For every `(Org, Year)` / `Org (Year)` in the source, the target retains BOTH org and year.
- [ ] Dropping the org name OR the year → P1.
- [ ] Changing the year (e.g. 2024 → 2026) without source basis → P1.

## E. Glossary compliance
- [ ] Every `mandatory: true` glossary term appears in the target exactly as specified.
- [ ] Violation → P1.

## F. Structure loss (claim-level, not section-level)
- [ ] Map source sections to target sections.
- [ ] Flag only structure loss that DROPS A CLAIM (a fact, a data point, a named entity narrative).
- [ ] Legitimate condensation (LinkedIn/Substack shorten a section) is P2 at most, not an error.

## G. Reviewable preview
- [ ] Summary: source → target(s), pass count, attention count.
- [ ] Line-level diff for each P0/P1: source sentence → target sentence → suggested fix (no auto-apply).
- [ ] Glossary-compliance block.
- [ ] Gate: **blocked** (any P0) / **needs review** (any P1) / **clear**.
