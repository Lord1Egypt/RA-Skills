# CHANGELOG

## [2.7.0] - 2026-04-03

### Changed
- Briefing output format: plain text/HTML for Gmail rendering, no markdown syntax
- Section markers: monochrome extended characters (▪ ✉ ⚑ ◈ ⟡ ⚙) replace color emoji headers
- Weather: narrative format with emoji directly before condition words, includes 10am/4pm commute forecasts, Friday weekend forecast
- Greeting: "Good morning Jared" / "Good evening Jared", no trailing punctuation
- Links: inline anchor text on relevant words (gcal, maps, gmail thread URIs), no trailing link labels
- Markets: morning shows previous close with change, evening shows open-to-close with change
- Silence on normal: empty sections omitted entirely, no "no flags" or normalcy confirmations
- ContentItem schema: `artifact_links` replaced with `inline_links` array (text, uri, uri_type)
- BriefingSection schema: `emoji_header` renamed to `section_marker`

### Added
- Vibes (ocas-vibes) cooperation: reads voice identity and anti-AI rules when present
- Silence-on-normal behavior constraint
- Weather emoji mapping table in briefing templates
- Link URI pattern reference (gcal, maps, gmail, status)

## [2.6.0] - 2026-04-02

### Added
- Structured entity observations in journal payloads (`entities_observed`, `relationships_observed`, `preferences_observed`)
- `user_relevance` tagging on journal observations (`user` for calendar/task entities, `agent_only` for external news context)
- Elephas journal cooperation in skill cooperation section

## 2.4.1 — 2026-03-30

### Added
- Ontology mapping: Vesper explicitly documented as aggregation-only, no entity extraction

### Changed
- Rally cooperation entry: clarified as cooperative read (Vesper reads daily report file)
- Dispatch cooperation entry: clarified as Vesper-initiated session-scoped request

## Prior

See git log for earlier history.
