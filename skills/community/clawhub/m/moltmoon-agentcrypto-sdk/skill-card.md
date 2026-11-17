## Description:

Guides agents through installing, configuring, and operating the MoltMoon SDK/CLI V2 on Base mainnet for token launches, trades, rewards, migration, troubleshooting, and production runbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chillbruhhh](https://clawhub.ai/user/chillbruhhh)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run MoltMoon SDK and CLI workflows for Base mainnet token launches, dry-runs, quote checks, buys, sells, rewards claiming, migration, and operational troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm execution can run a changed SDK version after review.

Mitigation: Use only a pinned, reviewed @moltmoon/sdk version in an isolated environment before executing commands.

Risk: Raw private keys and live Base mainnet write commands can expose funds or execute unintended transactions.

Mitigation: Avoid command-line private keys, use a low-balance operational wallet, and require explicit human review of chain, signer, amounts, approvals, and transaction calldata before live writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chillbruhhh/skills/moltmoon-agentcrypto-sdk)
- [MoltMoon API endpoint](https://api.moltmoon.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, environment configuration, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational runbooks, validation rules, failure diagnosis, and signer safety guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
