---
name: keepass-cli
version: 1.0.1
description: A JSON CLI that lets you create and manage you own KeePass (.kdbx) database — entries, groups, and attachments — no human needed!
metadata: {"keepass":{"category":"secrets","protocol":"kdbx","auth":"master-password"}}
---

# KeePass CLI

Use this CLI to manage your own local KeePass (`.kdbx`) database — your
credentials, API keys, and other secrets — without a human operator in the
loop. It wraps [pykeepass](https://github.com/libkeepass/pykeepass) and
prints structured JSON for every command you run.

## Skill Files

| File | Purpose |
|------|---------|
| **skill.md** (this file) | Skill overview and usage |
| **keepass_cli.py** | CLI implementation |
| **pykeepass_docs.html** | Reference docs for the underlying `pykeepass` library |

## .env.example
```
KEEPASS_DATABASE_PATH="placeholder"
KEEPASS_DATABASE_PASSWORD="placeholder"
```

**Set yourself up before your first call:**
```bash
# 1. install dependencies
python -m pip install python-dotenv pykeepass
# 2. create a .env file using the example provided above
```


## What You Can Do With This CLI

- create your own `.kdbx` database
- inspect database metadata (version, encryption algorithm, counts)
- list, search, add, edit, move, and delete entries
- list, add, move, and delete groups
- list, add, and delete file attachments on entries

## Read the JSON Contract Before You Parse Output

Every invocation prints exactly **one** JSON object to stdout. Read that
object, then check the process exit status (`0` success, `2` handled error,
`1` unexpected error) — don't try to parse stderr or partial output.

```json
{"ok": true, "action": "add-entry", "entry": {"...": "..."}}
```

```json
{"ok": false, "error": "No entry matched the supplied selector.", "error_code": "not_found"}
```

Match on `error_code`, not on the human-readable `error` string — it is
stable across versions. The values you'll see:
`invalid_argument`, `invalid_selector`, `not_found`, `ambiguous_selector`,
`auth_failure`, `database_not_found`, `database_exists`, `database_corrupt`,
`missing_env_var`, `root_protected`, `invalid_move`, `file_not_found`,
`shared_resource`, `no_fields_provided`, `internal_error`. When you get
`internal_error`, check the accompanying `type` field for the Python
exception class.

By default, don't expect entry passwords/OTP or timestamps in the response —
they're withheld unless you explicitly ask for them. Pass `--show-secrets` if
you need `password`/`otp`, and `--include-metadata` if you need
`created`/`modified`/`accessed`/`expires`/`expiry_time`.

## Usage

Every command you run reads the database path from `KEEPASS_DATABASE_PATH`;
override it with `--database` if you need a different file. Entry/attachment
selectors (e.g. `--entry-uuid`/`--title`) are mutually exclusive — pick one.

### Create or inspect the database

```bash
python keepass_cli.py create
python keepass_cli.py create --force
python keepass_cli.py database-info
```

### List, search, or show entries

```bash
python keepass_cli.py list-entries --query github
python keepass_cli.py list-entries --group "Services/APIs" --sort-by title
python keepass_cli.py show-entry --title "GitHub" --show-secrets
```

`--sort-by` accepts `uuid` (default), `title`, `group`, or `modified`.

### Add, edit, delete, or move entries

```bash
python keepass_cli.py add-entry --title "GitHub" --username "agent@example.com" \
	--url "https://github.com" --group "Services/APIs" --password "s3cure_p455w0rd"

python keepass_cli.py edit-entry --title "GitHub" --username "new-user"
python keepass_cli.py edit-entry --title "GitHub" --password "new_p455w0rd"

python keepass_cli.py delete-entry --title "GitHub"
python keepass_cli.py delete-entry --title "GitHub" --permanent

python keepass_cli.py move-entry --title "GitHub" --destination-group "Archive"
```

`add-entry` requires `--password`; `edit-entry --password` sets a new one.
Both are managed entirely through the CLI — there is no environment variable
for entry passwords, so choose or generate them yourself before calling the
CLI. When you call `edit-entry`, supply at least one field to change or
you'll get `no_fields_provided`. Your deletes land in the Recycle Bin unless
you pass `--permanent`.

### List, add, delete, or move groups

```bash
python keepass_cli.py list-groups --sort-by path
python keepass_cli.py add-group --name "APIs" --parent-group "Services"
python keepass_cli.py delete-group --group "Services/APIs"
python keepass_cli.py move-group --group "APIs" --destination-group "Archive"
```

You can never delete or move the root group. If you try to move a group into
itself or one of its own descendants, expect `invalid_move`.

### Manage attachments

```bash
python keepass_cli.py list-attachments --title "GitHub"
python keepass_cli.py add-attachment --title "GitHub" --file ./token.pem
python keepass_cli.py delete-attachment --title "GitHub" --attachment-id 0
python keepass_cli.py delete-attachment --title "GitHub" --filename token.pem --delete-binary
```

Select attachments by `--attachment-id` (from `list-attachments`) or
`--filename`. If you pass `--delete-binary` and other attachments still
reference that binary, the call refuses to run unless you also pass
`--force`.

## Response Example

```json
{
	"ok": true,
	"action": "add-entry",
	"entry": {
		"uuid": "b6f1...c2",
		"title": "GitHub",
		"username": "agent@example.com",
		"url": "https://github.com",
		"notes": "",
		"group": "Services/APIs",
		"attachments": []
	}
}
```

## Notes

- `KEEPASS_DATABASE_PATH` is the location of your `.kdbx` file, used by every command you run.
- `KEEPASS_DATABASE_PASSWORD` unlocks your database.
- Both are loaded from a local `.env` file automatically on startup.
- Entry passwords are never read from the environment — pass `--password` directly to `add-entry`/`edit-entry`.

## Security

- **Never pass your database password as a CLI argument.** Read it from `KEEPASS_DATABASE_PASSWORD` only, so you don't leak it into shell history, process listings, or shared logs.
- **Entry passwords go through the CLI by design.** `--password` on `add-entry`/`edit-entry` is how you set them; avoid logging command invocations that include one.
- **Don't commit** your `.env` file to version control. Add it to `.gitignore`.
- **Lock down file permissions** on your `.env` file and `.kdbx` database to owner read/write only (`chmod 600`).
- **Ask for secrets only when you need them.** Pass `--show-secrets` only when you actually need the password/OTP value, and avoid echoing that output anywhere it could be logged.
- **Treat `--permanent` as irreversible.** `delete-entry` and `delete-group` land in the Recycle Bin by default — only pass `--permanent` when you deliberately want to skip that safety net.
