## Description:

A disciplined, reproducible workflow for AI agents to log decisions, create rollback snapshots, and generate briefings for any change or feature implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tstokes06](https://clawhub.ai/user/tstokes06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to structure change work by recording decisions, taking rollback snapshots, maintaining TODO notes, and producing implementation briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback snapshots may preserve sensitive workspace data if secrets or private files are copied into them.

Mitigation: Review snapshot scope before copying files and exclude secrets or private data unless retention is intended.

Risk: Restoring a snapshot directly over an active workspace can overwrite newer work.

Mitigation: Restore into a temporary location or create a fresh backup before copying restored files into the active workspace.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON schemas and shell-style command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces workflow instructions and file-format examples; it does not require credentials or extra binaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
