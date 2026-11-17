---
name: juicer-competitor-checker
description: Compare a brand's social media with its competitors using Juicer. Finds each competitor's verified accounts on Instagram, TikTok, X, YouTube, LinkedIn, Facebook and Bluesky, then reports followers, posting frequency, top posts and hashtags side by side, with a short "what to copy" list. Use for "check my competitors", "competitor social media analysis", "what is [brand] posting", "benchmark us against".
version: 1.0.1
metadata:
  openclaw:
    emoji: "🥊"
    homepage: https://developers.juicer.io/mcp-server
    primaryEnv: JUICER_API_KEY
    envVars:
      - name: JUICER_API_KEY
        required: false
        description: Optional. Only needed when the Juicer MCP server is not connected. Get one at https://www.juicer.io/developer
---

# Competitor checker with Juicer

Goal: a side-by-side view of the user's brand and up to 4 competitors: who posts how often, what gets engagement and what the user should try next.

## Step 1: find the right accounts

1. Make sure Juicer is connected (see the `juicer` skill).
2. Ask for the user's brand and competitors (names, websites or handles) and which networks matter.
3. Resolve handles with `get_data_profiles` (up to 5 handles per call, comma-separated, no `#`; use platform name `Twitter` for X profiles).
4. **Verify every account before using it.** An exact handle match is often someone else. Keep an account only if its `description`, `display_name` or `url` clearly matches the company (name plus what they do, or their website). If there is no clear match on a network, mark it "not found" rather than picking the closest candidate.
5. **Before writing "not found", search wider.** Brands often use a different handle per network (the X account is @brandio, the Instagram is @brandsocial). Try, in one `get_data_profiles` call per network: the handles already confirmed on other networks, the plain brand name, the name with `social`, `app`, `hq` or `official` added, and any handle linked from the brand's website. Only then mark the network "not found", and list the handles you tried.
6. Show the user the confirmed accounts and ask them to correct any before you spend more credits.

Profile lookups cost 1 credit per call on most networks, 3 on Instagram, TikTok and LinkedIn, 6 on Facebook.

## Step 2: pull recent posts

For each confirmed account call `get_data_posts` with the `@handle` on its network (one page each). Tell the user the total cost first: for 3 brands on Instagram, TikTok and X that is (3 + 3 + 1) × 3 = 21 credits. Check the balance with `get_account`.

## Step 3: compare

Per brand and network, from the data returned:

- **Followers** (`follower_count` from the profile).
- **Posting frequency**: posts per week across the dates in the page you fetched.
- **Engagement**: average likes and comments per post, and engagement per 1,000 followers so small and big accounts compare fairly.
- **Top 3 posts** by likes plus comments, with link and the first line of text.
- **Formats** that appear in their top posts (video, image, carousel) when the media type is present.
- **Hashtags** they repeat.

Only use numbers from the API response. If a field is missing, write "n/a", do not estimate.

## Report format

Template (fill every [ ] from the run, never from this example):

```
Competitor check · [date] · last [n] posts per account

[Network]          Followers  Posts/wk  Avg eng.  Eng/1k
You (@[handle])    [n]        [n]       [n]       [n]
[Competitor] (@[handle])  ...

What works for them
- [Pattern seen in their top posts, with links]

Try next
1. [Idea tied to a post above]
2. ...

Not found: [competitor] on [network] (tried @[handle], @[handle]).
Used [n] credits, [n] left.
```

Keep "Try next" to 3 concrete ideas, each tied to a post in the data.

## Repeat

Offer a weekly or monthly run with an OpenClaw Automation (scheduled job). Repeat runs should show the change since last time (followers, posting frequency) and only new top posts.

## Honest limits

- Only public accounts and recent posts; this is a sample, not a full history. Say how many posts per account the numbers are based on.
- Views are not available on every network; do not compare views across networks.
