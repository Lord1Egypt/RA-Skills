## Description:

Chain PowerShell commands safely without &&. Use try/catch, ErrorAction, and proper sequencing for reliable Windows execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when writing or reviewing PowerShell scripts that chain commands, perform file operations, or need explicit fail-fast error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for many PowerShell-related tasks and influence file deletion, overwrite, or process-management commands.

Mitigation: Review generated commands before execution, especially commands that remove files, overwrite content, or stop processes.

Risk: Generated PowerShell examples can still be incorrect for a specific environment even when they follow safer chaining patterns.

Mitigation: Test scripts in a controlled shell and confirm paths, parameters, and error handling before production use.

## Reference(s):

- [PowerShell Safe Chain on ClawHub](https://clawhub.ai/dalomeve/skills/powershell-safe-chain)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown guidance with PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces safer PowerShell sequencing patterns and review criteria for generated scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
