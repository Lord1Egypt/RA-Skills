## Description: <br>
12周LeetCode跳槽刷题计划助手。当用户输入"第X天"或"DX"时触发，返回对应题目；当用户提交解题答案或表示未解出时，生成错题记录并写入errorset.md；根据当天进度推荐复习之前的错题。适用于系统性刷题打卡、错题管理和间隔复习场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[candiecandyy](https://clawhub.ai/user/candiecandyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and interview candidates use this skill to follow a 12-week LeetCode practice plan, receive daily problem prompts, record mistakes, and review due mistake entries on a spaced schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script creates or updates errorset.md in the agent's current working directory. <br>
Mitigation: Run the skill from the directory where the mistake notebook should be stored and review errorset.md after updates. <br>
Risk: Mistake explanations may contain sensitive personal learning notes or interview-preparation details. <br>
Mitigation: Keep mistake reasons concise and avoid entering sensitive personal information. <br>


## Reference(s): <br>
- [12 Week LeetCode Plan](references/plan.md) <br>
- [ClawHub skill page](https://clawhub.ai/candiecandyy/leetcode-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and rewrite errorset.md in the agent's current working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
