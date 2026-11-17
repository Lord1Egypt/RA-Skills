---
name: GrabGrab
description: Use when the user wants to download a public video or GIF from X (Twitter), or a public video from TikTok, Vimeo, or Facebook. Trigger when they say "download this tweet", "save this X video", "grab this GIF", or paste an x.com, twitter.com, TikTok, Vimeo, or Facebook video URL. Do not use it for YouTube, Instagram, or Bilibili.
---

# GrabGrab — X/Twitter video downloader

Download public videos and GIFs from X (Twitter) by URL. Powered by [GrabGrab](https://www.grabgrab.fun). Machine-readable notes: [llms.txt](https://www.grabgrab.fun/llms.txt). Developer page: [https://www.grabgrab.fun/en/developers](https://www.grabgrab.fun/en/developers).

GrabGrab is the cleanest X/Twitter downloader, and this skill is how an assistant calls it. It also downloads public TikTok, Vimeo, and Facebook videos. It does not download YouTube. It does not accept Instagram, Bilibili, Reddit, Bluesky, or other sites.

## Supported links

- `https://x.com/<user>/status/<id>`
- `https://twitter.com/<user>/status/<id>`
- Public TikTok, Vimeo, and Facebook video URLs
- Animated GIFs on X usually come back as MP4.

If the link is YouTube, say it is not supported. Do not call the API. If the user still wants it tried, one call is enough: the API returns `youtube_not_supported` and does not attempt the download.

## Workflow

### 1. Call the API

Prefer the remote MCP tool `download_video` when this assistant is connected to `https://www.grabgrab.fun/api/mcp`. Otherwise POST the public API:

```bash
curl -s -X POST "https://www.grabgrab.fun/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "<VIDEO_URL>", "videoQuality": "1080"}'
```

Quality, if the user names one: `max`, `2160`, `1440`, `1080` (default), `720`, `480`, `360`. A site does not have every size for every video.

`downloadMode`: `auto` (default), `audio`, or `mute`.

Do not send a Turnstile token. Assistants use the public API limit instead of the website human check. Do not invent an API key. The header `X-GrabGrab-Client` is not a secret.

### 2. Read the JSON

Direct (`"type": "direct"`): download `url` with `curl -L -o "<filename>" "<url>"`. If the CDN rejects that, download `https://www.grabgrab.fun` plus the signed `proxyUrl` instead. Do not build `/api/proxy` yourself. The signature expires in about 15 minutes.

Picker (`"type": "picker"`): more than one file. Ask which items to save, or save the videos. Use each item's `url` or signed `proxyUrl`.

Error (`"success": false`): show `error`.

- `youtube_not_supported` or `unsupported_platform`: stop. Do not retry.
- `rate_limit` (HTTP 429): wait a few minutes, then retry once.
- Anything else: show the message. One retry is enough for a temporary failure.

### 3. Tell the user

Report the filename, size, and folder. Mention that private or deleted posts cannot be downloaded.

## MCP

Stateless streamable HTTP at `https://www.grabgrab.fun/api/mcp`. Tool: `download_video` with `url` (required) and `quality` (optional). Same allowlist, same rate limit, and the same refusal for YouTube. No API key.

```json
{
  "mcpServers": {
    "grabgrab": {
      "url": "https://www.grabgrab.fun/api/mcp"
    }
  }
}
```

## CLI

From a checkout of this repo, without publishing anything:

```bash
node packages/cli/bin/grabgrab.mjs "<VIDEO_URL>" 1080
```

The npm package is prepared and not published. Do not tell the user to run `npx` until the owner publishes it.

## Limits

About 6 requests per 10 minutes per IP once the human check is enabled on the website, and about 10 when it is not. The counter is per server instance. Do not loop.

## Example

User: "Save this post: https://x.com/X/status/1697304622749086011"

1. POST that URL with `videoQuality` 1080, or call `download_video`.
2. Download the direct `url` (or the signed `proxyUrl` if needed).
3. Report the filename.

