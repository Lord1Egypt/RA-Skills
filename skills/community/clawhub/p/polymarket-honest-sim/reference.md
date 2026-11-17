# PaperBook reference — stable concepts

This file carries the parts that don't change: what the honest lenses mean,
how to read the report, and the integration gotchas. For the current wire
contract (endpoints, shapes, limits, paste-ready signing code), always fetch
`https://paperclob.com/llms-full.txt` — if the live server disagrees with
anything written anywhere, the server wins.

## Why "honest" fills

Every conventional paper-trading sim — including the Polymarket paper-traders
already on the agent marketplaces — fills your order at the price you are
looking at. That measures `corr(signal, observed price)`, not edge. Two things
it cannot see:

1. **Latency**: by the time your order arrives, the book has moved. PaperBook's
   sim lands your order at `submit + latency_ms` (default 330 virtual ms, a
   measured real-world figure) and crosses the book **as of arrival**.
2. **Adverse selection / fill self-selection**: the orders that fill easiest
   are the ones informed flow left behind. Graded on real tape, fills
   systematically select toward losers; a "would-have-filled" assumption at
   observed prices systematically selects toward winners.

The house falsified fifteen of its own strategies with this harness before
pointing it at anyone else's — the post-mortems are public at
https://paperclob.com/blog. The recurring pattern: always-positive paper
backtests, ≤ 0 on the fillable lens.

## The report, field by field

`GET /report` (signed) returns, verbatim:

- `realized` — the ledger: `{final_balance, pnl, n_orders, n_fills}`. This is
  what actually happened to the session's paper balance.
- `mode` — `"taker"` in the current phase.
- Three lenses, each `{n, wr, avg_px, edge_real, ci_lo, ci_hi}`:
  - `paper` — graded against the book you saw. Flattering.
  - `honest_persist` — requires the quote to persist. Intermediate.
  - `honest_fillable` — graded at the price you could actually transact.
    **The verdict is decided here and only here.**
- `edge_real = realized win rate − average price paid`, dollar-weighted. In an
  efficient venue the transactable price already contains the signal, so
  `WR ≈ price` and `edge_real ≈ 0`. A high win rate alone is not edge; WR
  above the price paid is.
- `ghost_gap` — how much of the paper edge evaporates under honest grading.
- `verdict`:
  - `real_edge` — fillable `ci_lo > 0` at `n ≥ 40`. Rare by construction.
  - `phantom` — paper looks positive, fillable ≤ 0. Adverse selection ate it.
  - `no_edge` — honest edge ≤ 0 at scale. The market priced the signal.
  - `inconclusive` — fewer than 40 gradeable fills. Not a verdict on the
    strategy; run a longer window or widen coins/durations.
- `regrade` — `"ok"` or the reason the re-grade was skipped (the realized
  ledger and the certificate stand regardless).
- `certificate` — the data-quality disclosure the verdict is founded on:
  `corpus_manifest_version`, `coverage`, `holes_in_window` (tape gaps inside
  your window), `biases_applied` (masked/flagged corpus biases),
  `phantom_rate_final30s_7d` (how often near-close quotes were phantoms).
  Quote it; a verdict without its certificate is marketing.
- `reproducibility_hash` — same window + seed + latency + ordered order
  intents + corpus manifest ⇒ same hash. Two runs that disagree with the same
  hash inputs indicate a bug, not variance.

Only **taker BUYs** are graded (buy NO to express a bearish view — that is the
graded path). A marketable order that finds no liquidity at arrival returns
`status: "unmatched"` — not an error, and the miss still counts as a decision
in the re-grade: you cannot cherry-pick your fills.

## The stepping clock

- A sim session starts **frozen at t0**. Nothing advances until you poll
  `GET /events?after=<last_seq>&wait=1` (signed). Each poll advances the clock
  to the next corpus event(s).
- Every read (`/markets`, `/book`, `/price`) is served at virtual now — the
  server cannot return a row newer than the clock, so **lookahead is
  structurally impossible**, not merely discouraged.
- Event kinds: `slot_open`, `book` (top of book), `slot_close`, `resolution`,
  plus your own `order_ack` / `order_fill` / `order_reject`. Track the max
  `seq` and pass it back as `after`; stop at `"end": true`.
- One clock per session — don't poll `/events` from multiple threads unless
  you intend them all to advance time.
- `POLY_TIMESTAMP` in the HMAC is **real wall time**, not virtual time.

## Gotchas (these cause most 401s and 400s)

1. **The HMAC signs the path WITHOUT the query string.** Sign `/events`, never
   `/events?after=3`. Sign `/orders`, never `/orders?x=1`.
2. **Sim sessions sign the STRIPPED path.** The wire path is
   `/sim/{id}/order`; the signed path is `/order`. The server strips the
   prefix before verifying — this is what makes `py-clob-client` pointed at
   the session `base_url` work unchanged.
3. The signature message is `timestamp + METHOD + path + body` — method
   uppercased, body the **exact bytes sent** (empty string for GET/DELETE),
   secret **base64url-decoded** before use, result base64url-encoded.
4. `POLY_TIMESTAMP` outside ±5 minutes of server time → 401.
5. **Minimum order size is 5 shares** (PM convention). The sim rejects less
   with a 400; the live book currently tolerates smaller but don't rely on it.
   Marketable orders should be ≥ $1. Prices live on a $0.01 grid in (0,1).
6. No shorting: SELL requires held shares (422 otherwise).
7. Rate limits: reads 20/s sustained (burst 40), orders 10/s (burst 20).
   429 responses carry `Retry-After` in seconds — honor it.
8. Sim sessions expire after **30 minutes idle** (any authed call keeps them
   alive) → 404 `"unknown sim session"`. The verdict is retained server-side.
9. `POST /sim` loads a corpus slice and can be slow; occasional proxy 504s are
   retryable. A 422 `"no slots in that window"` means that day/coin combo has
   a tape hole — try another day or widen coins; the certificate of any
   successful session discloses holes inside its window.
10. Credentials (`secret`, `passphrase`) are shown **once** at registration /
    session creation — persist immediately, never print them into logs or
    commit them.

## Honest reporting duty

When you run a strategy through the sim on a user's behalf:

- Lead with the `verdict` and the `honest_fillable` lens, not the PnL.
- If `paper` is positive and `fillable` is not, say "phantom — the paper edge
  is adverse selection", not "mixed results".
- `inconclusive` means insufficient n. Say that. Do not extrapolate.
- Include the `reproducibility_hash` so the result can be re-derived.
- A `real_edge` verdict is a reason to test more (longer windows, other
  regimes, live paper canary), never a reason to claim live profitability:
  a green verdict is necessary, not sufficient, for real edge.
