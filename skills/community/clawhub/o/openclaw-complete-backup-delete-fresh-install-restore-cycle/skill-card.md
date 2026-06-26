## Description: <br>
A runbook-style skill for backing up, deleting, reinstalling, and restoring OpenClaw installations, including full-cycle and selective restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators responsible for OpenClaw instances use this skill as a disaster-recovery runbook to create backups, perform clean reinstall cycles, and restore or selectively restore configuration, credentials, and agent state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runbook includes high-impact destructive and privileged commands that can remove or overwrite OpenClaw state. <br>
Mitigation: Review each command before execution, test the restore path in a sandbox, verify backups before any delete or restore step, and prefer moving old state aside before permanent deletion. <br>
Risk: Backups may contain credentials and API keys. <br>
Mitigation: Protect backup directories with strict permissions or encryption and restore only the credential material that is intentionally needed. <br>
Risk: The workflow includes a curl-to-shell install path. <br>
Mitigation: Use that path only after independently trusting and verifying the source; prefer package-manager or pinned installation methods where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefanferreira/openclaw-complete-backup-delete-fresh-install-restore-cycle) <br>
- [OpenClaw install script](https://cli.openclaw.ai/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown runbook with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes staged backup, clean install, restore, verification, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
2.2.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
