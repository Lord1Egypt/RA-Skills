# Scout Public Records Investigation

Public-records OSINT investigation framework integrated into Scout. Government contracts, corporate filings, lobbying, sanctions, offshore leaks, property records, court records, web archives, knowledge bases, and global news. All fetch scripts use Python stdlib only — zero install.

Source: adapted from [NousResearch/hermes-agent osint-investigation](https://github.com/NousResearch/hermes-agent/tree/main/optional-skills/research/osint-investigation) (MIT).

## When to use

Run public-records investigation when:
- Subject is a **company or organization** (always)
- Subject is a **person with corporate ties** (officer, director, lobbyist, contractor)
- Research goal involves **due diligence, background checks, or "follow the money"**
- User asks about **sanctions, government contracts, lobbying, property ownership, litigation**

Do NOT run for:
- Pure person-of-interest research with no corporate/government nexus (stick to person-specific tools)
- General topic research (use Sift)

## Source selection guide

| Source | Best for | Runs when |
|--------|----------|-----------|
| **SEC EDGAR** | Public company filings, insider transactions, beneficial ownership | Company research; person is known officer/director |
| **USAspending** | Federal contracts, grants, sub-awards | Company/person is a government contractor |
| **Senate LD-1/LD-2** | Lobbying disclosures, lobbyist-client relationships | Company/person is a lobbying client or registrant |
| **OFAC SDN** | Sanctions screening | Always (sanctions check) |
| **ICIJ Offshore** | Offshore entities, beneficial ownership hidden via shells | Company/person has known offshore ties |
| **NYC ACRIS** | NYC property deeds, mortgages, liens | Subject has known NYC property addresses |
| **OpenCorporates** | Global corporate registry, officers, filings | Company research (always) |
| **CourtListener** | Federal + state court opinions, PACER dockets | Litigation history needed |
| **Wayback Machine** | Historical web captures, dead URL recovery | Always (recover dead links from Tier 1) |
| **Wikipedia/Wikidata** | Narrative bio, structured facts, corporate hierarchies | Always (context layer) |
| **GDELT** | Global news in 100+ languages, ~2015→present | Always (news context) |

## Execution order

Run in parallel where possible. Group by API key requirements:

**Group A — No API key needed (run first):**
```bash
# Sanctions screening (always)
python3 SKILL_DIR/scripts/fetch_ofac_sdn.py --out data/ofac_sdn.csv

# Wikipedia + Wikidata (always, for context)
python3 SKILL_DIR/scripts/fetch_wikipedia.py --query "<subject>" --out data/wp.csv

# Wayback Machine (recover dead URLs from Tier 1)
python3 SKILL_DIR/scripts/fetch_wayback.py --url "<url>" --match host --collapse digest --out data/wayback.csv

# GDELT news (always, for news context)
python3 SKILL_DIR/scripts/fetch_gdelt.py --query '"<subject>"' --timespan 1y --out data/gdelt.csv
```

**Group B — Corporate/registry (company/org research):**
```bash
# SEC EDGAR (if public company or known CIK)
python3 SKILL_DIR/scripts/fetch_sec_edgar.py --cik <CIK> --types 10-K,10-Q --out data/edgar_filings.csv
# Or by name:
python3 SKILL_DIR/scripts/fetch_sec_edgar.py --name "<company name>" --types 10-K,10-Q --out data/edgar_filings.csv

# OpenCorporates (global corporate registry)
python3 SKILL_DIR/scripts/fetch_opencorporates.py --query "<company>" --jurisdiction <jurisdiction> --out data/opencorporates.csv

# USAspending (if government contractor)
python3 SKILL_DIR/scripts/fetch_usaspending.py --recipient "<company>" --fy <year> --out data/contracts.csv
```

**Group C — Key-optional (run if token available):**
```bash
# Senate lobbying (SENATE_LDA_TOKEN optional, raises rate limit)
python3 SKILL_DIR/scripts/fetch_senate_ld.py --client "<company>" --year <year> --out data/lobbying.csv

# CourtListener (COURTLISTENER_TOKEN optional, raises rate limit)
python3 SKILL_DIR/scripts/fetch_courtlistener.py --query "<case or party>" --type opinions --out data/courts.csv
```

**Group D — Specialized (run on demand):**
```bash
# ICIJ Offshore Leaks (~70 MB download on first run, cached 30 days)
python3 SKILL_DIR/scripts/fetch_icij_offshore.py --entity "<company>" --out data/icij.csv

# NYC ACRIS property records
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --name "<name>" --out data/acris.csv
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --address "<address>" --out data/acris_addr.csv
```

## Cross-reference keys

After fetching, resolve entities across sources:

```bash
# Match lobbying clients against contract recipients
python3 SKILL_DIR/scripts/entity_resolution.py \
    --left data/lobbying.csv --left-name-col client_name \
    --right data/contracts.csv --right-name-col recipient_name \
    --out data/cross_links.csv

# Match OpenCorporates officers against person research findings
python3 SKILL_DIR/scripts/entity_resolution.py \
    --left data/opencorporates.csv --left-name-col officer_name \
    --right data/harvester_emails.csv --right-name-col name \
    --out data/officer_cross_links.csv
```

Three matching tiers with explicit confidence:

| Tier | Method | Confidence |
|------|--------|------------|
| `exact` | Normalized strings equal after suffix/punctuation strip | high |
| `fuzzy` | Sorted-token equality (word-bag match) | medium |
| `token_overlap` | ≥60% token overlap, ≥2 shared tokens, tokens ≥4 chars | low |

Output columns: `match_type, confidence, left_name, right_name, left_normalized, right_normalized, left_row, right_row`.

## Timing correlation

Test whether event time series cluster suspiciously (e.g., lobbying filings near contract awards):

```bash
python3 SKILL_DIR/scripts/timing_analysis.py \
    --donations data/lobbying.csv --donation-date-col filing_date \
        --donation-amount-col income --donation-donor-col client_name \
        --donation-recipient-col registrant_name \
    --contracts data/contracts.csv --contract-date-col award_date \
        --contract-vendor-col recipient_name \
    --cross-links data/cross_links.csv \
    --permutations 1000 \
    --out data/timing.json
```

Null hypothesis: event timing is independent of award dates. One-tailed p-value = fraction of permutations with mean nearest-award distance ≤ observed. Minimum 3 events per (payer, vendor) pair.

**Important:** Statistical significance ≠ wrongdoing. p < 0.05 means the timing pattern is unlikely under the null. It does not establish corruption. Always state this in the brief.

## Evidence chain construction

Build structured findings JSON:

```bash
python3 SKILL_DIR/scripts/build_findings.py \
    --cross-links data/cross_links.csv \
    --timing data/timing.json \
    --out data/findings.json
```

Every finding has `id, title, severity, confidence, summary, evidence[], sources[]`. Each evidence item points back to a specific row in a source CSV.

## API keys

| Key | Source | Effect |
|-----|--------|--------|
| `SEC_USER_AGENT` | SEC EDGAR | Required — identifies your agent per SEC fair-use policy |
| `SENATE_LDA_TOKEN` | Senate LD-1/LD-2 | Raises rate limit from 120 to 1200 req/hour |
| `OPENCORPORATES_API_TOKEN` | OpenCorporates | Required — free token at opencorporates.com |
| `COURTLISTENER_TOKEN` | CourtListener | Raises rate limit |
| `HERMES_OSINT_UA` | Wikipedia/Wikidata | Recommended — identifies your app per Wikimedia policy |

## Source reference files

Each source has a detailed reference in `references/public_records/`:

| File | Source |
|------|--------|
| `sec-edgar.md` | SEC EDGAR corporate filings |
| `usaspending.md` | USAspending federal contracts |
| `senate-ld.md` | Senate Lobbying Disclosure (LD-1/LD-2) |
| `ofac-sdn.md` | OFAC SDN sanctions list |
| `icij-offshore.md` | ICIJ Offshore Leaks |
| `nyc-acris.md` | NYC property records (ACRIS) |
| `opencorporates.md` | OpenCorporates global registry |
| `courtlistener.md` | CourtListener court records |
| `wayback.md` | Wayback Machine archives |
| `wikipedia.md` | Wikipedia + Wikidata |
| `gdelt.md` | GDELT global news monitoring |

Each reference follows a 9-section template: summary, access, schema, coverage, cross-reference keys, data quality, acquisition script, legal, references.

## Adding a new public-records source

1. Copy the template: `cp references/public_records/source-template.md references/public_records/<your-source>.md`
2. Fill in all 9 sections
3. Write a `fetch_<source>.py` script in `scripts/` using stdlib only, outputting normalized CSV
4. Update the source selection guide above
5. Update cross-reference keys if the source joins with existing sources

## Legal note

All sources are public records. Bulk acquisition is permitted under their respective access terms (FOIA, public records law, ICIJ explicit publication, OFAC public data). However:
- Some sources rate-limit aggressively. Respect their headers.
- Some redact registrant info (GDPR on WHOIS, sealed filings).
- Cross-referencing public records to identify private individuals can have ethical implications. The skill produces evidence chains, not accusations.
