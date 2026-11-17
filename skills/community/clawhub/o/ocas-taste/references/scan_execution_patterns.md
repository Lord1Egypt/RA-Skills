# Scan execution patterns

Concrete command patterns for running taste scans, verified 2026-06-23.

## Historical email scan (365 days)

```bash
# Pre-flight: validate token (see "Pre-scan token repair checklist" section)
cd <hermes-home>/commons/data/ocas-taste && \
  ## Historical email scan (365 days)

  ```bash
  # Pre-flight: validate token (see "Pre-scan token repair checklist" section)
  cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && \
    /usr/bin/python3 \
    <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py \
    scan-historical 365 2>&1
  ```

  **Output:** JSON to stdout with `signals_created`, `cancellations`, `services_scanned`, `total_messages_processed`.

  **Confirmed 2026-06-23:** 599 messages processed, 142 signals created, 2 cancellations. Services: doordash, instacart, good_eggs, tock, opentable, yelp, amazon, hotels.

  **Note:** `scan-historical` is email-only. For the full pipeline (Styx delta + enrichment), use `taste_full_enrich.py`. Use `scan-historical` when the user explicitly wants broad historical email coverage, or when OAuth for calendar is broken but Gmail works.

  **Python runtime:** Use `/usr/bin/python3` (system Python 3.14 with `googleapiclient`). NOT `<hermes-venv>/bin/python3.13` — path does not exist on this profile. NOT ocas-taste venv Python — lacks googleapiclient. Confirmed 2026-06-29: `/usr/bin/python3` works reliably.

  ## Historical calendar scan

  ```bash
  cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && \
    /usr/bin/python3 \
    <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py \
    scan-calendar 365 2>&1
  ```

  ## Incremental daily scan (24h)

  ```bash
  cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && \
    /usr/bin/python3 \
    <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py \
    scan-incremental 24 2>&1
  ```

## OAuth token accounts

| Account | File | Used for |
|---|---|---|
| <operator> | `<gworkspace-creds>/credentials/<user-google-email>.json` | Gmail, Calendar (primary) |
| the agent | `<gworkspace-creds>/credentials/<agent-email>.json` | Fallback (no consumption emails) |

Always verify <operator>'s token was loaded. A 0-byte token or `+00:00` suffix causes silent fallback to the agent's account → 0 results.