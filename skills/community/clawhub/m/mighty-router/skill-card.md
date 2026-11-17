## Description:

Enforces risk-based coding profiles, impact mapping, adversarial planning, and strict verification gates before making edits, audits, or structural modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnymaconny](https://clawhub.ai/user/johnnymaconny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to classify coding, audit, research, verification, and high-risk edit workflows into risk-based execution profiles before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly governs coding, audit, research, verification, and high-risk edit workflows across a session.

Mitigation: Install it only when that session-wide workflow control is intentional, and review whether its profile rules match the workspace's expected operating process.

Risk: Workspace `.mightyrc` or `.mighty.json` files can affect high-risk path classification.

Mitigation: Inspect any workspace Mighty configuration before use and confirm that listed high-risk paths are appropriate for the project.

## Reference(s):

- [Mighty Router on ClawHub](https://clawhub.ai/johnnymaconny/skills/mighty-router)
- [johnnymaconny ClawHub profile](https://clawhub.ai/user/johnnymaconny)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown instructions and structured response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require profile-specific verification summaries or forensic XML sections for high-risk workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
