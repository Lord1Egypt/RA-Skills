---
name: propai-live
description: >
  PropAI Live is the complete AI-powered realtor automation suite, bundling OpenClaw core,
  PropAI Sync for WhatsApp lead management, Social Flow for Meta operations, and essential
  realtor skills for lead processing and AI assistance. It provides a unified CLI and UI for
  daily workflows, from lead follow-ups to social posting, with built-in risk management and
  approvals.
---

# PropAI Live

## Dependencies (auto-installed via ClawHub)

- openclaw
- propai-sync
- social-flow
- message-parser
- lead-extractor
- india-location-normalizer
- summary-generator
- action-suggester
- sentiment-priority-scorer
- lead-storage

## Core Workflow

For each session:
1. Validate environment: run `propai-live doctor`.
2. Validate license: run `node scripts/license-status.mjs`.
3. Parse intent: Lead (PropAI), Social (Social Flow), General (OpenClaw).
4. Propose commands: show plan, confirm for writes.
5. Execute minimal sequence, log outcomes.
6. On failure, diagnose and retry safe actions only.

## License Workflow

Run these from `skills/propai-live`:

```bash
node scripts/license-activate.mjs --key <LICENSE_KEY> --api <LICENSE_API_BASE_URL>
```

```bash
node scripts/license-status.mjs --mode read
```

Before any write operation:

```bash
node scripts/license-guard.mjs --mode write
```

Feature-specific gates:

```bash
node scripts/license-guard.mjs --mode write --require-entitlement lead-storage
node scripts/license-guard.mjs --mode write --require-entitlement social
```

For logout/device transfer:

```bash
node scripts/license-deactivate.mjs
```

## Validate Environment

Before operations:
- `propai-live --version` (checks bundle)
- `propai-live doctor` (auth, connections)
- `node scripts/license-status.mjs --mode read` (license local check)

If issues are found, run `propai-live setup` for wizard.

## Domain Routing

- Lead/Messaging: `propai-live lead ...` (PropAI + skills)
- Social/Meta: `propai-live social ...` (Social Flow)
- AI/General: `propai-live ask ...` (OpenClaw)

## Execution Policy

- Prefer CLI commands over narration.
- Keep commands profile-aware (agency, city).
- Do not print secrets in output.
- Run doctor first on new setups.
- Run `node scripts/license-guard.mjs --mode write` before any write action.

## Risk Policy

- Read-only: safe (status, insights).
- Low-risk: drafts, test messages.
- High-risk: live spends, real user messages; require explicit confirmation.
- Unknown impact: treat as high-risk.

## Output Contract

- Summarize intent and chosen domain.
- List exact commands in code blocks.
- State assumptions (agency, contacts).
- Mark risk levels.
- Ask confirmation before writes.

## References

- PropAI docs: `propai-sync/README.md`
- Social Flow docs: `social-flow/README.md`
- OpenClaw docs: `https://openclaw.ai`
- License API contract: `references/license-api-contract.md`
- License API starter template: `assets/license-api/`
