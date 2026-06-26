## Description: <br>
Dragon-class High Availability (HA) guardian with metabolic cleansing and 3-tier self-healing for OpenClaw environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxleolee-eng](https://clawhub.ai/user/maxleolee-eng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to maintain an OpenClaw workstation with heartbeat monitoring, scheduled maintenance, backups, recovery scripts, and guided restoration after local OpenClaw failures. It is intended for macOS and Linux environments where the user intentionally wants a persistent local guardian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guardian can run persistently and make broad changes to the local OpenClaw environment. <br>
Mitigation: Review and edit the shell scripts before installation, test on a non-critical machine, and confirm the terminate workflow before enabling the LaunchAgent or background process. <br>
Risk: Recovery scripts include force-kill, cache removal, package reinstall, rollback, and rsync-based restore behavior that can overwrite or remove local state. <br>
Mitigation: Create an independent backup, verify source and target paths, and run destructive recovery scripts only after confirming the intended OpenClaw instance and workspace. <br>
Risk: Some artifact scripts contain hard-coded user paths and assumptions about local OpenClaw layout. <br>
Mitigation: Replace hard-coded paths with the target user's paths or environment variables before execution. <br>
Risk: Backup scripts may copy authentication profile files into local vaults. <br>
Mitigation: Protect backup directories with appropriate filesystem permissions or exclude sensitive auth-profile backups when they are not required. <br>
Risk: The resurrection flow installs the latest global OpenClaw package, which may change behavior across releases. <br>
Mitigation: Pin package versions and validate compatibility before using the reinstall path in a production or long-lived workstation. <br>


## Reference(s): <br>
- [Openclaw Sys Guardian V4.1 Resurrection on ClawHub](https://clawhub.ai/maxleolee-eng/openclaw-sys-guardian-v4-1-resurrection) <br>
- [Product Manual](PRODUCT_MANUAL.md) <br>
- [Skill Guide](SKILL_GUIDE.md) <br>
- [Architecture](references/Architecture.md) <br>
- [Design](references/Design.md) <br>
- [Design V4.5](references/Design_V4.5.md) <br>
- [Full Manual](references/FullManual.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and bundled shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets local macOS and Linux OpenClaw environments; scripts may run persistently, modify configuration, manage processes, restore files, and reinstall packages.] <br>

## Skill Version(s): <br>
4.1.7 (source: server release metadata; artifact frontmatter reports 4.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
