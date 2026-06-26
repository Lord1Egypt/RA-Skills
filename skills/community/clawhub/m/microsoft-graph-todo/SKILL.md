---
name: microsoft-todo
description: "Microsoft To Do via Microsoft Graph. List task lists, read tasks, create tasks, update tasks, and mark tasks complete."
metadata:
  openclaw:
    category: "productivity"
    primaryEnv: "MS_TODO_CLIENT_ID"
    requires:
      bins: ["python3"]
      env: ["MS_TODO_CLIENT_ID", "MS_TODO_TENANT_ID"]
---

# microsoft-todo

Use Microsoft Graph To Do endpoints for personal task lists and tasks.

## When to Use

Use this skill when the user wants to:
- list Microsoft To Do task lists
- read tasks from a list
- create, update, complete, or delete tasks
- authenticate a Microsoft personal account or Entra-backed account for To Do

Do not use this skill for:
- Outlook mail APIs unrelated to To Do
- app-only Graph auth flows
- non-Microsoft task systems

## Inputs Needed

- `client_id` from an Entra app registration
- `tenant_id` for work/school accounts, or `consumers` for personal Outlook/Hotmail/Live accounts
- delegated Graph permissions: `Tasks.ReadWrite`

## Secret and Config Storage

Use the OS-native user config directory as the default. That matches common cross-platform practice and keeps secrets out of shell startup files.

Default config locations:
- Linux: `$XDG_CONFIG_HOME/microsoft-todo` or `~/.config/microsoft-todo`
- macOS: `~/Library/Application Support/microsoft-todo`
- Windows: `%APPDATA%\\microsoft-todo`

Use that config directory for:
- `client_id`
- `tenant_id`
- `token.json`
- `device_code.json`

Avoid putting bearer tokens or refresh tokens in:
- `~/.bashrc`
- `~/.zshrc`
- committed `.env` files

For quick local-only usage, the bundled Python helper also loads `scripts/.env` if it exists. That is an override path, not the primary default for published usage.

Supported environment overrides:
- `MS_TODO_TENANT_ID`
- `MS_TODO_CLIENT_ID`
- `MS_TODO_CONFIG_DIR`
- `MS_TODO_TOKEN_FILE`
- `MS_TODO_DEVICE_FILE`

## Auth Model

Microsoft To Do on Graph uses delegated permissions. Authenticate as a signed-in user with device-code flow.

Required delegated permissions:
- `Tasks.Read`
- `Tasks.ReadWrite`
- optional `offline_access`

Create a Microsoft Entra app registration, then store its IDs locally:

```bash
mkdir -p ~/.config/microsoft-todo
echo "YOUR_TENANT_ID_OR_consumers" > ~/.config/microsoft-todo/tenant_id
echo "YOUR_CLIENT_ID" > ~/.config/microsoft-todo/client_id
```

Where to get them:
- `tenant_id`: Azure Portal -> Microsoft Entra ID -> Overview -> `Tenant ID`
- `client_id`: Azure Portal -> Microsoft Entra ID -> App registrations -> your app -> `Application (client) ID`
- For personal Microsoft accounts, use `consumers` instead of the directory tenant ID in auth URLs

Authentication requirements in Entra:
- In `Authentication`, set `Allow public client flows` to `Yes`
- If shown, under `Mobile and desktop applications`, enable the platform and keep public client flows enabled
- Device-code flow will fail with `AADSTS7000218` if the app is still treated as a confidential client
- For personal Microsoft accounts, set supported account types to include personal accounts

Bundled helper:
- `scripts/ms_todo_auth.py` handles device-code auth, token polling, refresh-token exchange, access-token output, and resolved path inspection

Optional local override file:
- `scripts/.env.example` shows the supported variables for a portable setup
- copy it to `scripts/.env` only if you explicitly want local overrides

## Get an Access Token

Create the default config directory and store the app IDs:

```bash
python3 scripts/ms_todo_auth.py show-paths
```

Then place:
- `tenant_id` in the reported `tenant_file`
- `client_id` in the reported `client_file`

Request a device code:

```bash
python3 scripts/ms_todo_auth.py device-code
```

The response includes `user_code`, `verification_uri`, and `device_code`, and saves the full payload to `device_code.json`.

Open the `verification_uri`, enter the `user_code`, sign in, then poll for tokens:

```bash
python3 scripts/ms_todo_auth.py poll-token
```

This saves the full token response to `token.json` but does not echo raw token JSON with bearer or refresh secrets to stdout.

Refresh later when needed:

```bash
python3 scripts/ms_todo_auth.py refresh-token
```

This also updates `token.json` without echoing raw token JSON secrets to stdout.

Extract the bearer token when needed:

```bash
ACCESS_TOKEN=$(python3 scripts/ms_todo_auth.py access-token)
```

Do not hardcode access tokens in the skill. They expire.

Example with env-var overrides:

```bash
MS_TODO_TENANT_ID=consumers \
MS_TODO_CLIENT_ID="your-client-id" \
python3 scripts/ms_todo_auth.py device-code
```

Example with portable local overrides in `scripts/.env`:

```dotenv
MS_TODO_TENANT_ID=consumers
MS_TODO_CLIENT_ID=your-client-id
MS_TODO_CONFIG_DIR=./state
```

## Base Request Pattern

```bash
ACCESS_TOKEN=$(python3 scripts/ms_todo_auth.py access-token)

curl -s "https://graph.microsoft.com/v1.0/me/todo/lists" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" | jq
```

## Common Operations

### List task lists

```bash
curl -s "https://graph.microsoft.com/v1.0/me/todo/lists" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq
```

### Get one task list

```bash
LIST_ID="your-list-id"

curl -s "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq
```

### List tasks in a list

```bash
LIST_ID="your-list-id"

curl -s "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq
```

### Create a task

```bash
LIST_ID="your-list-id"

curl -s -X POST "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy milk",
    "importance": "normal"
  }' | jq
```

### Update a task

```bash
LIST_ID="your-list-id"
TASK_ID="your-task-id"

curl -s -X PATCH "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy milk and eggs",
    "status": "inProgress"
  }' | jq
```

### Mark a task complete

```bash
LIST_ID="your-list-id"
TASK_ID="your-task-id"

curl -s -X PATCH "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }' | jq
```

### Delete a task

```bash
LIST_ID="your-list-id"
TASK_ID="your-task-id"

curl -i -X DELETE "https://graph.microsoft.com/v1.0/me/todo/lists/$LIST_ID/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Notes

- To Do is user-scoped. Use delegated auth, not app-only auth.
- Hardcoding `tenant_id` and `client_id` is acceptable for a personal setup, but store them in the platform config directory unless you intentionally choose `scripts/.env` for a local portable copy.
- A bearer token comes from the token endpoint after device-code sign-in. It is not shown in the Azure dashboard.
- If you want automatic renewal, save the refresh token from `token.json` and exchange it for a new access token later.
- `poll-token` and `refresh-token` persist the full token payload to `token.json`; stdout is summarized so raw token JSON secrets are not printed.
- For personal Outlook/Hotmail/Live accounts, set `tenant_id` to `consumers` for device-code and token requests.

## Validation

The skill is working when:
- `python3 scripts/ms_todo_auth.py show-paths` reports the expected config locations
- `python3 scripts/ms_todo_auth.py device-code` returns a `user_code`
- `python3 scripts/ms_todo_auth.py poll-token` writes the platform config `token.json`
- `GET /v1.0/me/todo/lists` returns a JSON `value` array

## Common Failure Modes

- `AADSTS7000218`: app is not configured as a public client
- `AADSTS700016` on `consumers`: app does not allow personal Microsoft accounts
- `MailboxNotEnabledForRESTAPI`: account auth worked, but mailbox/To Do access is not usable for that account/authority combination
- `authorization_pending`: complete the device-code sign-in in the browser and retry token polling

## Links

- Graph To Do overview: https://learn.microsoft.com/en-us/graph/api/resources/todo-overview
- Device code flow: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code

## User Setup Checklist

Before using this skill, do this once in Azure Portal and once on your local machine:

1. Go to Azure Portal -> Microsoft Entra ID -> App registrations -> New registration.
2. Name the app something like `Microsoft To Do Skill`.
3. Set supported account types to `Accounts in any organizational directory and personal Microsoft accounts`.
4. Create the app, then copy the `Application (client) ID`.
5. If you want personal Microsoft accounts such as Outlook/Hotmail/Live, use `consumers` as the tenant value for this skill.
6. If you only want a specific work or school tenant, use that Entra tenant ID instead.
7. Open the app's `Authentication` page and enable `Allow public client flows`.
8. If Azure shows a `Mobile and desktop applications` platform section, enable it and keep the app as a public client.
9. Open `API permissions`, add Microsoft Graph delegated permissions, and include `Tasks.ReadWrite`.
10. Keep `offline_access` available for refresh-token renewal during device-code auth.
11. Run `python3 scripts/ms_todo_auth.py show-paths` to see where this skill expects local config files.
12. Create the reported `tenant_id` file and `client_id` file with your chosen tenant value and copied client ID.
13. Run `python3 scripts/ms_todo_auth.py device-code`, open the returned `verification_uri`, and enter the `user_code`.
14. After sign-in completes, run `python3 scripts/ms_todo_auth.py poll-token`.
15. Confirm that `token.json` was written, then use `python3 scripts/ms_todo_auth.py access-token` or call `GET /v1.0/me/todo/lists`.

If device-code auth fails, re-check these settings first:
- account type allows personal accounts if you are using `consumers`
- public client flows are enabled
- Microsoft Graph delegated permission `Tasks.ReadWrite` is present
