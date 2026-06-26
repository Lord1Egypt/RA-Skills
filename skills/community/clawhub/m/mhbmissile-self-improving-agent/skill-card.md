## Description: <br>
Captures learnings, errors, and corrections so agents can log, review, and promote reusable knowledge across future tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhbmissile](https://clawhub.ai/user/mhbmissile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture command failures, corrections, missing capabilities, knowledge gaps, and reusable practices in structured learning files. It also supports optional hooks and extraction helpers for turning repeated learnings into durable agent guidance or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files and cross-session sharing may capture sensitive personal, customer, project, or transcript context. <br>
Mitigation: Use project-level hooks where possible, review hook scripts before enabling them, redact sensitive data before logging, and require explicit review before promoting entries into durable agent memory files or sharing them across sessions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mhbmissile/mhbmissile-self-improving-agent) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown instructions with inline shell commands, configuration snippets, and generated skill scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write persistent learning entries and optional agent hook reminders when installed and enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
