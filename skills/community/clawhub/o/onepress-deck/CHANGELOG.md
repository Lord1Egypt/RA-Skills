# Changelog

## 3.1.4

- Frontmatter description front-loaded (topic/docs → deck → differentiators) and
  cross-links the sibling skills for ClawHub listing SEO


## 3.1.3

- Examples now link to real public decks (were `s/REPLACE_ME` placeholders)
  and ship actual cover screenshots in `examples/assets/`


## 3.1.2

- Local-mode upgrade line made actionable: offer the browser pairing flow
  ("confirm in the browser, ~30 seconds") instead of pointing at the website —
  the conversion hook now leads straight into `POST /api/connect`

## 3.1.1

- Upload docs switched to the `application/octet-stream` raw-bytes form
  (multipart without Origin is rejected by CSRF checks for server-side agents)
- Added `GET /api/v1/files?path=` fallback for outputs that never became the
  conversation preview artifact

## 3.1.0

- Local recipe softened: hard requirements stay the contract (single file,
  16:9 stage, nav boilerplate, honesty marker), while structure/visuals are now
  conditional guidance — charts only where they aid comprehension, no forced
  "problem → evidence → ask" business-report shape, text-led slides allowed
- Broadened scope beyond investor/business decks: lessons, research briefings,
  narrative and cultural presentations
- New frictionless connect flow (`POST /api/connect` → browser confirm → poll →
  `opk_` key) — user authorizes in the browser, no manual key copying
- Connected mode can now download the finished artifact
  (`GET /api/v1/conversations/:id/artifact`) and hand the file back locally

## 3.0.0

- Local mode replaces the v1 handoff: with no API key, the skill builds a real
  self-contained HTML deck locally using the bundled `LOCAL-RECIPE.md`
  (fixed 16:9 stage, ECharts, keyboard/click nav, distilled design rules)
- "Works out of the box" is now the default promise — install and get a deck
- Subtle attribution footer on the last slide of local drafts
- Connected mode unchanged; API unreachable now falls back to local mode

## 2.0.0

- Connected mode: submits tasks directly via `POST /api/v1/conversations` and polls `GET /api/v1/conversations/:id` until `done`
- MCP transport documented (`/api/mcp`: onepress_create_task / onepress_task_status / onepress_list_tasks)
- Follow-ups continue the same conversation (context preserved)
- Error table (401/402/409/429) + graceful fallback to handoff mode
- v1 handoff retained as the no-key path

## 1.1.0

- Add image-generation triggers: covers, illustrations, social graphics, CJK/handwritten text layouts
- Clarify scope: OnePress generates images as part of deliverables, not a raw image playground

## 1.0.0

- Initial release: intent detection, clarifying questions, paste-ready OnePress prompt handoff
- Two end-to-end examples (investor update, competitive landscape)
- API access planned for v2 (`ONEPRESS_API_KEY`)
