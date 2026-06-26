---
name: icecube-reddit-scout
description: "🧊 IceCube Reddit Scout — Free Reddit keyword monitoring integrated with your AI agent. No SaaS subscription. No cloud dependency. Track mentions, validate ideas, find leads. When users mention 'Reddit monitoring', 'keyword alerts', 'track mentions', 'GummySearch replacement', 'brand monitoring', 'lead generation from Reddit'."
metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# 🧊 IceCube Reddit Scout

**Free Reddit monitoring. Integrated with your agent.**

GummySearch is dead. F5Bot solves 10% of the workflow. Paid alternatives cost $50-200/month.

IceCube Reddit Scout gives you the other 90% for free.

## What This Skill Does

### 1. Keyword Monitoring
- Track keywords across any subreddit
- Get alerts when mentions appear
- No subscription, no rate limits

### 2. Context Extraction
- Don't just get alerts — get **context**
- Auto-extract: thread sentiment, user intent, engagement signals
- Filter noise automatically

### 3. Lead Identification
- Detect buying intent signals
- "I wish there was a tool for..."
- "Anyone know how to..."
- "Looking for recommendations..."

### 4. Opportunity Mining
- Find pain points in discussions
- Validate product ideas
- Track competitor mentions

## Setup

### 1. Configure Keywords

Create `config/reddit-scout.yaml`:
```yaml
keywords:
  - "openclaw"
  - "AI agent"
  - "memory system"
  - "context window"

subreddits:
  - "r/indiehackers"
  - "r/SaaS"
  - "r/startups"
  - "r/artificial"

filters:
  intent_signals:
    - "wish"
    - "need"
    - "looking for"
    - "recommendations"
    - "alternatives"
  noise_filter:
    - exclude_self_mentions: true
    - min_score: 5
    - exclude_downvoted: true

alerts:
  channels:
    - telegram
    - memory_log
  frequency: 1h
```

### 2. Reddit Native Alerts (Free)

Reddit now has built-in keyword alerts. Use them:

1. Go to Reddit settings → Notifications
2. Enable "keyword alerts"
3. Add your keywords
4. Get email notifications

IceCube Reddit Scout reads these emails and extracts context.

### 3. Polling Mode (Alternative)

If you don't want Reddit alerts:
```yaml
mode: polling
poll_interval: 30m
```

Uses Reddit search API to check for new mentions.

## Commands

### Add Keyword
```bash
curl -s "https://www.reddit.com/search.json?q=openclaw&sort=new&limit=10"
```

### Monitor Subreddit
```bash
curl -s "https://www.reddit.com/r/indiehackers/search.json?q=memory+system&sort=new&limit=25"
```

### Check Trends
```bash
curl -s "https://www.reddit.com/r/indiehackers/hot.json?limit=50"
```

## Workflow Integration

### Step 1: Detection
Agent polls Reddit every 30 minutes (cron job or heartbeat).

### Step 2: Extraction
When keyword found:
- Extract thread title, content, score, comments
- Detect intent signal (wish/need/looking_for)
- Calculate relevance score

### Step 3: Alerting
If relevance > threshold:
- Write to `memory/reddit-mentions/YYYY-MM-DD.md`
- Send Telegram notification (if configured)
- Add to `unclosed_work.yaml` if action needed

### Step 4: Response
Agent can:
- Log for later analysis
- Draft reply (human approves)
- Track competitor activity
- Capture pain point for product ideas

## Output Format

**memory/reddit-mentions/2026-03-31.md:**
```markdown
# Reddit Mentions — 2026-03-31

## RM-001 (14:32)
- Subreddit: r/indiehackers
- Thread: "I wish there was a tool that could remember my agent context"
- Intent: wish (high)
- Score: 42
- Sentiment: positive
- Opportunity: IceCube Memory candidate user
- Link: https://reddit.com/r/indiehackers/comments/xxx
- Action: Log for marketing outreach

## RM-002 (15:15)
- Subreddit: r/SaaS
- Thread: "GummySearch alternatives that don't cost $200/month"
- Intent: looking_for_alternatives (high)
- Score: 87
- Sentiment: frustrated
- Opportunity: IceCube Reddit Scout pitch
- Link: https://reddit.com/r/SaaS/comments/yyy
- Action: Draft reply for human approval
```

## Comparison

| Feature | GummySearch | F5Bot | Paid Alternatives | IceCube Scout |
|---------|-------------|-------|-------------------|---------------|
| Price | Dead | Free | $50-200/mo | **Free** |
| Cloud | Yes | Yes | Yes | **No** |
| Context extraction | Manual | Manual | Some | **Auto** |
| Intent detection | Manual | No | Yes | **Auto** |
| Agent integration | No | No | No | **Yes** |
| Response drafting | No | No | Some | **Yes** |
| Memory logging | No | No | No | **Yes** |

## Use Cases

### 1. Brand Monitoring
Track when people mention your product/project.

### 2. Lead Generation
Find people asking for solutions you offer.

### 3. Idea Validation
Capture pain points for product development.

### 4. Competitor Tracking
Monitor competitor mentions and sentiment.

### 5. Trend Detection
Spot emerging topics in your niche.

## Integration with IceCube Suite

**icecube-memory:** Mentions logged to memory structure
**icecube-heartbeat:** Polling triggered during heartbeat
**icecube-evolution:** Pain points feed improvement queue

## ⚠️ Important: Reddit API Access Required (2026)

As of 2026, Reddit has **blocked all anonymous API access**. You MUST use one of these methods:

### Method 1: Reddit OAuth (Recommended)
1. Create a Reddit app at https://www.reddit.com/prefs/apps
2. Configure OAuth credentials in `config/reddit-scout.yaml`
3. Get 60 requests/min with proper authentication

```yaml
oauth:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  user_agent: "IceCube-Reddit-Scout/1.0 by YOUR_REDDIT_USERNAME"
```

### Method 2: Browser Automation (peekaboo skill)
- Use the peekaboo skill to access Reddit via browser
- Slower but no API limits
- Works for logged-in Reddit users

### Method 3: F5Bot + Local Processing
- Use F5Bot for keyword alerts (free)
- Process alerts locally with IceCube Scout
- Combines free alerting with agent integration

## Limitations

- Reddit API requires OAuth (no anonymous access)
- Polling mode not real-time (30 min intervals)
- No DM automation (Reddit policy)
- Reddit may still block even OAuth requests if rate limits exceeded

## Advanced: OAuth Integration

For higher rate limits:
1. Create Reddit app at https://www.reddit.com/prefs/apps
2. Configure OAuth credentials
3. Get 60 requests/min

```yaml
oauth:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  redirect_uri: http://localhost:8080
```

## License

MIT — Use freely.

---

*GummySearch is dead. F5Bot is 10%. IceCube Scout is the 90%.*