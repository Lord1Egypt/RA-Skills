# HS Tariff Classification

**Platforms:** Claude · Openclaw · Codex
**Domain:** Trade Compliance — Customs Classification

## Purpose

A tariff-classification drafting partner for licensed customs brokers, trade-compliance analysts, importers of record, exporters, and 3PL trade desks. Walks a single product through the WCO General Rules of Interpretation (GRI 1–6) in the **strict order required by the GRI**, names the controlling section / chapter / subheading notes, and produces a DRAFT classification memo with a recommended 10-digit HTSUS code (or 8-digit EU CN / 10-digit TARIC), a CROSS / BTI ruling search list, a reasonable-care record, and an alternatives-rejected log.

## When to Use

- Classifying a new SKU before its first U.S. or EU entry / export
- Re-classifying after a 2026 EU CN update or U.S. HTSUS revision (batteries, hydrogen, renewables, advanced materials, additive-manufactured goods)
- Building the reasonable-care record CBP expects under 19 U.S.C. § 1484 for the importer of record
- Preparing the technical analysis for a CBP Binding Ruling (eRuling) or EU BTI (Binding Tariff Information) request
- Resolving composite / set / mixed-material classification with GRI 3
- Documenting the rejection of alternative headings to defend the chosen code in audit or post-entry review

## What It Does

**Phase 1: Product intake**
1. Captures importer / exporter of record, country of origin, country of import, intended use, and commercial / catalog / engineering identifiers
2. Captures the product's physical description, materials by weight / volume, function, packaging, presentation, and whether sold as a set or kit
3. Captures essential character drivers (which component gives the article its identity, function, value, or bulk)
4. Captures any prior classifications, supplier-suggested code, or competitor binding rulings the user has on file

**Phase 2: GRI walk (strict order)**
5. **GRI 1** — find candidate headings from the terms of headings and any relative section / chapter notes; record each candidate with note citations
6. **GRI 2(a)** — incomplete / unassembled goods test (only if relevant)
7. **GRI 2(b)** — mixtures and composite goods extension
8. **GRI 3(a)** — most specific description test
9. **GRI 3(b)** — essential character test (only if 3(a) does not resolve)
10. **GRI 3(c)** — last-in-numerical-order fallback (only if 3(a) and 3(b) do not resolve)
11. **GRI 4** — most akin (only if no heading applies)
12. **GRI 5(a)** — fitted cases / specially shaped containers; **GRI 5(b)** — packing materials and containers
13. **GRI 6** — subheading-level GRI, applied *mutatis mutandis* using subheading notes; U.S.: then the **Additional U.S. Rules of Interpretation** to reach the 10-digit HTSUS; EU: subheading notes + CN subdivisions to reach 8-digit CN, then TARIC measures

**Phase 3: Ruling research and reasonable care**
14. Generates a CROSS / EBTI search list with proposed query terms (product, material, function, use)
15. Records the reasonable-care steps actually taken (independent classification, ruling search, expert consultation flagged)
16. Logs an alternatives-rejected table so the audit trail shows *why* each rejected heading is wrong

## Output

A DRAFT classification memo with:

- Product identification block (SKU, description, materials, function, end use, packaging)
- GRI-ordered analysis (one section per rule actually applied, with note citations)
- Recommended classification: 10-digit HTSUS (or 8-digit CN / 10-digit TARIC) with statistical suffix
- Trade-program flags (USMCA / GSP / 301 / 232 / 201 / AD/CVD eligibility prompts)
- CROSS / EBTI ruling search list
- Alternatives-rejected log
- Reasonable-care record
- Binding-ruling recommendation (file or skip, with rationale)
- Unresolved-information list

## Safety

This skill drafts a recommendation, **not** an entry filing. Every output is labeled **DRAFT — LICENSED CUSTOMS BROKER / TRADE-COMPLIANCE REVIEW REQUIRED**. The skill never files a CBP entry, never transmits ACE / AES data, never opines on AD/CVD scope rulings, never opines on country-of-origin marking disputes, and never substitutes for a Binding Ruling. Reasonable-care liability rests with the importer of record under 19 U.S.C. § 1484; the skill records the steps taken but does not assume that liability. Section / chapter / subheading note text must be supplied by the user or verified against the official HTSUS / CN; the skill never invents note language.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
