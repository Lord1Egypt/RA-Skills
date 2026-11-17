## Description:

Enforce release discipline for AI agents and developers by preventing version spam, requiring quality checks before publishing, and maintaining a 24-hour cooldown between releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill as a release gatekeeper before publishing, deploying, or bumping versions. It prompts checks for cooldown timing, user feedback, documentation, release substance, project kill criteria, and consistency with stated principles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly interrupt releases and block publishing decisions when release scope or authority is unclear.

Mitigation: Define the repository or account scope before using the skill and require confirmation before the agent blocks a release.

Risk: The skill may inspect loosely scoped user messages, principles files, or external service data while evaluating release readiness.

Mitigation: Limit what sources the agent may read and require confirmation before it checks user messages, principles files, or external service data.

Risk: The skill can persist release decisions to a release log without clear user control.

Mitigation: Decide whether the release log may be written at all and confirm the destination before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/mupeng-release-discipline)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with checklist decisions and release-log entry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend blocking or warning on release actions and may request confirmation before writing a release log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
