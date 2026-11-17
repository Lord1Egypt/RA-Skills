## Description:

Process local files with batch rename, format conversion, organization by date, type, or metadata, duplicate detection, and metadata read, write, or removal workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:


## Use Case:

Developers and power users use this skill to have an agent prepare local file-processing workflows for renaming, converting, organizing, finding duplicates, and managing metadata on user-selected files and folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File rename, conversion, duplicate deletion, and metadata edits can modify or remove local files.

Mitigation: Use dry-run first on important folders, avoid force or overwrite unless backups exist, and rely on confirmation prompts for destructive actions.

Risk: The workflow depends on local Homebrew-installed tools for media and metadata operations.

Mitigation: Confirm the required dependencies are trusted and installed from expected sources before running generated commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ppopen/skills/openclaw-skill-local-file-processor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command flags such as dry-run, overwrite, force, recursive traversal, output format, quality, metadata keys, and destination directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
