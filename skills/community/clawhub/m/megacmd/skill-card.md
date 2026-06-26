## Description: <br>
CLI agent for MEGA.nz file upload, download, sync, backups, sharing, WebDAV/FTP serving, FUSE mounting, and account management through MEGAcmd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alefsanderribeiro](https://clawhub.ai/user/alefsanderribeiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to manage MEGA.nz cloud storage from an agent-assisted command-line workflow, including file transfer, synchronization, backups, sharing, diagnostics, and account operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-assisted MEGAcmd operations can delete, overwrite, synchronize, back up, or publicly share MEGA account data. <br>
Mitigation: Require explicit user confirmation for deletion, overwrite, sync, sharing, backups, mounts, account changes, and network service commands; verify local and remote paths before execution. <br>
Risk: Login credentials, session IDs, proxy credentials, and recovery keys can be exposed through command arguments, logs, shell history, or agent-visible output. <br>
Mitigation: Prefer interactive login or protected secret handling, avoid echoing or saving sensitive values, and store recovery keys only in encrypted or access-restricted storage. <br>
Risk: Public links, shared folders, WebDAV, and FTP can expose MEGA content beyond the intended audience. <br>
Mitigation: Use minimum necessary sharing permissions, passwords and expiration dates where available, TLS for network services, avoid public serving unless required, and stop services when no longer needed. <br>
Risk: Bidirectional sync and scheduled backups can propagate unintended local or remote changes. <br>
Mitigation: Confirm sync direction, backup targets, retention settings, and status output before and after changes; pause or remove sync configurations only after confirming the intended effect. <br>


## Reference(s): <br>
- [ClawHub MEGAcmd Skill Page](https://clawhub.ai/alefsanderribeiro/megacmd) <br>
- [MEGAcmd Complete Command Reference](references/complete-commands-reference.md) <br>
- [MEGAcmd Downloads](https://mega.nz/cmd) <br>
- [MEGA Help Center](https://mega.nz/help) <br>
- [MEGAcmd User Guide](https://github.com/meganz/MEGAcmd/blob/master/UserGuide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require local MEGAcmd installation, an authenticated MEGA account, network access, and explicit user confirmation for high-impact actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
