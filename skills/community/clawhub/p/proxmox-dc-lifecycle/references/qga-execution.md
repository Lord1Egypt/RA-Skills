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

- **Demotion (`Uninstall-ADDSDomainController`) on an existing domain member:** fails as SYSTEM with **LDAP error 58** ("server cannot perform the requested operation"), because SYSTEM never establishes a real logon session for the passed `-Credential`. **Fix:** run it inside a **scheduled task whose principal IS the domain admin** (`schtasks /create /ru <DOMAIN>\Administrator /rp * ...` — pass `/rp *` so the password is read from stdin, never an argument) — the box is already a domain member so the task's domain principal is valid, and it gets a genuine logon session. Use classic `schtasks.exe`, not the CIM `*-ScheduledTask` cmdlets (those fail with `0x80070008` under memory/heap pressure — see gotchas).

- **Promotion (`Install-ADDSDomainController`) on a fresh/just-installed box:** run it **DIRECTLY via QGA as SYSTEM, passing `-Credential`** — do NOT use the scheduled-task pattern. The promotion cmdlet authenticates to the domain itself with the supplied credential as part of joining, so it does NOT hit error 58. The scheduled-task pattern actively *breaks* here: a fresh box isn't a domain member, so `schtasks /ru DOMAIN\user` fails with "The trust relationship between this workstation and the primary domain failed." (And note: promotion needs the box to be a properly-trusted member first — see `promotion.md` §0 if its old computer object was deleted.)

Either way, validate the credential first with an explicit bind (`New-Object System.DirectoryServices.DirectoryEntry("LDAP://<dc>",$u,$p)`) so you know the password/account is good before blaming context.

## Timeouts & backgrounding

Long operations (dcdiag, promotion) can exceed a couple of minutes. Options, in order of reliability:
- **Long synchronous call:** raise `--timeout` (up to ~280s is comfortable) on a single `qm guest exec`. Simplest when the op fits.
- **Scheduled task** (`schtasks /create /sc ONCE /st <future-time> ; schtasks /run`): properly detached — survives the QGA call returning. Use for ops that exceed the timeout. Needs a valid task principal — a `/ru` with a directory account requires the box to already be a trusted member.
- **Do NOT use `Start-Job` to detach across a QGA call** — the job is a child of the `qm guest exec` powershell process and is killed when that call returns (seen on a promotion: it logged "LAUNCHER start" then nothing). It only works if the parent call stays alive, which defeats the purpose.

Always write progress to a marker file the launched script appends to, and poll it from the host. For reboots, poll the guest agent: wait for it to go *unresponsive* (going down), then wait for it to respond again (back up). Note the agent may answer mid-OOBE/mid-boot — confirm the real signal (a marker, `ImageState`, a service state), not just agent reachability.

## Driving QGA from off-host (REST API variant)

The lifecycle runs ON the Proxmox host, where `qm guest exec` is the right tool — it blocks and returns the guest's stdout/stderr directly. But when you're NOT on the host (e.g. driving from a workstation with a Proxmox API token and no `qm`), use the REST API instead. It's two calls: start the command, then poll for its result.

```bash
# 1) Start — returns {"data":{"pid":N}}
PID=$(curl -sk -H "Authorization: PVEAPIToken=$TOKENID=$SECRET" \
  -X POST "https://$PVE:8006/api2/json/nodes/$NODE/qemu/$VMID/agent/exec" \
  --data-urlencode 'command=cmd' --data-urlencode 'command=/c' --data-urlencode 'command=hostname' \
  | sed -E 's/.*"pid":([0-9]+).*/\1/')

# 2) Poll until "exited":1, then read out-data / exitcode
curl -sk -H "Authorization: PVEAPIToken=$TOKENID=$SECRET" \
  "https://$PVE:8006/api2/json/nodes/$NODE/qemu/$VMID/agent/exec-status?pid=$PID"
```

Each token of the command is its own repeated `command=` arg (no shell splitting on the wire); to run base64'd PowerShell as in "The core pattern," pass `command=powershell.exe`, `-NoProfile`, `-NonInteractive`, `-Command`, then the decoder string. Pass secrets with `input-data=` (stdin to the guest), not on the command line.

⚠️ **Proxmox returns unescaped control characters in `out-data`**, so `jq` chokes on multiline guest output (`Invalid string: control characters...`). Either keep guest output to a single clean line, or parse leniently (prints `__RUNNING__` until the command exits, then `__EXITED__` + decoded output):

```python
import sys,re
raw=sys.stdin.buffer.read().decode('utf-8','replace')
ex=re.search(r'"exited"\s*:\s*(\d+)',raw)
if not(ex and ex.group(1)=='1'): print("__RUNNING__"); sys.exit(0)
m=re.search(r'"out-data"\s*:\s*"(.*?)"\s*,\s*"exited"',raw,re.S)
out=m.group(1) if m else ""
try: out=out.encode('utf-8','replace').decode('unicode_escape','replace')
except: pass
print("__EXITED__"); sys.stdout.write(out)
```

The on-host `qm guest exec` path sidesteps all of this — which is why it's preferred whenever you're on the host.

## `cmd` vs PowerShell, and verifying installers by exit code

- **PowerShell startup is slow on Defender-heavy / freshly-installed VMs** — seconds per invocation while AMSI and the module cache warm up. Simple `cmd /c` operations are effectively instant. Base64 (the core pattern) is what lets you prefer PowerShell anyway: it removes the quoting hell that would otherwise push you to `cmd`. So encode PS when you need cmdlets/objects, use `cmd` when it's simpler.
- **8.3 short paths dodge `Program Files (x86)` paren-parsing in `cmd`.** Unquoted `C:\Program Files (x86)\...` breaks `cmd` on the parentheses; use the short form (`C:\PROGRA~2\...`, and `C:\PROGRA~1\...` for 64-bit Program Files). PowerShell is fine if the path is quoted.
- **Verify silent installers by exit code, not output.** A role/feature or MSI install run with `/qn` is silent — don't infer success from empty stdout. `msiexec /i ... /qn` returns **0** = success or **3010** = success-but-reboot-required; treat *both* as success. Read it from `.data.exitcode` (REST `exec-status`) or `$LASTEXITCODE` (PowerShell).
