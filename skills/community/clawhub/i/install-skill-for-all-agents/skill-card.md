## Description:

Install or upgrade a ClawHub skill and promote the global copy under the machine's OpenClaw home skills directory as the source of truth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or update one ClawHub skill through OpenClaw, promote it into the global skills directory, and verify the installed version and origin metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently replace global OpenClaw skills.

Mitigation: Review the target slug and version before running, keep backups before replacement, and verify the global origin metadata after promotion.

Risk: Path-derived file operations may affect unexpected OpenClaw directories if flags or environment variables are untrusted.

Mitigation: Use trusted, simple skill slugs and agent names, verify the resolved OpenClaw home path, and avoid untrusted input for flags or environment variables.

## Reference(s):

- [Script Notes](artifact/references/scripts.md)
- [ClawHub Skill Page](https://clawhub.ai/kadbbz/skills/install-skill-for-all-agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the target slug, global path, installed version, install or update method, backup path, staging cleanup state, and blockers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
