# plan.json

Every script reads this one file. Paths are relative to it. A full example is in
`examples/moon-phases/plan.json`.

```json
{
  "timezone": "America/New_York",
  "rules": {"per_day": 1, "link_gap_days": 7, "max_per_day": 5},
  "manifests": ["pins/manifest.json"],
  "accounts": {
    "main": {
      "handle": "@yoursite",
      "socialAccountId": "<from social_accounts_list>",
      "timezone": "America/New_York",
      "times": ["20:30"],
      "boards": {"Moon and night sky": "<board id>", "Space science lessons": "<board id>"}
    }
  },
  "links": {
    "moon-phases": {
      "url": "https://example.com/moon-phases",
      "page": "page.json",
      "keywords": ["moon phases", "phases of the moon", "lunar cycle"],
      "moment": "2026-12-25",
      "lead_days": [120, 60]
    }
  },
  "pins": [
    {
      "id": "phases-grid",
      "account": "main",
      "link": "moon-phases",
      "board": "Moon and night sky",
      "file": "pins/phases-grid.jpg",
      "layout": "grid",
      "title": "Moon phases in order: all 8, from new Moon to waning crescent",
      "description": "The 8 Moon phases in order: ...",
      "alt": "Eight views of the Moon in a grid, ...",
      "ai": false,
      "at": "2026-11-16T20:30",
      "mediaIds": ["<from media_uploads_complete_session>"],
      "postId": "<from posts_create>"
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `rules.per_day` | pins per account per day when scheduling (default 1) |
| `rules.link_gap_days` | days between new pins for one link (default 7) |
| `rules.max_per_day` | `pin_check.py` stops above this many pins a day per account, posted ones included (default 5) |
| `manifests` | `render_pins.py` manifests, so the check knows each pin's source photos and headline size |
| `accounts.*.boards` | board name to board id, from `social_accounts_get_platform_inputs` |
| `accounts.*.times` | local posting times; Pinterest cares little about the hour |
| `links.*.page` | `page.py` output: final URL, title, headings (match and redirect checks) |
| `links.*.keywords` | the phrases the title and description should use |
| `links.*.moment` | a date the pins are for (a holiday, a season); they go out 90 to 45 days before |
| `links.*.lead_days` | `[most, fewest]` days ahead for this moment (default `[90, 45]`) |
| `pins[].link` | a key in `links`, or a full https:// address |
| `pins[].file` | a JPEG/PNG pin or an MP4/MOV/M4V video |
| `pins[].sources` | what a pin was made from when it isn't in a render manifest (a video's clip, a photo): paths or names; two pins for one page may not share one |
| `pins[].keywords` | phrases for this pin when they differ from its link's |
| `pins[].alt` | alt text; WoopSocial doesn't send it, so `schedule.md` lists it to paste in Pinterest |
| `pins[].ai` | true when the image is AI-made; use the generator's original file and say so |
| `pins[].at` | local time, set by `schedule.py`; `"now": true` publishes at once instead |
| `pins[].mediaIds` | one WoopSocial media ID (the image or the video) |
| `pins[].postId` | from `posts_create`; `log.py record` logs pins that have one |

`pins-log.jsonl` (next to the plan) is the history: every pin posted, with a fingerprint of its
picture, plus the numbers `log.py results` collected. `log.py record` skips placeholder ids and
pins whose `status` is `FAILED`. Keep it with the account's work; it is what
stops repeats.
