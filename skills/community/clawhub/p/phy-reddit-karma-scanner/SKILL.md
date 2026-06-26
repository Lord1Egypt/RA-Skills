---
name: reddit-karma-scanner
description: Automated Reddit opportunity scanner that finds high-potential posts for karma building. Scans target subreddits, analyzes engagement patterns, and generates ready-to-post comments using OpenAI. Use when you want to build Reddit karma strategically through quality contributions on r/MachineLearning, r/cscareerquestions, r/artificial, and other tech subreddits.
metadata: {"requires": ["node"], "env": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD", "OPENAI_API_KEY"], "tags": ["reddit", "social-media", "karma", "engagement", "openai"]}
---

# Reddit Karma Scanner

Automated system for finding and engaging with high-potential Reddit opportunities. Designed for strategic karma building through quality technical contributions.

## Quick Setup

### 1. Reddit API Credentials
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_reddit_username"
export REDDIT_PASSWORD="your_reddit_password"
```

Get credentials at: https://www.reddit.com/prefs/apps

### 2. OpenAI API Key
```bash
export OPENAI_API_KEY="your_openai_api_key"
```

### 3. Run a Scan
```bash
node scripts/reddit-scanner.mjs --subreddits "MachineLearning,cscareerquestions" --user-context "Your background description"
```

## Core Features

### Smart Opportunity Detection
- Scans multiple subreddits for rising posts
- Filters by engagement sweet spot (20-100 upvotes, 5-50 comments)
- Identifies 24-48h old posts for optimal timing
- Prioritizes low-competition, high-growth potential

### Context-Aware Comments
- Generates personalized responses using your background
- Maintains professional tone matching your expertise
- Creates value-add content, not generic replies
- Ready-to-copy-paste format

### Anti-Spam Protection
- Max 1-2 opportunities per scan
- Natural posting patterns
- Quality over quantity approach
- Timing optimization to avoid detection

## Strategy Overview

The scanner implements a **quality-first approach**:

1. **Target Selection**: Focus on technical subreddits where expertise matters
2. **Timing Optimization**: Hit posts in their growth phase, not peak
3. **Competition Analysis**: Avoid oversaturated threads
4. **Value Creation**: Generate substantive, helpful comments

## Usage Patterns

### Automated Scanning (Recommended)
Set up cron jobs for regular scanning:

```bash
# 3x daily at optimal Reddit times
30 8,13,22 * * * /path/to/scripts/reddit-scanner.mjs --auto
```

### Manual Opportunity Search
```bash
node scripts/reddit-scanner.mjs --subreddit "MachineLearning" --limit 5
```

### Custom User Context
```bash
node scripts/reddit-scanner.mjs --user-context "Senior ML Engineer at startup" --expertise "computer-vision,nlp"
```

## Configuration

Create `config.json` in the skill directory:

```json
{
  "target_subreddits": ["MachineLearning", "cscareerquestions", "artificial"],
  "user_background": "Your background description",
  "expertise_areas": ["machine-learning", "data-science"],
  "quality_threshold": 40.0,
  "max_opportunities": 2
}
```

## Advanced Features

### User Profile Customization
Tailor comments to your background and expertise. Configure `user_background` and `expertise_areas` in `config.json` to match your professional context.

### Subreddit Strategy
Different subreddits reward different engagement styles:
- **r/MachineLearning**: Deep technical discussion, cite papers
- **r/cscareerquestions**: Practical career advice, share real experience
- **r/artificial**: Broader AI conversation, accessible explanations
- **r/SideProject**: Build-in-public culture, share what you learned

### Engagement Analytics
Track karma growth and comment performance by logging replied post IDs and monitoring upvote velocity over 24-48h windows.

## Scripts Reference

- `reddit.mjs` — Core Reddit API interface (PRAW-compatible OAuth flow)
- `generate-reddit-comments.mjs` — OpenAI-powered comment generation
- `reddit-scanner.mjs` — Main scanning and filtering logic

## Best Practices

1. **Start Conservative**: Begin with 1 scan per day
2. **Monitor Results**: Track which subreddits and comment styles perform best
3. **Stay Authentic**: Use your real expertise and opinions
4. **Engage Genuinely**: Follow up on your comments when appropriate
5. **Respect Communities**: Follow each subreddit's rules and culture

## Troubleshooting

**Rate Limiting**: Reddit allows ~60 requests/minute with auth, 10/minute without. Add `--delay 2000` flag to slow down requests.

**Comment Rejected**: Check subreddit karma/age requirements. New accounts often need 30+ days and 50+ karma before posting in strict subreddits.

**Low Quality Score**: Refine your `user_background` and `expertise_areas` in config. More specific context produces better comments.

**401 Unauthorized**: Re-export credentials and verify your Reddit app type is set to "script" at https://www.reddit.com/prefs/apps.

Built for strategic Reddit engagement that builds genuine reputation through quality contributions.
