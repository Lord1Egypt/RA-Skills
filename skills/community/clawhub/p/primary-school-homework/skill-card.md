## Description:

小学低年级作业管理助手。支持老师消息解析、睡前检查清单、错题拍照归档、每日闯关复习、每周错题总结（含表扬统计）、备考提醒、作业计时七个模式，适合1-3年级家长使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickytsao-swordedge](https://clawhub.ai/user/rickytsao-swordedge)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers use this skill to manage primary-school homework routines, including teacher-message parsing, bedtime checks, wrong-question review, weekly summaries, reminders, and homework timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process children's personal details, schoolwork, homework photos, school names, class screenshots, contact details, or other identifiers.

Mitigation: Use aliases instead of real names, avoid exact ages, crop or redact homework photos, and avoid uploading faces, school names, class screenshots, contact details, or other identifiers unless that sharing is acceptable for the chat platform and model provider.

Risk: Conversation memory or archived records may retain child-related homework data longer than intended.

Mitigation: Check how the OpenClaw environment stores and deletes conversation memory or archived records before using the skill with real children's information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rickytsao-swordedge/skills/primary-school-homework)
- [Project homepage](https://github.com/rickytsao-swordedge/primary-school-homework)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style chat responses with structured lists, short prompts, and summary cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Photo-based wrong-question archiving requires an image-capable model.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
