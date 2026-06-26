---
name: linkedin-automator-enhanced
description: Automate LinkedIn content creation, posting, engagement tracking, and audience growth. Use for posting content, scheduling posts, analyzing engagement metrics, generating content ideas, commenting on posts, and building LinkedIn presence. Requires browser access with LinkedIn logged in.
metadata: {"openclaw":{"emoji":"💼","requires":{"tools":["browser"]}}}
---

# LinkedIn Automator

Automate your LinkedIn presence: post content, track engagement, generate ideas, and grow your audience.

## Prerequisites

1. Browser tool enabled in OpenClaw
2. LinkedIn logged in via browser (use profile with LinkedIn session)

## Browser Cleanup Requirement

**CRITICAL:** All scripts that use `openclaw browser` commands MUST clean up tabs after execution to prevent accumulation.

### Updated Pattern (Selective Cleanup - Baseline Comparison)

**This pattern preserves pre-existing tabs and only closes tabs opened during script execution:**

```bash
# Global variable to store baseline tabs
BASELINE_TABS=""

# Capture baseline BEFORE any browser actions
capture_baseline_tabs() {
    BASELINE_TABS=$(openclaw browser tabs 2>/dev/null | grep -oE '\[t[0-9]+' | sed 's/\[//g' | sort -u || echo "")
}

# Cleanup function - closes ONLY tabs opened during script execution
cleanup_browser_tabs() {
    CURRENT_TABS=$(openclaw browser tabs 2>/dev/null | grep -oE '\[t[0-9]+' | sed 's/\[//g' | sort -u || echo "")
    
    # Find NEW tabs (not in baseline)
    NEW_TABS=$(comm -13 <(echo "$BASELINE_TABS") <(echo "$CURRENT_TABS") 2>/dev/null || echo "")
    
    # Close only new tabs
    echo "$NEW_TABS" | while read TAB_ID; do
        [[ -n "$TAB_ID" ]] && openclaw browser close "$TAB_ID" 2>/dev/null || true
    done
}

# Capture baseline immediately (before first browser command)
capture_baseline_tabs

# Set EXIT trap for cleanup (runs on success or failure)
trap cleanup_browser_tabs EXIT
```

**Benefits of this approach:**
- ✅ Preserves pre-existing tabs from other concurrent processes
- ✅ Automatically handles auxiliary tabs (reCAPTCHA, blob URLs, etc.)
- ✅ Works even if script fails mid-execution (EXIT trap)
- ✅ No need to track individual tab IDs

### Legacy Pattern (Label-Based - Still Valid for Simple Cases)

```bash
# 1. Label tabs when opening
openclaw browser open --label "my-tab-label" https://...

# 2. Set EXIT trap for cleanup
cleanup_browser_tabs() {
    TABS=$(openclaw browser tabs 2>/dev/null || echo "")
    TAB_ID=$(echo "$TABS" | grep "my-tab-label" | head -1 | sed -n 's/.*\[\(t[0-9]*\).*/\1/p')
    [[ -n "$TAB_ID" ]] && openclaw browser close "$TAB_ID"
}
trap cleanup_browser_tabs EXIT
```

**Use label-based pattern when:**
- Script is simple (1-2 tabs)
- No concurrent browser usage expected
- Don't need to handle auxiliary tabs

### Pattern for Agent Execution

```bash
# After completing browser workflow:
# Find tab by label and close with short ID (e.g., t74)
openclaw browser tabs | grep "my-tab-label" | sed -n 's/.*\[\(t[0-9]*\).*/\1/p' | xargs -I {} openclaw browser close {}
```

### Verify No Accumulation

```bash
openclaw browser tabs  # Check tab count before/after runs
```

### Reference Implementation

See `scripts/analytics-extract.sh` for a complete example with:
- Baseline capture before first browser command
- Re-capture after browser auto-start (if needed)
- Selective cleanup preserving pre-existing tabs
- Logging and verification

## Quick Commands

```bash
# Post content (feed post, up to 3,000 chars)
{baseDir}/scripts/post.sh "Your post content here"

# Post with image
{baseDir}/scripts/post.sh "Content" --image /path/to/image.png

# Publish native article (long-form, up to 120,000 words, Google-indexed)
{baseDir}/scripts/article.sh --title "Title" --subtitle "Subtitle" --content "Content" [--cover-image /path/to/image]

# Get engagement stats for recent posts
{baseDir}/scripts/analytics.sh

# Generate content ideas based on trending topics
{baseDir}/scripts/ideas.sh [topic]

# Engage with feed (like/comment on relevant posts)
{baseDir}/scripts/engage.sh --limit 10
```

## Workflows

### Posting Content (Feed Posts)

Use browser automation to post:

1. Navigate to linkedin.com/feed
2. Click "Start a post" button
3. Enter content in the post editor
4. Optionally attach media
5. Click "Post" button

For scheduled posts, use OpenClaw cron:
```
cron add --schedule "0 9 * * 1-5" --payload "Post my LinkedIn content: [content]"
```

### Publishing Articles (Native Long-Form)

Use browser automation to publish articles (up to 120,000 words, searchable on Google):

1. Navigate to linkedin.com/feed
2. Click "Write article" button (top of feed, near "Start a post")
3. In the article editor:
   - Enter title
   - Enter subtitle (optional)
   - Write content with rich formatting (H1/H2, bold, lists, images, embeds)
   - Upload cover image (optional)
4. Click "Publish" button
5. Article appears in your Activity section permanently

**Article vs Post:**
| Feature | Post | Article |
|---------|------|---------|
| Length | 1,200-3,000 chars | 120,000 words |
| Google-indexed | ❌ No | ✅ Yes |
| Lifespan | 24-72 hours | Permanent |
| Editor | Simple | Rich (H1-H6, images, embeds) |
| Location | Feed | Activity section |

### Content Strategy

See [references/content-strategy.md](references/content-strategy.md) for:
- High-engagement post formats
- Best posting times by region
- Hashtag strategies
- Hook templates

### Engagement Automation

See [references/engagement.md](references/engagement.md) for:
- Comment templates
- Engagement workflows
- Growth tactics

### Analytics Tracking

The analytics script extracts:
- Impressions per post
- Engagement rate (likes + comments + shares / impressions)
- Profile views trend
- Follower growth
- Top performing content themes

## Browser Selectors

Key LinkedIn selectors (as of 2026):

```
# Posts
Post button: button[aria-label="Start a post"]
Post editor: div.ql-editor[data-placeholder]
Submit post: button.share-actions__primary-action

# Articles
Write article button: button containing "Write article" (top of feed)
Article title: input[placeholder*="title"] or h1[contenteditable]
Article body: div[contenteditable="true"] or div.editor-content
Publish button: button containing "Publish"

# General
Like button: button[aria-label*="Like"]
Comment button: button[aria-label*="Comment"]
Profile stats: section.pv-top-card-v2-ctas
```

## Rate Limits

LinkedIn enforces activity limits. Stay under:
- Posts: 2-3 per day max
- Articles: 1-2 per day recommended
- Comments: 20-30 per day
- Connection requests: 100 per week
- Profile views: Natural browsing pace

## Troubleshooting

- **Login required**: Ensure browser profile has active LinkedIn session
- **Rate limited**: Reduce activity, wait 24h
- **Selector not found**: LinkedIn may have updated UI, check selectors
- **Article editor not loading**: Try desktop browser (mobile has limited editor support)
- **Tabs accumulating**: Scripts use selective cleanup (baseline comparison). If tabs remain:
  ```bash
  # Verify cleanup trap exists in script
  grep "trap cleanup" scripts/analytics-extract.sh
  
  # Check what the script considers "new tabs" (debug)
  # Run this DURING script execution to see baseline vs current
  
  # Manually close LinkedIn-related tabs if needed (use short tab IDs like t74)
  openclaw browser tabs | grep linkedin.com | sed -n 's/.*\[\(t[0-9]*\).*/\1/p' | \
    while read tab; do openclaw browser close "$tab"; done
  ```
- **Zombie tabs after script run**: Script may have crashed before cleanup, OR tabs were pre-existing (preserved by design). Verify:
  ```bash
  # Check if tabs were pre-existing (not script-created)
  openclaw browser tabs
  
  # If truly zombie tabs, close by label pattern
  openclaw browser tabs | grep "linkedin-analytics-tab" | sed -n 's/.*\[\(t[0-9]*\).*/\1/p' | xargs -I {} openclaw browser close {}
  openclaw browser tabs | grep "linkedin-activity-tab" | sed -n 's/.*\[\(t[0-9]*\).*/\1/p' | xargs -I {} openclaw browser close {}
  
  # Nuclear option: Close ALL tabs (use with caution - closes pre-existing too)
  openclaw browser tabs | grep -oE '\[t[0-9]+' | sed 's/\[//g' | while read tab; do openclaw browser close "$tab"; done
  ```
- **Browser unresponsive**: Restart browser (nuclear option):
  ```bash
  openclaw browser stop
  openclaw browser start
  ```
