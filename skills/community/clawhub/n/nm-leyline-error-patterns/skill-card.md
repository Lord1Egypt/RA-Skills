## Description: <br>
Provides error classification, recovery, and graceful-degradation patterns for agents and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a reference for classifying errors, choosing recovery strategies, and designing graceful degradation in service or multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation terms may cause agents to invoke the skill for unrelated debugging or resilience work. <br>
Mitigation: Invoke it only when error classification, recovery, or graceful-degradation guidance is needed. <br>
Risk: Copied logging and alerting examples could expose credentials, prompts, user data, file paths, or service responses. <br>
Mitigation: Sanitize copied logging and alerting patterns before writing to persistent logs or external alert systems. <br>
Risk: Example code and patterns are references, not drop-in production implementations. <br>
Mitigation: Adapt, review, and test the patterns in the target environment before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-error-patterns) <br>
- [Leyline project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Python and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only reference content; examples should be adapted and reviewed before use.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
