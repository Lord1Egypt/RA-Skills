## Description:

Lena lernt aus jeder Konversation und verbessert sich automatisch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwtomekk-bit](https://clawhub.ai/user/bwtomekk-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users can use this skill to make an assistant capture conversation learnings, corrections, user preferences, and session summaries for future personalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists conversation-derived content, including corrections, preferences, and project context.

Mitigation: Review saved memory before and after use, exclude secrets and sensitive personal data, and require explicit approval before writing memory files.

Risk: The skill may update agent instruction files such as AGENTS.md or TOOLS.md without clear user review.

Mitigation: Restrict writes to designated memory files unless a user explicitly approves instruction-file changes.

Risk: Long-term personalization can retain outdated or unwanted preferences.

Mitigation: Provide a clear process to inspect, correct, and delete saved memory.

## Reference(s):

- [Learnings-Datenbank](references/learnings.md)
- [Lena Learning on ClawHub](https://clawhub.ai/bwtomekk-bit/skills/lena-learning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown notes, session summaries, preference updates, and skill improvement guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent memory updates such as daily logs, long-term memory, user preferences, and environment notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
