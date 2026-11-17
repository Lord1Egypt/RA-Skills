# Polymarket: company → topic → market → outcomes

Use --platform polymarket. Origin: Polymarket public Gamma API; the Observer
publishes a curated/discovered pre-IPO company/topic snapshot, not exhaustive
coverage or a brokerage instrument list.

Filters: --industry; --type ipo|valuation|financing|acquisition|product|operations|other;
--status current|all (default current).
Sorts: volume_desc (default), topics_desc.
The type/search filters select companies with a matching associated topic;
their displayed topTopics can still contain other topic types. Inspect detail
and select the relevant topics before answering a specific prediction question.

List items have entityType: company and companyId, not token or market ID.
Search includes company names/aliases, tags AND associated topic text. Do not
identify every hit as the searched company; check companyName and sourceEvidence.
Cards expose counts and at most three current topTopics. detail returns all
associated topics and markets, including retained closed options.

## Probability and status

outcomes preserves source-order label/price/probabilityPct. probabilityPct is
ALREADY percentage units; 0.35 price corresponds to 35 probabilityPct.
Support Yes/No and company-name options. Show every option independently;
missing probabilities are unavailable and 0 is a real displayed zero.

Do not average, add or normalize different dates, valuation thresholds or
separate markets into a “company probability”. 0%/100% alone does not confirm
settlement. Present active, closed, archived and resolutionStatus independently
rather than inferring a result from probability or trading status.

apiEndDate is API market end time, not necessarily the question's prediction
deadline. Retain original timezone, original description, resolutionSource
and settlement exceptions. titleZh/summaryZh are derived event-level content,
not a verified translation of every individual market's rules. If missing,
failed or pending, use original content and state the processing status.

## Aggregates and time

Platform summary de-duplicates by market ID and aggregates current markets:
companyCount/currentCompanyCount, topicCount/currentTopicCount,
marketCount/currentMarketCount, volume24h/volumeCoverage,
liquidity/liquidityCoverage. Do not sum company totals: one market may belong
to more than one company. List summary is platform-wide, not search-filtered.

lastSuccessfulAt dates market retrieval; lastDiscoveryAt dates topic discovery.
Preserve record fetchedAt, source updatedAt, original sourceUrl and stale.
There is no authenticated trading functionality in this skill.

    node scripts/query-preipo.mjs search OpenAI --platform polymarket --type ipo
    node scripts/query-preipo.mjs detail openai --platform polymarket
