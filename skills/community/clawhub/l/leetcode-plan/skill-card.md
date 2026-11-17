## Description:

12周LeetCode跳槽刷题计划助手。当用户输入"第X天"或"DX"时触发，返回对应题目；当用户提交解题答案或表示未解出时，生成错题记录并写入errorset.md；根据当天进度推荐复习之前的错题。适用于系统性刷题打卡、错题管理和间隔复习场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[candiecandyy](https://clawhub.ai/user/candiecandyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and interview candidates use this skill to follow a structured 12-week LeetCode study plan, receive daily problem assignments, track missed problems, and schedule spaced review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to build shell commands that include user-provided text, which could cause unintended command execution if interpolated through a shell.

Mitigation: Pass arguments through a structured process API with shell execution disabled, and review generated commands before running them.

Risk: The helper script creates or rewrites errorset.md in the current working directory.

Mitigation: Run the skill only in the intended workspace and inspect or back up any existing errorset.md before use.

Risk: Generated study feedback, core ideas, and similar-problem recommendations may be incomplete or incorrect.

Mitigation: Verify important guidance against LeetCode problem statements, accepted solutions, or local tests.

## Reference(s):

- [12 周 LeetCode 跳槽计划 - 题目总表](references/plan.md)
- [ClawHub skill page](https://clawhub.ai/candiecandyy/skills/leetcode-plan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local errorset.md updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or rewrite errorset.md in the agent's current working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
