---
name: linkedin-content-optimizer-engagement-booster
description: "Analyze LinkedIn engagement patterns, optimize posting times, rewrite content for maximum reach, and automate personalized outreach sequences. Use when the user needs LinkedIn growth strategy, audience analysis, or connection re-engagement campaigns."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["LINKEDIN_API_KEY","OPENAI_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🔗"}}
---

## Overview

LinkedIn Content Optimizer & Engagement Booster is a comprehensive AI-powered skill that transforms your LinkedIn presence from passive to strategic. This skill automatically analyzes your network's engagement patterns, identifies your most receptive audience segments, and generates data-driven content recommendations—all without manual analysis.

**Why This Matters:**
- **Time Savings**: Automate 6+ hours/week of LinkedIn strategy planning
- **Data-Driven Decisions**: Replace guesswork with engagement analytics
- **Revenue Impact**: Identify and re-engage high-value dormant connections for pipeline generation
- **Content Multiplier**: Transform mediocre drafts into viral-ready posts in seconds

**Key Integrations:**
- LinkedIn API (posts, analytics, connection data)
- OpenAI GPT-4 (content rewriting, personalization)
- Google Sheets API (engagement tracking & reporting)
- Slack (notifications for optimal posting times)
- HubSpot CRM (prospect behavior sync)

---

## Quick Start

Try these prompts immediately to see the skill in action:

```
Analyze my last 30 LinkedIn posts and tell me which connection clusters 
(by industry/role) engaged most. When should I post to reach each cluster?
```

```
I have this draft: "Excited to announce our Q4 product launch! 
We've been working hard on this." Rewrite it for maximum engagement 
with a hook, social proof mention, and CTA.
```

```
Generate a 5-email re-engagement sequence for dormant connections 
in the tech/VC space who engaged heavily 6+ months ago but haven't 
interacted recently. Personalize by their last viewed content.
```

```
Show me my top 50 high-value connections (by engagement + company size) 
and create personalized outreach messages based on their recent activity, 
posts they've liked, and mutual connections.
```

```
Create a content calendar for next week optimized for my audience. 
Include posting times, content themes, and hashtag recommendations 
based on my engagement data.
```

---

## Capabilities

### 1. **Engagement Pattern Analysis**
Analyzes 90 days of your LinkedIn activity to identify:
- **Connection Clusters**: Groups connections by industry, seniority, company size, geography
- **Engagement Scores**: Ranks which clusters engage most (likes, comments, shares, profile views)
- **Content Performance**: Maps post type (article, carousel, video, text) to engagement by cluster
- **Timing Intelligence**: Identifies optimal posting windows for each cluster (e.g., "Tech founders engage 7-9am ET on Tuesdays")

**Usage Example:**
```
"Show me engagement heatmaps: which of my connections are most engaged 
by industry, and what time should I post to reach them?"
```

### 2. **Content Rewriting & Optimization**
Transforms your LinkedIn drafts into high-performing posts:
- **Hook Optimization**: Generates 3 attention-grabbing opening lines
- **Social Proof Integration**: Adds credibility markers (metrics, testimonials, third-party validation)
- **Emotional Triggers**: Rewrites for curiosity, urgency, or aspiration
- **CTA Optimization**: Suggests conversion-focused calls-to-action (profile visits, DMs, link clicks)
- **Emoji & Formatting**: Applies visual hierarchy for mobile readability
- **A/B Variants**: Creates 2-3 versions for testing different messaging angles

**Usage Example:**
```
"Rewrite this for maximum engagement: 'We just hit $1M ARR.' 
Make it vulnerable, add context, and include a CTA that drives 
meaningful conversation."
```

### 3. **Dormant Connection Re-engagement**
Intelligently identifies and re-engages cold connections:
- **Dormancy Detection**: Flags high-value connections who haven't engaged in 60+ days
- **Value Scoring**: Prioritizes by company size, industry relevance, past engagement level
- **Behavior Recovery**: Pulls their last 10 liked posts, commented threads, and viewed profiles
- **Personalized Sequences**: Generates multi-touch campaigns referencing their specific interests
- **Timing Optimization**: Staggers touches across 2-4 weeks to avoid spam perception

**Usage Example:**
```
"Find my top 100 dormant connections in enterprise SaaS/tech VC who 
engaged heavily in Q1-Q2. Create a 4-email re-engagement campaign 
that references their interests without being salesy."
```

### 4. **Prospect Behavior Analysis & Outreach**
Generates hyper-personalized outreach based on real behavior:
- **Profile Stalking Intelligence**: Analyzes prospect's recent posts, comments, profile changes
- **Content Affinity**: Identifies topics they engage with most
- **Mutual Connection Mapping**: Finds warm intro paths
- **Role-Specific Templates**: Customizes messaging for different buyer personas
- **Conversation Starters**: Suggests specific posts or articles to reference in DM

**Usage Example:**
```
"Create personalized outreach for 20 VCs who recently liked posts 
about AI infrastructure. Reference their recent activity and suggest 
a specific mutual connection for warm intro."
```

### 5. **Content Calendar & Strategy**
Builds week-by-week content plans:
- **Theme Recommendations**: Suggests content pillars based on top-performing topics
- **Posting Schedule**: Distributes posts across optimal times for each audience cluster
- **Content Mix**: Balances thought leadership, educational, personal, and promotional content
- **Hashtag Strategy**: Recommends 5-7 hashtags per post for discoverability
- **Series Planning**: Suggests multi-post threads and carousel formats

**Usage Example:**
```
"Build a 4-week content calendar for B2B SaaS founders. Mix thought 
leadership, case studies, and personal wins. Schedule around my 
audience's peak engagement times."
```

---

## Configuration

### Required Environment Variables

```bash
# LinkedIn API Authentication
export LINKEDIN_API_KEY="your_linkedin_api_key_here"
export LINKEDIN_ACCESS_TOKEN="your_oauth_token"

# OpenAI for Content Generation
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4"  # or gpt-4-turbo

# Optional: Google Sheets for Reporting
export GOOGLE_SHEETS_API_KEY="your_google_api_key"
export GOOGLE_SHEETS_ID="your_spreadsheet_id"

# Optional: Slack Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: HubSpot Sync
export HUBSPOT_API_KEY="your_hubspot_key"
```

### Setup Instructions

1. **LinkedIn API Access**: Request access at [LinkedIn Developers](https://www.linkedin.com/developers/apps)
   - You'll need a registered app with `r_liteprofile`, `r_basicprofile`, and `r_organization_social` permissions

2. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Recommended: GPT-4 for best content quality (GPT-3.5 works but less nuanced)

3. **Optional Google Sheets Integration**: Enable Google Sheets API and create a service account

4. **Test Your Setup**:
```bash
# Verify LinkedIn API connection
curl -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  https://api.linkedin.com/v2/me

# Verify OpenAI API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Advanced Options

```yaml
# engagement_analysis:
#   lookback_days: 90
#   min_connection_cluster_size: 5
#   engagement_weight_factors:
#     comment: 3.0
#     share: 2.5
#     like: 1.0
#     profile_view: 0.5

# content_rewriting:
#   tone: "professional_yet_approachable"
#   target_engagement_rate: 8.5
#   include_emoji: true
#   max_length: 1300

# reengagement:
#   dormancy_threshold_days: 60
#   min_historical_engagement: 3
#   sequence_length: 4
#   days_between_touches: 7

# outreach:
#   personalization_depth: "high"
#   include_mutual_connections: true
#   max_prospects_per_batch: 50
```

---

## Example Outputs

### Engagement Pattern Analysis Output

```json
{
  "analysis_period": "2024-01-01 to 2024-03-31",
  "total_posts": 28,
  "average_engagement_rate": "6.2%",
  "connection_clusters": [
    {
      "cluster_name": "Enterprise SaaS CTOs",
      "cluster_size": 247,
      "avg_engagement_rate": "9.8%",
      "top_content_types": ["technical articles", "product launches"],
      "optimal_posting_time": "Tuesday 8:00-9:00 AM ET",
      "growth_trajectory": "+15% month-over-month"
    },
    {
      "cluster_name": "Marketing Leaders",
      "cluster_size": 189,
      "avg_engagement_rate": "7.2%",
      "top_content_types": ["case studies", "thought leadership"],
      "optimal_posting_time": "Wednesday 2:00-3:00 PM ET",
      "growth_trajectory": "+8% month-over-month"
    }
  ],
  "recommendations": [
    "Post technical deep-dives on Tuesdays for CTOs",
    "Increase carousel format posts (3.2x engagement vs. single image)",
    "Test video content with Marketing Leaders cluster"
  ]
}
```

### Content Rewriting Output

```markdown
**Original Draft:**
"Excited to announce our Q4 product launch! We've been working hard on this."

---

**Version 1 - Curiosity Hook:**
"We spent 6 months rebuilding our core product. The results? 40% faster, 
60% fewer bugs, and something we haven't seen competitors ship yet.

Here's what changed (and why it matters for your workflow):
[details]

What would you want to see in a product like this?"

**Version 2 - Vulnerability Hook:**
"Honest confession: our product was broken. Our best customers were 
frustrated. So we did something crazy—we rebuilt it from scratch.

This is the story of how we went from 'please fix this' to 'this is 
exactly what we needed'..."

**Version 3 - Social Proof Hook:**
"When 3 Fortune 500 companies independently requested the same feature, 
we knew we had to act. Today, we're shipping something that changes 
how enterprise teams work."

---

**Recommended CTA:** "What's one feature you'd add? Drop it in the comments—
we're reading every single one."

**Optimal Posting Time:** Tuesday 8:15 AM ET (based on your CTO cluster)
**Predicted Engagement Rate:** 9.2% (vs. your 6.2% average)
**Recommended Hashtags:** #ProductLaunch #SaaS #TechInnovation #EngineeringLeadership
```

### Dormant Connection Re-engagement Campaign

```markdown
**Target Segment:** 47 VCs & Angel Investors (dormant 90+ days, previously engaged)

**Campaign: "Remember When" - 4-Touch Sequence**

---

**Touch 1 - Day 1 (LinkedIn Post Engagement)**
Post about recent funding/product milestone. Tag 5 of these VCs in comments.

*Example:* "Shoutout to @VCLeader1 and team—your Q2 thesis on AI infrastructure 
is exactly what we're building. Would love to reconnect."

---

**Touch 2 - Day 7 (Personalized DM)**
"Hi [Name],

I noticed you engaged heavily with posts about [Topic] back in Q2. 
We've just shipped something in that space, and I think you'd find it 
interesting given your recent [Company] investment in [Related Area].

Would you have 15 min next week for a quick call? No pitch—just thought 
you'd want to see where the market is heading."

---

**Touch 3 - Day 14 (Value-First Article Share)**
Share a relevant article/report with personalized note:

"[Name], saw this article on [Topic] and immediately thought of our 
conversation about [Specific Point]. Your perspective on this would be 
valuable—curious if you're seeing this play out with your portfolio?"

---

**Touch 4 - Day 21 (Warm Intro Request)**
"One last thought: I noticed you're connected with [Mutual Contact]. 
They'd be a great person to get your take on what we're building. 
Would you be open to a 3-way intro?"

---

**Expected Outcomes:**
- Response Rate: 15-22% (vs. 3-5% cold outreach)
- Meeting Rate: 6-9% of responses
- Pipeline Value: $2.1M (based on your typical deal size)
```

### Personalized Prospect Outreach

```markdown
**Prospect:** Sarah Chen | VP Product @ TechScale | 847 followers

**Engagement Profile:**
- Last 10 posts: 3 likes, 1 comment (low engagement, but high-quality accounts)
- Content interests: AI/ML infrastructure, product metrics, remote culture
- Recent activity: Liked post about "AI model optimization" (3 days ago)
- Mutual connections: 2 (including your former colleague Alex)

---

**Personalized DM Strategy:**

**Option A - Content Reference (Warmest):**
"Sarah, saw you engaged with the AI optimization post last week. 
We're actually solving that exact problem for enterprise teams—
would love your perspective on whether it's a real pain point in your 
market. 15 min call?"

**Option B - Mutual Connection (Warm):**
"Sarah, I noticed we're both connected with Alex Rodriguez. He mentioned 
you're building out TechScale's product infrastructure—sounds like an 
interesting challenge. Would be great to compare notes on how we're 
approaching similar problems. Free for coffee next week?"

**Option C - Insight Share (Value-First):**
"Sarah, been following your product work at TechScale. Built a framework 
for measuring product velocity that might be useful for your team—happy 
to share. Would love to get your feedback."

---

**Warm Intro Request (if no DM response in 5 days):**
"Alex, I noticed you're connected with Sarah Chen at TechScale. 
We're working on problems I think she'd find interesting. Would you 
be comfortable making a quick intro?"
```

---

## Tips & Best Practices

### 1. **Maximize Engagement Pattern Analysis**
- Run analysis weekly, not monthly, to catch emerging trends
- Focus on clusters with 50+ connections for statistical significance
- Track which posting times shift seasonally (summer vs. fall engagement patterns differ)
- **Pro Tip**: Test posting at the recommended time for 2 weeks before adjusting—one week isn't enough data

### 2. **Content Rewriting Best Practices**
- Always start with your authentic voice—don't let AI completely rewrite your personality
- Use Version 1 for thought leadership, Version 2 for personal/vulnerable content, Version 3 for announcements
- Test CTAs: "Drop a comment" drives engagement; "Schedule a call" drives conversions
- **Pro Tip**: Pair AI rewrites with your unique data/stories—"We analyzed 10,000 X and found Y" outperforms generic advice
- Include numbers: posts with specific metrics get 2.3x more engagement than vague claims

### 3. **Re-engagement Campaign Execution**
- Don't blast all 4 touches at once—space them 7 days apart minimum
- Personalize at least the first touch with a specific reference to their recent activity
- A/B test: send Version A to half, Version B to other half; measure response rates
- **Pro Tip**: Re-engage the "warm dormant" (engaged 60-120 days