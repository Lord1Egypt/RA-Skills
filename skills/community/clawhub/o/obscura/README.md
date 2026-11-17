# obscura-skill

An agent skill for [obscura](https://github.com/h4ckf0r0day/obscura) — a single-binary
Rust headless browser that speaks CDP, runs real JavaScript, and needs no Chrome or Node.

The skill covers the four ways in: `obscura fetch` (one page), `obscura scrape` (many
pages), `obscura serve` (CDP for Puppeteer/Playwright), and `obscura mcp` (38 `browser_*`
MCP tools for an agent). It is written for whichever agent framework reads `SKILL.md`.

Checked against **obscura 0.2.6** (macOS arm64, Homebrew build) on 2026-11-13. Every
command in `SKILL.md` was executed against that binary; `scripts/smoke.sh` runs the same
checks again so the skill can't silently rot.

## Why another one

The skill libraries carry obscura write-ups from the 0.1.x era. They are wrong about the
things that bite in 0.2.x:

- **Loopback and RFC1918 are blocked by default.** The SSRF guard kills every localhost
  dev-server or E2E flow until you pass `--allow-private-network`.
- **`obscura mcp` exists.** 38 tools, stdio or HTTP — the shortest path from "agent that
  can read pages" to "agent that can click through them".
- **`--selector` and `--eval` do not combine.** With both, the eval is dropped silently.
- **`--dump markdown` is a raw DOM→MD pass**, not readability extraction.
- **The Homebrew build has no stealth feature**, so `--stealth` there is JS-side only.

## Install

Hermes:

```bash
git clone https://github.com/bevisy/obscura-skill ~/.hermes/skills/obscura
```

Claude Code:

```bash
git clone https://github.com/bevisy/obscura-skill ~/.claude/skills/obscura
```

Other agents: point `AGENTS.md` (or your project's instructions file) at `SKILL.md`, or
paste `SKILL.md` into the system prompt when the task is page work.

For the MCP route you don't need the skill at all — just the binary:

```bash
hermes mcp add obscura -- obscura mcp
```

## Layout

```
SKILL.md                     the skill itself: surfaces, flags, pitfalls
references/cli.md            verbatim `--help` for 0.2.6 (regenerate, don't edit)
references/mcp-tools.md      the 38 MCP tools with parameter names
references/upstream-docs.md  index of obscura's own 22 docs
scripts/smoke.sh             re-verifies every claim; --dump-help regenerates cli.md
```

## Verify

```bash
brew install obscura && ./scripts/smoke.sh
```

Exit code 0 means the skill still matches the binary. A failure names the claim that
broke, which is the thing to fix before trusting it again.

## License

MIT for this skill. Obscura itself is Apache-2.0 and lives at
[h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura); the upstream docs index
links there rather than copying its text.
