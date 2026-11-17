## Description:

心理健康助手。情绪自查、呼吸练习、情绪日记、心理资源、压力管理、感恩练习。Mental health tool with mood check, breathing exercises, journaling, resources, stress management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for self-care support such as mood check-ins, breathing exercises, journaling prompts, stress-management suggestions, gratitude practice, and mental-health resource pointers. It is not a replacement for professional mental-health care or emergency services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive wellness or journal entries may be saved locally in plaintext.

Mitigation: Avoid entering sensitive details unless local file permissions, retention, and access controls are acceptable.

Risk: The reset command may not clear previously recorded tracker data.

Mitigation: Confirm and manually remove local data files before assuming records have been deleted.

Risk: Emergency and crisis resources are focused on the listed Chinese hotline context.

Mitigation: Users outside that context should use local emergency, crisis, or medical services instead of relying on the listed numbers.

Risk: Command behavior is inconsistent for a high-trust health context.

Mitigation: Review available commands and test expected behavior before offering the skill to end users.

## Reference(s):

- [Mental Health on ClawHub](https://clawhub.ai/bytesagain-lab/skills/mental-health)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like terminal text and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wellness prompts, crisis-resource pointers, and local tracker output.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
