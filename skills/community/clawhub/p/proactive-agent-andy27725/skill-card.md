## Description: <br>
Transforms task-following agents into proactive assistants with persistent memory, onboarding, heartbeat checks, self-healing routines, security hardening, WAL protocol, working buffer recovery, and autonomous cron patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an assistant that remembers user context, performs proactive check-ins, recovers from context loss, and applies explicit safety guardrails before external or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent personal memory can retain sensitive user context longer than intended. <br>
Mitigation: Avoid storing secrets or highly sensitive personal information, and regularly review or delete generated memory files. <br>
Risk: Proactive background checks, email or calendar monitoring, autonomous crons, spawned agents, app or tab cleanup, and automatic memory capture may act beyond the user's intended scope. <br>
Mitigation: Disable or tightly scope those behaviors before use, and require explicit approval for external, public, destructive, or irreversible actions. <br>
Risk: The release was classified by the server security scan as suspicious because it requests broad persistent memory, background monitoring, and local-environment actions without enough user control. <br>
Mitigation: Install only when those behaviors are explicitly desired and review the configured memory, monitoring, cron, and cleanup settings before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/proactive-agent-andy27725) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes starter workspace files for memory, onboarding, heartbeat checks, user profile, agent identity, tool notes, and security audit guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata); bundled artifact frontmatter version 3.1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
