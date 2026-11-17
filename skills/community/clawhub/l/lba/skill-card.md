## Description:

Automate Linear.app workflows in the OpenClaw-managed browser profile using browser tool actions for triage, issue updates, comments, filtering, bulk state changes, and visual verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hassam-powerhouse](https://clawhub.ai/user/hassam-powerhouse)

### License/Terms of Use:


## Use Case:

Developers, project managers, and operations teams use this skill to perform user-directed Linear issue workflows through an authenticated OpenClaw browser session. It is suited for creating, editing, commenting on, moving, filtering, triaging, and visually verifying Linear issues when the user provides the required issue context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify business data in a user's Linear workspace through issue creation, edits, comments, state changes, bulk triage, or destructive actions.

Mitigation: Review requested changes before execution; the skill requires explicit details for issue targets, confirmation for create and bulk workflows, and explicit confirmation for destructive actions.

Risk: The skill operates through a logged-in OpenClaw browser profile, so actions run with the user's active Linear permissions.

Mitigation: Install and use it only when the agent should operate Linear through that browser session, and verify the post-action snapshot or completion report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hassam-powerhouse/skills/lba)
- [Linear](https://linear.app/)
- [Linear Browser Workflows](references/workflows.md)
- [Selectors and Fallbacks](references/selectors-and-fallbacks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status reports, confirmation prompts, browser action guidance, and visible-state verification summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the OpenClaw-managed browser profile and authenticated Linear session when available.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
