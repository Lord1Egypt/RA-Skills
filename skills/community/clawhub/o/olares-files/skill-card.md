## Description: <br>
Olares Files helps agents manage files on an Olares system through `olares-cli files`, including listing, upload, download, editing, copy and move, deletion, ownership changes, sharing, SMB mounts, and Sync repository operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Olares users, developers, and operators use this skill to plan and run `olares-cli files` commands against the active Olares profile for remote file management, sharing, SMB mounting, and Sync repository maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands operate with the active Olares profile and may use sensitive credentials. <br>
Mitigation: Confirm the intended Olares profile before use and never expose access tokens, refresh tokens, or SMB passwords in terminal output or command history. <br>
Risk: Delete, move, ownership, share, SMB, and repository operations can materially change remote data or access. <br>
Mitigation: Confirm target paths, recipients, permissions, passwords, expirations, and network trust before running mutating commands. <br>
Risk: Uploads, copies, moves, and edits can overwrite or replace remote file contents. <br>
Mitigation: Verify destination paths and use preflight listing or existing CLI safeguards before operations that could clobber data. <br>


## Reference(s): <br>
- [files ls](references/olares-files-ls.md) <br>
- [files upload](references/olares-files-upload.md) <br>
- [files download](references/olares-files-download.md) <br>
- [files edit](references/olares-files-edit.md) <br>
- [files mkdir](references/olares-files-mkdir.md) <br>
- [files rm](references/olares-files-rm.md) <br>
- [files cp / files mv](references/olares-files-cp-mv.md) <br>
- [files rename](references/olares-files-rename.md) <br>
- [files chown](references/olares-files-chown.md) <br>
- [files share](references/olares-files-share.md) <br>
- [files smb](references/olares-files-smb.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are scoped to the active Olares profile and may require confirmation for mutating operations.] <br>

## Skill Version(s): <br>
4.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
