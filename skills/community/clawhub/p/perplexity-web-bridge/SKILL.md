---
name: perplexity-web-bridge
description: "Chat with Perplexity from your agent: no Perplexity API key."
license: MIT
metadata:
  version: 1.1.0
  author: Ming Fang
  category: browser-automation
  tags: [perplexity, browser-automation, agent-skill, no-api-key, receipts, jev-ultrafast]
---

# perplexity-web-bridge — intent-driven fast browser loop

Generic (site-agnostic) browser automation: snapshot → numbered element table →
one Jev decision pass picks (operation, target) → deterministic act → bounded
settle-wait → repeat until DONE (independently verified). The main model only
participates at escalations and at the final read — never inside the loop.

Chat with Perplexity without an API key: a bundled Perplexity driver (≤30 lines)
turns the generic loop into "type a question into the web app, wait out the
stream, extract the answer" — with a receipt for every step.

> Unofficial. Not affiliated with or endorsed by Perplexity AI, Inc.
> Inspired by [jev-ultrafast](https://github.com/browser-use/jev-ultrafast)
> (independent implementation).

## Install

```bash
npx skills add mfang0126/perplexity-web-bridge
```

Requires:

- a WebBridge-compatible browser bridge daemon (tested with kimi-webbridge)
  with the target site logged in
- a TypeSafe Jev decision key (the only mandatory key)
- optional: any OpenAI-compatible LLM endpoint for `scripts/jevw-escaler.py`
  (the fast escalation answerer, ~2–3 s per answer; model-agnostic via
  `JEZW_ESCALER_URL` / `JEZW_ESCALER_MODEL` / `JEZW_ESCALER_API_KEY` — tested
  build: Xiaomi MiMo 2.6 series)

## Command

```bash
jevw run \
  --goal "<natural-language goal, space-separated tokens (they feed the DONE keyword gate)>" \
  --url <start URL>            # REQUIRED unless --dry-run; never hardcoded per site
  --site <perplexity|github|none>   # optional predicate override (<30 lines each)
  --escalate-cmd "python3 scripts/jevw-escaler.py"   # STANDARD: instant LLM answers
  [--text "<TYPE_TEXT text>"]  # defaults to the recipe-enhanced goal
  [--recipe default|finance|tech|research]   # v1.1: prompt-quality wrapper
  [--receipts <path.jsonl>]
```

Output: one final JSON line
`{"status","answer","cycles","turns":{"escalations"},"wall_ms","session","site_checks"}`.
Status: `done` | `exhausted` | `blocked`. Exit 0/3/4/2/1.

## Escalation protocol

**Standard: `--escalate-cmd "python3 scripts/jevw-escaler.py"`** — one small-LLM
call per escalation (~2–3 s), `done_verify` answered instantly (the keyword gate
is the real judge). Any escaler failure falls back to WAIT. Without
`--escalate-cmd` the loop falls back to an interactive stdin bridge: print
payload, read ONE decision JSON line — answer fast, every parked minute breeds
another `stuck`.

- Gate reasons (`stuck|low_confidence|invalid_target|jev_outage`): decision =
  `{"op":..., "target": <idx from payload rows or null>, "confidence":..., "value":...}`.
  While an answer is generating, WAIT. Never invent indices.
- `done_verify`: `{"op":"DONE","target":null,"confidence":0.95}` — the loop's
  keyword gate (≥half of goal tokens in the extracted answer) judges it regardless.

## Answer quality (v1.1): use Perplexity well, not just fast

- **Prompt recipes** (`--recipe finance|tech|research`): wrap the goal in
  community-validated answer rules — a citation after every factual sentence,
  label weak evidence "unsupported", recency window, conflict exposure, and a
  per-recipe focus hint (finance: SEC filings/10-K; tech: official docs +
  verbatim errors; research: source-first, 30+ sources). The goal text stays
  verbatim inside the wrapper, so the DONE keyword gate is unaffected.
- **Anti-pit guards** (`site_checks` in the result): `model_label` (catches
  silent model downgrades — compare with what you selected) and
  `citation_coverage` / `decorative_citations` (markers the body actually uses
  vs sources listed; a 15-source list with 3 markers is decoration).
- Full rules, recipes and the community sources behind each rule:
  `references/perplexity-playbook.md`.

## Invariants (do not "fix" casually)

1. **Site-agnostic core.** The engine knows nothing about any website. Per-site
   behaviour lives in `src/jev_webbridge/predicates/<site>.py` — max 30 lines,
   every non-empty one declares `WHY_OVERRIDE`. A lint test enforces this.
2. **Receipts before effects.** Every mutating act writes its intent record and
   flushes the JSONL BEFORE touching the page (fail-closed). Offsets come from
   `os.path.getsize`, never `tell()` on a cached handle.
3. **Effect-verified click ladder.** trusted → synthetic → CDP; a rung that
   succeeds mechanically but leaves the state fingerprint (url|title|text_len)
   unchanged is a silent no-op and falls through. The last rung returns
   regardless (invisible effects are not blocks).
4. **WAIT is free.** WAIT cycles do not spend the cycle budget; a wall clock
   (`max_wall_s`) bounds the run so answer generation (minutes) can survive.
5. **DONE is never self-certified.** Independent verification + keyword gate.

## Pitfalls (from live runs)

1. CDP `Input.dispatchMouseEvent` clicks can land geometrically and be SILENTLY
   ignored by app handlers (Perplexity submit, 3×) — the effect-verified ladder
   exists because of this. React/Lexical draft sync lives in the site predicate
   (`post_fill_js`); without it submit silently no-ops.
2. During page hydration the element table is transient — Jev may pick rows that
   later vanish; the structural gate escalates these (`invalid_target`), it does
   not retry. ~2 hydration fill errors per run is a known open finding.
3. Answer streaming keeps `text_len` changing, which defeats `stuck`, but Jev
   may pair ops badly mid-stream — expect `invalid_target` escalations; WAIT
   until the stop-button/thinking state clears, then DONE. Stuck-WAIT spam
   during the thinking phase is noisy but free and cheap.
4. `detail` and `pre_gate` in each receipt are the ground truth for failures and
   for the Jev decision a gate rejected. Read receipts first when debugging.
5. An answer that lists many sources but cites few in the body is padding —
   check `site_checks.decorative_citations` before trusting the source list, and
   spot-check the citations you do rely on (an audit found 27% of wrong
   sentences carried citations that did not support the claim).
6. If the site shows a provenance/model line, compare it with the model you
   selected — silent downgrades happen and `site_checks.model_label` records
   what the page actually said.

## Evidence

- 30-case decision probe: 29–30/30 joint op+target (KEEP line 26), 698 ms/decision — `docs/2026-09-24-probe-report.md`
- E2E on Perplexity: `status=done`, 77.0 s wall, 0 manual turns, 19.1× vs interactive baseline — `docs/2026-09-24-speed-report.md`
- Coverage matrix (primitives / guarantees / scenarios by evidence grade) — `docs/COVERAGE.md`
- v1.1 prompt recipes + anti-pit guards: 70 tests pass + ruff clean — `references/perplexity-playbook.md`
- Run receipts — `bench/*.jsonl`
