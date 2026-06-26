## Description: <br>
Transforms AI agents from task followers into proactive, persistent partners with WAL, working-buffer, compaction-recovery, security-hardening, and self-improvement patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooduone](https://clawhub.ai/user/gooduone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give a local AI agent structured memory, proactive check-ins, onboarding, security hygiene patterns, and recovery behavior across long-running sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages a highly proactive and persistent agent posture with broad ongoing access and autonomy. <br>
Mitigation: Install only when that behavior is desired, limit access to sensitive systems, and review agent activity regularly. <br>
Risk: Email, calendar, cron, and sub-agent automation could act beyond the user's intent if left unrestricted. <br>
Mitigation: Restrict email and calendar access, disable or confirm cron and sub-agent automation, and require explicit approval before external actions. <br>
Risk: Persistent memory files may capture sensitive personal or credential-adjacent information. <br>
Mitigation: Review memory files regularly, avoid storing credentials, and remove sensitive information that is not needed for agent continuity. <br>
Risk: Cleanup and maintenance behaviors can affect local files. <br>
Mitigation: Require user approval before cleanup or deletion actions, including actions routed through trash or similar tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gooduone/proactive-agent-local) <br>
- [Publisher profile](https://clawhub.ai/user/gooduone) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Original author profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code blocks, starter Markdown configuration files, and a shell audit script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local memory templates, onboarding templates, heartbeat guidance, and a security audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog; artifact/SKILL.md frontmatter describes upstream 3.1.0 content) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
