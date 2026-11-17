## Description:

Create new OpenClaw skills that pass ClawHub validation by guiding developers from template setup through validation and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, validate, configure, and publish OpenClaw skills with scanner-aware guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can normalize publishing and configuration changes that are under-scoped for a user's environment.

Mitigation: Review generated skill directories, configuration changes, and publishing commands before installing or releasing them.

Risk: Generated or copied skill content may mishandle templates, external endpoints, or long-lived secrets if adopted without review.

Mitigation: Use a clean allowlisted template, pin CLI versions, document real external endpoints honestly, and protect any required secrets with appropriate file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ogdegenblaze/skills/kai-skill-creator)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also create an OpenClaw skill directory through the bundled shell script.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
