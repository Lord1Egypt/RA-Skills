# Auth & setup — how the CLI decides who you are

This reference covers: the three auth modes, the token cache, env vars, signup, and how the CLI resolves a workspace when you don't tell it.

---

## Before anything else: verify the auth state

ALWAYS run this first when context is ambiguous:

```bash
huly whoami --json
```

Returns:

```json
{
  "url": "https://huly.example.com",
  "account": "alice@example.com",
  "active_workspace": "production",
  "workspaces": [{"name": "production", "url": "…", "uuid": "…", "mode": "active"}, …]
}
```

If `active_workspace` is `null` or missing: STOP. Run `huly workspace list --json` to see what's available, then either pass `--workspace <name>` for one command or `huly workspace use <name>` to persist it.

---

## The three auth modes

### 1. Interactive password login (only for humans)

```bash
huly login
# prompts for URL, email, password if not set
```

Use this when a human is at the terminal. Do NOT use this in agent scripts.

### 2. Headless login (agents, CI, cron)

```bash
export HULY_URL=https://huly.example.com
export HULY_EMAIL=alice@example.com
export HULY_PASSWORD=…
huly login --headless
huly whoami
```

`--headless` reads ONLY env vars. NEVER prompts. Required env vars:

- `HULY_URL` — the server. The CLI refuses to run with **no** URL.
- `HULY_EMAIL`
- `HULY_PASSWORD`

If any are missing in headless mode: `ExitCode.Validation` with a hint listing every missing field.

### 3. Pre-issued JWT (best for service accounts / agents)

```bash
export HULY_URL=https://huly.example.com
export HULY_TOKEN=eyJ0eXAiOiJKV1Q…
huly whoami
```

`HULY_TOKEN` bypasses the credential cache entirely — it does NOT read or write `~/.config/huly/credentials.json`. Use this when:

- Running as a service account with a long-lived JWT
- You don't want to store the password anywhere
- The JWT has a short TTL you manage externally

**Caveat:** operations can fail with workspace-scoped authorization errors because `HULY_TOKEN` doesn't carry the per-workspace token cache. If you hit 403 on a workspace-scoped call, fall back to mode 2.

---

## The token cache (`~/.config/huly/credentials.json`, mode 0600)

Shape (simplified):

```json
{
  "huly.example.com": {
    "alice@example.com": {
      "accountToken": "eyJ…",
      "workspaces": {
        "production": { "token": "eyJ…", "role": "OWNER" },
        "staging": { "token": "eyJ…", "role": "MAINTAINER" }
      }
    }
  }
}
```

- **Re-login preserves `workspaces`** — calling `login` again only refreshes the account token, never clobbers your workspace tokens.
- **Cache hit silent** — if you have a token for the URL + email, you'll never be prompted for credentials.
- **Path:** `~/.config/huly/credentials.json` (or `$XDG_CONFIG_HOME/huly/credentials.json`). Always mode 0600.

Two sibling files:

| File               | Purpose                                                                                                                                                                                           | Mode        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `credentials.json` | Tokens (above)                                                                                                                                                                                    | 0600        |
| `bootstrap.json`   | Per-account marker for completed workspace-identity bootstrap, keyed on `host -> workspace -> accountUuid -> {at}`. Delete the file (or just the affected account entry) to force a re-bootstrap. | 0600        |
| `active-workspace` | Last-used workspace name                                                                                                                                                                          | 0600        |
| `active-account`   | `host\|email` per host                                                                                                                                                                            | 0600        |
| `.env`             | URL + credentials if you want them on disk                                                                                                                                                        | your choice |

---

## Why there is NO `huly logout` command

Intentionally. The CLI is designed for long automation runs. An accidental `logout` mid-automation would force every subsequent command to re-`selectWorkspace` for every workspace, breaking idempotency. The only way to "log out" is manual.

> **Manual cleanup (advanced).** You are about to delete local credentials and unset authentication env vars. This is irreversible until you `huly login` again. Confirm with the user before running this in any context other than your own machine.
>
> The procedure below is the **complete** reset: it clears the on-disk JWT cache (XDG-aware), the active-workspace / active-account pointers, the per-account bootstrap marker, the dotenv file the CLI loaded (`HULY_ENV_FILE` if set, else `$HOME/.config/huly/.env`), and unsets the auth env vars in the current shell. A partial reset that leaves the dotenv file intact will allow a later process to re-authenticate from that file.
>
> **Dotenv path note:** the dotenv loader (`packages/cli/src/auth/env.ts:23`) is **not** XDG-aware — its default is `$HOME/.config/huly/.env`, even when `XDG_CONFIG_HOME` is set. The cached credential files (`credentials.json`, `active-workspace`, `active-account`, `bootstrap.json`) **are** XDG-aware (`configDir()` honors `$XDG_CONFIG_HOME`). The reset handles both paths correctly.

```bash
# Advanced — manual credentials reset.
# Deletes the on-disk token cache (XDG-aware, mode 0600), the active-workspace
# pointer, the per-account bootstrap marker, the dotenv file the CLI loaded
# (note: dotenv loader is NOT XDG-aware — default is $HOME/.config/huly/.env),
# and unsets the auth env vars in the current shell.
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/huly"
env_file="${HULY_ENV_FILE:-$HOME/.config/huly/.env}"
rm -f "$config_dir/credentials.json" \
      "$config_dir/active-workspace" \
      "$config_dir/active-account" \
      "$config_dir/bootstrap.json" \
      "$env_file"
unset HULY_TOKEN HULY_EMAIL HULY_PASSWORD HULY_WORKSPACE
```

Then re-export the auth inputs the reset just unset, and re-authenticate. `--headless` reads ONLY env vars and will fail if `HULY_URL` / `HULY_EMAIL` / `HULY_PASSWORD` are missing:

```bash
# Re-export the auth inputs the reset just unset.
export HULY_URL=https://huly.example.com
export HULY_EMAIL=you@example.com
export HULY_PASSWORD=…     # or: export HULY_TOKEN=eyJ…

# Then re-auth.
huly login --headless
```

(Or skip the env setup and run interactive `huly login`.)

If you want a partial reset (only clear one host / email pair, keep the others), edit `credentials.json` by hand — the file is keyed by host then email — and keep the rest of the cache intact. The dotenv file and env vars above are NOT cleared in that case.

---

## Environment variables (full cheat sheet)

| Var                                  | Default               | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Required?                                            |
| ------------------------------------ | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `HULY_URL`                           | —                     | Server URL                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | **YES**. Exits with `HULY_URL is required` if unset. |
| `HULY_EMAIL`                         | —                     | Login email                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Required for `--headless` login                      |
| `HULY_PASSWORD`                      | —                     | Login password                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Required for `--headless` login                      |
| `HULY_TOKEN`                         | —                     | Pre-issued JWT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Alternative to password                              |
| `HULY_WORKSPACE`                     | —                     | Default workspace (URL slug or UUID)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Falls back to `active-workspace` file                |
| `HULY_PROJECT`                       | —                     | Default project for `--project` and bare-number issue refs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Optional                                             |
| `HULY_TEAMSPACE`                     | —                     | Default teamspace for `--teamspace`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Optional                                             |
| `HULY_FIRST_NAME` / `HULY_LAST_NAME` | —                     | Signup                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Required for headless signup                         |
| `HULY_ENV_FILE`                      | `~/.config/huly/.env` | Path to the dotenv file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Optional                                             |
| `HULY_NONINTERACTIVE`                | —                     | `1` disables ALL prompts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Optional                                             |
| `HULY_INSECURE_TLS`                  | —                     | `1` disables TLS verification globally                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Avoid in production                                  |
| `HULY_SKIP_BOOTSTRAP`                | —                     | `1` skips the auto workspace-identity bootstrap on `connectCli`. Set this in CI / benchmarks / when the workspace must stay untouched. Leave unset for normal agent runs — the bootstrap is idempotent and writes a per-`(host, workspace, accountUuid)` marker to `~/.config/huly/bootstrap.json`. Cost per fresh CLI process: 1 read of `bootstrap.json` to look up the marker for the current account, plus 1 `getAccount()` transactor round-trip and, only when that marker is missing, the bootstrap transactor round-trip (createDoc / addCollection / mixin) to reconcile Person + SocialIdentity + Employee. Subsequent calls within the same process short-circuit on an in-memory lookup once a bootstrap has succeeded, so they cost 0 after the first successful bootstrap in that process; later CLI processes pay the same per-process cost. | Optional                                             |
| `NO_COLOR`                           | —                     | Disables chalk colors                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Optional                                             |
| `CI`                                 | —                     | Triggers JSON output and disables spinner                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Optional                                             |

Precedence (highest to lowest): **CLI flag > env var > cached file > hardcoded default**.

---

## Signup — first-run for a new account

```bash
# Interactive (won't be used by agents)
huly signup --email you@example.com --password '…' --first You --last Name

# Headless
export HULY_URL=https://huly.example.com
export HULY_EMAIL=you@example.com
export HULY_PASSWORD=…
export HULY_FIRST_NAME=You
export HULY_LAST_NAME=Name
huly signup --headless

# Signup + create first workspace atomically
huly signup --headless --create-workspace my-ws
```

On selfhost the signup endpoint is open. On hosted/invite-only deployments the account server may reject uninvited signups — use `huly workspace access-link --role GUEST` instead.

If signup doesn't return a session token (account-pod propagation lag), the CLI retries login up to 3× with exponential backoff (250/500/750 ms).

**Right-after-signup caveat:** the CLI auto-runs `ensureEmployee()` on the first `connectCli` after signup / workspace creation / join, so `huly user update`, `huly notification settings update`, `--assignee <email>` lookups, and the `ProjectToDo` cascade all work on the first command without ever opening the workspace in a browser. The bootstrap is idempotent (a per-`(host, workspace, accountUuid)` marker is written to `~/.config/huly/bootstrap.json`): subsequent commands in the same process are zero-cost after the first successful bootstrap, while later CLI processes repeat the single disk read + `getAccount()` check (and the bootstrap transactors only if the per-account marker is missing). Set `HULY_SKIP_BOOTSTRAP=1` to opt out entirely.

---

## Workspace resolution algorithm

When you don't pass `--workspace`, the CLI tries (highest priority first):

1. `--workspace` flag on this invocation
2. `HULY_WORKSPACE` env var
3. `~/.config/huly/active-workspace` (set by `huly workspace use`)
4. Hard error: `set --workspace, HULY_WORKSPACE, or run huly workspace use <name>`

The workspace spec can be a name, a URL slug, or a UUID — the CLI passes the string through and the SDK resolves on connect.

---

## Minimal `.env` for an agent

```bash
HULY_URL=https://huly.example.com
HULY_EMAIL=agent@example.com
HULY_PASSWORD=…
HULY_WORKSPACE=production
HULY_PROJECT=BACKEND
HULY_NONINTERACTIVE=1
```

Mode 0600 recommended:

```bash
chmod 600 ~/.config/huly/.env
```

---

## Connecting to a new server (rotating URLs)

When the server URL changes (e.g. selfhost migration), update `HULY_URL` AND clear the cache, otherwise the CLI will try the cached token against the new host and fail:

```bash
export HULY_URL=https://huly-new.example.com
huly login --headless            # creates a new credentials.json entry
huly workspace list --json        # confirm reachability
```

The cache is keyed by host, so old entries do not interfere — they just sit unused.

---

## Multi-workspace operations

To act across workspaces in one session, pass `--workspace` per command. The active-workspace file is **only** the default; explicit `--workspace` overrides without persisting:

```bash
# Active is "production"; this one-shot targets "staging" without changing the default:
huly --workspace staging issue list --json | jq 'length'

# Persist a new default:
huly workspace use staging
```

`huly workspace use <name>` REFUSES to run if `--workspace` or `HULY_WORKSPACE` is already set in the environment — to prevent ambiguous state.

---

## CI / GitHub Actions recipe

```yaml
- name: Sync CI status to Huly
  env:
    HULY_URL: ${{ secrets.HULY_URL }}
    HULY_TOKEN: ${{ secrets.HULY_TOKEN }}
    HULY_WORKSPACE: production
    HULY_NONINTERACTIVE: '1'
  run: |
    huly issue create --project CI --title "${{ github.event.head_commit.message }}" \
                      --label auto --label ci --yes
```

Prefer `HULY_TOKEN` over password in CI. Issue a short-TTL service-account JWT and rotate.

---

## Looking up a user's UUID (you'll need this for `schedule create --owner`)

```bash
huly user get --json | jq -r '._id'
```

`schedule create --owner` takes a **Person UUID**, not an email. Don't confuse with `action create --owner` which DOES accept an email.

---

## Gotchas

- `HULY_TOKEN` does NOT write to cache — re-launching without it loses the token. Cache it externally.
- The account pod enforces `WORKSPACE_LIMIT_PER_USER` (default **10**). Hitting it returns `WorkspaceLimitReached`. The CLI does not retry.
- `huly signup --create-workspace` takes ~30-60s end-to-end (the workspace pod runs tracker migration). Don't kill it early.
- New workspaces auto-create `#general` and `#random` channels and seed default IssueStatuses. Server-side, out of CLI scope.
- After `workspace delete --yes --force`, deletion is asynchronous — the workspace pod runs `doCleanup` which drops all per-workspace tables. May take minutes.
