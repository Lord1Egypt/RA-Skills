# Promotion (rejoin + re-promote as replica DC)

Run inside the freshly installed guest via QGA. Unlike `Uninstall-ADDSDomainController`, the promotion cmdlet authenticates to the domain itself with the supplied `-Credential`, so it does NOT hit the SYSTEM/LDAP-error-58 trap — running it as SYSTEM with `-Credential` is fine.

**The decisive prerequisite is trust, not the launch mechanism** (this is what bit us on the DC2 rebuild). Get §0 right first — a properly-joined, trusted computer account. Once trust is good, the promotion works whether you run it directly via QGA or via a scheduled task. Before trust is established, BOTH fail: a scheduled task with `/ru DOMAIN\user` errors "The trust relationship ... failed" (no domain membership), and a direct attempt errors "security database ... does not have a computer account for this workstation trust relationship." So don't chase the launch method — fix §0.

**Detached execution — what actually works (and what doesn't):**
- `Start-Job` inside a `qm guest exec` call does NOT survive: the job is a child of the QGA powershell process and is torn down when that call returns. It launched but never ran (status stuck at "LAUNCHER start"). Avoid it for long operations.
- A **classic scheduled task** (`schtasks /create ... /sc ONCE /st <future> ; schtasks /run`) IS properly detached and survives the QGA call returning — this is what completed the DC2 promotion. Use it (once trust exists), or run a single synchronous `qm guest exec` with a long `--timeout` (promotion can finish in ~1 min on a small directory, but budget more).
- Either way, write progress to a marker file the launched script appends to, and poll it from the host.

## 0. Establish a clean computer account FIRST (fresh-wipe rebuilds)
The promotion needs the box to be a **properly-trusted domain member**. How much work this takes depends on a choice made back during metadata cleanup:

- **BEST — keep the computer object during cleanup.** If you deleted only the empty `CN=<DC>` *server* object under Sites and **left the computer object** in `CN=Computers` (where a graceful demote puts it), then after the OS reinstall the box comes up already trusted: `Test-ComputerSecureChannel` returns `True` with no repair needed. This is what DC3 did — promotion proceeded straight away. Prefer this: at cleanup time, delete the server-object shell but NOT the computer object.
- **REPAIR — if the computer object was deleted** (as on DC2), `Install-ADDSDomainController` fails with "security database ... trust relationship" and the box is stuck half-joined (`PartOfDomain=True` but `Test-ComputerSecureChannel=False`). Fix:
  1. Prestage on a surviving DC: `New-ADComputer -Name <DC> -SAMAccountName "<DC>$" -Enabled $true -Path "CN=Computers,<domainDN>"`.
  2. On the target: `Reset-ComputerMachinePassword -Credential $cred`, then **reboot**.
  3. Verify: `Test-ComputerSecureChannel` = `True`, `nltest /sc_query:<domain>` = `NERR_Success`.

Either way, confirm `Test-ComputerSecureChannel = True` before promoting. (Note: a fresh install may report `PartOfDomain=True` from the unattend's DNS suffix even without real trust — always check the secure channel, not just PartOfDomain.)

## 1. Point DNS at a healthy DC (so it can find the domain)
The unattend already set DNS to DC1 (`<dns-dc-ip>`). Confirm name resolution of the domain:
```powershell
Resolve-DnsName <domain> -Type SOA -Server <dns-dc-ip>
nltest /dsgetdc:<domain>
```

## 2. Install the AD DS role
```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
```

## 3. Promote as an additional (replica) domain controller
Supply domain creds + the DSRM (Directory Services Restore Mode) password. Reuse the same DNS-delegation skip as demotion. If a prior promotion attempt failed, **reboot the target first** to clear any half-completed dcpromo state before retrying. Launch it detached (scheduled task or long synchronous call — see the header; `Start-Job` does not survive).
```powershell
Import-Module ADDSDeployment
Install-ADDSDomainController `
  -DomainName "<domain>" `
  -Credential $cred `
  -SafeModeAdministratorPassword $dsrmSec `
  -InstallDns:$true `
  -CreateDnsDelegation:$false `
  -NoGlobalCatalog:$false `
  -SiteName "Default-First-Site-Name" `
  -Force -NoRebootOnCompletion:$false
```
- `-InstallDns:$true` matches the other DCs (they're DNS servers). `-CreateDnsDelegation:$false` for the same external-parent-DNS reason as demotion.
- `-NoGlobalCatalog:$false` ⇒ make it a GC (siblings are GCs here).
- It reboots on completion; wait for the guest agent to return.

## 4. Post-promotion DNS
Once it's a DC and DNS server, set its DNS to **itself first, then a partner** (best practice avoids island-mode):
```powershell
Set-DnsClientServerAddress -InterfaceAlias Ethernet -ServerAddresses <dc-subnet>.x,<dns-dc-ip>
```
(its own IP first, DC1 second).

## 5. Verify (gate)
From the new DC and from DC1:
```powershell
Get-ADDomainController -Filter * | Select Name,IPv4Address,IsGlobalCatalog   # new DC present
repadmin /replsummary                                                         # 0 fails, new DC both directions
Get-SmbShare | ? Name -in 'SYSVOL','NETLOGON'                                  # shares present
dcdiag                                                                         # clean (DFSR initial-sync warnings OK briefly)
netdom query fsmo                                                              # unchanged — all still on the FSMO holder
```
Force a sync to speed convergence: `repadmin /syncall /AdeP`. DFSR SYSVOL may show `State=2` (initial sync) for a bit before `4` (Normal).

## 6. Finalize
Detach install ISOs, set boot to disk, delete temp cred files and the unattend ISO, update any inventory/memory notes. Only now move to the next DC.
