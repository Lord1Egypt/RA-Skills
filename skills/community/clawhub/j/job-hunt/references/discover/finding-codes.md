# Discover gate findings

Read this when a discover gate (`check_no_write.py`, `check_candidate_match.py`,
`lint_no_prediction.py`, `check_shortlist.py` or `check_search_coverage.py`)
reports a finding. The repair rules every finding follows are in
`modes/discover.md` Step 10: the receipts in `journal.jsonl` and the captures in
`raw/` are the record and are never edited to reconcile a finding, and deleting a
row means deleting it from both `shortlist.yaml` and `shortlist.md`.

| Finding | What it means | What to do |
|---|---|---|
| `NO_MODE_ENTRY` | `journal.jsonl` has no `mode_entry` for discover | run `scripts/enter_mode.py --workspace <ws> --mode discover` and read `modes/discover.md` — it was not loaded |
| `MODE_FILE_CHANGED` | `modes/discover.md` changed after the run entered the mode | what you read is not what is on disk. Re-enter and re-read. |
| `SOURCE_ID_NOT_IN_RAW` | a row's identifier is in no capture from that site | delete the row **from `shortlist.yaml` AND from `shortlist.md`**. It was not retrieved. Do not "fix" it by editing `raw/`. |
| `RAW_TEXT_NOT_IN_RAW` | most of a row's card text is in no capture from that site | copy the card text the adapter returned. If you cannot, the row was not retrieved — delete it **from both files**. Paraphrase belongs in `why_matched`. |
| `NO_RAW_TEXT` | a row has an empty `raw_text` | recover the card text, or drop the row; nothing else ties its claims to the capture |
| `BAD_ROW_ID` | a row's `id` is not `<site>-<source_id>` | rewrite the id. It is the handle a reader quotes, and it must name the posting the row was traced to. |
| `SOURCE_REPORT_RAW_PATH` | a `raw_files` entry is not a `raw/…` workspace-relative path | write `raw/<site>-<n>.json`. One spelling for one file. |
| `SOURCE_REPORT_MISSING_RAW` | a `raw_files` entry names a file that does not exist | copy the exact capture name from `raw/` (`run_tool.py` names it `raw/<site>-<32-hex id>.json`); never invent `raw/<site>-1.json` |
| `WARN_ROW_OUTSIDE_BRIEF_MARKET` | *(warning, does not fail)* a row's location names a country outside `brief.markets` | check the adapter's geography — see `indeed` in `modes/discover.md` Step 2. Drop the row, or keep it and say why the warning is a false alarm. |
| `URL_NOT_FROM_ADAPTER` | the URL was assembled, not returned | replace it with the adapter's URL or drop the field. If you delete the row, delete it **from both files**. |
| `MD_ROW_NOT_IN_SHORTLIST` | `shortlist.md` renders a posting URL that is in no `shortlist.yaml` row | the .md is what the user acts on. Either the row belongs in the yaml and was traced, or it was retrieved by nothing — delete it from the .md. |
| `MISSING_POSTING_URL` / `BAD_POSTING_URL` / `MD_POSTING_URL_MISSING` | a row has no usable direct URL, or the user-facing list omits it | retain only rows whose captured posting URL is absolute HTTP(S), and render that same URL as a Markdown link in §1. |
| `COMPANY_NOT_IN_RAW` / `SALARY_NOT_IN_RAW` | a row's employer or pay contradicts the capture it cites | copy what the adapter returned, or leave the field empty. Salary is the field a reader acts on hardest and the one most easily invented from a blank. |
| `PAGES_ABOVE_CAP` / `ROWS_ABOVE_CAP` | the round actually exceeded a cap `brief.yaml` declares | the cap is compared to the run, not only to the ceiling. Both-language queries on one page are one page. |
| `DUPLICATE_SOURCE_ID` | one retrieved posting appears as two rows | delete the duplicate; de-duplication removes rows, nothing adds them |
| `SOURCE_REPORT_COUNT_MISMATCH` | the source report claims more than the receipts recorded | the receipts are right. Never reconcile by editing `raw/` or the journal. |
| `EMPTY_RESULT_UNSUPPORTED` | "no results" wording with no adapter that exited 0 | rewrite as "every adapter failed", and emit the disclosure block |
| `DEGRADED_WITHOUT_DISCLOSURE` | degraded run with no disclosure block in a supported report language | add the matching template, check and fill every answer |
| `DISCLOSURE_INCOMPLETE` | a disclosure line or answer is missing | fill all six lines in the document's language; change a pre-filled 否 / no only if a retry or bypass actually happened |
| `MD_MISSING_PROVISIONAL_STAMP` | `shortlist.md` lacks the provisional stamp matching the round's actual read quality | add the all-card or detail-reviewed stamp from `modes/discover.md` Step 7 (Japanese, Korean or Spanish: `references/report-localization.md`), in the round's own language, to the section heading. The YAML flag is not a disclosure. |
| `HIGH_VERDICT_UNVERIFIED` / `RECOMMENDATION_NOT_READY` | a high verdict or default recommendation lacks complete JD-to-CV evidence | keep the row as `review` / `stretch`, or repair the quoted evidence mapping. Do not claim an outcome. |
| `JOB_EVIDENCE_NOT_DETAIL` / `CV_EVIDENCE_PATH_INVALID` | the match evidence is not a successful row-specific detail capture, or does not point into the frozen profile | fetch the actual detail within the cap, or cite the exact profile leaf. Never cite an inferred skill. |
| `MATCH_REVIEWS_ABOVE_CAP` | more detail mappings than `brief.max_match_reviews` permits | keep only the highest-priority reviews this round; start a new bounded round for the rest. |
| `DETAIL_FETCH_OUT_OF_BAND` | a detail fetch below the top three verdicts | remove it, or record a named exception with a reason |
| `CAP_MISSING` / `CAP_ABOVE_CEILING` | `brief.yaml`'s round caps are absent or raised | read `references/source-policy.md`; the caps are its enforceable half |
| `SHORTFALL_NO_REASON` | fewer rows than `target_count`, no reason written | write the reason. Never pad. |
| `SOURCE_REPORT_CONTRADICTS_JOURNAL` | `sources:` disagrees with the receipts | the receipts are right; fix the report |
| `NOT_A_LISTING_SOURCE` | a row cites a source that publishes no job postings, or was retrieved by a command of that source which does not | the row asserts a vacancy exists and this capture cannot support that. A 面经 thread, a recruiter-side person record or a forum post is a **pointer for the report**, not a row — move it there and delete the row from `shortlist.yaml` AND `shortlist.md`. Which commands publish postings is `listing_commands` in `references/discovery-sources.md`; if a command really does return vacancies, measure it and record it there rather than editing the row. |
| `CATALOGUE_UNREADABLE` | `references/discovery-sources.md` is missing or its yaml block will not parse | no row's source was checked this run. Restore the file; this is a broken install, not a finding about the round. |
| `WRITE_COMMAND` | a write command was journaled | stop. Tell the user exactly what ran. It cannot be undone. |
| `UNKNOWN_ACCESS` | a command's access could not be resolved | save `opencli <site> --help -f yaml` into `raw/opencli-help/` and re-run |
