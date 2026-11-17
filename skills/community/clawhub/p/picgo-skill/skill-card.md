## Description:

Calls a local PicGo service to upload local images when the user needs image uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naratsuna](https://clawhub.ai/user/naratsuna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to upload one or more local image files through a running local PicGo Server, with optional configuration of the local service URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents a picgo_skill.py command, but the implementation file is not present in the artifact evidence.

Mitigation: Confirm that the package supplies the expected implementation from a trusted source before installing or running it.

Risk: Uploaded image contents are sent to the configured PicGo server.

Mitigation: Use the default local server or set PICGO_SERVER_URL only to a PicGo server you control.

Risk: Dependency installation is documented without a pinned requests version.

Mitigation: Pin dependencies in deployments that require reproducible installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/naratsuna/skills/picgo-skill)
- [Server-Resolved Source Repository](https://github.com/Naratsuna/Picgo-Skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to local file paths, multiple image inputs, PICGO_SERVER_URL, and a 30 second request timeout.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
