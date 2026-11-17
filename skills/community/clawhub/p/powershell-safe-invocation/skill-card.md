## Description:

在 Windows 上编写或运行 PowerShell 时使用，尤其适用于原生命令调用、带空格路径和引号、参数转义、pwsh、Start-Process、文件操作以及 Shell 故障排查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssesweb](https://clawhub.ai/user/ssesweb)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和工程师可用此技能编写或排查 PowerShell 命令，安全处理原生命令参数、引号、路径、文件操作及不同 PowerShell 版本的差异。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review flagged advice to use a full-access context, and the scan did not fully inspect all release components.

Mitigation: Review the full-access recommendation and decide whether the task can be done without it; inspect the incompletely scanned content before relying on the skill.

## Reference(s):

- [PowerShell Safe Invocation Reference](artifact/reference.md)
- [ClawHub release](https://clawhub.ai/ssesweb/skills/powershell-safe-invocation)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with PowerShell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows-specific guidance and cross-platform fallback notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
