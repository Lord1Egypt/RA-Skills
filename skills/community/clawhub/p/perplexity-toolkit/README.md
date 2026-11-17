# Perplexity Toolkit

**English** | [简体中文](README.zh-CN.md)

Automate Perplexity AI search via browser control — search, extract, batch, and analyze.

## What It Does

- **4 search modes**: Standard, Deep Research, Model Council, Step-by-step Learning
- **Batch pipeline**: Search hundreds of queries with resume and rate limiting
- **Result aggregation**: Dedup sources, rank by frequency, generate reports
- **Source extraction**: Get all cited URLs with titles and snippets
- **Follow-up capture**: Extract Perplexity's suggested follow-up questions
- **Resident console**: one fixed tab/group workspace with verified step gates — task threads, granular steps (fill/submit/wait/extract), model switching, file attachments, and an optional Jev judge layer
- **Agent skills**: Three ready-to-load `SKILL.md` files in [`skills/`](skills/) — routing policy, session discipline, and the verification rule — for agents that drive this toolkit

## Quick Start

```bash
# Install so `perplexity` is on your PATH (recommended)
pipx install git+https://github.com/mfang0126/perplexity-toolkit.git

# ...or for development, into the CURRENT environment only:
#   pip install -e .
# If you use pip, install into the same environment your agent runs,
# otherwise `command -v perplexity` will not find it.

# Single search
perplexity search "best AI coding agents 2026"

# Keep several CLI commands in one task session; this global option comes
# before the subcommand.
perplexity --session-prefix coding-agents-2026 search "best AI coding agents 2026"

# Skip the default quality/readback annotation only when explicitly needed.
perplexity --no-verify search "best AI coding agents 2026"

# Classify the original user wording before selecting CLI or direct browser.
# This command is local; it does not open Chrome or call Perplexity.
perplexity route -f json "Please use Perplexity in Chrome"

# Deep Research (multi-step, 60-120s)
perplexity search "AI safety risks 2026" -m deep_research

# Batch from file
perplexity batch -i queries.json -o results.json

# Aggregate results
perplexity aggregate results.json -f markdown
```

Search output is quality-annotated by default. A JSON search result is always
one JSON document on stdout; human-readable quality text is not appended to
`-f json`. The quality block distinguishes HTTP reachability from bounded page
readback and reports `verification_state: candidate` / `claim_support:
not_evaluated` until a human or semantic evidence pass confirms each claim.

## Resident Console (fixed tab/group)

Keep one persistent tab/group for Perplexity and route every question through verified steps — one task = one thread:

```bash
perplexity console ask "Will X happen?" --task my-project -f json   # creates or continues the task thread
perplexity console ask "And the Y angle?" --task my-project          # follow-up in the same thread
perplexity console ask "New topic" --new-thread --task other         # fresh thread in the same tab
perplexity console ask "Review this" --file report.pdf               # attach local files (repeatable, <=8MB)
perplexity console models                                            # list selectable models
perplexity console model "Claude Sonnet 5"                           # switch model (verified readback)
perplexity console status      # state + live tab readback
perplexity console threads     # recorded task threads
perplexity console selfcheck   # run the full gate pipeline on a canned query
```

Granular steps for intent-driven composition (share one implementation with `ask`, joined by a staged-turn ledger):

```bash
perplexity console fill "q" [--task T] [--file F]   # stage: attach + fill + verify (no send)
perplexity console submit                            # submit the staged turn (verified, self-healing)
perplexity console wait [--wait N]                   # wait for the staged answer to settle
perplexity console extract                           # turn-scoped answer; consumes the staged turn
perplexity console send "q"                          # fill + submit only
perplexity console attach --file F | files | detach NAME
perplexity console open <task|url> [--new-thread]
```

- **Gates, not best effort**: every step is verified (composer equality incl. editor state, user-turn ownership, completion signals, turn-scoped answer extraction). Failures raise with a screenshot under `~/.perplexity-console/evidence/` and a machine-readable `error_code` — silent wrong answers are the one outcome the console never reports as success.
- **Stepwise, not one-shot**: `ask` is a composite of granular steps (`fill → submit → wait → extract`) that share one implementation each; the steps are also callable alone and compose through a staged-turn ledger (`state.json → pending`), so retries and unusual flows are per-step instead of all-or-nothing. Every run appends one line to `~/.perplexity-console/runs.jsonl`.
- **Model & files**: `perplexity console models` / `model "<name>"` switch the Perplexity model with a verified readback; `ask --file` attaches local files (in-page injection, ≤8MB) and verifies every attachment chip before sending.
- **Optional Jev judge**: `ask --judge` / `extract --judge` (or `PERPLEXITY_CONSOLE_JUDGE=1`) adds an advisory verdict on extracted answers and recovery routing; on failing **fill/wait/extract** steps the chosen remedy is executed once (bounded Jev-directed recovery, re-run under all original gates) while send paths stay advisory-only — via one batched TypeSafe request, fail-open and validation-guarded; the pipeline never depends on it.
- **Durable state**: `~/.perplexity-console/state.json` (session, group, per-task thread URLs). WebBridge session→tab mappings are daemon-memory only; the console attach-or-recreates the tab from the saved thread URL after daemon/browser restarts.
- **Self-heal**: a desynced editor (DOM text vs internal state) is repaired by one bounded page reload before failing loudly; mis-sent turns (e.g. file-only) recover via reload + re-inject + a bounded, duplicate-safe retry.

## Python API

```python
from perplexity_toolkit.search import search, deep_research, model_council

# Standard search
result = search("Python vs Rust 2026")
print(result["answer"])      # Full answer text
print(result["sources"])     # [{text, href}, ...]
print(result["follow_ups"])  # ["follow-up question", ...]

# Deep Research (longer, more detailed)
result = deep_research("AI agent frameworks comparison")

# Model Council (multiple models answer)
result = model_council("best programming language for beginners")
```

## Batch Pipeline

```python
from perplexity_toolkit.batch import run_batch

queries = [
    {"query": "topic 1", "mode": "search"},
    {"query": "topic 2", "mode": "deep_research"},
]
results = run_batch(queries, output_file="results.json", delay=5.0)
```

## Architecture

```
perplexity_toolkit/
├── __init__.py          # Package init
├── config.py            # Configuration management
├── search.py            # Core search functions (4 modes)
├── batch.py             # Batch pipeline with resume
├── aggregator.py        # Result aggregation + reports
├── history.py           # Conversation history management
├── verify.py            # Source/answer quality verification
├── routing.py           # User-intent route gate (CLI vs direct browser)
├── console.py           # Resident console (fixed tab/group, verified step gates)
├── console_judge.py     # Optional Jev judge layer (advisory, fail-open)
├── drivers/             # Browser driver abstraction
│   ├── base.py          # Abstract BrowserDriver interface
│   └── webbridge.py     # Kimi WebBridge implementation
├── utils/               # DOM parsing + event/timing helpers
│   ├── __init__.py
│   ├── antidetect.py    # Human-like timing / anti-detection
│   └── i18n.py          # UI-string locale tables
└── commands/            # CLI
    └── cli.py
```

## Browser Driver

The toolkit uses an abstract `BrowserDriver` interface. Current implementation:

- **WebBridgeDriver** — Kimi WebBridge (Chrome extension + local daemon)

This is the **only** shipped backend. Every search mode drives a real logged-in
browser through it; there is no API-key or headless path. `aggregate` is the one
subcommand that runs without a browser, because it only post-processes result
JSON you already fetched.

To add a new backend (Playwright, Selenium, etc.), implement `BrowserDriver` in `drivers/`:

```python
from perplexity_toolkit.drivers.base import BrowserDriver

class PlaywrightDriver(BrowserDriver):
    def navigate(self, url, new_tab=True, group_title=""): ...
    # Optional session hygiene hook; unsupported drivers may omit it.
    def list_tabs(self): ...
    def snapshot(self): ...
    def click(self, selector): ...
    def fill(self, selector, value): ...
    def evaluate(self, code): ...
    def screenshot(self, path=None): ...
    def close(self): ...
```

## Requirements

- Python 3.9+
- Kimi WebBridge daemon (`~/.kimi-webbridge/bin/kimi-webbridge start`)
- Chrome with Kimi WebBridge extension installed
- Perplexity account (free or Pro)

## Verify Your Setup

Run these three checks in order. Each one isolates a different failure.

```bash
# 1. Is the command reachable?
command -v perplexity && perplexity --help >/dev/null && echo "CLI OK"

# 2. Is the WebBridge daemon up?
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"list_tabs"}'

# 3. Is Chrome connected?
#    Step 2 returns {"ok":true,...} when the daemon is up.
#    If it reports "no extension connected", the daemon is running but Chrome
#    is not attached — open Chrome and check the WebBridge extension.
```

| Symptom | Cause | Fix |
|---|---|---|
| `command -v perplexity` finds nothing | Installed into an environment that is not on your `PATH` | `pipx install git+https://github.com/mfang0126/perplexity-toolkit.git`, or export `PERPLEXITY_BIN=/full/path/to/perplexity` |
| `curl` to port 10086 fails | Daemon not started | `~/.kimi-webbridge/bin/kimi-webbridge start` |
| Daemon replies `no extension connected` | Chrome not attached | Open Chrome; confirm the WebBridge extension is enabled. This is **not** a rate limit or a thread cap |
| Search returns an empty answer | Not logged in to Perplexity in that browser | Log in to perplexity.ai in the same Chrome profile |

Note for agent authors: do not probe with a bare `python3 -c "import perplexity_toolkit"`.
The toolkit lives in whichever environment it was installed into, which is usually
not the interpreter that `python3` resolves to. Probe for the console script
(`command -v perplexity`, `$PERPLEXITY_BIN`, `$VIRTUAL_ENV/bin/perplexity`) instead,
and report "not resolved in this environment" rather than "not installed".

## Known Limitations

- Deep Research mode leaks a "/" prefix in the query (Perplexity handles it gracefully)
- Jev submenu model entries (e.g. "GPT-5.6 Sol | Max") are listed by `console models` but not programmatically selectable yet
- Console attachments are capped at 8 MB via in-page injection; larger files need Chrome's per-extension "Allow access to file URLs" for the official WebBridge upload path

## Research

See `docs/research/` for comprehensive analysis of Perplexity's known issues, API vs web gap, and browser automation mapping. [`docs/reference-pro-guide.md`](docs/reference-pro-guide.md) is a practical Perplexity Pro playbook (model-picking strategy, features, limits; snapshot 2026-08-30).

## License

MIT
