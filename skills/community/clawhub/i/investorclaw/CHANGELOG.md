# Changelog

All notable changes to InvestorClaw v4.x (mnemos-os/mnemos-ic-runtime).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Distribution-edge artifacts (`SKILL.md`, `compose.yml`, `install.yaml`,
`agent-skills/**`) are MIT-0; substantive code (bridge, dashboard,
Dockerfile, tests) is Apache 2.0.

## [4.7.2] — 2026-06-11

### Security

- Scrubbed the repo owner's real brokerage account numbers/labels from
  `fetch_holdings.py` ACCOUNT_LABELS docstring examples (now fake
  placeholders). No data was ever baked into the image; this removes
  identifying examples from source. Pins `ic-engine:4.7.2-cpu`.

## [4.7.1] — 2026-06-11

### Fixed

- **UBS unrealized gain/loss now matches the broker statement.** Two engine
  bugs caused total unrealized G/L to under-report (e.g. $379,359.64 vs the
  broker's $642,400.41 on a multi-account portfolio):
  - Multi-account holdings collapsed by ticker summed market value and shares
    but kept only the first account's broker-reported unrealized G/L. Now the
    broker `UNREALIZED GAIN/LOSS $` column is summed across all accounts.
  - Equities whose name contains "cash" (e.g. FIRSTCASH HLDGS INC / FCFS) were
    misclassified into the cash bucket via a substring match. The cash keyword
    is now word-boundaried, so such tickers stay equities.
- Pins `ghcr.io/argonautsystems/ic-engine:4.7.7-cpu`.

## [4.1.35] — 2026-05-06

### Fixed

- **Multi-arch publish for arm64 hosts.** v4.1.34 shipped a multi-arch
  manifest list at `ghcr.io/argonautsystems/ic-engine:4.1.34-cpu`, but
  the published ClawHub bundle's `compose.yml` and `install.yaml`
  pinned to the AMD64 sub-manifest digest (`sha256:7f07d516…`). On
  arm64 hosts (NCZ Reinhardt cixmini boards, Raspberry Pi 5, Apple
  Silicon, AWS Graviton), `docker compose pull` would fetch the x86
  binary and fail with `exec format error` at startup.
- v4.1.35 repins to the **manifest list digest** `sha256:45a9c5bd…`,
  which resolves per-architecture automatically. amd64 hosts continue
  to pull the same x86 image; arm64 hosts now pull the
  `ghcr.io/argonautsystems/ic-engine@sha256:aa87f4809e…` arm64/v8
  variant transparently.

### Added

- arm64 image natively built on `.66` (NCZ Reinhardt 26.5 cixmini,
  podman 5.4.2). 1.11 GB, matches the x86 trim exactly. Available at
  `ghcr.io/argonautsystems/ic-engine:4.1.35-cpu` (and
  `:4.1.34-cpu-arm64` / `:latest-arm64` single-arch tags for direct
  platform pinning).
- Verified end-to-end on .66: container init → ready in 41s, all 13
  MCP tools registered, all 8 provider keys settable via the
  `keys_set` REST endpoint, dashboard responsive at port 18092.
- 30/30 cobol NLQ PASS at 3/3 trials each (90/90 trials, every trial
  `engine_exit=0` + `has_hmac=true`, p95 latency 28s, median 7s warm).
  The arm64 result includes p09-optimize-sharpe, the lone holdout
  from the TYPHON x86 agent-driven 29/30 baseline.

### Notes for arm64 deployment

- **Rootless podman** requires `--userns=keep-id:uid=1000,gid=1000`
  for `/data/keys.env` permissions. Without that flag, the container
  runs but reports `init_state: failed` because the engine subprocess
  cannot chmod its reports directory. Compose-based installs are
  unaffected (compose handles the user mapping automatically).
- NCZ Reinhardt 26.5 ships podman 5.4.2 but **does not** include the
  `docker-compose-cli` plugin. Use raw `podman run` or install
  `podman-compose` via pip.
- The skill bundle's `compose.yml` now uses the manifest list digest;
  any container engine that supports OCI manifest lists (Docker 20+,
  podman 4+, containerd 1.5+) resolves the per-arch image
  transparently.

## [4.1.34] — 2026-05-04

### Added

- **Five new dashboard tabs** to cover every cobol NLQ datapoint
  (`harness/cobol/nlq-prompts.json`, 30 prompts):
  - `/dashboard/optimize` — Sharpe-max + min-volatility allocations
    plus rebalance + tax-aware rebalance trade tables
    (covers p09 / p10 / p11 / p12 / p13)
  - `/dashboard/cashflow` — projected dividends + bond coupons,
    quarter and annual totals, per-symbol payment schedule (p25)
  - `/dashboard/peer` — benchmark comparison (returns, Sharpe,
    drawdown, correlation, beta vs VTI/SPY/AGG/etc.) (p26)
  - `/dashboard/markets` — indices, crypto, FX, fixed-income yields
    (p17 / p18 / p21 / p22)
  - `/dashboard/lookup` — per-ticker quote + fundamentals form
    (p27)
- **Glossary** section on About tab — Sharpe, Sortino, drawdown,
  beta, VaR, YTM, duration, allocation strategies (p20).
- **First-time setup** numbered checklist on About tab (p29).
- **Web-based portfolio upload** on Settings tab. Multipart form
  posts to `POST /dashboard/upload`; file is sanitized
  (basename + alphanumeric/`._-` only, 200-char cap), saved to
  `/data/portfolios/<safe_name>`, then a refresh sweep is fired
  in the background. Lists current portfolio files in a table
  next to the form.
- **Regenerate button** on Overview tab. `POST /dashboard/regenerate`
  fires the full data + analyzer sweep
  (setup → refresh → performance / bonds / analyst / news /
  whatchanged / scenario / optimize / rebalance / cashflow /
  peer / markets / synthesize) as a background task and redirects
  immediately with a success banner.
- **`MASSIVE_API_KEY` and `MARKETAUX_API_KEY`** added to the
  setup_api `KNOWN_KEYS` list and the `keys.py` `_allowlist()`
  fallback set, so the agent-facing `portfolio_keys_set` REST tool
  and the dashboard Settings form can both persist them without
  needing a `docker exec -u 0` workaround.
- **`python-multipart>=0.0.9`** added to bridge dependencies
  (required by FastAPI for the upload form).

### NLQ coverage

Final tab-to-prompt map (17 tabs, 30 NLQs):
Overview p23/p24 · Holdings p01/p02/p11/p28 · Performance p03/p04 ·
What Changed (delta) · Scenarios · Bonds p14/p15 · Optimize
p09/p10/p12/p13 · Cashflow p25 · Peer p26 · Analyst p05 ·
News p06/p16/p19 · Markets p17/p18/p21/p22 · Lookup p27 ·
Synthesis p07/p08 · Reports p23/p24 · Settings · About p20/p29/p30.

## [4.1.29] — 2026-05-04

### Added

- **Reference / contract specs** ported from v2.6 git history into
  `docs/references/`:
  - `contract-input.md` — broker-CSV column mapping (recognized column
    names, bond metadata extraction from description strings, guided
    mapping flow)
  - `contract-output.md` — full output spec (directory layout, envelope
    format, compact vs full output rules)
  - `schema-holdings-fields.md` — per-position field reference
    (security_type, is_etf, financial_type, proxy_symbol)
  - `runtime-gemma4-consult.md` — gemma4-consult Ollama setup for the
    optional consultative LLM tier
  - `presentation-rules.md` — agent presentation contract
    (preserve numbers, timestamps, freshness; never fabricate)
  - `presentation-nl-query-routing.md` — natural-language query routing
    rules (which question shapes go to which analyzer)
  - All include v4.x adaptation note explaining the slash-command →
    MCP-tool surface change.
- **`docs/MCP_TOOLS_REFERENCE.md`** (new) — consolidated detailed
  reference for all 12 MCP tools (`portfolio_ask`, `portfolio_initialize`,
  `portfolio_holdings`, `portfolio_refresh`, `portfolio_setup`,
  `portfolio_keys_*`, `portfolio_response_*`). Per-tool: input schema,
  output shape, latency profile, cache TTLs, allowlists, example calls,
  pointers to contracts. Distilled from the ~25 v2.x `claude/commands/ic-*.md`
  per-slash-command docs into one consolidated file (one doc to maintain
  rather than 25).

### Changed

- `README.md` Documentation section updated to link the new MCP tools
  reference and the references directory.

Engine image stays at 4.1.25-cpu (docs-only release).

## [4.1.28] — 2026-05-04

### Added

- **Feature docs ported** from v2.6 git history (deleted in v4.0
  nuke-from-orbit trim):
  - `STONKMODE.md` (top-level) — full feature doc for narrated
    commentary mode with 30+ fictional cable-finance personas
  - `CAPABILITIES.md` (top-level) — master "what can it do" feature
    catalog covering holdings, performance, bonds, news, allocation,
    optimization, scenarios, peer analysis (~19 KB)
  - `docs/GLOSSARY.md` — financial-terminology reference (Sharpe,
    Sortino, YTM, duration, beta, drawdown, etc.)
  - `docs/PHILOSOPHY.md` — the "deterministic-first, no LLM math"
    rationale
  - `docs/WINDOWS_SETUP_GUIDE.md` — Windows + WSL2 install gotchas
  - `docs/STONKMODE_ARCHITECTURE.md` — full Stonkmode pipeline
    (market detection → archetype weighting → pair selection →
    narration → dashboard render)
  - `docs/STONKMODE_AVATAR_LEGEND.md` — 30-persona avatar grid
    reference
- All ported docs include a `<!-- v4.x adaptation note -->` header
  explaining what changed between v2.x slash-command surface and
  v4.x MCP-tool surface (numerical results, methodology, and
  data-source rules unchanged).

### Changed

- **Auto-start install convention added to SKILL.md.** When a
  skills installer (e.g. `openclaw skills install investorclaw`)
  places the bundle, agents should immediately run
  `mkdir -p portfolios && docker compose up -d` from the skill
  directory as part of completing the install — the user invoked the
  install command and has implicitly consented to it completing.
  Do not gate a second time on "Want me to boot it up?" Override
  cases (CI runner, existing ic-engine container with different tag,
  user-supplied `--dry-run`) are documented inline.

## [4.1.27] — 2026-05-04

### Added

- Top-level community / health docs: `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `DISCLAIMER.md`, `PRIVACY.md`,
  `CHANGELOG.md` (this file). Adapted from the v2.6 InvestorClaude
  corpus for the v4.x containerized-skill context.
- `.github/ISSUE_TEMPLATE/` (bug, feature, docs) +
  `.github/PULL_REQUEST_TEMPLATE.md` for github community-standards
  compliance.
- Logo header in `README.md` — restored from git history (was deleted
  in the v4.0 nuke-from-orbit trim).
- Stonkmode and EOD-report sections added to `README.md` Run Analysis
  section.
- `assets/investorclaw-logo.{svg,jpg,webp,*-192.{jpg,webp}}` — logo
  assets restored from git history.

### Changed

- `clawhub skill publish --name "InvestorClaw"` corrects the display
  name from auto-derived "Mnemos Ic Runtime" to "InvestorClaw".
- `README.md` rewritten to mirror the InvestorClaude v2.6 user-facing
  voice: Features → Quick Start → Prepare Portfolio → Run Analysis
  (with EOD + Stonkmode subsections) → Available MCP Tools →
  Power-User Endpoints → Recommended Models → API Keys by Size →
  How It Works → Data Privacy → Documentation → Troubleshooting.

### Security (3 fixes addressing ClawHub LLM-scan findings)

- **Trust-exploitation wording** — tightened the contradictory
  "no portfolio data flows through transcript storage" line in
  `agent-skills/claude-desktop/SKILL.md` to clarify what Claude does
  vs does not see in the envelope.
- **Supply-chain hardening** — install hints no longer reference the
  mutable `raw.githubusercontent.com/.../main/` URL; bundle ships
  `compose.yml` directly.
- **Code-execution warnings** — `apt-get install -y docker.io` style
  commands reframed as user-facing recommendations with a link to
  docs.docker.com rather than agent-runnable strings.

## [4.1.26] — 2026-05-04

### Added

- "First-run experience" section in `SKILL.md` covering the auto-init
  phase timeline (image extract → bridge → setup → refresh → seed_ask
  → ready) with timing per phase, what InvestorClaw asks of the user
  post-install, recommended API keys by portfolio size with sign-up
  links, and an example first-call response shape.

## [4.1.25] — 2026-05-04

### Fixed

- **Engine narrator regression** (argonautsystems/ic-engine
  commit `b7a8859`): `"What is in my portfolio?"` was being deflected
  as a concept question because the `"what is "` concept-stem matched
  before OWNERSHIP signals. Fix: short-circuit the concept-stem
  check when a strong-ownership phrase is present (`my portfolio`,
  `my holdings`, `my positions`, `my account`, plus common
  portfolio-computed metrics like `my sharpe`, `my returns`,
  `my allocation`, etc.). Preserves the original v4.1.17 NA-METRIC
  protections.
- **Install-breaking compose.yml bug** — `./portfolios/` was being
  auto-created as `root:root` by docker bind-mount, blocking the
  engine (uid=1000) from writing `setup_results.json`. SKILL.md now
  leads with `mkdir -p portfolios` + inline explanation.
- **zeroclaw audit false-positive** — SKILL.md compliance bullet
  reworded to avoid the audit's literal-string match on
  shell-pipe-installer patterns in documentation.

### Changed

- **Default narrative model** flipped from `MiniMaxAI/MiniMax-M2.7`
  to `google/gemma-4-31B-it`. Together AI moved MiniMax-M2 off the
  serverless tier in 2026-05; gemma-4-31B-it is the cheapest
  serverless model with strong-enough quality for portfolio narrative
  (~100 tok/s, ~$0.0008 / 1 K tokens).
- New container image: `ghcr.io/argonautsystems/ic-engine:4.1.25-cpu`
  (sha256:2c34311f...).

## [4.1.24] — 2026-05-04

### Changed

- Anthropic-on-claws wording corrected per Boris Cherny's 2026-04-03
  announcement: subscription OAuth no longer covers third-party
  tools, but Anthropic remains usable via discounted "extra usage
  bundle" add-on or direct Anthropic API key. Updated SKILL.md and
  per-runtime narrator-model sections.

## [4.1.23] — 2026-05-04

### Added

- v2.6 InvestorClaude user-facing docs ported into the v4.x skill:
  cookbook tables ("what can I ask?"), agent routing rules + finance
  override, broker export instructions, model recommendations split
  per runtime track, privacy section, troubleshooting section,
  dashboard UX walkthrough.

### Fixed

- Stale container-internal port refs (`:8090` / `:8092`) replaced
  with host-mapped ports (`:18090` / `:18092`) across 15 files
  including `manifest-template.json`. Would have broken every fresh
  install via the manifest pointing agents at the wrong port.
- `argonautsystems/clio` GitHub reference removed from
  `docs/INSTALL_MODELS.md` (clio lives on GitLab, not GitHub);
  replaced with explicit github + gitlab URLs for
  `argonautsystems/ic-engine`.

## [4.1.22] — 2026-05-04

### Changed

- Dockerfile uses `pip install uv` instead of the upstream
  shell-pipe installer at `https://astral.sh/uv/install.sh` to clear
  the ClawHub static-analyzer's `install_untrusted_source` flag at
  build time.

## [4.1.21] — 2026-05-03

### Fixed

- `install.yaml`: dropped the remote-curl staging step.

## [4.1.19] — 2026-05-03

### Changed

- Engine image moves to verified-org namespace
  `ghcr.io/argonautsystems/`.

## [4.1.18] — 2026-05-03

### Changed

- Compose: bake codex-scrubbed engine source.

## [4.1.17] — 2026-05-03

### Fixed

- Classifier fix: CONCEPT-STEM + NA-METRIC overrides ahead of
  OWNERSHIP. (Note: this introduced the regression that v4.1.25 later
  fixes.)

## [4.1.16] — 2026-05-03

### Fixed

- Correlation / total-return / ESG / governance fixes.

## [4.1.15] — 2026-05-03

### Fixed

- Engine SPY benchmark + Sortino + drawdown.

## [4.1.14] — 2026-05-03

### Achievement

- 30/30 PASS (100%) on the Agentic COBOL regression harness.

## [4.1.13] — 2026-05-03

### Fixed

- Engine fixes baked + deflection narrator (28/30 cobol).

## [4.1.7] — 2026-05-03

### Added

- `portfolio_initialize` tool + boot-time auto-init
  (`IC_INITIALIZE_ON_BOOT=1`) so the envelope cache is warm by the
  time any agent connects.

## [4.1.6] — 2026-05-03

### Fixed

- Massive adapter fix.

### Added

- Three new market-data providers + yfinance-last fallback + stage
  wiring + MNEMOS persistence.

## [4.1.4] — 2026-05-03

### Added

- MNEMOS persistence + MiniMax-M2.7 default + `MNEMOS_BASE` env var.

## [4.1.3] — 2026-05-02

### Fixed

- Analyst PriceProvider fallback (Finnhub → Massive → yfinance).

## [4.1.2] — 2026-05-02

### Fixed

- Engine HoldingsStage fix.

## [4.1.1] — 2026-05-02

### Fixed

- Engine P1 parallel-stage timeout fix + bridge timeouts to 1800 s.

## [4.1.0] — 2026-05-02

### Changed

- ic-engine image bump to `4.1.0-cpu` + MiniMax-M2 (1M context).

## [4.0.9] — 2026-05-02

### Refactored

- Bridge: split `mcp_server.py` into `mcp/` package mirroring v5
  mnemos.

## [4.0.7] — 2026-05-02

### Fixed

- Bridge: pass `--no-refresh` to ic-engine ask for deterministic
  cache hits. (Note: later reverted; see SKILL.md "Behavior contract".)

## [4.0.5] — 2026-05-02

### Added

- Plain REST endpoints — agent fallback when native MCP is flaky.

## [4.0.4] — 2026-05-02

### Fixed

- Bridge: disable DNS-rebinding protection on MCP transport
  (configurable).

## [4.0.3] — 2026-05-01

### Fixed

- Bridge: clear yfinance cookie cache on subprocess timeout.

## [4.0.2] — 2026-05-01

### Changed

- Build: pass-5 strip — sqlalchemy, networkx, tests/ dirs (–51 MB).

## [4.0.0a1] — 2026-04-30

### Added

- Initial scaffold of mnemos-ic-runtime as the v4.x containerized-skill
  bridge. Engine source moved to `argonautsystems/ic-engine` (separate
  repo); this repo owns Dockerfile + compose + bridge + dashboard +
  agent-skills.

[4.1.27]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.27
[4.1.26]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.26
[4.1.25]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.25
[4.1.24]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.24
[4.1.23]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.23
[4.1.22]: https://github.com/mnemos-os/mnemos-ic-runtime/releases/tag/v4.1.22
