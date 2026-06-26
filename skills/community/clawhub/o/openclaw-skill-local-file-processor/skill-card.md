## Description: <br>
Process local files with batch rename, format conversion, organization by date, type, or metadata, duplicate detection, and metadata read, write, or removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and other users working with local files use this skill to perform common batch file operations such as renaming, conversion, organization, duplicate handling, and metadata updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented commands can rename, move, overwrite, or delete local files, including recursive operations and duplicate deletion. <br>
Mitigation: Use --dry-run first, scope commands to specific folders, avoid --force and --overwrite unless intentional, and keep backups for important directories. <br>
Risk: Metadata operations can write or remove file metadata. <br>
Mitigation: Preview metadata changes, verify target globs and keys before execution, and require confirmation for write or delete operations unless --force is intentionally used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-local-file-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include dry-run, overwrite, force, recursive, path, format, quality, metadata key, duplicate action, and destination options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
