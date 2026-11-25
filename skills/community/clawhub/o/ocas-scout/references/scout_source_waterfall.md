# Scout Source Waterfall

## Intent

Research should exhaust free, low-friction sources before escalating. This reduces cost, respects rate limits, and ensures paid sources are used only when they add genuine value.

## Tier 1 — Public Sources (Automatic)

Sources: public web search, official websites, reputable news outlets, public filings (SEC, state registries), public social profiles (LinkedIn public view, Twitter/X, GitHub).

Behavior: runs automatically on every research request. No permission required.

Minimization: collect only what the goal requires. Do not harvest all available data.

### Tier 1 Person-Specific Tools

These are run automatically when the relevant input data is available. See
`references/scout_person_sources.md` for the full tool list and usage.

**Always run (person research):**
- **theHarvester** — gathers names, emails, subdomains from 40+ public sources. Run on every person research request.

**When handles/usernames known:**
- **Sherlock** — username check across 400+ sites (already integrated)
- **Maigret** — deep username enumeration across 3000+ sites. Run if Sherlock returns < 3 verified profiles.

**When email known:**
- **Holehe** — discovers which sites the email is registered on
- **h8mail** — searches 20+ breach databases locally
- **Ghunt** — if email is Gmail (reveals Google Maps, Photos, YouTube)
- **EmailRep** — email risk/reputation scoring (no API key needed)

**When phone known:**
- **PhoneInfoga** — carrier, location, line type (no API key needed)

**Always run (sanctions screening):**
- **OpenSanctions** — sanctions and PEP check

**Tier 1 tool execution order (parallel where possible):**

```
1. theHarvester (domain/email)     } parallel
2. OpenSanctions (sanctions)        }

3. Sherlock (username)             } parallel (if handles known)
4. Holehe (email → accounts)       } parallel (if email known)
5. h8mail (breach check)           }
6. EmailRep (email risk)           }
7. Ghunt (Google account)          } if Gmail

8. PhoneInfoga (phone)             } if phone known

9. Maigret (deep username)         } if Sherlock < 3 verified (Tier 1 escalation)
```

### Platform Search via Sift

Tier 1 benefits from Sift's shared search stack, which runs **agent-reach** platform search in parallel with web providers (Brave/DuckDuckGo). When Scout delegates web search queries, results automatically include platform-native content from Twitter/X, Reddit, LinkedIn, GitHub, Weibo, WeChat Articles, Bilibili, YouTube, and more.

See Sift's `references/search_tiers.md` for the full parallel execution model and deduplication logic.

Benefits:
- Broader OSINT coverage across social platforms
- Platform-native content not indexed by general search
- No additional latency (parallel execution)
- Shared infrastructure — improvements to Sift's search benefit all skills

### Tier 1.5 — Public Records Investigation (Company/Org Research)

For company/org research or when person research reveals corporate ties, run public-records fetch scripts. All scripts use Python stdlib only — zero install. Most sources work without API keys.

**Always run (company/org research):**
- **OpenCorporates** — global corporate registry (130+ jurisdictions). Free token required (`OPENCORPORATES_API_TOKEN`).
- **OFAC SDN** — sanctions screening. No key needed.
- **Wikipedia/Wikidata** — narrative bio + structured facts. Set `HERMES_OSINT_UA` per Wikimedia policy.
- **GDELT** — global news monitoring. No key needed.

**When subject is a public company or known officer/director:**
- **SEC EDGAR** — corporate filings (10-K, 10-Q, 3/4/5). Set `SEC_USER_AGENT` per SEC fair-use policy.

**When subject is a government contractor:**
- **USAspending** — federal contracts, grants. No key needed.

**When subject has lobbying ties:**
- **Senate LD-1/LD-2** — lobbying disclosures. Token optional (`SENATE_LDA_TOKEN` raises rate limit).

**When litigation history needed:**
- **CourtListener** — federal + state court opinions. Token optional (`COURTLISTENER_TOKEN` raises rate limit).

**When offshore ties suspected:**
- **ICIJ Offshore Leaks** — offshore entities, beneficial ownership. ~70 MB download on first run, cached 30 days.

**When NYC property records needed:**
- **NYC ACRIS** — deeds, mortgages, liens. No key needed.

**When recovering dead URLs or historical context:**
- **Wayback Machine** — web archives. No key needed.

**Execution order:** See `references/scout_public_records.md` for parallel execution groups, cross-reference keys, and timing correlation.

**Entity resolution:** After fetching, run `entity_resolution.py` to cross-link entities between public-records CSVs and person-tool findings. Three match tiers: exact (high), fuzzy (medium), token_overlap (low).

**Timing correlation (optional):** Run `timing_analysis.py` to test whether event time series cluster suspiciously (e.g., lobbying filings near contract awards). Permutation test, one-tailed p-value.

**Evidence chain:** Run `build_findings.py` to produce structured findings JSON with `id, title, severity, confidence, summary, evidence[], sources[]`.

### Tier 1.5 — RapidAPI Social Enrichment (Structured APIs)

After Tier 1 free tools and platform search, but before Tier 2 expensive tools, use RapidAPI to get **structured profile data** from social media platforms. This is especially useful when:
- A username/handle is already known from Tier 1 results
- Email or phone is known and social profiles need enrichment
- Company/organization LinkedIn data is needed

RapidAPI runs **in parallel** with Tier 1 tools when enrichment data is available (known handles, emails, phones).

**RapidAPI reference:** `~/.hermes/references/rapidapi/ocas-mapping.md`

### Tier 2 — Extended Sources (Config-Gated)

Sources: rate-limited APIs, business registries, extended public datasets, professional directories, MCP-discovered servers.

Behavior: runs only if `waterfall.enabled_tiers` includes 2 AND the Tier 1 results are insufficient for the goal.

Escalation criteria: Tier 1 produced fewer than 3 findings, or key identity questions remain unresolved.

### Tier 2 Person-Specific Tools

- **Social Analyzer** — 1000+ site username check (slow but broad)
- **Blackbird** — 600+ site username check with AI false-positive reduction
- **LeakCheck / LeakIX** — extended breach database search
- **Numverify** — international phone validation
- **FaceCheck.ID / Socialcatfish** — face search (when photo available)
- **FamilyTreeNow / VoterRecords** — US public records
- **OnionClaw** — Tor dark web search (12 engines, .onion fetch, circuit rotation, Robin pipeline). Preferred dark web tool. Requires Tor.
- **Robin** — alternative dark web OSINT (requires Tor + LLM)
- **MCP-discovered servers** — dynamically discovered OSINT MCP servers matching research needs (see `scout_mcp_discovery.md`)

## Tier 3 — Paid Sources (Permission-Gated)

Sources: paid OSINT providers, background check databases, premium data services, paid MCP servers.

Behavior: requires both config enablement AND explicit user permission grant recorded as a PermissionGrant.

Escalation criteria: Tier 1 and Tier 2 insufficient, and the research goal explicitly requires deeper investigation.

Hard stop: if no PermissionGrant exists, Tier 3 does not execute. The brief notes that further sources are available but not authorized.

### Tier 3 Person-Specific Tools

- **Pipl** — professional identity resolution
- **Spokeo** — US people search
- **BeenVerified** — background check
- **IntelX** — dark web + leak search (paid tier)
- **Twilio Lookup** — caller name lookup (~$0.01/call)
- **Social Links API** — email/phone/social profiling (paid per request)

## When to Stop

Stop escalating when:
- The research goal is satisfied
- Additional tiers are unlikely to add material value
- The time budget is exhausted
- The user has not granted permission for the next tier
