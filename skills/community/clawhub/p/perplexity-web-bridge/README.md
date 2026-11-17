# Chat with Perplexity — use Perplexity without an API key

[English](README.md) | [中文](README.zh-CN.md)

Use Perplexity without an API key: this unofficial open-source agent skill drives
the **Perplexity web UI** — search, click, wait, extract — with your existing
logged-in session. One command runs a whole task autonomously and writes a
receipt for every step. The decision loop is site-agnostic and inspired by
[jev-ultrafast](https://github.com/browser-use/jev-ultrafast) ("Inspired by
jev-ultrafast" — the code is an independent implementation).

> **Keys, honestly**: no **Perplexity** API key (that's the point — your web
> subscription instead of per-question API pricing). It does need a free
> TypeSafe Jev decision key; the escalation answerer takes ANY
> OpenAI-compatible LLM key (optional — tested with Xiaomi MiMo 2.6 series).
> See [Requirements](#requirements).

> Unofficial. Not affiliated with or endorsed by Perplexity AI, Inc.
> "Perplexity" is a trademark of Perplexity AI, Inc.

## Why

- **No Perplexity API key, no per-question API cost** — it types into and clicks
  the same web app you use, on your subscription.
- **Autonomous fast loop** — snapshot → numbered element table → one tiny model
  call picks (operation, target) → deterministic act → bounded wait → repeat
  until an independently verified DONE. The big model never sits inside the loop.
- **Receipts, not vibes** — fail-closed JSONL evidence chain: what was decided,
  why a gate rejected a decision (`pre_gate`), which click rung fired, and the
  final answer verification.
- **Built with Xiaomi MiMo 2.6 series, model-agnostic by design** — measured on
  the MiMo 2.6 build: end-to-end **24.5 min → 77 s (19.1×)** vs a human-in-the-loop
  baseline; escalations answered in **2–3 s** (was 144–302 s); decisions 698 ms.
  Swap in any OpenAI-compatible model — only the TypeSafe Jev decision key is
  mandatory.

## What you get

- `jevw run --goal … --url …` — one-command task runner (search, fill, submit,
  stream-wait, extract)
- `scripts/jevw-escaler.py` — instant escalation answerer (a small LLM answers
  the loop's questions in ~2–3 s; a canned `done_verify` is free)
- Coverage matrix & evidence: [`docs/COVERAGE.md`](docs/COVERAGE.md)
- Measured numbers: [`docs/2026-09-24-speed-report.md`](docs/2026-09-24-speed-report.md)

## More than fast: use Perplexity well

Speed is the hook; answer quality is the point. `--recipe finance|tech|research`
wraps your goal in the community-validated answer rules (citations after every
sentence, "unsupported" labeling, recency window, conflict exposure), and two
automatic guards watch the answer afterwards: silent **model-downgrade
detection** (the #1 recurring complaint) and **decorative-citation detection**
(a 15-source list the body never cites). Both ship in v1.1 (70 tests pass). See
[`references/perplexity-playbook.md`](references/perplexity-playbook.md) for
the distilled playbook and the sources behind each rule.

## Requirements

- A WebBridge-compatible browser bridge daemon (tested with kimi-webbridge)
  controlling a browser where Perplexity is logged in
- A [TypeSafe](https://typesafe.ai) Jev decision key (the fast decision head — the only mandatory key)
- Optional: any OpenAI-compatible LLM endpoint for the escalation answerer
  (`JEZW_ESCALER_URL` / `JEZW_ESCALER_MODEL` / `JEZW_ESCALER_API_KEY`; tested
  build: Xiaomi MiMo 2.6 flash)

## Install

```bash
npx skills add mfang0126/perplexity-web-bridge   # any of 77 agent harnesses
```

## 60-second usage

```bash
jevw run \
  --goal "research the best database options for a growing startup" \
  --url https://www.perplexity.ai/ \
  --site perplexity \
  --escalate-cmd "python3 scripts/jevw-escaler.py"
```

Output: one JSON line with `status`, the extracted `answer`, cycle and
escalation counts, wall time — plus the JSONL receipt file.

## How it works

![jev-webbridge decision loop](docs/assets/loop.svg)
*(source: [`docs/assets/loop.mmd`](docs/assets/loop.mmd) — "Inspired by jev-ultrafast")*

1. **Observe** — one JS snapshot becomes a numbered element table (no raw DOM
   ever reaches the model)
2. **Decide** — one Jev forward pass classifies (operation, target) in
   ~0.7–0.9 s; gates check the decision against the table (`op ⊆ row ops`)
3. **Act** — 3-rung effect-verified click ladder (trusted → synthetic → CDP);
   silent no-ops fall through to the next rung
4. **Settle & repeat** — bounded wait, WAIT cycles don't spend the budget;
   stuck/confidence/Jev-outage escalations go to the fast answerer
5. **Verify** — DONE is independently verified and the goal's keywords must
   appear in the extracted answer

Full matrix (6 action primitives, 5 loop guarantees, composite scenarios with
evidence grades): [`docs/COVERAGE.md`](docs/COVERAGE.md).

## Comparison

| | Perplexity API | `perplexity-web-mcp` style | raw Playwright | **this skill** |
|---|---|---|---|---|
| No Perplexity API key | ✗ | ✓ | ✓ | ✓ |
| Works on your existing subscription | ✗ | ✓ | ✓ | ✓ |
| Autonomous multi-step loop | ✗ | partial | hand-written | ✓ |
| Decision receipts / evidence chain | ✗ | ✗ | ✗ | ✓ |
| Site-agnostic core | n/a | ✗ (one site) | per script | ✓ (per-site ≤30-line patches) |

## Evidence (2026-09-24)

| Test | Result | Evidence |
|---|---|---|
| 30-case decision probe (joint op+target) | 29–30 / 30 (KEEP line: 26) | [`docs/2026-09-24-probe-report.md`](docs/2026-09-24-probe-report.md) |
| E2E: multi-part research query on Perplexity | `status=done`, 77.0 s wall, 0 manual turns | [`docs/2026-09-24-speed-report.md`](docs/2026-09-24-speed-report.md) |
| vs interactive-escalation baseline | 24.5 min → 77 s (**19.1×**) | same |
| Receipt integrity | pre-act flush, fail-closed, `pre_gate` provenance | `bench/*.jsonl` in this repo |

## FAQ

**How do I use Perplexity without an API key?**
Run the skill against a browser where you are logged in to Perplexity. It types
your question into the web app and reads the answer — no Perplexity API key and
no per-question API charge.

**Do I still need any keys at all?**
One mandatory, one optional, neither from Perplexity: a free TypeSafe Jev
decision key (the fast decision head — ~$0.00001 per decision) and, optionally,
any OpenAI-compatible LLM key for the escalation answerer (the tested build is
Xiaomi MiMo 2.6 flash; any provider works). What you never need is a Perplexity
API key.

**Is this an official Perplexity product?**
No. It is an unofficial, unaffiliated open-source project.

**What is it inspired by?**
The [jev-ultrafast](https://github.com/browser-use/jev-ultrafast) pattern: push
the model down to a tiny decision head over a reduced observation and keep the
loop deterministic. This is an independent implementation with a different
architecture (cloud decision service + escalation fallback + receipts).

**Which scenarios are covered?**
Search, type, click, submit, streaming waits, and answer extraction are
live-verified; see the graded coverage matrix in
[`docs/COVERAGE.md`](docs/COVERAGE.md). File upload, iframes, and shadow DOM are
out of scope.

**How is this different from Perplexity automation scripts?**
It is a generic fast-loop browser engine with a bundled Perplexity driver
(≤30 lines of site glue), a verified-DONE acceptance gate, and per-step
receipts — not a one-off script.

## Repo layout

```
SKILL.md                 # the skill (npx skills add entry)
scripts/jevw-escaler.py  # fast escalation answerer
src/jev_webbridge/       # generic loop engine (no site code)
src/jev_webbridge/predicates/   # per-site patches (≤30 lines, why_override required)
docs/COVERAGE.md         # capability matrix + naming research
docs/2026-09-24-*.md     # probe & speed reports
bench/*.jsonl            # run receipts (evidence)
```

## License

MIT — see [LICENSE](LICENSE). Trademarks belong to their owners; this project's
use of "Perplexity" is nominative/descriptive only.

---

Keywords: perplexity automation · use perplexity without an api key ·
perplexity web mcp alternative · browser automation agent skill · no api key
