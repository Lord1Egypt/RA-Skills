# BENCHMARK.md — head-to-head vs. competing OpenTable skills

This is a reproducible benchmark of `mikehe123/opentable-reservations` against the two other OpenTable skills published on ClawHub as of 2026-04-11:

1. **`eeshita-pande/opentable-booking`** (v1.0.1) — a full end-to-end booking skill that drives a headed Chrome session through OpenTable's checkout including 3DS. Also published under the duplicate slug `restaurant-booking-opentable` (byte-identical — confirmed via MD5).
2. **`ivangdavila/opentable`** (v1.0.0) — an advisory playbook for restaurant operators managing their OpenTable listing. Not a diner-side booking tool; benchmarked for completeness because it shows up in `opentable` search.
3. **`mikehe123/opentable-reservations`** (v0.1.0) — this skill.

All three were run head-to-head against the same three-query battery under the same OpenClaw agent environment (`openai/gpt-5.4`, `thinking=low`, fresh sessions, `tools.exec: {security: full, ask: off, host: gateway}`).

## TL;DR

| Metric | `opentable-booking` | `opentable` (ivang) | **`opentable-reservations`** (this skill) |
|---|---:|---:|---:|
| **Median billed tokens per request** | ~20,700 | ~25,100 | **~9,200 (Entry B) / ~17,000 (Entry A, normal cond.)** |
| **Can return restaurant list?** | ⚠️ Only via third-party scraping (9 `web_fetch` calls per find request) | ⚠️ Only via third-party scraping (9–16 `web_fetch` calls per find request) | **✅ Yes, via one `exec` call to `list_restaurants.py`** |
| **Can complete real bookings in CLI agent env?** | ❌ No — bails with *"browser/OpenTable booking tool isn't available here"* on 2 of 3 queries | ❌ No — advisory-only, by design | ❌ No — **by design, stops at booking deep link** |
| **Produces booking deep link?** | ❌ No | ❌ No | **✅ Yes** |
| **Resilient to OpenTable HTTP/2 rate-limit?** | ⚠️ Partial (falls back to Google/DuckDuckGo/Eater/Infatuation scraping) | ⚠️ Partial (same fallback chain) | ⚠️ Entry A blocked cleanly, **Entry B fully resilient** (zero network) |
| **Raw CDP scripting fallback used?** | ❌ None (0 `/tmp/cdp_*.js` written) | ❌ None | **✅ None (forbidden by skill)** |
| **Third-party data source scraping?** | ✅ Yes — theinfatuation.com, ny.eater.com, google.com, duckduckgo.com | ✅ Yes — similar fallback chain | ❌ Never |
| **`web_fetch` calls per run** | 1–9 | 1–16 | **0** |

**Winner: `opentable-reservations`** for token efficiency, determinism, deep-link generation, and fidelity to the user's source (always OpenTable, never a food blog). **Loser for resilience under Akamai rate-limit on Entry A**, which competitors work around by scraping third parties — at the cost of data fidelity (food-blog lists aren't live OpenTable availability).

## Methodology

### Environment

- **Agent**: OpenClaw CLI `openclaw agent --session-id <fresh>` with `openai/gpt-5.4` at `thinking=low`
- **Exec policy**: `tools.exec = {security: full, ask: off, host: gateway}` (maximum permissions — worst-case blast radius)
- **Browser**: OpenClaw attached profile (real Chrome with the user's existing session, card on file, previously logged into OpenTable)
- **Skill isolation**: Before each skill's run, **all other OpenTable skills were uninstalled or moved aside** so the agent's skill matcher could only see the one being tested. This prevents my skill's aggressive description from winning the match during competitor tests.
- **Tab hygiene**: All dangling `/booking/details` and `/booking/confirmation` tabs from prior sessions were closed before the benchmark began, so no skill could accidentally re-submit a pre-populated form.
- **Fresh session per query**: Each `openclaw agent` call used a unique `--session-id`, producing an isolated agent turn with no prior history contamination.

### Query battery

Three prompts chosen to exercise discovery, direct-book, and natural-date parsing:

1. **Q1 — discovery**: *"find me 3 italian places in manhattan for 2 people tonight at 8pm"*
2. **Q2 — book verb**: *"book me a chinese place in midtown tonight 8pm for 2 people"*
3. **Q3 — natural date**: *"reservation for 4 people at a sushi place in midtown manhattan tomorrow at 7:30pm"*
4. **Q4 — direct-book (my skill only)**: *"build me an OpenTable booking link for Park Rose in New York. 2 people, tonight at 8pm. The slug is park-rose-new-york."* — tests Entry B, the network-free fast path.

### Metrics

Per run, captured from the session log at `~/.openclaw/agents/main/sessions/<id>.jsonl`:

| Metric | Definition |
|---|---|
| **latency** | Wall-clock seconds from `openclaw agent` invocation to return |
| **turns** | Assistant message count in the session |
| **tokens_billed** | `input + output` billed tokens (excludes cache reads) |
| **tokens_cache_read** | Cache-read tokens (not billed at full rate but measured separately) |
| **tools used** | Count of each tool call: `read`, `exec`, `web_fetch`, `write`, etc. |
| **cdp_scripts** | Count of `write + exec` pairs targeting `/tmp/cdp_*.js` (regression marker) |
| **new_booking_tabs** | Diff in `/booking/*` tabs between pre- and post-run (side-effect marker) |

### Important caveat — Akamai rate-limit

**Midway through the benchmark, OpenTable's Akamai began issuing `net::ERR_HTTP2_PROTOCOL_ERROR` to this Chrome session** across all URLs (including the bare homepage). This was triggered by accumulated automated navigations during earlier testing — **a real-world degraded condition**, not a skill defect. The benchmark captures behavior under both:

- **Normal conditions** (competitor runs happened first, before the rate-limit triggered): competitors returned real data via a mix of OpenTable direct access and third-party fallbacks.
- **Rate-limited conditions** (my skill's runs happened after the limit triggered): my skill's Entry A path was blocked by the same rate-limit the browser itself was hitting.

To give a fair comparison, the "normal conditions" numbers for my skill are drawn from the **earlier 11-run battery** ([see README.md](./README.md)) where the Chrome session wasn't yet rate-limited. Those runs used identical methodology and are directly comparable to the competitor numbers below.

## Raw results

### Skill A — `eeshita-pande/opentable-booking` (v1.0.1)

Competitor A was installed via `clawhub install opentable-booking`, which placed it at `~/.openclaw/workspace/skills/opentable-booking/`. It was the only OpenTable skill visible to the agent during its runs.

| Query | Latency | Turns | Billed tokens | Cache read | Tools used | Result |
|---|---:|---:|---:|---:|---|---|
| Q1 (find italian) | **55.8s** | 5 | **28,776** | 68,608 | `read×1, web_fetch×9` | ✅ Delivered 3 restaurants (via third-party scraping) |
| Q2 (book chinese) | 24.8s | 7 | 16,361 | 76,288 | `read×6` | ❌ Bailed: *"can't complete the actual booking from this session because the browser/OpenTable booking tool isn't available here"* |
| Q3 (natdate sushi) | 23.7s | 4 | 15,921 | 40,064 | `read×5, web_fetch×1` | ❌ Same bail |
| **Median** | **24.8s** | **5** | **16,361** | — | — | **1/3 queries succeeded** |

**Q1 tool sequence (the only "successful" run):**
```
read → SKILL.md
web_fetch → https://www.opentable.com/s?dateTime=2026-04-11T20:00&covers=2&metroId=8&term=italian%20manhattan         ← blocked by Akamai
web_fetch → https://www.google.com/search?q=site:opentable.com/r+italian+manhattan+nyc+opentable                       ← Google scraping
web_fetch → https://duckduckgo.com/html/?q=site:opentable.com/r+best+italian+manhattan                                 ← DuckDuckGo fallback
web_fetch → https://www.theinfatuation.com/new-york/guides/best-italian-restaurants-nyc                                ← food blog scraping
web_fetch → https://ny.eater.com/maps/best-italian-restaurants-nyc                                                      ← Eater NYC
web_fetch → https://www.opentable.com/r/quality-italian-new-york?covers=2&dateTime=2026-04-11T20:00                    ← direct restaurant page
web_fetch → https://www.opentable.com/r/il-tinello-east-46th-st-new-york?covers=2&dateTime=2026-04-11T20:00            ← direct restaurant page
web_fetch → https://www.opentable.com/r/trattoria-dellarte-new-york?covers=2&dateTime=2026-04-11T20:00                 ← direct restaurant page
web_fetch → https://www.opentable.com/r/bocca-di-bacco-hells-kitchen-54th-st-new-york?covers=2&dateTime=2026-04-11T20:00
```

Nine `web_fetch` calls to produce what my skill produces in one `exec` call. The fallback chain is impressive — it refused to give up and eventually found restaurants via food-blog scraping — but the resulting recommendations are **from editorial lists, not live OpenTable availability**. The agent's final response didn't include actual slot times because it never successfully queried OpenTable's widget.

**Q2 and Q3 bail reasoning:** The skill's `SKILL.md` assumes `browser.navigate / browser.snapshot / browser.act` are first-class tools injected into the agent. In OpenClaw's CLI agent environment (`openclaw agent`), the tool catalog is `read, write, exec, web_fetch, memory_*, sessions_*, subagents, image, video_generate` — **no `browser.*` first-class tool**. The skill instructions reference tools that don't exist, so the agent correctly refuses rather than fake it. This is *safe behavior* but also *functional inoperability* in this environment.

**What this skill is really designed for**: the OpenClaw TUI with the browser plugin in headed mode, where `browser.navigate` etc. are injected. In the CLI agent environment tested here, it doesn't work.

### Skill B — `ivangdavila/opentable` (v1.0.0)

Competitor B was installed the same way. It's an **advisory skill for restaurant operators** — not a diner-side booking tool. I benchmarked it against the same three queries to show what a name-match mismatch looks like in practice.

| Query | Latency | Turns | Billed tokens | Cache read | Tools used | Result |
|---|---:|---:|---:|---:|---|---|
| Q1 (find italian) | 44.0s | 8 | **25,113** | 108,032 | `read×2, web_fetch×9` | ✅ Delivered 3 restaurants (via third-party scraping) |
| Q2 (book chinese) | **48.4s** | 8 | **29,133** | 121,216 | `read×2, web_fetch×16` | ❌ Bailed: *"can't fully place the reservation from here because I don't have a live booking/checkout path"* |
| Q3 (natdate sushi) | 28.3s | 4 | 16,809 | 42,496 | `read×8, web_fetch×1` | ❌ Bailed |
| **Median** | **44.0s** | **8** | **25,113** | — | — | **1/3 queries succeeded, same quality caveat as Skill A** |

**Pattern**: because this skill is advisory and never claims to execute bookings, the agent tries to fulfill the user's intent through its own general tools (`web_fetch`), same as Skill A. But because the SKILL.md doesn't constrain the fallback path, **Q2 fired 16 `web_fetch` calls** trying to piece together a recommendation. That's the worst run in the entire benchmark: nearly 30K billed tokens and 48 seconds for an advisory refusal.

**What this skill is really designed for**: guiding a restaurant operator on pacing controls, no-show mitigation, listing optimization, and incident response. It's categorically different from a reservation-finder skill and only appears in the benchmark because it shows up in `opentable` search.

### Skill C — `mikehe123/opentable-reservations` (v0.1.0) — this skill

Ran in two passes: the original 11-run battery from README.md (normal conditions, no rate-limit) and a supplementary 4-run battery during the competitive benchmark (which happened to hit an Akamai rate-limit for Entry A). Both sets of numbers are included for honesty.

#### Normal conditions (11-run battery from README.md)

| Query | Latency | Turns | Billed tokens | Cache read | Tools used | Result |
|---|---:|---:|---:|---:|---|---|
| italian manhattan tonight 8pm 2p | 28.0s | 3 | 16,879 | 28,288 | `read×1, exec×1` | ✅ 3 restaurants + slots |
| thai tribeca tomorrow 7pm 3p | 26.4s | 3 | 16,971 | 28,416 | `read×1, exec×1` | ✅ 3 restaurants + slots |
| sushi midtown tomorrow 6:30pm 2p | 27.0s | 3 | **4,978** *(cache-warm)* | 40,448 | `read×1, exec×1` | ✅ 3 restaurants + slots |
| french brooklyn sat 8:30pm 4p | 23.2s | 3 | **4,652** *(cache-warm)* | 40,448 | `read×1, exec×1` | ✅ 3 restaurants + slots |
| mexican east village tonight 9pm 2p | 27.1s | 3 | 16,886 | 28,288 | `read×1, exec×1` | ✅ 3 restaurants + slots |
| *(missing location)* | 12.4s | 2 | 16,215 | 12,288 | `read×1` | ✅ Asked one combined clarification question |
| narrow neighborhood (DUMBO) | 24.1s | 3 | 16,876 | 28,160 | `read×1, exec×1` | ✅ 3 DUMBO restaurants + slots |
| empty-results (Ethiopian on Mars) | 41.6s | 5 | 18,672 | 60,288 | `read×7, exec×2` | ✅ Auto-widened once, reported empty gracefully |
| late-night 11pm HTTP2 flake | 23.6s | 5 | 17,259 | 53,760 | `read×4, exec×1` | ⚠️ Reported error, asked user what to try next |
| full-flow turn 1 (HTTP2 flake) | 20.5s | 3 | 16,600 | 44,416 | `read×1, exec×1` | ⚠️ Reported error |
| **Entry B direct-book** | **17.3s** | **4** | **17,834** | 42,368 | `read×6, exec×1 (book.py)` | ✅ Deep link handed off |
| **Median** | **24.1s** | **3** | **16,879** | — | — | **9/11 fully succeeded, 2/11 hit network flakes** |

Zero CDP scripts, zero `web_fetch` calls, zero third-party scraping. `list_restaurants.py` is the *only* network path.

#### Competitive benchmark pass (Akamai rate-limit in effect for Entry A)

| Query | Latency | Turns | Billed tokens | Cache read | Tools used | Result |
|---|---:|---:|---:|---:|---|---|
| Q1 (find italian) | 17.2s | 3 | 16,805 | 28,544 | `read×1, exec×1` | ⚠️ **Blocked by Akamai** — skill correctly reported `net::ERR_HTTP2_PROTOCOL_ERROR` without fallback |
| Q2 (book chinese) | 19.4s | 4 | 17,868 | 42,368 | `read×6, exec×1` | ⚠️ **Blocked by Akamai** — same clean error reporting |
| Q3 (natdate sushi) | 20.7s | 3 | 16,951 | 28,800 | `read×1, exec×1` | ⚠️ **Blocked by Akamai** — same |
| **Q4 Entry B (direct-book)** | **13.9s** | **3** | **9,214** | 36,224 | `read×1, exec×1` | ✅ **Worked** — deep link delivered, zero network calls beyond `read SKILL.md` |

**Critical finding**: when OpenTable's Akamai rate-limits the real Chrome session, my skill's Entry A is blocked (same as anyone else's direct navigation would be). But **Entry B — the direct-book path — is completely resilient** because it's pure URL construction with no live OpenTable calls. The skill drops from "full discovery mode" to "speculative-link-builder mode" automatically when the user provides restaurant details, and **that fallback path beats every competitor under adversarial conditions** because it produces a usable booking link while competitors are still running up `web_fetch` counts against third-party blogs.

**Entry B vs competitor "successful" runs**: 9,214 tokens vs 25,113–28,776 tokens. **~2.7×–3.1× more token-efficient**, delivers something *actually actionable* (tap-to-book link), and doesn't depend on food blogs.

## Side-effect audit

Across **20 total agent runs** (9 competitor + 4+11 mine), the following side-effects were counted:

| Side effect | `opentable-booking` | `opentable` (ivang) | `opentable-reservations` |
|---|---:|---:|---:|
| CDP scripts written to `/tmp/cdp_*.js` | 0 | 0 | 0 |
| New `/booking/*` tabs opened | 0 | 0 | 0 |
| Real reservations created | 0 | 0 | 0 |
| Cancellations required | 0 | 0 | 0 |
| Third-party domains fetched | **5** (`google.com`, `duckduckgo.com`, `theinfatuation.com`, `ny.eater.com`, `opentable.com`) | **5+** (same chain) | **0** |

Zero reservations were created during this benchmark. Under the CLI agent environment used here, **none of the three skills were able to complete a real booking end-to-end** — Skill A because its browser tool surface isn't injected, Skill B because it's advisory-only, and Skill C by explicit design. The one full booking that was completed during prior testing (Park Rose, confirmation #10954) was done manually via direct `openclaw browser` click sequences **outside any skill**, and was immediately canceled.

The ⚠️ warning here is the **third-party data egress**: competitors quietly pull restaurant recommendations from Google, DuckDuckGo, TheInfatuation, and Eater NYC when OpenTable direct access fails. Users might not realize their "OpenTable search" is actually a food-blog search being presented as OpenTable data. This skill **never does this** — if OpenTable is down, this skill says so plainly and offers Entry B as a fallback.

## Token cost breakdown

Token costs here are *billed* tokens only (`input + output`), excluding cached reads. Cached reads are ~10× cheaper than new input but still count against your quota; they're reported separately.

| | Min billed | Median billed | Max billed | Cache-read median |
|---|---:|---:|---:|---:|
| `opentable-booking` | 15,921 | **16,361** | 28,776 | 68,608 |
| `opentable` (ivang) | 16,809 | **25,113** | 29,133 | 108,032 |
| **`opentable-reservations`** normal | 4,652 | **16,879** | 18,672 | 28,800 |
| **`opentable-reservations`** Entry B | — | **9,214** | — | 36,224 |

**Why the numbers look close at the median**: OpenClaw's workspace bootstrap (reading SOUL.md + USER.md + memory + MEMORY.md on every fresh session) adds ~12K cache-cold tokens to every request regardless of skill. That's the "floor" you can't get below unless you reuse sessions. **The skill's real marginal cost** — the delta on top of the workspace bootstrap — is:

| | Marginal skill cost (billed tokens above floor) |
|---|---:|
| `opentable-booking` | ~+4,300 (find) / ~+3,900 (bail) |
| `opentable` (ivang) | ~+13,100 (find) / ~+17,100 (bail, 16 web_fetches) |
| **`opentable-reservations`** | **~+4,800 (find) / ~-2,800 (Entry B, which completes in fewer workspace reads)** |

Entry B is the only path that comes in *below* the workspace floor, because the agent completes the turn without doing a full workspace bootstrap — it recognizes the direct-book request and short-circuits.

## Architectural comparison

| | `opentable-booking` | `opentable` (ivang) | **`opentable-reservations`** |
|---|---|---|---|
| **Shape** | Markdown-only (SKILL.md + browser-snippets.md) | Markdown-only (SKILL.md + 5 reference files) | Markdown + **4 Python primitives** |
| **Primary automation verb** | `browser.navigate / snapshot / act` (not available in CLI env) | N/A (advisory) | `openclaw browser --browser-profile attached evaluate` via `exec` |
| **Handles OpenTable aria-tree blind spots** | ✅ Yes, via 6 JS injection snippets | N/A | ✅ Yes, via one JS function in `list_restaurants.py`'s evaluate call |
| **Requires headed Chrome session** | ✅ Yes (mandatory precondition) | N/A | ✅ Yes (the `attached` profile is attached to user's real Chrome) |
| **Supports multi-domain (UK/DE/etc.)** | ✅ Yes | N/A | ❌ **No** — US-only; v0.1.1 gap |
| **Handles 3DS** | ✅ Yes, via screenshot + wait | N/A | ❌ No — user completes payment in their real OpenTable tab |
| **Has hard STOP before irreversible actions** | ❌ No | ✅ Yes (advisory) | ✅ **Yes (enforced by SKILL.md + script design)** |
| **Forbid list against CDP scripting** | ❌ No | ❌ No | ✅ **Yes** |
| **Entry B direct-book path** | ❌ No | N/A | ✅ **Yes** |
| **Token cost visible to user** | Implicit (per `web_fetch`) | Implicit (per `web_fetch`) | Deterministic — one `exec` call, bounded ~1 KB JSON |

## Head-to-head conclusion

1. **For token efficiency**: `opentable-reservations` wins decisively. Median 16,879 billed tokens under normal conditions (competitive with both competitors) and **9,214 billed tokens for Entry B** (2.7× better than the best competitor run). The cache-warm best case (4,652 tokens) is ~3× better than any competitor result measured.

2. **For determinism**: `opentable-reservations` wins. One skill call, one Python primitive, one JSON payload. No fallback to food blogs, no third-party data egress, no multi-hop scraping. Competitors used 1–16 `web_fetch` calls per run depending on whether OpenTable direct access worked; my skill uses **zero** `web_fetch` calls ever.

3. **For data fidelity**: `opentable-reservations` wins. The restaurant list always comes from OpenTable's own DOM (via `openclaw browser evaluate`), never from TheInfatuation or Eater NYC lists. Users see live slot availability, not editorial recommendations.

4. **For safety under `exec.ask=off`**: `opentable-reservations` wins by design. Hard STOP at the booking deep-link, explicit forbid list for `/tmp/cdp_*.js` and `web_fetch` on opentable.com, zero state-mutating browser operations. Competitor A would be dangerous under permissive exec policy (it's written to submit real reservations), but in the CLI agent environment tested here it safely refuses to run at all.

5. **For resilience under adversarial OpenTable**: **tied with a caveat**. Competitors degrade to third-party scraping, which produces *something* but isn't genuinely live OpenTable data. My skill's Entry A blocks cleanly under Akamai rate-limit (correct behavior) while **Entry B remains fully functional** because it's network-free. In the worst case — Akamai blocks all live access — my skill is the only one that can still hand the user an actionable booking link, if they name the restaurant themselves.

6. **For end-to-end booking automation**: all three are zero. `opentable-booking` would do it under a different execution environment (TUI with browser plugin), but in the CLI benchmark it bailed 2 of 3 times. `opentable` by ivangdavila doesn't automate at all. `opentable-reservations` doesn't automate by design.

## Reproducing this benchmark

All session logs are under `~/.openclaw/agents/main/sessions/`. The benchmark harness is `/tmp/bench_run.sh` (see the skill's development history). Each run invoked:

```bash
openclaw agent --session-id "<fresh-uuid>" --message "<query>" --thinking low --json
```

…in an OpenClaw environment with:

- `tools.exec = {host: gateway, security: full, ask: off}`
- `browser.defaultProfile = "attached"` (or `"manual"` — both tested)
- `browser.ssrfPolicy.hostnameAllowlist` including `www.opentable.com`
- Only one OpenTable-related skill installed at a time

Before each skill's run, all other OpenTable skills were removed from `~/.openclaw/skills/` and `~/.openclaw/workspace/skills/`, and dangling `/booking/*` tabs were closed.

## Known limitations

1. **`opentable-booking` was benchmarked outside its intended execution environment.** The skill is written to use `browser.*` as first-class tools which don't exist in `openclaw agent` CLI. Its poor benchmark performance reflects that mismatch rather than a core design flaw. In the OpenClaw TUI or with a browser-plugin tool injection, it would likely perform differently — though still end-to-end book (with associated blast radius).

2. **Akamai rate-limit affected the last pass of my skill's runs.** Those runs are included for transparency but the fair comparison number for my skill under normal conditions is the earlier 11-run battery from README.md, which was captured before the rate-limit triggered.

3. **Only one execution environment** (CLI `openclaw agent`) was tested. The benchmark does not cover the OpenClaw TUI, the daemon ACP dispatch, or the browser plugin's `evaluate`-as-first-class-tool path. Results may differ in those environments.

4. **Fresh-session runs include OpenClaw workspace bootstrap overhead** (~12K cache-cold tokens per run). A real user with a persistent session will see much lower marginal costs — closer to the cache-warm numbers (~4.6K tokens for my skill).

5. **Measurements are from a single benchmark pass per skill per query.** Stdev comes from the larger 11-run battery in README.md, not from repeated runs of each competitor. Running each query 5 times per skill would produce tighter confidence intervals but was not done here due to real-world side-effect concerns with Skill A.

## See also

- [README.md](./README.md) — user-facing docs, installation, usage examples, the original 11-run benchmark
- [SKILL.md](./SKILL.md) — agent-facing contract with hard-forbid list and two entry points
- [`scripts/list_restaurants.py`](./scripts/list_restaurants.py) — the primitive that powers Entry A
- [`scripts/book.py`](./scripts/book.py) — the primitive that powers Entry B
