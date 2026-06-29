---
name: makewpfast-bench
description: This skill should be used when the user asks about a WordPress plugin's or theme's real performance/speed impact, wants to compare the speed of plugins or themes, asks whether a plugin is slow or heavy, or wants to audit the plugins on a WordPress site — e.g. "how fast is WooCommerce", "compare Yoast vs Rank Math speed", "is this plugin slow", "what's the TTFB cost of this plugin", "audit my site's plugins". It queries the MakeWPFast Benchmark API (real measured activation/homepage/wp-admin deltas for ~52,000 WordPress.org plugins and themes) via the bundled mwf-bench CLI.
version: 1.0.0
domain: wordpress
type: action
tools: [python3]
---

# MakeWPFast Benchmark API

Answer questions about the **real, measured** performance impact of WordPress plugins and
themes using the bundled `mwf-bench` CLI. Each plugin/theme has a speed grade plus TTFB,
memory, and query deltas measured in three contexts (activation, homepage, wp-admin) against
a clean WordPress baseline.

The API is **paid and quota-limited**. The CLI protects the user's quota with a local cache,
name→slug resolution, and batch guards — so **always delegate to the CLI; never hand-write
`curl`**. Treat the CLI as the only way to touch the API.

## Setup (once)

The CLI needs an API key (subscribe at https://makewpfast.com/api/). It is read from, in order:
`MWF_API_KEY` env var → macOS keychain → `~/.config/makewpfast/key`.

- If no key is configured, the CLI prints a subscribe link and exits. Relay that to the user.
- To store a key: `scripts/mwf-bench auth` (prompts, never echoes), or `export MWF_API_KEY=...`.

## Usage

Run the CLI at `scripts/mwf-bench` (relative to this skill). Parse its stdout. Add
`--format json` when you need structured data to reason further; the default text output is
already human-readable.

| Goal | Command |
|------|---------|
| One plugin | `mwf-bench lookup "WooCommerce"` |
| One theme | `mwf-bench lookup astra --theme` |
| Compare several | `mwf-bench compare wordpress-seo seo-by-rank-math` |
| Quota / tier (free) | `mwf-bench me` |
| Just the slug | `mwf-bench resolve "Yoast SEO"` |
| Audit a local site | `mwf-bench audit --path /path/to/wp --top 10` |

Accepts plain names ("WooCommerce", "Yoast SEO") or exact slugs. The CLI resolves names to
WordPress.org slugs for free before spending any paid quota.

## Rules (protect the user's quota)

- **Never write raw curl.** Every API interaction goes through `mwf-bench`.
- **Prefer `compare` over multiple `lookup` calls** when the user names several plugins.
- **Don't re-query a slug already fetched this session** unless the user says the data is stale
  (add `--refresh` only then). Cached rows are free and printed as "(cached, N days old)".
- **For broad / site-wide asks, run `mwf-bench me` first** to show remaining quota, then use
  `audit` (it benchmarks only active, heaviest plugins) rather than looping over everything.
- **If the CLI returns "Ambiguous" candidates (exit 3), stop and ask the user which one** before
  spending quota — do not guess the slug from training data.
- **A 404 means the slug isn't in the dataset** (`not in dataset`); `benchmarked: false` means
  the slug is known but not yet measured. Report these honestly; don't invent numbers.
- On 401/403/429 the CLI prints the subscribe/upgrade link — relay it, don't retry.

## Interpreting results

- **Speed grade** A–F (+ numeric 0–100) is computed from activation memory + query deltas.
  Higher numeric = faster/lighter.
- **Deltas** are vs a clean WP baseline: TTFB in ms, memory in KB, queries are raw counts. A
  context can be `null`/`not measured` (e.g. an admin-only plugin has no homepage row) — treat
  null as "not measured", not "zero impact".
- Suggesting faster alternatives is *your* job after seeing the numbers — the API has no search
  endpoint, so propose alternatives, then verify them with another `compare`.

See `references/api.md` for the full field/status reference and `references/examples.md` for
worked prompt→command examples.
