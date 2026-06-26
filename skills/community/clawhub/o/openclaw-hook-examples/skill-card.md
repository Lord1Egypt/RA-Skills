## Description: <br>
Provides example hooks for OpenClaw to intercept, modify, block tool calls, switch models, log actions, and handle subagent events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and plugin authors use this skill as reference material for implementing OpenClaw hooks that audit, block, validate, route, or modify agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool-audit logging examples can expose raw tool arguments, outputs, or session identifiers if reused without filtering. <br>
Mitigation: Use allowlisted fields, redaction, restricted log access, and clear retention rules before converting the examples into a real plugin. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/openclaw-hook-examples) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference material; examples should be reviewed and adapted before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
