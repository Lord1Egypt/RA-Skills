# openclaw-skill-hubspot-by-altf1be

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![HubSpot](https://img.shields.io/badge/HubSpot-API-orange.svg)](https://developers.hubspot.com/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-hubspot--by--altf1be-orange)](https://clawhub.ai/skills/hubspot-by-altf1be)
[![Security](https://img.shields.io/badge/Security_Scan-Benign-green)](https://clawhub.ai/skills/hubspot-by-altf1be)
[![GitHub last commit](https://img.shields.io/github/last-commit/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be/issues)
[![GitHub stars](https://img.shields.io/github/stars/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be/stargazers)

Full HubSpot platform CLI covering CRM, CMS, Marketing, Conversations, and Automation.

By [Abdelkrim BOUJRAF](https://www.alt-f1.be) / ALT-F1 SRL, Brussels 🇧🇪 🇲🇦

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Commands](#commands)
- [Security](#security)
- [API Coverage](#api-coverage)
- [ClawHub](#clawhub)
- [License](#license)
- [Author](#author)
- [Contributing](#contributing)

## Features

- **CRM** — Full CRUD for contacts, companies, deals, tickets. Plus owners, pipelines, associations (v4), properties, and engagements (notes, emails, calls, tasks, meetings)
- **CMS** — Blog posts (CRUD), site pages, domains
- **Marketing** — Email campaigns, forms, marketing emails with stats, contact lists
- **Conversations** — Inbox threads and messages
- **Automation** — Workflows list and details
- **Auth** — Private App token (simple) or OAuth 2.0 with auto-refresh (advanced)
- **Security** — `--confirm` required for deletes, no secrets to stdout, rate-limit retry with backoff

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ALT-F1-OpenClaw/openclaw-skill-hubspot-by-altf1be.git
cd openclaw-skill-hubspot-by-altf1be

# 2. Install
npm install

# 3. Configure
cp .env.example .env
# Edit .env with your HubSpot Private App token

# 4. Use
node scripts/hubspot.mjs contacts list
node scripts/hubspot.mjs deals read --id 42
node scripts/hubspot.mjs companies create --name "Acme Corp"
```

## Setup

1. Go to HubSpot Settings > Integrations > Private Apps
2. Create a Private App and copy the access token
3. Copy `.env.example` to `.env` and fill in:
   - `HUBSPOT_ACCESS_TOKEN` — your Private App token
4. Run `npm install`

### OAuth 2.0 (alternative)

For OAuth, set `HUBSPOT_CLIENT_ID`, `HUBSPOT_CLIENT_SECRET`, and `HUBSPOT_REFRESH_TOKEN` instead. When `HUBSPOT_CLIENT_ID` is set, OAuth mode is activated automatically.

### Prerequisites

- Node.js >= 18
- HubSpot account with API access
- Private App token or OAuth credentials (see [Setup](#setup))

## Commands

See [SKILL.md](./SKILL.md) for full command reference with examples.

### 50+ commands across 16 entities:

| Entity | Commands |
|--------|----------|
| Contacts | `list`, `search`, `create`, `read`, `update`, `delete` |
| Companies | `list`, `search`, `create`, `read`, `update`, `delete` |
| Deals | `list`, `search`, `create`, `read`, `update`, `delete` |
| Tickets | `list`, `search`, `create`, `read`, `update`, `delete` |
| Owners | `list`, `read` |
| Pipelines | `list` |
| Associations | `list`, `create`, `delete` |
| Properties | `list` |
| Engagements | `notes`, `emails`, `calls`, `tasks`, `meetings` |
| Blog Posts | `list`, `read`, `create`, `update` |
| Pages | `list`, `read` |
| Domains | `list` |
| Email Campaigns | `list`, `read` |
| Forms | `list`, `read` |
| Marketing Emails | `list`, `read`, `stats` |
| Contact Lists | `list`, `read` |
| Conversations | `list`, `read` |
| Messages | `list` |
| Workflows | `list`, `read` |

## Security

- Bearer token (Private App) or OAuth 2.0 authentication with auto-refresh
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Built-in rate limiting with exponential backoff retry (3 attempts)
- OAuth token cache: `~/.cache/openclaw/hubspot-token.json`
- Lazy config validation (only checked when a command runs)

## API Coverage

See [docs/API-COVERAGE.md](./docs/API-COVERAGE.md) for a full breakdown of supported vs unsupported API resources.

## ClawHub

Published as: `hubspot-by-altf1be`

```bash
clawhub install hubspot-by-altf1be
```

## License

MIT — see [LICENSE](./LICENSE)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
- GitHub: [@abdelkrim](https://github.com/abdelkrim)
- X: [@altf1be](https://x.com/altf1be)

## Contributing

Contributions welcome! Please open an issue or PR.
