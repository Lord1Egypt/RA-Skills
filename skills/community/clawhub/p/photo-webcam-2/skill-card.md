## Description:

Lists and retrieves webcam snapshots, especially for foto-webcam.eu, with Chinese-language guidance for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to request authorized webcam listing and snapshot retrieval, especially for foto-webcam.eu sources. It is intended for Chinese-language agent workflows where the user provides target webcam inputs and checks the returned retrieval status or metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles webcam sources, which can expose people, private spaces, or sensitive locations.

Mitigation: Use it only for webcam sources you are authorized to access, and avoid capturing people, private spaces, or sensitive locations without clear consent.

Risk: The security review notes broad execution and file authority for a privacy-sensitive workflow.

Mitigation: Keep command execution and file writes constrained to explicit snapshot retrieval tasks, and review actions before installation or use.

Risk: The artifact includes unrelated security-analysis and CI/CD claims that are not supported by the webcam-focused evidence.

Mitigation: Do not rely on those unrelated claims when assessing fitness for use; evaluate the skill as a webcam listing and snapshot retrieval aid.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/photo-webcam-2)
- [ClawHub publisher profile: thcjp](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON result examples and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include webcam snapshot metadata, retrieval status, and execution logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
