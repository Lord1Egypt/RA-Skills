## Description: <br>
Transforms AI agents from task-followers into proactive partners that anticipate needs, maintain memory, run heartbeats, and continuously improve with security and verification patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makaronz](https://clawhub.ai/user/makaronz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install documentation, starter files, and audit scripts that encourage proactive behavior, persistent memory, onboarding, self-improvement, and security checks in an AI agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages highly proactive behavior, persistent memory files, heartbeat checks, and scan-every-message logging that can collect sensitive user context without enough user control. <br>
Mitigation: Require explicit opt-in before enabling memory or heartbeat routines; define review, retention, and deletion rules for profile, memory, and conversation files. <br>
Risk: Autonomous check-ins, background agent turns, email or calendar checks, and cleanup routines may act without timely user awareness. <br>
Mitigation: Disable or rewrite autonomous crons, email/calendar checks, heartbeat cleanup, and background agent turns by default; require human review before external actions or workspace cleanup. <br>
Risk: Self-healing and local cleanup guidance could modify or delete files in ways the user did not intend. <br>
Mitigation: Keep destructive actions draft-only or dry-run by default, prefer trash over permanent deletion, and require explicit confirmation before changing or deleting files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/makaronz/proactive-agent-install) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes starter workspace files and a local security audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
