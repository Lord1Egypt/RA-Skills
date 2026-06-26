# majia-meeting-svg

[![skills.sh](https://skills.sh/b/maojiebc/majia-meeting-svg)](https://skills.sh/maojiebc/majia-meeting-svg)

> **SVG 会议纪要卡片 · 马甲实战版** (SVG Meeting Card · Majia Real-World Edition)

A Claude Code Skill that turns a multi-party meeting transcript into a single phone-friendly SVG summary card — auto-converted to PNG so it can be forwarded directly inside WeChat / DingTalk / Feishu and other IM channels.

> 🇨🇳 Chinese readers: see [README.md](./README.md) for the full Chinese documentation.

## What it does

Feed in a meeting recording transcript / verbatim, get back a structured SVG card — color-blocked modules, checkbox-style action items, milestone timeline. Everyone in the meeting gets the *same* card; a 30-second scan tells them "what was decided, who does what, when".

**Input**: multi-party meeting transcript / speech-to-text dump
**Output**: SVG file + PNG image (2x Retina, generated automatically)

## Install

```bash
# GitHub CLI (recommended)
gh skill install maojiebc/majia-meeting-svg

# skills.sh
npx skills add maojiebc/majia-meeting-svg

# Manual clone
git clone https://github.com/maojiebc/majia-meeting-svg.git ~/.claude/skills/majia-meeting-svg
```

## Usage

```bash
/majia-meeting-svg path/to/transcript.txt
/majia-meeting-svg   # then paste the transcript inline
```

## Examples

The [`references/examples/`](references/examples/) directory contains five sanitized examples (SVG + PNG) covering different meeting scenarios:

| Scenario | Preview |
|------|------|
| **Cross-brand alignment** — first-time collaboration between two brands, resource alignment and ownership | <img src="references/examples/example-cross-brand.png" width="280" /> |
| **Store campaign plan** — single-store promo mechanic confirmation and action items | <img src="references/examples/example-campaign-plan.png" width="280" /> |
| **CRM dev requirements review** — brand owner / tech vendor requirements review | <img src="references/examples/example-crm-dev-review.png" width="280" /> |
| **Payment integration** — three-party technical integration plan (includes a technical flow diagram) | <img src="references/examples/example-payment-integration.png" width="280" /> |
| **Regional ops sync** — HQ / regional multi-topic alignment | <img src="references/examples/example-regional-ops.png" width="280" /> |

## Visual style

- Color-blocked modules (red / blue / green / orange / purple / gray)
- White card with clear typographic hierarchy
- Checkbox-style action list, grouped by owner
- Timeline marks key milestones
- Callouts for risks and key decisions
- Rounded corners, generous whitespace, phone-first layout

## 👤 Author / Contact

**Majia (@maojiebc)** · 超级马甲 (Super Majia)

If this skill helps you, find me on any of these channels — happy to chat about field experience, take feature requests, hear bug reports, or trade notes on user operations / data platforms / BI engineering work:

| Channel | Link |
|---|---|
| 📧 Email | [m9224@163.com](mailto:m9224@163.com) |
| 🐙 GitHub | [github.com/maojiebc](https://github.com/maojiebc) |
| 🪝 ClawHub | [clawhub.ai/p/maojiebc](https://clawhub.ai/p/maojiebc) |
| 🐦 X | [@maojiebc](https://x.com/maojiebc) |
| 📕 Xiaohongshu | [Super Majia](https://xhslink.com/m/4fQMJeHHWKC) |
| 📰 WeChat Official Account | **超级马甲** |

> Built from 14 years of user-operations work and field-tested team coordination workflows.

## License

MIT
