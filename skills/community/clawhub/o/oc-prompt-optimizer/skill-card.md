## Description: <br>
Turn vague maintainer intent into an execution-ready prompt with scope, variables, missing facts, tests, and acceptance criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiepu110](https://clawhub.ai/user/jiepu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to convert ambiguous agent requests into scoped prompts with explicit variables, missing information, acceptance criteria, validation commands, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An optimized prompt could carry forward incorrect assumptions from an ambiguous request. <br>
Mitigation: Review the variables, assumptions, missing information, and acceptance criteria before using the prompt for agent execution. <br>
Risk: A prompt may involve credentials, non-public data, or destructive actions when the original task explicitly requires them. <br>
Mitigation: Keep sensitive data requests explicit, avoid unnecessary credentials, and require opt-in wording for destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiepu110/oc-prompt-optimizer) <br>
- [Support repository mentioned by skill](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown sections with prompt text, variables, acceptance criteria, validation commands, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute generated prompts unless the user separately asks for execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
