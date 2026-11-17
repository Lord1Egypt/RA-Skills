## Description:

Use KaspaCom Lending through the KaspaCom DeFi MCP/CLI for market discovery, position checks, and lending actions like supply, borrow, and repay on IGRA and Kasplex environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marciano147](https://clawhub.ai/user/marciano147)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect KaspaCom lending markets and wallet positions, then prepare lending actions such as supply, borrow, and repay through the KaspaCom DeFi MCP/CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide fund-affecting lending actions such as supply, borrow, and repay.

Mitigation: Require manual review of wallet, network, token, amount, and transaction payload before executing any lending action.

Risk: The skill installs and uses a global npm package for KaspaCom DeFi operations.

Mitigation: Pin and verify the npm package before installation, and avoid installing or running it with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marciano147/skills/kaspacom-lending-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for market discovery, wallet position checks, and human-reviewed lending transaction preparation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
