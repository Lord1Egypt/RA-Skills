## Description:

Generates lip-synced Jiuma digital-human videos from text or audio input using selected avatar and voice IDs or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect digital-human video parameters, call Jiuma APIs to create a video task, and check task status until a video URL is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, audio or avatar URLs, and generated-task data are sent to Jiuma.

Mitigation: Avoid sensitive or regulated content unless the deployment owner has approved sending that data to Jiuma.

Risk: The login flow can expose or persist API credentials in local .jiuma files and terminal logs.

Mitigation: Treat .jiuma files and logs as sensitive, restrict local file permissions, and rotate the Jiuma key if it may have been printed or captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddcn1/skills/jiuma-free-meta-human)
- [Skill instructions](artifact/SKILL.md)
- [Login flow documentation](artifact/LOGIN.md)
- [Avatar ID reference](artifact/meta-human.json)
- [Voice ID reference](artifact/voice.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Jiuma task IDs, payment or login URLs, task status, and generated video URLs.]

## Skill Version(s):

1.0.13 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
