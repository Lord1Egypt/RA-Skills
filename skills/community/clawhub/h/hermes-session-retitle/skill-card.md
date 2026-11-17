## Description:

Bulk-rename Hermes session titles to a consistent format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesarjue](https://clawhub.ai/user/caesarjue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes users use this skill to inventory and normalize local Hermes session titles after bulk runs, scheduled jobs, or inconsistent automatic naming. It supports reviewable rename plans, backup records, and post-rename verification for title-only cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect a local Hermes session database and propose title changes based on session history.

Mitigation: Install it only for Hermes session title cleanup and review the generated rename plan before applying changes.

Risk: Bulk title changes can make session history harder to navigate if the proposed names are inaccurate or too broad.

Mitigation: Use the precheck and backup workflow, keep the printed backup output, and verify renamed counts after applying a plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caesarjue/skills/hermes-session-retitle)
- [Publisher profile](https://clawhub.ai/user/caesarjue)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with JSON rename plans and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reviewable rename plans, backup records, and verification summaries for Hermes session title changes.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
