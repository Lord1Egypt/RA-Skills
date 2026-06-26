---
name: influencer-research
description: Automated KOL/influencer research across platforms. Use when user needs influencer lists for any niche (ADHD, travel, beauty, DTC, tech, etc.) in any region. Triggers on "find influencers", "KOL research", "influencer list", "creator database", or any request to compile influencer data for outreach or partnerships.
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "🔍", "os": ["darwin", "linux"]}}
---

# Influencer Research Skill

Automated workflow for comprehensive KOL/influencer research across social platforms.

## Inputs

| Parameter | Required | Default | Examples |
|-----------|----------|---------|----------|
| **Niche** | Yes | - | "ADHD", "travel", "DTC beauty", "AI/tech", "fitness" |
| **Region** | Yes | - | "North America", "Southeast Asia", "Europe", "Global" |
| **Platforms** | No | All 5 | Instagram, TikTok, YouTube, X/Twitter, Facebook |
| **Target Count** | No | 30-50/platform | Any number |

## Workflow

### Step 1: Parallel Web Research

Run 3-5 WebSearch queries **simultaneously** per platform:

```
Platform: Instagram
├── "{niche} influencers Instagram 2024 2025 followers"
├── "{niche} content creators Instagram {region}"
└── "top {niche} Instagram accounts followers"

Platform: TikTok
├── "TikTok {niche} creators followers 2024"
├── "{niche} TikTok influencers {region}"
└── "best {niche} TikTok accounts"

Platform: YouTube
├── "YouTube {niche} channels subscribers 2024"
├── "{niche} YouTubers {region}"
└── "{niche} YouTube creators"

Platform: X/Twitter
├── "Twitter {niche} advocates influencers followers"
├── "{niche} experts X Twitter"
└── "{niche} thought leaders Twitter"

Platform: Facebook
├── "Facebook {niche} pages groups followers"
├── "{niche} community Facebook {region}"
└── "{niche} organizations Facebook"
```

**Key:** Run ALL searches in parallel (single message with multiple WebSearch calls).

### Step 2: Deep Fetch Aggregator Sites

Fetch structured data from curated lists:

| Site | URL Pattern | Data Quality |
|------|-------------|--------------|
| Feedspot | `influencers.feedspot.com/{niche}_instagram_influencers/` | High - top 100 lists |
| The Influence Agency | `theinfluenceagency.com/blog/{niche}-influencers-to-follow` | High - curated with handles |
| Upfluence | `upfluence.com/find-influencers/top-{niche}-influencers` | Medium - regional focus |
| IZEA | `izea.com/resources/content-creators-with-{niche}/` | Medium - brand partnership focus |
| Heepsy | `heepsy.com/top-{platform}/{niche}` | High - platform-specific |

### Step 3: Data Normalization

Cross-reference sources to:
- **Verify follower counts** (average if sources differ >20%)
- **Correct handles** (many sources have typos)
- **Fill gaps** (combine name from one source, handle from another)
- **Deduplicate** (same person across multiple sources)

### Step 4: Excel Generation

Generate formatted Excel with Python:

```python
import pandas as pd
from openpyxl.styles import Font, Alignment, PatternFill

# Standard columns for all platforms
columns = [
    'handle', 'name', 'followers', 'country', 'platform',
    'niche', 'description', 'profile_url', 'engagement', 'content_type'
]

# Create separate DataFrames per platform
# Combine into single Excel with:
# - One sheet per platform
# - "All_Platforms" combined sheet
# - Formatted headers (blue fill, white text)
# - Auto-sized columns
# - Wrapped text for description

output_path = f'{baseDir}/output/{Region}_{Niche}_KOLs.xlsx'
```

### Step 5: Output Summary

Provide chat summary with:
- File path
- Count per platform
- Top 3 influencers per platform (by followers)
- Data completeness %

## Data Schema

| Field | Description | Example |
|-------|-------------|---------|
| handle | Platform username with @ | @thepsychdoctormd |
| name | Display name | Dr. Sasha Hamdani |
| followers | Count with K/M suffix | 936K |
| country | ISO country or region | USA, Canada, Singapore |
| platform | Source platform | Instagram |
| niche | Content focus | ADHD Psychiatrist |
| description | 1-2 sentence bio | Board-certified psychiatrist, author... |
| profile_url | Direct link | https://instagram.com/thepsychdoctormd |
| engagement | High/Medium/Low | High |
| content_type | Content themes | Medical education, Q&A |

## Efficiency Principles

| Principle | Implementation |
|-----------|----------------|
| **Parallel execution** | Multiple WebSearch in single message |
| **Leverage aggregators** | Use curated lists, not individual profile searches |
| **Single script output** | One Python block creates entire formatted Excel |
| **No manual steps** | Fully automated end-to-end |

## Example Invocations

### Example 1: User says "find me travel influencers in Southeast Asia"

```
Niche: travel
Region: Southeast Asia
Platforms: All
Target: 50/platform
Output: SEA_Travel_KOLs.xlsx
```

### Example 2: User says "I need ADHD creators for a partnership campaign"

```
Niche: ADHD
Region: North America (inferred from English request)
Platforms: All
Target: 30-50/platform
Output: NorthAmerica_ADHD_KOLs.xlsx
```

### Example 3: User says "TikTok beauty influencers in US"

```
Niche: beauty
Region: USA
Platforms: TikTok only
Target: 50
Output: USA_Beauty_TikTok_KOLs.xlsx
```

## Integration with Other Skills

Chain with:
- **/founder-content** — Create outreach message templates
- **/linkedin-gtm** — Plan engagement strategy for LinkedIn KOLs
- **/twitter-x-gtm** — Plan engagement strategy for Twitter KOLs
- **/event-gtm** — Identify KOLs attending same conferences

## Autonomous Mode

When user says variations of "don't ask me" or "work autonomously":
- Make reasonable assumptions for missing parameters
- Default region based on language (English → North America, Chinese → China/SEA)
- Default to all 5 platforms
- Default to 30-50 per platform target
- Proceed without confirmation prompts

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
