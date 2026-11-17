## Description:

Postey Video transcribes videos, prepares platform-specific captions, uploads media with a cover frame, and creates drafts for approval, including for local files and large uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media teams use it to turn a local video or video URL into a transcript, platform-specific captions, uploaded media, and drafts for connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weaknesses in account selection and remote downloads could expose private media or local services.

Mitigation: Prefer a corrected release before processing private media or unfamiliar URLs. Use a trusted working directory, explicitly supply your own authentication, and restrict downloads from reaching internal services.

Risk: A draft operation may not have completed even when the workflow appears to have progressed.

Mitigation: Verify that Postey created each draft before reporting success.

Risk: Publishing or scheduling makes content public without another review step.

Mitigation: Show the platform captions and get explicit user approval before publishing or scheduling.

## Reference(s):

- [Postey Video on ClawHub](https://clawhub.ai/posteyai/skills/postey-video)
- [Video Workflow](video-workflow.md)
- [Video Everywhere](references/video-to-everywhere.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Transcripts, platform-specific captions, draft-post content, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captions are tailored per connected platform; drafts await user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
