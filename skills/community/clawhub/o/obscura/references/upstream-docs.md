# Upstream docs index

Obscura maintains its own docs under `docs/` in the upstream repo (Apache-2.0).
Read those before inventing behaviour; this skill only distils the daily-use path
and the pitfalls measured on 0.2.6.

| Doc | Answers |
|---|---|
| [`Adding-a-CDP-method-or-Web-API.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Adding-a-CDP-method-or-Web-API.md) | Two recipes for the two most common extensions: a new CDP method, and a new JS Web API. |
| [`Architecture-overview.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Architecture-overview.md) | Obscura is a workspace of ten crates. |
| [`Build-from-source.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Build-from-source.md) | - Current stable Rust ([rustup.rs](https://rustup.rs)) |
| [`CDP-media.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/CDP-media.md) | `Emulation.setEmulatedMedia` accepts `prefers-color-scheme` and |
| [`CLI-reference.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/CLI-reference.md) | `--verbose`, `--proxy`, `--stealth`, `--obey-robots`, `--user-agent`, and |
| [`Configure-stealth-and-proxies.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Configure-stealth-and-proxies.md) | ```bash |
| [`Connect-Puppeteer-or-Playwright.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Connect-Puppeteer-or-Playwright.md) | Examples use Node.js ES modules. Save scripts with a `.mjs` extension. |
| [`Environment-variables.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Environment-variables.md) | Allow fetches to addresses in the SSRF deny-set. Off by default to block SSRF. The deny-set is defined once, in `is_forbidden_ip` (`crates/obscura-ssr |
| [`Extract-data.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Extract-data.md) | `--dump` formats the page output without writing JavaScript. |
| [`Installation.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Installation.md) | ```bash |
| [`Intercept-and-modify-requests.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Intercept-and-modify-requests.md) | CDP `Fetch.enable` lets you inspect, block, or modify every request the page makes. |
| [`Markdown-extraction.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Markdown-extraction.md) | `--dump markdown` converts the rendered page to markdown. |
| [`Persist-cookies-and-storage.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Persist-cookies-and-storage.md) | `--storage-dir` persists cookies and `localStorage` so they survive across runs. |
| [`README.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/README.md) | Official documentation for Obscura, maintained in this repository. |
| [`Run-in-production-at-scale.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Run-in-production-at-scale.md) | ```bash |
| [`Testing-and-debugging.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Testing-and-debugging.md) | ```bash |
| [`Use-as-a-Rust-library.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Use-as-a-Rust-library.md) | The `obscura` crate embeds the engine in a Rust program with a `Browser` / `Page` / `Element` API plus a cookie store, no CDP round-trips. It builds V |
| [`Use-the-MCP-server.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Use-the-MCP-server.md) | `obscura mcp` exposes obscura as a Model Context Protocol server so MCP-capable clients (Claude Desktop, Claude Code, etc.) can drive it. |
| [`Use-with-Playwright.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Use-with-Playwright.md) | Examples use Node.js ES modules. Save scripts with a `.mjs` extension. |
| [`Use-with-Puppeteer.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Use-with-Puppeteer.md) | Examples use Node.js ES modules. Save scripts with a `.mjs` extension. |
| [`Watch-agent-sessions-live.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Watch-agent-sessions-live.md) | Capture frames through the same CDP connection that drives the page. Separate |
| [`Your-first-fetch.md`](https://github.com/h4ckf0r0day/obscura/blob/main/docs/Your-first-fetch.md) | `obscura fetch` loads a URL, runs its JavaScript, and prints the result. |
