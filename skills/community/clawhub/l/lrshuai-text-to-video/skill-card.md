## Description:

Generates video from a text prompt using supported remote video-generation models such as Veo 3.1, Sora 2, and Doubao Seedance 1.5 Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can invoke this skill to submit a short text description, and optionally media inputs, to a configured remote service for video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Python script directly and bypasses the normal runner.

Mitigation: Review the artifact before installation and run it only in an environment where direct script execution is acceptable.

Risk: Prompts, model choices, credentials, and optional local media can be sent to a configurable remote endpoint.

Mitigation: Use a narrowly scoped TEAM_API_KEY, verify TEAM_BASE_URL before running, and provide local file paths only when those files are intended for upload.

Risk: The script polls the remote service until completion and may continue waiting if the service does not finish promptly.

Mitigation: Monitor the process and stop it if polling does not complete in an acceptable time window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-text-to-video)
- [Publisher profile](https://clawhub.ai/user/lrshu)
- [Default Team AI endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Console text and JSON responses from the remote video-generation API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY and may poll until the remote generation task completes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
