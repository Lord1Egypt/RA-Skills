---
name: music-intel
description: Music data across Spotify, Apple Music, SoundCloud and TikTok without accounts or API keys. Artist monthly listeners, followers and top tracks with play counts, albums, tracks and playlists, Apple Music artists and songs, SoundCloud artists and tracks, and TikTok's Top 50 and Viral 50 sound charts. Use this skill for artist research, A&R scouting, playlist pitching, or music trend tracking.
---

# Music Intel: Spotify, Apple Music, SoundCloud & TikTok Sounds

![Music Intel: Spotify, Apple Music, SoundCloud & TikTok Sounds](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/music-intel.gif)

Measure any artist or song across platforms: Spotify listeners and play counts, Apple Music catalogue, SoundCloud tracks, and how a sound is doing on TikTok.

No Spotify, Apple or SoundCloud account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=music-intel).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/music-intel.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “How big is Sabrina Carpenter on Spotify right now?”
- “What's on TikTok's Viral 50?”
- “Compare this track on Spotify and Apple Music”
- “Show this SoundCloud artist's latest tracks”

## When to Use This Skill

Use it when the user wants artist, song, album or chart data from Spotify, Apple Music, SoundCloud or TikTok.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Music platforms  │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Spotify

| Tool | What it returns | Price |
|------|-----------------|-------|
| `spotifydata_search` | Search Spotify for tracks, artists, albums, playlists and podcasts | $0.00282 |
| `spotifydata_artist` | A Spotify artist by id or URL: monthly listeners, followers, top tracks, discography | $0.00282 |
| `spotifydata_track` | A Spotify track by URL: play count, popularity, album and artists | $0.00282 |
| `spotifydata_album` | A Spotify album by URL with its track list | $0.00282 |
| `spotifydata_playlist` | A Spotify playlist by URL: follower count and tracks | $0.00282 |

### Apple Music

| Tool | What it returns | Price |
|------|-----------------|-------|
| `applemusicdata_search` | Search Apple Music by keyword: songs, artists, albums, playlists, stations and music videos | $0.00282 |
| `applemusicdata_artist` | An Apple Music artist: top songs, albums, music videos, playlists and editorial notes | $0.00282 |
| `applemusicdata_album` | An Apple Music album: tracks, release info, artist and more by the artist | $0.00282 |
| `applemusicdata_track` | An Apple Music song: title, artist, album, duration, release date | $0.00282 |

### SoundCloud & TikTok

| Tool | What it returns | Price |
|------|-----------------|-------|
| `soundclouddata_artist` | Public SoundCloud artist by handle: followers, track count, playlists, city, country, bio, verified flag | $0.00282 |
| `soundclouddata_artist_tracks` | Tracks of a SoundCloud artist, newest first: plays, likes, reposts, comments, genre, duration, release date | $0.00282 |
| `soundclouddata_track` | One SoundCloud track by URL: plays, likes, reposts, comments, genre, tags, label, duration, release date | $0.00282 |
| `tiktokdata_music_charts` | TikTok's music charts: Top 50 (scene 0) or Viral 50 (scene 1) | $0.0015 |
| `tiktokdata_song` | A TikTok sound or song: title, artist, duration and how many videos use it | $0.00282 |

## Recipes

### Is this song breaking out?

1. `spotifydata_track` for play count.
2. `tiktokdata_song` for how many TikTok videos use it.
3. `tiktokdata_music_charts` (`scene: 1`) to see if it is on the Viral 50.

## Code Examples

### A Spotify artist

```bash
clawlink_call_tool --tool "spotifydata_artist" \
  --params '{"url": "https://open.spotify.com/artist/74KM79TiuVKeVCqs8QtB0B"}'
```

### TikTok Viral 50

```bash
clawlink_call_tool --tool "tiktokdata_music_charts" \
  --params '{"scene": 1}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `spotify artist`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Spotify tools take the open.spotify.com URL.
- Play counts are lifetime; monthly listeners is a rolling 28 days.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Artist not found | Search first and use the URL from the result. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=music-intel; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=music-intel)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=music-intel)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [TikTok Trend Radar](https://clawhub.ai/hith3sh/skills/tiktok-trend-radar)
- [Podcast Scout](https://clawhub.ai/hith3sh/skills/podcast-scout)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=music-intel)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
