# Music Discovery Guide — OpenClaw Skill

**Personalised music recommendations with real context — not just a list of names.**

Tell it your mood, a favourite artist, a genre, or an era. Get back a curated guide with entry points, listening pathways, and genuine reasons why each pick fits.

---

## What it does

Give it something to work with. Get back:

- **5 recommendations** per session with context for each
- **Why you'll like it** — connected to your specific taste, not generic
- **Start with this** — one specific album or track as your entry point
- **The mood** — when and where to listen
- **Where to find it** — streaming availability notes
- **Listening pathway** — suggested order to work through the picks

Two modes, or mix both:

| Mode | Best for |
|---|---|
| Mainstream discovery | Artists you've missed, adjacents to what you know |
| Underground/niche | Obscure gems, scene-specific deep cuts, overlooked artists |

---

## Who it's for

- Music fans who've exhausted their usual algorithms
- People who want to explore a new genre or era properly
- Underground music enthusiasts looking for genuine obscure recommendations
- Anyone who hates getting a list of names with no context

---

## Installation

```bash
npx clawhub@latest install tetsuakira-vk/music-discovery
```

---

## Usage

```
Use music-discovery for: [mood / artist / genre / activity]
```

Examples:
```
Use music-discovery for: something like Radiohead but more obscure
Use music-discovery for: late night driving, underground mode
Use music-discovery for: 90s Japanese city pop
Use music-discovery for: high focus study music, no lyrics
Use music-discovery for: underground Asian artists across any genre
```

---

## Features

- Three modes: mainstream, underground, or mixed
- Underground mode genuinely prioritises obscure artists — not just slightly less famous ones
- Honest availability notes — flags when something is hard to find on streaming
- Scene context for era and genre requests
- "More like X" mode identifies the specific qualities to follow, not just vibes
- Never fabricates artists or albums

---

## Requirements

- OpenClaw installed and running
- Any supported LLM
- No API keys or Spotify integration required — pure curation

---

## Tips

- Underground mode works especially well for regional scenes — try "underground UK garage", "Brazilian funk", "Japanese noise rock"
- Use the rabbit hole section at the end of underground sessions to keep going
- Ask for "all three modes" on a genre to get the full picture from mainstream to obscure
- Follow up with "more like [one of the recommendations]" to go deeper on anything that lands

---

## Licence

MIT — free to use, modify, and build on.

---

## Feedback & issues

Open an issue on GitHub. Actively maintained.
