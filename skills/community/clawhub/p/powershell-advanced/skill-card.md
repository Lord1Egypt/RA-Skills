## Description:

Provides advanced PowerShell 7 and Windows PowerShell guidance for parsing, quoting, process handling, error handling, parallel jobs, JSON and HTTP, encoding, Windows administration, testing, and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and engineers use this skill to troubleshoot advanced PowerShell behavior and build scripts for native processes, parallel work, HTTP and JSON, and Windows-specific tasks. It is especially useful when quoting, output capture, or job execution behaves unexpectedly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process output handling may hang or behave unreliably when stdout and stderr are read sequentially.

Mitigation: Use concurrent or asynchronous stream reads, and verify process handling under expected output volumes before production use.

Risk: Timeout cleanup may not fully stop a child process or its descendants.

Mitigation: Bound cleanup behavior and confirm the process tree has exited before relying on timeout handling in production.

Risk: HTTP examples could expose credentials or send them to an unintended endpoint.

Mitigation: Keep tokens out of logs and send them only to intended HTTPS endpoints.

Risk: Examples that change permissions or execution settings may have persistent effects.

Mitigation: Review permission changes before running examples.

## Reference(s):

- [PowerShell Advanced on ClawHub](https://clawhub.ai/deepseekoracle/skills/powershell-advanced)
- [about_Parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5)
- [about_Try_Catch_Finally](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5)
- [about_Jobs](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs?view=powershell-7.5)
- [ForEach-Object -Parallel](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object?view=powershell-7.5)
- [ProcessStartInfo.ArgumentList](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.argumentlist)
- [PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview)
- [Pester](https://pester.dev/docs/quick-start)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with PowerShell examples and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples target PowerShell 7 unless stated otherwise; verify compatibility before using them with Windows PowerShell 5.1.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
