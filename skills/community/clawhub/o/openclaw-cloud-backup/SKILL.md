---
name: cloud-backup
description: Secrets-safe encrypted OpenClaw backups to S3/R2/B2/MinIO — lean modes, opt-in cron, staged restore. Use only when explicitly asked to back up/restore OpenClaw.
metadata: {"openclaw":{"emoji":"☁️","homepage":"https://github.com/obuchowski/openclaw-cloud-backup","os":["linux","darwin"],"requires":{"bins":["bash","tar","jq"]},"install":[{"kind":"brew","formula":"awscli","bins":["aws"]},{"kind":"brew","formula":"gnupg","bins":["gpg"]}],"primaryEnv":"CLOUD_BACKUP_GPG_PASSPHRASE"}}
---

# OpenClaw Cloud Backup

The cloud layer for OpenClaw's native backup. Wraps `openclaw backup create`
(config, credentials, consistent SQLite snapshots, workspace), then GPG-encrypts
and uploads the archive to any S3-compatible bucket, with retention,
verification, and staged restore.

All commands: `bash "{baseDir}/scripts/cloud-backup.sh" <subcommand>`

## When to use this skill — and when not to

Act ONLY on an explicit user request about OpenClaw backups: "back up
openclaw", "restore my openclaw state", "set up cloud backups for openclaw",
"/cloud-backup", and similar.

- Generic requests ("back up my project", "save this file", "restore the
  database") are NOT for this skill. Ask what the user means before touching it.
- NEVER run this skill as a side effect of another task, proactively, or
  "while you're at it".
- Read-only subcommands (`status`, `list`, `verify`, `schedule`, and any
  `--dry-run`) may run freely once the user has asked about backups.
  Everything else follows the gates below.

## Confirmation gates

Before ANY state-changing action, show the user exactly what will happen and
get an explicit yes. One gate per action — do not re-ask for things the user
just confirmed, and never batch-confirm.

| Action | What you MUST show before doing it |
|---|---|
| Write config (`openclaw config patch`) | Every key=value you will write, verbatim. Never write secrets — see Credentials. |
| First backup to a new destination | Output of `backup <mode> --dry-run`: scope, sensitivity verdict, encryption status, target `s3://bucket/prefix`. |
| Store/replace a credential | Only the file path + storage method (AWS profile / passphrase file). The secret value itself should not transit this conversation — the user runs those commands themselves. |
| Restore | Step 1: always `restore <name> --dry-run` and show the file list. Step 2: state which paths will be overwritten (staged restores write to a fresh directory; `--in-place` overwrites live state), then require an explicit yes. Never skip the dry run. |
| Prune | Output of `prune --dry-run`: which archives (local and remote) will be deleted, by name. |
| Schedule creation | The exact `openclaw cron add ...` command and full payload text (see Scheduling). |

Repeat manual backups to an already-confirmed destination need no new gate —
the user's request IS the confirmation. Still echo the one-line plan
("full backup, encrypted, → s3://bucket/prefix") before running.

### Unattended runs (cron)

A scheduled job's payload marks the run as operator-preconfirmed for `backup`
and `prune` ONLY. In unattended runs: never restore, never change config,
never create or modify schedules, never store credentials.

## Modes — what each backup contains

Echo this table when the user asks what gets backed up:

| Mode | Includes | Excludes by default | Sensitivity |
|---|---|---|---|
| `backup full` (default) | openclaw.json, credentials/, secret stores, state + agent SQLite snapshots, agent memory, workspace, installed skills | session transcripts, codex caches/logs, tools/, media/, logs/, old backups | SENSITIVE — encryption forced |
| `backup full --everything` | everything above PLUS session transcripts and codex history | previous backup archives only | SENSITIVE — encryption forced |
| `backup settings` | openclaw.json, secret stores, credentials/, auth files | everything else | SENSITIVE — always encrypted, no opt-out |
| `backup workspace` | workspace directories (skills, memory files) | all state/config | encrypted by default; `--no-encrypt` allowed here only |

"SENSITIVE — encryption forced" means the script refuses to produce a plaintext
archive for that scope (exit 14). Do not work around it; if the user explicitly
wants a plaintext-shareable archive, offer `config.excludeSecrets=true` instead.
Users can tune scope with `config.exclude` / `config.include` (state-relative
globs).

## Subcommands

| Command | What it does | Gate? |
|---|---|---|
| `backup [full\|settings\|workspace] [--everything] [--no-upload] [--dry-run] [--json]` | Create archive, encrypt, upload, apply retention | dry-run free; see gates |
| `list` | Local + remote backups; flags failure debris | no |
| `status` | Health: last backup, credential sources, sensitivity verdict, schedule, reachability | no |
| `verify [name\|--latest] [--deep]` | Checksum + decrypt + listing; `--deep` adds `openclaw backup verify` | no |
| `restore <name\|--latest> [--target DIR \| --in-place] [--only GLOB] [--dry-run] [--yes] [--force]` | Staged restore by default | YES — two-step |
| `prune [--dry-run]` | Apply retention; remove failure debris | YES |
| `schedule` | PRINT the opt-in cron command (creates nothing) | no |
| `setup` | Setup checklist + connection test (never writes config) | config writes gated individually |

Exit codes (report them precisely, especially from cron): 0 ok ·
3 ok-with-warnings · 4 usage · 10 another run holds the lock · 11 missing
dependency · 12 insufficient disk · 13 cloud unreachable/bad credentials ·
14 encryption required but unavailable · 20-25 create/filter/encrypt/upload/
verify failures · 30 restore failure.

## First-time setup

Follow `references/setup-flow.md` step by step. Summary: choose provider →
user creates a least-privilege bucket-scoped key (per provider guide) → store
credentials OUTSIDE OpenClaw config (AWS profile recommended) → write
non-secret config (gate) → test connection → enable encryption with a
generated passphrase file → first manual backup (gate) → only then offer
scheduling (gate).

## Credentials

Resolution order and storage rules: `references/credentials.md`. Hard rules:

- NEVER write access keys or passphrases into openclaw.json (no
  `skills.entries.cloud-backup.env.*`). Backups archive that file: a plaintext
  credential in config is carried inside every archive it protects.
- S3 credentials live in an AWS named profile (`config.profile`, recommended)
  or operator-managed process env. The passphrase lives in a chmod-600
  passphrase file (`config.passphraseFile`).
- Operators who run OpenClaw's secret store can point the skill at it
  instead: `config.accessKeyRef` / `config.secretKeyRef` /
  `config.passphraseRef` accept OpenClaw SecretRefs ({source: env|file|exec})
  resolved against `.secrets.providers` — including 1Password-style exec
  providers. Configured-but-broken refs abort the run; they never fall back.
- Prefer flows where the secret never appears in this conversation: the user
  runs `aws configure --profile ...` and the passphrase generator themselves.
- If the script prints a DEPRECATED warning about plaintext config
  credentials, surface it to the user verbatim and offer the migration in
  `references/credentials.md`.

## Scheduling — strictly opt-in

NEVER create, modify, or enable a cron job by default, implicitly, or because
"backups should be scheduled". Skills document cron setup; only the user
opts in.

Offer scheduling exactly once, AFTER the first successful manual backup:

> "Backup verified. Want me to schedule this daily? I'd create this cron job —
> nothing is scheduled until you confirm:"

Then run `schedule` to print the exact command, adjust time/timezone/delivery
to the user's setup, show it in full, and wait for an explicit yes before
running it. If the user declines: drop it, and do not re-offer on later runs
(check `openclaw cron list` first — if a cloud-backup job exists, never offer).
To remove a schedule: `openclaw cron rm <id>`.

## Error handling (for you, the agent)

- Surface script stderr to the user verbatim (trim to the relevant lines).
  Never summarize an error into vagueness, never hide a WARN.
- Non-zero exit: diagnose using the exit-code table, explain, propose ONE fix.
  Never auto-retry `restore`, `prune`, or any `openclaw cron` mutation.
  `backup` may be retried once, only after the cause is fixed and the user
  agrees.
- Never invent bucket names, endpoints, or passphrases. Missing value → ask.
- Exit 14 (encryption required, no passphrase) fails hard by design — do not
  work around it with `--no-encrypt` or an ad-hoc passphrase. Run setup.
- The script cleans its staging on failure; if it reports it could not, tell
  the user the exact leftover path.

## Reference docs (read only when needed)

- `references/credentials.md` — resolution chain, v1→v2 migration, warnings
- `references/setup-flow.md` — guided first-time setup
- `references/providers/{aws-s3,cloudflare-r2,backblaze-b2,digitalocean-spaces,minio,other}.md`
- `references/security.md` — threat model, restore safety, incident response
