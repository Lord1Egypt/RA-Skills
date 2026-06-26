# How to Publish to ClawHub

## Before You Publish

1. Verify the API endpoints in SKILL.md match your actual production routes
2. Confirm the request/response schema is accurate
3. Make sure lovelybots.com/developer is live and self-serve
4. Test the skill locally with a real API key

## One-time Setup

```bash
# Install the ClawHub CLI
npm install -g clawhub

# Authenticate with GitHub
clawhub login
```

Your GitHub account must be at least 1 week old to publish.

## Publish

```bash
# From the parent directory of tiktok-video-maker/
clawhub publish ./tiktok-video-maker --slug tiktok-video-maker --name "TikTok Video Maker" --version 1.0.1 --changelog "Initial release — talking video generation for OpenClaw agents"
```

Your skill will be live at:
**https://clawhub.ai/[your-github-username]/tiktok-video-maker**

Users install it with:
```bash
openclaw skills install tiktok-video-maker
```

## After Publishing

Post in the OpenClaw GitHub Discussions or Discord:

> "Just published a video generation skill to ClawHub — lets your agent generate talking videos from a script and image. Built on LovelyBots API. Install with `npx clawhub add tiktok-video-maker`"

That's it. The community does the rest.

## Updating the Skill

```bash
clawhub publish . --slug tiktok-video-maker --version 1.0.3 --changelog "Updated API docs for unified image input and image quality guidance"
```

## Schema Check

Before publishing, verify these assumptions in SKILL.md are correct:

- [ ] POST /api/create takes `script`, unified `image` input (file/url/base64), plus optional `action_prompt` and `camera_prompt`
- [ ] URL-based image input is documented as public http/https only (`localhost`/private-network hosts blocked)
- [ ] Skill docs mention image best-practice guidance: front-facing portrait, `9:16` orientation
- [ ] Create response includes `id`, `status`, `credits_remaining`, and `share_url`
- [ ] Polling endpoint is GET /api/videos/:id
- [ ] Poll response includes `video_url` only once the job is completed
- [ ] Production base URL is https://api.lovelybots.com/api (not the ngrok URL)

If any fields differ, update SKILL.md before publishing.
