## Description:

Guides an agent through preparing a Douyin Creator Platform short-video upload and saving it as a draft with title, description, cover, collection, permission, and AI-content declaration settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators and their agents use this skill to prepare Douyin short-video uploads with required metadata, cover, collection, permissions, and AI-generated content declarations. The flow is intended to save the prepared video as a draft for human review rather than immediately publishing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises publishing Douyin videos, but the security summary says the actual final step saves the video as a draft.

Mitigation: Use it with a dedicated OpenClaw browser profile and confirm the final Douyin draft or publication state manually before relying on the automation result.

Risk: The workflow automates uploads and account-facing creator-platform settings.

Mitigation: Review the selected video, title, description, tags, permissions, and AI-content declaration before any manual publication step.

## Reference(s):

- [Douyin Creator Platform upload page](https://creator.douyin.com/creator-micro/content/upload)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with browser-operation steps and inline Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent to use an OpenClaw browser profile, page snapshots for current element references, and pyautogui/tkinter for file picker interaction.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
