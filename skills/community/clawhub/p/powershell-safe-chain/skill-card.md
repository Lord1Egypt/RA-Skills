## Description: <br>
Chain PowerShell commands safely without &&. Use try/catch, ErrorAction, and proper sequencing for reliable Windows execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when writing PowerShell scripts that chain commands, perform file operations, or need explicit fail-fast error handling on Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PowerShell could delete files, stop processes, or otherwise modify system state if run without review. <br>
Mitigation: Review commands before execution, use fail-fast error handling, and prefer preview modes such as -WhatIf when available. <br>
Risk: PowerShell scripts can expose sensitive values if credentials are hardcoded or printed. <br>
Mitigation: Avoid hardcoded credentials, use SecureString for passwords where appropriate, and pass configuration through approved environment or secret handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dalomeve/powershell-safe-chain) <br>
- [Publisher profile](https://clawhub.ai/user/Dalomeve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users should review generated PowerShell before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
