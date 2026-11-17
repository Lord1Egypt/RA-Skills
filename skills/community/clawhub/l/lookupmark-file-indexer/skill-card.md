## Description:

Fast filesystem catalog for finding files by name, date, type, or size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and file-heavy users use this skill to build and query a local metadata-only catalog for finding files by name, extension, size, and modified date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local SQLite catalog can make filenames, paths, sizes, and modified dates searchable for indexed folders.

Mitigation: Install only when this local catalog is acceptable, keep catalog file permissions tight, and limit indexed roots to intended folders.

Risk: Broad natural-language triggers such as "where is" can invoke file lookup behavior in ambiguous contexts.

Mitigation: Use explicit file-search phrasing when invoking the skill and narrow triggers if deployment policy requires stricter activation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem metadata lookup guidance; it does not read file contents or generate embeddings.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
