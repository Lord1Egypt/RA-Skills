---
name: obscura
description: Use when scraping or automating pages with obscura.
---

# Obscura

Single-binary Rust headless browser: real V8 JavaScript, a CDP server, ~20–35 MB
RSS, no Chrome and no Node. Exposes a CLI (`fetch`, `scrape`, `serve`, `mcp`) and a
38-tool MCP server.

Verified against **obscura 0.2.6** (macOS arm64, Homebrew build) on 2026-11-13 —
every command here was run. Re-run `scripts/smoke.sh` after an upgrade. Any guide
written for 0.1.x is wrong about the SSRF guard, the `--dump` values, and MCP.

## Choose the surface

| Job | Command |
|---|---|
| One page, one value | `obscura fetch URL --eval "document.title"` |
| One page, whole output | `obscura fetch URL --dump text` (also `html`, `links`, `markdown`, `assets`, `cookies`) |
| Raw bytes or an API response | `obscura fetch URL --dump original` — skips the browser layer, binary safe |
| Many URLs, one extractor | `obscura scrape URL... --concurrency 20 --eval "..."` |
| Many raw URLs from a file | `obscura fetch --file - < urls.txt` — one status line per URL |
| Stateful flow handed to an agent | `obscura mcp` — 38 `browser_*` tools |
| Your own Puppeteer/Playwright script | `obscura serve`, then connect over CDP |

## Install and verify

```bash
brew install obscura                 # builds from source: needs Rust, ~5 min
obscura fetch https://example.com --eval "document.title"   # → Example Domain
```

Stealth builds ship as `obscura-<arch>-<os>-stealth.tar.gz` release assets. The
Homebrew formula runs `cargo install` **without** `--features stealth`, so on a brew
binary `--stealth` only does the JS-side fingerprint work — no TLS impersonation, no
tracker blocklist. Take the `-stealth` asset when either matters.

## fetch

```bash
obscura fetch https://example.com --eval "document.title"
obscura fetch https://news.ycombinator.com --dump text
obscura fetch https://example.com --dump links
obscura fetch https://api.github.com/repos/OWNER/REPO --dump original | jq .id
obscura fetch https://app.example.com --eval "JSON.stringify({t:document.title,rows:document.querySelectorAll('tr').length})"
```

Flags worth knowing (full list: `references/cli.md`):

| Flag | Default | Notes |
|---|---|---|
| `--dump` | `html` | `html`, `text`, `links`, `markdown`, `original`, `assets`, `cookies` |
| `--eval` | — | runs after load; `JSON.stringify(...)` for structured output |
| `--wait-until` | `load` | `load`, `domcontentloaded`, `networkidle0` |
| `--wait` | adaptive, 5 s cap | settle delay after load |
| `--timeout` | `30` s | navigation timeout |
| `--selector` | — | wait for a selector before dumping (see pitfalls) |
| `-s` / `-o` | — | screenshot to PNG / write output to file |
| `--storage-dir` | — | profile dir: cookies + localStorage survive runs |
| `--proxy` | — | `http://user:pass@host:port`, `socks5://host:port` |
| `--stealth` | off | fingerprint hardening (build-dependent, see above) |
| `--obey-robots` | off | respect robots.txt |
| `--allow-private-network` | off | required for localhost / RFC1918 targets |
| `-q` | off | quiet: banner and progress off |

stdout carries only the result; progress goes to stderr, so pipes stay clean
(`obscura scrape ... | jq` works).

## scrape

```bash
obscura scrape https://example.com https://example.org \
  --concurrency 20 --eval "document.title" --format json | jq -c '.results[]'
```

- `--concurrency` default `10`, `--timeout` default `60` s, `--format json|text`.
- json: `{total_urls, concurrency, total_time_ms, avg_time_ms, results:[{url, title, eval, time_ms, worker}]}`
- text: one `<ms>\t<url>\t<value>` line per URL.

`scrape` extracts values; `fetch --file` only reports per-URL status and byte counts.

`scrape` fans work out to `obscura-worker` processes and finds them **in the same
directory as the `obscura` binary**. Homebrew and the release tarballs ship both;
an install that copies only `obscura` makes `scrape` print nothing and exit 0.

## MCP server

```bash
obscura mcp                                             # stdio: Hermes, Claude Code, Codex
obscura mcp --http --port 3000                          # POST /mcp, MCP protocol 2024-11-05
OBSCURA_MCP_TOKEN=$(openssl rand -hex 32) obscura mcp --http --host 0.0.0.0 --port 3000
hermes mcp add obscura -- obscura mcp                   # Hermes
claude mcp add obscura /path/to/obscura mcp             # Claude Code
```

38 tools, all `browser_*`: navigate, snapshot, click, fill, type, press_key,
select_option, evaluate, wait_for, wait_for_text, wait_for_function, markdown, links,
interactive_elements, extract (CSS schema → JSON), detect_forms, fill_form, scroll,
get_attribute, count, search, network_requests, console_messages, tab_new/list/switch/
close, get/set/clear_cookies, storage_state, set_storage_state, screenshot, pdf,
back, forward, reload, close. Parameter names: `references/mcp-tools.md`.

Targeting localhost through MCP needs `--allow-private-network`, same as the CLI.

## serve (CDP)

```bash
obscura serve --port 9222                # /json/version: Chrome/145.0.0.0, protocol 1.3
```

Both verified end to end against a live `serve`:

```js
// puppeteer-core
const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:9222/devtools/browser' });

// playwright-core
const browser = await chromium.connectOverCDP('ws://127.0.0.1:9222');
```

Playwright Test: `use: { connectOptions: { wsEndpoint: 'ws://127.0.0.1:9222' } }`.
Throughput knobs: `--workers N`, `--max-connections`, `--ready-file`.
`connectOverCDP` gives you one default context — `browser.contexts()[0]`; a
`newContext()` also works but starts an incognito target.

## Sessions

`--storage-dir ./profile` persists cookies and localStorage between processes:
set a login once, then reuse the dir for every later `fetch`/`scrape`/`serve`.
Verified: a cookie written in one `fetch` was replayed by the next. Use one dir per
identity, and treat it as a credential store — it contains live session tokens.

## Pitfalls (each observed on 0.2.6)

1. **A lone `obscura` binary breaks `scrape` silently.** Work is fanned out to
   `obscura-worker`, which is looked up in the `obscura` binary's own directory. Homebrew
   and the release tarballs ship both; an install that copies only `obscura` gets empty
   output and exit code 0 (hit in CI). `scripts/smoke.sh` checks for it.
2. **Loopback is blocked by default.** `obscura fetch http://127.0.0.1:8765/` fails with
   `Access to private/internal IP address 127.0.0.1 is not allowed` (SSRF guard).
   Add `--allow-private-network` or set `OBSCURA_ALLOW_PRIVATE_NETWORK=1`. Any local
   dev-server or E2E flow dies here without it.
3. **`--selector` and `--eval` do not combine.** With both, the eval is silently dropped
   and fetch prints HTML. Wait via `--wait-until`/`--wait`, or poll inside the eval.
4. **`--dump markdown` is a raw DOM→MD pass** — nav chrome, tab runs and blank lines
   survive (checked on wikipedia and quotes.toscrape). For readable article text prefer
   `--dump text` plus slicing, or a targeted `--eval`.
5. **`fetch` has no JSON mode.** Return JSON yourself: `--eval "JSON.stringify(...)"`.
6. **`--file` batch mode returns status lines**, not page content:
   `{url, ok, status, content_type, bytes, elapsed_ms}`.
7. **Version strings disagree.** `/json/version` advertises `Chrome/145.0.0.0`, the
   default `fetch` UA is `Chrome/143.0.0.0` (Windows). Don't gate behaviour on either;
   set `--user-agent` when a site needs a specific one.
8. **Don't shell-loop `fetch`** over thousands of URLs — use `scrape` (worker pool) or
   `fetch --file` (concurrency option). Both reuse one engine.

## Anti-patterns

- `--stealth` hides automation; it is not a paywall or auth bypass.
- Respect a site's terms and robots.txt (`--obey-robots`) where they apply.
- Always leave a kill path for `serve`/`mcp` processes; they hold ports and profiles.

## References

- `references/cli.md` — verbatim 0.2.6 `--help` for the root command and every subcommand.
- `references/mcp-tools.md` — the 38 MCP tools with parameter names.
- `references/upstream-docs.md` — index of obscura's own docs (22 files) and what each answers.
- Upstream repository: https://github.com/h4ckf0r0day/obscura (Apache-2.0).
