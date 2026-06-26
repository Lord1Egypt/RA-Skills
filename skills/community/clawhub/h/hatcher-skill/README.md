# hatcher-skill

Machine-readable skill files for [Hatcher](https://hatcher.host) — a managed hosting platform for AI agents. Give your AI agent the URL `https://hatcher.host/skill.md` and it will know how to register, create agents, configure integrations, and handle payments on the platform.

## What's in this repo

| File | Purpose |
| --- | --- |
| [`skill.md`](./skill.md) | Entry point: index + hello-world flow + user-agent convention |
| [`auth.md`](./auth.md) | Register, email verify polling, API keys |
| [`agents.md`](./agents.md) | Frameworks, templates (199 available), create/configure/lifecycle |
| [`pricing.md`](./pricing.md) | Tiers, addons, payment rails (credits / Stripe / SOL / USDC / HATCHER) |
| [`integrations.md`](./integrations.md) | Telegram, Discord, Twitter, WhatsApp, Slack setup |

## Canonical URLs

The canonical source is this GitHub repo. Hatcher mirrors content at:

- `https://hatcher.host/skill.md`
- `https://hatcher.host/.well-known/skill.md`
- `https://hatcher.host/skill/auth.md` (and `/agents.md`, `/pricing.md`, `/integrations.md`)

Changes to this repo automatically trigger a rebuild of the hatcher.host serving layer via GitHub Actions.

## Contributing

PRs welcome. All curl examples are linted via shellcheck; URLs are validated weekly. Breaking changes bump the major version in `CHANGELOG.md` and in each file's YAML front-matter.

## License

MIT — see [LICENSE](./LICENSE).
