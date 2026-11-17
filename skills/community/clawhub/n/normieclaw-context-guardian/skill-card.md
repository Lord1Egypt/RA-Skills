## Description:

Context Guardian helps an agent manage long conversations by tracking session health, saving important notes, and suggesting fresh starts when continuity may degrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and workspace agents use this skill to preserve conversation continuity during long or multi-topic sessions by saving notes, summarizing decisions, and guiding session resets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext conversation notes may preserve secrets, personal data, or confidential business details.

Mitigation: Use the skill only where local note saving is appropriate, redact sensitive content, and periodically review or delete memory files.

Risk: Automatically reloading prior notes may carry stale or untrusted context into a new session.

Mitigation: Keep memory files scoped to trusted workspaces and review saved notes before relying on them for sensitive decisions.

## Reference(s):

- [Context Guardian setup guide](references/setup-guide.md)
- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-context-guardian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and plaintext Markdown note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory notes such as daily Markdown files and optional long-term memory files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
