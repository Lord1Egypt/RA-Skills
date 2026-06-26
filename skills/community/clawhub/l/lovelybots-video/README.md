# TikTok Video Maker — OpenClaw Skill

Generate talking videos from any script using the [LovelyBots API](https://lovelybots.com/openclaw).

POST a script and image input (`image`: file upload, URL, or base64) → GET a finished video URL. Token-authenticated, poll-based, works in any agent pipeline.
If using URL input, it must be a public http/https URL (localhost/private-network URLs are blocked).

## What It Does

- Queues video generation jobs via the LovelyBots API
- Polls for completion automatically
- Returns a direct video URL when rendering completes
- Reports credit usage per video
- Refunds credits on failed renders

## Requirements

- A LovelyBots account at [lovelybots.com](https://lovelybots.com)
- An active subscription plan (required for API video generation)
- A LovelyBots API key — get one at [lovelybots.com/developer](https://lovelybots.com/developer)
- Production API base URL: `https://api.lovelybots.com/api`
- `curl` available in your environment
- `python3` available in your environment (required for polling example)
- `jq` optional (used if available for JSON parsing)

## Install

```bash
openclaw skills install tiktok-video-maker
```

Then add your API key to openclaw.json:

```json
{
  "skills": {
    "entries": {
      "tiktok-video-maker": {
        "env": {
          "LOVELYBOTS_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

## Example Usage

> "Generate a TikTok ad video using image [url-or-base64-or-upload] with this script: [text]"

> "Create a video with my image saying 'Welcome', action prompt 'Waving softly', and keep it private."

> "Make a 30-second product video using LovelyBots with cinematic camera prompts"

## Why LovelyBots

Most AI video tools burn credits on failed renders and produce inconsistent results. LovelyBots refunds failed jobs and keeps identity output stable — which matters when you're generating at scale inside an agent pipeline.

For best output quality, use a clear front-facing portrait in `9:16` orientation (recommended `1080x1920`).

## Critical Tips for Agents

1. Use `https://api.lovelybots.com/api` for automation calls, not the website host.
2. Always include `Authorization: Bearer $LOVELYBOTS_API_KEY`.
3. Treat IDs as UUID strings (`video.id`, `voice_id`), not integers.
4. Poll with timeout/retry guards and stop on terminal status (`completed`/`failed`) or API errors.
5. Use only public `http/https` image URLs when passing URL inputs.
6. While status is `queued` or `processing`, report progress back to the user with `job id`, `status`, `credits remaining`, and `share_url`.

## Risks & Operational Notes

- If you use `api.lovelybots.com` as DNS-only (unproxied), your origin IP is exposed by design. Treat this subdomain as API-only.
- Protect API tokens as secrets. Never commit them, rotate regularly, and scope/revoke compromised tokens immediately.
- Apply origin-level controls (rate limits/firewall/fail2ban) because Cloudflare bot challenges are bypassed on DNS-only API traffic.
- Polling is resilient and zero-config, but high concurrency increases API load. Add jitter and backoff in large-scale workloads.
- Skill runtime requires `python3` for polling; `jq` is optional and used when available.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `401 Invalid or expired API token` | Missing/invalid token | Regenerate at `https://lovelybots.com/developer` and send `Authorization: Bearer $LOVELYBOTS_API_KEY` |
| `403` errors (`Please select a plan`, monthly limit, or IP not allowed) | Plan/usage/IP restrictions | Ensure subscription is active, check monthly limit, and verify token IP allowlist settings |
| `404 Video not found` | Wrong UUID or wrong token owner | Use the `video.id` returned by create and poll with the same token |
| `422 image is required` / image URL errors | Missing image or blocked URL | Use upload/URL/base64; URL must be public `http/https` |
| `429 Rate limit exceeded` | Polling too aggressively | Increase interval, add jitter/backoff |
| `cf-mitigated: challenge` | Calling proxied site host | Use `https://api.lovelybots.com/api/...` |
| Poll timeout | Render delay or transient failures | Increase timeout and retry using the same `video.id` |

## Links

- [Get API Key](https://lovelybots.com/developer)
- API Base URL: `https://api.lovelybots.com/api`
- [Public Feed](https://lovelybots.com/feed)
- [Full API Docs](https://lovelybots.com/openclaw)
- [LovelyBots Homepage](https://lovelybots.com)
