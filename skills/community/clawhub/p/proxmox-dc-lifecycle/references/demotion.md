# Demotion

Demote the target DC **from inside its own guest** via QGA. Do not remote from another DC (see gotchas: `0x8009030e`).

## Pre-flight
- Confirm the target holds no FSMO and is not the last DC (`verification.md`).
- Snapshot the VM (`qm snapshot`).
- Have ready: a domain credential in Domain/Enterprise Admins, the new local-admin password for the resulting member server (often the same value), and the target's identity.
- Validate the credential first with an explicit bind so you don't chase a context error later:
  ```powershell
  $de = New-Object System.DirectoryServices.DirectoryEntry("LDAP://<fsmoDC-fqdn>",$u,$p); $de.NativeObject  # throws if bad
  Get-ADPrincipalGroupMembership $acct | Select -Expand Name  # expect Domain/Enterprise Admins
  ```

## Graceful demotion (preferred)

Because QGA runs as SYSTEM, run the uninstall in a **scheduled task as the domain admin** to avoid LDAP error 58 (see qga-execution.md). The task script reads creds from a locked temp file and deletes it first.

Required parameters that prevent the known hangs/failures:
- `-LocalAdministratorPassword <SecureString>` — else it prompts and blocks under NonInteractive.
- `-RemoveDnsDelegation:$false` — else it stalls on external parent DNS (Cloudflare etc.) it can't reach.
- `-SkipPreChecks` — skips the `Test-` phase that has hung in the field.
- `-Force -NoRebootOnCompletion` — no reboot prompt; you control the reboot after verifying.

The cmdlet (run as the domain-admin task principal, inside the target guest):
```powershell
Import-Module ADDSDeployment
Uninstall-ADDSDomainController `
  -Credential $cred `
  -LocalAdministratorPassword $laSec `
  -RemoveDnsDelegation:$false `
  -SkipPreChecks -Force -NoRebootOnCompletion `
  -WarningAction SilentlyContinue -ErrorAction Stop
```
Run a `-WhatIf` version first to confirm parameters resolve without the long live-prereq checks.

Scheduled-task scaffolding (classic schtasks, NOT the CIM cmdlets — see `0x80070008` gotcha): write the demote script + a locked cred file into `C:\Windows\Temp\.hdc\`, then create the task **without the password on the command line**.

> **Never use `/rp "<password>"`.** A literal password in the `schtasks` arguments lands in the process list, the task XML, and shell history — and contradicts this skill's secrets-only-via-stdin rule. Instead pass `/rp *`, which makes `schtasks` read the run-as password from **stdin**; feed it the same way you feed every other secret here (the QGA `--pass-stdin` channel). The password never appears as an argument.

```powershell
# inside the guest, $taskPw holds the domain-admin password read from stdin (NOT a literal).
# Pipe it to schtasks' /rp * prompt:
$taskPw | schtasks /create /tn HDC_Demote /ru "<DOMAIN>\Administrator" /rp * /rl HIGHEST `
  /sc ONCE /st 00:00 /tr "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Windows\Temp\.hdc\run.ps1" /f
schtasks /run /tn HDC_Demote
```
Poll for completion via a status/marker file the script appends to; then `schtasks /delete /tn HDC_Demote /f` and wipe the temp dir (its locked cred file should already be deleted as the run script's first action).

## Forced removal (only if graceful is impossible)

Only after intentionally taking the DC offline, and knowing you'll do metadata cleanup immediately after:
```powershell
Uninstall-ADDSDomainController -ForceRemoval -DemoteOperationMasterRole -Force `
  -LocalAdministratorPassword $laSec -RemoveDnsDelegation:$false
```
`-ForceRemoval` converts the box to a standalone server locally but does **not** clean metadata on surviving DCs — you MUST then run `metadata-cleanup.md`.

## Verify (gate)
From a surviving DC: target absent from `Get-ADDomainController`, no `nTDSDSA` object for it, `repadmin /replsummary` still `0 fails` among remaining DCs. If those hold, demotion is effectively done even if the target's local OS is now broken.
