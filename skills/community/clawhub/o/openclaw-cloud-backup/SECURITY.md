# Security Policy

## Threat model

Archive encryption protects backups **at rest in the bucket and in leak
scenarios** (bucket compromise, provider insiders, mislaid archive files).
It does not protect against host compromise — a shell on the host already
reads `~/.openclaw` directly. Consequences:

- Host-side mode-600 secret files (`~/.aws/credentials`, the passphrase
  file) are acceptable storage.
- Secrets inside `openclaw.json` are not: **this skill archives that file**,
  so a credential stored there is replicated into every backup it protects —
  exposure multiplied by retention count × destinations. This is the
  "amplifier" that drives the entire v2 credential design.

## v1.1.5 scanner findings → v2.0.0 remediation

ClawHub's automated scanners (skillspector v2.0.0 + clawscan) rated v1.1.5
"suspicious / DO_NOT_INSTALL". Each finding, what v1 did, and what v2 does:

| Finding | v1.1.5 (file:line) | v2.0.0 |
|---|---|---|
| **SQP-1** — activation description broad enough to trigger on generic "backup"/"restore" phrases, on a skill that archives, uploads, mutates config, and schedules | `SKILL.md:3` — "Use when the user says 'backup' …" | Description names OpenClaw state + S3 cloud and requires explicit intent; SKILL.md adds a "When to use — and when not to" section, per-action confirmation gates (config writes, first upload, credential storage, restore, prune, scheduling), and an unattended-runs policy restricting cron payloads to `backup`/`prune` |
| **SQP-2 (cron)** — daily cron job created by default without user opt-in | `SKILL.md:61-75` — "This step should be executed by default unless user asked not to do it" | Scheduling is strictly opt-in: offered once, after the first successful manual backup, with the exact `openclaw cron add` command and full payload shown; never created by default; never re-offered after a decline; the `schedule` subcommand only prints |
| **SQP-2 (credentials)** — provider docs instructed storing long-lived access keys in plaintext OpenClaw config without warnings | `references/providers/aws-s3.md:59-61`, `backblaze-b2.md:28-29`, `digitalocean-spaces.md:27-28`, `cloudflare-r2.md:28-29`, `minio.md:37-38`, `other.md:27-28`, `scripts/cloud-backup.sh:43-47`, and `SKILL.md:33-35` even instructed the agent to write the GPG passphrase into config | All six provider docs lead with least-privilege bucket-scoped keys stored in AWS named profiles (run by the user, outside the chat); the passphrase lives in a chmod-600 file or an OpenClaw SecretRef (`apiKey` + `primaryEnv`); every doc carries an identical "Credential safety" warning block including the amplifier; plaintext config keys still resolve (lowest priority) but emit loud DEPRECATED warnings on every run and are removed in v3 |

Beyond the findings, v2 also fixes two security defects the scanners did not
see:

- **Durable plaintext leftovers**: v1 wrote the plaintext tarball to disk,
  then encrypted; any failure in between stranded an unencrypted full-state
  archive in `~/.openclaw/backups`. v2 builds archives in a per-run mode-700
  staging directory removed on any exit (and swept after `kill -9`), and
  refuses plaintext output for secret-bearing scopes entirely (exit 14).
- **Passphrase on argv**: v1 invoked `gpg --passphrase "$GPG_PASSPHRASE"`,
  visible in `ps`/`/proc/*/cmdline` during every run. v2 passes it over a
  file descriptor.

## Operational hardening in v2

- Sensitivity verdict before every backup (file-provider stores,
  `credentials/`, legacy auth files, plaintext-in-config heuristic) →
  encryption forced for secret-material scopes.
- sha256 sidecars; decrypt-and-list verification after encryption (streamed,
  no plaintext on disk); HEAD size/sha verification after upload, with
  best-effort removal of mismatched remote objects.
- `flock`-based concurrency lock; disk-space and reachability preflights;
  documented exit-code map for unattended runs.
- Staged restores by default; tar member-path validation (no absolute paths,
  no `..`); in-place restores require typed confirmation and refuse
  cross-host state-dir mismatches.
- Local archive store relocated outside the state dir, with `backups/**`
  excluded non-negotiably — archives can never swallow older archives.

## Reporting a vulnerability

Please use GitHub Security Advisories on this repository
(https://github.com/obuchowski/openclaw-cloud-backup/security/advisories)
or open an issue asking for a private contact if the report is sensitive.
