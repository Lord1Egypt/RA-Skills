# Marketing Engineer · Skill (English)

Turn marketing into an engineering system: **knowledge layer → business lines → ticket pipeline → human sign-off → data feedback loop**, plus a single-file **dashboard** you can open anytime.
No inspiration-driven content piles. Reusable structure makes every output stand on verified facts and fixed voice/brand rules.

Methodology credit: Shann Holmberg ([@shannholmberg](https://x.com/shannholmberg)) — *Marketing Engineer* (the X thread "this is my AI marketing engine" and the article *How to Become a Marketing Engineer*, with four building blocks: Context / Loops / Graphs / Harness). This project is the engineering practice and productization built on top of that theory.

---

## What it solves

AI can already write and design. What really breaks is three other things:

| Problem | How this fixes it |
|---|---|
| **Context drift**: the voice you set today wanders off in three days | A single citable `shared-knowledge/` pack of five files + the hard rule "no source, no writing" |
| **Standards not persisted**: every review made up on the spot = no standard | Protocols written into files (glossary, domain rules, pre-publish checklist); machine audits, humans only judge taste |
| **State invisible**: dozens of files, no idea which is at what stage | Single-file dashboard: left tree / right file list, date + status + click-to-read |

## 30-second start

After install, **no commands**. You talk, it runs:

```
"Build a marketing workspace for product X, with dashboard"
"Show me the overall status"
"Content updated, refresh the dashboard"
"Published this on WeChat, link is xxx"
```

Agent-side actions (normally run automatically by the agent; commands left for your cron or troubleshooting):

| Your intent | Script it runs |
|---|---|
| Build workspace | `scripts/init_workspace.py <dir> --product "<product>" --with-dashboard` |
| See overview | `scripts/serve_dashboard.py <workspace> 8799` → <http://127.0.0.1:8799/dashboard.html> |
| Refresh snapshot | `scripts/build_dashboard.py <workspace>` |
| Re-scan only | `scripts/scan_workspace.py <workspace>` |

Full usage in [`references/usage-manual.md`](references/usage-manual.md).

## Install

```bash
# Option 1: clone then copy into skills dir
git clone https://github.com/iguoguo/marketing-engineer.git
cp -r marketing-engineer ~/.workbuddy/skills/

# Option 2: download zip (no git)
# https://github.com/iguoguo/marketing-engineer/releases/download/v1.1.0/marketing-engineer-skill.zip
```

Only dependency is Python 3 (standard library), no third-party packages.

## Workspace after build

```
<workspace>/
├── README.md                  # workspace constitution (eight iron rules)
├── shared-knowledge/          # single citable source (fill this first)
│   ├── product-and-offer.md   # product facts: positioning, modules, official copy, offer, internal data
│   ├── positioning.md         # positioning & differentiation (incl. unverified hypotheses)
│   ├── brand-voice.md         # glossary / visual spec / domain rules / pre-publish self-check
│   ├── audience.md            # audience personas
│   └── channels.md            # channel list & grouped playbook
├── content/ geo-seo/ outbound/ competitor-intel/ launch-campaigns/ raw/
├── scripts/                   # dashboard trio
├── workspace-folders.json     # optional: custom folder notes
└── dashboard.html             # single-file dashboard, double-click to view
```

## Dashboard

- **Left tree / right file list**: folder notes appear once on the left; every file clickable (Markdown render, tables, code copy, image preview)
- **Status isn't guessed**: manual registry → publish ledger hit → file header `> 状态：待审核` → folder-rule fallback, four-level judgment
- **Two update modes**: realtime (local server, re-scans each open) / manual (rebuild static snapshot, works offline)
- **Light / Dark themes**; any `<section id="tab-xxx">` auto-becomes a Tab

## Doc index

| File | Content |
|---|---|
| [`SKILL.md`](SKILL.md) | Skill entry: interaction principles, quick start, workflow, eight iron rules, toolbox |
| [`references/usage-manual.md`](references/usage-manual.md) | Usage manual: three entry points, five-step launch, daily command cards, dashboard usage, troubleshooting |
| [`references/workspace-structure.md`](references/workspace-structure.md) | Folder template, file skeletons, folder semantics, status rules, channel matrix |
| [`references/workflow-content-production.md`](references/workflow-content-production.md) | Ticket-based content production pipeline |
| [`references/geo-playbook.md`](references/geo-playbook.md) | GEO / SEO: keyword research, AI-engine diagnostics, probes, KPIs |
| [`references/dashboard-playbook.md`](references/dashboard-playbook.md) | Dashboard design + dashboard engine (scripts / status / theme / pitfalls) |
| [`references/brand-consistency-audit.md`](references/brand-consistency-audit.md) | Brand voice audit — six-item checklist |

## Eight iron rules (never violate)

1. **Read before write**: must check `shared-knowledge/` before output; never fabricate channels, data, features
2. **Evidence trail**: facts carry source + date; unverified marked `[unverified]`, never into final
3. **Publish needs human approval**: ledger follows the actually-published online version
4. **Voice consistency**: terms / domains / free-tier wording uniform across channels; change triggers audit (internal board included)
5. **Secrets only in `.env`**, never in any asset or doc
6. **Output in place**: drafts / final / ledger stored per folder convention
7. **Sensitive boundary**: no named competitor disparagement; no concrete prices before pricing finalized
8. **Board is a view, not the source**: derived from ledger / tickets / channel table, never reversed as truth source

## Known boundaries

- If you only publish one post and don't plan to keep producing, don't install — cost is in startup, payoff is in compounding
- Empty knowledge layer → output immediately drops to generic AI level
- Dashboard is a view not a source; at thousands of files, reset snapshot budget

## License

MIT © 2026 iguoguo. See [LICENSE](LICENSE).

Methodology credit: Shann Holmberg ([@shannholmberg](https://x.com/shannholmberg)).

Practiced by the 2Ryun team · 2ryun.com
