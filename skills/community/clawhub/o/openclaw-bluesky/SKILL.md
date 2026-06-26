---
name: bluesky
description: "Bluesky/AT Protocol orchestration skill for authenticated interaction with the Bluesky Social network: post, reply, like, repost, quote, bookmark, and upload media."
metadata:
  {
    "openclaw": {
      "emoji": "🦋",
      "env": {
        "BSKY_PDS": "https://bsky.social",
        "BSKY_HANDLE": "<required>",
        "BSKY_APP_PASSWORD": "<required>"
      },
      "secrets": ["BSKY_APP_PASSWORD"],
      "install": [
        {
          "id": "python-atproto",
          "kind": "pip",
          "package": "atproto",
          "label": "Install AT Protocol Python SDK"
        }
      ]
    }
  }
---

# Bluesky Skill

Advanced Bluesky/AT Protocol orchestration skill. This skill allows for authenticated interaction with the Bluesky Social network, including robust handling of rich text, media uploads, and thread management.

## Provenance & Source
- **GitHub Repository**: [https://github.com/Heather-Herbert/openclaw-bluesky](https://github.com/Heather-Herbert/openclaw-bluesky)
- **Standard**: Follows OpenClaw AT Protocol implementation patterns.

## Configuration & Authentication
This skill expects the following environment variables to be set for secure operation:

- `BSKY_PDS`: The PDS URL (default: `https://bsky.social`).
- `BSKY_HANDLE`: Your full Bluesky handle (e.g., `user.bsky.social`).
- `BSKY_APP_PASSWORD`: A unique **App Password** generated via Bluesky Settings.

### Setup
1. **Dependency**: Ensure the `atproto` Python library is installed: `pip install atproto`.
2. **Generate App Password**: Go to `Settings` > `Advanced` > `App Passwords` in your Bluesky client.
3. **Environment Variables**: Configure your shell or `OPENCLAW_ENV` to include the variables listed above. Do not store your primary account password here.

## Capabilities
- `post(text, { reply_to, embed, facets })`: Create new posts. Threading requires `root` and `parent` references (`uri`+`cid`).
- `like(uri, cid)`: Like content.
- `repost(uri, cid)`: Repost content.
- `quote(text, uri, cid)`: Quote a post by embedding its Strong Reference.
- `bookmark(uri, cid)`: Private bookmarking (App View specific storage).
- `upload_blob(bytes, mimetype)`: Upload media (limit 1MB for images) before embedding.

## Implementation Details
- **Handles vs DIDs**: Always resolve handles to DIDs using the `resolveHandle` API before performing write operations.
- **Rich Text**: Use `TextEncoder` to ensure byte-accurate `byteStart` and `byteEnd` for facets. Never rely on UTF-16 character indices.
- **Indexing**: Always fetch the latest post `cid` before interacting (liking/reposting/quoting) to ensure valid Strong Reference anchors.

## Official Documentation
- [AT Protocol Docs](https://atproto.com/)
- [Bluesky Developer Docs](https://docs.bsky.app/)

## Author
- [Jennifer Strategist](https://bsky.app/profile/jenniferstrategist.bsky.social)
