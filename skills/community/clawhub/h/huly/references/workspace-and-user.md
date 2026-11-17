# Workspace & user — multi-tenant operations

This reference covers workspace lifecycle, member roles, and looking up user identities. Most other surfaces scope to a workspace; this is the layer they all sit on.

---

## Before you act on a workspace: confirm scope

`huly whoami --json` returns the active workspace. If multiple workspaces are available and the user didn't say which, ASK. Workspace boundaries are hard — a project in `production` is not visible from `staging`.

---

## Workspace lifecycle

```bash
huly workspace list                  # all accessible workspaces
huly workspace current               # what --workspace thinks is active
huly workspace use my-ws             # persist to active-workspace file
huly workspace info                  # uuid, region, mode
```

### Creating a workspace (requires OWNER on the account pod, or signup-time)

```bash
huly workspace create --name "my-project" --region us-west --yes
```

Takes ~30-60s. The CLI polls with retries (login can retry 3× if account-pod propagation lags). On success, prints `created workspace <name> <uuid>`.

### Deleting a workspace (CATASTROPHIC — no undo)

```bash
huly workspace delete my-ws --yes           # any non-active workspace
huly workspace delete --yes --force         # the ACTIVE workspace
```

The server pod runs `doCleanup` which drops **every document in every per-workspace table**. Comments, issues, channels, calendar events, documents, cards — all gone. There is no soft-delete.

**`--yes` is mandatory.** Deleting the active workspace additionally requires `--force`. The active-workspace file is NOT auto-cleared; subsequent commands will fail until you `huly workspace use <something-else>`.

### Renaming a workspace

```bash
huly workspace rename "new-name"
```

Reversible. Requires OWNER.

---

## Permissions — what each role can do

| Action                                                        | OWNER | MAINTAINER (Admin) | GUEST | READONLY |
| ------------------------------------------------------------- | ----- | ------------------ | ----- | -------- |
| `workspace delete`                                            | ✓     | ✗                  | ✗     | ✗        |
| `workspace member add`                                        | ✓     | ✗                  | ✗     | ✗        |
| `workspace rename`                                            | ✓     | ✗                  | ✗     | ✗        |
| `workspace guests` settings                                   | ✓     | ✗                  | ✗     | ✗        |
| `workspace access-link` create                                | ✓     | ✗                  | ✗     | ✗        |
| `workspace info` / `members` / `list` / `current` / `regions` | ✓     | ✓                  | ✓     | ✓        |
| Create projects, channels, calendars                          | ✓     | ✓                  | ✗     | ✗        |
| Read flagged-accessible spaces                                | ✓     | ✓                  | ✓     | n/a      |
| Write anywhere                                                | ✓     | ✓                  | ✗     | ✗        |
| Archive `#general` / `#random`                                | ✓     | needs Spaces Admin | ✗     | ✗        |

`MAINTAINER` cannot change their own role. Use the role alias `MAINTAINER` (or `admin`) — both normalize to `Admin`. The full set: `Owner | Admin | Guest | ReadOnlyGuest | DocGuest`.

---

## Adding / changing a member's role

```bash
huly workspace member add alice@example.com --role Admin
huly workspace member add bob@example.com --role Guest
huly workspace member add … --role ReadOnlyGuest   # read-only guest
```

There is NO `workspace member remove` exposed in the CLI (the underlying SDK method is not available). To remove someone: the account-server UI, or reset their role.

---

## Workspace guest settings

```bash
huly workspace guests --read-only true    # forces read-only on all members
huly workspace guests --sign-up true      # allows guest signups via invite link
```

Both flags parsed loosely: anything that isn't `'false'` or `'0'` is `true`. At least one must be passed.

---

## Creating invite links

```bash
huly workspace access-link --role Guest --exp-hours 24
huly workspace access-link --role Guest --email specific@invitee.com
huly workspace access-link --role DocGuest --auto-join
```

Returns the invite URL. Print or send it.

---

## Listing regions

```bash
huly workspace regions --json
```

Returns all available hosting regions (for selfhost, returns 1 region).

---

## User commands

### Get the current user

```bash
huly user get                        # current account profile
huly user get --json                 # machine-readable Person doc
```

### Get a user by UUID

```bash
huly user get --ref <uuid>           # Profile by account uuid
huly user get <email>                # may also work via resolver
```

### Update your own profile

```bash
huly user update --city "Berlin" --country "Germany" --bio "…" --name "Display Name"
```

At least one field required. Right after signup, if the Person doc isn't yet provisioned, throws `ExitCode.NotFound` with the hint "re-login and retry".

### Find a user by email (THE two-tier algorithm)

```bash
huly user find alice@example.com
huly user find alice@example.com --json
```

The CLI tries in order:

1. **Account-level:** `accountClient.findPersonBySocialKey(email, false)`. This catches users across the entire account pod — even users that aren't in your current workspace.
2. **Workspace-local:** scans `contact:class:Person` docs (limit 200) in your workspace, matches `name` case-insensitively (no email match).

Returns:

```json
{ "email": "alice@example.com", "personUuid": "…", "source": "account" }
```

When this command is useful: you need someone's `Person._id` for `schedule create --owner`, or you're trying to figure out whether someone is in the workspace at all.

---

## Common task recipes

### "What workspaces do I have access to?"

```bash
huly workspace list --json | jq -r '.[] | "\(.name)\t\(.url)\t\(.mode)"'
```

### "Switch the active workspace"

```bash
huly workspace use staging
huly whoami --json | jq .active_workspace
```

### "Who's in this workspace?"

```bash
huly workspace members --json | jq -r '.[] | "\(.name)\t\(.email)\t\(.role)"'

# Filter by role
huly workspace members --role Owner --json
huly workspace members --role Guest --json
```

### "Add someone as Guest"

```bash
huly workspace member add newuser@example.com --role Guest
```

### "Find a person who's not in our workspace"

```bash
huly user find someone@elsewhere.com --json
# {"personUuid": null, "source": "account"} means: exists in account pod, not in your workspace
# You can't add them directly — invite them via access-link.
```

---

## Gotchas

- **`workspace use`** refuses to run when `--workspace` or `HULY_WORKSPACE` is set. Unset first.
- **`workspace delete`** does NOT clear `active-workspace` automatically. Subsequent commands fail until you `use` something else.
- **`workspace members` on selfhost single-account** falls back to the cached login email for the operator (you). Don't be surprised when only one row appears.
- **`user find`** without `--json` prints `<email>\t<personUuid>` tab-separated — pipe to `awk`, not `jq`.
- **`workspace access-link`** with `--email` pre-binds the invite to that address. Without it, the link is anyone-with-the-link.
- The Huly account server uses `Owner | Admin | Guest | ReadOnlyGuest | DocGuest`. The CLI's `--role` flag aliases `MAINTAINER → Admin`, `READONLY → ReadOnlyGuest`. If you pass an unknown role, the server rejects it.
- **`WORKSPACE_LIMIT_PER_USER`** defaults to 10 on the account pod. Hitting it returns `WorkspaceLimitReached` from `createWorkspace`. CLI does not retry.
