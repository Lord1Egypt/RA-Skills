# Credential handling — what this skill owns, and where it hands off

**Scope reality:** this skill runs *on the Proxmox host*. The host has no password manager.
So the skill can generate and apply secrets, but it **cannot store, retrieve, or vault them**.
Be honest about that boundary — don't emit instructions the host can't execute.

## What the skill does with secrets
- **Pass existing creds to a guest over QGA stdin** (`--pass-stdin`), never on a command
  line — see `qga-execution.md`.
- **Generate throwaway randoms** for the new local Administrator (in the unattend) and the
  DSRM password (at promotion), so install/promotion run non-interactively. Generate them
  on the host, use them once, and **show only a sha256 fingerprint — never the value**.
- **Delete the carrier immediately:** the unattend ISO (which holds the local-admin value)
  is deleted right after install; any in-guest cred file is deleted as the script's first
  action.

## What the skill must NOT pretend to do
- It cannot put a password into a vault — there is no secret manager on the host. Do not
  write vault-CLI commands (1Password/Vault/Bitwarden/etc.) as skill steps; the assistant
  running this skill on the host can't execute them.
- It cannot "remember" or later reveal a value it generated. Once shown as a fingerprint
  and the carrier is deleted, the value exists only as a hash inside the guest.

## The hand-off (do this every rebuild)
Treat every skill-generated local-admin / DSRM password as **throwaway**. Immediately after
the rebuild, tell the operator — plainly and in one place — that:
1. these values are random and unrecorded (give the sha256 fingerprints for their records);
2. they are NOT needed for normal (domain) logon, only for break-glass (DC off-domain, DSRM
   recovery);
3. the operator should set **known** values from a machine that HAS their secret manager.
   The pattern: generate/store the value in the vault on that machine, then apply it by
   piping it into the guest's stdin over SSH — e.g.
   `<vault-read-cmd> | ssh root@<pvehost> 'qm guest exec <vmid> --pass-stdin 1 -- powershell ...'`
   — so the value is born in the vault and never touches the Proxmox host, its shell history,
   or any assistant transcript. Online resets used: `Set-LocalUser` for the local
   Administrator; `ntdsutil "set dsrm password"` → `reset password on server null` (prompts
   twice) for DSRM; `Set-ADAccountPassword -Reset` (against a DC) for a domain account.

The division of labor: **skill = generate-throwaway + apply + hand off; operator (off-host,
with a vault) = own the secrets.** Keep the vault mechanics OUT of this skill — they belong
on the machine where they can actually run.

## If a password is ever exposed
If a credential leaks in clear text anywhere it does not belong (pasted into a transcript, a log, a
task's XML), treat it as compromised and **rotate it** — file-scrubbing is secondary and
never sufficient alone. Rotate via the same vault → SSH → guest-stdin pattern above.
