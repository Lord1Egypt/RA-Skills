## Description:

Runs a design grilling session that interviews the user until shared understanding is reached, then generates CONTEXT.md and ADR files from the discussion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to clarify project design language, resolve domain decisions through a guided interview, and capture the outcome as repository documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated glossary or ADR documentation may misstate project decisions or code behavior.

Mitigation: Review generated CONTEXT.md and docs/adr files before committing or sharing them.

Risk: The skill reads project context and may update repository documentation during the session.

Mitigation: Use it only in repositories where documentation updates are intended, and inspect diffs before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/genortg/skills/grill-docs)
- [GSD Core attribution](https://github.com/open-gsd/gsd-core)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown documentation files and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update CONTEXT.md and docs/adr Markdown files during the session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
