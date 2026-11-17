## Description:

Calibrates when and how an agent uses humor: wit, jokes, banter, and playful tone matched to each user, context, and platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent decide when humor is appropriate, adapt joke style and intensity to user feedback, and draft humorous text when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain humor preferences, reaction history, callbacks, and some exact joke text in local files.

Mitigation: Avoid storing sensitive personal details in jokes or preferences, and delete ~/Clawic/data/humor/ to reset the profile.

Risk: Humor may be inappropriate in stressful, high-stakes, group, cultural, or persistent external-artifact contexts.

Mitigation: Apply the skill's zero-humor gates for stress, debugging, serious topics, external artifacts, and least-tolerant-reader group settings.

## Reference(s):

- [ClawHub Humor Skill](https://clawhub.ai/ivangdavila/skills/humor)
- [Clawic Humor Skill](https://clawic.com/skills/humor)
- [Setup - Humor](artifact/setup.md)
- [Memory Templates - Humor](artifact/memory-template.md)
- [Context-Aware Humor](artifact/contexts.md)
- [Off-Limits](artifact/off-limits.md)
- [Feedback System](artifact/feedback.md)
- [Humor Types](artifact/types.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Configuration]

**Output Format:** [Conversational text and markdown-backed local preference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local YAML and Markdown state under ~/Clawic/data/humor/ when the host agent persists humor preferences and reactions.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
