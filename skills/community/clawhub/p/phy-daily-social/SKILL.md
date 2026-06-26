---
name: daily-social
description: Daily social media routine for indie developers and founders. Runs a structured 15-20 minute engagement routine across Reddit, Twitter/X, LinkedIn, and 小红书. Triggers on "/daily-social", "daily social routine", "social media check", "15 min social", or "do my social today".
metadata: {"category": "social-media", "duration": "15-20min", "platforms": ["reddit", "twitter-x", "linkedin", "xiaohongshu"], "features": ["karma-tracking", "opportunity-finding", "engagement-logging", "weekly-review"]}
---

# Daily Social Media Routine

A structured 15-20 minute daily routine to build indie developer presence consistently.

---

## Execution Flow

When this skill is triggered, execute in order:

### Step 1: Status Check (1 min)

**Reddit:**
- Check current karma score on your Reddit profile
- Compare to previous day's snapshot to calculate delta
- Note post karma vs comment karma breakdown

**Other platforms to check:**
- Twitter/X — follower count, recent engagement
- LinkedIn — connection requests, post performance

### Step 2: Reddit Engagement (5 min)

Navigate to target subreddits and find engagement opportunities:

**Target subreddits (sorted by priority):**
1. `r/SideProject` — rising posts
2. `r/indiehackers` — new posts with questions
3. `r/ClaudeAI` — if relevant to AI work
4. `r/coolgithubprojects` — if you have something to share

**Action:** Find 2-3 posts to comment on. For each, identify:
- Post title
- Current engagement (upvotes, comments)
- Suggested angle for your comment

**Comment principles:**
- Add genuine value before mentioning your project
- Answer the question fully, project mention is secondary
- Be specific, not generic ("I built X that does Y" not "check out my tool")
- 100-200 word comments perform best

### Step 3: Twitter/X Scan (3 min)

Check for:
- Mentions to respond to
- Threads from key accounts to engage with
- Trending topics in your niche (DTC / AI / indie hacking / SaaS)

**Key account categories to check:**
- DTC / ecom voices in your space
- Indie hackers with active discussions
- Recent AI / tool discussions relevant to your product

### Step 4: LinkedIn Quick Check (2 min)

Check for:
- Connection requests (accept relevant ones)
- Comments on recent posts
- Posts from target accounts to engage with

**LinkedIn engagement rules:**
- Thoughtful comments on others' posts build more credibility than posting
- Target: 3-5 meaningful comments per week, not per day
- Prioritize founders and potential customers over peers

### Step 5: Action Items (2 min)

Present a prioritized list of today's tasks:

```
Today's Social Tasks:

Reddit:
[ ] Comment on "[Post 1 title]" — [suggested angle]
[ ] Comment on "[Post 2 title]" — [suggested angle]

Twitter/X:
[ ] Reply to [mention or thread]
[ ] Engage with [account]'s post about [topic]

LinkedIn:
[ ] Accept [N] connection requests
[ ] Comment on [post] from [person]
```

### Step 6: Log Engagement

After completing actions, record what was done:

```
Date: [date]
Reddit: [N] comments, topics: [areas]
Twitter: [N] engagements
LinkedIn: [N] actions
Time spent: [X] min
Karma change: +[N]
```

### Step 7: Content Opportunity (Optional)

If there is bandwidth, suggest:
- Topic for an original post based on today's engagement patterns
- Repurpose opportunity from high-performing older content

---

## Database Tracking (Optional)

If you have a database connected, track the following:

**Tables:**
- `reddit_account_stats` — karma snapshots over time
- `reddit_opportunities` — posts identified as engagement opportunities
- `reddit_engagement_log` — activity tracking

**Snapshot fields:**
```json
{
  "username": "your_username",
  "karma": 1240,
  "post_karma": 340,
  "comment_karma": 900,
  "snapshot_at": "2025-03-06T08:00:00Z"
}
```

**Opportunity fields:**
```json
{
  "subreddit": "SideProject",
  "post_id": "abc123",
  "post_title": "...",
  "post_url": "https://reddit.com/r/...",
  "upvotes": 45,
  "comments_count": 12,
  "suggested_angle": "Share your tech stack approach"
}
```

**Engagement log fields:**
```json
{
  "subreddit": "SideProject",
  "action_type": "comment",
  "target_post_title": "...",
  "target_post_url": "...",
  "karma_before": 1200,
  "karma_after": 1240
}
```

---

## Browser Automation

Use Playwright or browser tools to check platforms without logging in repeatedly:

```
# Reddit profile check
Navigate to: https://reddit.com/user/{your_username}/
Snapshot: extract karma values

# Subreddit scan
Navigate to: https://reddit.com/r/SideProject/rising
Navigate to: https://reddit.com/r/indiehackers/new
Snapshot: list of post titles, upvotes, comment counts

# Twitter check
Navigate to: https://twitter.com/notifications
Snapshot: pending mentions and replies
```

---

## Quick Commands Within Routine

User can say:
- `"skip reddit"` — Skip Reddit phase
- `"reddit only"` — Only do Reddit engagement
- `"just scan"` — Status check only, no action items
- `"post something"` — Switch to content creation mode

---

## Integration with Other Skills

| Need | Invoke |
|------|--------|
| Draft Reddit comment | `/reddit-cultivate` |
| Draft Twitter thread | Your twitter content skill |
| Draft LinkedIn post | Your linkedin content skill |
| Create content | `/founder-content` |
| Post to platforms | `/social-posting` |

---

## Tracking

After each session, optionally append to a log file:

```
[2025-03-06]
Reddit: 2 comments (r/SideProject, r/indiehackers)
Twitter: 3 engagements
LinkedIn: 1 comment, 2 connections accepted
Time: 18 min
Karma: 1200 → 1240 (+40)
```

---

## Weekly Review (Saturday)

On Saturdays, run an extended version:

1. Karma/follower changes over the week
2. Best-performing content from the week
3. Engagement rate trends
4. Plan next week's original content topics

**Weekly report summary:**
```
Week of [date]:
- Reddit karma: [start] → [end] (+[delta])
- Comments posted: [N] across [subreddits]
- Twitter followers: [start] → [end]
- LinkedIn connections: +[N]
- Best performing content: [title/link]
- Next week plan: [2-3 content ideas]
```

---

## Subreddit Guide

| Subreddit | Best For | Post Types to Engage |
|-----------|----------|---------------------|
| `r/SideProject` | Project launches, indie devs | Show HN-style posts, help requests |
| `r/indiehackers` | Revenue/growth discussions | Milestone posts, questions |
| `r/ClaudeAI` | AI tooling audience | Use cases, comparisons |
| `r/coolgithubprojects` | Open source visibility | Project showcases |

**Engagement rate benchmark:**
- Getting 5+ upvotes on a comment = good
- Getting 20+ upvotes = very good, reuse the angle
- Getting replies = best signal, the community is engaging

---

## Rate Limiting Notes

- Wait 2+ seconds between page loads when scraping
- Do not post more than 5 comments in a single session
- Space Reddit comments at least 5 minutes apart to avoid spam filters
- New accounts need 100+ karma before links are not filtered
