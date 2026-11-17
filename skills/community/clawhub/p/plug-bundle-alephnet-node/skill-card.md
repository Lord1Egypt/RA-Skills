## Description:

Bundles four Security skills into a coordinated workflow for security audit, data collection, file scanning, result analysis, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident response teams, compliance analysts, and developers can use this plug to coordinate the bundled Security skills for audit, scanning, log review, incident response, and consolidated reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release as suspicious because it requests broad read, write, command, and API capabilities while leaving scope and data-flow boundaries unclear.

Mitigation: Review before installing, use only in a controlled audit environment, confirm which member skills will be installed, and verify command, file-write, and data-transfer boundaries before use.

Risk: Audit workflows may expose sensitive production secrets, logs, network captures, or broad filesystem paths.

Mitigation: Do not submit production secrets or unrestricted paths until required credentials, inputs, and retention behavior are understood; use least-privilege credentials and sanitized test data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-bundle-alephnet-node)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code examples, configuration notes, and security reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include synthesized findings from multiple bundled skills; review generated commands and file operations before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
