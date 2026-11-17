## Description:

Jiuma AI Video Generation (Free) helps agents submit and check AI media-generation tasks for video, image, audio, action imitation, and character replacement through Jiuma.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github-gamma](https://clawhub.ai/user/github-gamma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authenticate with Jiuma, upload media, submit AI generation jobs, and retrieve generated media task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload helper can send any readable local file path to Jiuma.

Mitigation: Use explicit intended media paths only, avoid secrets or private documents, and run from a limited workspace.

Risk: The skill stores and uses a bearer token for Jiuma API access.

Mitigation: Use a native OS keyring, avoid sharing real authorization values in prompts or logs, and reauthorize if token status checks fail.

## Reference(s):

- [Jiuma official website](https://www.jiuma.com)
- [ClawHub skill page](https://clawhub.ai/github-gamma/skills/jiuma-ai-video-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task identifiers, task status values, uploaded file URLs, and generated media URLs.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
