# QGA Execution — how this skill runs commands in Windows guests

Every Windows-side action in this skill runs through the QEMU guest agent (QGA) from the Proxmox host. There is no WinRM, no PowerShell Remoting, no SSH into the guests. This is deliberate: remoting between DCs failed repeatedly in the field (see `gotchas.md`, error `0x8009030e`), and QGA runs reliably as `NT AUTHORITY\SYSTEM` inside the guest with no auth handshake to break.

## The core pattern

Encode the PowerShell as base64 (avoids quoting hell and keeps it off the visible command line), decode and `Invoke-Expression` it inside the guest:

```bash
run_guest() {
  local vmid="$1" ps="$2" b64
  b64=$(printf '%s' "$ps" | base64 -w0)
  sudo qm guest exec "$vmid" --timeout 120 -- \
    powershell.exe -NoProfile -NonInteractive -Command \
    "\$d=[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$b64')); Invoke-Expression \$d" 2>&1
}
run_guest <dc-vmid> 'hostname; netdom query fsmo'
```

`scripts/run-guest-ps.sh` is this wrapper as a standalone script.

## Passing secrets — over stdin, never on the command line

`qm guest exec` supports `--pass-stdin 1`. Feed credentials as the first lines of stdin; the guest script reads them with `[Console]::In.ReadLine()`. The password never appears in the process table, in `-EncodedCommand`, or in the base64 blob.

```bash
read -r -d '' GUEST <<'PS'
$u = [Console]::In.ReadLine()   # domain user
$p = [Console]::In.ReadLine()   # domain password
$sec  = ConvertTo-SecureString $p -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($u,$sec)
# ... use $cred ...
PS
B64=$(printf '%s' "$GUEST" | base64 -w0)
printf '%s\n%s\n' '<DOMAIN>\Administrator' "$PW" | \
  sudo qm guest exec <dc-vmid> --timeout 150 --pass-stdin 1 -- \
  powershell.exe -NoProfile -NonInteractive -Command \
  "\$d=[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('$B64')); Invoke-Expression \$d" 2>&1
```

If you must drop a cred file inside the guest (e.g. for a scheduled task), make the consuming script **delete it as its very first action**, lock the directory ACL to SYSTEM+Administrators, and overwrite-then-delete on cleanup. Never leave plaintext creds on a guest disk.

## Two behaviors that will surprise you

1. **NonInteractive blocks prompts as errors, not hangs.** With `-NonInteractive`, any cmdlet that tries to prompt (for a password, a confirmation) throws `Windows PowerShell is in NonInteractive mode` instead of hanging. That's actually a *useful* signal — it tells you a required parameter is missing. Supply the parameter rather than dropping `-NonInteractive`.

2. **`qm guest exec` can return a `{"pid": N}` instead of output.** If the guest command runs longer than `--timeout`, QGA detaches it and returns the pid; the process keeps running *inside the guest*. Your call "returns" but the work is still going. Two consequences:
   - Don't assume completion from a returned pid. Re-query the guest (`Get-Process -Id N`) to see if it's still alive.
   - **Don't fire a second attempt on top of a detached first one** — especially for AD operations. Check for and kill orphaned `powershell` processes before retrying (`Get-Process powershell | Where Id -ne $PID`).

## Running as SYSTEM — the credential-context trap

QGA runs your PowerShell as `NT AUTHORITY\SYSTEM`. SYSTEM is a local identity with no outbound domain credentials. For LDAP reads against the local DC this is fine. The catch is **DEMOTE vs PROMOTE behave differently**, and the right pattern is the opposite for each:

- **Demotion (`Uninstall-ADDSDomainController`) on an existing domain member:** fails as SYSTEM with **LDAP error 58** ("server cannot perform the requested operation"), because SYSTEM never establishes a real logon session for the passed `-Credential`. **Fix:** run it inside a **scheduled task whose principal IS the domain admin** (`schtasks /create /ru <DOMAIN>\Administrator /rp <pw> ...`) — the box is already a domain member so the task's domain principal is valid, and it gets a genuine logon session. Use classic `schtasks.exe`, not the CIM `*-ScheduledTask` cmdlets (those fail with `0x80070008` under memory/heap pressure — see gotchas).

- **Promotion (`Install-ADDSDomainController`) on a fresh/just-installed box:** run it **DIRECTLY via QGA as SYSTEM, passing `-Credential`** — do NOT use the scheduled-task pattern. The promotion cmdlet authenticates to the domain itself with the supplied credential as part of joining, so it does NOT hit error 58. The scheduled-task pattern actively *breaks* here: a fresh box isn't a domain member, so `schtasks /ru DOMAIN\user` fails with "The trust relationship between this workstation and the primary domain failed." (And note: promotion needs the box to be a properly-trusted member first — see `promotion.md` §0 if its old computer object was deleted.)

Either way, validate the credential first with an explicit bind (`New-Object System.DirectoryServices.DirectoryEntry("LDAP://<dc>",$u,$p)`) so you know the password/account is good before blaming context.

## Timeouts & backgrounding

Long operations (dcdiag, promotion) can exceed a couple of minutes. Options, in order of reliability:
- **Long synchronous call:** raise `--timeout` (up to ~280s is comfortable) on a single `qm guest exec`. Simplest when the op fits.
- **Scheduled task** (`schtasks /create /sc ONCE /st <future-time> ; schtasks /run`): properly detached — survives the QGA call returning. Use for ops that exceed the timeout. Needs a valid task principal — a `/ru` with a directory account requires the box to already be a trusted member.
- **Do NOT use `Start-Job` to detach across a QGA call** — the job is a child of the `qm guest exec` powershell process and is killed when that call returns (seen on the DC2 promotion: it logged "LAUNCHER start" then nothing). It only works if the parent call stays alive, which defeats the purpose.

Always write progress to a marker file the launched script appends to, and poll it from the host. For reboots, poll the guest agent: wait for it to go *unresponsive* (going down), then wait for it to respond again (back up). Note the agent may answer mid-OOBE/mid-boot — confirm the real signal (a marker, `ImageState`, a service state), not just agent reachability.
