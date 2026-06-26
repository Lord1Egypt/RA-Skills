# Microsoft Commercial Marketplace Notes

Product name: One Person Company OS

Version: 1.0.3

Marketplace positioning:

One Person Company OS helps a solo founder build and maintain a visual operating cockpit for an AI-native one-person company. The cockpit keeps the founder focused on promise, buyer, product capability, delivery, cash, learning, assets, the current bottleneck, and today's shortest action.

Package layers:

- Copilot Studio agent instructions: `agent-instructions.md`
- Teams app manifest draft: `teams-app-manifest.template.json`
- Backend/action schema recommendation: reuse `platforms/openai-gpt/actions-openapi.yaml`
- Canonical local package: repository root and `platforms/mcp-server/`

Commercial Marketplace boundary:

- Copilot Studio publication makes a tenant agent available only after the tenant/admin flow is complete.
- Commercial Marketplace submission must use the supported Microsoft 365 Agents Toolkit / Partner Center package path.
- Do not describe this adapter as marketplace-ready until the app package, responsible AI checks, support/compliance assets, and Partner Center review are complete.

Tenant requirements:

- Microsoft tenant
- Copilot Studio license
- admin approval for connectors and Teams publication
- Microsoft Partner Center / Commercial Marketplace publisher account
- Microsoft 365 Agents Toolkit package path for Commercial Marketplace submission
- privacy, support, compliance, and listing assets required by the marketplace

Safety and compliance notes:

- Do not claim files were saved unless a connector or backend action confirms it.
- Do not request unrelated credentials.
- Keep generated content inside approved tenant storage or founder-approved workspace locations.
- Ask for founder approval before legal, pricing, budget, launch, or risky customer-facing actions.
- Treat AI images as optional creative assets, not exact operating records.

Published evidence required:

- Copilot Studio agent URL or tenant-visible record
- Teams app package record if submitted to Teams
- Commercial Marketplace offer URL or review record
- visible version or package date
