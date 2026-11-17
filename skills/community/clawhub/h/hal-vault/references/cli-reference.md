# hal-vault CLI reference

Complete command reference for [hal-vault](https://github.com/ofoxai/hal-vault).
Every command accepts `-d DIR` to select the vault directory (default
`$HAL_VAULT_DIR`, or `~/.hal-vault`).

## init

```
hal-vault init [-r PUBKEY] [-i PRIVKEY] [-d DIR]
```

Binds a new vault to an SSH key pair and writes an encrypted empty database.

- With no flags: uses the dedicated key `~/.ssh/hal-vault_ed25519(.pub)`,
  generating it on first use (never overwrites an existing file). Your
  day-to-day SSH keys are not touched.
- `-r` / `-i`: use an existing key pair (`ssh-ed25519` or `ssh-rsa`). With
  only `-r`, the private key path is derived by stripping `.pub`; with only
  `-i`, the public key is expected at `PRIVKEY.pub`.
- Fails if the vault is already initialized (`config.json` exists).
- Passphrase-protected private keys are prompted for on the terminal when
  decrypting.

## add

```
hal-vault add LABEL [-t TYPE] [--tags TAG,...] [-n NOTE] [-d DIR]
```

Stores a new secret. The value is **never** passed as an argument:

- stdin piped → reads all of stdin, strips one trailing newline (and CR)
- stdin is a terminal → hidden double prompt

Types: `api_key`, `password`, `token`, `ssh_key`, `cert`, `identity`,
`other` (default). Values must be valid UTF-8 (base64-encode binary
material first; invalid input is rejected, not corrupted).

Output: `added <id> <label>: <masked>`.

## get

```
hal-vault get ID|LABEL [--reveal] [--json] [-d DIR]
```

- Default: human-readable detail view with the value **masked**.
- `--reveal`: prints the raw value plus exactly one trailing newline —
  designed for `KEY=$(hal-vault get x --reveal)`, and for piping into a tool
  that reads the value on stdin. A substitution that lands in a command
  **argument** instead puts the plaintext in the process table; see
  "Where a revealed secret still leaks" in `SKILL.md`.
- `--json`: JSON object `{id,label,type,tags,note,masked,created_at,updated_at}`;
  a `value` field is included **only** when `--reveal` is also given.
- Lookup: exact ID match wins; otherwise case-insensitive exact label
  match. Ambiguous labels return an error listing candidate IDs (no values).

## list

```
hal-vault list [--json] [-d DIR]
```

Table of all entries: `ID TYPE LABEL TAGS MASKED UPDATED`. Always masked.

## search

```
hal-vault search [QUERY] [--tag TAG] [--type TYPE] [--json] [-d DIR]
```

- `QUERY`: case-insensitive substring over label, note, tags, and type.
- `--tag`: exact tag filter. `--type`: exact type filter.
- Filters AND-combine; at least one of query/tag/type is required.
- Same masked table rendering as `list`.

## update

```
hal-vault update ID|LABEL [--label L] [-t TYPE] [--tags TAG,...] [-n NOTE] [--value] [-d DIR]
```

- Metadata flags update in place; `--tags` **replaces** the whole tag list.
- `--value` (boolean): reads a new secret value from stdin or the hidden
  prompt, exactly like `add`.
- At least one flag is required.

## rm

```
hal-vault rm ID|LABEL [-f] [-d DIR]
```

Asks `remove <id> (<label>)? [y/N]` on a terminal. Non-interactive use
(piped stdin) requires `-f`.

## version

```
hal-vault version
```

Prints the release version (e.g. `v0.0.1`).

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | success |
| 1 | runtime error (not found, decryption failure, I/O) |
| 2 | usage error (bad flags/arguments, unknown command) |

## Storage model

- `~/.hal-vault/secrets.db` — the entire database as one age-encrypted blob
- `~/.hal-vault/secrets.db.bak` — previous generation, kept on every save
- `~/.hal-vault/config.json` — paths of the bound SSH key pair
- Saves are atomic and durable (fsync + single rename); concurrent
  processes serialize through an exclusive lock (`.lock`)
