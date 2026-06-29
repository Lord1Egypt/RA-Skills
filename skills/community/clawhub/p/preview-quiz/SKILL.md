---
name: preview-quiz
description: Create a shareable RooQuiz preview quiz — a right/wrong assessment where correct answers earn points and the taker gets a score — and get a link to open in the browser. No account, login, or API key required. Use this when someone wants to build, try out, or share a graded quiz, test, trivia, or exam with correct answers and a final score. For a scored questionnaire where every option adds points, use the preview-scorecard skill; for a personality/type test with no right answers, use the preview-outcome skill.
---

# Create a RooQuiz Preview Quiz

POST a quiz as JSON to RooQuiz's open preview endpoint and instantly get a **short-lived (~1 hour)**, **browser-openable** preview link. The creation endpoint is public (`access.create => true`), so this needs **no account, login, API key, or credentials** — anything that can make an HTTP request can use it.

A **quiz** (`scene: "quiz"`) is a right/wrong assessment: each scored question carries a correct answer and earns points; the total is the sum of earned points, then bucketed into levels on the results page. It produces a **temporary preview**, not a permanently published form — the link expires automatically (recreate the quiz in RooQuiz if you need to keep it).

Two sibling skills cover the other assessment types — pick the one that matches:
- **preview-scorecard** — a scored questionnaire where each option adds points toward a total + level (no "correct" answer).
- **preview-outcome** — a personality / type test where options vote for result types and the most-voted type wins (no right answers).

## Three steps

1. **Build the quiz JSON** (structure below).
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

<the quiz JSON as the raw request body>
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

## Quiz JSON — top level

```jsonc
{
  "scene": "quiz",                 // required & fixed for this skill. Sets allowed question types and scoring. Cannot change after creation.
  "title": "My Quiz",              // required
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
  "secret": "optional; if set, the preview link must include ?secret="
}
```

Key points:
- Every question needs a **unique `code`** (string); option `code`s must be unique within their question. A `code` must be a valid identifier — start with a letter or `_`, then only letters/digits/`_` (no `-`, spaces, or leading digit), max 64 chars, and not a reserved math word (`e`, `E`, `pi`, `PI`, `tau`, `phi`, `i`, `Infinity`, `NaN`, `true`, `false`, `null`, `undefined`). The server rejects violations with HTTP 400.
- `name` is the question text; `description` is optional helper text.
- Unknown top-level fields are silently ignored by the server (no error).
- **`secret`**: omit it for a clean link that works with just the token (tokens are random 8-char and expire in ~1 hour — fine for previews). Set it to make the token unguessable, at the cost of requiring `?secret=` on the link. Default: omit.

## Themes

`personalized.theme.name` sets the visual theme. Omit `theme` to default to `light`. Set it as `"personalized": { "key": "default", "theme": { "name": "synthwave" }, "layout": "card" }` (`layout` is still only `list` or `card`).

Pick a theme that fits the quiz's topic/mood. **To use a random theme** — when the user asks for one, wants variety, or has no preference — just choose a random `name` from this list when building the JSON (there's no server-side "random" option). Recommended quiz palette:

| name | vibe / good for |
| --- | --- |
| `light` | clean neutral bright; default, formal/general quizzes |
| `corporate` | professional blue+gray; B2B, career, business |
| `dark` | modern sleek dark; tech, night, cool personality quizzes |
| `cupcake` | soft pink, cute, rounded; fun, food, kids, lighthearted |
| `pastel` | gentle pastel artsy; lifestyle, aesthetics, soft mood |
| `valentine` | pink romantic hearts; love, relationships, holidays |
| `synthwave` | neon purple/pink retro; gaming, trends, bold personality |
| `luxury` | dark + gold premium; finance, luxury, high-end |
| `forest` | deep green nature; environment, health, outdoors |
| `coffee` | warm brown cozy; food & drink, cafe, lifestyle |
| `autumn` | warm orange/brown seasonal; autumn, cozy, harvest |
| `halloween` | purple + orange spooky; Halloween, horror, festive |
| `night` | deep calm blue; astronomy, mindfulness, calm tech |
| `cyberpunk` | high-contrast neon yellow; tech, esports, gaming |

The full daisyUI theme set also renders (e.g. `emerald`, `dracula`, `retro`, `nord`, `sunset`, `winter`, `lofi`, `garden`, `aqua`, `business`, `lemonade`, `dim`, `bumblebee`, `acid`, `fantasy`, `wireframe`, `black`, `cmyk`) — the table above is just the recommended quiz palette. The server doesn't validate the name, so a typo silently falls back to default styling rather than erroring.

## Question types

Each field is `{ type, code, name, ... }`. In a quiz you can use:

- **Choice** (carry `choices: [{ code, value }]`, where `value` is the option label):
  `SingleCheck` (single), `MultiCheck` (multiple; optional `min`/`max`), `DropDown`, `Cascade`, `Ordering`, `TrueFalse` (no choices)
- **Input**: `FillBlank` (optional `multiline`), `NumberField`, `DateField` (needs `precision`), `TimeField`
- **Display only** (never scored): `Statement` (`content`), `Breaker` (page break / divider), `Swiper` (image carousel, `items`)

`Rate` is **not** allowed in a quiz (it's a scorecard type). Optional shared props on any field: `required`, `description`, `explain`, `hidden`, `activeColor` (`primary`/`secondary`/`accent`/`neutral`), `layout` (`list`/`grid`).

## Scoring

Add **`correctAnswer`** + **`exactScoring`** to each scored question:

```jsonc
"correctAnswer": "b",
"exactScoring": { "mode": "exactMatch", "score": 10 }
```

**`correctAnswer` value depends on the question type:** single choice = the correct option's `code` (string); multiple/ordering = array of `code`s; fill-in = string; true/false = boolean.

Optional partial credit: `exactScoring.accuracy` + `extraLevels`, or `partialScoring` on choice questions (using `partialScoring` requires `exactScoring` too). Display-only fields (`Statement`/`Breaker`/`Swiper`) are never scored — leave scoring off them.

## Report configuration

`report.overallAnalysis` is **required**. A quiz **auto-sums** earned points, so **omit `formula`** — just map the total to `levels`.

```jsonc
"report": {
  "overallAnalysis": {
    "title": "Your Score",
    "summaryTemplate": "<p><art-field data-type=\"fieldVariable\" data-cid=\"score\"></art-field> pts · <art-field data-type=\"fieldVariable\" data-cid=\"level\"></art-field></p>",
    "levels": [                    // map total score → level (see strict rules below)
      { "minScore": null, "maxScore": 10, "label": "Beginner" },
      { "minScore": 10, "maxScore": 20, "label": "Intermediate" },
      { "minScore": 20, "maxScore": null, "label": "Expert", "description": "Top tier!" }
    ]
  }
}
```

**Strict `levels` rules** (violations return HTTP 400): the first level's `minScore` must be `null` (−∞); the last level's `maxScore` must be `null` (+∞); middle levels have finite numbers on both ends; for adjacent levels `current.minScore === previous.maxScore`; `maxScore` strictly increases down the array. A single level has `null` on both ends.

Levels may carry a `cta` (results-page button): `{ enabled, type: "link", text, url, newWindow }`. When enabled, `text` and `url` are required, and `url` must be an `http`/`https` link. `summaryTemplate` defaults to a built-in template if omitted.

## Common mistakes

These wrong patterns get reached for out of habit; the server rejects them with HTTP 400. The formats above are correct — match them exactly.

- **Option lists are `choices`, never `options`.** Every choice question uses `"choices": [{ "code": "a", "value": "Label" }]`. There is no `options` key.
- **Codes must be valid identifiers, not arbitrary text** — no hyphens (`type-a`), spaces, or leading digits (`1q`), and not reserved math words. Watch out for **5+ options coded `a,b,c,d,e`**: `e` (Euler's number) is reserved and rejected — use `o1, o2, …` or another non-reserved identifier.
- **Scoring is field-level, not nested inside each choice.** `correctAnswer` and `exactScoring` sit next to `choices` on the field, not on an individual option.
- **Don't set a `formula` for a quiz** — quizzes auto-sum earned points. `formula` is a scorecard thing; including it here is unnecessary (use the preview-scorecard skill if you actually want a custom total).
- **`report.overallAnalysis` is required** — give it at least a `title` and a valid `levels` array.

## Complete example

The `personalized.theme.name` is matched to the topic (see **Themes** above) — swap in any other name, or pick one at random.

```json
{
  "scene": "quiz",
  "title": "World Capitals Quiz",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "corporate" }, "layout": "card" },
  "indexDisplayMode": "number",
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "Capital of France?", "required": true,
      "choices": [
        { "code": "a", "value": "Berlin" },
        { "code": "b", "value": "Paris" },
        { "code": "c", "value": "Rome" }
      ],
      "correctAnswer": "b",
      "exactScoring": { "mode": "exactMatch", "score": 10 }
    },
    {
      "type": "MultiCheck", "code": "q2", "name": "Which are in Asia?", "required": true,
      "choices": [
        { "code": "a", "value": "Japan" },
        { "code": "b", "value": "Brazil" },
        { "code": "c", "value": "Thailand" }
      ],
      "correctAnswer": ["a", "c"],
      "exactScoring": { "mode": "exactMatch", "score": 10 }
    }
  ],
  "report": {
    "overallAnalysis": {
      "title": "Your Score",
      "summaryTemplate": "<p><art-field data-type=\"fieldVariable\" data-cid=\"score\"></art-field> pts · <art-field data-type=\"fieldVariable\" data-cid=\"level\"></art-field></p>",
      "levels": [
        { "minScore": null, "maxScore": 10, "label": "Novice" },
        { "minScore": 10, "maxScore": 20, "label": "Good" },
        { "minScore": 20, "maxScore": null, "label": "Perfect" }
      ]
    }
  }
}
```

## Notes & limits

- **Expiry:** previews self-destruct after about **1 hour** (`expiresAt`); the link 404s afterward. Recreate the quiz in RooQuiz to keep it permanently.
- **Rate limit:** anonymous creation is capped at about **10 previews per hour** per IP.
- **Validation errors:** a 400 response includes `errors[].path` and `message` — fix the JSON and retry. Most common: a question type or scoring style that doesn't match `scene: "quiz"`, or non-contiguous `levels`.
- **Results page looks empty?** This is a preview (no submission backend); results are computed in the browser from the returned questions + `report`. Make sure `report.overallAnalysis` exists and scored questions carry `correctAnswer` + `exactScoring`.
- **`language` values:** `en_US` `de_DE` `es` `pt_BR` `fr` `zh_CN` (default) `zh_TW` `ja_JP` `ko_KR`.
