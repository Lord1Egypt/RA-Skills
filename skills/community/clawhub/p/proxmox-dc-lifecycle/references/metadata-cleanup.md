# Metadata cleanup

A graceful demotion cleans its own metadata. A **forced or interrupted** removal does not — you clean it from a surviving DC. This is a *required* step after forced removal (per Microsoft), and the gate that unlocks the OS rebuild.

## First, find the residue (read-only, from a surviving DC)
```powershell
$cfg=(Get-ADRootDSE).configurationNamingContext
$dom=(Get-ADRootDSE).defaultNamingContext
$srv="CN=<DC>,CN=Servers,CN=Default-First-Site-Name,CN=Sites,$cfg"

# 1. nTDSDSA (the DC marker) — should be ABSENT
Get-ADObject -SearchBase $srv -SearchScope OneLevel -LDAPFilter "(objectClass=nTDSDSA)"
# 2. empty server object shell
Get-ADObject -Identity $srv -Properties protectedFromAccidentalDeletion
# 3. computer object (note its OU — Domain Controllers vs Computers)
Get-ADComputer -Identity <DC> -Properties protectedFromAccidentalDeletion,distinguishedName
# 4. DFSR member
Get-ADObject -SearchBase "CN=Topology,CN=Domain System Volume,CN=DFSR-GlobalSettings,CN=System,$dom" -LDAPFilter "(&(objectClass=msDFSR-Member)(name=<DC>))"
# 5. DNS records
Resolve-DnsName <DC>.<domain> -Type A -Server 127.0.0.1
Get-DnsServerResourceRecord -ZoneName "_msdcs.<domain>" | ? { "$($_.RecordData)" -like "*<DC>*" }
```

## What each leftover means
| Object | If present | If absent |
|---|---|---|
| `nTDSDSA` (NTDS Settings) | AD still sees it as a DC — **do NOT rebuild yet**; clean it | Prime-directive gate is open |
| `CN=<DC>` server object | Empty shell after nTDSDSA removed — safe to delete | n/a |
| Computer obj in `OU=Domain Controllers` | Still treated as a DC computer | If moved to `CN=Computers` → demotion-to-member completed |
| DFSR `msDFSR-Member` | SYSVOL replication still references it — remove | Already cleaned |
| `_msdcs` CNAME/SRV | DC-locator records linger — remove | DC locator already cleaned |

## Remove the residue

> **These are destructive AD writes — gate them.** Object deletion is hard to undo and easy to point at the wrong target. Before deleting anything: (1) **validate the target** — confirm each object's distinguishedName resolves to the DC you intend and to no other; (2) confirm the `nTDSDSA` for that DC is already gone (so you're deleting residue, not a live DC); (3) **get explicit operator confirmation** for the specific DNs you're about to remove. The `-Confirm:$false` below suppresses the *interactive* prompt for automation — it does NOT replace the operator sign-off, which you must obtain first. Never run these unattended or against a wildcard.

If the `nTDSDSA` object still exists, the cleanest supported route is `ntdsutil metadata cleanup` (`connect to server <healthyDC>` → `remove selected server <DC>`), which removes the nTDSDSA and connection objects but **not** the parent server object. If `nTDSDSA` is already gone (typical after a forced attempt that got far enough), `ntdsutil` will report "not found" — then, after the validation + confirmation above, delete the leftovers:
```powershell
# 1. VALIDATE: resolve and show exactly what will be deleted; abort if it doesn't match the intended DC
$srvObj = Get-ADObject -Identity $srv -ErrorAction Stop      # empty server shell
$kids   = Get-ADObject -SearchBase $srv -SearchScope OneLevel -LDAPFilter '(objectClass=*)'
if ($kids) { throw "ABORT: server object still has children: $($kids.Name -join ',')" }  # not an empty shell — stop
$comp   = Get-ADComputer <DC> -ErrorAction Stop
Write-Output "WILL DELETE:`n  $($srvObj.DistinguishedName)`n  $($comp.DistinguishedName)"
# 2. OPERATOR CONFIRMS the two DNs above are correct, THEN:
Remove-ADObject -Identity $srvObj.DistinguishedName -Confirm:$false   # interactive prompt suppressed; operator already approved
Remove-ADObject -Identity $comp.DistinguishedName  -Confirm:$false
```
Keep the **DNS A record** if the rebuild reuses the same IP — the new DC re-registers it on join. Remove stale `_msdcs` records only if they actually exist.

If you hit "Access is denied", the object is likely protected from accidental deletion — clear `protectedFromAccidentalDeletion` first.

## Verify (gate)
- No `nTDSDSA`, no server object, no computer object for the target.
- `Get-ADDomainController` lists only the surviving DCs (target absent).
- `repadmin /replsummary` = 0 fails; `dcdiag` clean on survivors except the benign DFSREvent referencing the removed DC.
- **Only now is the VM disk safe to wipe.**
