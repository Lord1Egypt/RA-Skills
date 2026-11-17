# Changelog

All notable changes to this skill. Format based on
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic
versioning.

## [2.2.1] — 2026-09-19

### Fixed

- **Display name restored to "Polymarket Agent".** The 2.2.0 publish ran from
  a working directory named `work` without `--name`, so the registry took the
  folder name and the listing read "Work". No content change; versions are
  immutable, so correcting it needed a patch release.

## [2.2.0] — 2026-09-18

Self-review after the 2.1.3 publish, looking specifically for controls that
exist but can be reached around. Both findings are of that shape: the guard
was real, and a sibling code path walked past it. Minor, not patch, because
one key that used to be writable no longer is.

### Fixed

- **Autonomy is now gated on the field, not on one command.** `poly auto`
  required an explicit acknowledgement flag, clamped the validity window to
  24h and journalled the decision — and the same two settings were reachable
  through the generic `poly config` setter, which walked past all three. They
  now live in `config.LOCKED_KEYS`: still readable and still listed, writable
  only through `poly auto`. This is the gap ClawHub's own scan described as
  the implementation not fully enforcing the documented acknowledgement and
  expiry boundary. Regression test:
  `tests/test_guardrails.py::AutonomyConfigBypassTest`.

- **Text from the Polymarket API is neutralised at the parse boundary.**
  Market titles, outcome names and trader nicknames are written by other
  users, and reach three places that read text as instructions: the terminal,
  the `openclaw cron` alert and the agent's context. `cli.safe()` covered
  terminal markup only, which is a rendering concern. New `http.clean_text`
  strips control characters and line breaks and caps length in
  `parse_trade`/`parse_market`, so no consumer has to remember to. It is not
  a detector — wording gets around those; it removes the structure needed to
  impersonate the frame around the text. The defence that actually holds is
  unchanged: the money path is deterministic.

- **Event links can no longer be forged.** `WhaleTrade.url` pasted the API's
  slug straight into a polymarket.com address, so a crafted slug produced a
  link that reads as polymarket.com and resolves elsewhere — on a phone
  notification the prefix is all that is visible. `http.clean_slug` restricts
  it to RFC 3986's unreserved set. Regression tests:
  `tests/test_whales.py::UntrustedApiTextTest`.

Full technical detail for each item, including the exact pre-fix behaviour,
is in the commit history rather than here.

## [2.1.2] — 2026-07-20

Response to ClawHub's SkillSpector scan on the 2.1.0/2.1.1 publish. Full
report: `clawhub scan --slug polymarket-agent --version <n>`. The scan is
async and multi-stage, so fixing one round's findings surfaced a new one on
the next pass — see the two sub-entries below.

### Fixed (round 2, after the fix below was scanned)

- **`POLYMARKET_KEY` no longer takes silent precedence over the keystore**
  (SkillSpector finding E2, High severity, 0.93 confidence — this pushed the
  score from 49 to 59 and the recommendation to `DO_NOT_INSTALL` on the
  interim scan). The legacy env var was checked BEFORE the encrypted
  keystore and activated on its mere presence, silently at the point
  of use — so a leftover `POLYMARKET_KEY` from testing could silently
  override a properly configured keystore, and env vars are readable by
  child processes, `/proc/<pid>/environ`, crash dumps and CI logs. Fixed in
  `keystore.load_key`: the keystore is now tried first; the env var is a
  gated fallback requiring the NEW `POLYMARKET_ALLOW_ENV_KEY=1` (declared in
  `SKILL.md`'s `envVars`), and prints a stderr warning every time it is
  actually used, not just in `poly doctor`.

### Fixed (round 1)

- **`requests` floor raised to 2.33.0** (from 2.32.4). SkillSpector caught
  CVE-2026-25645 (insecure temp-file reuse in `extract_zipped_paths()`), an
  advisory published after the 2.32.4 floor had already been set — dependency
  pins need periodic re-checking against new advisories, not a one-time floor.
- **Trigger table split and tightened** (SkillSpector finding SQP-1). Broad,
  single-domain phrases like "what's trending" or "stop everything" could
  activate a wallet-holding skill outside a Polymarket context. Triggers are
  now split into a research tier (loose phrasing is fine, nothing at risk) and
  a wallet/trading/scheduling tier that requires the phrase to name Polymarket
  and the specific action, never inferred from a bare verb.

### Reviewed and kept as-is

- **Autonomous mode** (SkillSpector findings EA2 × 3, the scan's strongest
  recommendation was to remove it). Decision: keep it. It already requires an
  explicit `--i-understand-the-risk` flag, expires within 24h, stays bound by
  every financial cap, and is overridden by the kill switch — and ClawScan's
  holistic review independently rated the disclosure `benign`/high-confidence.
  Autonomous mode was carried over from 1.0.2's feature set rather than
  requested for this rewrite; removing it remains an option if a future scan
  or user report changes the calculus.
- **LP3 (declare permissions in metadata)** — `metadata.openclaw.permissions`
  is not a field in the ClawHub skill schema (confirmed against the official
  docs; see SECURITY.md's "Metadata coherence" section). There is currently no
  schema-level way to declare network/filesystem capability beyond
  `requires`/`envVars`, which are already fully declared.

## [2.1.1] — 2026-07-20

### Fixed

- Restored `skill-card.md`. 2.1.0 removed it on the assumption that ClawHub
  always generates the card server-side from `SKILL.md`; in practice the
  registry's card endpoint returned `card.missing` without a file present in
  the artifact. Updated its content to match 2.1.0's whale-tracking and
  smart-money features.

## [2.1.0] — 2026-07-20

Whale tracking and smart-money research, plus five accounting bugs found while
reviewing 2.0.0 — the guard-rails were correct, but they were being fed wrong
numbers, which is equally dangerous.

### Added

- **`poly whales`** — recent large trades. The size filter is applied
  **server-side** (`filterType=CASH`), so long windows stay cheap instead of
  paginating thousands of small trades to discard them client-side.
- **`poly leaderboard`** — most profitable traders by category and period, via
  `/v1/leaderboard`. The starting point for smart-money research.
- **`poly trader <address>`** — any wallet's bankroll, open positions and
  recent trades. All public data.
- **`poly holders <conditionId>`** — largest holders of each outcome.
- **`poly quote <id|slug>`** — spread and top of book, read straight from Gamma
  (no extra CLOB round-trip needed just to see whether you can get in and out).
- **`--alert` mode with deduplication** — returns only unseen trades and prints
  `NO_REPLY` when there is nothing, which OpenClaw's cron suppresses. Without
  this, a 15-minute alert becomes noise and the user turns it off.
  `--preview` inspects without consuming the dedup state;
  `poly alerts-reset` clears it.
- **Shared HTTP layer** with exponential backoff and jitter, honouring
  `Retry-After`. It deliberately does **not** retry 4xx — repeating a 400 only
  burns rate-limit quota. Matters because Polymarket's Cloudflare *delays*
  rather than rejects over-limit requests, so a naive client degrades silently
  (`/trades` allows 200 req/10s).
- `CHANGELOG.md`.

### Fixed

- **Open-order counter grew forever (P0).** The journal never learned that an
  order had filled or been cancelled elsewhere, so after ten orders in the
  skill's lifetime `max_open_orders` blocked **all trading permanently**, with
  no obvious way out. The exchange is now the source of truth
  (`reconcile_open_orders`); the offline fallback ignores entries older than
  seven days.
- **Journal rotation reset the daily budget.** Crossing 5 MB rotated the file
  and `spend_since()` only read the current one, releasing the entire daily
  cap. A maintenance event must not free up budget. Rotation-aware now.
- **Cancelling did not close the order.** `cancel_order` wrote a *new* journal
  line; the original stayed `submitted` forever and kept counting against the
  open-order cap. `close_by_order_id` now closes the original entry.
- **Status updates distorted the 24h window.** `update_status` rewrote the
  timestamp, so a two-day-old order updated today counted against today's
  spend. `first_ts` preserves the original instant.
- **Race between concurrent processes.** Two simultaneous `poly buy` runs read
  the same accumulated spend and both passed, jointly breaching the daily cap
  without either violating the rule alone. The evaluate-and-send critical
  section is now guarded by an inter-process `flock` (released by the kernel on
  process death, so it cannot wedge).
- **Manifest declared a field that does not exist.** 2.0.0 used
  `metadata.openclaw.permissions`, which is not in the ClawHub schema, and
  `install.kind: script`, which is not a supported kind (only `brew`, `node`,
  `go`, `uv`). Both removed. The three environment variables the code reads are
  now declared under `envVars` to avoid a metadata-mismatch flag from the
  security scanner.

### Changed

- `markets.py` moved onto the shared HTTP layer, gaining retry/backoff and
  dropping duplicated session code.
- `redact()` no longer reveals the last four characters of a secret. Showing a
  suffix is a credit-card habit that makes no sense for a private key — it
  shrinks the search space for anyone reading a terminal or log without
  offering anything in return. `short_address()` handles the legitimate
  "which wallet is this?" case, on the **public** address.
- `skill-card.md` removed — ClawHub generates it server-side from `SKILL.md`.

## [2.0.0] — 2026-07-20

Complete security rewrite addressing all 28 findings from the ClawHub audit of
1.0.2. See [SECURITY.md](SECURITY.md) for the finding-by-finding mapping.

### Security

- **Private key never passes through argv.** 1.0.2 claimed the key "never
  leaves your machine" while passing it as a **command-line argument** to
  `clawdbot config set`, exposing it via `ps aux`, `/proc/<pid>/cmdline`, shell
  history and parent-process logs. It is now read with `getpass` (no echo),
  encrypted with scrypt+AES (`eth_account`, standard V3 keystore) and written
  0600 via `os.open` — no window in which the file exists with loose
  permissions. `LoadedKey.__repr__`/`__str__` are overridden so the key cannot
  leak into a traceback.
- **No external process is spawned.** 1.0.2 spawned six, one of them through a
  shell. Dependency
  checks now use `importlib.util.find_spec` in-process; configuration is local
  JSON read with the stdlib.
- **Output injection closed.** All externally-sourced text is markup-escaped
  before terminal rendering, so a `[/]` in a market title cannot forge output.
- **`requests` pinned to >= 2.32.4** (CVE-2024-35195, CVE-2024-47081), and all
  sessions set `trust_env=False` so the host's credentials file and proxy
  settings cannot inject credentials — closing the CVE-2024-47081 vector by
  construction.
- **`web3` removed entirely.** It carried CVE-2026-40072 (SSRF via CCIP Read)
  and no line of code used it. `questionary` dropped too (stdlib `getpass`
  instead), and `typer[all]` narrowed to `typer`.
- **All dependencies pinned** with documented security floors.
- **No host configuration access.** The skill no longer reads or writes
  OpenClaw config; only a closed set of validated keys within bounded ranges.

### Added

- **Financial guard-rails** enforced in code, independent of model output:
  per-order notional cap, bankroll percentage, rolling 24h spend, open-order
  cap, price range.
- **Kill switch** (`poly halt`) — a file-based stop that overrides everything,
  including autonomous mode. Works even with the process dead and can be
  created by hand.
- **Append-only audit journal** (`poly history`) recording every attempt.
  Intent is written *before* sending, so a mid-flight crash still counts the
  spend (fails safe).
- **Dry-run enabled by default.**
- **Time-boxed autonomous mode** — requires `--i-understand-the-risk`, expires
  within 24h, stays subject to every cap. A hand-edited config claiming
  `autonomous_mode: true` with no expiry is treated as **off**.
- Explicit financial-risk warnings at setup and before every order.

### Fixed

- **Market search returned nothing.** 1.0.2 fetched the top `limit` markets by
  volume and only *then* filtered by text, so searching "bitcoin" with
  `limit=10` only worked if a bitcoin market happened to be in the top ten that
  second. Now uses the server search endpoint with real pagination as fallback.
- **Trading was impossible to complete.** `clobTokenIds` arrived from the API
  as a *JSON string* and was passed through raw. Since trading requires the
  outcome's `token_id`, the "find market → buy" flow could never close. Each
  outcome now comes paired with its token id.
- **`positions` and `orders` were stubs** printing "Coming soon" — but
  `SKILL.md` told the agent to run `poly positions`, so it reported emptiness
  as if it were the user's portfolio. Both now query the real API.
- **Broken packaging.** `pip install .` produced a `poly` that crashed on first
  import, because `py-modules = ["cli"]` left `analyze.py`, `trade.py` and
  `configure.py` unpackaged. Restructured into a real package.
- Every `poly config` invocation shelled out to the `clawdbot` binary, which no
  longer exists (the CLI is `openclaw`).

## [1.0.2] — earlier

Initial published version. Superseded; see the security audit for the 28
findings addressed in 2.0.0.
