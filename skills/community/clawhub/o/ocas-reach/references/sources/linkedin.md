# LinkedIn (linkedin-scraper-mcp)

LinkedIn profile, company, job, and messaging access via browser automation. Uses the `linkedin-scraper-mcp` pip package invoked via MCP stdio.

## Prerequisites

```bash
pip install linkedin-scraper-mcp
uv tool install linkedin-scraper-mcp
```

**First-time login (required):**

```bash
uvx linkedin-scraper-mcp@latest --login
```

This opens a browser window for manual LinkedIn login (5-minute timeout for 2FA). The browser profile is saved to `~/.linkedin-mcp/`. For headless servers, create the profile on a desktop and copy `~/.linkedin-mcp/` to the server.

Optional env vars:
- `LINKEDIN_USER_DATA_DIR` — Custom browser profile path (default: `~/.linkedin-mcp/profile`)
- `LINKEDIN_CHROME_PATH` — Custom Chrome/Chromium executable path

## Actions

### `person_profile`
Get a person's LinkedIn profile.

```bash
python3 scripts/reach.py query linkedin person_profile '{"public_id": "william-gates", "sections": "experience,education,skills"}'
```

Params:
- `public_id` (string, required) — LinkedIn profile slug (from URL)
- `sections` (string or list, optional) — Comma-separated: experience, education, interests, honors, languages, certifications, skills, projects, contact_info, posts

### `company_profile`
Get company information.

```bash
python3 scripts/reach.py query linkedin company_profile '{"public_id": "microsoft", "sections": "posts,jobs"}'
```

Params:
- `public_id` (string, required) — Company slug
- `sections` (string or list, optional) — posts, jobs

### `search_people`
Search for people on LinkedIn.

```bash
python3 scripts/reach.py query linkedin search_people '{"keywords": "machine learning engineer", "company": "Google", "limit": 10}'
```

Params:
- `keywords` (string, optional)
- `location` (string, optional)
- `company` (string, optional) — Current company filter
- `connection_degree` (string, optional) — 1st, 2nd, 3rd
- `limit` (int, optional)

### `search_companies`
Search for companies.

```bash
python3 scripts/reach.py query linkedin search_companies '{"keywords": "artificial intelligence", "limit": 10}'
```

### `search_jobs`
Search for jobs.

```bash
python3 scripts/reach.py query linkedin search_jobs '{"keywords": "quantitative researcher", "location": "New York", "limit": 10}'
```

### `company_employees`
List employees at a company.

```bash
python3 scripts/reach.py query linkedin company_employees '{"public_id": "apple", "keyword": "engineer", "limit": 25}'
```

### `company_posts`
Get recent company posts.

```bash
python3 scripts/reach.py query linkedin company_posts '{"public_id": "nvidia", "limit": 10}'
```

### `feed`
Get the authenticated user's home feed.

```bash
python3 scripts/reach.py query linkedin feed '{"limit": 20}'
```

### `inbox` / `conversation` / `search_messages`
Messaging operations.

```bash
python3 scripts/reach.py query linkedin inbox '{"limit": 20}'
python3 scripts/reach.py query linkedin conversation '{"username": "john-doe"}'
python3 scripts/reach.py query linkedin search_messages '{"query": "interview"}'
```

### `send_message`
Send a message.

```bash
python3 scripts/reach.py query linkedin send_message '{"username": "john-doe", "message": "Hi, I enjoyed your post on..."}'
```

### Other actions
- `job_details` — Get job posting details. Params: `{job_id}`
- `sidebar_profiles` — Get "People also viewed" sidebar. Params: `{public_id}`
- `my_profile` — Get authenticated user's profile. Params: `{sections}`

## Use cases

- **Executive research** — Look up company leadership profiles
- **Competitive intelligence** — See who competitors are hiring
- **Job market analysis** — Search job postings by title/company/location
- **Employee research** — Find employees at specific companies
- **Company monitoring** — Track company posts and updates

## Pitfalls

- **Authentication required** — Unlike most Reach sources, LinkedIn requires a valid browser session. Run `--login` first.
- **Session expiration** — Browser sessions expire. If you get auth errors, run `--login` again.
- **LinkedIn TOS** — Automated scraping may violate LinkedIn's Terms of Service. Use reasonable volumes; this tool is for targeted lookups, not bulk scraping.
- **Rate limiting** — LinkedIn may send warnings about automated tool usage with heavy use. Tool calls are serialized to protect the shared browser session.
- **Chromium dependency** — The MCP server downloads Patchright Chromium on first use (~200MB). Ensure sufficient disk space.
- **Cloud IP issues** — LinkedIn may require additional verification (CAPTCHA, 2FA) when logging in from cloud IPs. Using a residential proxy or VPN may help.
