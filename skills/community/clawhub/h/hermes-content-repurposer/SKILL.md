---
name: ai-content-repurposer
description: Takes one long-form piece of content and repurposes it into Twitter threads, LinkedIn posts, newsletter editions, and short video scripts.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ffmpeg
    category: Automation
---

# AI Content Repurposer

## Name & Purpose
Takes one long-form piece of content (article, blog post, video transcript, podcast episode) and intelligently repurposes it into multiple platform-optimised formats: Twitter threads, LinkedIn posts, newsletter editions, and short video scripts. Eliminates the "create once, post once" waste.

## Prerequisites

| Requirement | Version/Detail |
|---|---|
| OpenClaw | v2.4+ |
| Python 3 | v3.10+ |
| FFmpeg | v4.4+ (for video excerpts) |
| NLP libraries | See requirements.txt |
| API Key (optional) | ElevenLabs for voiceover scripts |

## Installation

### 1. Copy skill files

```bash
cp -r streams/01_ClawHub_Skills/02_AI_Content_Repurposer/* ~/.openclaw/skills/
```

### 2. Install dependencies

```bash
cd ~/.openclaw/skills/ai-content-repurposer
pip install -r requirements.txt
```

### 3. Configure

Edit `config/repurpose.yaml` with your brand voice preferences:

```yaml
brand:
  name: "YourBrand"
  voice: "professional-but-warm"
  industry: "tech"
  target_audience: "SaaS founders and marketers"
  tone_adjectives: ["confident", "insightful", "approachable"]
  hashtags:
    default: ["#YourBrand", "#Industry"]
    twitter: ["#YourBrand"]
    linkedin: ["#YourBrand", "#IndustryInsights"]
  cta:
    default: "Want more? Subscribe to our newsletter."
    newsletter: "Loved this? Get more insights delivered weekly."

output_formats:
  twitter_thread:
    enabled: true
    max_tweets: 15
    max_chars_per_tweet: 280
    include_cta: true
  linkedin_post:
    enabled: true
    max_chars: 3000
    include_hashtags: true
    include_cta: true
  newsletter:
    enabled: true
    max_chars: 5000
    include_header: true
    include_footer: true
  video_script:
    enabled: true
    max_duration_seconds: 60
    include_timestamps: true
    format: "tiktok"  # Options: tiktok, youtube_shorts, instagram_reels
  tweet:
    enabled: true
    max_chars: 280
    count: 5
```

## Usage

### Repurpose a single piece of content

```bash
# From a URL (article, blog, transcript)
openclaw skill run ai-content-repurposer --input https://example.com/blog-post

# From a local file
openclaw skill run ai-content-repurposer --input ./my-article.md

# From a YouTube video (auto-transcribe)
openclaw skill run ai-content-repurposer --input https://youtube.com/watch?v=XXXX
```

### Specify output platforms

```bash
# All platforms
openclaw skill run ai-content-repurposer --input article.md --output all

# Specific platforms
openclaw skill run ai-content-repurposer --input article.md --output twitter,newsletter

# Just video scripts
openclaw skill run ai-content-repurposer --input transcript.md --output video_script
```

### Batch process

```bash
openclaw skill run ai-content-repurposer --batch ./content_queue/ --output all
```

## Workflow

```
Source Content (article/transcript/video) 
  → Extract Core Narrative (key points, quotes, data, angle)
  → Platform Router
     ├── Twitter Thread: Hook → Tweets (numbered) → CTA
     ├── LinkedIn Post: Headline → Body (with line breaks) → Hashtags
     ├── Newsletter: Subject → Intro → Sections → Outro
     └── Video Script: Hook → Scene breakdown → Voiceover text
  → Quality Checks (character limits, tone alignment, quote accuracy)
  → Output Files (saved to ./output/{platform}/)
```

## Available Commands

| Command | Description |
|---|---|
| `/status` | Show queue depth, recent jobs, completion stats |
| `/queue` | List items waiting for processing |
| `/outputs` | Show recent output files |
| `/schedule <cron>` | Set recurring schedule (e.g., `/schedule "0 8 * * 1-5"`) |
| `/config` | Show current repurpose configuration |
| `/preview <job_id>` | Preview outputs before publishing |

## Repurposing Templates

Templates define *how* each platform's output is structured. Edit `./templates/`.

```
templates/
├── twitter_thread/
│   └── default.yaml
├── linkedin/
│   ├── thought_leader.yaml
│   ├── company_page.yaml
│   └── short_tip.yaml
├── newsletter/
│   ├── weekly_digest.yaml
│   └── deep_dive.yaml
├── video_script/
│   ├── tiktok.yaml
│   ├── youtube_shorts.yaml
│   └── instagram_reels.yaml
└── quality_checks.yaml
```

### Twitter Thread Template (default.yaml)

```yaml
structure:
  hook:
    type: "question_or_controversial_opener"
    length: "1 tweet"
    rules:
      - "Start with a bold claim or surprising question"
      - "Hook must fit in 280 chars"
  body:
    type: "numbered_tweets"
    count: "8-15"
    rules:
      - "Each tweet = 1 idea maximum"
      - "Include line breaks within tweets for readability"
      - "Number tweets: 1/10, 2/10, etc."
      - "Quote exact source where needed"
  cta:
    type: "final_tweet"
    rules:
      - "Summarise or give opinion"
      - "Add CTA: follow, retweet, subscribe"
      - "Include 2-3 relevant hashtags"
  spacing:
    type: "smart_delay"
    config:
      initial_delay_minutes: 0
      tweet_interval_minutes: 3
      thread_label: true
```

### LinkedIn Post Template (thought_leader.yaml)

```yaml
structure:
  headline:
    type: "bold_claim"
    length: "1-3 lines"
    rules:
      - "Lead with the contrarian take or key insight"
      - "Use all caps for emphasis on 2-3 words max"
  body:
    type: "story_problem_solution"
    sections:
      - name: "context"
        length: "2-4 lines"
      - name: "problem"
        length: "3-5 lines"
      - name: "insight"
        length: "4-6 lines"
      - name: "actionable_takeaway"
        length: "3-5 lines"
    rules:
      - "Keep paragraphs to 2-3 lines max (mobile readability)"
      - "Use bullet points for lists"
      - "Include 1-2 line breaks between sections"
  engagement:
    type: "question"
    rules:
      - "End with an open-ended question to drive comments"
  hashtags:
    count: "3-5"
    rules:
      - "Mix broad (#Marketing) and niche (#SAFounders) tags"
```

## Quality Checks

The system runs automated quality checks on every output before saving:

```yaml
# templates/quality_checks.yaml
checks:
  - name: character_limits
    description: "Enforce platform-specific length limits"
    severity: error
  - name: tone_alignment
    description: "Check output matches brand voice configuration"
    severity: warning
    threshold: 0.7 # confidence score
  - name: quote_accuracy
    description: "Ensure quotes from source are exact"
    severity: error
  - name: link_integrity
    description: "Verify all links are from trusted domains"
    severity: warning
  - name: duplicate_content
    description: "Flag near-duplicate sentences across outputs"
    severity: warning
  - name: hashtag_relevance
    description: "Check hashtags match content topic"
    severity: warning
  - name: cta_presence
    description: "Every output must have a CTA"
    severity: error
```

## Input Format Spec

The system accepts these input formats:

| Format | Extension | Notes |
|---|---|---|
| Markdown | .md | Preferred. Headers = sections |
| Plain text | .txt | Auto-detect paragraphs |
| HTML | .html | Stripped and converted |
| YouTube URL | https://... | Auto-transcribe via subtitles |
| Podcast RSS | https://... | Fetch and transcribe latest episode |
| PDF | .pdf | Text extraction (via PyMuPDF) |
| WordPress URL | https://... | Fetch and parse article content |

## Scheduling

Use cron-style scheduling for regular repurposing:

```bash
# Run every Monday at 8 AM on the latest blog post
openclaw cron add "0 8 * * 1" "ai-content-repurposer --input https://blog.yoursite.com/latest --output all"

# Auto-repurpose RSS feed items as they drop
openclaw skill run ai-content-repurposer --watch-rss https://blog.yoursite.com/feed.xml
```

## Example Prompts for Human Operators

> "Hey Marvis, repurpose this article into a Twitter thread and a LinkedIn post: [URL]"
> "What's in the queue for today's repurposing schedule?"
> "The last TikTok script was too long — tighten it to 30 seconds max."
> "Run quality checks on all pending outputs."
> "Schedule this newsletter draft for Friday at 10 AM."

## Directory Structure

```
ai-content-repurposer/
├── SKILL.md
├── README.md
├── config/
│   ├── repurpose.yaml        # Brand voice & platform config
│   └── sources.yaml          # RSS feeds, WordPress URLs to watch
├── templates/
│   ├── twitter_thread/
│   │   └── default.yaml
│   ├── linkedin/
│   │   ├── thought_leader.yaml
│   │   ├── company_page.yaml
│   │   └── short_tip.yaml
│   ├── newsletter/
│   │   ├── weekly_digest.yaml
│   │   └── deep_dive.yaml
│   ├── video_script/
│   │   ├── tiktok.yaml
│   │   ├── youtube_shorts.yaml
│   │   └── instagram_reels.yaml
│   └── quality_checks.yaml
├── prompts/
│   ├── extract_narrative.yaml
│   ├── twitter_thread.yaml
│   ├── linkedin_post.yaml
│   ├── newsletter.yaml
│   ├── video_script.yaml
│   └── quality_check.yaml
├── output/
│   ├── twitter/              # Generated Twitter threads
│   ├── linkedin/             # Generated LinkedIn posts
│   ├── newsletter/           # Generated newsletter editions
│   └── video/                # Generated video scripts + timestamps
├── scripts/
│   ├── batch.sh              # Batch process directory
│   ├── schedule.sh           # Set up cron jobs
│   └── publish.sh            # Auto-post to social platforms (opt-in)
├── requirements.txt
└── package.json
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| "Content too short" | Source under 500 words | Adjust min_length in repurpose.yaml |
| Twitter threads > 280 chars | Template token budget wrong | Lower `max_chars_per_tweet` |
| Video scripts too wordy | Duration section misconfigured | Check `max_duration_seconds` in template |
| Quotes off by one word | Transcription error | Fix source, re-run with `--force` |
| Newsletter missing sections | Article has no clear structure | Add Markdown headers to source |
| Batch job hangs | One large file blocking queue | Run `--max-size 10000` to split |
| Tone sounds off | Brand voice not configured | Update `config/repurpose.yaml` adjectives |
