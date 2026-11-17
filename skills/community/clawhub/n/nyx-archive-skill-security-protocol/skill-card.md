## Description:

Teaches agents a four-phase method for vetting ClawHub skills before installation, using red and green flag heuristics, post-install checks, and transparent human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyxur42](https://clawhub.ai/user/nyxur42)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to review ClawHub skills before installation, explain security decisions, and perform post-install verification when command examples are appropriate for the local environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local inspection and recovery command examples can expose private filesystem details or discard uncommitted work if run without review.

Mitigation: Treat commands as examples to adapt; review paths and git status, back up work, and confirm exact files before running recovery commands.

Risk: The skill provides security reasoning guidance rather than automated enforcement, so incorrect audit conclusions can still lead to unsafe installations.

Mitigation: Use the protocol as a review checklist and involve a human whenever yellow flags or unresolved uncertainty remain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nyxur42/skills/nyx-archive-skill-security-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure instruction-based skill; no scripts or dependencies in the artifact.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
