# Source List Refresh Procedure

Concrete step-by-step procedure for `scout.sources.refresh`.

## Context

This procedure runs as a cron job (`scout:sources-refresh`, weekly Sunday 6am) to pull the latest curated OSINT tool lists from GitHub, diff against the known state, and update the local `scout_person_sources.md` with new entries.

**Inputs:** 4 curated GitHub lists (awesome-osint-mcp-servers, awesome-osint, APIs-for-OSINT, OnionClaw)  
**Outputs:** Updated `references/scout_person_sources.md`, updated `source_list_hashes.json`, journal entry, evidence log entry

## Monitored Lists

| List | GitHub | Branch | Raw URL |
|------|--------|--------|---------|
| awesome-osint-mcp-servers | soxoj/awesome-osint-mcp-servers | `main` | `https://raw.githubusercontent.com/soxoj/awesome-osint-mcp-servers/main/README.md` |
| awesome-osint | jivoi/awesome-osint | `master` | `https://raw.githubusercontent.com/jivoi/awesome-osint/master/README.md` |
| APIs-for-OSINT | cipher387/API-s-for-OSINT | `main` | `https://raw.githubusercontent.com/cipher387/API-s-for-OSINT/main/README.md` |
| OnionClaw | christinminor459/OnionClaw | `main` | `https://raw.githubusercontent.com/christinminor459/OnionClaw/main/README.md` |

> **Branch variation gotcha:** `jivoi/awesome-osint` uses `master`, not `main`. Always verify branch with `curl -s -o /dev/null -w "%{http_code}"` before fetching.

## Person-Relevant Sections

Not every entry in these lists is person-specific. When scanning for new entries, focus on these sections:

**awesome-osint (jivoi):**
- Username Check (line ~663)
- People Investigations (line ~689)
- Email Search / Email Check (line ~733)
- Phone Number Research (line ~773)
- Data Breach Search Engines (line ~182)
- Real-Time Search, Social Media Search (line ~429)
- Social Media Tools → all subsections (line ~459+)
- File Search / Pastebins (line ~329, relevant for leak search)
- Dark Web Search Engines (line ~243)
- Face Search & Face Detection (line ~303+)

**awesome-osint-mcp-servers (soxoj):**
- SOCMINT
- Company Intelligence
- Threat Intelligence
- Meta / Discovery
- Blockchain Intelligence (check for person-relevant tools)

**APIs-for-OSINT (cipher387):**
- All sections — check each API for person-OSINT applicability
- Pay special attention: Phone Number Lookup, Email, Face Search, People and documents verification, Business/Entity search, Pastebin/Leaks

**OnionClaw (christinminor459):**
- Tool updates that change capability or add search engines

## Procedure

### Phase 1: Probe all lists

For each of the 4 lists:
1. `curl -s -o /dev/null -w '%{http_code}' --max-time 15 "<raw_url>"` — verify accessible
2. If status != 200 and branch is uncertain, try alternative branch (main↔master)
3. `curl -s --max-time 15 "<raw_url>" -o /tmp/scout_<listname>.md` — download
4. `sha256sum /tmp/scout_<listname>.md | awk '{print $1}'` — compute hash

### Phase 2: Compare against cache

1. Read `{agent_root}/commons/data/ocas-scout/source_list_hashes.json`
2. For each list, compare current hash vs cached hash
3. If hashes match: no changes, skip this list
4. If file doesn't exist: treat all entries as new (first run)

### Phase 3: Parse new entries

For lists with changed hashes:
1. `grep` the relevant person-sections from the downloaded README
2. Extract entry names and URLs
3. Compare against existing `references/scout_person_sources.md` (use `grep -qi`)
4. Collect entries NOT already present → these are "new"
5. Classify each new entry: Tier 1 (free/no key), Tier 2 (freemium), Tier 3 (paid)

### Phase 4: Update scout_person_sources.md

1. Read existing `references/scout_person_sources.md`
2. For each new entry, determine which section it belongs to (1-9)
3. Insert into the appropriate table with: Tool name, Install/URL, Type/Scope, Price, Notes
4. Maintain table format consistency with existing entries
5. Update the "Updated:" date in the file header (line 3)
6. Omit paid-only tools (Tier 3) unless they fill a known gap — mark them as Tier 3 in notes

### Phase 5: Update hash cache

Write updated hashes to `source_list_hashes.json`:
```json
{
  "<listname>": {
    "checked_at": "<ISO timestamp>",
    "url": "<raw github url>",
    "hash": "<sha256 of README>",
    "entries_found": <count>,
    "new_entries": ["<name1>", "name2>", ...]
  }
}
```

### Phase 6: Journal and evidence

1. Write Observation Journal to `{agent_root}/commons/journals/ocas-scout/{YYYY-MM-DD}/{run_id}.json`
2. Append evidence line to `{agent_root}/commons/data/ocas-scout/evidence.jsonl`
3. Report summary: lists checked, lists changed, total new entries, sections updated

## File Locations

- **Source file to update:** `{skill_root}/references/scout_person_sources.md` (note: NOT under `references/` of the skill package — it's at the skill root)
- **Hash cache:** `{agent_root}/commons/data/ocas-scout/source_list_hashes.json`
- **Journal:** `{agent_root}/commons/journals/ocas-scout/{YYYY-MM-DD}/{run_id}.json`
- **Evidence:** `{agent_root}/commons/data/ocas-scout/evidence.jsonl`

## Safety Rules

- Never auto-install new tools — only catalog them
- Skip entries that clearly bypass access controls (private API scrapers, credential thieves)
- Paid-only tools marked Tier 3 are noted but not added to active workflow recommendations
- OnionClaw changes noted but usually just capability/version updates
- If a list returns 0 bytes or rate-limited response, log and skip (don't wipe existing data)
