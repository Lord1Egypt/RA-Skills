# Storage and Backups — Volumes, Snapshots, Storage Box, Object Storage

Scope: where bytes live and how they come back. Prices are EU locations, net of VAT, recorded 2026-07 — ratios stable, absolutes need verifying.

**Before proposing a backup design**, read `backup_target` in `~/Clawic/data/hetzner/config.yaml` and the restore-drill line in `## Due` — a design that contradicts the drill the user already runs is a regression.

**Contents:** [The Four Products](#the-four-products) · [Volumes](#volumes) · [Snapshots](#snapshots) · [Hetzner Backups](#hetzner-backups) · [Storage Box](#storage-box) · [Object Storage](#object-storage) · [Append-Only Borg](#append-only-borg) · [Choosing a Backup Target](#choosing-a-backup-target) · [The Restore Drill](#the-restore-drill) · [Encryption at Rest](#encryption-at-rest)

## The Four Products

| Product | Shape | Priced by | Survives the server | Good for |
|---|---|---|---|---|
| Volume | Block device, attached | GB/month | Yes | Data the server is actively using |
| Snapshot | Full disk image in the project | GB/month of used space | Yes | Cloning, moving, cheap "off", pre-change safety |
| Backup | Automated snapshot slots tied to a server | +20% of the server price | **No** | One-click whole-server restore |
| Storage Box | External SFTP/SMB/WebDAV/Borg target | TB/month | Yes | Backups, archives, anything cold |
| Object Storage | S3-compatible buckets | TB/month + traffic | Yes | Application assets, artifacts, S3-API workloads |

The economics that decide most designs: **per-TB storage is an order of magnitude cheaper than per-GB block storage.** Backups on a volume is the most common expensive mistake here.

## Volumes

- 10 GB minimum, 10 TB maximum, up to 16 attached per server, and always in the same location as the server. No cross-location attach, no cross-location move — copying over the network is the only migration.
- Attach and detach are live. **Grow is live and one-way**: a volume never shrinks. Grow the filesystem after growing the volume, or the extra space does not exist to the OS.
- Mount by stable path (`/dev/disk/by-id/…`), never by `/dev/sdb`, which reorders. Every `/etc/fstab` entry for a volume carries `nofail`, so a detached or slow volume never blocks boot into an unreachable state.
- A volume is not a backup: it fails with the server's availability domain, and `rm -rf` propagates to it instantly.
- Detached volumes keep billing. After every teardown, list volumes with no server (`costs.md`).

## Snapshots

- Billed on **used** space, not provisioned, so a 200 GB disk with 30 GB written costs like 30 GB.
- Taken from a running server they are **crash-consistent**: the filesystem journal replays, but an in-flight database transaction may not. Stop the database, or take a logical dump, before snapshotting anything transactional.
- The count is capped per project and there is **no lifecycle policy** — nothing expires them, nothing warns you. Whatever you create, you sweep, on the `## Due` cadence.
- A snapshot restores onto the same architecture and a disk at least as large. An ARM snapshot never boots an x86 server (`servers.md`).
- Snapshots can be transferred to another project, which is the supported path for promoting a machine between environments.

Use them as the safety step before anything irreversible: snapshot → verify it exists → then resize, rebuild, upgrade, or delete.

## Hetzner Backups

- Enabled per server, +20% of that server's price, keeping a rolling set of slots (7).
- Taken automatically in a rough daily window you influence but do not control precisely.
- **Deleted with the server.** They are a rollback tool, not disaster recovery: they die with the resource, with the project, and with the account.
- A restore overwrites the server in place. To restore *beside* production instead, convert the backup to a snapshot and build a new server from it.
- Worth paying for on stateful servers whose rebuild path is long. Waste on stateless servers that cloud-init recreates in two minutes (`costs.md`).

## Storage Box

External storage reached over SFTP, SCP, rsync, SMB, WebDAV and BorgBackup. It is not attached to a server and has no compute.

- Priced per TB per month — roughly an order of magnitude cheaper per byte than a volume.
- **Sub-accounts** are the feature that makes it safe: each server gets its own sub-account with its own credentials and its own directory, so one compromised host cannot delete another's backups.
- Supports its own snapshots of the box contents, which protects against a client deleting files.
- Traffic to and from a Storage Box in the same ecosystem is generally not the cost driver; the per-TB price is.
- Credentials are secrets: pointer only (`keychain:hetzner-storagebox`), never written under `~/Clawic/data/`.

## Object Storage

S3-compatible buckets in EU locations, priced per TB stored with an included traffic allowance and per-TB overage.

- Use the S3 API and existing tooling (`aws s3` clients, `rclone`, SDKs) — the compatibility is the point.
- Access keys and secrets are credentials: pointer only.
- No CDN in front of it from the provider. If public assets need edge caching, put an external CDN in front or serve from a server with caching headers.
- Good for artifacts, user uploads, and anything already written against S3. Not a filesystem — do not mount it and expect POSIX semantics for a database.

## Append-Only Borg

The pattern that survives a compromised server and an account lockout, and the reason `storage-box` is the default `backup_target`:

1. Each server has its own Storage Box sub-account and its own Borg repository.
2. The SSH key used for backups is restricted to append-only Borg operations on the server side, so a host that gets rooted **cannot delete or rewrite its own history** — the classic ransomware failure mode.
3. Pruning runs from somewhere the servers cannot reach: a separate maintenance job with a different, non-append-only credential.
4. Repository passphrases are secrets — pointer only, and stored somewhere that is not the machine being backed up.
5. Encryption is on: Borg encrypts client-side, which is also the answer to "the provider does not manage disk encryption" (below).

Keep at least one copy outside Hetzner if the account itself is a plausible failure mode — an abuse suspension or a payment problem takes same-provider backups with it.

## Choosing a Backup Target

| Situation | Target | Why |
|---|---|---|
| Solo operator, one or two servers, wants simplicity | `hetzner-backups` plus one off-provider copy of the data that matters | One click, whole-server restore, and the copy covers the account-level risk |
| Anything with a database or user data | `storage-box` with append-only Borg | Point-in-time history, client-side encryption, survives a rooted host |
| Assets and artifacts already written against S3 | `object-storage` | The application does not change |
| Regulated, or backups must leave the provider | `external` | Say the egress cost out loud in the design |

Whatever the target, the design states three numbers: how much data is lost in the worst case (RPO), how long a restore takes (RTO, measured not guessed), and the monthly cost.

## The Restore Drill

A backup nobody has restored is a hypothesis. The drill, quarterly, on the `## Due` cadence:

1. Create a scratch server (smallest type that fits the data).
2. Restore the most recent backup onto it — from the real repository, with the real credentials, following the runbook as written.
3. Start the application, verify the newest row or file is actually there.
4. **Time it**, and write down everything the runbook was missing: the `fstab` entry, the rDNS, the parameter file nobody backed up, the key that lived only on the dead machine.
5. Delete the scratch server.

**Write it down.** The measured RTO and the gaps go into the recovery-drill table in `~/Clawic/data/hetzner/deploys/<year>.md`, the next drill date into `## Due`, and the corrected procedure into `~/Clawic/data/hetzner/artifacts/runbook-restore.md` with its `## Boxes` line. A drill whose findings are not written down is a drill you will run identically next quarter.

## Encryption at Rest

Hetzner does not offer customer-managed encryption of cloud disks. If a compliance regime requires encryption at rest with your own key, it is LUKS inside the guest, and the honest cost is the unlock path:

- Unattended reboot needs the key available at boot — via a remote unlock over SSH in the initramfs, or a key server the machine can reach. Both are systems you now maintain.
- Document the unlock path in `~/Clawic/data/hetzner/artifacts/runbook-luks-unlock.md` with its `## Boxes` line, and rehearse it in the restore drill. An encrypted volume nobody can unlock at 3am is data loss with extra steps.
- The lighter alternative that covers most of the real risk: client-side encrypted backups (Borg) plus full-disk encryption only on the machines that genuinely hold regulated data.
