# Coverage & Capability Matrix

> Narrative structure for README/diagram: **primitives → loop guarantees → composite
> scenarios** (each with an evidence grade). "Scenario" alone is not a stable unit —
> composites multiply; primitives and guarantees do not.

## A. Action primitives — 6/6 live-verified

| Primitive | What it does | Evidence |
|---|---|---|
| `TYPE_TEXT` | Fill native inputs & contenteditable; site `post_fill_js` hook keeps React/Lexical drafts in sync | E2E run3 (`bench/2026-09-24-perplexity_runs_v2.jsonl` c2–c4) |
| `CLICK` | 3-rung effect-verified ladder: trusted → synthetic → CDP; silent no-ops fall through | run3 c2 `synthetic_click` fired submit after CDP was ignored 3× (`runs_v2diag.jsonl`) |
| `SCROLL` | One viewport per step, lazy content discovery | probe cases 22–24 (`tests/fixtures/probe_cases.jsonl`) |
| `WAIT` | Free toward the cycle budget, wall-clock bounded | run3 c5–c11 survived a 2-min generation phase |
| `DONE` | Independent verification + goal-keyword gate | run3 c12 → `done_verify` → keywords → done |
| `BLOCKED` | All rungs failed; screenshot + receipts preserved | `test_blocked_when_all_rungs_fail`; v1 run1 capture |

Also: `--url` navigation, answer extraction, JSONL receipts (`detail`, `pre_gate`).

## B. Loop guarantees — live-verified

- stuck detection on a stable state signature
- structural gate (`op ⊆ row ops`, index exists) with `pre_gate` provenance
- low-confidence / Jev-outage escalation to an instant LLM answerer (mimo-flash, 2–3 s)
- act-before-receipts flush (fail-closed), pre-act readback
- acceptance gate: keyword coverage + terminal readback

## C. Composite scenarios (by evidence grade)

| Grade | Scenarios |
|---|---|
| ✅ live E2E (×2 runs) | search → submit → stream-wait → extract (Perplexity) |
| ✅ live probes (30 cases, 29–30/30) | cross-page clicking, GitHub blob/Actions/search navigation |
| ⚠️ probes only | model-menu switching (occlusion; ladder fixed, not re-run), multi-turn follow-up (capability present, untested) |
| ❌ out of scope | file upload, iframe, shadow DOM, login/credentials |

## Diagram plan (for publish)

1. Loop state machine: observe → table → Jev head → gates → executor ladder → receipts → settle → WAIT / stuck / DONE
2. This matrix as a coverage table

Credit line for README/figure captions: *Inspired by jev-ultrafast.*

## Naming & discovery (researched 2026-09-24)

- Marketplace fact (our own release pipeline, validated on `conductor` v1.3.0): **description
  wins discovery** — skills.sh indexes name/description/body, but only the description carries
  long-tail queries; agent-side skill selection reads the description's first sentence. Name must
  be short, install-friendly, collision-checked (`hermes skills search`), and equal the repo name
  (single-skill repo, `npx skills add`).
- Search intent (Perplexity research, 2026-09-24): "chat with perplexity" = navigational (large
  volume, low tool-seeker value); "perplexity automation" and "use perplexity without api key" =
  tool-seeking long tail (small volume, high conversion). Community READMEs put "No API key
  required" on the first screen (`perplexity-web-mcp`, `perplexity-web-wrapper`,
  `Perplexity-Automation`, `perplexity-ai` — the `perplexity-<what>` naming pattern).
- Trademark: putting "Perplexity" in the **product name** (e.g. "Chat with Perplexity") reads as
  an official product and carries more risk than descriptive use in the description. Community
  norm: descriptive use + "Unofficial" + a non-affiliation disclaimer.

### Recommendation

- **Repo/skill name**: `perplexity-web-bridge` (follows the `perplexity-<what>` community pattern;
  still generic inside).
- **Description (trigger first, ≤60 chars)**: `"Chat with Perplexity from your agent: no Perplexity API key."` — exactly 60 chars (measured); honest scope ("Perplexity API key") while still containing the money phrase "no … API key".
- **README H1**: "Chat with Perplexity — from any agent, no API key" + one-line: "Unofficial. Generic fast-loop web automation (search, click, wait, verify) with a bundled Perplexity driver. Inspired by jev-ultrafast."
- **Disclaimer** (README top or bottom): "Perplexity is a trademark of Perplexity AI, Inc. This project is unofficial and not affiliated with or endorsed by Perplexity AI."
- README keyword block for long tail: `perplexity automation`, `use perplexity without api key`,
  `perplexity web mcp alternative`, `browser automation skill`, `no api key`.
- The generic engine keeps its name in code (`jev-webbridge` / `src/`); only the published skin
  is named for the traffic.
