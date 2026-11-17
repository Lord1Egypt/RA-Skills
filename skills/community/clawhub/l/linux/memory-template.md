# Working File Templates — Linux

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced on their hosts. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/linux/config.yaml` | Key by key, read-modify-write |
| Host OS profiles, recurring incident patterns, tooling, how they work, due dates, box index | `~/Clawic/data/linux/memory.md` | Rewritten in place; stays small |
| The machines themselves — provider, region, role, cost, access reference | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| The people around the hosts — an admin, an on-call peer, a provider contact, someone being offboarded | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, referenced from here by name only |
| Decisions belonging to a tracked project — the summary, not the procedure | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, the procedure stays in `artifacts/` |
| What the OS on each host looks like — distro, init, firewall front end, MAC, filesystem layout, quirks | `## Hosts` in `memory.md`; `~/Clawic/data/linux/hosts.md` once it outgrows the split threshold | One row per host, keyed by the name in `servers.md` |
| Healthy-state numbers and the audit surface of a host | `~/Clawic/data/linux/baselines/<host>.md` | Its own file from the first host measured |
| Things you produced that get re-read — recovery runbooks, a tuning set with its rollback, an SELinux policy that finally worked, a documented procedure or decision | `~/Clawic/data/linux/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Incidents: symptom, root cause, fix, time to resolve | `~/Clawic/data/linux/incidents/<year>.md` | Append-only, cut by year |
| Changes applied to a host, with the persistence file and the rollback | `~/Clawic/data/linux/changes/<year>.md` | Append-only, cut by year |
| **Anything durable this table does not name** | `~/Clawic/data/linux/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A host was provisioned, discovered, rebuilt or decommissioned | Its row in `servers.md`, and its OS row in `## Hosts` |
| You learned the distro, init, firewall front end, MAC mode, or filesystem layout of a host | Its row in `## Hosts` |
| A healthy-state measurement, a listening-port sweep, or an audit-surface sweep ran | `baselines/<host>.md` |
| Anything on a host was changed — sysctl, unit drop-in, firewall rule, fstab entry, account, package hold, kernel parameter | `changes/<year>.md`, with the persistence file and the rollback |
| An incident was diagnosed and closed | `incidents/<year>.md`; if the same cause appears twice, add the pattern to `## Recurring Incidents` |
| A recovery procedure, a tuning set, or a policy that finally worked came out of the session | `artifacts/` |
| A backup target or retention was set, or a restore was actually verified | The host's row in `## Hosts`, and the drill in `## Due` |
| Recurring work was scheduled or run — patch window, reboot drill, restore drill, log vacuum, audit diff | `## Due` |
| A reboot became required and was not taken | The host's row in `## Hosts` (`reboot pending since <date>`) |
| The user declared a preference — distro, firewall tool, privilege style, thresholds, reboot policy, or a stance inside a preference area | Its key in `config.yaml`, never `memory.md` |
| A person entered or left the picture — a co-admin, an on-call peer, a provider or datacentre contact, an account being offboarded | Their row in the shared `contacts.md`; referenced from a change or incident row by name only |
| A decision was made inside a tracked project — a migration accepted, an architecture chosen, a window agreed | Its summary in the shared `projects/<project>.md`; the procedure stays in `artifacts/` and is referenced by name |

## Start flat, split only when it hurts

`## Hosts`, `## Recurring Incidents`, `## Environment` and `## How They Work` begin inside `memory.md`. Baselines, artifacts, incidents, changes and the shared inventory are born in their own box, because each is read whole and only when its subject comes up. Splitting a `memory.md` section is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/linux/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Hosts` in `memory.md` becomes `## Hosts` in `hosts.md`, same columns.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted `sshd_config`, `.env`, crontab, unit file, `smbcredentials`, or shell history is the densest source of secrets in this domain: substitute before writing, not after. Store the pointer in place of the value, in this shape: `<kind>:<locator>`.

`env:DB_PASSWORD` · `keychain:web01-root` · `1password:Infra/web01/root` · `vault:secret/infra/web01` · `file:~/.ssh/id_ed25519` · `file:/root/.smbcred` · `profile:ops`

In a config or a runbook the pointer goes exactly where the value was: `password: <vault:secret/infra/db>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: hostnames and FQDNs, IP addresses and CIDRs, usernames, UIDs and GIDs, group names, unit and package names, versions, kernel releases, device paths and UUIDs, mount points and mount options, port numbers, SSH public keys and key fingerprints, the *path* to a key or credential file, sudoers rule text, firewall rule shapes, SELinux labels and booleans. **Secrets, strip them**: private key material and passphrases, `/etc/shadow` hashes, LUKS passphrases and header backups, root and user passwords, contents of `EnvironmentFile` and `.env`, `smbcredentials` and `.pgpass` contents, API and webhook tokens, wifi PSKs, TPM recovery keys, database connection strings that carry a password, and anything in a shell history line that reads like a password.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [baselines/](#baselines) · [artifacts/](#artifacts) · [incidents/](#incidents) · [changes/](#changes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference — never from an observation, and never from a preflight question.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/linux/` if it does not exist.

```yaml
distro_family: rhel
init_system: systemd
firewall_tool: firewalld
privilege_mode: sudo
disk_alert_pct: 85
load_alarm_ratio: 1.5
destructive_confirm: true
reboot_policy: maintenance-window

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  config_management: ansible        # /etc is owned by a converge; fixes go to the repo
  multiplexer: tmux
conventions:
  local_units: /etc/systemd/system
  script_dir: /usr/local/sbin
restrictions:
  compliance: cis-level1
cadence:
  patch_window: "Tue 02:00 UTC"
```

A per-host fact is not a preference: `distro_family: rhel` in `config.yaml` means "this user's hosts are RHEL by default". A single Alpine box in a Debian shop goes in `## Hosts`, not here. If you find a declared preference sitting in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Linux Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Baseline for web01 → `baselines/web01.md`; read before calling any number on web01 high or low
- Boot recovery after the fstab incident → `artifacts/runbook-emergency-boot.md`; read the moment a host drops to emergency mode
- Incidents (7 this year) → `incidents/2026.md`; read when a symptom looks familiar or the user asks whether it happened before
- Changes (23 this year) → `changes/2026.md`; read before changing a host, and whenever a rollback is needed

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Security patching, all hosts | week, Tue 02:00 UTC | 2026-07-21 | 2026-07-28 |
| Restore drill (verify a backup by restoring it) | quarter | 2026-05-04 | 2026-08-04 |
| Reboot drill on web01 | quarter | 2026-04-12 | 2026-07-12 |
| Audit-surface diff (setuid, world-writable, listeners) | month | 2026-07-02 | 2026-08-02 |
| Journal and log retention review | quarter | 2026-06-30 | 2026-09-30 |

## Hosts
| Host | Distro / version | Init | Firewall | MAC | Filesystem layout | Backup target / last verified restore | Notes |
|------|------------------|------|----------|-----|-------------------|---------------------------------------|-------|
| web01 | Ubuntu 24.04 | systemd | ufw | AppArmor | LVM, ext4, /boot 512M separate | restic → b2, verified 2026-05-04 | reboot pending since 2026-07-20 (kernel) |
| db01 | Rocky 9 | systemd | firewalld | SELinux enforcing | XFS on LVM, /var/lib/pgsql own LV | pgBackRest → s3, verified 2026-06-11 | swappiness 10, THP never |

## Recurring Incidents
- `/boot` fills before every kernel upgrade on web01 — autoremove is not scheduled; fix applied 2026-06-02, watch it
- Cron report job silently stops after DST — moved to a timer with `Persistent=true` 2026-03-30

## Environment
Ansible owns `/etc` on both hosts; hand fixes must be followed by a commit. Prometheus node_exporter present, no alerting on PSI yet. No out-of-band console on db01 — provider web console only.

## How They Work
Wants the command first and the reasoning after. Dry-runs everything on db01. Never reboots outside the Tuesday window.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here: patch windows, restore drills, reboot drills, audit diffs, log retention reviews, certificate and key rotations.
- **`## Hosts`** is the OS profile, not the machine. The machine — provider, region, size, cost, access reference — lives in the shared inventory below, and `Host` here is the same name used there. Never duplicate provider or cost columns into this table; two copies of one machine is how two skills start contradicting each other.
- **`## Recurring Incidents`** holds patterns, not events: a line appears here only when the same cause has been seen twice. Every individual incident goes to `incidents/<year>.md`.
- These headings are exactly the ones `hosts.md` gets when `## Hosts` outgrows this file, so the split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their environment |
| `complete` | Know their hosts and habits well |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| web01 | hetzner | personal | fsn1 | CX32 | web + app | 8 EUR | file:~/.ssh/id_ed25519_web01 |
| db01 | bare-metal | office rack | — | Dell R640 | postgres | — | keychain:db01-console |
```

- **Identity is `Name` + `Provider`.** Read the file before adding anything. If that pair is already present it is the SAME machine, whichever skill wrote the row: update in place the fields you have direct evidence for (role, access reference, name) and leave every other cell byte for byte. Never append a second row for a host that is already listed.
- **Use the name the host answers to** (`hostnamectl`, or the name the user says), so the row a cloud skill wrote and the row you would write collide on purpose instead of becoming duplicates.
- **The OS profile does not go here.** Distro, init, firewall front end, MAC and filesystem layout belong in `## Hosts` in `memory.md`, keyed by this `Name`. Do not add columns for them.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Amounts carry their currency in the value** (`8 EUR`), because rows from other providers are in other currencies and someone will add the column up. Bare metal you own has no monthly figure: leave `—` rather than inventing one.
- **Retirement is part of the inventory.** When a host is decommissioned, delete its row, delete its `## Hosts` row, and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- Access reference is a pointer only (`file:~/.ssh/id_ed25519_web01`, `keychain:db01-console`, `1password:Infra/web01`). Never a key, a passphrase, or a password.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill. Written here when a person becomes part of the operation: a co-admin, the on-call peer, a provider or datacentre contact, or an account being offboarded (`users.md`).

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Ana Ruiz | sysadmin, shares root on web01 and db01 | email ana@example.com | on call weekends; owns the Ansible repo |
| Hetzner support | provider support | portal, ticket per host | escalation path for fsn1 hardware faults |
```

- **Identity is the email address or handle**, lowercased — not the Unix username, which is a per-host fact and stays in `## Hosts` or the offboarding row in `changes/<year>.md`. Read the file before adding.
- **Collision: update in place, never append.** If that address or handle is already there, whichever skill wrote the row, update only the fields you have direct evidence for and leave every other cell byte for byte. Two rows for one person is how two skills start contradicting each other.
- **This box holds the person, not the access.** Which accounts they hold, which groups, which keys are authorized — that is host state and belongs in `## Hosts`, `changes/<year>.md` and the offboarding row, which point here by name only.
- **Retirement is part of the record.** When someone is offboarded or leaves the team, delete their row and note the date in the offboarding row in `changes/<year>.md`. A contact list that only grows stops being one.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name-kebab>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Channel is how to reach them, never a password, a portal login, a public key, or a private judgement about them.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, and is shared with planning and delivery skills — the user may not have any of them installed, so the format travels with this skill. Written here only when the work belongs to a project the user tracks: the decision and its consequence, never the procedure, which stays in `artifacts/` and is referenced by name.

```markdown
# Datacentre migration — fsn1 to hel1

status: active            # active | paused | closed | cancelled

## Decisions
| Date | Decision | Why | Where the detail lives |
|---|---|---|---|
| 2026-07-22 | db01 moves last, after a timed restore drill | rollback window is the restore time, measured 38 min | `linux/artifacts/runbook-db01-cutover.md` |
```

- **Identity is the project name that names the file**, kebab-cased. Read the folder before creating anything: a file for that project probably already exists, written by another skill.
- **Collision: append under the existing heading, never a second file.** If the file exists, add your rows to the closest matching heading and leave the rest untouched. If its headings differ from these, follow its structure rather than imposing this one — foreign structure wins.
- **Only the summary crosses over.** Hosts stay in `servers.md`, OS profiles in `## Hosts`, the runbook or tuning set in `artifacts/`, people in `contacts/`. This file carries the decision, its date, its reason, and a pointer to where the detail lives.
- **Closing is a status, not a deletion.** A finished migration keeps its file with `status: closed` and the close date — it is the record of why the fleet looks the way it does. Only a project that never started is deleted.
- **Scale cut**: already one file per project, so there is none. If a single project's decision log passes ~40 lines, split the detail into `~/Clawic/data/linux/artifacts/<kebab-name>.md` and leave the pointer, exactly as with any other artifact.
- No credential and no access reference in a project file — those live where the Secrets section says, as `<kind>:<locator>` pointers.

## baselines/

One file per host, at `~/Clawic/data/linux/baselines/<host>.md`, created the first time you measure a healthy state or sweep the audit surface. The value of a baseline is entirely in the diff: without it, "high" is an opinion and "this listener is new" is a guess.

```markdown
# Baseline — web01
*Read before judging any number on web01, and before an audit review. Measured 2026-07-26, healthy period.*

## Healthy Numbers
load1 0.4-0.9 (4 cores) · PSI io some avg60 <2 · available 5.2 GiB of 8 · root fs 46% · await sda ~0.4 ms

## Listening
22 sshd · 80/443 nginx · 5432 postgres bound to 127.0.0.1 only

## Audit Surface
setuid binaries: 17 (list below) · world-writable: none outside /tmp · enabled units: 24

## Storage Layout
LVM vg0: root 40G ext4, /var 60G ext4, /boot 512M ext4 (separate — watch before kernel upgrades)
```

- Re-measure after a deliberate change of size (new workload, resize, distro upgrade) and overwrite the section; a stale baseline is worse than none because it makes a real regression look normal.
- Record the date and the words "healthy period". A baseline captured during an incident is a record of the incident.

## artifacts/

One file per thing, at `~/Clawic/data/linux/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **recovery runbook**, **tuning set with its rollback**, **a policy or ACL recipe that finally worked**, **a documented procedure or decision**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — db01 will not boot after a storage change
*Read when db01 drops to emergency mode or the initramfs prompt. Written 2026-07-26.*

...steps, with every secret replaced by its pointer...
```

```markdown
# Tuning set — db01 kernel parameters for postgres
*Read before changing anything under /etc/sysctl.d on db01, and to roll this back. 2026-07-26.*

Applied: vm.swappiness=10, vm.dirty_background_ratio=5, THP=never (kernel cmdline)
Persistence: /etc/sysctl.d/90-postgres.conf, GRUB_CMDLINE_LINUX
Rollback: delete the file, sysctl --system, remove transparent_hugepage=never, update-grub, reboot
Why: p99 write latency spikes traced to THP compaction; measured before/after, 40 ms → 6 ms
```

If the work belongs to a tracked project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md` (format and protocol under [shared projects](#shared-projects)), with the procedure staying here and referenced by name.

## incidents/

```markdown
# Incidents — 2026

| Date | Host | Symptom | Root cause | Fix | Time to resolve |
|------|------|---------|------------|-----|-----------------|
| 2026-06-02 | web01 | apt upgrade failed mid-transaction | /boot 100% full, truncated initramfs | freed /boot, `update-initramfs -u -k all`, autoremove scheduled | 40 min |
| 2026-07-14 | db01 | latency spikes, host CPU idle | cgroup CPU throttling, `nr_throttled` climbing | CPUQuota 100% → 250% | 25 min |
```

The second time a root cause repeats, add the pattern to `## Recurring Incidents` in `memory.md` — that is what turns a log into a lesson.

## changes/

```markdown
# Changes — 2026

| Date | Host | Change | Persistence | Rollback | Verified by |
|------|------|--------|-------------|----------|-------------|
| 2026-07-20 | web01 | ufw default deny inbound, allow 22/80/443 | ufw (persists by design) | `ufw default allow incoming` | new SSH session + external port scan |
| 2026-07-22 | db01 | LimitNOFILE=65536 on postgresql | drop-in /etc/systemd/system/postgresql.service.d/limits.conf | delete drop-in, daemon-reload, restart | `cat /proc/<pid>/limits` |
```

A change with no persistence column is a change that will disappear at the next reboot; a change with no rollback column is one nobody will dare undo at 3am. Fill both or the row is not worth writing.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings and columns it had inside `memory.md`.

`hosts.md` — `## Hosts`, one row per host with the same columns. This is the file that makes a fleet answerable: which boxes are RHEL, which still run SELinux permissive, which have a reboot pending, which had their last restore verified more than a quarter ago.
