## Description:

Trade prediction markets non-custodially via the official KashDAO CLI (@kashdao/cli), including market discovery, quotes, buy and sell trading with idempotency and high-value confirmation, portfolio review, webhook management, request tracing, and REST API or direct-to-chain modes from one binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwhdx](https://clawhub.ai/user/bwhdx)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to install and drive the KashDAO CLI for prediction-market discovery, quotes, trading, portfolio review, webhooks, and request tracing. It is suited to agent workflows that need stable shell commands and machine-readable JSON output from the Kash CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global npm package for a trading workflow.

Mitigation: Prefer a pinned, reviewed @kashdao/cli version before use.

Risk: The skill requires sensitive trading credentials and allows API endpoint overrides.

Mitigation: Start with a least-privilege revocable test key, avoid custom base URLs unless they are official Kash endpoints you control, and independently review CLI behavior before using valuable signer keys.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bwhdx/skills/kashdao-cli)
- [KashDAO CLI homepage](https://github.com/KashDAO/cli)
- [Kash CLI documentation](https://docs.kash.bot/developer-docs/cli)
- [Kash REST API overview](https://docs.kash.bot/developer-docs/rest-api/overview)
- [Kash API error catalog](https://docs.kash.bot/developer-docs/api-errors)
- [KashDAO CLI npm package](https://www.npmjs.com/package/@kashdao/cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with shell command examples and JSON output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent workflows should prefer --json, --quiet, --wait, and --auto-idempotency-key for stable machine-readable execution.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
