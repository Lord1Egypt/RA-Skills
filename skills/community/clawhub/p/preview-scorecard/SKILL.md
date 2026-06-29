---
name: preview-scorecard
description: Create a shareable RooQuiz preview scorecard — a scored questionnaire where each option adds points toward a total that buckets into levels — and get a link to open in the browser. No account, login, or API key required. Use this when someone wants to build, try out, or share a self-assessment, health/habit score, readiness or maturity check, satisfaction survey, or any rated questionnaire that turns answers into a total score and a level (no "correct" answer). For a right/wrong graded quiz, use the preview-quiz skill; for a personality/type test with no scores, use the preview-outcome skill.
---

# Create a RooQuiz Preview Scorecard

POST a scorecard as JSON to RooQuiz's open preview endpoint and instantly get a **short-lived (~1 hour)**, **browser-openable** preview link. The creation endpoint is public (`access.create => true`), so this needs **no account, login, API key, or credentials** — anything that can make an HTTP request can use it.

A **scorecard** (`scene: "scorecard"`) is a scored questionnaire: there's no "correct" answer — instead each option carries a point value, the `report.formula` totals them, and `report.levels` buckets the total into a result band (e.g. "Needs Work" → "Healthy"). It produces a **temporary preview**, not a permanently published form — the link expires automatically (recreate it in RooQuiz if you need to keep it).

Two sibling skills cover the other assessment types — pick the one that matches:
- **preview-quiz** — a right/wrong assessment where correct answers earn points and the taker gets a graded score.
- **preview-outcome** — a personality / type test where options vote for result types and the most-voted type wins (no scores).

## Three steps

1. **Build the scorecard JSON** (structure below).
2. **Create it:** `POST {PREVIEW_BASE}/api/preview-forms` with the JSON as the body and header `Content-Type: application/json`. Returns `{ doc: { publicToken, expiresAt }, message }`.
3. **Hand back the link:** `{QUIZ_BASE}/b/{publicToken}` (append `?secret={secret}` only if you set a `secret` when creating).

### Endpoints

| | Default (RooQuiz cloud) | Override env var |
| --- | --- | --- |
| `PREVIEW_BASE` (create) | `https://preview.rooquiz.com` | `ROOQUIZ_PREVIEW_BASE` |
| `QUIZ_BASE` (open preview) | `https://quizster.app` | `ROOQUIZ_QUIZ_BASE` |

Override the env vars only when targeting a self-hosted RooQuiz deployment; otherwise the defaults work as-is.

### Create it

Send one HTTP request. There is no auth — `Content-Type: application/json` is the only required header. Use whatever HTTP client your environment has (an agent's built-in fetch/HTTP tool, `curl`, `requests`, `fetch`, Postman, …):

```http
POST https://preview.rooquiz.com/api/preview-forms
Content-Type: application/json

<the scorecard JSON as the raw request body>
```

For example, with `curl` (write the JSON to a file first, or inline it with `--data`):

```bash
curl -sS -X POST https://preview.rooquiz.com/api/preview-forms \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/preview-form.json
```

The response is JSON shaped like:

```json
{ "doc": { "publicToken": "7k3m9q2p", "expiresAt": "2026-06-16T09:12:00.000Z" }, "message": "..." }
```

Read `doc.publicToken` and build the preview link to hand the user:

```
https://quizster.app/b/<publicToken>
```

If you set a `secret` in the JSON, append `?secret=<secret>` to that link. For a self-hosted RooQuiz, swap the two hosts for your deployment's preview-API and quiz hosts (see the endpoints table above).

## Scorecard JSON — top level

```jsonc
{
  "scene": "scorecard",            // required & fixed for this skill. Sets allowed question types and scoring. Cannot change after creation.
  "title": "My Scorecard",         // required
  "description": "Optional intro",
  "language": "en_US",             // form language; default zh_CN. See "language values" in Notes.
  "personalized": {                // appearance; omit to use defaults (list layout, light theme)
    "key": "default",
    "theme": { "name": "light" },
    "layout": "card"               // "list" | "card"
  },
  "indexDisplayMode": "number",    // question numbering: none (default) | number | uppercase | roman
  "fields": [ /* questions — see "Question types" and "Scoring" */ ],
  "report": { /* results page — see "Report configuration" */ },
  "rules": [],                     // conditional-display rules (scorecard-only feature); usually []
  "secret": "optional; if set, the preview link must include ?secret="
}
```

Key points:
- Every question needs a **unique `code`** (string); option `code`s must be unique within their question. A `code` must be a valid identifier — start with a letter or `_`, then only letters/digits/`_` (no `-`, spaces, or leading digit), max 64 chars, and not a reserved math word (`e`, `E`, `pi`, `PI`, `tau`, `phi`, `i`, `Infinity`, `NaN`, `true`, `false`, `null`, `undefined`). The server rejects violations with HTTP 400. Codes are also what the `formula` references.
- `name` is the question text; `description` is optional helper text.
- Unknown top-level fields are silently ignored by the server (no error).
- **`secret`**: omit it for a clean link that works with just the token (tokens are random 8-char and expire in ~1 hour — fine for previews). Set it to make the token unguessable, at the cost of requiring `?secret=` on the link. Default: omit.

## Themes

`personalized.theme.name` sets the visual theme. Omit `theme` to default to `light`. Set it as `"personalized": { "key": "default", "theme": { "name": "synthwave" }, "layout": "card" }` (`layout` is still only `list` or `card`).

Pick a theme that fits the questionnaire's topic/mood. **To use a random theme** — when the user asks for one, wants variety, or has no preference — just choose a random `name` from this list when building the JSON (there's no server-side "random" option). Recommended palette:

| name | vibe / good for |
| --- | --- |
| `light` | clean neutral bright; default, formal/general questionnaires |
| `corporate` | professional blue+gray; B2B, career, business, maturity checks |
| `dark` | modern sleek dark; tech, night, cool |
| `cupcake` | soft pink, cute, rounded; fun, food, kids, lighthearted |
| `pastel` | gentle pastel artsy; lifestyle, aesthetics, soft mood |
| `valentine` | pink romantic hearts; love, relationships, holidays |
| `synthwave` | neon purple/pink retro; gaming, trends, bold |
| `luxury` | dark + gold premium; finance, luxury, high-end |
| `forest` | deep green nature; environment, health, outdoors, wellness |
| `coffee` | warm brown cozy; food & drink, cafe, lifestyle |
| `autumn` | warm orange/brown seasonal; autumn, cozy, harvest |
| `halloween` | purple + orange spooky; Halloween, horror, festive |
| `night` | deep calm blue; astronomy, mindfulness, calm tech |
| `cyberpunk` | high-contrast neon yellow; tech, esports, gaming |

The full daisyUI theme set also renders (e.g. `emerald`, `dracula`, `retro`, `nord`, `sunset`, `winter`, `lofi`, `garden`, `aqua`, `business`, `lemonade`, `dim`, `bumblebee`, `acid`, `fantasy`, `wireframe`, `black`, `cmyk`) — the table above is just the recommended palette. The server doesn't validate the name, so a typo silently falls back to default styling rather than erroring.

## Question types

Each field is `{ type, code, name, ... }`. In a scorecard you can use:

- **Choice** (carry `choices: [{ code, value }]`, where `value` is the option label):
  `SingleCheck` (single), `MultiCheck` (multiple; optional `min`/`max`), `DropDown`, `Cascade`, `TrueFalse` (no choices)
- **Input**: `NumberField`, `DateField` (needs `precision`), `TimeField`, `Rate` (needs `steps`)
- **Display only** (never scored): `Statement` (`content`), `Breaker` (page break / divider), `Swiper` (image carousel, `items`)

`FillBlank` and `Ordering` are **not** allowed in a scorecard (they're quiz types). Optional shared props on any field: `required`, `description`, `explain`, `hidden`, `activeColor` (`primary`/`secondary`/`accent`/`neutral`), `layout` (`list`/`grid`).

## Scoring

Give each option a point value with **`partialScoring`** (a field-level array, sitting next to `choices`). Do **not** set `correctAnswer` or `exactScoring` — there are no "correct" answers in a scorecard.

```jsonc
"partialScoring": [
  { "value": "never", "score": 0 },
  { "value": "some",  "score": 5 },
  { "value": "daily", "score": 10 }
]
```

Each `value` must be one of that question's `choices[].code`s. A `Rate` question contributes its selected step value to the total. Display-only fields (`Statement`/`Breaker`/`Swiper`) are never scored. The per-question scores are combined by the `report.formula` (below).

## Report configuration

`report.overallAnalysis` is **required**. A scorecard needs a **`formula`** to total the questions, plus `levels` to bucket the total.

```jsonc
"report": {
  "overallAnalysis": {
    "title": "Your Score",
    "formula": "q1 + q2",          // total from question codes via + - * / ( )
    "summaryTemplate": "<p><art-field data-type=\"fieldVariable\" data-cid=\"score\"></art-field> pts · <art-field data-type=\"fieldVariable\" data-cid=\"level\"></art-field></p>",
    "levels": [                    // map total score → level (see strict rules below)
      { "minScore": null, "maxScore": 10, "label": "Needs Work" },
      { "minScore": 10, "maxScore": 20, "label": "On Track" },
      { "minScore": 20, "maxScore": null, "label": "Excellent", "description": "Top tier!" }
    ]
  }
}
```

**Strict `levels` rules** (violations return HTTP 400): the first level's `minScore` must be `null` (−∞); the last level's `maxScore` must be `null` (+∞); middle levels have finite numbers on both ends; for adjacent levels `current.minScore === previous.maxScore`; `maxScore` strictly increases down the array. A single level has `null` on both ends.

Levels may carry a `color` (hex) and a `cta` (results-page button): `{ enabled, type: "link", text, url, newWindow }`. When the cta is enabled, `text` and `url` are required, and `url` must be an `http`/`https` link. `summaryTemplate` defaults to a built-in template if omitted.

## Common mistakes

These wrong patterns get reached for out of habit; the server rejects them with HTTP 400. The formats above are correct — match them exactly.

- **Option lists are `choices`, never `options`.** Every choice question uses `"choices": [{ "code": "a", "value": "Label" }]`. There is no `options` key.
- **Codes must be valid identifiers, not arbitrary text** — no hyphens (`type-a`), spaces, or leading digits (`1q`), and not reserved math words. Watch out for **5+ options coded `a,b,c,d,e`**: `e` (Euler's number) is reserved and rejected — use `o1, o2, …` or another non-reserved identifier.
- **Scoring is a field-level `partialScoring` array, not a value nested inside each choice.** Correct: `"partialScoring": [{ "value": "a", "score": 5 }]` next to `choices`. Wrong: `{ "code": "a", "value": "…", "score": 5 }` on the option itself.
- **Don't set `correctAnswer`/`exactScoring`** — those are for the right/wrong quiz scene and are rejected here.
- **Provide a `formula`** that references your question codes — without it the total won't add up. And `report.overallAnalysis` is required.

## Complete example

The `personalized.theme.name` is matched to the topic (see **Themes** above) — swap in any other name, or pick one at random.

```json
{
  "scene": "scorecard",
  "title": "Healthy Habits Score",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "forest" }, "layout": "card" },
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "How often do you exercise?",
      "choices": [
        { "code": "never", "value": "Never" },
        { "code": "some", "value": "Sometimes" },
        { "code": "daily", "value": "Daily" }
      ],
      "partialScoring": [
        { "value": "never", "score": 0 },
        { "value": "some", "score": 5 },
        { "value": "daily", "score": 10 }
      ]
    },
    {
      "type": "SingleCheck", "code": "q2", "name": "Hours of sleep per night?",
      "choices": [
        { "code": "low", "value": "Under 6" },
        { "code": "ok", "value": "6-8" },
        { "code": "great", "value": "8+" }
      ],
      "partialScoring": [
        { "value": "low", "score": 0 },
        { "value": "ok", "score": 5 },
        { "value": "great", "score": 10 }
      ]
    }
  ],
  "report": {
    "overallAnalysis": {
      "title": "Your Wellness Score",
      "formula": "q1 + q2",
      "levels": [
        { "minScore": null, "maxScore": 10, "label": "Needs Work", "color": "#e57373" },
        { "minScore": 10, "maxScore": null, "label": "Healthy", "color": "#4caf50" }
      ]
    }
  }
}
```

## Notes & limits

- **Expiry:** previews self-destruct after about **1 hour** (`expiresAt`); the link 404s afterward. Recreate it in RooQuiz to keep it permanently.
- **Rate limit:** anonymous creation is capped at about **10 previews per hour** per IP.
- **Validation errors:** a 400 response includes `errors[].path` and `message` — fix the JSON and retry. Most common: a question type or scoring style that doesn't match `scene: "scorecard"`, non-contiguous `levels`, or a `formula` referencing a code that isn't a question.
- **Results page looks empty?** This is a preview (no submission backend); results are computed in the browser from the returned questions + `report`. Make sure `report.overallAnalysis` exists with a `formula`, and scored questions carry `partialScoring`.
- **`language` values:** `en_US` `de_DE` `es` `pt_BR` `fr` `zh_CN` (default) `zh_TW` `ja_JP` `ko_KR`.
