# obscura-skill

A Claude Code skill that teaches Claude how to use [**Obscura**](https://github.com/h4ckf0r0day/obscura) — the open-source, Rust-based, drop-in headless Chrome replacement for AI agents and web scraping.

> Lightweight (~30 MB), stealthy, and Puppeteer/Playwright compatible via the Chrome DevTools Protocol.

## What this skill does

When loaded into Claude Code, this skill triggers automatically whenever the user mentions:

- Web scraping, headless browser, JS rendering
- Puppeteer / Playwright / CDP
- Anti-bot, anti-detection, fingerprinting
- Parallel page fetching
- The `obscura` CLI itself

It then guides Claude on how to install Obscura, pick the right command (`fetch` / `scrape` / `serve`), enable stealth mode, connect Puppeteer or Playwright over CDP, and avoid common anti-patterns.

## Install

### Option 1 — `npx skills`

```bash
npx skills add git@github.com:FelipeOFF/obscura-skill.git
```

### Option 2 — Manual

```bash
git clone https://github.com/FelipeOFF/obscura-skill.git ~/.claude/skills/obscura
```

Then restart Claude Code (or reload skills) and the `obscura` skill becomes available.

## Verify

Inside Claude Code, ask:

> "Como faço scraping de uma SPA pesada de JavaScript?"

Claude should invoke the `obscura` skill and recommend `obscura fetch ... --wait-until networkidle0` (or `obscura serve` + Puppeteer for multi-step flows).

## What's inside

| File | Purpose |
|---|---|
| `SKILL.md` | The skill itself — frontmatter + installation + usage + CLI reference |
| `README.md` | This file — how to install and verify the skill |
| `LICENSE` | MIT |

## About Obscura

Obscura is **not** built or maintained by me. It's an Apache 2.0 project by [h4ckf0r0day](https://github.com/h4ckf0r0day). This repo only packages a Claude Code skill that knows how to use it.

- Upstream repo: https://github.com/h4ckf0r0day/obscura
- Releases (prebuilt binaries): https://github.com/h4ckf0r0day/obscura/releases

## License

MIT — for the skill files in this repo. Obscura itself is Apache 2.0.
