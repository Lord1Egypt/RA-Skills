## Description:

Builds an interactive digital-human free mini course from supplied expertise materials, grounded in user-provided facts and designed for learner voice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and educators use this skill to turn their own expertise materials into an askable lead-magnet mini course. The skill guides an agent through PersonWise CLI authentication, readiness checks, course creation, source upload, review checkpoints, and final access reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update path can ask the agent to run shell commands selected by a remote response.

Mitigation: Approve only commands that clearly invoke the expected PersonWise bootstrap or CLI from expected PersonWise locations and origins, and require current signed trust metadata and native publisher verification where available.

Risk: The skill can install or upgrade a local CLI and start browser OAuth.

Mitigation: Require explicit approval for installer or upgrade actions, keep authentication in the browser flow, and do not handle passwords, tokens, cookies, or callback secrets.

Risk: Course creation may upload user-selected materials to the PersonWise service.

Mitigation: Upload only files the user named, attached, or explicitly selected; disclose and seek approval before uploading any agent-discovered local file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-lead-magnet)
- [PersonWise Publisher Profile](https://clawhub.ai/user/personwiseai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON configuration, Shell commands, Guidance]

**Output Format:** [Markdown responses with structured JSON inputs and PersonWise CLI command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates PersonWise course runs, may upload user-selected source files, and reports run, project, source, review, access, and URL status without secrets.]

## Skill Version(s):

2.1.9 (source: ClawHub release metadata and SKILL.md attribution block)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
