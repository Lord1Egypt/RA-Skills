# plan.json

One file holds a batch: one post or a week of them. Every script reads it; `ig_check.py --fix`,
`schedule.py` and the agent write to it. Paths are relative to the plan's folder.

```json
{
  "brand": {"name": "Plodd", "handle": "@plodd.app"},
  "timezone": "Europe/Amsterdam",
  "accounts": {
    "main": {"handle": "@plodd.app", "socialAccountId": "<from social_accounts_list>",
             "timezone": "America/New_York", "times": ["12:30"]},
    "es":   {"handle": "@plodd.es",  "socialAccountId": "<id>",
             "timezone": "Europe/Madrid", "times": ["13:30"]}
  },
  "posts": [
    {
      "id": "habits",
      "format": "carousel",
      "media": ["slides/slide-01.jpg", "slides/slide-02.jpg", "photos/desk.jpg"],
      "caption": "Missed a day? Your habit is fine. ...",
      "alt": ["Cover: ...", "Rule 1: ...", "A desk with ..."],
      "targets": [
        {"account": "main"},
        {"account": "es", "media": ["slides-es/slide-01.jpg", "slides-es/slide-02.jpg", "photos/desk.jpg"],
         "caption": "¿Te saltaste un día? ..."}
      ],
      "checklist": ["Paste the alt text per slide", "Tag @coffeebrand as collaborator"]
    },
    {
      "id": "habits-teaser",
      "format": "story",
      "media": ["story/slide-01.jpg"],
      "with": {"post": "habits", "minutes": -60},
      "targets": [{"account": "main"}, {"account": "es", "media": ["story-es/slide-01.jpg"]}]
    },
    {
      "id": "demo",
      "format": "reel",
      "media": ["video/demo.mov"],
      "frame": {"title": "How Plodd counts weeks, not days"},
      "cover": "reel-demo/cover.jpg",
      "caption": "...",
      "trial": "MANUAL",
      "targets": [{"account": "main", "at": "2026-11-11T19:00"}]
    }
  ]
}
```

## Fields

| Field | Meaning |
|---|---|
| `format` | `image` (one picture), `carousel` (2 to 20 pictures and/or videos), `reel` (one video), `story` (one picture or video; no caption) |
| `media` | files in order. `ig_check.py --fix` replaces entries with fixed copies in `fixed/` and keeps a `plan.json.bak` |
| `caption` | the default caption. A target's own `caption` replaces it for that account |
| `accounts.<key>.timezone`, `.times` | each account's time zone and posting times (from its Insights); `schedule.py` uses them |
| `targets[].media`, `.cover`, `.mediaIds`, `.coverId` | the account's own version of the post (another language, cover or order). Needed for a second account: under Instagram's 2026 originality rules the same media there is likely seen as a repost |
| `with` | Stories only: `{"post": "<feed post id>", "minutes": -60}` places the Story that many minutes before (or after) that post on each account |
| `frame` | Reels from landscape video: `{"title": "..."}` makes a framed Reel (video full width on a plain background, headline above); `bg` sets the colour. Only for the user's own footage: set `"own_footage": true` |
| `alt` | alt text per image, pasted in the app after posting (WoopSocial doesn't set it) |
| `cover` | Reels only: a 1080x1920 JPEG, made with `reel.py cover` |
| `trial` | Reels only: `MANUAL` or `SS_PERFORMANCE` to post as a Trial Reel; leave out otherwise |
| `targets[].at` | local time `YYYY-MM-DDTHH:MM` in `timezone`. `schedule.py` fills it when missing. `"now": true` posts right away |
| `checklist` | what the user adds in the Instagram app afterwards (collaborators, location, music, alt text, tags) |
| `mediaIds`, `coverId` | set after uploading; `schedule.py --bodies-only` puts them in the requests |
| `targets[].postId`, `targets[].url` | set after `posts_create` / `posts_get`; `log.py record` logs them |

## Files the scripts write next to it

`fixed/` (fixed media), `check.json`, `requests/<post>-<account>.json`, `schedule.md`,
`preview/index.html` and `preview/preview.png`, `posts.jsonl` (the log), `results.md`.
