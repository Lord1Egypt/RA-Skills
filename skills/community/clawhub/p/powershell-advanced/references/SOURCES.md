# PowerShell Advanced — Sources

Official and primary references used to build this skill:

- about_Parsing (PowerShell 7.5): https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5
- about_Try_Catch_Finally: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5
- about_Jobs: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_jobs?view=powershell-7.5
- about_Classes: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_classes?view=powershell-7.5
- about_Execution_Policies: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5
- ForEach-Object -Parallel: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object?view=powershell-7.5
- ProcessStartInfo.ArgumentList: https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo.argumentlist
- PSScriptAnalyzer: https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview
- Pester: https://pester.dev/docs/quick-start

Local verification:

```text
PowerShell 7.6.7
Test: Invoke-SafeProcess.ps1 against cmd.exe
Result: exit_code=0, stdout="advanced", stderr="err"
Test: parallel.ps1
Result: 12 items, throttle behavior observed
```

Notes:

- `about_Parsing` and `about_Try_Catch_Finally` were fetched live on 2026-10-20.
- Other links are the canonical Microsoft Learn modules; the local examples were tested on this machine.
- PowerShell 5.1 behavior differs; do not treat these examples as 5.1-compatible without testing.
