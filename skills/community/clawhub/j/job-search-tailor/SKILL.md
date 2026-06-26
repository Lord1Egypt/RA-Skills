---
name: job-search-tailor
description: >
  Daily job search + resume archetype matching skill. Searches LinkedIn for jobs matching
  your target roles and locations, deduplicates against previously seen listings, and
  automatically matches each job to the best-fit tailored resume archetype (or creates
  a new one on-the-fly). On first run, bootstraps config by asking for your resume,
  target roles, locations, and delivery preferences, then clusters your resume into
  3–5 archetypes. Trigger phrases: "run job search", "find me jobs", "search for ML
  roles", "set up job search", "tailor my resume for jobs", "find jobs and match my
  resume", "job search".
---

# job-search-tailor

You are a job search assistant. You help users find relevant job postings and match
each posting to the best tailored resume archetype from their collection.

Refer to `references/config-guide.md` for config field documentation and
`references/archetypes-guide.md` for archetype scoring details.

---

## Step 0 — Detect mode

Run:
```
python3 ~/.openclaw/workspace/skills/job-search-tailor/scripts/load_config.py
```

- If exit code is non-zero or output contains `"error": "config_not_found"` → **Flow A (First-run setup)**
- If archetypes array is empty or missing → **Flow A**
- Otherwise → **Flow B (Ongoing search)**

---

## Flow A — First-run setup

### A1. Gather user inputs

Ask the user (one message, list all questions):
1. Paste your resume text, or provide the file path to your resume
2. What job titles are you targeting? (e.g. Data Scientist, ML Engineer)
3. What locations? (e.g. "remote US", "New York, NY")
4. Delivery preference: Telegram chat ID (format: `telegram:CHAT_ID`), or just print results here?
5. Enable Google Docs integration for resume hosting? (default: no — v1 uses local files)

Wait for user's answers before proceeding.

### A2. Bootstrap search

For each combination of (role × location), run ONE `web_search`:
- Query format: `site:linkedin.com/jobs "{role}" "{location}" job posting`
- Collect top 5–8 result URLs

For each result URL, `web_fetch` the full page to extract:
- Job title, company, location, salary (if shown), full job description

### A3. Create archetypes

Analyze the user's resume text alongside 3–5 of the fetched job descriptions.
Identify 3–5 natural clusters of role types that appear in the JDs and align with
the user's background. Clusters depend entirely on the user's field — do not assume
tech roles. Examples by field:

- **Tech:** mle, ds, applied-sci, ai-eng, swe, devops
- **Finance:** quant-analyst, risk-analyst, investment-associate
- **Design:** ux-designer, product-designer, visual-designer
- **Marketing:** growth-marketer, content-strategist, brand-manager
- **Healthcare:** clinical-data-analyst, health-informatics, research-coordinator

Derive cluster names from the actual JDs and resume — these are just examples.

For each archetype cluster:
1. Write a tailored resume markdown file to `~/.job-search/archetypes/<name>.md`
   - Use the user's actual resume content, reordered and reworded for that archetype
   - Lead with the most relevant skills and experience for that role type
   - Keep formatting clean: `# Name`, `## Summary`, `## Experience`, `## Skills`, `## Education`
2. Call `save_archetype.py` to register it:
   ```
   python3 ~/.openclaw/workspace/skills/job-search-tailor/scripts/save_archetype.py \
     --name "<name>" \
     --keywords "<kw1,kw2,kw3>" \
     --resume-path "~/.job-search/archetypes/<name>.md"
   ```

### A4. Write config.json

Create `~/.job-search/config.json` with these fields (fill in from user answers):
```json
{
  "target_roles": ["<role1>", "<role2>"],
  "locations": ["<loc1>", "<loc2>"],
  "job_boards": ["linkedin"],
  "dedup_window_days": 30,
  "max_per_company": 2,
  "target_count": 8,
  "tracking_file": "~/.job-search/memory/shared_jobs.json",
  "archetypes_dir": "~/.job-search/archetypes/",
  "archetype_match_threshold": 0.5,
  "google_docs_enabled": false,
  "delivery_channel": "<telegram:CHAT_ID or 'print'>",
  "archetypes": []
}
```

Create tracking file if missing: `~/.job-search/memory/shared_jobs.json` → `[]`

### A5. Deliver initial digest

Proceed directly to Flow B Step B3 using the URLs already fetched in A2.

---

## Flow B — Ongoing search

### B1. Load config

```
python3 ~/.openclaw/workspace/skills/job-search-tailor/scripts/load_config.py
```

Parse the JSON output. Extract: `target_roles`, `locations`, `archetypes`,
`tracking_file`, `dedup_window_days`, `target_count`, `archetype_match_threshold`.

### B2. Search for jobs

For each (role × location) pair, run:
```
web_search: site:linkedin.com/jobs "{role}" "{location}" job posting
```

Collect all result URLs. Aim for `target_count` total unique URLs.

### B3. Deduplicate

Join all collected URLs into a comma-separated string. Call:
```
python3 ~/.openclaw/workspace/skills/job-search-tailor/scripts/update_tracking.py \
  --urls "<url1,url2,...>" \
  --tracking-file <tracking_file> \
  --window-days <dedup_window_days>
```

Parse stdout as a JSON array — these are the **new URLs** only.

If the array is empty: report "No new jobs found since last search." and stop.

### B4. Fetch and score each new job

For each new URL:
1. `web_fetch` the page — extract job title, company, location, salary, description
2. Score against each archetype using **keyword overlap**:
   - Lowercase the job title + first 200 chars of description
   - For each archetype: count how many of its keywords appear in that text
   - Score = 1.0 if ANY keyword from that archetype appears in the text, 0.0 if none
   - Pick the archetype with the highest score
3. If best score ≥ `archetype_match_threshold`:
   - Attach that archetype's `resume_path` (and `resume_url` if set)
4. If best score < threshold (no good match):
   - Create a new archetype on-the-fly:
     a. Name it after the dominant role type in the title (slugify: lowercase, hyphens)
     b. Write tailored resume markdown to `~/.job-search/archetypes/<name>.md`
     c. Extract 4–6 keywords from the job title and description
     d. Call:
        ```
        python3 ~/.openclaw/workspace/skills/job-search-tailor/scripts/save_archetype.py \
          --name "<name>" \
          --keywords "<kw1,kw2,...>" \
          --resume-path "~/.job-search/archetypes/<name>.md"
        ```
     e. Note: Google Docs push is not implemented in v1 — local file only

### B5. Format digest

For each job produce one entry:

```
**{Company} — {Title}**
📍 {Location} | 💰 {Salary or "Not listed"}
🔗 {Apply URL}
📄 Resume: {resume_path or resume_url}
```

### B6. Deliver

- If `delivery_channel` starts with `telegram:` — format digest as one message and
  tell the user to send it via their configured Telegram bot to the given chat ID
  (v1 does not auto-send; present the formatted message for manual use or copy-paste)
- Otherwise: print the full digest in the conversation

---

## Error handling

- If `load_config.py` fails: switch to Flow A
- If `web_search` returns no results for a query: skip that role/location pair, note it
- If `web_fetch` fails for a URL: skip that job, note it
- If `update_tracking.py` fails: warn the user and continue without dedup
- If `save_archetype.py` fails: warn but continue — archetype is not persisted

---

## Notes

- Always use `python3` (not `python`) to invoke scripts
- Script paths: `~/.openclaw/workspace/skills/job-search-tailor/scripts/`
- Default config path: `~/.job-search/config.json`
- v1 does not auto-send Telegram messages or push to Google Docs — these are formatted outputs
