# 🔧 OpenClaw Intune Skill – Complete Microsoft Intune Management

> **Author:** Mattia Cirillo
> **Website:** [kaffeeundcode.com](https://kaffeeundcode.com)
> **License:** MIT
> **Platform:** [OpenClaw](https://github.com/openclaw/openclaw)

---

## 🌐 About This Project

This skill was built by **Mattia Cirillo**, an IT administrator and automation enthusiast from Germany. It is part of the **[Kaffee & Code](https://kaffeeundcode.com)** project – a platform dedicated to sharing real-world PowerShell scripts, n8n automation workflows, and Microsoft Intune knowledge with the IT community.

### What is this Skill?

The **OpenClaw Intune Skill** teaches any [OpenClaw](https://github.com/openclaw/openclaw)-compatible AI agent how to **fully manage Microsoft Intune** through the Microsoft Graph API. Instead of manually navigating the Intune admin portal or writing custom scripts for every task, you talk to your agent in natural language – it handles the rest.

### What does it actually do?

- **Query your device fleet** – list, search, compliance status, reports
- **Execute remote actions** – sync, reboot, lock, wipe, retire, rename, locate – with tiered safety confirmations
- **Manage compliance & configuration policies** – incl. the modern Settings Catalog
- **Handle app deployment** – apps, assignments, detected apps, App Protection (MAM)
- **Control Endpoint Security** – baselines, BitLocker/FileVault, Firewall, Defender, ASR
- **Automate Windows Autopilot** – devices, profiles, user assignment, cleanup
- **Deploy PowerShell scripts & remediations** – upload, monitor execution
- **Manage users & groups** – search, memberships, devices per user
- **Generate reports** – compliance summary, OS distribution, stale devices, export jobs
- **Configure Conditional Access** – policies, named locations, auth strengths
- **Manage network profiles** – Wi-Fi, VPN, SCEP/PKCS/root certificates
- **Control Windows Updates** – rings, feature/quality/driver updates, pause/resume
- **Administer Apple devices** – DEP/ADE, APNS monitoring, VPP, Activation Lock bypass
- **Manage Android Enterprise** – Managed Google Play, enrollment profiles
- **Audit everything** – Intune audit logs, directory audits, sign-in logs
- **Search the Settings Catalog** – "Can Intune configure setting X?" + GPO migration reports

## 📂 Structure

```
intune-graph/
├── SKILL.md                     # Core: auth, safety tiers, Graph mechanics, routing
├── scripts/
│   ├── get_token.sh             # OAuth2 token with caching & multi-tenant profiles
│   └── graph.sh                 # API wrapper: pagination, 429 retry, read-only guard
├── references/
│   ├── devices.md               # Devices, remote actions, categories, scripts
│   ├── policies.md              # Compliance, config, Endpoint Security, CA, filters
│   ├── apps.md                  # Apps & App Protection (MAM)
│   ├── platform.md              # Autopilot, enrollment, Apple, Android
│   ├── network-updates.md       # Wi-Fi/VPN/certs, Windows Update
│   ├── reporting.md             # Reports, audit logs, Settings Catalog search
│   ├── admin.md                 # Users, groups, RBAC, terms, notifications
│   ├── workflows.md             # Multi-step MSP recipes (on/offboarding, reports)
│   └── troubleshooting.md       # Common Graph errors and fixes
└── examples/
    └── conversations.md         # Example dialogues
```

The agent loads only the reference file it needs – keeping context small and safety rules front and center.

## 🔑 Required Graph API Permissions

Create an **App Registration** in Microsoft Entra ID and grant these Microsoft Graph **Application** permissions (admin consent required). Grant only what you need:

| Permission | Needed for | Read-only alternative |
|---|---|---|
| `DeviceManagementManagedDevices.ReadWrite.All` | Devices & remote actions | `…ManagedDevices.Read.All` |
| `DeviceManagementConfiguration.ReadWrite.All` | Compliance/config policies, updates, network profiles | `…Configuration.Read.All` |
| `DeviceManagementApps.ReadWrite.All` | Apps & App Protection | `…Apps.Read.All` |
| `DeviceManagementServiceConfig.ReadWrite.All` | Autopilot, enrollment, Apple/Android setup, T&C | `…ServiceConfig.Read.All` |
| `DeviceManagementRBAC.Read.All` | RBAC roles (skill only reads) | – |
| `Policy.ReadWrite.ConditionalAccess` | Conditional Access (category was broken in v1.x – permission was missing!) | `Policy.Read.All` |
| `AuditLog.Read.All` | Sign-in logs & directory audits | – |
| `Directory.Read.All` | User/group/device directory reads | – |
| `User.Read.All` | User lookups | – |
| `Group.ReadWrite.All` | Group membership changes | `Group.Read.All` |
| `GroupMember.ReadWrite.All` | Add/remove members | `GroupMember.Read.All` |

💡 **Read-only deployment:** grant only the `Read.All` variants **and** set `INTUNE_READ_ONLY=true` – the wrapper then refuses every write. Ideal for reporting-only access to customer tenants.

## 📦 Installation

```bash
mkdir -p ~/.openclaw/workspace/skills/intune-graph
cp -r SKILL.md scripts references examples ~/.openclaw/workspace/skills/intune-graph/
chmod +x ~/.openclaw/workspace/skills/intune-graph/scripts/*.sh
```

Dependencies: `bash`, `curl`, `jq`.

## ⚙️ Setup

Single tenant:

```bash
export INTUNE_TENANT_ID="your-tenant-id"
export INTUNE_CLIENT_ID="your-client-id"
export INTUNE_CLIENT_SECRET="your-client-secret"
```

Multiple tenants (MSP):

```bash
export INTUNE_CONTOSO_TENANT_ID="…"
export INTUNE_CONTOSO_CLIENT_ID="…"
export INTUNE_CONTOSO_CLIENT_SECRET="…"
export INTUNE_FABRIKAM_TENANT_ID="…"
# …
export INTUNE_PROFILE="contoso"   # active tenant; the agent asks if unset and several exist
```

Optional:

```bash
export INTUNE_READ_ONLY="true"    # block all write operations
```

## 🛡️ Safety

Every operation is classified into a tier – and **anything that isn't a GET is at least Tier 2 by default**:

| Tier | Examples | Behaviour |
|---|---|---|
| 0 | All reads | Instant, no prompt |
| 1 | Sync, reboot, lock, locate | One short confirmation |
| 2 | Create/change/delete policies, apps, groups, reset passcode | Change summary + explicit confirmation |
| 3 | Wipe, retire, delete device/Autopilot identity, Activation Lock bypass, delete CA policy | User must **type back the exact device/policy name** |

Plus: read-only mode via env var, client secret is never printed or logged, batch actions list all affected objects first, output is always formatted Markdown – never raw JSON.

The wrapper also enforces these boundaries: it only accepts documented
Intune/Entra Graph endpoint families, requires `--confirm` for Tier 1/2
writes, requires `--confirm-name "EXACT NAME"` for Tier 3, and never emits a
raw bearer token.

## 💬 Example Usage

> **You:** "Zeig mir alle Geräte die nicht compliant sind"
> **Agent:** "5 Geräte nicht compliant. 3 Windows (fehlende Updates), 2 iOS (kein Passcode). Soll ich die syncen?"

> **You:** "Wipe MAX-LAPTOP"
> **Agent:** "⚠️ Das setzt MAX-LAPTOP komplett auf Werkseinstellungen zurück – alle Daten gehen verloren. Tippe zur Bestätigung den Gerätenamen exakt ein."

More in [`examples/conversations.md`](examples/conversations.md).

## 🔗 Links

- 🌐 [Kaffee & Code](https://kaffeeundcode.com) – Blog, Skripte & Automatisierung
- 🦞 [OpenClaw](https://github.com/openclaw/openclaw)
- 📖 [Microsoft Graph API Docs](https://learn.microsoft.com/en-us/graph/api/resources/intune-graph-overview)

---
Made with ☕ by [Mattia Cirillo](https://kaffeeundcode.com)
