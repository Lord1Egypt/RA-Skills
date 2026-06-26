## Description: <br>
Enable managers to self-diagnose, identify defects, track improvements, and maintain skill health without relying on external prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjl1004](https://clawhub.ai/user/wjl1004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers and agent operators use this skill to run local self-diagnostics, identify recurring behavior issues, and track follow-up improvements in an evolution log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local OpenClaw memory, context, and daily memory files during diagnostics. <br>
Mitigation: Use it only in workspaces where that local context may be reviewed by the agent, and avoid storing highly sensitive material in those files. <br>
Risk: Diagnostic observations can persist in a local evolution-log.md file. <br>
Mitigation: Review the generated log periodically and remove entries that should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjl1004/manager-self-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown log entries, with usage guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends a local evolution-log.md when diagnostics find issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
