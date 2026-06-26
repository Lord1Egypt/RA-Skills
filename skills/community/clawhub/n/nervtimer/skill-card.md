## Description: <br>
Set one-shot or recurring timers across channels and keep nagging every 5 minutes until the user explicitly says it is done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fragwuerdig](https://clawhub.ai/user/fragwuerdig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create one-shot or recurring reminder timers, schedule reminder turns, and continue short escalating reminders until the user explicitly confirms completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and notes behavior that may use full-access review helpers or external reviewer fallbacks. <br>
Mitigation: Review the skill before installing it in sensitive workspaces and disable full-access or external fallback review behavior unless explicitly intended. <br>
Risk: The skill creates scheduled reminder jobs and repeated nagging turns that can continue until explicit completion. <br>
Mitigation: Confirm schedule details before creating timers, keep reminders scoped to the intended channel, and mark or cancel timers when they are no longer needed. <br>
Risk: Timer state is persisted locally under the user's OpenClaw directory by default. <br>
Mitigation: Use an isolated store path for sensitive workspaces and review stored timer data if timer titles or reasons may contain private information. <br>


## Reference(s): <br>
- [NervTimer Intent Schema](references/intent-schema.md) <br>
- [NervTimer Escalation Policy](references/escalation-policy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fragwuerdig/nervtimer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON cron payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces short reminder text, cron scheduling payloads, and local timer state transitions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
