---
name: powershell-advanced
description: "Advanced PowerShell 7 / Windows PowerShell workarounds on Windows: parsing and quoting, native argument passing, error handling, reliable process capture, parallel jobs, JSON/HTTP, encoding, ACLs, scheduled tasks, modules, Pester, and Windows-specific debugging. Use when a basic one-liner fails, output deadlocks, quoting breaks, a job hangs, or a script must be safe enough to ship."
category: devops
---

# PowerShell Advanced

Audited environment: **PowerShell 7.6.7** (`C:\Program Files\PowerShell\7\pwsh.exe`) and Windows PowerShell 5.1 (`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`).

## 0. Know which engine you are in

```powershell
$PSVersionTable
$PSVersionTable.PSEdition          # Core or Desktop
[Environment]::Is64BitProcess
$PSHOME
```

Rules:

- Write for **PowerShell 7** unless the target is explicitly 5.1.
- `pwsh` and `powershell.exe` are different engines with different JSON, encoding, and parallel behavior.
- Do not assume a module installed for 5.1 is visible in 7 (or the reverse).
- `$PSVersionTable.PSVersion.Major -ge 7` gates `ForEach-Object -Parallel`, `ConvertFrom-Json -AsHashtable`, and `utf8NoBOM`.

## 1. Parsing and quoting

PowerShell has two modes: **expression** and **argument**. The same token can mean different things.

| Input | Mode | Result |
|---|---|---|
| `Write-Output 2+2` | argument | string `"2+2"` |
| `Write-Output (2+2)` | expression | integer `4` |
| `Write-Output $a+2` | argument | string, e.g. `"4+2"` |
| `Write-Output ($a+2)` | expression | integer `6` |

Practical rules:

- Put expressions in parentheses when passing to a command.
- Use single quotes for literal strings, double quotes for expansion.
- Escape `$` in an expandable string with a backtick: `` "`$HOME" ``.
- Do **not** use backtick line continuation when a natural break exists (after `|`, `,`, `(`, `{`, an operator). Use splatting for many parameters.
- `--%` stops PowerShell parsing for a native command; use it only when needed and remember it stops at newline/pipe.
- `--` ends PowerShell parameters; for native commands it is usually passed through.
- `$PSNativeCommandArgumentPassing` (7.3+) changes native quote behavior. If a native call worked in 5.1 but breaks in 7, inspect this variable.

```powershell
# Preferred: splatting
$p = @{
    Path        = 'C:\Program Files\App\app.exe'
    ErrorAction = 'Stop'
}
Get-Item @p
```

## 2. Error handling

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    Get-Item -LiteralPath 'C:\missing' -ErrorAction Stop
}
catch [System.Management.Automation.ItemNotFoundException] {
    Write-Error "Not found: $($_.Exception.Message)"
}
catch {
    Write-Error ("{0}`n{1}" -f $_.Exception.Message, $_.ScriptStackTrace)
}
finally {
    # always runs, including on many terminating paths
}
```

Key facts:

- Cmdlets often emit **non-terminating** errors; `try/catch` will not see them unless `-ErrorAction Stop` or `$ErrorActionPreference='Stop'`.
- `throw` creates a terminating error.
- `$ErrorActionPreference='SilentlyContinue'` can suppress `throw`; do not use it globally in a library.
- `$?` and `$LASTEXITCODE` are not the same. `$LASTEXITCODE` is for native processes.
- `catch` matches exception type by inheritance; put specific catches before general ones.

## 3. Native process capture without deadlocks

The common failure: `& tool` with large stdout/stderr, or `Start-Process` with `-Wait` and redirected streams, hangs. Capture via `System.Diagnostics.Process` with `ArgumentList` for exact quoting.

Template: `scripts/Invoke-SafeProcess.ps1`.

```powershell
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = 'C:\Program Files\Git\bin\git.exe'
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
$psi.ArgumentList.Add('status')
$psi.ArgumentList.Add('--short')

$p = [System.Diagnostics.Process]::new()
$p.StartInfo = $psi
[void]$p.Start()
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$exit = $p.ExitCode
```

Rules:

- Use `ArgumentList`, not a hand-built argument string, when paths/quotes matter.
- Read stdout and stderr **before** `WaitForExit` for large output, or use async event handlers.
- For a child that may outlive the helper, redirect to files or `DEVNULL`; do not leave a pipe open.
- `Start-Process -Wait` waits for the process tree in some cases; `Wait-Process` waits for the process object only.
- `cmd /c` changes quoting; avoid it when a native exe can be called directly.

## 4. Parallelism: choose the right tool

| Need | Use |
|---|---|
| A few CPU-bound jobs, PS 7 | `ForEach-Object -Parallel -ThrottleLimit N` |
| Jobs needing separate runspaces | `Start-ThreadJob` |
| Child process isolation | `Start-Job` |
| Long-lived worker pool | `RunspacePool` |
| Native process concurrency | `Start-Process` + wait/handles |

```powershell
$items = 1..8
$results = $items | ForEach-Object -Parallel {
    Start-Sleep -Milliseconds 200
    [pscustomobject]@{ n = $_; pid = $PID }
} -ThrottleLimit 4
$results
```

Caveats:

- `-Parallel` scriptblocks run in separate runspaces; variables do not flow in automatically. Use `$using:name`.
- Do not mutate a shared `List` from parallel runspaces without a lock.
- Pipeline output ordering may differ.
- A hung child can hang the whole job; add timeouts at the native process layer.

## 5. JSON, HTTP, encoding

```powershell
$r = Invoke-RestMethod -Uri $url -Headers @{
    Authorization = "Bearer $env:TOKEN"
    Accept        = 'application/json'
} -TimeoutSec 30

$r | ConvertTo-Json -Depth 20
```

- Use `-Depth` when nesting is deeper than 2; the default truncates.
- PS 7: `ConvertFrom-Json -AsHashtable` gives a hashtable, not `PSCustomObject`.
- `Invoke-RestMethod` parses JSON automatically; use `Invoke-WebRequest` when you need raw bytes/status/headers.
- Do not log Authorization headers or tokens.
- TLS 1.2 is default in modern .NET; old 5.1 may need `[Net.ServicePointManager]::SecurityProtocol`.

Encoding:

```powershell
Set-Content -LiteralPath $path -Value $text -Encoding utf8NoBOM   # PS 7
Get-Content -LiteralPath $path -Raw -Encoding utf8
[IO.File]::WriteAllText($path, $text, [Text.UTF8Encoding]::new($false))
```

- 5.1 `-Encoding UTF8` writes a BOM; 7's `utf8NoBOM` does not.
- Use `-LiteralPath` for names containing `[ ] * ?`.
- Use `-Raw` to read a file as one string, not an array of lines.
- Use `[IO.Path]::GetFullPath` and `\\?\` for very long paths.

## 6. Advanced Windows workarounds

### Spaces, brackets, and quotes

```powershell
Get-Item -LiteralPath 'C:\Program Files (x86)\App [x64]\app.exe'
```

Do not use `-Path` with wildcard characters in literal paths.

### Elevation

```powershell
Start-Process -FilePath 'pwsh.exe' -Verb RunAs -ArgumentList @(
    '-NoProfile','-File','C:\path\script.ps1'
)
```

- UAC cannot be bypassed silently. If the task must run unattended, use a scheduled task with the right principal, not a fake elevation trick.
- Do not disable UAC or Defender to make a script work.

### Services, tasks, registry

```powershell
Get-Service -Name 'Spooler'
Get-ScheduledTask -TaskName 'Hermes_Gateway'
Get-CimInstance Win32_Process -Filter "ProcessId = 1234"
```

- Prefer `Get-CimInstance` over deprecated `Get-WmiObject`.
- Registry writes are persistent and risky; export the key first.
- Scheduled tasks are better than startup scripts for restartable services.

### ACLs

```powershell
$acl = Get-Acl -LiteralPath $path
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "$env:USERDOMAIN\$env:USERNAME", 'Modify', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
$acl.SetAccessRule($rule)
Set-Acl -LiteralPath $path -AclObject $acl
```

- Back up the ACL (`Get-Acl | Export-Clixml`) before changing it.
- Do not grant `Everyone`/`Users` broad write on system paths.

### Execution policy

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\script.ps1
```

- This is process-scoped. Do not change the machine policy to run one script.
- Sign production scripts; `Get-AuthenticodeSignature` verifies.

### Exit codes

```powershell
& tool.exe
if ($LASTEXITCODE -ne 0) { throw "tool failed: $LASTEXITCODE" }
```

- `$LASTEXITCODE` is set by native programs, not cmdlets.
- `exit $LASTEXITCODE` preserves it; `exit 0` hides failures.
- In a function, `return` does not set exit code.

## 7. Script skeleton

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputPath,
    [string]$OutPath = (Join-Path $PWD 'out.json')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
        throw "Input not found: $InputPath"
    }
    $data = Get-Content -LiteralPath $InputPath -Raw | ConvertFrom-Json
    $data | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $OutPath -Encoding utf8NoBOM
    Write-Output "OK $OutPath"
}
catch {
    Write-Error ("FAILED: {0}`n{1}" -f $_.Exception.Message, $_.ScriptStackTrace)
    exit 1
}
```

## 8. Testing and quality

```powershell
Invoke-ScriptAnalyzer -Path .\script.ps1 -Severity Warning,Error
Invoke-Pester -Path .\tests
```

- Pester 5 uses `Describe`, `Context`, `It`, `Should`.
- Test with a temporary directory and clean up in `finally`.
- Use `-WhatIf`/`-Confirm` only if the function supports `SupportsShouldProcess`.
- Avoid `Invoke-Expression` on user input; it is a code-injection primitive.

## 9. Troubleshooting table

| Symptom | Likely cause | Fix |
|---|---|---|
| `try/catch` never catches | non-terminating cmdlet error | `-ErrorAction Stop` or `$ErrorActionPreference='Stop'` |
| Native command gets wrong args | PowerShell re-parsed quotes | `ProcessStartInfo.ArgumentList` or `--%` |
| Script hangs on child output | pipe buffer full | read stdout/stderr before wait; redirect to files |
| `$LASTEXITCODE` is blank | last command was a cmdlet | check after native call only |
| JSON truncated | default `ConvertTo-Json` depth 2 | `-Depth 20` |
| UTF-8 file has BOM | 5.1 `-Encoding UTF8` | use .NET `UTF8Encoding(false)` or 7 `utf8NoBOM` |
| Path with `[ ]` not found | wildcard globbing | `-LiteralPath` |
| Parallel block cannot see variable | separate runspace | `$using:name` |
| Job survives shell | child inherits job object | scheduled task or detached process |
| `Start-Process` quoting wrong | single argument string | `ArgumentList` array / .NET |
| Script blocked by execution policy | policy | process-scoped `-ExecutionPolicy Bypass`, or sign |
| Module missing in 7 | installed for 5.1 only | install for the target engine |
| `Get-WmiObject` slow/deprecated | legacy WMI | `Get-CimInstance` |

## 10. Templates in this skill

- `scripts/Invoke-SafeProcess.ps1` — exact native args, separate stdout/stderr, timeout, JSON result.
- `templates/parallel.ps1` — throttled parallel runspace.
- `templates/http-json.ps1` — API call with timeout and no secret logging.

## Sources

- Microsoft Learn: `about_Parsing`, `about_Try_Catch_Finally`, `about_Jobs`, `about_Classes`, `about_Execution_Policies`.
- PowerShell 7.3 native argument passing notes.
- .NET `System.Diagnostics.ProcessStartInfo.ArgumentList`.

See `references/SOURCES.md`.
