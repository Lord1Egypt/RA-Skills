## Description:

Creates grounded, askable digital-human student orientation courses from institution-supplied handbooks, policies, and orientation materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Student-services staff, education teams, and their supporting agents use this skill to turn supplied orientation materials into an interactive digital-human course for incoming students. The course is intended to answer common new-student questions while keeping consequential or individual cases routed to offices named in the supplied materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser OAuth, uploads selected course materials, consumes existing course credits, and can publish links when requested.

Mitigation: Install and use it only when the user trusts PersonWise and intentionally authorizes the account, source materials, credit use, and requested access mode.

Risk: The update flow asks the agent to run opaque commands returned by the CLI or service after approval.

Mitigation: Review any printed update command before approving it, especially the command origin and requested action.

Risk: Orientation content can become misleading if source materials are incomplete, outdated, or do not cover individual student cases.

Mitigation: Ground course content only in supplied materials, include the source document and year, and route consequential individual questions to the named office.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-student-orientation)
- [PersonWise publisher profile](https://clawhub.ai/user/personwiseai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON course blueprints and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and structured inputs for creating a PersonWise digital-human course from selected source materials; final course creation depends on account authorization, available credits, and service responses.]

## Skill Version(s):

2.1.9 (source: server release metadata, created 2026-08-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
