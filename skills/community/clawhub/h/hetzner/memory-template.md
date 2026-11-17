# Working File Templates — Hetzner

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/hetzner/config.yaml` | Key by key, read-modify-write |
| Account context, infrastructure, pain points, how they work, spend, due dates, box index | `~/Clawic/data/hetzner/memory.md` | Rewritten in place; stays small |
| Cloud servers and Robot dedicated servers | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| Domains, zones, renewal dates | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| A client who owns a server or a domain | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, identified by email or handle; referenced here by name only |
| Cloud projects, their purpose and their token pointer | `## Cloud Projects` in `memory.md` while there is one; `~/Clawic/data/hetzner/cloud-projects.md` from the second | One row per project |
| Things you produced that get re-read — runbooks, a cloud-init that finally booted clean, a firewall ruleset, an installimage config, an architecture decision and its diagram, a migration plan, a post-mortem, a price comparison | `~/Clawic/data/hetzner/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Deploys, restores, and timed recovery drills | `~/Clawic/data/hetzner/deploys/<year>.md` | Append-only, cut by year |
| Abuse notices, null-routes, hardware failures, provider maintenance | `~/Clawic/data/hetzner/incidents/<year>.md` | Append-only, cut by year |
| An architecture decision for work the user tracks as a project | Summary in `## Infrastructure (hetzner)` inside `~/Clawic/data/projects/<project>.md` (**shared**), diagram stays in `artifacts/` | One file per project, from the first |
| **Anything durable this table does not name** | `~/Clawic/data/hetzner/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A server was created, resized, rebuilt, discovered, or deleted | Its row in `servers.md`; delete the row on deletion and note the date |
| An inventory or exposure sweep ran (Rule 1) | `## Current Infrastructure` |
| The invoice was read, or a saving landed | `## Spend` |
| A budget figure or a cost alert was agreed | `### Alerts Configured` |
| A cloud project was created, renamed, or its token rotated | The Cloud Projects table (token as a pointer, never a value) |
| A domain was registered, transferred, or a zone moved | Its row in `domains.md`, and the renewal date in `## Due` |
| A server, domain or project turned out to belong to a client | That person's row in `contacts.md` (email or handle is the identity); only their name here |
| The user tracks this infrastructure work as a project | `## Infrastructure (hetzner)` in `~/Clawic/data/projects/<project>.md` |
| A deploy shipped, a snapshot was restored, or a recovery drill was timed | `deploys/<year>.md` |
| An abuse notice, null-route, hardware failure, or maintenance window arrived | `incidents/<year>.md` |
| A dedicated server was ordered | Its row in `servers.md` **and** its cancellation deadline in `## Due` |
| A runbook, a working cloud-init, a firewall ruleset, an installimage config, or an architecture decision came out of the session | `artifacts/` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, deploy records, incident records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/hetzner/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook, a cloud-init template or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:HCLOUD_TOKEN` · `keychain:hetzner-prod` · `1password:Infra/Hetzner/prod` · `bitwarden:Hetzner/robot` · `vault:kv/hetzner/prod` · `file:~/.ssh/id_ed25519` · `profile:prod`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `password: <keychain:hetzner-storagebox>`. Say in one line that you did it. Two file types in this domain are dense in secrets and are exactly the ones people ask to keep: **cloud-init / `user_data`** (database passwords, join tokens, WireGuard private keys) and a **runbook** (the rescue password, the Storage Box credentials, the token used in the recovery command).

In this domain — **not secrets, keep them**: server names and ids, project names, public IPv4 and IPv6 addresses, private network CIDRs, location ids (`fsn1`, `hel1`, `ash`), server types (`cax31`), volume, network, firewall and load-balancer names, image names, label keys and values, SSH key *fingerprints* and their names in the project, Robot server numbers, invoice numbers, the customer number, domain names, public DNS records, monthly figures. **Secrets, strip them**: Cloud API tokens, Robot web-service passwords, account and console passwords, rescue-mode passwords, the root password mailed on server creation, Storage Box and sub-account passwords, Object Storage access keys and secrets, DNS API tokens, SSH private keys and passphrases, WireGuard and VPN private keys, DKIM private keys, Borg repository passphrases, database passwords and connection strings that carry one, `.env` contents.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared domains inventory](#shared-domains-inventory) · [shared contacts inventory](#shared-contacts-inventory) · [shared projects box](#shared-projects-box) · [cloud-projects.md](#cloud-projectsmd) · [artifacts/](#artifacts) · [deploys/](#deploys) · [incidents/](#incidents) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/hetzner/` if it does not exist.

```yaml
default_location: fsn1
cpu_arch: arm64
os_image: debian-13
iac_tool: terraform
monthly_budget_eur: 80
price_mode: net
backup_target: storage-box
dns_provider: hetzner
data_residency: eu

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  server_naming: "<role>-<env>-<n>"
  network_cidr: "10.10.0.0/16, /24 per role"
  labels: [env, role, owner]
safety_posture:
  protection_flags: on-stateful
  destructive_commands: confirm-each
operations_model: k3s
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Hetzner Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Cloud projects (3) → `cloud-projects.md`; read before any command that needs a token or a project scope
- Spend history (14 months) → `spend-log.md`; read before any cost comparison or budget question
- Checkout outage runbook → `artifacts/runbook-checkout.md`; read the moment checkout is the symptom
- k3s node cloud-init → `artifacts/cloud-init-k3s-node.md`; read before adding a node
- 2026 incidents (4) → `incidents/2026.md`; read when an abuse notice, null-route or hardware fault appears

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Invoice vs resource reconciliation | month | 2026-06-30 | 2026-07-31 |
| Snapshot and orphan sweep | month | 2026-07-02 | 2026-08-02 |
| Restore drill (Borg → scratch server) | quarter | 2026-05-14 | 2026-08-14 |
| API token rotation | 6 months | 2026-03-01 | 2026-09-01 |
| AX41 cancellation deadline | one-off | — | 2026-09-20 |
| domain example.com renewal | year | 2025-11-04 | 2026-11-04 |

## Account Context
Customer 1234567, two cloud projects plus one dedicated in Robot, EU only, reverse charge (valid VAT ID), Terraform-managed.

## Cloud Projects
| Project | Purpose | Environment | Token | Location | Notes |
|---------|---------|-------------|-------|----------|-------|
| acme-prod | main app | prod | keychain:hetzner-prod | fsn1 | read-write; CI uses a separate read-only token |

## Current Infrastructure
Network 10.10.0.0/16 in fsn1 · LB11 → 2× cax21 app · ccx13 postgres + 200 GB volume · Storage Box BX11 for Borg · dedicated AX41 (Robot) for CI, vSwitch into the network.

## Spend
### Monthly
| Month | Actual | As of | Budget | Top items | Notes |
|-------|--------|-------|--------|-----------|-------|
| 2026-06 | 118 EUR | 2026-06-30 | 150 EUR | AX41 49 · ccx13 26 · volumes 11 | closed, net |
| 2026-07 | 31 EUR | 2026-07-08 | 150 EUR | AX41 49 pro-rata · ccx13 · volumes | month-to-date, net |

### Alerts Configured
- Budget 150 EUR/month, reviewed on the invoice date; no provider-side budget alarm exists, so this is a `## Due` cadence

### Optimization Log
| Date | Change | Monthly saving |
|------|--------|----------------|
| 2026-05-11 | Deleted 6 orphaned primary IPs and 3 unattached volumes | 9 EUR |

## Pain Points
March 2026: staging left powered off for two months and billed in full. Sensitive to "off is free" advice since.

## How They Work
Comfortable in the console, new to Terraform. Wants the exact resource block, not the concept.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Cancellation deadlines and domain renewals belong here the day they become knowable; both are irreversible if missed.
- **`## Spend`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month. Re-reading the current month **overwrites** its row; never a second row for the same month. Amounts always carry their currency, and `Notes` records `net` or `gross` — a net figure compared against a gross one is a 19% error.
- **`## Cloud Projects`**: the `Token` column holds a pointer, never a token. One project stays here; from the second, the whole table moves to `cloud-projects.md` by the split procedure.
- These headings are exactly the ones the split-out files get, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their setup |
| `complete` | Know their projects, hardware and workflow well |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| app-prod-1 | hetzner | acme-prod | fsn1 | cax21 | app | 7 EUR | file:~/.ssh/id_ed25519 |
| db-prod | hetzner | acme-prod | fsn1 | ccx13 | postgres | 26 EUR | file:~/.ssh/id_ed25519 |
| ci-01 | hetzner-robot | Robot #2345678 | fsn1 | AX41 | CI runner | 49 EUR | keychain:hetzner-robot |
```

- **Identity is `Name` + `Provider`.** Read the file before adding. If that pair is already there, update the row in place — it is yours. Rows whose `Provider` is not `hetzner` or `hetzner-robot` belong to another skill: never touch them.
- **Cloud and Robot are different systems**, so they get different `Provider` values (`hetzner` and `hetzner-robot`) and different `Account / Project` values (the cloud project name, or the Robot server number). Same table, because the user's question is "what am I paying for", not "which API".
- **Retirement is part of the inventory.** When a server is deleted or a dedicated cancellation takes effect, delete its row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Amounts carry their currency in the value** (`7 EUR`), because AWS rows next to yours are in USD and someone will add the column up. Note `net` in `memory.md`, not in the value.
- **`Monthly` is a planning estimate, not the invoice.** After each reconciliation, refresh any Hetzner row whose real cost moved more than ~20%.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Access reference is a pointer only. Never a key, a token, or a password.

## Shared domains inventory

Lives at `~/Clawic/data/domains/domains.md`, shared with every DNS, hosting and registrar skill. Write here whenever a Hetzner DNS zone is created or moved, or a domain is registered or transferred.

```markdown
# Domains

| Domain | Registrar | Zone hosted at | Expires | Auto-renew | Used for | Notes |
|--------|-----------|----------------|---------|------------|----------|-------|
| example.com | hetzner | hetzner-dns | 2026-11-04 | yes | app + mail | managed LB certificate depends on this zone staying here |
```

- **Identity is the domain name.** Read the file before adding; if the row exists, update it in place. Rows for domains registered elsewhere are still updated in place when *this* skill moves their zone — change `Zone hosted at`, leave `Registrar` alone.
- **Renewal and expiry are the point of the box**: every row's `Expires` gets a matching `## Due` line in `memory.md`. An expired domain is not recoverable on the same terms.
- **Removal**: on transfer-out or expiry, delete the row and note the date in `memory.md`.
- **Scale cut**: one table in `domains.md` while there are ≤40 hostnames. Past that, group **by apex**, not by hostname: one `~/Clawic/data/domains/<apex>.md` holding every hostname under that apex with the same columns, and `domains.md` stays as the index (`Domain | Registrar | → file`). If it already looks like that, follow it — do not start a parallel `domains.md`.
- **Foreign columns win**, exactly as with `servers.md`. Never rewrite an existing header.
- Zone secrets (DNS API tokens, DKIM private keys) never appear here — pointer only.

## Shared contacts inventory

Lives at `~/Clawic/data/contacts/contacts.md`, shared with every skill that deals with people. This skill writes here for one reason: a server, a domain or a cloud project belongs to a client, and the person is not Hetzner data. The person goes there, the name alone stays here.

```markdown
# Contacts

| Name | Email or handle | Role | Preferred channel | Context |
|------|-----------------|------|-------------------|---------|
| Marta Ruiz | marta@acme.example | client | email | owns the acme-prod project; pays its invoice, wants figures net |
```

- **Identity is the email or handle**, never the display name — two clients share a name, nobody shares an address. Read the file and match on that column before writing. If the person is already there, update the row in place; only absence justifies a new row. With no address, put the handle in the same column (`@marta`, `slack:marta`), never a second identity column.
- **Only the person goes here.** The server, domain or project they own stays in its own box and names them. Duplicating the entity on both sides is the usual way two skills end up contradicting each other.
- **Rows this skill did not write are not yours.** Append your relationship to `Context` if the person is already listed; never edit another skill's `Role`, `Preferred channel` or identity value.
- **Removal**: when a client relationship ends, delete only rows this skill created and note the date in `memory.md`. If any other data still points at the person, keep the row and remove just the Hetzner clause from `Context`.
- **Scale cut**: table while there are ≤15 people. Past that, one file per person at `~/Clawic/data/contacts/<name-kebab>.md` with the same fields, and `contacts.md` becomes the index (`Name | Email or handle | Role | → file`). If you arrive and it already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- No credential a client shares ever lands here — their Hetzner login, a shared token, an invoice portal password are pointers or nothing.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, shared with the planning and delivery skills. Write here only when the user tracks this infrastructure work as a project: the decision summary and its monthly figure go there; the diagram, the runbook and the full text stay in `~/Clawic/data/hetzner/artifacts/` and are referenced by file name.

```markdown
## Infrastructure (hetzner)
2026-07-26 — Postgres on a CCX with Borg to a Storage Box, not a managed database.
Monthly: 26 EUR net, quoted 2026-07-26, fsn1. Restore drill quarterly, next 2026-08-14.
Detail and diagram: `~/Clawic/data/hetzner/artifacts/adr-postgres-ccx.md`.
```

- **Identity is the project name, and it is the file name** in kebab-case. Read the folder before creating anything: `acme-redesign.md` and `acme_redesign.md` are the same project and the second one is the bug.
- **Collision is an update in place**: if the file exists, edit the `## Infrastructure (hetzner)` section already in it; add that section only when it is absent. Never a second file for a project that exists, and never a rewrite of a section another skill wrote.
- **Amounts carry currency and quote date** (`26 EUR net, quoted 2026-07-26`) — the skills that read this file do not know Hetzner prices are net EUR.
- **Removal**: when the infrastructure is torn down, delete the `## Infrastructure (hetzner)` section and note the date in `memory.md`. Deleting the project file belongs to the skill that owns the project, never to this one.
- **Scale cut**: one file per project from the first — no shared table stage, no threshold. If the Hetzner content in one project file passes ~40 lines, move it to `~/Clawic/data/hetzner/artifacts/<project>-infrastructure.md` with its `## Boxes` line and leave a two-line summary plus the pointer behind.
- **Foreign structure wins.** If the file already organises itself under different headings, put the summary under the closest existing one instead of imposing this one. Never restructure someone else's project file.
- Token and credential pointers only, as everywhere else — a project file is the most-shared file in the system.

## cloud-projects.md

One project lives in `## Cloud Projects` in `memory.md`. From the second, this file, with the same heading and columns:

```markdown
# Cloud Projects

| Project | Purpose | Environment | Token | Location | Notes |
|---------|---------|-------------|-------|----------|-------|
| acme-prod | main app | prod | keychain:hetzner-prod | fsn1 | read-write |
| acme-stg | staging | staging | keychain:hetzner-stg | fsn1 | read-write, deleted nightly |
| acme-ci | CI read-only reporting | shared | env:HCLOUD_TOKEN_RO | — | read-only token |
```

The project is the permission boundary (SKILL.md Rule 2), so this table is the access map: which token can destroy what. When a project belongs to a client, the client goes in `~/Clawic/data/contacts/contacts.md` by the protocol in [shared contacts inventory](#shared-contacts-inventory) — identified by email or handle — and is referenced here by name only. Never duplicate the client record inside the Hetzner box.

## artifacts/

One file per thing, at `~/Clawic/data/hetzner/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **runbook**, **cloud-init / `user_data` that finally booted clean**, **firewall ruleset that finally worked**, **installimage config for a dedicated box**, **architecture decision with its diagram**, **migration or cutover plan**, **post-mortem of an abuse notice or an outage**, **price comparison against another provider**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — app-prod-1 rebuild from snapshot
*Read when: app-prod-1 is unbootable or compromised. Written 2026-07-26.*

...steps, with every secret replaced by its pointer...
```

```markdown
# Architecture decision — Postgres on CCX, not a managed database
*Read before any change to the data tier, and before sizing anything. 2026-07-26.*

Decision: ...one sentence...
Diagram: ...mermaid or ASCII...
Rejected: managed Postgres elsewhere — egress and latency across providers.
Estimated monthly: 26 EUR net, fsn1.
Irreversible parts: disk growth on the CCX; restore path is Borg from the Storage Box.
First limit: 16 volumes per server. First deadline: restore drill quarterly.
```

If the user tracks this work as a project, the decision summary also belongs in `~/Clawic/data/projects/<project>.md` by the protocol in [shared projects box](#shared-projects-box), with the diagram staying here and referenced by name.

## deploys/

```markdown
# Deploys and restores — 2026

| Date | Target | Image / commit | Provisioner version | Rollback target | Notes |
|------|--------|----------------|---------------------|-----------------|-------|
| 2026-07-24 | app-prod-1,2 | sha256:9f2c… / a41b7e | tf 1.14.2 | snapshot 2026-07-23 | rolling, LB drained |

## Recovery Drills
| Date | What was restored | Measured RTO | What was missing |
|------|-------------------|--------------|------------------|
| 2026-05-14 | Borg repo → scratch cax21 | 38 min | fstab entry, rDNS on the new IP |
```

## incidents/

Hetzner-specific and worth its own box, because the causes repeat and the response is time-boxed.

```markdown
# Incidents — 2026

| Date | Kind | What happened | Deadline | Response | Outcome |
|------|------|---------------|----------|----------|---------|
| 2026-04-02 | abuse notice | outbound scan from a compromised container | reply in 24h | container rebuilt, key rotated | closed |
| 2026-06-11 | hardware | AX41 disk failed, RAID degraded | — | Robot ticket, disk swapped, resync 6h | closed |
```

Kinds worth recording: `abuse notice`, `null-route`, `hardware`, `maintenance`, `lockout`, `limit reached`. Anything with a reply deadline also gets a `## Due` line until it is closed.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`spend-log.md` — `## Monthly`, `## Alerts Configured`, `## Optimization Log`. The optimization log is the reason this file exists: without it the same orphaned primary IPs get rediscovered every quarter and nobody can say what the last sweep was worth.

`resources.md` — the Hetzner-shaped inventory that is not a host (`## Networks`, `## Volumes And Snapshots`, `## Load Balancers`, `## Firewalls`, `## Known Gaps`), one `## <project>` heading per cloud project when there is more than one.
