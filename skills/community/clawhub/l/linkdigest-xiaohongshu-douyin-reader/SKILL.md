---
name: linkdigest-xiaohongshu-douyin-reader
description: "Read a Xiaohongshu (RedNote) or Douyin link in English. Use when the user shares a xiaohongshu.com, xhslink.com, rednote.com, douyin.com or v.douyin.com link and wants to know what the post says: the caption, the text inside the images (OCR), the spoken transcript of the video, on-screen captions, likes and saves, hashtags, or an English translation. No Chinese phone number, app, login or cookie needed. Reads through the LinkDigest API; needs LINKDIGEST_API_KEY. Pay as you go: an image note is 1 credit (about $0.02), 10 free credits on sign-up."
version: 1.0.0
homepage: https://linkdigest.dev/docs
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3","curl"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API key (starts with ld_live_). Create one at https://linkdigest.dev/app/keys"}],"homepage":"https://linkdigest.dev/docs"}}
---

# Xiaohongshu (RedNote) & Douyin Reader

Chinese social posts are hard to read from outside China. Xiaohongshu shows a login wall or an "open in app" page to a plain fetch, and most of an image note's content is written inside the pictures. Douyin videos carry their content in speech and burned-in captions. This skill hands the link to LinkDigest and gets back text an agent can work with, and translates it to English when asked.

## Quick start

```bash
export LINKDIGEST_API_KEY=ld_live_...   # create at https://linkdigest.dev/app/keys (10 free credits, no card)
python3 {baseDir}/scripts/linkdigest.py "<link or the whole share text>" --translate-to en
```

The script uses only the Python standard library. It prints Markdown by default; add `--format json` for structured fields. The whole share text copied from the app works as input: the link is picked out on the server.

## What comes back

For a Xiaohongshu image note:
- title, author, post date, caption, hashtags;
- likes, saves, comments and shares as the platform reported them that day;
- every image in order: a description and the text written on it;
- key points, each with a short quote checked word for word against the post.

For a Douyin or Xiaohongshu video:
- the spoken transcript with timecodes;
- on-screen text with approximate times;
- the post's own chapters and category when Douyin provides them;
- key points with checked quotes.

For both:
- `translation` (with `--translate-to en`): title, caption, key points, transcript and image text in English. The Chinese original stays beside it, so quotes can be checked.
- `coverage`: a receipt of how much was read (seconds transcribed, images read) and a plain list of what was not.
- `links`: links and QR codes the post points to. They are listed, never opened.

## When to use it, and when not

Use it when the user gives one post link and asks what it says, wants it summarised or translated, or wants the text for research on a product, a trend or a competitor.

Do not use it to search Xiaohongshu or Douyin, read comments, list a creator's posts, download media, post or like. It reads one public post per call. Private, deleted or login-only posts cannot be read (HTTP 422, no charge).

## Options

- `--translate-to en` (or `ja`, `ko`, `es`, ...): adds the translation, +1 credit.
- `--breakdown`: adds a structure analysis of the post (hook, beats with timestamps, title formula, reusable template), +1 credit.
- `--depth transcript`: for long videos. Full transcript with a few frames, 1 credit per 2 minutes instead of 1 per minute.
- `--max-credits N`: never spend more than N credits on this link.
- `--partial-ok`: when a video is longer than the budget allows, read the opening part instead of refusing.
- `--job-id <id>`: collect a job that was still running.

Exit codes: 0 done; 3 bad key; 4 not enough credits (nothing charged; a payment link is printed); 5 link cannot be read (nothing charged); 6 rate limited; 7 still running, collect with `--job-id`.

## Cost

One credit is about $0.02 on the $5 pack (250 credits; cards, or Alipay in CNY).

| Read | Credits |
| --- | --- |
| Image note, up to 6 images | 1 |
| Each further 6 images | +1 |
| Video, per started minute | +1 on top of the base 1 |
| Long video with `--depth transcript`, per started 2 minutes | +1 on top of the base 1 |
| Translation, breakdown | +1 each |
| A link anyone has read before (cached) | 0 |
| A link that cannot be read | 0 |

Ten free credits on sign-up, once. Current prices: https://linkdigest.dev/pricing

## Tips for links

- Use the link from the app's Share → Copy link. Keep its parameters; Xiaohongshu refuses links without the `xsec_token` part.
- `rednote.com` links are the same notes as `xiaohongshu.com` and work the same way.
- A Douyin short link (`v.douyin.com/...`) and the full address of the same video cost one read, not two.

## Telling the user

Give the translated text when they asked in English, and say which parts are the post's own words (caption, transcript, image text, counts) and which were written by a model (image descriptions, key points, translation). Mention anything in `coverage.not_captured`, and how many credits the call used.

## Privacy

The link is the only thing sent, and only to linkdigest.dev. No Xiaohongshu or Douyin account is used. Media is fetched to a temporary folder for the read and deleted. Text results are cached per link, so the same public post is free to read again and may be served to others who ask for the same link; do not submit private links. `scripts/linkdigest.py` reads one environment variable, `LINKDIGEST_API_KEY`, talks to one host, and writes no files. Details: https://linkdigest.dev/privacy

Other ways in: remote MCP at `https://linkdigest.dev/mcp` (tool `digest_url`), OpenAPI at https://linkdigest.dev/openapi.json, source and examples at https://github.com/jcaiagent7143-ui/linkdigest-mcp. Questions: support@linkdigest.dev
