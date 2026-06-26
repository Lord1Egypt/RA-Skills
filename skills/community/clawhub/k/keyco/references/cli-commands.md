# Keyco CLI — Complete Command Reference

Full reference for every `keyco` command. Use this when you need precise flags or behavior.

## Global Flags

| Flag | Description |
|---|---|
| `--output`, `-o` | `table` (default), `json`, or `csv` |
| `--help`, `-h` | Help for any command |

## Configuration

- `keyco configure` — Interactive setup
- `keyco status` — Check API connectivity
- Environment overrides: `KEYCO_API_KEY`, `KEYCO_BASE_URL`, `KEYCO_OUTPUT`

## Auth

- `keyco auth login [--email E] [--password P]` — Email/password
- `keyco auth logout` — Clear credentials
- `keyco auth status` — Verify current token

## DUBs (assets)

- `keyco dub get --uuid <UUID>` — Single asset
- `keyco dub list [--page N] [--size N]` — Paginated inventory
- `keyco dub search --term "<q>"` — Search
- `keyco dub summary` — Aggregate stats
- `keyco dub assigned-to-me` — Assets assigned to caller
- `keyco dub map-data` — Location coordinates
- `keyco dub activity-log --uuid <UUID>` — Event history
- `keyco dub count` — Active DUB count
- `keyco dub performance` — Performance rankings
- `keyco dub location history --dub-id <UUID> [--page] [--size]` — Location history
- `keyco dub sync-device --uuid <UUID>` — Sync device to physical DUB
- `keyco dub claim-virtual` — Claim from virtual pool

## Workflows

- `keyco workflows list` — All workflows
- `keyco workflows get --workflow-id <UUID>` — Single workflow
- `keyco workflows dubs --workflow-id <UUID>` — Assets in workflow
- `keyco workflows assign-dubs --workflow-id <UUID> --dub-ids a,b,c` — Assign DUBs
- `keyco workflows inventory-report --workflow-id <UUID>` — Inventory report

**Note:** Workflow completion and step advancement are intentionally removed. They must happen via verified DUB scan events, not manual CLI commands.

## Lifecycles

- `keyco lifecycles create --event-type T --name N --assigned-user U --assigned-dub D --description DESC --due-date YYYY-MM-DD` — Create event
- `keyco lifecycles get --id <UUID>` or `--event-number LC-00042` — Get event

## Users

- `keyco user get` — Current user profile
- `keyco user list [--with-stats]` — Org users
- `keyco user assigned-dubs --user-id <UUID>` — User's assets
- `keyco user unassigned-dubs` — Assets with no assignee
- `keyco user preferences` — Preferences

## Analytics

- `keyco analytics summary` — Summary metrics
- `keyco analytics weekly-digest` — Weekly digest
- `keyco analytics digest [--start-date] [--end-date]` — Custom range
- `keyco analytics assets` — Asset metrics
- `keyco analytics workflows` — Workflow metrics
- `keyco analytics utilization` — Utilization %
- `keyco analytics stale-assets [--page] [--size]` — Stale/unused assets

## Groups

- `keyco groups list` — All groups
- `keyco groups get --id <UUID>` — Single group
- `keyco groups create --name N` — Create group
- `keyco groups delete --id <UUID>` — Delete
- `keyco groups dubs --id <UUID>` — Assets in group

## Notifications

- `keyco notifications list [--limit N]`
- `keyco notifications unread-count`
- `keyco notifications read --id <UUID>`
- `keyco notifications read-all`
- `keyco notifications clear-read`

## API Keys

- `keyco api-keys list [--include-inactive]`
- `keyco api-keys get --id <UUID>`
- `keyco api-keys create --name N --scopes s1,s2,s3`
- `keyco api-keys revoke --id <UUID>`
- `keyco api-keys scopes` — Available scopes

## Shell Completion

- `keyco completion bash|zsh|fish|powershell`
