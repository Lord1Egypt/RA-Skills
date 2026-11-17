---
name: health-provider-research
description: Find and compare public physician, hospital, pharmacy, urgent-care, and group-practice directory records through Crawlora Healthgrades. Use for a provider shortlist, specialty/location discovery, or directory and review evidence; confirm insurance and appointments with the provider.
---

# Health provider directory research

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Build a source-attributed provider or facility shortlist from public Healthgrades
records. Directory labels, awards, and patient reviews are evidence to inspect,
not a clinical recommendation or a verified measure of care outcomes.

## Discover and match directory records

- Establish location/radius, specialty, language, facility type, and practical
  preferences. Use `healthgrades_specialties`, location search, and autocomplete
  to resolve the request; do not infer a specialty from symptoms or choose a
  treatment. No diagnosis is part of directory research.
- Fetch physician filters for the exact query/location before using clinical-focus,
  hospital, insurer, or language codes. Insurance plan IDs require their insurer;
  codes from an unrelated query are not automatically valid choices.
- Keep physician search separate from facility search. Facilities require a
  documented type (`hospital`, `pharmacy`, `group_practice`, `urgent_care`) and
  location; fetch that search's filters before narrowing its results. Hospital
  award filters are their own discovery surface, not physician-search filters.
- Resolve a returned canonical physician/facility/hospital URL before detail.
  Match name, address, specialty, and affiliation to distinguish people with
  similar names and multiple office locations. Keep offices separate in the
  appointment shortlist without double-counting the clinician.
- Bound pagination and retain the exact query, filters, collection time, and
  source URL. For health-topic/article context, attribute the publisher and date;
  it does not validate an individual's diagnosis, safety, or treatment choice.

```sh
scripts/crawlora.sh /healthgrades/specialties
scripts/crawlora.sh /healthgrades/locations term="Boston, MA"
scripts/crawlora.sh /healthgrades/physicians/filters query="cardiology" where="Boston, MA"
scripts/crawlora.sh /healthgrades/physicians/search query="cardiology" where="Boston, MA" page=1
# Follow a returned URL for detail:
# scripts/crawlora.sh /healthgrades/physician url="$PHYSICIAN_URL"
```

## Deliver an evidence-based shortlist

Show identity, office/location, specialty, stated affiliation, public contact
channel, relevant directory attributes, source/date, and unresolved questions.
Attribute ratings, reviews, and awards with their sample/population and scope;
missing or low review counts are not evidence of poor care. An insurer/plan
label or availability filter is not confirmation of network coverage, current
appointments, acceptance of new patients, or out-of-pocket cost. Mark those as
needing confirmation with the office/insurer. Keep clinical preference and
eligibility questions open rather than producing an unsupported quality rank.
Do not book, contact a provider, or submit patient/insurance information unless
the user requests it.
