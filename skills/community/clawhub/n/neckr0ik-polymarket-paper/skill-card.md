## Description:

Paper trading platform for Polymarket that helps users practice prediction-market trading with virtual money, strategy guidance, performance tracking, and leaderboards before risking real capital.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to run a local CLI paper-trading simulator for Polymarket-style prediction markets. It supports virtual accounts, simulated trades, portfolio review, leaderboards, analytics, and export workflows for practice before using real capital.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-file handling can be tricked into reading or overwriting JSON files outside the intended data folder.

Mitigation: Validate account IDs, constrain account file paths to the configured data directory, and avoid untrusted account identifiers or crafted account JSON files.

Risk: Generated account and trading-history files may contain private practice portfolio data.

Mitigation: Treat generated local files as private, review exports before sharing them, and avoid storing sensitive real-world financial information in simulator records.

Risk: Unvalidated monetary inputs can produce misleading paper-trading results.

Mitigation: Validate trade amounts and starting balances before use, including rejecting negative, non-finite, or otherwise malformed values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-polymarket-paper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CLI guidance, and code/configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The implementation can create local JSON account and trading-history files when its commands are executed.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
