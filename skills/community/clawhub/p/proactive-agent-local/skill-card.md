## Description:

Helps agents act proactively, preserve working context, recover from compaction, maintain memory files, and apply guardrails for security-sensitive or external actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooduone](https://clawhub.ai/user/gooduone)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to give an agent structured local practices for proactive assistance, persistent memory, onboarding, heartbeat checks, and safe self-improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent memory and automatic profile capture can retain sensitive user context.

Mitigation: Limit what the agent records, review generated memory files, and require user consent before capturing profile details.

Risk: Autonomous monitoring and heartbeat access to email, calendar, browser, or apps can exceed the expected operating scope.

Mitigation: Disable or approval-gate autonomous crons and external actions, and restrict tool access to the minimum needed.

Risk: Self-modification of AGENTS.md or skill files can change future agent behavior.

Mitigation: Require approval and diff review before local behavior changes, especially security or operating-rule changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gooduone/skills/proactive-agent-local)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, local file templates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local operating practices and templates for an agent; review security posture before enabling autonomous monitoring or self-modification.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
