## Description: <br>
Control the Windows PC from WSL2 for opening and closing applications, managing processes, taking screenshots, controlling windows, managing Windows files, and automating host tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Amirgu](https://clawhub.ai/user/Amirgu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill when an agent running in WSL2 needs to control the Windows host, inspect running applications, launch programs, capture screenshots, or work with files under Windows paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad Windows host control from WSL2, including PowerShell and cmd commands, screenshots, process termination, and access to Windows user directories. <br>
Mitigation: Install it only when host control is intended, review sensitive commands before execution, and use precise requests so the agent does not affect private data or unsaved work unintentionally. <br>


## Reference(s): <br>
- [Common Windows App Executable Names](references/windows-apps.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline bash, cmd, and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may interact with Windows applications, processes, screenshots, and files through WSL2 interop.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
