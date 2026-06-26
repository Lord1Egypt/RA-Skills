---
name: niche-twitter
description: Specialized Twitter/X discovery, analysis, content generation, and strategy for niche topics: ClawHub/AI agents, WHL hockey scouting, acreage/land dev, Saskatchewan housing, indie hackers. Use when: finding niche experts/accounts, trend/hashtag research, generating threads/polls/replies, Twitter growth strategies, monitoring mentions. Examples: &quot;WHL scouts on Twitter&quot;, &quot;ClawHub twitter thread&quot;, &quot;#ReginaRealEstate trends&quot;. Leverages web_search, browser snapshots, advanced operators.
---

# Niche Twitter

## Overview
Master niche Twitter engagement: Find hidden gems (accounts, threads), craft viral content, build strategies tailored to Thomas&#39;s worlds (hockey, AI/ClawHub, acreage biz).

Key wins:
- Expert discovery in 5min searches
- Thread templates for quick posts
- Local Sask focus (hockey, housing)
- Autonomous monitoring via cron/web_search

## Triggers
Direct mentions or implied:
- &quot;twitter [niche]&quot;, &quot;x.com [topic]&quot;
- &quot;find influencers [domain]&quot;
- &quot;generate twitter thread [idea]&quot;
- Hashtags: #ClawHub, #WHL, #AcreageLife, #IndieHackers
- Goals: growth, leads, research

## Workflow Decision Tree
```
Query?
├── Discovery/Research → Research Phase
├── Generate Content → Content Gen Phase
├── Strategy/Analysis → Strategy Phase
└── Monitor/Alerts → Monitoring Phase
```

## 1. Research Phase (Discovery)
**Goal:** Top accounts, trends, conversations.

1. Advanced web_search:
   ```
   web_search &quot;[niche] twitter OR x.com (experts OR influencers OR &quot;top accounts&quot;) 2026&quot; country=&quot;CA&quot; freshness=&quot;pm&quot;
   web_search &quot;#[niche] OR &quot;[niche] twitter&quot; trends OR viral&quot;
   ```
   Niche ex: &quot;WHL scouting twitter&quot;, &quot;ClawHub skills influencers&quot;

2. Browser validation:
   ```
   browser action=&quot;snapshot&quot; targetUrl=&quot;https://twitter.com/search?q=[query]&amp;f=live&quot; refs=&quot;aria&quot;
   ```

3. Extract: Followers, bio keywords, post engagement. Table format.

**See:** [references/advanced-search.md](references/advanced-search.md)

## 2. Content Generation
**Frameworks:** PAS (Problem-Agitate-Solution) for threads.

1. Research hook: Pain/trend from search.
2. Generate 1-3 variants (short/long).
3. Format: Numbered thread, emojis, CTA.

Ex thread (ClawHub promo):
```
1/10 Ever built an AI agent that actually *sticks* around? 

ClawHub skills = plug-n-play superpowers for OpenClaw.

Thread: [benefits]
#ClawHub #AIAgents
```

**Script:** `exec scripts/format-thread.py &quot;[content]&quot;`

**Template:** [assets/thread-template.md](assets/thread-template.md)

## 3. Strategy Phase
- Best times: Evenings CST (hockey fans), weekdays for devs.
- Growth: Engage top 10 accounts/week.
- Tools: message for polls, tts for voice threads(?).

## 4. Monitoring
Proactive cron: web_search &quot;[niche] twitter mentions {today}&quot; → notify.

## Examples

**&quot;Find top acreage twitter accounts Sask&quot;**
| Account | Followers | Bio Snippet | Why Follow |
|---------|-----------|-------------|------------|
| @SaskLand | 5k | Acreage expert | Local tips |

**Thread Gen:** &quot;Hockey scouting evolution&quot; → 8-post thread.

## Pro Tips
- X.com > twitter.com for new UI.
- country=&quot;CA&quot; for local relevance.
- Parallel tools: search + browser.
- Publish-ready: Copy-paste to X.
