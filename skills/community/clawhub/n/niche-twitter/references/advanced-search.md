# Twitter/X Advanced Search Operators

Use these in web_search query or browser search URL for precise results.

## Core Operators
- **from:username** - Posts from user
- **@username** - Mentions user
- **&quot;exact phrase&quot;** - Exact match
- **word1 OR word2 OR #hashtag** - Alternatives
- **since:YYYY-MM-DD** - After date (e.g., since:2026-03-01)
- **until:YYYY-MM-DD** - Before date
- **min_faves:N** - Min likes (N=50 for popular)
- **min_replies:N** - Min replies
- **filter:verified** - Verified accounts only
- **filter:safe** - No NSFW
- **lang:en** - Language
- **near:Regina** - Location (if supported)

## Niche Examples
**WHL Hockey Scouting:**
```
&quot;WHL scouting&quot; OR &quot;hockey analytics&quot; OR &quot;player eval&quot; filter:verified min_faves:20 since:2026-01-01 lang:en
```

**ClawHub/AI Agents:**
```
ClawHub OR &quot;OpenClaw skills&quot; OR &quot;AI agent skills&quot; -filter:replies min_faves:5 lang:en
```

**Acreage Sask:**
```
acreage OR homesteading OR &quot;land development&quot; near:&quot;Regina, SK&quot; lang:en
```

**Query Gen:** `web_search &quot;[operators] site:twitter.com OR site:x.com&quot;`

## URL Builder
https://twitter.com/search?q=[encoded query]&src=typed_query&f=live
