## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve with persistent memory, proactive check-ins, security hardening, autonomous maintenance patterns, and self-improvement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackmcvn](https://clawhub.ai/user/blackmcvn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure an assistant with persistent workspace memory, onboarding files, periodic self-checks, proactive suggestions, and safety rules for external content and irreversible actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent memory files that may contain personal context, preferences, relationships, and session history.

Mitigation: Install only in trusted workspaces, review captured memory regularly, and narrow or disable automatic memory capture when sensitive data should not persist.

Risk: The skill describes proactive and background-style agent behavior that may act without direct prompting.

Mitigation: Require explicit approval for autonomous cron or isolated agentTurn jobs and keep external, public, destructive, or irreversible actions gated by the user.

Risk: The skill includes patterns for updating workspace instructions and local operating files, which can alter future agent behavior.

Mitigation: Review changes to AGENTS.md, skill files, and memory templates before accepting them, and keep a versioned record of instruction changes.

Risk: The bundled audit script reads local workspace and configuration files to produce a manual security report.

Mitigation: Inspect the script before running it and treat its output as advisory rather than as an automated remediation step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackmcvn/skills/proactive-agent-3-1-0)
- [Publisher profile](https://clawhub.ai/user/blackmcvn)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [Hal 9001 profile](https://x.com/halthelobster)
- [Bulletproof Memory companion skill](https://clawdhub.com/halthelobster/bulletproof-memory)
- [PARA Second Brain companion skill](https://clawdhub.com/halthelobster/para-second-brain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workspace file templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local operating procedures and starter files; users should review before enabling persistent memory or autonomous behavior.]

## Skill Version(s):

3.1.0 (source: artifact/SKILL.md frontmatter and artifact/_meta.json; release package version 1.0.0 in evidence.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
