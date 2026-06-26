---
name: hostinger-mcp
version: 1.0.0
license: MIT
description: |
  Operational guide for managing Hostinger infrastructure — VPS, websites/hosting, domains, DNS, email marketing (Reach), and billing — via the official Hostinger MCP server (npm hostinger-api-mcp), across one or several Hostinger accounts.
  Use whenever the user mentions Hostinger, hPanel, a Hostinger VPS, a Hostinger-hosted site, Hostinger domains/DNS, domain purchase/transfer/lock, Hostinger email/Reach contacts, or Hostinger billing/subscriptions.
  Any write operation (create/update/delete/recreate a VPS, change firewall/DNS, purchase a domain or VPS, change a subscription or payment method, deploy/import a site) requires explicit confirmation of the target resource and intended action — and the cost, for money-spending operations — before execution.
---

# Hostinger MCP — Operational Skill

Managing Hostinger infrastructure — VPS, hosting, domains, DNS, Reach, billing — through the official Hostinger MCP server.

> **Connection / tool loading:** This skill targets the **official Hostinger MCP server**, which runs as a **LOCAL npm process** (`hostinger-api-mcp`, Node.js **v24+**) — not a hosted URL. The server exposes **127 tools** split across category binaries. **Load only the category binaries you need for the task — do not load all 127 tools at once.** The binaries:
>
> - `hostinger-vps-mcp` — **62** (VPS)
> - `hostinger-hosting-mcp` — **22** (websites/hosting)
> - `hostinger-domains-mcp` — **18** (domains)
> - `hostinger-reach-mcp` — **10** (email marketing)
> - `hostinger-dns-mcp` — **8** (DNS)
> - `hostinger-billing-mcp` — **7** (billing)
> - `hostinger-api-mcp` — **all 127** (everything; use only when a task genuinely spans categories)
>
> **Default to the smallest set covering the task.** A pure DNS edit needs only `hostinger-dns-mcp` (8 tools), not the full 127. See `references/installation.md`.
>
> **Tool names match the upstream package.** The catalog and workflows use the official `hostinger-api-mcp` tool names. Always treat the live `mcp__hostinger*__*` tools as the source of truth if Hostinger changes them (see "Versioning and source of truth" below).

---

## Quick Route

| Intent | Load |
|--------|------|
| Initial installation/configuration of the MCP server | `references/installation.md` |
| Don't know which tool exists / searching for a tool by name | `references/tools-catalog.md` |
| VPS operations (create, firewall, snapshot, recreate, etc.) | `references/workflows-vps.md` |
| Multiple Hostinger accounts / multi-account configuration | `references/installation.md` (Multi-account section) |

**Load only what's needed.** Match the binary to the task (see Connection above), and don't load the full catalog just to "list my VPSes" — call `VPS_getVirtualMachinesV1` directly.

---

## Safety rules (read before every operation)

1. **Identify the account first (multi-account).** Each Hostinger account is a **separate MCP connection** with its own prefix (`mcp__hostinger-<account>__*`). Resource IDs are **NOT interchangeable between accounts** — VM ID 123456 in account A is a different resource (or nonexistent) in account B. Before every call, verify which account it belongs to. If it's unclear which account is meant, **stop and ask** — don't guess, and don't run across all of them "to be safe".

2. **Write operations require explicit confirmation.** Before any write tool, present: the **account**, the tool name, the **target resource (ID + name)**, the parameters, and the expected impact. Wait for an explicit "yes". One confirmation ≠ blanket consent for further operations, and a confirmation on one account never carries to another.

3. **Money-spending operations require cost-confirmation.** `domains_purchaseNewDomainV1`, `VPS_purchaseNewVirtualMachineV1`, subscription create/cancel, and `billing_setDefaultPaymentMethodV1` spend **real money**. Confirm the **cost AND the account** before executing.

4. **Destructive operations double-confirm (W!).** Any `*delete*` tool, `VPS_recreateVirtualMachineV1` (reinstalls the OS, **wipes all data**), and `DNS_resetDNSRecordsV1` on production require confirmation of **both** the operation and the **specific target**.

5. **Multiple workloads per VPS.** A single VPS may host several sites/services. `VPS_stopVirtualMachineV1`, `VPS_restartVirtualMachineV1`, and `VPS_recreateVirtualMachineV1` affect **everything** on it. Make the user aware of what runs on the VM before any VPS-level operation.

6. **Credentials.** Each account uses its own `HOSTINGER_API_TOKEN` — **full account access**, with no per-tool permission at the MCP layer. Never print the token in responses. If the user asks to see it, refer them to hPanel.

7. **Read-only by default.** For "show / check / list", pick the read-only tool (e.g. `VPS_getVirtualMachinesV1`, `domains_getDomainListV1`, `DNS_getDNSRecordsV1`). Never suggest a destructive operation unless explicitly asked.

---

## Confirmation pattern

Before executing a write, present a block like this:

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-vps)
   Tool: VPS_recreateVirtualMachineV1
   Target: vps-prod-01 (ID: 123456)
   Impact: reinstalls the OS and WIPES ALL DATA on the VM
   Proceed? (yes / no / check for a snapshot first)
```

For money-spending operations, add an `Estimated cost:` line:

```
🔒 Confirm operation?
   Account: clientA (mcp__hostinger-clientA-domains)
   Tool: domains_purchaseNewDomainV1
   Target: example.co.il (new registration)
   Estimated cost: <price> for <term>
   Impact: charges the account's default payment method
   Proceed? (yes / no)
```

Wait for an explicit "yes" — implied consent is not enough. The **account line is mandatory** when more than one account is connected; it prevents executing on the wrong account.

---

## Multi-account — working with multiple Hostinger accounts

Token-per-connection. Each account connects as a **separate** MCP connection with its own `HOSTINGER_API_TOKEN`, and appears in Claude with its own prefix:

```
mcp__hostinger-clientA__VPS_getVirtualMachinesV1
mcp__hostinger-clientB__domains_getDomainListV1
mcp__hostinger-clientA-dns__DNS_getDNSRecordsV1
```

Name each connection `hostinger-<account>` — or, when loading per-category binaries, `hostinger-<account>-<category>` (e.g. `hostinger-clientA-vps`, `hostinger-clientA-dns`).

### Rules
- **Identify the account before every operation.** Single account connected → use it. Multiple → determine which from the request; if unclear, stop and ask. If a resource name unambiguously identifies one account you may infer, but state which account you're operating on.
- **IDs don't cross accounts.** A VM/domain/subscription ID from one connection is valid only against that connection. Never pass it to another.
- **Never reuse a token across accounts.** Each connection has its own `HOSTINGER_API_TOKEN`; don't assume the same token works elsewhere.
- **Per-account confirmation.** A write confirmation on one account never applies to another — each write on a new account gets a fresh confirmation block (including the account line).
- **Cross-account reads are fine.** For broad "which account owns example.com?" questions, run the same read on each connection separately and tag each result with the account name. Never run a broad write across accounts without individual confirmation for each.

---

## Authentication — quick overview

- **`HOSTINGER_API_TOKEN` (default).** A Bearer token generated in **hPanel**, passed to the MCP server via env. This is the standard path.
- **OAuth 2.0 PKCE (interactive alternative).** Available on **stdio transport only**, via `hostinger-api-mcp --login`.

The token has **full account access** — every action the account can perform in hPanel. There is **no granular / per-tool permission at the MCP layer**: any connected client can call any tool. Treat it like a password and **never print it** in responses. If the user asks to see it, refer them to hPanel.

For the full connection and multi-account setup, see `references/installation.md`.

---

## Versioning and source of truth

- **Tool names match the upstream package.** The tool names and categories here are taken from the official `hostinger-api-mcp` package.
- **The live MCP wins if Hostinger changes them.** If a tool name or capability differs from what's documented, the live `mcp__hostinger*__*` tools connected in Claude are the source of truth — check them and update the catalog accordingly.
- **Every write tool goes through the confirmation pattern.** W = single confirmation; W! = double-confirmation for destructive ops (any `*delete*`, `VPS_recreateVirtualMachineV1`, `DNS_resetDNSRecordsV1` on production), per `references/tools-catalog.md`. Money-spending ops additionally require cost-confirmation.
