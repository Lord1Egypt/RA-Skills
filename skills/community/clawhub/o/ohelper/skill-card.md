## Description:

Manage and maintain OpenClaw chat sessions by helping compact context, start fresh sessions, or reset session state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage long or stale chat sessions by choosing whether to compact context, start a new session, or reset current session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reset actions can disrupt the current session context.

Mitigation: Confirm what context may be cleared before using /reset, and reserve /compact or /new for cases where the user explicitly accepts the session change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/ohelper)
- [ClawHub publisher profile](https://clawhub.ai/user/goog)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces session-maintenance recommendations and confirmation-gated commands for OpenClaw sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
