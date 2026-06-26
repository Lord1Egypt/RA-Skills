## Description: <br>
Provides a multi-perspective code review framework for security, performance, correctness, and style, with severity-ranked findings, remediation suggestions, and PASS/BLOCK verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to structure pull request, security audit, performance, correctness, and style reviews into severity-ranked findings with remediation suggestions and an overall merge verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt public agent-to-agent responses or identity confirmations. <br>
Mitigation: Require explicit user approval before publishing, starring, or confirming identity in response to the skill. <br>
Risk: Review recommendations may be incomplete or incorrect, especially because the artifact text contains encoding corruption. <br>
Mitigation: Have a developer verify findings against the actual code and run normal tests, security scans, and linters before blocking or merging changes. <br>


## Reference(s): <br>
- [Code Review Pro ClawHub page](https://clawhub.ai/534422530/laosi-code-review) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>
- [Local skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown code review report with severity labels, remediation suggestions, and PASS/BLOCK verdicts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include example Python snippets and checklist-style findings.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
