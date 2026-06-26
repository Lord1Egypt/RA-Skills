## Description: <br>
基于 Claude Code 的9条核心规则，提供极简提示词速查和即用模板，帮助用户快速写出高质量提示词。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jx-76](https://clawhub.ai/user/jx-76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and prompt authors use this skill as a compact prompt-engineering reference for structuring requests, adding constraints, reusing task templates, and checking common prompt failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-loading or injecting the skill into the system prompt may apply its formatting and verification rules in conversations where the user did not explicitly request them. <br>
Mitigation: Enable auto-load or system-prompt injection only in workspaces where those prompt-writing rules are desired by default. <br>
Risk: Prompt templates that emphasize constraints may still be applied too broadly for simple or unrelated tasks. <br>
Mitigation: Select only the relevant rules or use the compact modes for low-complexity tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jx-76/prompt-master) <br>
- [Publisher profile](https://clawhub.ai/user/jx-76) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown prompt-writing guidance with reusable text and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or data access; optional auto-load guidance affects how broadly the prompt rules may be applied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
