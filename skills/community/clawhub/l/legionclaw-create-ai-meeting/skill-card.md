## Description:

Creates intelligent meetings for users in LegionClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

LegionClaw agents use this skill to create an intelligent meeting for the current user, deriving the meeting user identifier from trusted runtime session metadata and returning the meeting number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity handling is under-scoped for creating account-linked meeting resources.

Mitigation: Derive the meeting userId only from trusted LegionClaw runtime metadata and avoid accepting arbitrary user-provided identifiers except through an authorized admin workflow.

Risk: Full session identifiers or internal agent identifiers could be exposed in model-visible text.

Mitigation: Avoid displaying full session identifiers by default and keep user-facing errors free of raw service URLs or internal identifiers.

Risk: Unvalidated identifiers could produce incorrect or unauthorized meeting creation requests.

Mitigation: Strictly validate and URL-encode the identifier before issuing the meeting creation request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/legionspace-hackathon/skills/legionclaw-create-ai-meeting)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with optional Markdown and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a meeting creation success or failure message and avoids exposing full session identifiers by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
