## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve through durable memory, onboarding, heartbeat checks, security patterns, and self-improvement routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure an assistant that preserves continuity across sessions, learns user preferences through onboarding, performs periodic maintenance checks, and proposes useful work while keeping external actions gated by approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages durable workspace memory that may capture personal context or sensitive information.

Mitigation: Require explicit approval before writing personal data, exclude secrets and sensitive personal information, and keep memory files out of version control and backups.

Risk: The skill encourages proactive updates to operating notes and self-improvement files.

Mitigation: Review proposed changes to AGENTS.md, TOOLS.md, SOUL.md, USER.md, memory files, and skill files before applying them.

Risk: Proactive behavior can initiate work before the user asks for it.

Mitigation: Keep public, external, destructive, or irreversible actions gated on explicit human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/proactive-agent-jarvis)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, workspace file templates, and a local audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating notes and templates for durable memory, onboarding, heartbeat checks, tool notes, and security review.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
