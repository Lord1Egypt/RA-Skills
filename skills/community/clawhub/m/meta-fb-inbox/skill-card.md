## Description:

Checks and manages Facebook page inbox messages through Meta Business Suite browser automation, including message review, replies, conversation URLs, labels, notes, and image extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picseeinc](https://clawhub.ai/user/picseeinc)

### License/Terms of Use:

MIT

## Use Case:

External business page operators and support teams use this skill to check Facebook inbox conversations, respond to customers, and manage Meta Business Suite labels and notes across one or more configured pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read customer messages, store sensitive conversation URLs, and download customer media.

Mitigation: Use it only for business pages the operator is authorized to manage, and keep config.json, saved conversation URLs, and downloaded media out of shared folders and repositories.

Risk: The skill can send replies and modify labels or notes in Meta Business Suite.

Mitigation: Require explicit approval before sending replies, changing labels or notes, or deleting notes.

Risk: The documented tab cleanup flow may close unrelated browser tabs.

Mitigation: Change cleanup behavior to close only tabs opened by this skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/picseeinc/skills/meta-fb-inbox)
- [Meta Business Suite](https://business.facebook.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline browser actions, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report customer names, message previews, unread state, conversation URLs, labels, notes, and downloaded image handling instructions.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
