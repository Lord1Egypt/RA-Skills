# Platform Strategy

Platform-specific best practices for the indie app marketing pipeline.

## TikTok

### Why TikTok First

TikTok's algorithm is the most discovery-friendly for new accounts. A well-executed
video can reach thousands of non-followers. It's the highest-leverage platform for
an indie dev starting from zero.

The pipeline posts 3 videos/day at 08:00, 13:00, 18:00. YouTube Shorts reuses the
same video 15 minutes later.

### What Works

- **Hook in the first 2 seconds** — TikTok measures "2-second view rate." Start with
  your hook as on-screen text before you say anything.
- **9:16 vertical, 1080×1920** — Full-screen. Any other ratio gets letterboxed.
- **15–45 seconds** — Shorter completion rates are better. 30s is the sweet spot.
- **Text overlays** — Many viewers watch without sound. Always caption key points.
- **Loop-friendly ending** — Ending that flows back into the beginning increases
  replay rate, which is a strong ranking signal.

### Hashtag Strategy

Use 3–5 hashtags. Mix:
- 1 branded tag (`#YourAppName`)
- 1–2 niche tags for your domain (`#ProductivityHack`, `#IndieApp`)
- 1 broad tag (`#AppDev`, `#TechTok`)

Avoid using only huge hashtags (millions of posts) — your video gets buried.
Avoid using only tiny hashtags — no audience to reach.

### Caption Format

The caption is secondary on TikTok — most viewers don't read it — but it helps
search and SEO. Keep it under 150 characters. Put hashtags at the end.

### Template Variables for TikTok

The pipeline uses the `tiktokStory.3-frame-reveal` template for structure:

- `{setupLine}` — The hook restated as an on-screen title
- `{twistLine}` — The insight or turn
- `{ctaLine}` — App name or soft CTA

---

## YouTube Shorts

### Reuse Strategy

The pipeline reuses the TikTok video for YouTube Shorts (same file, posted 15 minutes
after TikTok). This is intentional — both platforms prefer 9:16 video and the content
performs equivalently.

### What Differs

- **Title matters more** — YouTube uses the caption as the title in search. Write
  captions that read as search queries: "How I stopped losing ideas on my phone"
  not "this changed everything 😮"
- **Description field** — YouTube gives you more space. Add the App Store link here.
- **Community** — YouTube Shorts viewers are more likely to subscribe and watch
  longer content later. Good for building an audience if you plan regular videos.

### Template Variables

YouTube Shorts uses the `youtube` templates:
- `simple-question` — `{shortQuestion}` + "Be honest."
- `poll-prompt` — `{pollQuestion}`
- `challenge-prompt` — `{challengeDescription}` + "Try it and tell me how it went."

---

## X / Twitter

### Tone

X works best when it reads like a real person talking, not a brand posting.

The pipeline generates tweets using natural-voice patterns:
- **Observation** — stating something you noticed, then expanding on it
- **Dev perspective** — "Something I keep hearing from people: [hook]"
- **Quick thought** — "[Hook]. That's it. That's the tweet."
- **Engagement question** — "Be honest: [rephrased hook as question]?"
- **Story snippet** — two lines from the angle's texts joined together

### Link Placement

The pipeline alternates between two link types:
- Even tweets include the App Store link
- Odd tweets use the website URL (or no link, for purely engagement-focused tweets)

This avoids every tweet looking like an ad.

### Hashtag Strategy on X

Use 2–3 hashtags maximum. On X, more than 3 hashtags looks spammy and hurts
organic reach. The pipeline uses:
- 1–2 trending tags from `hashtag-bank.json` (if populated)
- 1–2 evergreen tags from the bank or config defaults

### Character Count

The pipeline trims tweets to 280 characters automatically while preserving the
last line (link or hashtags). Tweets that exceed 280 chars have their body truncated.

### Posting Schedule

- x-1: 10:30 — morning engagement window
- x-2: 16:00 — afternoon re-engagement

### Template Variables

```
{hook}        — the angle's hook sentence
{insight}     — 1-2 lines from texts[] expanded
{cta}         — config.app.defaultCta
{appHandle}   — config.app.handle
{hashtags}    — resolved from hashtag-bank.json or defaults
{topic}       — config.app.topicCategory
```

---

## Facebook

### Why Facebook

Facebook is different from the other platforms — it's not for discovery, it's for
community. Your Facebook posts go to people who already follow your page.

The pipeline posts on Mon/Wed/Fri at 12:00 (configurable). 3 posts/week is the
right cadence for a brand page without being annoying.

### Content Style

Facebook posts work best when they:
- Tell a short story or share a behind-the-scenes moment
- End with a genuine engagement question (not "like and share!")
- Are longer than a tweet but not essay-length (100–250 words)
- Feel personal and authentic, not corporate

Facebook audiences are more tolerant of imperfection and vulnerability than
TikTok or X audiences. Use that.

### Facebook Content Bank (`fb-brand-content-bank.json`)

Facebook posts come from a separate bank (not the same angles as TikTok/YouTube).
This is intentional — Facebook wants different content.

Good patterns for Facebook brand posts:

| Pattern | Description |
|---|---|
| `behind-the-scenes` | What happened this week building the app |
| `user-story` | Anonymous user feedback or outcome (with permission) |
| `tip` | One practical tip related to your app's domain |
| `myth-buster` | Counter-intuitive truth about your topic area |
| `challenge` | Invite followers to try something for a week |
| `personal-update` | Something you learned, struggled with, or fixed |

### Template Variables

```
{storyOpener}         — opening sentence that draws the reader in
{storyBody}           — the main content (2–3 paragraphs)
{engagementQuestion}  — the closing question for comments
{hashtags}            — 3–5 hashtags (less important on Facebook)
{challengeIntro}      — for challenge-post pattern
{challengeSteps}      — numbered steps
{challengeOutcome}    — what they'll get
{topic}               — your app's topic area
{mythBust}            — the myth being busted
{reframe}             — the better framing
```

---

## Cross-Platform Timing

Default schedule (all times configurable via `config.json`):

```
08:00  TikTok #1
08:15  YouTube Short #1  (same video)
10:30  X tweet #1
12:00  Facebook (Mon/Wed/Fri only)
13:00  TikTok #2
13:15  YouTube Short #2
16:00  X tweet #2
18:00  TikTok #3
18:15  YouTube Short #3
```

All times use the timezone offset in `config.json` (`schedule.timezoneOffset`).
Default is EST (`-05:00`). For PST use `-08:00`, for UTC use `+00:00`.

### Time Slot Rationale

- **8 AM, 1 PM, 6 PM** — standard TikTok high-engagement windows (commute, lunch, evening)
- **15 min after TikTok** — YouTube Shorts can use the same video file; slight delay
  avoids exact same-second posting which can look robotic
- **10:30 AM X** — morning engagement before lunch
- **4 PM X** — afternoon slump, people check their phones
- **12 PM Facebook** — peak Facebook engagement on weekdays

## Hashtag Bank (`hashtag-bank.json`)

Optional but recommended. Update weekly with trending tags in your niche.

Format:
```json
{
  "trending": [
    { "tag": "#TrendingTag", "addedAt": "2026-03-21" }
  ],
  "evergreen": [
    "#YourApp", "#IndieApp", "#AppStore", "#MobileApp"
  ]
}
```

The weekly planner pulls from this bank for X tweets. If the file doesn't exist,
it falls back to `config.app.defaultHashtags`.
