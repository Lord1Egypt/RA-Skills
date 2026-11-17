## Description:

Generates daily Xiaohongshu-style Chinese health and wellness notes with checklist formatting, emoji-rich short lines, hashtag guidance, platform-compliant calls to action, and optional local archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meimei-shoulu](https://clawhub.ai/user/meimei-shoulu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, health-content operators, and social media teams use this skill to draft daily Xiaohongshu wellness posts in a repeatable style with titles, short-form body structure, compliance checks, and hashtags. The skill can also provide a shell command to add finished Markdown notes to a local HTML article library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an embedded WeChat contact and payment upgrade flow unrelated to normal note generation.

Mitigation: Ignore the payment instructions unless you independently trust the publisher and verify the transaction path outside the agent workflow.

Risk: Generated wellness content may contain unsupported medical claims, absolute efficacy language, or platform-sensitive calls to action if not reviewed.

Mitigation: Review each draft before publishing, remove diagnosis or treatment claims, avoid absolute efficacy wording, and keep calls to action within Xiaohongshu-supported in-platform options.

Risk: The local archive helper saves generated notes into an HTML library, which can preserve sensitive health or personal details if included in drafts.

Mitigation: Use a dedicated notes folder, avoid storing sensitive personal data, and confirm scheduled or repeated runs before they save or index content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown content with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language Xiaohongshu post drafts are intended to be reviewed before publishing; local archiving writes generated article content into an HTML library.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
