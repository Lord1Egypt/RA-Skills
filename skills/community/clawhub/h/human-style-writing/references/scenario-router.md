# Scenario Router (Daily chat + Social media only)

Goal: classify a request into a **scenario_id** so we can apply the right prompt recipe.

This router intentionally supports **only**:
- daily chat / DMs
- social media posts (generic + platform-specific)

## Off-scope guardrail (hard)
If the user asks for **work email/report, academic writing, news/press, customer support templates/macros, marketing copy, or legal/compliance language**:
- do **not** route to those registers
- ask **one** question:
  > “Do you want this rewritten as (A) a DM/text message, or (B) a social post? If social, which platform (X/Reddit/LinkedIn/IG/TikTok/小红书/朋友圈)?”
- then continue with the chosen on-scope scenario

Do not “fake” an academic/news/legal tone inside this skill.

## Output schema (always)
Return these internally (not necessarily shown to user):
- scenario_id: one of the IDs below
- platform: x | reddit | linkedin | instagram | tiktok | xiaohongshu | wechat_moments | generic
- language: zh | en | mixed | other
- formality: 0=very casual, 1=casual, 2=professional-ish, 3=formal
- tone: friendly | neutral | urgent | apologetic | assertive | playful
- audience_relationship: friend | peer | partner | manager | client | public

## Scenario IDs
- daily_chat
- social_generic
- social_x
- social_reddit
- social_linkedin
- social_instagram
- social_tiktok
- social_xiaohongshu
- social_wechat_moments

## Router heuristics (fast, practical)
### Step 1 — Language
- If user writes mostly 中文 or asks “用中文/中文发” → zh
- If mostly English → en
- If they mix languages or request bilingual → mixed

### Step 2 — Explicit platform mapping (highest priority)
If user explicitly mentions:
- “tweet”, “X”, “Twitter”, “thread” → social_x
- “Reddit”, “subreddit”, “r/…”, “comment”, “AMA” → social_reddit
- “LinkedIn” → social_linkedin
- “Instagram”, “IG”, “caption”, “Reel caption” → social_instagram
- “TikTok”, “TT caption” → social_tiktok
- “小红书”, “RedNote”, “笔记”, “种草” → social_xiaohongshu
- “朋友圈”, “WeChat Moments” → social_wechat_moments

### Step 3 — Social vs chat (when platform is not explicit)
- If user says “post”, “caption”, “write a social post”, “make this go viral”, “hook”, “thread”, “headline line 1”, “hashtag” → social_generic
- If it sounds like a 1:1 message (text/DM to a specific person; “text my…”, “message my…”, apology, scheduling, quick question) → daily_chat

### Default
- daily_chat

## When unsure (ask 1 question only)
Ask:
> “Do you want this as (A) a DM/text message, or (B) a social post? If social, which platform (X/Reddit/LinkedIn/IG/TikTok/小红书/朋友圈)?”
