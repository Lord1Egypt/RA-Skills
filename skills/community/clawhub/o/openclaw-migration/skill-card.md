## Description:

Guides the renaming of the Clawd project to OpenClaw by detailing file moves, updates, testing, and documentation steps for consistent migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill as a migration playbook when renaming the Clawd project to OpenClaw, updating references, moving project metadata, and validating tooling after the rename.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-wide renames and directory moves can break scripts, workspace references, CI workflows, or documentation links if applied without verification.

Mitigation: Use this skill in a Clawd/OpenClaw repository branch, preview replacements before applying them, keep the old directory until the new layout is verified, and run the listed tests and lint checks before cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyuan99/skills/openclaw-migration)
- [Publisher profile](https://clawhub.ai/user/chenyuan99)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklist steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration planning, validation, and communication guidance for repository maintainers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
