# Evidence and reporting method

## Evidence labels

- unverified: a search snippet, inaccessible original, unattributed claim or rumor. Useful lead; do not describe it as checked.
- attributed: the accessible source is identifiable, but primary confirmation is absent. Say who reports it.
- primary: a directly read first-party announcement, signed release, governance record, regulator filing or canonical on-chain evidence supports the specified claim. This is provenance, not an endorsement of a project's claims or finances.
- corroborated: the specified claim has primary evidence and genuinely independent support. Two press-release copies, two media articles citing the same anonymous source, or the two parties' marketing posts are not automatically independent corroboration.
- disputed: accessible sources contradict materially, or a correction/retraction changes the claim. Preserve the disagreement, source times and uncertainty.

Keep claim-level qualifications even inside an event with strong evidence. An issuer may confirm an announcement while adoption statistics remain unaudited. A blockchain transfer proves an asset movement, not beneficial ownership, intent, a trade or the merchant order it belongs to. A contract tickers/name alone does not identify an asset.

## Event identity and time

An event is a development, not an article. Stable keys can use project, change and unique reference: `ethereum-upgrade-testnet-2026-xx`, `project-governance-proposal-123`. This is an identity example, not an actual event. If a proposal changes from proposed to scheduled/executed, retain its event key. A separate new proposal gets a new key even if its title resembles an old one. Do not fuzzy-merge events based only on amount or headline similarity.

Record `published_at` for the underlying original publication, `event_at` for the scheduled/actual occurrence (as supported by the current stage) and source `checked_at` for this read. Date-only values remain date-only; do not invent midnight UTC. Clearly distinguish an upcoming event mentioned in today's news from an event that occurred today. If the source timezone is unknown, disclose it rather than forcing a timestamp into the lookback window. A feed's `updated` value is separate from `published`.

## Coverage and attention

A global brief should sample multiple relevant publishers and source types; the exact choices depend on scope and availability. The bundled list is a starter set, not exhaustive coverage. Use official project/exchange/regulator material plus independent reporting and public discussion when accessible. Expand discovery for projects absent from the list by identifying the genuine official domain from more than an unverified search ad. Avoid promotional coin lists masquerading as source directories.

Feed subscription or browsing reveals only accessible items, not the entire market. Search engines may cache results, publishers may omit timestamps and sources may be blocked in one host. State the query window, checked sources and collection gaps. Do not replace missing sources with fabricated totals.

Narratives may be summarized qualitatively from observed discussion. To quantify a change in attention, compare like-for-like source/account coverage, equal time windows, the same counting method and publication-time basis. Deduplicate syndication and report both numerator and denominator. On the first run say "observed in the sources checked"; no invented market-wide heat score, whale score or percentage growth. Source evidence strength and market sentiment are separate axes.

## Report shape

Adapt to the user. A normal brief can use:

1. Scope and cutoff, UTC; local display time if known.
2. Key changes, prioritised. For each: factual claim, event stage, publication/event date, evidence label, source link(s), possible impact and what would confirm or weaken the interpretation.
3. Updates/corrections to previously tracked events, separately from new events.
4. Upcoming sourced dates, if requested or material.
5. Coverage gaps and next observations. No claim of "nothing happened" when key sources were unavailable.

Use original paraphrases. Link to originals and use only short necessary quotations. Do not republish full articles or strip source attribution. Distinguish the user's provided artifacts from independently retrieved sources. This Skill performs research and local bookkeeping; it does not trade, publish or send messages by itself.
