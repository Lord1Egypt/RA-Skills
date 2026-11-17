## Description:

Multi-Agent Codegen turns a short software request into Python code, pytest tests, and a review report through a Plan, Write, Verify, Test, and Refine agent workflow with Feishu progress notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to convert short software, tool, or script requests into runnable Python code, pytest tests, and review feedback when a structured multi-agent workflow is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive project details through Feishu notifications to a fixed recipient using local messaging credentials.

Mitigation: Review the recipient and notification behavior before installation; disable notifications or change the recipient to a user-controlled destination before running it on confidential work.

Risk: Generated code and tests may still be incomplete or incorrect despite verify and retry steps.

Mitigation: Review and run generated files in an isolated workspace before using or deploying the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/multi-agent-codegen)
- [RULE-20260701-001](https://my.feishu.cn/docx/Nw3RdgXR0oKVpSxyQRLcUG9nnm2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans and reviews, Python source files, pytest test code, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plan.md, code.py, test_code.py, and refine.md to the selected output directory.]

## Skill Version(s):

3.3.0 (source: server release and artifact/skill.json; changelog released 2026-09-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
