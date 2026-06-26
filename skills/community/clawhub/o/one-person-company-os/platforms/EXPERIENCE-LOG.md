# Experience Log

Updated: 2026-05-06

## Lessons

- A single `SKILL.md` package cannot be uploaded unchanged to every market.
- Keep one canonical implementation and generate thin adapters for each platform.
- MCP should be the shared execution layer; prompt-only markets should link to or describe the MCP/API bridge.
- Browser-only marketplaces cannot be published by automation without account sessions and approvals.
- CLI timeouts are not proof of failure. Verify using version APIs and downloadable packages.
- Capability labels on registry sites may be inferred from text and historical metadata; check scan verdicts separately from marketing tags.
- The mainstream push list should be the primary planning surface, not a scattered inventory of directories.
- `ready-to-submit`, `backend-needed`, and `tenant-needed` are useful statuses because they prevent local packaging from being mistaken for publication.

## Platform Mapping

- Full local execution: OpenClaw, Claude Skills, Hermes Agent, MCP clients.
- MCP registry distribution: MCP Registry, Smithery, Glama, PulseMCP.
- Hosted/API execution: OpenAI GPT Actions, GitHub Copilot Extension, Microsoft Copilot Studio, Dify.
- Prompt-only/guided execution: Poe, Gemini Gems, basic GPT/Gem without Actions.
- Marketplace listing layer: ClawHub, agentskills.io, Dify Marketplace, GitHub Marketplace, Microsoft Commercial Marketplace, Poe, Gemini, GPT Store.

## Safety Pattern

For every platform listing:

1. State that normal use does not need API keys.
2. State that files are written only inside the founder-approved workspace.
3. State that system packages are not auto-installed.
4. State that high-risk actions require founder approval.
5. Provide a first-run prompt that asks for promise, buyer, core problem, and workspace path.
