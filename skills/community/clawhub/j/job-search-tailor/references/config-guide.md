# config-guide — job-search-tailor

Config file location: `~/.job-search/config.json`

---

## Field reference

| Field | Type | Default | Description |
|---|---|---|---|
| `target_roles` | `string[]` | required | Job titles to search for (e.g. `["Data Scientist", "ML Engineer"]`) |
| `locations` | `string[]` | required | Locations to search (e.g. `["remote US", "New York, NY"]`) |
| `job_boards` | `string[]` | `["linkedin"]` | Job boards to search. Only `"linkedin"` is supported in v1 |
| `dedup_window_days` | `int` | `30` | Days to remember a URL before showing it again |
| `max_per_company` | `int` | `2` | Max jobs to show per company per run |
| `target_count` | `int` | `8` | Target number of new jobs to surface per run |
| `tracking_file` | `string` | `~/.job-search/memory/shared_jobs.json` | Path to the dedup tracking file |
| `archetypes_dir` | `string` | `~/.job-search/archetypes/` | Directory where resume markdown files live |
| `archetype_match_threshold` | `float` | `0.5` | Minimum keyword overlap score (0–1) to match an archetype |
| `google_docs_enabled` | `bool` | `false` | Whether to use Google Docs URLs for resumes (v1: not implemented) |
| `delivery_channel` | `string` | `"print"` | Where to send results: `"print"` or `"telegram:CHAT_ID"` |
| `archetypes` | `Archetype[]` | `[]` | List of resume archetypes (see below) |

### Archetype object

| Field | Type | Description |
|---|---|---|
| `name` | `string` | Slug identifier (e.g. `"mle"`, `"data-scientist"`) |
| `keywords` | `string[]` | Keywords used for job-to-archetype matching (lowercase) |
| `resume_path` | `string` | Local path to the tailored resume markdown file |
| `resume_url` | `string` | Optional public URL (Google Docs, etc.) — empty string if unused |

---

## Example configs

### Data Scientist job seeker

```json
{
  "target_roles": ["Data Scientist", "Senior Data Scientist", "Staff Data Scientist"],
  "locations": ["remote US", "San Francisco, CA", "New York, NY"],
  "job_boards": ["linkedin"],
  "dedup_window_days": 30,
  "max_per_company": 2,
  "target_count": 8,
  "tracking_file": "~/.job-search/memory/shared_jobs.json",
  "archetypes_dir": "~/.job-search/archetypes/",
  "archetype_match_threshold": 0.4,
  "google_docs_enabled": false,
  "delivery_channel": "print",
  "archetypes": [
    {
      "name": "ds-analytics",
      "keywords": ["data scientist", "analytics", "experimentation", "a/b testing", "sql"],
      "resume_path": "~/.job-search/archetypes/ds-analytics.md",
      "resume_url": ""
    },
    {
      "name": "ds-ml",
      "keywords": ["data scientist", "machine learning", "modeling", "prediction", "python"],
      "resume_path": "~/.job-search/archetypes/ds-ml.md",
      "resume_url": ""
    }
  ]
}
```

### ML Engineer job seeker

```json
{
  "target_roles": ["ML Engineer", "Machine Learning Engineer", "MLOps Engineer"],
  "locations": ["remote US", "Seattle, WA"],
  "job_boards": ["linkedin"],
  "dedup_window_days": 21,
  "max_per_company": 1,
  "target_count": 10,
  "tracking_file": "~/.job-search/memory/shared_jobs.json",
  "archetypes_dir": "~/.job-search/archetypes/",
  "archetype_match_threshold": 0.5,
  "google_docs_enabled": false,
  "delivery_channel": "telegram:123456789",
  "archetypes": [
    {
      "name": "mle",
      "keywords": ["ml engineer", "machine learning engineer", "model training", "pytorch", "tensorflow"],
      "resume_path": "~/.job-search/archetypes/mle.md",
      "resume_url": ""
    },
    {
      "name": "mlops",
      "keywords": ["mlops", "ml platform", "kubeflow", "airflow", "model serving", "kubernetes"],
      "resume_path": "~/.job-search/archetypes/mlops.md",
      "resume_url": ""
    }
  ]
}
```

### Product Manager job seeker

```json
{
  "target_roles": ["Product Manager", "Senior PM", "Group Product Manager", "AI Product Manager"],
  "locations": ["remote US", "New York, NY", "Austin, TX"],
  "job_boards": ["linkedin"],
  "dedup_window_days": 30,
  "max_per_company": 2,
  "target_count": 6,
  "tracking_file": "~/.job-search/memory/shared_jobs.json",
  "archetypes_dir": "~/.job-search/archetypes/",
  "archetype_match_threshold": 0.35,
  "google_docs_enabled": false,
  "delivery_channel": "print",
  "archetypes": [
    {
      "name": "pm-data",
      "keywords": ["data product manager", "analytics pm", "data platform", "metrics", "sql"],
      "resume_path": "~/.job-search/archetypes/pm-data.md",
      "resume_url": ""
    },
    {
      "name": "pm-ai",
      "keywords": ["ai product manager", "ml product", "llm", "generative ai", "ai features"],
      "resume_path": "~/.job-search/archetypes/pm-ai.md",
      "resume_url": ""
    }
  ]
}
```

---

## Google Docs opt-in

**v1 status: not yet implemented.** Setting `google_docs_enabled: true` has no effect.

When implemented, Google Docs integration will:
1. Require a service account credential or OAuth token in `~/.job-search/gcp-creds.json`
2. Push each archetype markdown to a dedicated Google Doc
3. Populate `resume_url` with the shareable Doc link

For now, set `"google_docs_enabled": false` and use `resume_path` for local files.

---

## Troubleshooting

**Missing config / config_not_found error**
- First run? Trigger the skill and it will walk you through setup.
- Already set up? Check the path: `ls ~/.job-search/config.json`

**Empty archetypes array**
- Re-run the skill — it detects an empty archetypes list and re-enters Flow A.
- Or manually add archetype entries and run `save_archetype.py`.

**No results returned**
- Check `target_roles` spelling — use terms that appear in actual LinkedIn job titles.
- Try broader locations (e.g. `"United States"` instead of a specific city).
- Lower `archetype_match_threshold` (try `0.25`).

**Same jobs appearing repeatedly**
- Check `tracking_file` path exists and is writable.
- Increase `dedup_window_days` if jobs cycle back quickly.
- Inspect the tracking file: `cat ~/.job-search/memory/shared_jobs.json | python3 -m json.tool`
