## Description:

CLI agent for MEGA.nz operations including upload, download, sync, scheduled backups, public links, FUSE mounting on Linux, WebDAV/FTP serving, and account management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alefsanderribeiro](https://clawhub.ai/user/alefsanderribeiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users can use this skill to have an agent operate MEGAcmd for MEGA.nz file transfer, sync, backup, sharing, diagnostics, and account workflows. It is intended for MEGAcmd users, not for building or debugging the MEGAcmd source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MEGAcmd account credentials, MFA codes, session IDs, recovery keys, proxy passwords, and link passwords can be exposed through chat, inline commands, process listings, shell history, or logs.

Mitigation: Use interactive login or protected secret handling, avoid placing secrets in chat or command arguments, and never include secret values in scripts or reports.

Risk: The skill can guide destructive or high-impact cloud operations including delete, password or session changes, sync setup, backups, public links, writable shares, and account cancellation.

Mitigation: Require explicit user confirmation before high-impact operations and verify target paths, account identity, and expected effects before execution.

Risk: Public links, writable shares, WebDAV, and FTP can expose MEGA content beyond the intended audience, and non-TLS services can expose data in transit.

Mitigation: Prefer password protection, expiration dates, minimum sharing permissions, TLS where available, localhost-only services unless necessary, and stop network services when no longer needed.

Risk: Bidirectional sync and troubleshooting commands can affect both local files and MEGA cloud state.

Mitigation: Review sync direction, IDs, ignore rules, and file paths before changes, and confirm any local delete or conflict-resolution command before running it.

## Reference(s):

- [MEGAcmd Skill Page](https://clawhub.ai/alefsanderribeiro/skills/megacmd)
- [README](README.md)
- [README pt-BR](README.pt-BR.md)
- [MEGAcmd Complete Command Reference](references/complete-commands-reference.md)
- [MEGAcmd Complete Command Reference pt-BR](references/comandos-completos.pt-BR.md)
- [MEGAcmd Releases](https://mega.nz/cmd)
- [MEGA Help Center](https://mega.nz/help)
- [MEGAcmd User Guide](https://github.com/meganz/MEGAcmd/blob/master/UserGuide.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MEGAcmd commands that affect cloud files, account sessions, sharing, sync, backups, and local network services.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
