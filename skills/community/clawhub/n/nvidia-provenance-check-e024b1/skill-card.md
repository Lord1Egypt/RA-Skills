## Description:

Summarize a repository release's provenance for a reviewer by listing the source repository, commit, and the change areas touched between two revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release reviewers use the skill to prepare a concise provenance note for a release and identify changed areas that need maintainer confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A provenance note could contain incorrect or misleading release details.

Mitigation: Ask the owning maintainer to confirm each source, revision, and flagged entry before relying on the note.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cindypapa/skills/nvidia-provenance-check-e024b1)
- [Provenance note template](references/notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain Markdown with source, changed areas, and review notes sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries are one line each and quote paths and revisions only.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
