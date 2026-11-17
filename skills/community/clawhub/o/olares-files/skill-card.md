## Description:

Olares Files helps agents guide users through olares-cli files commands for listing, uploading, downloading, editing, sharing, SMB mounts, ownership changes, and Sync repository operations on an Olares system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill to help manage files and shares on Olares through olares-cli while respecting path, namespace, authentication, and confirmation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers high-impact file operations such as deletion, moving, ownership changes, repository removal, unmounting, and overwrite-capable transfers.

Mitigation: Confirm the target path, operation, and expected effect with the user before proposing state-changing commands, and prefer listing or preflight checks before mutation.

Risk: Public-share and SMB actions can expose folders or credentials if recipients, permissions, passwords, or expiration settings are wrong.

Mitigation: Review target folders, recipients, permissions, expiration, and password handling before sharing; prefer generated or strong passwords and stdin or prompts over command-line passwords.

Risk: Incorrect Olares namespace or path syntax can cause failed commands or operations against the wrong file or directory.

Mitigation: Preserve case-sensitive frontend paths, trailing-slash intent, and namespace allow-lists, and use olares-cli files verb help plus relevant reference material before composing commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/olares/skills/olares-files)
- [files ls](references/olares-files-ls.md)
- [files upload](references/olares-files-upload.md)
- [files download](references/olares-files-download.md)
- [files edit](references/olares-files-edit.md)
- [files mkdir](references/olares-files-mkdir.md)
- [files rm](references/olares-files-rm.md)
- [files cp / files mv](references/olares-files-cp-mv.md)
- [files rename](references/olares-files-rename.md)
- [files chown](references/olares-files-chown.md)
- [files share](references/olares-files-share.md)
- [files smb](references/olares-files-smb.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires olares-cli and an active Olares account context; guidance should confirm high-impact file, sharing, SMB, and ownership actions before execution.]

## Skill Version(s):

4.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
