## Description: <br>
Provides error classification, recovery, and graceful-degradation patterns for resilient agent and plugin workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to classify operational errors, choose recovery strategies, and define graceful degradation behavior for production-style integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may cause the skill to influence unrelated error-handling or debugging tasks. <br>
Mitigation: Narrow when the skill activates when deploying it in a production agent environment. <br>
Risk: Logging examples that include full context could capture prompts, credentials, request payloads, or user data. <br>
Mitigation: Redact or allowlist logged fields before adopting the snippets in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-error-patterns) <br>
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Error Classification](modules/classification.md) <br>
- [Recovery Strategies](modules/recovery-strategies.md) <br>
- [Agent Damage Control](modules/agent-damage-control.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, YAML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only guidance; no hidden execution behavior was found in the release security evidence.] <br>

## Skill Version(s): <br>
1.9.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
