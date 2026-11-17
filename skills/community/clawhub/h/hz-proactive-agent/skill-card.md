## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add proactive assistance patterns, persistent memory files, onboarding flows, security checks, heartbeat routines, and self-improvement workflows to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent storage of broad conversation and user data.

Mitigation: Require explicit user opt-in for memory writes, minimize retained personal data, and keep writes scoped to skill-owned memory files.

Risk: Background proactive behavior can create actions the user did not explicitly request.

Mitigation: Require confirmation before cron setup, isolated agent turns, deletion, external communication, or public actions.

Risk: Full-exchange logging can retain more sensitive context than necessary.

Mitigation: Disable full-exchange logging by default and prefer concise summaries that omit secrets, credentials, and unrelated personal details.

Risk: Workspace automation may affect files, browser state, calendar, email, or desktop applications.

Mitigation: Restrict reads and writes to skill-owned files unless the user explicitly expands scope, and remove or gate automatic email, calendar, browser, app, and desktop cleanup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lidekahdjdhdhsjjs-lang/skills/hz-proactive-agent)
- [Publisher profile](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace files and operating procedures for agent memory, onboarding, security checks, heartbeat routines, and proactive workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; source skill frontmatter version 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
