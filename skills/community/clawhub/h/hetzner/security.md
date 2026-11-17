# Security — Tokens, Access, Abuse, and the Leak Runbook

Scope: identity and the account. Packet filtering and exposure are a separate route from the Quick Reference (`firewall.md`).

**Before an audit or a hardening pass**, read `## Cloud Projects` in `~/Clawic/data/hetzner/memory.md` (or `cloud-projects.md` if `## Boxes` points there) — it is the access map: which token can destroy what.

**Contents:** [The Threat Model in Three Lines](#the-threat-model-in-three-lines) · [The Project Is the Permission Boundary](#the-project-is-the-permission-boundary) · [Tokens](#tokens) · [Robot Credentials](#robot-credentials) · [SSH](#ssh) · [Server Creation Hygiene](#server-creation-hygiene) · [Leaked Token Runbook](#leaked-token-runbook) · [Abuse Notices](#abuse-notices) · [Account Lockout as a Failure Mode](#account-lockout-as-a-failure-mode) · [Compliance and Data Residency](#compliance-and-data-residency) · [Audit Checklist](#audit-checklist)

## The Threat Model in Three Lines

1. **A leaked API token is a full project takeover** — create, delete, rebuild, and read every resource. There is nothing inside a project to limit it.
2. **A rooted server is a lateral-movement platform**, because the private network it sits on is unfiltered (`firewall.md`).
3. **Losing the account loses everything in it**, including same-provider backups. Abuse suspension and payment failure are the realistic paths.

Everything below is a control against one of those three.

## The Project Is the Permission Boundary

Hetzner Cloud has no IAM: no roles, no policies, no conditions, no per-resource grants. A token is read-only or read-write, and its scope is one project. That single fact should shape the layout:

- **One project per environment**: `prod`, `staging`, and one per client if you host for others. This is the only isolation mechanism available, and it is also the only cost boundary (`costs.md`).
- **One token per consumer**, not per person: CI gets its own, Terraform gets its own, the monitoring exporter gets a read-only one. Shared tokens cannot be rotated without an outage, so they never get rotated.
- **Read-only wherever writing is not required.** Dashboards, inventory scripts and cost reports never need write.
- A token that can reach production and staging at once is one leaked CI variable away from deleting both. If a tool genuinely needs both, give it two tokens.

Record every project, its purpose, and its token *pointer* in the Cloud Projects table. The value never appears anywhere under `~/Clawic/data/`.

## Tokens

- Shown exactly once at creation. If it was not captured, it is gone — create a new one rather than hunting for it.
- Store in the OS keychain, a password manager, or CI secrets. Never in a repository, a `terraform.tfvars` that gets committed, a shell history, a cloud-init `user_data` block, or a note file.
- Rotate on a cadence (six months is a reasonable default) and immediately on any suspicion. Rotation is: create the new token → update every consumer → verify → delete the old one. Deleting first causes the outage that makes people stop rotating.
- Environment variables leak into child processes and logs. That is acceptable for a short-lived CI job, and not acceptable for a long-running server — those should read from a secret manager at start.
- The `## Due` table carries the rotation date. A rotation nobody scheduled is a rotation that happens after the incident.

## Robot Credentials

Robot (dedicated servers) is a separate system with separate credentials, and people forget it exists during an audit:

- The Robot web interface login and the **web-service credentials** used by the Robot API are distinct from the Cloud console login and from Cloud API tokens.
- Robot API access is effectively account-wide over the dedicated fleet — there is no per-server scoping.
- Rescue-mode passwords are generated and displayed once per activation. They are credentials: pointer only, and they should be considered burnt after use.
- Two-factor on the account covers the interactive logins, not the API credentials. Rotate those separately.

## SSH

- Key-only. `PasswordAuthentication no`, and confirm it, because a distribution image can ship it enabled.
- One key per human, plus separate keys for automation. Shared keys make revocation impossible.
- Upload keys to the project so servers are created with them attached (below), and keep the project key list pruned when someone leaves.
- Port 22 scoped by the cloud firewall to fixed addresses, a bastion, or a VPN range — or closed publicly with access via WireGuard (`firewall.md`).
- Key *fingerprints* and key *names* are inventory and belong in notes; private keys and passphrases are secrets and are referenced as `file:~/.ssh/id_ed25519`, never copied.

## Server Creation Hygiene

- **Always attach an SSH key at creation.** Without one, the root password is emailed in plain text and now lives in a mailbox and its backups indefinitely. If it has already happened: log in, switch to key-only, rotate anything that password protected, and note the rotation in `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md` — the password itself is never written down.
- Apply the firewall by label selector so a new server is protected the moment it exists, not after someone remembers (`firewall.md`).
- Bake nothing secret into snapshots or images: a snapshot with a token in `/root/.config` is now a copyable credential that survives every server rebuild.
- Enable delete and rebuild protection on stateful servers in the same step (`servers.md`).

## Leaked Token Runbook

A Hetzner Cloud token in a public repository, a screenshot, a log, or a support ticket:

1. **Delete the token first.** Not rotate, not audit — delete. It grants full write to the project and there is no way to narrow it.
2. Create a replacement and update the consumers that legitimately needed it.
3. Read the project's resource list against your inventory: new servers, new firewalls detached, new SSH keys added, snapshots created (exfiltration path), servers rebuilt.
4. Check for a new server in an unfamiliar location — the common outcome is cryptomining on the biggest type available.
5. Rotate anything the token could have reached indirectly: keys stored in snapshots, credentials in `user_data`, anything a created server could have read from the private network.
6. Check the invoice and the resource count for the period, and expect an abuse notice if a created server misbehaved.
7. **Write it down**: the event, the exposure window, what was found, and what was rotated go into `~/Clawic/data/hetzner/incidents/<year>.md`; the corrected procedure goes into `~/Clawic/data/hetzner/artifacts/runbook-token-leak.md` with its `## Boxes` line.

Same shape for a leaked SSH private key, with step 1 being "remove the public key from every project and every `authorized_keys`", and for Storage Box credentials, with step 1 being "change the sub-account password and verify the append-only restriction held".

## Abuse Notices

Hetzner forwards abuse reports (spam, scanning, copyright, attack traffic) to the account's contact address with a **reply deadline**. This is an operational obligation, not correspondence:

- An unanswered report escalates: first a warning, then the server is locked, and a locked server takes the service down with it.
- Answer inside the deadline even if the investigation is not finished. "Received, investigating, service isolated" stops the escalation clock; silence does not.
- Investigate for real: a compromised container, an open relay, a forwarded mail loop, or a user-generated-content service being used as intended by the wrong people.
- Fix and say what you fixed. Repeated reports on the same cause are how accounts end.
- **Write it down**: the notice, its deadline, the cause and the outcome go into `incidents/<year>.md`, and the deadline goes into `## Due` until it is closed.

Make sure the abuse contact reaches a human who reads it. An abuse mail routed to an unmonitored alias is the single cheapest way to lose a production account.

## Account Lockout as a Failure Mode

Design for it, because it is real and it is total: an abuse suspension or a failed payment can make every resource unreachable at once, including Hetzner Backups and snapshots.

- Keep at least one copy of the data that matters outside the provider (`storage.md`).
- Keep infrastructure in code somewhere else (a git remote that is not on the same account), so rebuilding elsewhere is a day, not a project.
- Keep the billing contact and payment method current, and the abuse contact monitored. These two lines cover most of the risk.

## Compliance and Data Residency

- EU locations put processing under EU jurisdiction, which is a common and legitimate reason to be here. `data_residency: eu` removes the US and Singapore locations from every recommendation.
- A data processing agreement is available from the provider; whether one is on file is a fact worth recording in `## Account Context`, not something to guess about.
- The provider publishes certifications and audit documentation for its data centres — cite the current published set rather than a remembered one, and point the user at their own account's documents for anything contractual.
- What compliance does *not* come with: encryption at rest managed by the provider, key management, log retention, or access reviews. Those are yours (`storage.md`).

## Audit Checklist

| Check | Passing looks like |
|---|---|
| Account two-factor | On, for every human with access |
| Project layout | One per environment or client; no shared prod/staging project |
| Tokens | One per consumer, read-only where possible, all recorded as pointers, rotation date in `## Due` |
| Tokens in code | Nothing in the repository, `user_data`, or committed variable files |
| SSH | Key-only everywhere; project key list matches current people |
| Firewalls | Attached to every server, no `0.0.0.0/0` beyond 80/443/ICMP (`firewall.md`) |
| Private side | No service bound to `0.0.0.0` that should be private |
| Protection flags | On for every stateful server and volume |
| Backups | Off-provider or append-only copy exists, and a restore has been timed this quarter |
| Robot credentials | Web-service credentials rotated, rescue passwords treated as burnt |
| Abuse contact | Reaches a monitored inbox |
| Incidents | `incidents/<year>.md` has an entry for every notice, with its outcome |

**Write it down.** The audit result goes into `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`, any server it turns up into `~/Clawic/data/servers/servers.md`, token changes into the Cloud Projects table (pointers only), and the next audit date into `## Due`. The next session should start from the gaps, not from a fresh listing.
