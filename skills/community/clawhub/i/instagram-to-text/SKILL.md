---
name: instagram-to-text
description: "Instagram reel and post to text / Instagram 转文字. Use when someone shares an instagram.com/reel/… or /p/… link and wants the spoken script, the words shown on screen, the caption, key points or a summary — for research, notes, competitor analysis or rewriting. Returns the transcript with times, on-screen text, caption, hashtags and engagement counts, without logging in to Instagram. A post is 1 credit; a reel adds 1 per started minute; links anyone has read before are free; failed reads are free. Needs a LinkDigest API key (10 free credits on sign-up, no card)."
version: 1.0.2
homepage: https://linkdigest.dev/platforms?ref=skill-instagram-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API key (starts with ld_live_), create it at https://linkdigest.dev/signin?ref=skill-instagram-to-text&next=/app/keys — 10 free credits on sign-up"}],"homepage":"https://linkdigest.dev/platforms?ref=skill-instagram-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-instagram-to-text&next=/app/keys"
    required_for: "reading Instagram reels and posts; sign-up gives 10 free credits, no card"
---

# Instagram → text

An agent that fetches a reel link from a server usually gets a login prompt or a thin page, and a reel's script is in its audio and on-screen captions anyway, not in the page. This skill reads the reel or post through LinkDigest and hands back text.

## Run it

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-instagram-to-text&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py "https://www.instagram.com/reel/XXXXXXXXXXX/"
```

- `--format json` for structured output.
- `--translate-to zh-CN` (or `en`, `ja` …) adds a translation beside the original, +1 credit.
- `--breakdown` adds a viral breakdown — hook, beats, title formula, a reusable template — +1 credit.
- `--ask "What product does she recommend?"` answers one question from the post, with the quotes it rests on, +1 credit.

## What you get back

A real reel read on 2026-10-27, for scale: one transcript passage and 16 lines of on-screen text, each with the second it appeared.

- **Transcript** — what is said, timed by segment.
- **On-screen text** — captions and titles read from the frames, with times.
- **Caption and hashtags** — as posted.
- **Key points** — each tied to a quote that was found word for word in the reel's own material.
- **Engagement** — likes, comments and views where Instagram shows them, as of the read.

Photo posts (`/p/…`) come back with the caption and the first image described and its text read; for a carousel, only the first slide is read, and the result says so.

## Agent notes

1. When a user pastes an Instagram link and asks what it says, run the script on it. Long reels may first answer with a job id; the script waits and collects it.
2. Give the transcript as-is when they want the script; summarise only when asked, and quote from `key_point_support` entries marked `verified: true`.
3. Tell the user the credits spent (last line on stderr).

## Cost and limits

| Read | Credits |
| --- | --- |
| A photo post | 1 |
| A reel | 1 + 1 per started minute |
| A link anyone has read before | 0 |
| A link that cannot be read | 0 |

Private accounts, deleted posts and stories cannot be read. Out of credits returns 402 and charges nothing; the body carries the buy links (50 credits for $1.50, or ¥9.9 by Alipay; once, no subscription).

## Privacy

Only the link you give is sent to linkdigest.dev. No Instagram login or cookie is used or asked for; media is read and discarded, only the text is kept. https://linkdigest.dev/privacy · Remote MCP: `https://linkdigest.dev/mcp` (`digest_url`) · support@linkdigest.dev
