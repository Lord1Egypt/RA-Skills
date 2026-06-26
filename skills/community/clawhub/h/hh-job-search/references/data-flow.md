# Data flow

## Recommended practical flow

1. Initialize a job-search project.
2. Fill `PROFILE.md`, `TARGET_ROLES.md`, and `SEARCH_RULES.md`.
3. Convert project state into profile JSON with `profile_to_json.py` when needed.
4. Parse source material into structured vacancy JSON/JSONL.
5. Deduplicate vacancies.
6. Score vacancies against the project profile.
7. Export shortlist or append rows into `PIPELINE.md`.
8. Tailor resume and cover letter only for shortlisted roles.

## Typical command chain

```bash
python -m pip install -r skills/job-search/scripts/requirements.txt
python skills/job-search/scripts/init_job_search_project.py projects/job-search
python skills/job-search/scripts/batch_parse_telegram_jobs.py incoming/tg-posts projects/job-search/exports/tg.jsonl
python skills/job-search/scripts/dedupe_vacancies.py projects/job-search/exports/tg.jsonl > projects/job-search/exports/tg-deduped.json
python skills/job-search/scripts/score_vacancies_jsonl.py projects/job-search projects/job-search/exports/tg.jsonl projects/job-search/exports/tg-scored.jsonl
python skills/job-search/scripts/export_shortlist.py projects/job-search/exports/tg-scored.jsonl projects/job-search/exports/shortlist.csv
```

## Current limitation

`dedupe_vacancies.py` currently emits grouped JSON, not JSONL. If you want a canonical-only JSONL flow, either add a converter step or extend the script later.
