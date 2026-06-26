# Local Configuration

Keep user-specific configuration outside the public skill directory, for example in a local project workspace. Never store tokens, cookies, private handles, channel IDs, or personal preferences inside the reusable public skill.

`assets/config.example.json` is intentionally a starter config with `onboarding.complete=false`. It should be copied and completed with the user during onboarding before any personalized issue or recurring job is created.

## Starter config shape

```json
{
  "version": "0.2.1",
  "onboarding": {
    "complete": false,
    "note": "Starter config only. Complete the Personalization Gate before generating a personal issue or scheduling a recurring job.",
    "requiredBeforePersonalIssue": [
      "newspaper.title",
      "newspaper.language",
      "editorial.readerPromise",
      "editorial.topics",
      "editorial.exclusions",
      "signals",
      "cadence",
      "delivery",
      "design"
    ]
  },
  "newspaper": {
    "title": null,
    "subtitle": null,
    "language": null,
    "timezone": "local"
  },
  "cadence": {
    "mode": null,
    "day": null,
    "time": null,
    "createCron": false
  },
  "editorial": {
    "readerPromise": null,
    "topics": [],
    "exclusions": [],
    "sections": [],
    "tone": null,
    "selectionBias": "user-saved signals first, general discovery second"
  },
  "signals": [
    { "id": "manual_urls", "type": "manual_urls", "enabled": true, "priority": 100 },
    { "id": "x_bookmarks", "type": "x_bookmarks", "enabled": false, "priority": 90, "limit": 30 },
    { "id": "browser_reading_list", "type": "browser_reading_list", "enabled": false, "priority": 80 },
    { "id": "read_later", "type": "read_later", "enabled": false, "priority": 75 },
    { "id": "rss", "type": "rss", "enabled": false, "priority": 60, "feeds": [] },
    { "id": "newsletter", "type": "newsletter", "enabled": false, "priority": 55 },
    { "id": "web_search", "type": "web_search", "enabled": false, "priority": 40, "queries": [] }
  ],
  "issue": {
    "maxPages": 3,
    "targetStories": { "lead": 1, "features": 4, "briefs": 10 },
    "sourceWindowDays": 7,
    "dedupe": true
  },
  "design": {
    "preset": "classic-newspaper",
    "density": "compact",
    "accentColor": "#6f3b1b",
    "pageSize": "A4",
    "imagePolicy": "source-only"
  },
  "delivery": {
    "mode": null,
    "format": ["html", "pdf"],
    "requireApprovalBeforeExternalSend": true
  },
  "reasoning": {
    "recommendedThinking": "xhigh",
    "proofreadingRequired": true
  }
}
```

## Completion rule

A config is production-ready only when:

- `onboarding.complete` is `true`;
- newspaper title, language, and reader promise are filled;
- topics and exclusions have been discussed with the user;
- at least one signal/source path is enabled and understood;
- cadence is set, including whether a cron/scheduled job should be created;
- delivery mode and output formats are set;
- design preset/density/page count are confirmed.

If `onboarding.complete=false`, agents may validate the starter config and use it to guide questions, but must not generate a personalized issue, create cron, or set up external delivery.

## Field notes

### `newspaper`

- `title`: display masthead. Ask the user; do not silently default.
- `subtitle`: reader promise or issue tagline.
- `language`: output language.
- `timezone`: needed for scheduled issues and source windows. Use `local`, `UTC`, or a specific IANA timezone such as `America/New_York`.

### `cadence`

- `mode`: issue frequency / Turnus: `on-demand`, `daily`, `weekly`, `monthly`, or custom scheduler label.
- `day` and `time`: optional for on-demand, required before scheduling.
- `createCron`: must be explicitly approved by the user. Never create cron silently.
- If scheduling through a platform cron, the cron should start an agent run with this skill and enough time for research/rendering.

### `editorial`

- `readerPromise`: the north star for selection and writing.
- `topics`: preferred recurring areas, chosen by the user.
- `exclusions`: recurring noise to suppress, chosen by the user.
- `sections`: default newspaper sections; the agent may adapt section names per issue.
- `selectionBias`: how to rank saved signals against general discovery.

### `signals`

Signal entries describe what to collect. A signal is not a verified source until fetched/read.

Common `type` values:

- `manual_urls` — pasted URLs/notes/files.
- `x_bookmarks` — X/Twitter bookmarks or saved posts via configured CLI/API/export.
- `browser_reading_list` — Safari Reading List, Chrome/Arc/Firefox bookmarks, or exported browser bookmark HTML/JSON.
- `read_later` — Pocket, Instapaper, Wallabag, Raindrop, Readwise Reader, Omnivore-style exports.
- `rss` — feed URLs or OPML import.
- `newsletter` — mailbox searches or forwarded newsletter files when configured.
- `web_search` — recurring topic searches.
- `local_manifest` — JSON/CSV/Markdown source manifest.

Use `priority` to bias ranking; use `limit` and `sourceWindowDays` to keep issues manageable.

### `design`

See `references/design-presets.md`. Keep customization simple: preset, density, accent color, page size, image policy.

### `delivery`

External sending/publishing should require explicit approval unless the user has clearly automated it. Local file generation does not need external approval.

## Validation

Run:

```bash
python scripts/check_config.py path/to/non-annoying-news.config.json
```

The validator accepts incomplete starter configs, but it prints the missing onboarding fields and warns that no personalized issue or cron should be produced yet. It fails production configs (`onboarding.complete=true`) when required fields are missing.
