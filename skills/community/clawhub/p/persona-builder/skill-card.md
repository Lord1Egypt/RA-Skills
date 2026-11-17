## Description:

Guided interview to generate a complete agent workspace with SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, and USER.md files that capture identity, goals, communication style, epistemic standards, anti-sycophancy rules, dissent protocol, and agent personality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interview a human and generate editable local workspace files that define an agent's identity, memory structure, operating preferences, autonomy bounds, and user context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated files may persist sensitive profile details and personal operating preferences in plaintext.

Mitigation: Review generated files before use, redact sensitive details, and avoid committing persona or memory files to public repositories.

Risk: Unvalidated user-provided interview text can shape future agent behavior through generated SOUL.md and AGENTS.md files.

Mitigation: Do not paste untrusted prewritten answers, and review SOUL.md and AGENTS.md carefully before adopting them.

## Reference(s):

- [Interview Blocks](references/interview-blocks.md)
- [Generation Rules](references/generation-rules.md)
- [Research Notes](references/research-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five local, human-editable workspace files: SOUL.md, IDENTITY.md, MEMORY.md, AGENTS.md, and USER.md.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
