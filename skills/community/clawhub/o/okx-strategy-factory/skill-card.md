## Description:

Okx Strategy Factory coordinates a five-agent pipeline to develop, backtest, deploy, publish, and iterate OKX OnchainOS on-chain trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synththoughts](https://clawhub.ai/user/synththoughts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to coordinate specialist agents that turn a trading idea into strategy code, configuration, risk controls, backtest reports, deployment actions, and release packaging. It is intended for OKX OnchainOS workflows that need strict phase gates across development, validation, production deployment, publishing, and post-live review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live on-chain trading using OKX credentials and wallet signing.

Mitigation: Use an isolated workspace, least-privilege OKX keys, a limited test wallet, and explicit human confirmation before any signing or funded-wallet action.

Risk: The workflow can deploy strategy processes to a VPS and publish releases to GitHub.

Mitigation: Require manual approval before production deployment, git push, tag creation, or GitHub release, and verify rollback and health-check results before continuing.

Risk: Generated strategy skills and reference files may be treated as authoritative by downstream agents.

Mitigation: Audit generated skills, configuration, risk profiles, and reference files before installation or reuse.

Risk: Installer and runtime dependencies can change over time.

Mitigation: Pin installer versions and validate OnchainOS CLI compatibility in dry-run mode before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synththoughts/skills/okx-strategy-factory)
- [README](artifact/README.md)
- [onchainos CLI interface reference](artifact/references/api-interfaces.md)
- [Risk profile schema](artifact/references/risk-schema.json)
- [Strategy lessons reference](artifact/references/strategy-lessons.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with generated files, JSON configuration, code, reports, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized by strategy name and version with gate-driven state tracking.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
