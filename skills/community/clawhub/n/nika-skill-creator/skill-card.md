## Description:

Create or update Nika platform skills (main doc + sub docs) that follow Nika constraints (two-level docs, @sub-doc references, no path/extension references). Use when user asks to make a Nika skill, refactor an existing one to Nika format, or validate a Nika skill draft; also useful to output documents that can be pasted into Nika.

This skill is ready for commercial/non-commercial use.

## Publisher:

[typewrong](https://clawhub.ai/user/typewrong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, refactor, and validate Nika platform skill drafts with two-level documentation, defined input/output contracts, and reusable subdocuments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can write or overwrite files in a user-selected filesystem location.

Mitigation: Run it only in a workspace intended for Nika skill creation, check the destination before execution, and avoid --force unless overwriting is intentional.

Risk: Unexpected output directories could place generated skill files outside the intended project area.

Mitigation: Use project-relative output directories and avoid absolute paths or parent-traversal path components.

## Reference(s):

- [Nika Skill Constraints](references/nika-spec.md)
- [Main Document Template](references/main-doc-template.md)
- [Sub-document Template](references/sub-doc-template.md)
- [Validation Checklist](references/validation-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/typewrong/skills/nika-skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional generated files and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or validate Nika skill Markdown files in a user-selected workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
