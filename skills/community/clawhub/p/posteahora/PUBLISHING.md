# Publishing & Scheduling

How posts move from a command to live content across your social networks.

## The three states

A post is created in one of three states, controlled by how you run
`posteahora post`:

| State | How | What happens |
|-------|-----|--------------|
| **Draft** | `--draft` | Saved, not queued. Nothing goes live. |
| **Scheduled** | `--at <ISO 8601>` | Queued to publish at the given future time. |
| **Publish now** | neither flag | Enters the publishing pipeline immediately. |

```bash
# Draft
posteahora post "Idea" --to twitter:a1b2 --draft

# Schedule
posteahora post "Tuesday tip" --to twitter:a1b2 --at 2026-07-20T09:00:00Z

# Publish now
posteahora post "Live now 🚀" --to twitter:a1b2
```

## Multi-platform fan-out

A single command can target many channels. Each channel is published
independently with its own connected account, so one failing platform never
blocks the others:

```bash
posteahora post "Big announcement" \
  --to instagram:a1b2 --to twitter:c3d4 --to linkedin:e5f6
```

## Caption formatting

A caption is published **byte for byte** — nothing re-wraps, trims or normalizes
it. Every empty line you send is an empty line your audience sees, and every one
you forget is a wall of text.

### Multi-line captions

The caption is a raw positional argument. Inside double quotes the shell does
**not** turn a backslash-n into a line break, so this publishes the two
characters `\n` in the middle of the post:

```bash
posteahora post "line one\nline two" --to twitter:a1b2   # ✗ literal \n
```

Use a heredoc instead:

```bash
CAPTION=$(cat <<'EOF'
Hook line

🍷 Feature one
🥂 Feature two

Which one would you pick?

#tag #tag
EOF
)

posteahora post "$CAPTION" --to instagram:a1b2           # ✓ real line breaks
```

A real multi-line double-quoted string works too, as does ANSI-C quoting
(`$'line one\nline two'`) in bash and zsh — but the heredoc stays readable as the
caption grows.

### Structure

Separate blocks with exactly one empty line; use a single line break inside a
list. Never three or more breaks in a row.

```
Hook line

Short CTA or question

🍷 Feature one
🏞 Feature two

Closing CTA

Link line

#hashtag #hashtag
```

Put a short CTA near the top as well as at the end — Instagram and TikTok
truncate the caption in-feed, so anything below the bullets is unseen by most
viewers.

### Rules

- **No Markdown.** `**bold**`, `- bullets`, `#headings` and `[text](url)` render
  literally on every platform except Discord. Use emoji or numbers for bullets.
- **Hashtags go inside the caption**, as the last block. The `--hashtags` flag
  stores them on the post but they never reach the platform.
- **No URL in Instagram or TikTok captions** — Instagram won't linkify it and
  TikTok penalizes links in captions. Use "link in bio". URLs are fine on every
  other network.
- No leading or trailing whitespace on a line — indentation ships.

### Limits

| Platform | Limit | |
|---|---:|---|
| X (Twitter) | 280 | 25000 with premium; line breaks cost characters |
| Bluesky | 300 | counted in **graphemes**, not UTF-16 units |
| Threads | 500 | the tightest real-world limit |
| Mastodon | 500 | default; your connected instance's own limit wins |
| Pinterest | 800 | the Pin description; the title is separate (≤100) |
| Google Business | 1500 | the Local Post summary |
| Discord | 2000 | Markdown supported here |
| Instagram | 2200 | |
| TikTok (video) | 2200 | |
| LinkedIn | 3000 | "see more" collapses after ~3 lines |
| Telegram | 4096 | 1024 when the post has media (it becomes a caption) |
| TikTok (photos) | 4000 | also needs `photoTitle` ≤90 in `platformOptions` |
| YouTube | 5000 | only ~2 lines show under the video |
| Facebook | 63206 | |
| WordPress / Dev.to / Tumblr | — | the caption is the article body; title is a separate field |

Per-platform caption overrides (`platformCaptions`) exist in the REST API and the
MCP server, but the CLI has no flag for them — when the text must differ per
channel, run a separate `posteahora post` per channel.

## Media

Attach media with `--media`, using public URLs from `posteahora upload`:

```bash
posteahora upload ./cover.jpg          # → https://cdn.posteahora.com/…
posteahora post "With a cover image" --to instagram:a1b2 --media https://cdn.posteahora.com/…
```

Pass `--media` multiple times for carousels. See
[SUPPORTED_FILE_TYPES.md](SUPPORTED_FILE_TYPES.md).

## Scheduling rules

- `--at` must be a **future** ISO 8601 timestamp (e.g. `2026-07-20T09:00:00Z`).
- Times are interpreted in the timezone you provide in the timestamp; use `Z`
  for UTC.
- The CLI validates the time locally before calling the API, so a past time fails
  fast.

## Checking status

After publishing, confirm what happened:

```bash
posteahora posts --status scheduled
posteahora posts --status published
posteahora posts --json
```

Post statuses: `draft`, `scheduled`, `queued`, `published`, `failed`.

## Quotas & limits

Publishing counts against your PosteAhora plan's monthly post quota. The API is
also rate-limited per key (HTTP `429` when exceeded) — space out large batches.
