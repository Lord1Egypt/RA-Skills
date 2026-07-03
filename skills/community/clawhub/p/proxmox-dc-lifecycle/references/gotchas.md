# Gotchas — field-tested failure modes

Each entry: the **signature** (what you'll see), the **cause**, and the **fix**. Skim before starting; jump here the instant something hangs or errors. These are real failures from DC rebuilds, not hypotheticals.

## Demotion hangs "inside Test-ADDSDomainControllerUninstallation"
- **Signature:** the demotion never gets to the uninstall; `Test-ADDSDomainControllerUninstallation` sits forever, or `qm guest exec` returns a `{pid}`.
- **Cause:** usually a downstream prompt or a DNS-delegation stall (see next two entries), surfacing as an apparent hang in the test phase. The test cmdlet also does live prereq checks that can be slow.
- **Fix:** skip the test cmdlet and go straight to `Uninstall-ADDSDomainController -SkipPreChecks` with all required params supplied (see below). Run a `-WhatIf` first (it summarizes without the live checks) to confirm parameters resolve.

## Demotion stalls for minutes on DNS delegation (error 1722 / status 10060)
- **Signature:** `dcpromoui.log` shows `DnsRpcError: Status is 10060`, `Error 1722 deleting NS record`, `Delegation deletion failed ... against parent DNS server <something>.ns.cloudflare.com`. The operation appears hung.
- **Cause:** the demotion tries to delete the AD zone's DNS delegation on the **parent (public) nameservers**. If the parent zone lives on external DNS (Cloudflare, registrar, etc.) unreachable via Windows DNS RPC, it retries with long timeouts.
- **Fix:** pass **`-RemoveDnsDelegation:$false`** (and no `DnsDelegationRemovalCredential`). The delegation is managed out-of-band; dcpromo should not touch it.

## "Windows PowerShell is in NonInteractive mode"
- **Signature:** `Test-`/`Uninstall-ADDSDomainController` throws this immediately.
- **Cause:** a required interactive prompt — almost always the **local administrator password** for the resulting member server.
- **Fix:** supply **`-LocalAdministratorPassword (ConvertTo-SecureString <pw> -AsPlainText -Force)`** and `-Force`. Keep `-NonInteractive`; don't drop it.

## LDAP error 58 during demote/promote
- **Signature:** `Verification of user credential permissions failed ... LDAP connect/bind operation failed: error: 58`.
- **Cause:** the cmdlet runs as `NT AUTHORITY\SYSTEM` (via QGA) but is handed a `-Credential`; SYSTEM has no real logon session for it.
- **Fix (demote):** run the cmdlet via a **scheduled task whose run-as principal is the domain admin** (`schtasks /create /ru ... /rp *`, password via stdin), so it executes in a true logon session. (Promotion does NOT hit this — it self-authenticates; run it directly.) Validate the credential separately with a `DirectoryEntry` bind to rule out a bad password.

## WinRM/Remoting between DCs fails: 0x8009030e "A specified logon session does not exist"
- **Signature:** remote demotion driven from one DC to another dies before remote execution.
- **Cause:** SSPI/credential delegation across the remoting hop.
- **Fix:** don't remote between DCs at all. Run the operation **locally in the target guest** via QGA. This skill is built around that.

## Scheduled-task / CIM cmdlet fails: 0x80070008 "Not enough memory resources"
- **Signature:** `New-ScheduledTaskAction` / `Get-CimInstance` / `Restart-Computer` throw `0x80070008` even though RAM looks available.
- **Cause:** desktop-heap / WMI exhaustion after many churned PowerShell sessions, common on a low-RAM (4 GB) DC during a long troubleshooting session.
- **Fix:** **reboot the guest to reset the heap** (a healthy DC is safe to reboot; it resyncs). Use non-CIM tools that don't depend on the starved provider: `shutdown.exe /r /t 3 /f` instead of `Restart-Computer`; classic `schtasks.exe` instead of `*-ScheduledTask` cmdlets. Consider bumping the DC's RAM if it recurs.

## NTDS won't start after a botched/interrupted demotion
- **Signature:** box boots but AD is down. `net start NTDS` → error **1058** ("service disabled") OR error **3534**/"did not report an error". Other AD services may be fine.
- **Cause:** an interrupted forced removal left NTDS (and ADWS) set to **Disabled**, and/or deleted `ntds.dit`.
- **Diagnosis:** check the registry start type (`HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Start`: 2=Auto,3=Manual,4=Disabled) and whether `C:\Windows\NTDS\ntds.dit` exists.
  - If only Disabled (dit present): re-enable (`Set-Service NTDS -StartupType Automatic`) and start. Recoverable.
  - **If `ntds.dit` is MISSING:** the box was effectively force-demoted at the DB level. It can NOT come back as a DC by fixing services. Treat it as already-demoted locally and verify/clean the AD side (it may already be done), then rebuild the OS. This is good news for the rebuild path, not a disaster.

## A forced/interrupted removal that "already worked"
- **Signature:** the target's local AD is broken, but from a surviving DC the `nTDSDSA` object, DFSR member, and `_msdcs` records for it are already **gone**, and its computer object has moved from `OU=Domain Controllers` to `CN=Computers`.
- **Reading it:** that combination is the signature of a removal that **succeeded on the AD side** but left local OS debris. The prime-directive gate (no `nTDSDSA`) is already satisfied. You only need to delete the cosmetic residue (empty server object, computer object) and verify — then you're clear to rebuild. Don't re-run a demotion against a DC that AD no longer considers a DC.

## Promotion fails: "security database ... does not have a computer account for this workstation trust relationship"
- **Signature:** `Install-ADDSDomainController` runs for minutes then fails with "A domain controller could not be contacted ... that contained an account for this computer" / "trust relationship ... failed". From a surviving DC, `Get-ADComputer <DC>` finds nothing; on the target `Test-ComputerSecureChannel` is `False` but `PartOfDomain` is `True`.
- **Cause:** the target is a **freshly wiped** server whose old computer object was deleted during metadata cleanup. A failed promotion left it in an orphaned half-joined state: local secure-channel keys reference an AD account that doesn't exist. Windows' unjoin/repair tools refuse ("No mapping between account names and security IDs", "Cannot find the computer account") because the account is gone.
- **Fix (the sequence that works):**
  1. **Prestage** the computer account on a surviving DC: `New-ADComputer -Name <DC> -SAMAccountName "<DC>$" -Enabled $true -Path "CN=Computers,..."`.
  2. On the target, `Reset-ComputerMachinePassword -Credential $cred` (binds local machine secret to the prestaged account).
  3. **Reboot the target** — netlogon rebuilds the secure channel on boot. After reboot, `Test-ComputerSecureChannel` returns `True` and `nltest /sc_query:<domain>` shows `Status = 0 NERR_Success`.
  4. Retry `Install-ADDSDomainController` — now succeeds from the properly-trusted member.
- **Prevention:** for a fresh-wipe rebuild reusing a name whose computer object was deleted, keep the computer object during cleanup (delete only the server-object shell), or do a clean **domain join + reboot** BEFORE promoting. The join-and-promote-a-workgroup-box-in-one-shot path is what triggers this orphaned state.

## Unattend installs the wrong edition (Datacenter instead of Standard)
- **Signature:** post-install `(Get-WindowsEdition -Online).Edition` shows `ServerDatacenter*` when you specified Standard.
- **Cause:** Setup ignored the unattend's image selection and defaulted to Datacenter. On some Server 2025 Eval media this happened with BOTH `/IMAGE/NAME` (name mismatch) AND a correct `/IMAGE/INDEX=1` (= SERVERSTANDARDCORE per `wiminfo`). So index selection alone is NOT always sufficient — Setup may choose Datacenter regardless, likely due to an `ei.cfg`/`PID.txt` on the media or the `ImageInstall` block not being honored as expected for an eval WIM.
- **What actually controls it:** to truly force Standard you'd address the media-level default — e.g. remove/override `sources\ei.cfg`, or pre-`dism`-apply the specific index to the disk rather than relying on the unattend's `ImageInstall`.
- **Practical fix:** for a domain controller the edition is functionally irrelevant — **Datacenter Core is a licensing superset of Standard and behaves identically as a DC**. Accept it unless you specifically need Standard licensing; don't burn a reinstall over it. Still keep `/IMAGE/INDEX` in the unattend (it's the correct intent) and verify the result with `(Get-WindowsEdition -Online).Edition` + `InstallationType`.

## `Start-Job` inside a QGA call never runs (status stuck at launch)
- **Signature:** you launch a long op (e.g. promotion) via `Start-Job` inside `qm guest exec` so the call returns fast, but the marker file only shows the pre-job line ("LAUNCHER start") and never progresses; `Get-Job` shows nothing.
- **Cause:** the background job is a child of the `qm guest exec` powershell process. When that QGA call returns, its process tree (including the job) is torn down before the job does any work.
- **Fix:** detach with a **classic scheduled task** (`schtasks /create /sc ONCE /st <future> ; schtasks /run`) — it's owned by the task scheduler, not your QGA call — or run a single **long synchronous** `qm guest exec` (`--timeout` up to ~280s). Never `Start-Job` to outlive a QGA call.

## scheduled task `/ru DOMAIN\user` fails on a non-member box: "trust relationship failed"
- **Signature:** `schtasks /create /ru <DOMAIN>\Administrator /rp * ...` errors "The trust relationship between this workstation and the primary domain failed."
- **Cause:** the box isn't a domain member yet (fresh install, or trust broken), so Windows can't validate a *domain* principal for the task.
- **Fix:** establish membership/trust first (join + reboot, or the prestage/reset/reboot sequence). Then the domain-principal task works. For promotion specifically you don't need a domain-principal task at all — run `Install-ADDSDomainController` directly as SYSTEM with `-Credential` (it self-authenticates). See `qga-execution.md` (DEMOTE vs PROMOTE).

## Guest agent answers before the OS is actually ready
- **Signature:** right after starting an install or reboot, `qm guest cmd <vmid> ping` succeeds within seconds — far too fast for "done." A naive "wait for agent" loop reports success immediately.
- **Cause:** the QEMU guest agent can respond while Windows is still in OOBE or mid-boot (or the *previous* OS briefly answered before the wipe).
- **Fix:** don't treat agent reachability as completion. Confirm a real signal: install done = registry `...\Setup\State\ImageState` = `IMAGE_STATE_COMPLETE`; DC up = `NTDS` service Running + `ProductType=LanmanNT`; or a marker your own first-logon script wrote.

## `oobe_done.txt` / FirstLogonCommands marker doesn't appear
- **Signature:** install clearly finished (agent up, services running) but the `oobe_done.txt` marker the unattend was supposed to write is missing.
- **Cause:** `cmd /c echo ... > C:\file` redirects inside `FirstLogonCommands` can misfire (tokenization/escaping in the unattend XML, or context/perms).
- **Fix:** don't gate on the marker — use `ImageState=IMAGE_STATE_COMPLETE` as the authoritative signal. The template writes the marker with `powershell -Command "Set-Content ..."` (more robust than a cmd redirect) but treats it as secondary.

## dcdiag SystemLog fails right after a rebuild
- **Signature:** a freshly promoted/rebooted DC fails dcdiag's `SystemLog` test, citing recent System-log errors.
- **Cause:** `SystemLog` flags any Error in the last ~60 minutes — and a box built minutes ago has reboot/promotion/trust-repair churn (netlogon errors during repair, DNS-not-up-yet at boot, a one-shot service start failure from a leftover agent). Also a stray third-party agent (RMM, etc.) failing once at first boot can trip it.
- **Fix:** it's transient — the events age out of the window. Re-run dcdiag ~1 hour later; confirm `SystemLog` passes and DFSR reached `State=4`. Investigate only if *fresh, recurring* errors persist.

## Windows Setup can't see the virtio disk
- **Signature:** unattended install fails / no disk found; or interactive Setup shows no drives.
- **Cause:** missing virtio storage driver in WinPE.
- **Fix:** inject the right one in the `windowsPE` pass — **viostor** for a `virtio0` (virtio-blk) disk, **vioscsi** for a `scsiN` disk on a virtio-scsi controller. Inject both to be safe, plus **NetKVM** for the NIC. Match the OS folder (e.g. `2k25` for Server 2025).
