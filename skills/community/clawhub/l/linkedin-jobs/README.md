# LinkedIn Jobs Skill for OpenClaw

Search and monitor LinkedIn job listings with powerful filters, city-based searches, and smart deduplication.

## Features

- **City-based search**: 100+ tech hubs worldwide with precise geo IDs
- **Hourly monitoring**: Set up cron jobs to track new listings
- **Smart deduplication**: Only see truly new jobs
- **Detailed notifications**: Tech stack, experience requirements, role summary
- **Fully configurable**: Customize defaults, scraper behavior, and more

## Installation

```bash
clawhub install linkedin-jobs
```

Or manually:
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/linkedin-jobs.git
cd linkedin-jobs
pip install -r requirements.txt
```

## Quick Start

Just tell your OpenClaw agent:

```
"Search LinkedIn for AI Engineer jobs in Bengaluru"
"Monitor Python Developer jobs in San Francisco every hour"
"Add ML Engineer positions in Berlin to my job searches"
"Search for AI Engineer, ML Engineer, Data Scientist jobs in Noida"
"Show my job searches"
"Check for new jobs now"
```

### Multiple Job Titles

You can search for multiple roles at once using comma-separated keywords:

```
"Add AI Engineer, ML Engineer, RAG Engineer, Data Scientist to my Bengaluru job searches"
```

This creates separate profiles for each role with the same location and filters, and automatically deduplicates results across all of them.

## Configuration

Copy `config.example.json` to `config.json` to customize:

```bash
cp config.example.json config.json
```

### Default Filters

```json
{
  "defaults": {
    "experience": "2",        // Entry level
    "remote": "1,3",          // On-site + Hybrid
    "date_posted": "r86400",  // Last 24 hours
    "max_pages": 2            // ~50 jobs per search
  }
}
```

### Filter Codes Reference

**Experience Levels:**
| Code | Level |
|------|-------|
| 1 | Internship |
| 2 | Entry level |
| 3 | Associate |
| 4 | Mid-Senior level |
| 5 | Director |
| 6 | Executive |

**Remote Options:**
| Code | Type |
|------|------|
| 1 | On-site |
| 2 | Remote |
| 3 | Hybrid |

**Date Posted:**
| Code | Period |
|------|--------|
| r86400 | Last 24 hours |
| r604800 | Last week |
| r2592000 | Last month |

## Supported Cities

### India
Bengaluru, Noida, Hyderabad, Mumbai, Delhi NCR, Pune, Chennai, Gurugram, Kolkata, Ahmedabad, Jaipur, Chandigarh, Kochi, Coimbatore, Indore, Lucknow, and more.

### USA
San Francisco, New York, Seattle, Austin, Boston, Los Angeles, Chicago, Denver, San Diego, Washington DC, Atlanta, Dallas, Houston, Phoenix, Miami, Portland, and more.

### UK
London, Manchester, Edinburgh, Cambridge, Oxford, Bristol, Birmingham, Leeds, Glasgow, Belfast.

### Europe
Berlin, Amsterdam, Dublin, Paris, Munich, Zurich, Stockholm, Barcelona, Madrid, Milan, Vienna, Prague, Warsaw, Brussels, Copenhagen, and more.

### Asia Pacific
Singapore, Sydney, Melbourne, Tokyo, Hong Kong, Seoul, Taipei, Kuala Lumpur, Jakarta, Bangkok, Shanghai, Beijing, and more.

### Canada
Toronto, Vancouver, Montreal, Ottawa, Calgary, Waterloo.

### Middle East
Dubai, Abu Dhabi, Riyadh, Tel Aviv, Doha.

### Latin America
Sao Paulo, Mexico City, Buenos Aires, Bogota, Santiago.

### Africa
Johannesburg, Cape Town, Lagos, Nairobi, Cairo.

## Adding Custom Cities

Edit `config.json` and add your city's geo ID:

```json
{
  "custom_geo_ids": {
    "my city": "123456789"
  }
}
```

**How to find a geo ID:**
1. Go to [linkedin.com/jobs](https://linkedin.com/jobs)
2. Search for jobs in your city
3. Look at the URL for `geoId=XXXXXX`
4. Add that number to your config

## Cron Setup (Optional)

Once you've configured your search profiles, ask your OpenClaw agent to set up automated monitoring:

- "Run my LinkedIn job searches every hour"
- "Check for new jobs every 30 minutes"  
- "Set up daily job monitoring at 9 AM"

The agent will configure the appropriate cron schedule based on your preference.

## Commands

| Command | Description |
|---------|-------------|
| `python linkedin_scraper.py --keywords "..." --location "..."` | One-time search |
| `python linkedin_cron.py add --keywords "..." --location "..."` | Add search profile |
| `python linkedin_cron.py add --keywords "A, B, C" --location "..."` | Add multiple profiles at once |
| `python linkedin_cron.py list` | List all profiles |
| `python linkedin_cron.py run` | Run all enabled profiles |
| `python linkedin_cron.py run --profile <id>` | Run specific profile |
| `python linkedin_cron.py enable --profile <id>` | Enable profile |
| `python linkedin_cron.py disable --profile <id>` | Disable profile |
| `python linkedin_cron.py remove --profile <id>` | Remove profile |
| `python linkedin_cron.py clear-history` | Clear seen jobs |
| `python linkedin_cron.py stats` | View statistics |

## Example Notification

```
Found 3 new jobs for "AI Engineer":

━━━ Bengaluru, India ━━━

1. AI Engineer @ Google
   📍 Bengaluru, Karnataka (Hybrid)
   💼 Full-time | Entry level
   🕐 Posted 2 hours ago
   
   📋 Requirements:
   • Experience: 0-2 years
   • Tech Stack: Python, TensorFlow, PyTorch, GCP
   • Role: Build ML models for search ranking
   
   🔗 linkedin.com/jobs/view/123456

━━━ San Francisco, USA ━━━

2. ML Platform Engineer @ Stripe
   📍 San Francisco, CA (Remote)
   💼 Full-time | Entry level
   🕐 Posted 4 hours ago
   
   📋 Requirements:
   • Experience: 1+ years Python
   • Tech Stack: Python, Kubernetes, AWS, Spark
   • Role: Scale ML infrastructure
   
   🔗 linkedin.com/jobs/view/789012
```

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill definition for OpenClaw |
| `linkedin_scraper.py` | Core scraper with CLI |
| `linkedin_cron.py` | Cron runner with deduplication |
| `geo_ids.json` | 100+ city geo IDs |
| `config.example.json` | Configuration template |
| `search_profiles.json` | Your saved searches (auto-created) |
| `seen_jobs.json` | Seen job tracker (auto-created) |

## Requirements

- Python 3.9+
- requests
- beautifulsoup4

## License

MIT License - see [LICENSE](LICENSE)

## Contributing

1. Fork the repository
2. Add your improvements
3. Submit a pull request

### Adding New Cities

PRs welcome for adding geo IDs to `geo_ids.json`!

## Disclaimer

This skill uses LinkedIn's public job search endpoint. Use responsibly and respect LinkedIn's terms of service. The default rate limiting (1.5-3.5s delays) helps avoid issues.
