# donsetch integration — ocas-sift tier-3 anti-bot fallback

Source: https://github.com/dondai44423/donsetch (AGPL v3, Rust). Binary: v3.2.3 installed at `/usr/local/bin/donsetch` (`donsetch-linux-x64.tar.gz`, 39.9 MB). Verified locally on this host (`uname`: x86_64 Ubuntu 26.04).

## What it does

Built-from-scratch web agent: fetch, search, crawl. Uses Chrome's native TLS (BoringSSL), temporal stealth (TLS session resumption, conditional revalidation 304, persistent cookies), headless escalation, solve-and-bounce (browser solves challenge, hands cookies to tier 1), and adaptive domain intelligence (per-domain cookie lifetimes, warm-start routing). Not a Python/playwright stack — zero dependency on existing OSS web tooling.

## Tier placement (do NOT replace SearXNG tiers 1-2)

- Tier 1: Internal knowledge + free web search (SearXNG at `localhost:8888`, N2 MCP, Brave, platform search) — stays primary.
- Tier 2: `sift.fetch` (Scrapling → Jina Reader fallback) — static / near-instant fetch.
- **Tier 3 (this integration):** `donsetch fetch` — when tier 1 + tier 2 return bot-wall / 403 / CAPTCHA / empty body / <200-char body against CF, Akamai, DataDome, Imperva.
- Tier 4: `sift.webwright` (`playwright` + stealth) — interactive JS-heavy flows.

## Error-code mapping (`donsetch` exit codes)

From verified `--help` output: `0` success · `1` permanent error · `2` transient (retry) · `3` walled (try different source). When exit `3`, escalate to `sift.webwright` (tier 4), do NOT retry `donsetch` with same URL.

## Commands integrated

- `donsetch fetch [url]` — clean markdown extraction with bot-wall bypass. First call after this integration; verify before relying.
- `donsetch search` — 5 keyless engines merged + reranked (not integrated as tier 1 — SearXNG stays primary).
- `donsetch crawl [url]` — sitemap-aware resumable crawl.
- `donsetch mcp --supervised` — MCP server (JSON-RPC on stdio) — available but not wired into `sift`'s pipeline yet; requires explicit opt-in.

## Caveats

- AGPL v3 — license-aware if redistributing the binary; installed locally here only.
- One binary (~40 MB) — larger footprint than Python dependency.
- `solve-and-bounce` uses a persistent Chrome session; watch for `donsetch stop` to kill orphaned Chrome + clean locks (documented in help output, `doctor` health-check available).
- Not a replacement for `sift.search` / SearXNG tier 1; uses different backend mix (`donsetch`'s own keyless search fusion vs. SearXNG plugin routing).
- Integration scope (this file): binary installed; SKILL.md + pitfalls.md patched. `sift` command wrappers not yet added to `sift.search` / `sift.research` — requires further skill update by user/Koda.
