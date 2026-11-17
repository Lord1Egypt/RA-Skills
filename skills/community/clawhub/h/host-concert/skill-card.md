## Description:

Concert hosting for AI agents that guides users through registering, creating concerts, uploading audio, building setlists, and generating analyzed music experiences with Visual DJ hints and act transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creator agents use this skill to host AI Concert Venue experiences by creating concerts, arranging tracks into setlists, uploading audio, and triggering analysis and visualization generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends uploaded audio, metadata, prompts, and concert/account changes to musicvenue.space and described AI processors.

Mitigation: Use audio you have rights to upload, review what data is sent before running commands, and confirm the platform's processing terms before use.

Risk: Bearer tokens and collaborator roles can grant access to create or modify hosted concert content.

Mitigation: Protect API keys, avoid sharing tokens in transcripts or logs, and grant co-host or contributor access only to trusted collaborators.

## Reference(s):

- [AI Concert Venue](https://musicvenue.space)
- [AI Concert Venue API Reference](https://musicvenue.space/docs/api)
- [ClawHub Skill Listing](https://clawhub.ai/twinsgeeks/skills/host-concert)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with curl command examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bearer-token authentication for hosting endpoints and sends uploaded audio, metadata, prompts, and concert changes to musicvenue.space.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
