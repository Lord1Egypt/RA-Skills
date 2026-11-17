# wikidata — structured facts via SPARQL

## What this source has

Wikidata is the structured-data sibling of Wikipedia. Every "thing" (person, place, work, concept) is a Q-entity (`Q42` = Douglas Adams), every property is a P-entity (`P31` = "instance of"). 100M+ items, multilingual, machine-readable. Updated continuously.

Two surfaces:
1. **SPARQL endpoint** (`https://query.wikidata.org/sparql`) — full graph queries. The most expressive way to ask "what cities in California with population > 1M and a beach?"
2. **Entity JSON** (`Special:EntityData/Q42.json`) — bulk fetch one entity's full record (labels, descriptions, claims, sitelinks).

Use Wikidata when you need structured values rather than prose: birthdates, coordinates, population counts, ISBN→OL key mappings, "list all X with property Y".

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Reach sends a User-Agent automatically. SPARQL queries that take long enough to be flagged as abusive can get the IP blocked.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 5 queries/sec; 60-second timeout per query; concurrent-request cap |

Long-running queries (>30 sec) often get killed mid-execution. Optimize with `LIMIT`, indexed properties, and the right service order.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `sparql` | Run any SPARQL query | `query` (raw SPARQL string) |
| `entity` | Fetch one entity's full JSON | `qid` (e.g. `Q42`) |

## Worked examples

```bash
# All cities in California with population > 1M
python3 scripts/reach.py query wikidata sparql '{
  "query": "SELECT ?city ?cityLabel ?pop WHERE { ?city wdt:P31/wdt:P279* wd:Q515; wdt:P131* wd:Q99; wdt:P1082 ?pop. FILTER(?pop > 1000000) SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". } } LIMIT 20"
}'

# Get the full record for Douglas Adams
python3 scripts/reach.py query wikidata entity '{"qid": "Q42"}'
```

## Response shape

- `sparql`: SPARQL JSON results format — `{head: {vars: [...]}, results: {bindings: [{var1: {type, value}, var2: {...}}, ...]}}`. Most useful is `results.bindings`.
- `entity`: `{entities: {Q42: {labels, descriptions, aliases, claims, sitelinks}}}`. Each `claim` is a list of statements with `mainsnak.datavalue`.

## Pitfalls

- **Property lookups are by P-id, not name.** "Population" is `P1082`. Use the search box at https://www.wikidata.org/ to find P-ids before writing a query.
- **`SERVICE wikibase:label`** must come *after* the data clauses, otherwise label resolution fails silently.
- **Date values** come as XSD datetimes with calendar info: `+1952-03-11T00:00:00Z`. Strip the leading `+`.
- **Coordinates** come as `Point(<lon> <lat>)` — note longitude FIRST, opposite of most other systems.
- **Federated queries** (against external SPARQL endpoints via `SERVICE`) work but multiply the timeout risk.
- **POST not GET** for non-trivial queries — Reach uses POST automatically to avoid URL-length limits.

## Source links

- Endpoint: https://query.wikidata.org/sparql
- Query examples: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
- Entity model: https://www.mediawiki.org/wiki/Wikibase/DataModel
