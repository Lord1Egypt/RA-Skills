---
name: linkdigest
description: Read a social media link that returns nothing useful when fetched — Xiaohongshu (小红书), Douyin (抖音), TikTok, YouTube, X, or an ordinary web page. Returns the transcript, the on-screen text, a description of every image, the caption and the metadata. Use whenever a task involves a social link whose content you cannot otherwise see, including when the user pastes one without explaining it.
allowed-tools: mcp__linkdigest__digest_url
---

# Reading social links

Fetching a social media link yourself returns nothing usable. The share URL is
tokenised (`xsec_token`, `app_code_link`), the content lives in video and images
rather than HTML, and the server answers with an app-download shell or a login
wall. On Xiaohongshu that shell is an app page whose `<title>` is the site's
slogan and which holds none of the note.

This tool resolves the link, fetches the media with a warmed session, transcribes
the audio, describes and OCRs every image, and hands back text.

## When to use it

Reach for it the moment a task involves a link you cannot read:

- The user pastes a Xiaohongshu, Douyin, TikTok, YouTube or X link — with or
  without instructions. A bare link is a request to read it.
- A task references a post you need the contents of: "summarise this", "what does
  this creator claim", "pull the steps out of this video"
- You already tried fetching a URL and got an app-download page, a login wall or
  a title with no body

Do **not** use it as a general web scraper. For an ordinary article that fetches
fine, read it directly — this costs credits and takes longer.

## Calling it

```
digest_url(url: "https://v.douyin.com/…")
```

`url` is the only required argument. The others:

- `format` — `markdown` (default, best for reading) or `json` (structured fields)
- `job_id` — collect a digest already running; see below
- `breakdown` — `true` adds a teardown of how the post is built (爆款拆解): the hook,
  timed beats, title formula, call to action and a reusable template. Use it when the
  user wants to learn from or remake a post. +1 credit
- `translate_to` — a language code (`en`, `ja`, `zh-CN`): adds a translation beside
  the original. +1 credit
- `ask` — a question to answer from the post ("what products and prices does it
  recommend?", "does the speaker say X?"). The answer comes with the quotes it rests
  on, each checked against the post; `found` is false when the post does not say. Use
  it when the user asked something specific about the link. +1 credit
- `partial_ok` — `true` reads the opening minutes of a video that is too long for the
  plan, instead of refusing it

## Long videos need two calls

A short post or a cached link comes back immediately. A long video cannot finish
inside one tool call, so the result names a job id instead. When that happens,
call the tool again with that `job_id` and **no url** — re-sending the url starts
the work over and charges for it twice.

```
digest_url(job_id: "abc123…")
```

Wait about 15 seconds between attempts. A Xiaohongshu note with images takes one
to two minutes; a YouTube video with captions about two and a half.

## What comes back

`platform`, `author`, `title`, `posted_at`, `caption`, `transcript` (`{t, text}`;
per line for platform captions, per ~170 s segment for speech recognition),
`ocr_text`, `on_screen` (`{t, text}`, approximate times), `images`
(`{description, ocr}` per image), `key_points`, `stats`, `tags`, `source_url`,
`transcript_source`, `degraded` — plus `breakdown` and `translation` when asked for.

Two of those change how you should use the result:

- **`transcript_source`** is `native_captions`, `asr`, `gemini_video` (an uncaptioned
  YouTube video watched by Gemini) or `none`. Captions the
  platform published are exact; speech recognition is not. If you are about to
  quote a number or a name back to the user as fact, and the source was `asr`,
  say where it came from.
- **`degraded`** lists anything that did not fully work, in plain words. It also
  carries route notes ("read via oEmbed", "read by Gemini watching the video
  directly") on complete digests. When an entry says something could not be
  read or failed, the digest is thinner than the post — do not present it as
  complete.

## Platforms

Works: Xiaohongshu (小红书), Douyin (抖音), TikTok, YouTube, X, ordinary web pages.

Not supported: Bilibili returns HTTP 412 to the service's address. Instagram and
Facebook need a logged-in session for most posts. If the user asks for one of
these, say so rather than trying it.

## Cost

10 free credits to start, once per account, no card. A typical post is one credit
and video adds one per started minute. `breakdown: true` (the hook, timed beats and a
reusable template — 爆款拆解) and `translate_to` add one credit each. Anything anyone
has digested before is served from cache — free, and back in about a second.
