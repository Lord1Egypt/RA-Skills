---
name: haven-media-x402
description: Generate music, images, and video (silent or with a synchronized soundtrack) by paying per call in USDC via x402 — no account or API key. Use when the agent needs to create media it cannot produce natively.
compatibility: Needs network access to api.havenagent.ai and a USDC wallet on Base — either the @havenagent/mcp server (Node.js 20+), which holds one locally, or your own x402 v2 client.
metadata:
  homepage: https://api.havenagent.ai/x402/api/v1/catalog
  payment: x402
  network: base
  asset: USDC
---

# Haven Media (x402)

Pay-per-call media generation for AI agents. Every endpoint is priced in
USDC and settled over the [x402 protocol](https://x402.org) — the agent's
wallet pays at request time, so there is no signup, no API key, and no
human in the loop.

## When to use

Reach for this whenever a task needs generated media the agent can't make
itself:

Each row is the kind id the catalog and job responses use, then the path to
POST, then the default price.

- **Music** — a jingle, background track, or theme.
  `music` · `/music` · $0.10
- **Text-to-image** — illustrations, concept art, thumbnails.
  `image_generate` · `/image/generate` · $0.05
- **Image edit** — instruction-based edits of a supplied image.
  `image_edit` · `/image/edit` · $0.10
- **Upscale** — 2×/4× super-resolution.
  `image_upscale` · `/image/upscale` · $0.06
- **Photo restore** — denoise / deblur / dehaze old photos.
  `image_restore` · `/image/restore` · $0.10
- **Video** — short clips, text- or image-to-video.
  `video` · `/video` · $0.80
- **Video with sound** — a short 2K clip with a synchronized soundtrack:
  dialogue, effects, ambience.
  `video_sound` · `/video-sound` · $1.50

Prices are the defaults, **not** a promise that every endpoint is on sale.
Not every kind is mounted on every deployment, so always read the live catalog for what is actually being sold,
the current price, and the exact request schema before paying.

## Option A: the Haven MCP server (recommended)

`@havenagent/mcp` does the whole payment flow for you: it holds a local
wallet, checks every quote against the live catalog, enforces spend caps,
and tracks jobs across restarts. Use it if your agent supports MCP
(Claude Code, Cursor, Hermes, and most others).

**In Claude Code**, install the Haven plugin. It bundles this server and
this skill:

```bash
claude plugin marketplace add havenagent/skills
claude plugin install haven@havenagent
```

**In any other MCP client**, register a stdio server: command `npx`, args
`-y @havenagent/mcp@latest`. For example, this install can read the
catalog but **cannot spend**:

```bash
claude mcp add haven -s user \
  -e HAVEN_MCP_NETWORK=base \
  -e HAVEN_MCP_ALLOW_MAINNET=0 \
  -- npx -y @havenagent/mcp@latest
```

For Hermes, add the same command and `env` values under
`mcp_servers.haven` in `~/.hermes/config.yaml`.

Paying needs two steps, and only your **operator** can do them — do not
do them yourself:

- Turn spending on: `HAVEN_MCP_ALLOW_MAINNET=1` in the MCP registration,
  or **Allow spending real USDC** in the plugin's settings.
- Fund the wallet that `haven_wallet` shows with USDC on Base. No ETH is
  needed.

The server already knows Haven's receiving wallet and refuses any quote
that pays a different address.

**Use** these tools, in order:

1. `haven_catalog` (free) — what is on sale, the live prices, and ETAs.
2. `haven_wallet` (free) — the wallet address and USDC balance.
3. `haven_generate` with a `kind` from the list above and its fields —
   verifies payment and returns a `jobId`. Nothing is charged yet.
4. `haven_job_status` with the `jobId` (free) — poll until `status` is
   `completed` or `ready_unpaid`. Jobs take 60–600 seconds, so keep the
   `jobId` and resume in a later turn.
5. `haven_job_result` with the `jobId` — **the paid step**. It pays,
   downloads, checks the file, and returns a local `path`.

`haven_jobs` (free) lists every open job if you lose track of a `jobId`.
Default caps are $2 per call and $2 per rolling 24 hours. The operator can
raise both.

Full reference: https://www.npmjs.com/package/@havenagent/mcp

## Option B: your own x402 client

If your agent already has a funded x402 **v2** client (it sends
`Payment-Signature`, not the v1 `X-PAYMENT` header), read
[references/x402-http.md](references/x402-http.md) for the raw HTTP flow:
quote, pay, poll, pay on delivery, and download.

## Rules & limits

- **SFW only.** Prompts and input images are moderated before the job is
  even enqueued, so a rejection happens before any charge. Every output is
  screened again before payment is requested: images and video frames by an
  image classifier, generated audio by transcription plus a text classifier,
  and `video_sound` by both. If screening can't run we withhold the artifact
  rather than serve it, and you aren't charged.
- **You are only charged on delivery, and there are no automatic refunds.**
  Submitting a job only verifies your payment authorization. The charge
  happens once the finished, screened artifact is ready: at `haven_job_result`
  with the MCP server, or at the completing status poll over raw HTTP.
  Abandon a job before that point and you are never charged; once paid, the
  charge stands whether or not you download the file. x402 payments are
  final. In the rare case a charge lands before the artifact reaches you,
  keep polling the job rather than paying again — reconciliation completes
  almost all of these on its own. A job it cannot resolve is worked by a
  human: report the jobId to `support@havenagent.ai`.
- **Long jobs:** GPU workers scale to zero, so a job can take several minutes
  to start. Keep the `jobId` and check back in a later turn rather than
  submitting again.
- **7-day retention** — download results promptly; artifacts are deleted
  after a week.

## Video: use terms

`video` and `video_sound` are served under upstream model licences whose use
restrictions pass through to you, and **paying for one of those requests
accepts them**. In short: disclose that the output is machine-generated
wherever you publish it, keep the AI-generated disclosure embedded in the
file, do not use the output to train or fine-tune any model, and pass these
terms on to anyone you share the output with. Read
[references/use-terms.md](references/use-terms.md) before buying either
kind; the controlling text is at the catalog's `terms.url`.
