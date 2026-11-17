## Description:

Use when updating ProxyGate CLI or SDK to the latest version, including when an update notification is shown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check the installed ProxyGate CLI version, compare it with the npm-published version, and update the CLI, SDK dependency, installed skills, and update cache when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update global npm tooling, project dependencies, installed Claude Code skills, and a local update-check cache.

Mitigation: Require explicit confirmation before install, delete, or cache-modifying commands; prefer exact reviewed versions instead of @latest where operationally possible.

Risk: The broader ProxyGate command reference includes API keys, Solana wallet keypairs, deposits, withdrawals, and escrow operations.

Mitigation: Treat credentials and financial commands as sensitive; review command arguments carefully and use dry-run modes for financial flows when available.

Risk: Refreshing installed skills can introduce behavior changes outside the current project.

Mitigation: Review and scan skill changes before deployment or continued use.

## Reference(s):

- [ProxyGate CLI Command Reference](references/commands.md)
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command snippets and JSON update-check status from the checker script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update global npm tooling, project dependencies, installed Claude Code skills, and a local update-check cache.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
