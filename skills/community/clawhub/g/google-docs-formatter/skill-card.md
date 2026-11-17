## Description:

Instruction-only workflow for formatting, editing, and creating Google Docs using the existing gog skill/CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asperitas-solutions](https://clawhub.ai/user/asperitas-solutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to format, edit, create, and verify Google Docs through an existing gog workflow while preserving document structure and requiring approval for risky writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Docs changes may overwrite, clear, delete, or substantially replace document content.

Mitigation: Require explicit approval before writes, clears, large replacements, deletions, or changes to shared/work documents with unclear ownership or audience.

Risk: The delegated gog tool may have Google account scopes that affect documents or Drive content.

Mitigation: Confirm the installer trusts and understands gog and its Google account scopes before using the skill.

Risk: Advanced formatting may not be supported by the gog workflow.

Mitigation: Inspect and export the document before editing, verify the result afterward, and propose the nearest gog-supported alternative when formatting is unsupported.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; Google Docs and Drive operations are delegated to the existing gog tool.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
