---
name: juicer-social-listening
description: Social listening for any topic, product category or industry using Juicer. Pulls recent posts from Reddit, TikTok, X, YouTube, Instagram, Bluesky and more, then summarises what people say, the recurring questions and complaints and the posts worth reading, with links. Use for "what are people saying about X", "trend research", "audience research", "content ideas from real conversations", "find real quotes for an article".
version: 1.0.1
metadata:
  openclaw:
    emoji: "👂"
    homepage: https://developers.juicer.io/mcp-server
    primaryEnv: JUICER_API_KEY
    envVars:
      - name: JUICER_API_KEY
        required: false
        description: Optional. Only needed when the Juicer MCP server is not connected. Get one at https://www.juicer.io/developer
---

# Social listening with Juicer

Goal: a digest of what real people are saying about a topic right now, grounded in posts the user can click. Good for research, content ideas and articles that are not generic AI text.

## Set up the search

1. Make sure Juicer is connected (see the `juicer` skill).
2. Ask for the topic and turn it into search terms per network:
   - **Reddit**: 1 to 3 keyword phrases with `term_type: mentions`, plus the 1 to 3 subreddits where the topic lives with `term_type: channel` (e.g. `webdev`, `marketing`).
   - **TikTok**: the keyword phrase with `term_type: mentions`, and the main hashtag.
   - **YouTube, Instagram, X, Bluesky, LinkedIn, Pinterest**: the main hashtags (`#veganprotein`). These networks do not support keyword search, so hashtags are the way in.
3. Show the user the plan and the credit cost before running: Reddit, X, YouTube, Bluesky and Pinterest 1 credit per call; Instagram, TikTok and LinkedIn 3; Facebook 6. A typical run (3 Reddit + TikTok + 2 hashtags on Instagram and YouTube) costs about 10 credits. Check the balance with `get_account`.

## Run

Call `get_data_posts` once per term and network. Fetch more pages (`cursor`) only for the networks where the first page was mostly on topic.

- Reddit returning `fetch_timeout` ("Reddit request timed out"): Reddit is slow at times. Retry it once at the end of the run (1 credit). If it fails again, say "Reddit could not be reached, so Reddit is not covered" and never report it as "no mentions on Reddit".

## Analyse

1. Drop posts that only share a word with the topic (a "#protein" post about haircare is noise). Count what you dropped.
2. Drop exact duplicates and cross-posts.
3. Group what is left into 3 to 6 themes. For each theme: one sentence, how many posts, and 1 or 2 short real quotes with links.
4. Pull out separately:
   - **Questions people ask** (content and FAQ ideas).
   - **Complaints and frustrations** (product and positioning ideas).
   - **Top posts** by engagement (`like_count`, `comment_count`) per network.
5. Quote only text that is in the posts. Never paraphrase a post and present it as a quote.

## Digest format

Template (fill every [ ] from the run, never from this example):

```
[Topic], last [n] days · [n] posts read, [n] on topic

Themes
1. [Theme in a few words] ([n] posts)
   "[exact quote from a post]" · [where]
   [link]
2. ...

Questions people ask
- [Question] ([n] posts)

Top posts
- [Network] · @[poster]: [n] likes · [link]

Searched: [each network and term]. [n] credits used, [n] left.
```

## Repeat

Offer a weekly version with an OpenClaw Automation (scheduled job). In repeat runs, show what changed: new themes, themes growing or fading.

## Honest limits

- Data lookups return recent posts, best effort per network, not a full archive. Say "in the posts we found", never "on all of TikTok".
- No keyword search on Instagram, Facebook or LinkedIn.
- If a network returns nothing or times out, say so in the searched line.
