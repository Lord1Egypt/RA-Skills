## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jash2368-collab](https://clawhub.ai/user/jash2368-collab)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to design, create, validate, package, and iterate on agent skills with reusable instructions, references, scripts, and assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can create directories, write files, and produce archives in user-selected locations.

Mitigation: Run the scripts only in trusted workspaces on skill names and paths you control; avoid absolute paths and parent-directory path components.

Risk: Packaging an untrusted skill folder can include unexpected local content in a .skill archive.

Mitigation: Package only trusted skill folders and inspect the directory contents, including symlinks, before creating an archive.

## Reference(s):

- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)
- [ClawHub skill page](https://clawhub.ai/jash2368-collab/skills/pro)
- [ClawHub publisher profile](https://clawhub.ai/user/jash2368-collab)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local skill directories, example resource files, validation messages, and .skill archives when its bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
