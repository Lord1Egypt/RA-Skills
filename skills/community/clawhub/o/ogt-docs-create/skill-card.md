## Description:

Create new documentation entities in the docs-first system. Routes to specialized creation sub-skills for tasks, definitions, rules, features, and social content. Use when adding any new documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduardou24](https://clawhub.ai/user/eduardou24)

### License/Terms of Use:


## Use Case:

Developers and documentation maintainers use this skill to create tasks, definitions, rules, feature docs, social content, and changelog entries in a docs-first repository structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample shell commands and batch scripts can create files outside intended documentation folders if names or paths are not validated.

Mitigation: Validate slugs, quote path variables, and review generated paths before running copied shell snippets.

Risk: Template examples include TODO placeholders that can remain in final documentation if not reviewed.

Mitigation: Run the documented checklist and section checks, then remove placeholder content before publishing created documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with example shell commands and document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes folder conventions, template outlines, validation checks, and batch-creation examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
