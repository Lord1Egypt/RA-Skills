## Description:

Helps agents write and troubleshoot PECMD2012 WinPE scripts for lightweight Windows GUI tools, system utilities, boot and startup automation, disk and registry tasks, and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtualhotbar](https://clawhub.ai/user/virtualhotbar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and troubleshoot PECMD2012 scripts for WinPE automation, GUI utilities, startup initialization, disk partitioning, registry work, process control, and system information collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts may include privileged WinPE or administrator operations such as disk partitioning, registry edits, process termination, shutdown, shell changes, network configuration, direct DLL calls, or DeviceIoControl calls.

Mitigation: Review generated scripts before running them, test in a VM or disposable PE image, and back up disks and registry hives before applying changes.

Risk: Generated examples can expose sensitive network settings or credentials, especially in ADSL or WiFi connection patterns.

Mitigation: Avoid hardcoded credentials and use runtime input or operator-provided values for secrets.

Risk: Dynamic script evaluation patterns can execute untrusted file content.

Mitigation: Do not copy the rules.ini dynamic-evaluation pattern for untrusted files; validate and constrain external script or configuration input before loading it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/virtualhotbar/skills/pecmd-pro-max)
- [PECMD2012 interpreter](https://pecmd.net)
- [PECMD command reference](references/commands-full.md)
- [PECMD GUI reference](references/pecmd-gui.md)
- [WinPE startup reference](references/pe-startup.md)
- [Storage, registry, and device how-tos](references/how-tos/storage.md)
- [System, process, and thread how-tos](references/how-tos/system.md)
- [GUI how-tos](references/how-tos/gui.md)
- [Network, SOCK, COM, and WMI how-tos](references/how-tos/net.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with PECMD script snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged WinPE commands that require human review before execution.]

## Skill Version(s):

1.7.1 (source: ClawHub release metadata; artifact frontmatter shows 1.5.5 and README badge shows 1.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
