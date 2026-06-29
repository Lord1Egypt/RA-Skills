---
name: preview-outcome
description: Create a shareable RooQuiz preview personality / outcome test — options vote for result types and the most-voted type is the result — and get a link to open in the browser. No account, login, or API key required. Use this when someone wants to build, try out, or share a personality quiz, a "which X are you" / type / archetype test, or any quiz where there are no right answers and the taker is sorted into one of several result types. For a right/wrong graded quiz, use the preview-quiz skill; for a scored questionnaire that totals points into a level, use the preview-scorecard skill.
---

# Create a RooQuiz Preview Outcome (Personality) Test

POST an outcome test as JSON to RooQuiz's open preview endpoint and instantly get a **short-lived (~1 hour)**, **browser-openable** preview link. The creation endpoint is public (`access.create => true`), so this needs **no account, login, API key, or credentials** — anything that can make an HTTP request can use it.

An **outcome test** (`scene: "outcome"`) is a personality / type test: there are no right answers and no numeric score. Each option *votes* for one or more result types, and the most-voted type is shown as the result (e.g. "The Explorer" vs "The Homebody"). It produces a **temporary preview**, not a permanently published form — the link expires automatically (recreate it in RooQuiz if you need to keep it).

Two sibling skills cover the other assessment types — pick the one that matches:
- **preview-quiz** — a right/wrong assessment where correct answers earn points and the taker gets a graded score.
- **preview-scorecard** — a scored questionnaire where each option adds points toward a total that buckets into a level.

## Three steps

1. **Build the outcome JSON** (structure below).
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

<the outcome JSON as the raw request body>
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

## Outcome JSON — top level

```jsonc
{
  "scene": "outcome",              // required & fixed for this skill. Sets allowed question types and scoring. Cannot change after creation.
  "title": "What's Your X?",       // required
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
- Every question needs a **unique `code`** (string); option `code`s must be unique within their question. A question/option `code` must be a valid identifier — start with a letter or `_`, then only letters/digits/`_` (no `-`, spaces, or leading digit), max 64 chars, and not a reserved math word (`e`, `E`, `pi`, `PI`, `tau`, `phi`, `i`, `Infinity`, `NaN`, `true`, `false`, `null`, `undefined`). The server rejects violations with HTTP 400.
- `name` is the question text; `description` is optional helper text.
- Unknown top-level fields are silently ignored by the server (no error).
- **`secret`**: omit it for a clean link that works with just the token (tokens are random 8-char and expire in ~1 hour — fine for previews). Set it to make the token unguessable, at the cost of requiring `?secret=` on the link. Default: omit.

## Themes

`personalized.theme.name` sets the visual theme. Omit `theme` to default to `light`. Set it as `"personalized": { "key": "default", "theme": { "name": "synthwave" }, "layout": "card" }` (`layout` is still only `list` or `card`).

Pick a theme that fits the quiz's topic/mood. **To use a random theme** — when the user asks for one, wants variety, or has no preference — just choose a random `name` from this list when building the JSON (there's no server-side "random" option). Recommended palette:

| name | vibe / good for |
| --- | --- |
| `light` | clean neutral bright; default, general |
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

The full daisyUI theme set also renders (e.g. `emerald`, `dracula`, `retro`, `nord`, `sunset`, `winter`, `lofi`, `garden`, `aqua`, `business`, `lemonade`, `dim`, `bumblebee`, `acid`, `fantasy`, `wireframe`, `black`, `cmyk`) — the table above is just the recommended palette. The server doesn't validate the name, so a typo silently falls back to default styling rather than erroring.

## Question types

Each field is `{ type, code, name, ... }`. An outcome test allows **only** these types:

- **Choice** (carry `choices: [{ code, value }]`, where `value` is the option label):
  `SingleCheck` (single), `MultiCheck` (multiple), `DropDown`, `TrueFalse` (no choices)
- **Display only** (never scored): `Statement` (`content`), `Breaker` (page break / divider), `Swiper` (image carousel, `items`)

Input/number/date/time/`Rate`/`FillBlank`/`Ordering`/`Cascade` are **not** allowed here — an outcome test only votes via the choice types above. Optional shared props on any field: `required`, `description`, `explain`, `hidden`, `activeColor` (`primary`/`secondary`/`accent`/`neutral`), `layout` (`list`/`grid`).

## Scoring

Map each option to the result type(s) it votes for with **`outcomeScoring`** (a field-level array, sitting next to `choices`). Do **not** set `correctAnswer`, `exactScoring`, or `partialScoring` — none of those are allowed in the outcome scene.

```jsonc
"outcomeScoring": [
  { "value": "a", "outcomes": [{ "code": "explorer" }] },
  { "value": "b", "outcomes": [{ "code": "homebody" }] }
]
```

- Each `value` must be one of that question's `choices[].code`s.
- Each `outcomes[].code` must exist in `report.outcomeAnalysis.outcomes` (defined below).
- An option may vote for more than one type — list multiple entries in its `outcomes` array.

At the end, the type with the most votes is shown as the result.

## Report configuration

Two parts are needed:

- **`report.overallAnalysis`** is **required** even though there's no numeric score — give it at least a `title`.
- **`report.outcomeAnalysis`** defines the result types (every `code` referenced from a field's `outcomeScoring` must be listed here).

```jsonc
"report": {
  "overallAnalysis": { "title": "Your Result" },
  "outcomeAnalysis": {
    "source": "votes",
    "outcomes": [
      { "code": "explorer", "name": "The Explorer", "color": "#ff9800", "description": "You crave adventure!" },
      { "code": "homebody", "name": "The Homebody", "color": "#4caf50", "description": "You treasure comfort." }
    ]
  }
}
```

Each outcome carries a `code` (referenced by `outcomeScoring`), a display `name`, and optional `color` (hex) and `description`. Define at least two so the vote has something to choose between.

## Common mistakes

These wrong patterns get reached for out of habit; the server rejects them with HTTP 400. The formats above are correct — match them exactly.

- **Option lists are `choices`, never `options`.** Every choice question uses `"choices": [{ "code": "a", "value": "Label" }]`. There is no `options` key.
- **Question/option codes must be valid identifiers, not arbitrary text** — no hyphens (`type-a`), spaces, or leading digits (`1q`), and not reserved math words. Watch out for **5+ options coded `a,b,c,d,e`**: `e` (Euler's number) is reserved and rejected — use `o1, o2, …` or another non-reserved identifier. (This constraint is on question/option codes; result-type codes in `outcomeAnalysis.outcomes` are free-form.)
- **Scoring is a field-level `outcomeScoring` array, not a value nested inside each choice.** Correct: `"outcomeScoring": [{ "value": "a", "outcomes": [{ "code": "type1" }] }]` next to `choices`. Wrong: `{ "code": "a", "value": "…", "outcomeScoring": { "type1": 1 } }` on the option.
- **`report.overallAnalysis` is still required** (give it a `title`) — the result *types* go in the separate `report.outcomeAnalysis.outcomes`.
- **Every `outcomes[].code` used in scoring must be defined in `outcomeAnalysis.outcomes`**, or you'll get a 400 for an undefined result code.
- **Don't set `correctAnswer`/`exactScoring`/`partialScoring`** — those belong to the quiz/scorecard scenes and are rejected here.

## Complete example

The `personalized.theme.name` is matched to the topic (see **Themes** above) — swap in any other name, or pick one at random.

```json
{
  "scene": "outcome",
  "title": "What's Your Travel Style?",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "pastel" }, "layout": "card" },
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "Ideal weekend?",
      "choices": [
        { "code": "a", "value": "Hiking a new trail" },
        { "code": "b", "value": "Cozy at home" }
      ],
      "outcomeScoring": [
        { "value": "a", "outcomes": [{ "code": "explorer" }] },
        { "value": "b", "outcomes": [{ "code": "homebody" }] }
      ]
    },
    {
      "type": "SingleCheck", "code": "q2", "name": "Pick a vacation:",
      "choices": [
        { "code": "a", "value": "Backpacking abroad" },
        { "code": "b", "value": "A quiet cabin" }
      ],
      "outcomeScoring": [
        { "value": "a", "outcomes": [{ "code": "explorer" }] },
        { "value": "b", "outcomes": [{ "code": "homebody" }] }
      ]
    }
  ],
  "report": {
    "overallAnalysis": { "title": "Your Result" },
    "outcomeAnalysis": {
      "source": "votes",
      "outcomes": [
        { "code": "explorer", "name": "The Explorer", "color": "#ff9800", "description": "You crave adventure and new horizons!" },
        { "code": "homebody", "name": "The Homebody", "color": "#4caf50", "description": "You treasure comfort and calm." }
      ]
    }
  }
}
```

## Notes & limits

- **Expiry:** previews self-destruct after about **1 hour** (`expiresAt`); the link 404s afterward. Recreate it in RooQuiz to keep it permanently.
- **Rate limit:** anonymous creation is capped at about **10 previews per hour** per IP.
- **Validation errors:** a 400 response includes `errors[].path` and `message` — fix the JSON and retry. Most common: a question type that doesn't match `scene: "outcome"`, or an `outcomeScoring` referencing a result `code` that isn't defined in `outcomeAnalysis.outcomes`.
- **Results page looks empty?** This is a preview (no submission backend); results are computed in the browser from the returned questions + `report`. Make sure `report.overallAnalysis` exists and every voted question carries `outcomeScoring` pointing at defined outcomes.
- **`language` values:** `en_US` `de_DE` `es` `pt_BR` `fr` `zh_CN` (default) `zh_TW` `ja_JP` `ko_KR`.
