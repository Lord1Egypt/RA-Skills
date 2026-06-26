# 🍽️ opentable

A token-efficient OpenClaw skill for OpenTable restaurant discovery and reservation handoff. Built to be ~14× cheaper than the raw-CDP path most agents fall into on Chrome-automation tasks.

## What it does

- **Entry A — discovery**: *"find me 3 italian places in Tribeca tonight 8pm"* → three restaurants with cuisine, neighborhood, price, review count, and available time slots, in ~17K tokens and ~25 seconds.
- **Entry B — direct book**: *"build me a booking link for Carbone at 8pm"* → one `book.py` call, zero network dependencies, works even when OpenTable is rate-limiting your IP.

The skill never clicks Confirm, never fills forms, never submits reservations. It **stops at the booking deep link** and hands control back to the user, who completes the booking with their own OpenTable account in their own browser. This is a deliberate, hard-coded invariant — no flag toggles it off.

## Why this skill exists

When a naive agent is asked *"find me 3 italian places in Manhattan tonight 8pm"*, its default move is to write a Node.js CDP script to `/tmp/cdp_search.js`, connect to Chrome's DevTools WebSocket on port 18800, scrape the full OpenTable search page, and parse the resulting HTML inside its own context. This pattern:

1. Dumps ~2 KB of page body text into the conversation per retry (OpenTable responses are ~400 KB pre-filter, but agents typically trim to what they can parse).
2. Triggers multi-turn retry loops when the scrape is incomplete or stale.
3. Can accidentally walk the agent through a real booking flow if the user said *"book it for me"* — we've observed agents writing `cdp_click_<restaurant>_8pm.js`, `cdp_select_standard_seating.js`, `cdp_complete_reservation.js` chains and **actually confirming real reservations**.
4. Costs **~242K billed tokens per request** in the worst case observed (7 agent turns, 601K cache read, 1.8K output).

This skill replaces that entire pattern with:

- A single Python primitive (`list_restaurants.py`) that runs one `openclaw browser evaluate` call against OpenTable's own DOM data-test selectors and returns structured JSON (~1 KB).
- A non-mutating booking-link builder (`book.py`) that constructs the OpenTable deep-link URL pattern without ever fetching the page.
- A `SKILL.md` with two entry points, a hard-forbid list, a budget tracker, and troubleshooting for the three real errors we've seen in production.

## Installation

Via ClawHub (once published):
```bash
openclaw skills install opentable
```

Manual install from source:
```bash
git clone <this repo> opentable
mv opentable ~/.openclaw/skills/opentable
openclaw skills info opentable   # should show ✓ Ready
```

Requirements:
- `python3` on PATH (3.8+)
- OpenClaw browser plugin enabled with a working `attached` profile (native Chrome session via `chrome-mcp`)
- `www.opentable.com` on `browser.ssrfPolicy.hostnameAllowlist` (the SKILL.md has a one-line fix command if missing)

## Usage

Just ask your agent for a reservation. Some tested phrasings (all return three options in ~25s):

- *"find me 3 italian places in manhattan for 2 people tonight at 8pm"*
- *"thai restaurants in tribeca tomorrow at 7pm for 3 people"*
- *"book me a chinese place in midtown tonight 8pm for 2"*
- *"reservation for 4 people at a sushi place in midtown manhattan tomorrow at 7:30pm"*

When the user picks a restaurant, the agent calls `book.py` and hands back a deep link:

```
Carbone — Saturday, April 12 at 8:00 PM for 2

Tap to confirm on OpenTable: https://www.opentable.com/booking/details?rid=...

Restaurant page: https://www.opentable.com/r/carbone-new-york
```

The user completes the reservation in OpenTable. The agent stops here — this is intentional and enforced by the SKILL.md.

## Benchmark

> **See also: [BENCHMARK.md](./BENCHMARK.md)** — head-to-head comparison against the two other OpenTable skills on ClawHub (`eeshita-pande/opentable-booking` and `ivangdavila/opentable`), run under identical fresh-session conditions with each competitor isolated. Covers raw per-run data, side-effect audit, architectural comparison, and an honest accounting of the environments each skill is (and isn't) designed for.
>
> Head-to-head summary:
>
> | | `opentable-booking` | `opentable` (ivang) | **this skill** |
> |---|---:|---:|---:|
> | Median billed tokens | 16,361 | 25,113 | **16,879** (normal) / **9,214** (Entry B) |
> | `web_fetch` calls per run | 1–9 | 1–16 | **0** |
> | Third-party data egress (food blogs, search engines) | yes | yes | **no** |
> | Full booking completed in CLI agent env | no (bails 2/3) | no (advisory) | **no (by design, stops at deep link)** |
> | Resilient to OpenTable rate-limit | partial (third-party fallback) | partial | Entry B fully resilient |

Measured by running 11 fresh-session agent turns through the OpenClaw gateway on April 2026 with `openai/gpt-5.4` at `thinking=low`. Each run was a different prompt: diverse cuisines, locations, party sizes, date phrasings, plus four edge cases (missing info, narrow neighborhood, no-results query, HTTP/2 flake) and one direct-book flow.

### Per-run numbers

| Run | Prompt | Latency | Turns | Tokens billed | CDP scripts |
|---|---|---:|---:|---:|---:|
| 1 | italian · manhattan · tonight 8pm · 2 | 28.0s | 3 | 16,879 | 0 |
| 2 | thai · tribeca · tomorrow 7pm · 3 | 26.4s | 3 | 16,971 | 0 |
| 3 | sushi · midtown · tomorrow 6:30pm · 2 *(cache-warm)* | 27.0s | 3 | 4,978 | 0 |
| 4 | french · brooklyn · saturday 8:30pm · 4 *(cache-warm)* | 23.2s | 3 | 4,652 | 0 |
| 5 | mexican · east village · tonight 9pm · 2 | 27.1s | 3 | 16,886 | 0 |
| 6 | edge: missing location + time + party | 12.4s | 2 | 16,215 | 0 |
| 7 | edge: narrow neighborhood (DUMBO) | 24.1s | 3 | 16,876 | 0 |
| 8 | edge: no results + auto-widen | 41.6s | 5 | 18,672 | 0 |
| 9 | edge: late-night (HTTP/2 error) | 23.6s | 5 | 17,259 | 0 |
| 10 | fullflow turn 1 (HTTP/2 error) | 20.5s | 3 | 16,600 | 0 |
| 11 | **Entry B direct book** | **17.3s** | **4** | **17,834** | **0** |

### Aggregate vs. baseline

|  | Baseline *(CDP scripting)* | This skill *(median)* | Improvement |
|---|---:|---:|---:|
| **Tokens billed** per request | 242,227 | **16,879** | **14.4×** fewer |
| Best-case (cache-warm) | — | 4,652 | **52×** fewer |
| **Wall-clock latency** | 78s | **24s** | **3.2×** faster |
| Assistant turns | 7 | 3 | **2.3×** fewer |
| CDP scripts written to `/tmp/` per run | 2–5 | **0** | ∞ |
| HTML body bytes into context | ~2 KB/turn | **0** | ∞ |
| SKILL.md read rate | 0/1 | **11/11** | — |
| Accidental real bookings in test | 1 | **0** | — |

### What the numbers mean

**The 14.4× win is real but needs context.** The skill itself only accounts for ~4–5K marginal tokens per request. The remaining ~12K per cache-cold run is OpenClaw's workspace bootstrap (reading `SOUL.md` / `USER.md` / `memory/*.md` on session start) — that's shared across every skill and unrelated to this one. Cache-warm runs (when the workspace context is cached) show the skill's true floor: **~4.7K tokens per reservation**, roughly **52×** cheaper than the baseline CDP runaway.

**Why the baseline was so bad.** The baseline number (242,227 tokens) came from a real observed failure mode: an agent on `thinking=low` handed *"find me 3 italian places tonight"* decided to write three separate `/tmp/cdp_*.js` scripts, ran them via `exec node`, got partial results, then spent five more turns patching its own scripts while the conversation history grew linearly. At turn 7 it finally returned three restaurants. The cached read alone was 601K tokens — just from re-reading its own prior tool outputs.

**Why 0 CDP scripts is the critical metric.** Token count correlates with agent behavior, but the real regression risk is the agent drifting into `write + exec + node + CDP` patterns. The **0 CDP scripts** result across all 11 runs is the signal that the skill's forbid list is actually being respected. Before the skill, an agent had accumulated 15 `/tmp/cdp_*.js` scripts across a session — one per Chrome automation task. After the skill, the count stays at 0 no matter how many reservations the agent processes.

**Why the edge-case runs matter.** A skill that only handles the happy path is a demo, not a tool. The four edge cases (missing info, narrow neighborhood, no-results, HTTP/2 flake) all resolved without regression:

- **Missing info** → one combined clarification question, no search call. 12.4s, 2 turns. This is the shortest path to *"what are you looking for"*.
- **Narrow neighborhood (DUMBO)** → the primitive correctly returned 3 DUMBO restaurants because OpenTable's search handled the neighborhood fine. The auto-widen fallback is only triggered on empty results.
- **No-results (Ethiopian food on Mars)** → auto-widened once to the nearest city (Pittsburgh), still empty, offered the user alternatives (later time, nearby cities, different cuisine). 41.6s, 5 turns. No retry loop.
- **HTTP/2 protocol error** → OpenTable's Akamai rate-limited our IP after too many navigations. The agent reported the error and asked the user for a URL, instead of writing a CDP script to "try another way". **This is the failure mode that most demo skills regress on** — graceful network degradation without fallback to forbidden patterns.

**The Entry B direct-book win.** The 11th run (added after the first 10 surfaced the missed optimization) tests the direct-book path: *"build me a booking link for Park Rose, 8pm tonight, 2 people, slug park-rose-new-york"*. The agent now calls `book.py` immediately with zero network dependencies — 17.3s, 0 calls to `list_restaurants.py`, works even when OpenTable is returning 500s. This makes the skill **robust to OpenTable outages** for the case where the user already knows what they want.

## Design principles

If you're building similar skills, here's what we learned optimizing this one across three improvement rounds:

1. **Description is the gatekeeper.** OpenClaw's system prompt tells the agent to *"scan `<available_skills>` descriptions; if one clearly applies, read its SKILL.md"*. If your description is passive or buried in context, the agent will skip reading the body and fall back to its default tool habits. Lead with imperative verbs: *"MUST use for..."*.

2. **Frontload SKILL.md.** Agents may lazy-read. The first 500 bytes of your SKILL.md should contain the hard-forbid list and the exact command to run. If the agent stops reading at paragraph 3, it should still have enough to behave correctly.

3. **The primitive's output is part of the skill.** Every field the agent might need in the next turn should be in your primitive's JSON: nav context, current URL, action refs, explicit next-step hints. Anything missing forces a second call, which invites the agent to improvise. This skill's `list_restaurants.py` returns `{nav, restaurants[], next_actions[]}` as a single payload — the `next_actions` array is an in-band reminder to *"NEVER click slots yourself. NEVER write /tmp/cdp_*.js. NEVER web_fetch opentable.com."*

4. **Forbid, don't just recommend.** *"Prefer X"* loses to an agent's trained prior. *"Never Y, every other path is an error"* wins. Make the recommended path the only valid one.

5. **Delete the tempting alternatives.** Pre-existing `/tmp/cdp_*.js` files bias session history. Clean them. The agent's "default move" for Chrome automation on a fresh machine is very different from a machine with 15 stale CDP scripts in `/tmp`.

6. **Test in fresh sessions.** A 266-message session with accumulated CDP-scripting habits will always regress. The only valid test bench is a clean session, run for each prompt.

7. **Two entry points, not one.** Every non-trivial workflow has a *discovery* path and a *direct* path. This skill learned this the hard way when the agent tried to "verify" a user-provided restaurant with `list_restaurants.py` before calling `book.py` — hit OpenTable rate-limiting, refused to produce a link. The fix was adding an explicit Entry B that short-circuits the discovery phase.

## File layout

```
opentable/
├── README.md                   ← this file
├── SKILL.md                    ← the skill contract (agent-facing)
└── scripts/
    ├── list_restaurants.py     ← primitive: navigate + DOM evaluate + filter
    ├── book.py                 ← primitive: deep-link URL builder
    ├── extract_rid.py          ← primitive: URL parser (slug/rid extraction)
    └── search.py               ← primitive: search URL builder (legacy, kept for symmetry)
```

## What this skill does NOT do

- **Complete reservations automatically.** By design. Requires OpenTable auth + card on file; too dangerous under `exec.ask=off`.
- **Modify or cancel existing reservations.** Direct the user to OpenTable.
- **Handle waitlists / notify-me / prepaid experiences.** Out of scope.
- **Search beyond OpenTable.** Resy, Tock, Yelp Reservations are separate systems.
- **Fetch OpenTable pages via `web_fetch`, `curl`, `urllib`, or raw CDP.** Akamai blocks them. The primitive scripts are the only sanctioned path.

## License & Credits

MIT. Built with [OpenClaw](https://github.com/openclaw/openclaw)'s browser plugin — the attached-profile path that bypasses Akamai's bot detection is what makes the single-call primitive possible.

Benchmark methodology and full test transcript available on request.
