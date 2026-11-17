## Description:

Use KaspaCom LFG Launchpad through the KaspaCom DeFi MCP/CLI for launch discovery and launch-token trading on IGRA and Kasplex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marciano147](https://clawhub.ai/user/marciano147)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to discover active KaspaCom LFG launches and guide launch-token buy or sell flows through the KaspaCom DeFi MCP/CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may run launch-token buy or sell commands that have financial impact.

Mitigation: Require explicit operator confirmation before any buyLaunchToken or sellLaunchToken command is executed.

Risk: The artifact recommends a global npm install without package version pinning.

Mitigation: Pin and verify the npm package version, and avoid elevated or global installs where possible.

Risk: Wallet-connected command execution can expose funds or credentials if used without review.

Mitigation: Prefer read-only launch discovery until the package, wallet setup, command arguments, and network are reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only launch discovery examples and transaction command examples that require operator review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
