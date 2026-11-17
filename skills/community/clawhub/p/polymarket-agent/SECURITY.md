# Security model — polymarket-agent

This skill can custody the private key of a wallet holding money and can sign
irreversible transactions. This document describes what it protects, what it
does not, and how each finding from the ClawHub audit of 1.0.2 was addressed.

## Core principle

> **The language model proposes; the code disposes.**

No financial control depends on the LLM behaving well. A prompt injected into a
news article, a market description or a web page cannot break the limits,
because the decision is made by `guardrails.evaluate_order()` — deterministic
code, with tests.

## Surface

| Resource | Access | Note |
|---|---|---|
| Network | Polymarket `gamma-api`, `clob`, `data-api` | Hosts are module constants; never sourced from user config |
| Disk | `~/.openclaw/polymarket-agent/` (0700) | Keystore, config, journal, kill switch, alert state |
| Secret | Polygon private key | Encrypted V3 keystore (scrypt+AES), 0600 |
| Subprocesses | **none** | Removed entirely |
| Host config | **none** | The skill neither reads nor writes OpenClaw configuration |

### Metadata coherence

ClawScan flags a *metadata mismatch* when code references an environment
variable the frontmatter does not declare. All four the package reads are
declared under `metadata.openclaw.envVars`, marked `required: false` — because
the skill works without any of them (research needs no credential):

| Variable | Read in | Role |
|---|---|---|
| `POLYMARKET_KEY` | `keystore.load_key` | Legacy/CI mode; only tried if no keystore exists, and only alongside the gate below |
| `POLYMARKET_ALLOW_ENV_KEY` | `keystore._load_from_legacy_env` | Must be `1` for `POLYMARKET_KEY` to activate — mere presence of the key is not enough |
| `POLYMARKET_PASSPHRASE` | `keystore._resolve_passphrase` | Opens the keystore without a terminal (cron) |
| `POLYMARKET_AGENT_HOME` | `paths.app_dir` | Overrides the state directory |

`requires.env` is **deliberately empty**: declaring them there would hide the
skill from anyone who has not configured a wallet, when most of the value
(research, whales, leaderboard) requires no credential at all.

⚠️ **Correction from 2.0.0**: that version declared a
`metadata.openclaw.permissions` field. It **does not exist** in the ClawHub
schema — it was an assumption. An unknown manifest field is noise for the
scanner and could give a false impression that sandboxing existed. Removed.
Real authority is declared where the schema expects it (`requires`, `envVars`)
and, above all, in explicit prose in the body of `SKILL.md` — which is what the
generated Skill Card is derived from.

### Published scan result (2.1.x)

ClawHub's public scan (`clawhub scan --slug polymarket-agent`) rates this
skill `CAUTION`, while the holistic ClawScan review independently rates it
`benign` with high confidence. Both are correct readings of the same facts —
this is real-money trading software, disclosed clearly, with guard-rails that
are real but not infinite. Findings across the 2.1.0–2.1.2 publishes, and the
response to each:

1. **Env var key took silent precedence over the keystore** (High, 0.93
   confidence, surfaced on the 2.1.2 scan) — `POLYMARKET_KEY` was checked
   BEFORE the encrypted keystore and activated on its mere presence, silently
   at the point of use. **Fixed**: the keystore is now tried first;
   the env var is a fallback that additionally requires
   `POLYMARKET_ALLOW_ENV_KEY=1` and prints a warning every time it is
   actually used, not just in `poly doctor`. See `keystore._load_from_legacy_env`.
2. **Autonomous mode** (3 findings, the scan's top recommendation was
   removal). Kept deliberately — see the 2.1.2 entry in `CHANGELOG.md`.
3. **Trigger phrases too broad** — fixed in 2.1.2 by splitting `SKILL.md`'s
   trigger table into a research tier and a funds/schedule tier that requires
   naming Polymarket explicitly.
4. **`requests` dependency floor** — fixed in 2.1.2 (CVE-2026-25645, floor
   raised to 2.33.0). This CVE postdated the floor set for the 2.0.0 rewrite;
   pins need periodic re-checking, not a one-time floor.
5. **No `permissions` field in the manifest** — not actionable; see above.

If you are deciding whether to install this skill: read the trigger table and
the guard-rails table in `SKILL.md`, not just the scan badge. A `CAUTION`
rating on a skill that custodies a wallet key is the expected outcome of
disclosing that capability honestly, not evidence of hidden behavior — the
scan's own static analysis came back clean both times.

---

## Audit findings from 1.0.2 and their resolution

### High severity

**Tool Poisoning (Tp4, 99%)** — the description promised analysis while the
skill installed software, provisioned a wallet and traded real money.
→ `SKILL.md` opens with a table of real capabilities and marks what is
high-risk. The frontmatter `description` states the financial capability.

**Intent-Code Divergence (98%)** — it said "your key never leaves your machine"
while passing it as a **command-line argument** to `clawdbot config set`,
exposing it in `ps aux`, `/proc/<pid>/cmdline`, shell history and logs.
→ The key never transits argv. It is read with `getpass` (no echo), encrypted
with `eth_account.Account.encrypt` (scrypt n=2¹⁸ + AES-128-CTR) and written
0600 via `os.open(..., 0o600)` — no window between creation and `chmod`.
`poly setup` refuses non-interactive input. `LoadedKey.__repr__` and `__str__`
are overridden so the key cannot leak into logs or tracebacks, and `redact()`
reveals no character of the secret (not even the last four).

**Unvalidated Output Injection (88%)** — subprocess stdout printed raw.
→ There are no subprocesses. All externally-sourced text passes through
`safe()` (`rich.markup.escape`), so a `[/]` or `[link=...]` in a market title
cannot forge terminal output.

**Vulnerable dependency: requests (95%)** — CVE-2024-35195 (TLS verification
dropped), CVE-2024-47081 (credential leak via the per-user credentials file).
→ Floor at `requests>=2.32.4`. Additionally, all sessions use
`trust_env=False`, so the credentials file, the CA-bundle override and the host
proxy variables never enter the requests — closing the CVE-2024-47081 vector by
construction.

### Medium severity

**Dangerous Code Execution (3×, up to 97%)** — `doctor` handed a command string
to a shell; `config` shelled out with user-supplied values.
→ **No external process is spawned by the package.** Dependency checks use
`importlib.util.find_spec` in-process; configuration is local JSON via stdlib.

**MCP Least Privilege (Lp3, 97%)** — shell, network and `POLYMARKET_KEY` with
no permission declaration.
→ Environment variables are declared under `envVars`; network hosts are fixed
constants documented above; shell access no longer exists.

**Context-Inappropriate Capabilities (2×, 92-94%)** — unrestricted writes to
host global config; unnecessary host introspection in `doctor`.
→ The skill no longer touches OpenClaw config. Only the keys in `Settings`
exist, with type and range validated (`config._coerce`); unknown keys are
rejected. `doctor` reports only this skill's dependencies and active limits.

**Autonomous Decision Making (97%)** — `poly auto true` disabled all
confirmation, with no cap, no expiry and no trail.
→ Enabling requires `--i-understand-the-risk`; it **expires on its own** (max
24h, default 1h); it remains subject to every financial cap; the kill switch
takes precedence; enable/disable is journaled. A hand-edited config with
`autonomous_mode=true` and no expiry is treated as **off**.

**Missing User Warnings (4×, 90-96%)** — no financial-loss warning, no dry-run,
no transparency in `doctor`.
→ `poly setup` opens with an irreversibility warning and a dedicated-wallet
recommendation. **Dry-run is on by default.** Turning it off prints an alert.
Every order shows cost, balance and warnings before confirmation. `doctor`
states exactly what it inspects.

**Session Persistence (88%)** — suggested cron jobs to monitor markets.
→ The skill creates no schedules itself. `SKILL.md` instructs: scheduled alerts
are read/notify only, always disclosed to the user, never combined with
autonomous mode.

**Vague Trigger Phrases (3×, 92-95%)** — "what should I bet on?" and "setup" as
broad triggers.
→ The trigger table separates analysis from execution, and rule 1 is explicit:
never infer an order from a question. "Is this cheap?" is analysis.

### Low severity

**Supply Chain (6×, 90-98%)** — unpinned dependencies.
→ All pinned with floors and ceilings in `requirements.txt` and
`pyproject.toml`, each floor's reason commented. Lockfile instructions included.

**Vulnerable dependency: web3 (84%)** — CVE-2026-40072, SSRF via CCIP Read.
→ **Removed.** No line of code used `web3`; dropping the package eliminates the
CVE and dozens of transitive dependencies. `questionary` was also dropped (the
wizard uses stdlib `getpass`), and `typer[all]` became `typer`.

---

## Financial protection layers

In the order they block an order:

1. **Kill switch** — the `HALT` file. Blocks everything, including autonomous
   mode. Works even with the process dead and can be created by hand.
2. **Numeric sanity** — price in `[0.01, 0.99]`, size > 0, no `NaN`/`inf`,
   side ∈ {BUY, SELL}, numeric `token_id`.
3. **Per-order cap** — `max_position_usd` (default $25).
4. **Bankroll share** — `max_bankroll_pct` (default 5%). If the balance cannot
   be read, it warns rather than passing silently.
5. **Daily cap** — `max_daily_spend_usd` (default $100), computed from the
   journal. Rejected orders and sells do not consume budget.
6. **Open-order cap** — `max_open_orders` (default 10).
7. **Human confirmation** — mandatory except under valid autonomous mode.
8. **Dry-run** — on by default; validates and journals without sending.

Every attempt — allowed, blocked or failed — becomes a line in the append-only
journal (`poly history`). Intent is recorded **before** sending: if the process
dies mid-flight, the spend still counts (fails safe). An inter-process `flock`
covers the evaluate-and-send section so two concurrent runs cannot read the
same consumed budget.

---

## Accounting bugs fixed in 2.1.0

Found while reviewing 2.0.0 itself. The guard-rails were correct, but they were
being fed wrong numbers — which is equally dangerous:

| Bug | Effect | Fix |
|---|---|---|
| Open-order counter only grew | After ten orders in the skill's lifetime, **all trading blocked permanently** | Exchange became source of truth (`reconcile_open_orders`); fallback ignores entries older than 7 days |
| Journal rotation reset spend | Crossing 5 MB **released the entire daily cap** | `iter_entries` also reads the rotated file |
| `cancel` wrote a new line | A cancelled order counted as open forever | `close_by_order_id` closes the original entry |
| `update_status` rewrote the timestamp | A days-old order entered the 24h window | `first_ts` preserves the original instant |
| No mutual exclusion | Two concurrent `poly buy` runs jointly breached the daily cap | `flock` around the critical section |

Each has a dedicated test in `tests/test_journal.py`.

---

## Public-read surface (whales and smart money)

The `whales`, `leaderboard`, `trader`, `holders` and `quote` commands query
only public Polymarket endpoints, with no credential and signing nothing.
Specific risks and how they are handled:

- **Third-party data is untrusted content.** Trader names, market titles and
  descriptions are arbitrary text written by internet users. All of it passes
  through `escape()` before reaching the terminal, and `SKILL.md` instructs the
  agent to treat it as data, never as instructions — the natural prompt-injection
  vector for a skill that reads the outside world.
- **An alert is not an order.** The alert path touches no trading function.
  `SKILL.md` explicitly forbids converting an alert into an order, and forbids
  combining scheduling with autonomous mode.
- **Rate limits.** `/trades` allows 200 req/10s; Cloudflare *delays* rather
  than rejects, so a naive client degrades silently. The HTTP layer applies
  exponential backoff with jitter, honours `Retry-After`, and **does not retry
  4xx** (retrying a 400 only burns quota).
- **Privacy.** Queried wallet addresses are public on-chain data. The skill
  sends them nowhere except Polymarket's own API.

---

## What this skill does NOT protect

Be realistic about the boundaries:

- **It does not protect against market loss.** Guard-rails limit exposure, not
  analytical error. You can lose everything within the limits.
- **It does not protect the key on a compromised host.** Malware running as
  your user can read the keystore and capture the typed passphrase. Use a
  dedicated wallet.
- **It does not protect you from yourself.** `--yes`, dry-run off and high
  limits are your decisions.
- **It does not audit market resolution criteria.** Ambiguous resolution is a
  real risk and reading the rules is on you.
- **The keystore passphrase is not recoverable.** Lose it and you lose keystore
  access (the on-chain wallet still exists under its original seed).

## Best practices

1. A **dedicated wallet**, funded only with what you accept losing.
2. Keep dry-run on until you have validated the whole flow.
3. Keep limits low; raise them slowly and deliberately.
4. Review `poly history` regularly.
5. `poly halt` at the first sign of odd behaviour.
6. Never paste a private key into a chat, prompt or issue.

## Reporting a vulnerability

Open a report on the skill's ClawHub page. Do not include keys, addresses
holding meaningful balances, or wallet data in the report.
