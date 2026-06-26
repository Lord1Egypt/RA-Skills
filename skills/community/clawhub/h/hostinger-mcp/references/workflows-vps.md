# Workflows — VPS (flagship playbook)

VPS operational playbook. **Always identify the account first** (each account is a separate MCP connection — IDs don't cross accounts). Every **W / W!** op uses the confirmation block from `SKILL.md` (Confirmation pattern). Read before write.

> **A VPS may host multiple workloads.** Lifecycle, recreate, and firewall ops affect *everything* on the machine. Know what runs on it before you touch it.

---

## 1. Inventory (read-only)

List what exists. No confirmation needed.

1. `VPS_getVirtualMachinesV1` — all virtual machines on the account (IDs, names, plan, state, IPs).
2. `VPS_getProjectListV1` — Docker Compose projects deployed on a VM.

Tag every result with the account name when more than one account is connected.

---

## 2. Inspect a VM (read-only)

Drill into one machine. No confirmation needed.

1. `VPS_getVirtualMachineDetailsV1` — full config for a single VM (plan, OS template, hostname, nameservers, state).
2. `VPS_getMetricsV1` — historical CPU / memory / disk usage for the VM.
3. `VPS_getScanMetricsV1` — Monarx malware-scanner metrics (if Monarx is installed).
4. `VPS_getActionsV1` / `VPS_getActionDetailsV1` — recent operations run on the VM and their detail.
5. `VPS_getAttachedPublicKeysV1` — SSH keys currently attached to the VM.

Use these to build a baseline *before* any write below.

---

## 3. Lifecycle — start / stop / restart (W)

**When:** scheduled maintenance, stuck services, applying a change that needs a reboot.

> A VPS may host several sites/services. Stop/restart takes **all of them** offline. Identify the workloads first (`VPS_getProjectListV1`, plus whatever runs outside Docker).

**Sequence:**

1. `VPS_getVirtualMachineDetailsV1` — confirm target and current state.
2. `VPS_getProjectListV1` — what's running on it.
3. **CONFIRM (W):** the chosen lifecycle tool —
   - `VPS_startVirtualMachineV1` — boot a stopped VM.
   - `VPS_stopVirtualMachineV1` — full shutdown.
   - `VPS_restartVirtualMachineV1` — full stop + start.
4. **VERIFY:** `VPS_getVirtualMachineDetailsV1` (state) and `VPS_getActionsV1` (operation completed).

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-vps)
   Tool: VPS_restartVirtualMachineV1
   Target: vps-prod-01 (ID: 123456)
   Impact: full reboot — EVERY site/service on this VM goes offline ~1-2 min
   Proceed? (yes / no)
```

> **Recovery mode** (`VPS_startRecoveryModeV1` / `VPS_stopRecoveryModeV1`, both W) is for booting into a repair environment when the VM won't boot normally — same multi-workload warning applies.

---

## 4. Provision a new VPS (W! — spends money)

**When:** standing up a new machine. Two steps: **purchase** (spends money), then **setup** (configure the purchased VM).

**Sequence:**

1. `VPS_getDataCenterListV1` — pick a location.
2. `VPS_getTemplatesV1` / `VPS_getTemplateDetailsV1` — pick an OS template.
3. **CONFIRM (W! + cost):** `VPS_purchaseNewVirtualMachineV1` — confirm plan, term, COST, and account.
4. After purchase the VM sits in `initial` state. **CONFIRM (W):** `VPS_setupPurchasedVirtualMachineV1` — apply template, hostname, password, SSH keys, optional post-install script.
5. **VERIFY:** `VPS_getVirtualMachineDetailsV1` — VM is `running` and configured.

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-vps)
   Tool: VPS_purchaseNewVirtualMachineV1
   Target: new VPS — <plan>, <datacenter>, <OS template>
   Estimated cost: <price> for <term> (charged to the account's default payment method)
   Impact: provisions and bills a new virtual machine
   Proceed? (yes / no)
```

> Optional pre-setup prep (all W): register SSH keys with `VPS_createPublicKeyV1`, and stage a `VPS_createPostInstallScriptV1` so setup runs it automatically.

---

## 5. Recreate / reinstall (W! — destructive, WIPES ALL DATA)

**When:** rebuilding a VM from scratch — fresh OS install. `VPS_recreateVirtualMachineV1` **reinstalls the OS and wipes all data on the VM.** Irreversible.

**Sequence — follow in order:**

1. **STOP.** Confirm this is really what the user wants. Recreate is not a restart.
2. `VPS_getVirtualMachineDetailsV1` + `VPS_getProjectListV1` — what's on the machine that will be destroyed.
3. **Check for a recovery point first:**
   - `VPS_getSnapshotV1` — is there a current snapshot? `VPS_getBackupsV1` — any backup points?
   - If none and the data matters: **CONFIRM (W):** `VPS_createSnapshotV1` before proceeding.
4. **DOUBLE CONFIRM (W!):** show the block, then ask the user to **type the VM name** to confirm.
5. `VPS_recreateVirtualMachineV1`.
6. **VERIFY:** `VPS_getVirtualMachineDetailsV1` — fresh OS up; `VPS_getActionsV1` — completed.

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-vps)
   Tool: VPS_recreateVirtualMachineV1
   Target: vps-prod-01 (ID: 123456)
   Impact: REINSTALLS THE OS AND WIPES ALL DATA — irreversible
   Proceed? (yes / no / create a snapshot first)
   → Then: type the VM name to confirm.
```

> Recovery, not reinstall: to roll back to a known-good state instead of wiping, use `VPS_restoreSnapshotV1` (W) or `VPS_restoreBackupV1` (W). To clear an old snapshot, `VPS_deleteSnapshotV1` (W!).

---

## 6. Firewall (W / W!)

**When:** locking down or opening ports on a VM.

> **A wrong rule can lock you out of SSH.** Before applying any rule, confirm the rule itself **and** that SSH (port 22) from your IP stays allowed. A firewall with no allow-rule for your IP = no way back in except hPanel.

**Inspect (R):** `VPS_getFirewallListV1` — all firewalls; `VPS_getFirewallDetailsV1` — one firewall and its rules.

**Build / change:**

1. `VPS_getFirewallDetailsV1` — read current rules (baseline).
2. **CONFIRM (W):** create or edit —
   - `VPS_createNewFirewallV1` — new firewall config.
   - `VPS_createFirewallRuleV1` — add a rule.
   - `VPS_updateFirewallRuleV1` — change a rule.
3. **CONFIRM (W):** `VPS_activateFirewallV1` — attach to a VM (one active firewall per VM). `VPS_deactivateFirewallV1` to detach.
4. After any rule change on an attached firewall: **CONFIRM (W):** `VPS_syncFirewallV1` — push the updated rules to the VM.
5. **VERIFY:** `VPS_getFirewallDetailsV1`, then test SSH **immediately** from the allowed IP.

**Delete (W!):** `VPS_deleteFirewallRuleV1` (one rule) / `VPS_deleteFirewallV1` (whole firewall — auto-deactivates on attached VMs).

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-vps)
   Tool: VPS_createFirewallRuleV1
   Target: firewall "prod-fw" (ID: 7788) → attached to vps-prod-01
   Impact: changes inbound access; SSH/22 from <your-IP> stays ALLOWED (confirmed)
   Proceed? (yes / no)
```

> **Lockout safety:** after any firewall change, the next confirmation is implicit — *test SSH now*. If you can't get back in, recover via hPanel. Don't end the session until SSH is verified.

---

## 7. Snapshots & backups (recovery points)

A single restore point each, plus backup history.

- **Inspect (R):** `VPS_getSnapshotV1` (current snapshot), `VPS_getBackupsV1` (backup points).
- **Create (W):** `VPS_createSnapshotV1` — capture current state/data. Take one before any risky op (recreate, major upgrade).
- **Restore (W):** `VPS_restoreSnapshotV1` (to the snapshot) or `VPS_restoreBackupV1` (to a backup point) — both overwrite current state; confirm the target point with the user first.
- **Delete (W!):** `VPS_deleteSnapshotV1`.

> One snapshot per VM — creating a new one replaces the old. For longer history, rely on backup points (`VPS_getBackupsV1`).

---

## Cleanup after a session

Before ending a conversation that included writes:

1. Summarize what was done, per account.
2. Note any snapshot/backup created (and that snapshots are single-slot, so the previous one is gone).
3. Flag anything still needing verification — SSH reachable after a firewall change, services back up after a restart/recreate.
4. If something is unfinished, document what remains open.
