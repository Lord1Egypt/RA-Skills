## Description:

IS-IS protocol analysis with adjacency diagnosis, LSPDB analysis, level 1/2 routing validation, and NET address verification across Cisco IOS-XE, Juniper JunOS, and Arista EOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and operators use this skill to diagnose IS-IS adjacency formation, LSP database consistency, level 1/2 routing behavior, NET address uniqueness, and post-change routing health. It supports read-only troubleshooting workflows for Cisco IOS-XE, Juniper JunOS, and Arista EOS environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting inputs and reports may include sensitive network topology, hostnames, addresses, or authentication details.

Mitigation: Use read-only device accounts where possible and avoid pasting secrets or unnecessary sensitive details into prompts or reports.

Risk: Diagnostic conclusions may be wrong if expected topology, vendor behavior, or configured IS-IS levels are incomplete or inaccurate.

Mitigation: Validate recommendations against documented topology, device configuration, and vendor documentation before making network changes.

## Reference(s):

- [IS-IS CLI Reference - Cisco / JunOS / EOS](references/cli-reference.md)
- [IS-IS Adjacency State Machine and LSPDB Flooding](references/state-machine.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/isis-analysis)
- [ClawHub Publisher Profile](https://clawhub.ai/user/vahagn-madatyan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with read-only vendor CLI command blocks and structured report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic reasoning and recommendations; does not execute commands itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
