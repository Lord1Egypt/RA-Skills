## Description:

Transforms AI agents from task-followers into proactive partners that anticipate needs, preserve working context, improve over time, and apply security hardening patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eathon](https://clawhub.ai/user/eathon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a proactive, persistent assistant with onboarding files, memory routines, heartbeat checks, recovery protocols, and security guardrails. It is intended for agents that should anticipate user needs while preserving human approval for sensitive, external, or irreversible actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and local profile files can retain sensitive personal data or secrets longer than intended.

Mitigation: Make memory and profile writes opt-in, exclude secrets and sensitive personal data, and review or delete generated memory files on a regular schedule.

Risk: Self-modifying operating rules and autonomous maintenance can change agent behavior or cleanup files without enough user control.

Mitigation: Require explicit approval for rule changes, cleanup actions, security changes, public actions, and irreversible operations.

Risk: Proactive background behavior can blur the line between helpful local work and actions that affect external systems or other people.

Mitigation: Allow local drafts and analysis, but require human approval before sending, publishing, purchasing, deleting, or connecting to external agent networks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eathon/skills/proactive-agent-v2)
- [Publisher Profile](https://clawhub.ai/user/eathon)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with starter Markdown files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable workspace files for onboarding, memory, heartbeat checks, operating rules, user profile notes, tool notes, and a local security audit script.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
