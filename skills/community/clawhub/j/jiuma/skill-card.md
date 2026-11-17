## Description:

Jiuma AI Video Generation (Free) helps an agent authenticate with Jiuma, upload selected media, submit AI media-generation tasks, and retrieve generated video or image results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github-gamma](https://clawhub.ai/user/github-gamma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external users use this skill to automate Jiuma media-generation workflows, including text-to-video, image-to-video, action imitation, character replacement, local media upload, and result retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Jiuma service token for authenticated API access.

Mitigation: Use a secure OS keychain where available, run the skill in an isolated Python environment, and revoke the Jiuma token when the skill is no longer needed.

Risk: The skill uploads user-selected local media files to api.jiuma.com.

Mitigation: Upload only files intended for Jiuma processing and avoid sensitive documents, private media, or files outside the requested generation workflow.

## Reference(s):

- [Jiuma Website](https://www.jiuma.com)
- [ClawHub Skill Page](https://clawhub.ai/github-gamma/skills/jiuma)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful generation tasks may return video_url or image_url values; uploads return a file_url for later task submission.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
