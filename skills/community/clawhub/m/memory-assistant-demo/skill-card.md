## Description:

记忆助手 - 帮助用户管理、搜索和组织记忆文件。支持创建记忆条目、按日期或关键词搜索记忆、以及长期记忆的个性化更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agent developers can use this skill to keep local daily memory notes, search past entries by keyword or date, and consolidate important information into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory notes may contain private or sensitive information.

Mitigation: Store only information appropriate for local persistence and review memory content before sharing, searching, or summarizing it.

Risk: The skill suggests commands that append to daily notes or edit MEMORY.md.

Mitigation: Review the target file path and proposed memory changes before allowing them to persist.

Risk: Requests from untrusted people could cause inappropriate memory reads or updates.

Mitigation: Use the skill only for trusted workflows and avoid applying memory changes requested by untrusted parties.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/memory-assistant-demo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to local memory files such as daily notes and MEMORY.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
