---
name: m5stack-firmware-query
description: Query the public M5Burner/M5Stack firmware repository by keyword, device, category, functional intent, ID, version, developer, UIFlow2, recommendations, rankings, or comments. Use for read-only firmware discovery; not for uploads, account data, or device flashing.
---

# M5Stack Firmware Query

Use this skill when a user or agent needs current public information from the M5Stack M5Burner firmware repository.

## Operating Rules

- Treat firmware counts, versions, rankings, download totals, and timestamps as live data. Query the API at answer time instead of relying on memory, and state the retrieval date when the value matters.
- The default API is `https://burner.m5stack.com`. Override it with `M5BURNER_API_BASE_URL` or the command's `--base-url` option when testing another compatible deployment.
- Keep this skill read-only. Do not upload, publish, edit, approve, reject, delist, like, follow, comment, create shares, download BIN files, flash devices, or access account/admin endpoints.
- Do not request, paste, print, or persist bearer tokens. Public catalog routes are sufficient for the supported queries.
- IDs are opaque strings. Preserve them exactly in the response and do not infer meaning from their numeric shape.
- When an API request fails, report the HTTP status or API `code`, `msg`, and `requestId` when present. Distinguish an empty result (`200` with no rows) from an authentication or server error.

## Query Workflow

1. Identify the query mode:
   - `search`: keyword, category, device, sort, or pagination.
   - `intent-search`: functional intent search such as AI projects; it paginates candidates and checks names/descriptions instead of trusting a category label alone.
   - `detail`: one firmware project's public metadata and current version.
   - `versions`: public version history for a firmware ID.
   - `devices` or `device-by-slug`: device catalog lookup.
   - `categories`: localized category counts, optionally scoped to a device or developer.
   - `developers`, `developer`, or `developer-firmwares`: public developer information and published firmware.
   - `uiflow2`: latest UIFlow2 records and CDN URLs.
   - `recommended`, `ranking`, or `comments`: public discovery and community data.
   - `recommend-device`: answer "what interesting apps can I flash on this device?" by aggregating latest, most-downloaded, most-liked, and detail records.
2. Run `scripts/m5stack_firmware_query.py` from this skill directory. Use JSON output for agent processing and `--format table` for a concise terminal report.
3. For name-based device or category filtering, use `--device-name` or `--category-name`; the script resolves the current catalog ID before searching.
4. Use `search --sort LATEST`, `search --sort MOST_DOWNLOADED`, or `search --sort MOST_LIKED`; do not guess unverified sort values.
5. For questions such as “有没有 AI 项目”, prefer `intent-search --intent ai` with the exact device. Treat `AI & Assistants` as a discovery signal, not proof: report the catalog candidate count, description-confirmed count, and notable exclusions when they differ. Use the bounded exclusion sample; do not paste every non-match into the answer.
6. Distinguish API facts from curation inference. Use wording such as “项目描述显示” or “本次筛选认为”; do not call a project stable, simple, compatible, or recommended unless the source or an actual test supports that claim. Download counts are popularity signals, not quality or stability evidence. `intent-search` is heuristic, so state that ambiguous projects may require manual detail review.
7. Summarize the fields relevant to the question: firmware ID when useful for reproducibility, name, version, publication date, status, supported device, source URL, M5Burner page URL, statistics, and required versus optional prerequisites. Do not dump full descriptions unless asked.
8. For recommendation-style answers, prefer `recommend-device`. Treat its score as a candidate-generation aid, not as the final ranking; curate a balanced answer across music/media, games, launchers, desktop displays, developer tools, and hardware/network experiments when those categories are available.
9. Keep hardware variants separate. In particular, original `Cardputer` and `Cardputer ADV` are different catalog devices; if the user does not specify one, answer for the exact matched device and mention that the other variant needs a separate query.
10. Include the retrieval date, mention that the result is from public M5Burner data, and call out external prerequisites such as SD cards, legal ROM/game files, keyboards, API keys, cloud account binding, or required modules.
11. Read [references/api.md](references/api.md) when the endpoint contract, response envelope, parameter names, or public/authenticated boundary needs clarification.

## Common Commands

```bash
# Latest public firmware
python3 scripts/m5stack_firmware_query.py search --sort LATEST --page-size 20 --pretty

# Search by keyword and device name
python3 scripts/m5stack_firmware_query.py search \
  --keyword UIFlow2.0 \
  --device-name CoreS3 \
  --format table

# Recommend interesting firmware for one device
python3 scripts/m5stack_firmware_query.py recommend-device \
  --device-name Tab5 \
  --limit 10 \
  --format table

# Most downloaded firmware for one device
python3 scripts/m5stack_firmware_query.py search \
  --device-name Tab5 \
  --sort MOST_DOWNLOADED \
  --page-size 20 \
  --format table

# Search by category name
python3 scripts/m5stack_firmware_query.py search \
  --category-name Tools \
  --page 1 \
  --page-size 10 \
  --format table

# Verify AI functionality instead of trusting the AI category label
python3 scripts/m5stack_firmware_query.py intent-search \
  --intent ai \
  --device-name Cardputer \
  --sort LATEST \
  --format table

# Inspect one project and its public versions
python3 scripts/m5stack_firmware_query.py detail 1897200000000000393 --pretty
python3 scripts/m5stack_firmware_query.py versions 1897200000000000393 --format table

# Catalog and UIFlow2
python3 scripts/m5stack_firmware_query.py devices --format table
python3 scripts/m5stack_firmware_query.py categories --language US --format table
python3 scripts/m5stack_firmware_query.py uiflow2 --format table

# Public discovery data
python3 scripts/m5stack_firmware_query.py ranking --kind weekly --format table
python3 scripts/m5stack_firmware_query.py ranking --kind all-time --limit 20 --format table
python3 scripts/m5stack_firmware_query.py recommended --limit 6 --pretty
```

The script uses only Python's standard library. Run `python3 scripts/test_m5stack_firmware_query.py` after changing it.
