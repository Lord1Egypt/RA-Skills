# OpenClaw Twitter OAuth

OAuth-based X/Twitter posting for user-approved workflows through the AISA relay.

## When to use

- The user wants to publish, reply, or quote on X/Twitter.
- The user has approved OAuth or is ready to receive an authorization link.
- The user attached local image or video files that should be uploaded as part of the post.

## Quick Start

```bash
export AISA_API_KEY="your-key"
```

## Python Client

```bash
# Show current client configuration
python3 {baseDir}/scripts/twitter_oauth_client.py status

# Request an authorization link
python3 {baseDir}/scripts/twitter_oauth_client.py authorize

# Optional: open the authorization link in the default browser
python3 {baseDir}/scripts/twitter_oauth_client.py authorize --open-browser

# Publish a text post after the user confirms the final public content
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "Hello from Twitter OAuth" --confirm-public-write

# Publish an image-only post after confirmation
python3 {baseDir}/scripts/twitter_oauth_client.py post --media-file ./workspace/photo.png --confirm-public-write

# Publish a video-only post after confirmation
python3 {baseDir}/scripts/twitter_oauth_client.py post --media-file ./workspace/demo.mp4 --confirm-public-write

# Publish an image with text
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "Shipping day." --media-file ./workspace/photo.png --confirm-public-write

# Publish a video with text
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "Demo clip" --media-file ./workspace/demo.mp4 --confirm-public-write

# Publish long text as a reply thread when it exceeds one post
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "Hello from Twitter OAuth" --type reply --confirm-public-write

# Quote another tweet only when the quoted tweet URL is explicit
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "My take on this:" --type quote --quote-tweet-url "https://x.com/example/status/1888888888888888888" --confirm-public-write

# Start the thread from a specific external tweet
python3 {baseDir}/scripts/twitter_oauth_client.py post --text "Reply content" --type reply --in-reply-to-tweet-id "1888888888888888888" --confirm-public-write
```

## Core Behavior

Recommended flow:

1. Confirm the final text, media files, and reply or quote target before any public write.
2. Check authorization status or request an authorization link before publishing when authorization is missing.
3. Publish only after the user has approved OAuth, the final content is clear, and `--confirm-public-write` is present.
4. Use `--open-browser` only when the user explicitly wants local browser launch instead of receiving the URL.
5. Use plain post mode for standalone posts, `--type reply` for reply threads, and `--type quote --quote-tweet-url <url>` only for quote posts.

### OpenClaw Attachment Flow

When the user drops image or video files into OpenClaw:

1. OpenClaw stores the attachment in the local workspace and provides the workspace file path to the skill.
2. The skill passes that local path through `--media-file <workspace_path>`.
3. The Python client reads the local file and sends it to the relay backend as `multipart/form-data`.
4. The relay backend uploads the media to Twitter/X and then publishes the tweet.
5. The skill returns the final publish result, including the tweet link or tweet ID when available.

## Agent Instructions

When the user asks to publish content to X/Twitter:

1. Check whether `AISA_API_KEY` is configured.
2. Use `post --confirm-public-write` only after the user intent, final content, and authorization state are clear.
3. If the user attached workspace files, pass each image or video path with `--media-file`.
4. If the user explicitly wants to quote another tweet, require the tweet URL and pass it with `--quote-tweet-url`.
5. If the user wants to reply to a specific tweet, use `--type reply --in-reply-to-tweet-id <tweet_id>`.
6. If posting indicates that authorization is required, run `authorize` and return the approval link.
7. Do not claim the post succeeded until the publish step actually succeeds.

## Guardrails

- Do not ask the user for their Twitter password.
- Do not run the `post` command without `--confirm-public-write`.
- Do not use `--type quote` without `--quote-tweet-url`.
- Do not describe `--type reply` as quote posting; it creates reply relationships for a thread or a specific reply target.
- Do not use cookie-based login or proxy-based login unless the user explicitly asks for legacy behavior.
- Do not default to `--open-browser`; return the authorization link unless the user explicitly wants local browser launch.
- Do not invent remote URLs for attachments; always use the provided local workspace file path with `--media-file`.
- If the user provides a single image attachment, do not duplicate it or turn it into a multi-image post.
- If the user did not provide tweet text, do not generate or attach any caption text.

## Runtime Boundary

- Posting, OAuth, and approved media uploads are relay-based and go to `api.aisa.one`.
- Required secret: `AISA_API_KEY`.
- CLI output reports `aisa_api_key_present` instead of printing the key value.
- This workflow does not use passwords, browser cookies, cache sync, or home-directory persistence.
