---
name: imgur-cli
description: Imgur API CLI for agents. Upload images by file path or URL, fetch image metadata, delete uploads via delete-hash, create and manage albums. Anonymous uploads with IMGUR_CLIENT_ID, or authenticated uploads with IMGUR_ACCESS_TOKEN. Useful as a media-hosting primitive for agents that post to Instagram, Discord, Reddit, Telegram, etc. Outputs JSON. Use when a user needs to host an image publicly, turn a local file into a shareable URL, archive URLs into albums, or embed images in downstream pipelines.
license: MIT
---

# Imgur CLI

Wraps the official Imgur v3 API for AI agents. Upload images by file or URL, fetch metadata, delete by delete-hash, and manage albums — all as subcommands that print JSON.

## When to use

Trigger this skill when:

- An agent just produced an image (from `nano-banana-pro`, `generate-image`, ffmpeg, matplotlib, etc.) and another step needs a public URL.
- A user asks to "host this image", "get a shareable link for this file", or "upload to Imgur".
- You need to persist screenshots or render artifacts as shareable links.
- Archiving URLs into Imgur albums for later retrieval.

Pairs well with: `instagram-api` (needs hosted URLs), `nano-banana-pro`, `generate-image`, Discord/Telegram posting skills.

## Install

```bash
pip install -e .
```

Then set either:

- `IMGUR_CLIENT_ID` — anonymous uploads (get one at https://api.imgur.com/oauth2/addclient)
- `IMGUR_ACCESS_TOKEN` — OAuth2 bearer token (takes precedence if both are set)

## Commands

```bash
imgur-cli upload <file-or-url> [--title T] [--description D] [--album HASH]
imgur-cli get <image-hash>
imgur-cli delete <delete-hash-or-id>
imgur-cli album-create [--title T] [--description D] [--privacy public|hidden|secret] [--image ID ...]
imgur-cli album-add <album-hash> --image ID [--image ID ...]
```

All commands print the Imgur API `data` object as indented JSON. Errors exit non-zero with the Imgur error payload on stderr.

## Examples

```bash
# Anonymous upload, grab the shareable link
export IMGUR_CLIENT_ID="<client id>"
imgur-cli upload ./photo.jpg --title "cat pic" | jq -r '.link'

# Upload to user account
export IMGUR_ACCESS_TOKEN="<oauth token>"
imgur-cli upload https://example.com/pic.png --description "from pipeline"

# Save the delete-hash for later cleanup
imgur-cli upload ./tmp.png | jq -r '.deletehash' > .imgur-delete

# Create a private album of existing images
imgur-cli album-create --title "run-042" --privacy hidden --image aBc12 --image xYz34
```

## Notes

- Max image size: 10MB; videos are not supported by this skill (images only).
- Anonymous `deletehash` is the **only** way to remove anonymous uploads — store it.
- Respect Imgur rate limits (see your developer dashboard).
