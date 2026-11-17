## Description:

Generates environmental audio and special sound effects from text prompts using the Keling SFX model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to submit text prompts for environmental audio or special sound effects and receive generation results from the configured model service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires direct Python execution rather than the standard runner path.

Mitigation: Review the script before installation and remove or justify the runner-bypass instruction before routine use.

Risk: The model client can send local image or video file contents to the configured remote service.

Mitigation: Do not allow local file path arguments unless uploading those files is intended and approved.

Risk: The remote endpoint and bearer credential determine where prompts and optional media are sent.

Mitigation: Use a dedicated, revocable TEAM_API_KEY and verify TEAM_BASE_URL or the default endpoint before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-sfx-generation)
- [Publisher profile](https://clawhub.ai/user/lrshu)
- [Default remote model API endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Command-line status text and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY; optional local image, image-tail, or video paths may be encoded and sent to the configured remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
