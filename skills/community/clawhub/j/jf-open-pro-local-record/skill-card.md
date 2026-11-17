## Description:

JFTech local-recording skill for devices with TF card or hard-disk storage; it helps an agent query recording calendars and recording lists, generate playback or download URLs, retrieve local alarm images, and switch the recording stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to manage local recordings on supported JFTech devices, including finding stored recordings, getting temporary playback or download links, viewing alarm images, and changing future recording stream quality.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Device tokens, app secrets, and device passwords may be sent to a hostname selected through JF_ENDPOINT.

Mitigation: Set JF_ENDPOINT only to the documented JFTech regional host for the deployment region and store credentials in a protected secret store.

Risk: The skill can expose private recording metadata and temporary playback, download, or image URLs.

Mitigation: Limit use to authorized device operators and avoid sharing generated URLs outside approved incident or support workflows.

Risk: The skill can switch the device recording stream, affecting the quality and size of future recordings.

Mitigation: Require operator confirmation before stream changes and document any change made during an investigation or maintenance session.

## Reference(s):

- [JFTech documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-local-record)
- [ClawHub publisher profile](https://clawhub.ai/user/jftech)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recording metadata, temporary playback or download URLs, and alarm image URLs returned by JFTech device APIs.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
