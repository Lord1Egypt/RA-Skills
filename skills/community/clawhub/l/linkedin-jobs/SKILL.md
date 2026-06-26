---
name: linkedin_jobs
description: Search and monitor LinkedIn job listings with city-based filters, hourly cron support, and smart deduplication. Supports 100+ global tech hubs.
metadata: { "openclaw": { "requires": { "bins": ["python"] }, "emoji": "💼", "homepage": "https://clawhub.ai/skills/linkedin-jobs", "install": [{ "id": "pip", "kind": "pip", "packages": ["requests", "beautifulsoup4"], "label": "Install Python dependencies" }] }, "clawhub": { "version": "1.0.0", "license": "MIT", "tags": ["jobs", "linkedin", "scraping", "career", "automation", "cron"], "category": "productivity" } }
user-invocable: true
---

# LinkedIn Job Search Skill

Search and monitor LinkedIn job listings with powerful filters. Supports 100+ global tech hubs with precise geo IDs, hourly monitoring via cron, and smart deduplication.

## Configuration

After installation, optionally customize by copying `config.example.json` to `config.json`:

```bash
cp {baseDir}/config.example.json {baseDir}/config.json
```

Configurable options:
- Default filters (experience, remote, date_posted)
- Scraper delays and timeout
- Notification preferences
- Custom geo IDs for your cities

## Capabilities

1. **One-time search**: Search LinkedIn for jobs matching keywords and filters
2. **Scheduled monitoring**: Add search profiles that run hourly via cron
3. **Smart deduplication**: Only shows new jobs you haven't seen before
4. **Global city support**: 100+ tech hubs with precise geo IDs

## How to Use

### One-Time Job Search

Use the `exec` tool to run a direct search:

```bash
python {baseDir}/linkedin_scraper.py --keywords "AI Engineer" --location "Bengaluru, India" --max-pages 2
```

**Parameters:**

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `--keywords`, `-k` | Job search keywords (required) | "AI Engineer", "Python Developer" |
| `--location`, `-l` | City, country | "Noida, India", "San Francisco", "Berlin" |
| `--experience`, `-e` | Experience levels | 2 (Entry), 3 (Associate), 4 (Mid-Senior) |
| `--remote`, `-r` | Work arrangement | 1 (On-site), 2 (Remote), 3 (Hybrid) |
| `--date-posted`, `-d` | Time filter | r86400 (24h), r604800 (1wk), r2592000 (1mo) |
| `--job-type`, `-j` | Employment type | F (Full-time), P (Part-time), C (Contract) |
| `--max-pages`, `-p` | Pages to scrape (25 jobs/page) | 1-5 |

**Example - Entry level AI jobs in Noida, hybrid/on-site:**
```bash
python {baseDir}/linkedin_scraper.py --keywords "AI Engineer" --location "Noida, India" --experience "2" --remote "1,3" --max-pages 2
```

### Managing Search Profiles (for Hourly Monitoring)

When the user wants to set up recurring job searches, use these commands:

**Add a new search profile:**
```bash
python {baseDir}/linkedin_cron.py add --keywords "AI Engineer" --location "Bengaluru, India"
```

**Add multiple job titles at once (comma-separated):**
```bash
python {baseDir}/linkedin_cron.py add --keywords "AI Engineer, ML Engineer, Data Scientist" --location "Bengaluru, India"
```
This creates 3 separate profiles with the same location and filters, and deduplicates results across all of them.

**Add with custom filters:**
```bash
python {baseDir}/linkedin_cron.py add --keywords "Python Developer" --location "San Francisco" --experience "2" --remote "2,3"
```

**List all search profiles:**
```bash
python {baseDir}/linkedin_cron.py list
```

**Run all enabled profiles now (for hourly cron or manual check):**
```bash
python {baseDir}/linkedin_cron.py run
```

**Run specific profile:**
```bash
python {baseDir}/linkedin_cron.py run --profile ai-engineer-bengaluru
```

**Enable/Disable a profile:**
```bash
python {baseDir}/linkedin_cron.py enable --profile ai-engineer-bengaluru
python {baseDir}/linkedin_cron.py disable --profile ai-engineer-bengaluru
```

**Remove a profile:**
```bash
python {baseDir}/linkedin_cron.py remove --profile ai-engineer-bengaluru
```

**Clear job history (to see all jobs again):**
```bash
python {baseDir}/linkedin_cron.py clear-history
```

**View statistics:**
```bash
python {baseDir}/linkedin_cron.py stats
```

## Supported Cities (100+ Global Tech Hubs)

The skill has built-in geo IDs for precise location-based results:

**India:** Bengaluru, Noida, Hyderabad, Mumbai, Delhi NCR, Pune, Chennai, Gurugram, Kolkata, Ahmedabad, Jaipur, Chandigarh, Kochi, Coimbatore, Indore, Lucknow

**USA:** San Francisco, New York, Seattle, Austin, Boston, Los Angeles, Chicago, Denver, San Diego, Washington DC, Atlanta, Dallas, Houston, Phoenix, Miami, Portland

**UK:** London, Manchester, Edinburgh, Cambridge, Oxford, Bristol, Birmingham, Leeds, Glasgow

**Europe:** Berlin, Amsterdam, Dublin, Paris, Munich, Zurich, Stockholm, Barcelona, Madrid, Milan, Vienna, Prague, Warsaw, Brussels, Copenhagen

**Asia Pacific:** Singapore, Sydney, Melbourne, Tokyo, Hong Kong, Seoul, Taipei, Kuala Lumpur, Jakarta, Bangkok, Shanghai, Beijing

**Canada:** Toronto, Vancouver, Montreal, Ottawa, Calgary, Waterloo

**Middle East:** Dubai, Abu Dhabi, Riyadh, Tel Aviv, Doha

**Latin America:** Sao Paulo, Mexico City, Buenos Aires, Bogota, Santiago

**Africa:** Johannesburg, Cape Town, Lagos, Nairobi, Cairo

For unlisted cities, the skill falls back to text-based search. You can also add custom geo IDs in `config.json`.

## Output Format

The scraper returns JSON with job details including:

- **title**: Job title
- **company**: Company name
- **location**: Job location
- **employment_type**: Full-time, Part-time, Contract, etc.
- **experience_level**: Entry level, Mid-Senior, etc.
- **posted_date**: When the job was posted
- **requirements**: Experience requirements extracted from description
- **tech_stack**: Technologies mentioned (Python, TensorFlow, AWS, etc.)
- **role_summary**: Brief description of the role
- **url**: Direct link to apply

## Formatting Job Notifications

When presenting new jobs to the user, format them clearly:

```
Found X new jobs for "[keywords]":

━━━ [Location] ━━━

1. [Title] @ [Company]
   📍 [Location] ([Remote/Hybrid/On-site])
   💼 [Employment Type] | [Experience Level]
   🕐 Posted [time ago]
   
   📋 Requirements:
   • Experience: [requirements]
   • Tech Stack: [tech_stack]
   • Role: [role_summary]
   
   🔗 [url]
```

## User Intent Mapping

| User Says | Action |
|-----------|--------|
| "Search LinkedIn for X jobs in Y" | Run one-time search with linkedin_scraper.py |
| "Monitor LinkedIn for X jobs" | Add profile with linkedin_cron.py add |
| "Add X jobs in Y to my searches" | Add profile with linkedin_cron.py add |
| "Search for AI Engineer, ML Engineer, Data Scientist in Bengaluru" | Add multiple profiles with comma-separated keywords |
| "Monitor these roles: X, Y, Z in location" | Add multiple profiles at once |
| "Stop searching for X" | Disable or remove profile |
| "Show my job searches" | Run linkedin_cron.py list |
| "Check for new jobs" | Run linkedin_cron.py run |
| "Clear job history" | Run linkedin_cron.py clear-history |

## Default Filters

When the user doesn't specify filters, use these defaults (configurable in config.json):
- **Experience**: Entry level (code: 2)
- **Remote**: On-site + Hybrid (codes: 1,3)
- **Date Posted**: Last 24 hours (code: r86400)
- **Max Pages**: 2 (~50 jobs)

## Filter Code Reference

**Experience Levels (`--experience`):**
- 1 = Internship
- 2 = Entry level
- 3 = Associate
- 4 = Mid-Senior level
- 5 = Director
- 6 = Executive

**Job Types (`--job-type`):**
- F = Full-time
- P = Part-time
- C = Contract
- T = Temporary
- I = Internship

**Remote Options (`--remote`):**
- 1 = On-site
- 2 = Remote
- 3 = Hybrid

**Date Posted (`--date-posted`):**
- r86400 = Last 24 hours
- r604800 = Last week
- r2592000 = Last month

## Cron Setup (Optional)

Once you've configured your search profiles, you can ask the agent to set up automated monitoring:

- "Run my LinkedIn job searches every hour"
- "Check for new jobs every 30 minutes"
- "Set up daily job monitoring at 9 AM"

The agent will configure the appropriate cron schedule in OpenClaw based on your preference.
