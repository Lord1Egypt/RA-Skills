---
name: medical-conference-search
description: "Search medical conference and presentation databases. Use this skill whenever the user asks about medical conferences, academic conferences, session abstracts, posters, oral presentations, or conference-presented drug/trial data. Three scripts are available: search_conferences.py (find conferences), search_presentations.py (find abstracts/presentations), and search_chained.py (find conferences then auto-inject into presentation search). Trigger words include: conference, symposium, congress, ASCO, ESMO, AHA, ACC, session, abstract, poster, oral presentation, data presented at, efficacy data, safety data, congress abstract."
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["NOAH_API_TOKEN"]},"primaryEnv":"NOAH_API_TOKEN" } }
---

# Conference Search Skill

This skill searches a conference and presentation database using three independent scripts. Choose the script that fits the task — each can be used standalone, or combined in sequence.

---

## Scripts Overview

| Script | When to use |
|---|---|
| `scripts/search_conferences.py` | Find conferences by name, date, location, or therapeutic area |
| `scripts/search_presentations.py` | Find abstracts/presentations when you already know the conference name or series |
| `scripts/search_chained.py` | Discover the conference first, then auto-inject its name into a presentation search |

---

## Script 1 — Search Conferences Only

Use when the user asks about **which conferences exist**, **when/where they are held**, or wants to **browse conferences** by area or organization.

```bash
python scripts/search_conferences.py --params '<JSON>'
python scripts/search_conferences.py --params-file query.json
python scripts/search_conferences.py --params '<JSON>' --raw
python scripts/search_conferences.py --params '<JSON>' --output results.json
```

### Query fields

| Field | Type | Description | Example |
|---|---|---|---|
| `conference_name` | `str` | Full or partial conference name | `"ASCO Annual Meeting 2024"` |
| `conference_start_date` | `str` | Start date (YYYY-MM-DD) | `"2024-06-01"` |
| `conference_end_date` | `str` | End date (YYYY-MM-DD) | `"2024-06-05"` |
| `conference_location` | `str` | City, country, or venue | `"Chicago"` |
| `series_name` | `str` | Conference series name | `"ASCO"` |
| `series_organization` | `str` | Organizing body | `"American Society of Clinical Oncology"` |
| `from_n` | `int` | Pagination offset | `0` |
| `size` | `int` | Results per page | `50` |

### Examples

```bash
# Find all ASCO conferences
python scripts/search_conferences.py --params '{"series_name": "ASCO"}'

# Conferences in Chicago in 2024
python scripts/search_conferences.py --params '{"conference_location": "Chicago", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}'

# ESMO conferences, raw JSON
python scripts/search_conferences.py --params '{"series_name": "ESMO"}' --raw
```

### Result fields
`conference_name`, `conference_abbreviation`, `conference_website`, `conference_description`, `conference_start_date`, `conference_end_date`, `conference_location`, `series_id`, `series_name`, `series_abbreviation`, `series_website`, `series_organization`

---

## Script 2 — Search Presentations Only

Use when the user asks about **specific drugs, diseases, targets, authors, or institutions** and already knows (or doesn't need to filter by) an exact conference. The `series_name` field is sufficient for most queries.

```bash
python scripts/search_presentations.py --params '<JSON>'
python scripts/search_presentations.py --params-file query.json
python scripts/search_presentations.py --params '<JSON>' --raw
python scripts/search_presentations.py --params '<JSON>' --output results.json
```

### Query fields

| Field | Type | Description | Example |
|---|---|---|---|
| `authors` | `List[str]` | Presenter / author name(s) | `["John Smith"]` |
| `institutions` | `List[str]` | Author institution(s) | `["MD Anderson"]` |
| `drugs` | `List[str]` | Drug name(s) | `["pembrolizumab"]` |
| `diseases` | `List[str]` | Disease / indication(s) | `["lung cancer", "NSCLC"]` |
| `targets` | `List[str]` | Biological target(s) | `["PD-1", "VEGF"]` |
| `conference_name` | `str` | Exact conference name | `"2024 ASCO Annual Meeting"` |
| `series_name` | `str` | Conference series name | `"ESMO"` |
| `from_n` | `int` | Pagination offset | `0` |
| `size` | `int` | Results per page | `10` |

### Examples

```bash
# Pembrolizumab lung cancer abstracts at ESMO
python scripts/search_presentations.py --params '{"drugs": ["pembrolizumab"], "diseases": ["lung cancer"], "series_name": "ESMO"}'

# KRAS G12C data from MD Anderson researchers
python scripts/search_presentations.py --params '{"targets": ["KRAS G12C"], "institutions": ["MD Anderson"]}'

# All presentations at a specific conference (exact name required)
python scripts/search_presentations.py --params '{"conference_name": "2024 ASCO Annual Meeting", "diseases": ["NSCLC"]}'

# Save to file
python scripts/search_presentations.py --params '{"drugs": ["nivolumab"]}' --output results.json
```

### Result fields
`session_title`, `presentation_title`, `presentation_website`, `main_author`, `main_author_institution`, `authors`, `institutions`, `abstract`, `design`, `efficacy`, `safety`, `summary`, `drugs`, `diseases`, `targets`, `series_name`, `conference_name`

---

## Script 3 — Chained Search (Conference → Presentation)

Use when you need to **find the exact conference first**, then search its presentations. The top-matching `conference_name` from Step 1 is **automatically injected** into Step 2 — no manual copy-paste needed.

```bash
python scripts/search_chained.py \
    --conference-params '<JSON>' \
    --presentation-params '<JSON>'

# With file inputs
python scripts/search_chained.py \
    --conference-params-file conf.json \
    --presentation-params-file pres.json

# Raw JSON + save to file
python scripts/search_chained.py \
    --conference-params '<JSON>' \
    --presentation-params '<JSON>' \
    --raw --output results.json
```

### Examples

```bash
# PD-1 data at ASCO 2024 (auto-resolves conference name)
python scripts/search_chained.py \
    --conference-params '{"series_name": "ASCO", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}' \
    --presentation-params '{"targets": ["PD-1"]}'

# Roche bispecific antibodies at ASH conferences
python scripts/search_chained.py \
    --conference-params '{"series_name": "ASH"}' \
    --presentation-params '{"drugs": ["bispecific antibody"], "institutions": ["Roche"]}'
```

---

## Choosing the Right Script

```
User asks about conferences / dates / locations
  → search_conferences.py

User asks about drug / disease / abstract data, knows the series (e.g. "at ESMO")
  → search_presentations.py  (use series_name field)

User asks about drug / disease / abstract data, knows the year but not exact conference name
  → search_chained.py  (resolves conference_name automatically)
```

---

## Fallback Search Strategies

When an initial query returns zero or poor results, try these strategies **in order**:

### Strategy 1 — Conference Name / Series Variant Expansion

Conference abbreviations and full names are often stored inconsistently. Try common variants before giving up.

```bash
# Try abbreviation first, then full name
python scripts/search_conferences.py --params '{"series_name": "ASCO"}'
python scripts/search_conferences.py --params '{"series_name": "American Society of Clinical Oncology"}'

# Try alternate known abbreviations
# ESMO → "European Society for Medical Oncology"
# AHA  → "American Heart Association"
# ACC  → "American College of Cardiology"
```

For presentations, switch from `conference_name` (exact match) to `series_name` (fuzzy):

```bash
# Exact match — fails if name is slightly off
--params '{"conference_name": "2024 ASCO Annual Meeting", ...}'

# Safer fallback — use series instead
--params '{"series_name": "ASCO", ...}'
```

---

### Strategy 2 — Switch to Chained Search

If `search_presentations.py` returns nothing with a manually typed `conference_name`, the name is likely mismatched. Let `search_chained.py` resolve it automatically.

```bash
# Instead of (may fail on exact name mismatch):
python scripts/search_presentations.py \
  --params '{"conference_name": "ASCO 2024", "drugs": ["pembrolizumab"]}'

# Use chained (auto-resolves correct conference_name):
python scripts/search_chained.py \
  --conference-params '{"series_name": "ASCO", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}' \
  --presentation-params '{"drugs": ["pembrolizumab"]}'
```

---

### Strategy 3 — Drug / Disease Term Expansion

Drug names and disease terms in abstracts may use brand names, INNs, aliases, or abbreviations. Expand the `drugs` or `diseases` list to cover variants.

```bash
# Expand drug name variants
--params '{"drugs": ["SHR-A1904", "SHR A1904", "A1904"], "series_name": "ASCO"}'

# Expand disease terms (specific → broad)
--params '{"diseases": ["NSCLC", "non-small cell lung cancer", "lung cancer"], "series_name": "ESMO"}'

# Try target if drug name fails entirely
--params '{"targets": ["CLDN18.2", "Nectin-4"], "series_name": "ASCO"}'
```

---

### Strategy 4 — Institution-First Search

When drug name and disease matching both fail, anchor on the presenting institution or author and filter results locally.

```bash
# Broad institutional pull
python scripts/search_presentations.py \
  --params '{"institutions": ["Jiangsu Hengrui", "Hengrui Medicine"], "series_name": "ASCO", "size": 100}'

# Then filter locally by drug name pattern or disease keyword
```

---

### Strategy 5 — Relax Filters Incrementally

Drop constraints one at a time in this order:

1. Remove `conference_name` → use `series_name` only
2. Remove date range constraints
3. Broaden `diseases` (e.g. `"NSCLC"` → `"lung cancer"` → `"cancer"`)
4. Remove `series_name` to search across all conferences
5. Search by `targets` alone if drug name is unknown

---

## Decision Tree

```
Query returns results?
├── Yes → present results
└── No (presentations) →
      Strategy 1: switch conference_name → series_name
      └── Still no → Strategy 2: switch to search_chained.py
                     └── Still no → Strategy 3: expand drugs / diseases / targets terms
                                    └── Still no → Strategy 4: institution anchor + local filter
                                                   └── Still no → Strategy 5: relax filters incrementally

No (conferences) →
      Strategy 1: try series abbreviation ↔ full name swap
      └── Still no → try different series_name or remove location filter

Any step hits HTTP 429?
└── Pause entire chain 30s → resume from current strategy
    (sleep ≥5s between every request to avoid triggering 429)
```

---

## Conversion Examples

**User:** "What PD-1 drug data was presented at ASCO 2024?"

```bash
python scripts/search_chained.py \
  --conference-params '{"series_name": "ASCO", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}' \
  --presentation-params '{"targets": ["PD-1"]}'
```

---

**User:** "Pembrolizumab lung cancer abstracts from ESMO"

```bash
python scripts/search_presentations.py \
  --params '{"drugs": ["pembrolizumab"], "diseases": ["lung cancer"], "series_name": "ESMO"}'
```

---

**User:** "Oncology conferences in Chicago 2024"

```bash
python scripts/search_conferences.py \
  --params '{"conference_location": "Chicago", "conference_start_date": "2024-01-01", "conference_end_date": "2024-12-31"}'
```

---

**User:** "KRAS G12C presentations by MD Anderson researchers"

```bash
python scripts/search_presentations.py \
  --params '{"targets": ["KRAS G12C"], "institutions": ["MD Anderson"]}'
```

---

**User:** "Roche bispecific antibody data at ASH conferences"

```bash
python scripts/search_chained.py \
  --conference-params '{"series_name": "ASH"}' \
  --presentation-params '{"drugs": ["bispecific antibody"], "institutions": ["Roche"]}'
```

---

## Tips

- If no results are returned, try relaxing filters (e.g. use `series_name` instead of `conference_name`, or broaden the disease term).
- `conference_name` in `search_presentations.py` must be an **exact match** — use `search_chained.py` or run `search_conferences.py` first to get the correct name.
- All `List[str]` fields accept multiple values: `["NSCLC", "lung cancer"]`.

---

## Dependencies

- Python 3.8+
- `requests` library (`pip install requests`)
- Environment variable `NOAH_API_TOKEN` — register at [noah.bio](https://noah.bio) to obtain your API key.

---

## Security & Packaging Notes

- This skill only calls NoahAI official HTTPS endpoints under `https://www.noah.bio/api/` and does not contact third-party services.
- It requires exactly one environment variable: `NOAH_API_TOKEN`. Store it in the environment or a local `.env` file, and never place it inline in commands, chats, or packaged files.
- The token is scoped to read medical public details only and cannot access private user records.
- The skill does not intentionally persist request parameters locally. Any server-side retention is determined by the NoahAI API service and its operational logging policies.
- It does not request persistent or system-level privileges and does not modify system configuration.
- The skill is source-file based (Python scripts only) and does not require runtime installs, package downloads, or external bootstrap steps.