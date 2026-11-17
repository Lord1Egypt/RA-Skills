# Integrations (`iga pages integration`)

Connect an existing external resource (currently **Volcengine Supabase** only) to the Pages project so its connection variables are synced as project env. The CLI does **not** create, delete, or modify anything inside Supabase — it only manages the IGA-side binding.

All `integration` commands require the directory to be linked to a Pages project (`iga pages link` writes `.iga/project.json`). Changes take effect on the **next deployment**.

```bash
iga pages integration list         # bindings on the current Pages project
iga pages integration list --format=json    # as JSON

iga pages integration link supabase             # interactive
iga pages integration link supabase --format=json   # as JSON; returns next missing flag until all provided
iga pages integration unlink                     # interactive: pick a binding to remove
iga pages integration unlink --format=json --yes # as JSON (requires --yes)
```

Non-interactive link (all selection flags required when there's no TTY):

```bash
iga pages integration link supabase \
  --product volc_supabase \
  --region cn-beijing \
  --resource <workspace-name-or-id> \
  --branch <branch-name-or-id> \
  --yes
# --prefix and --framework-prefix are both optional:
#   --framework-prefix is auto-detected from the framework; pass it only to override.
#   --prefix is optional for the first Supabase binding; required from the second binding onward.
```

Non-interactive unlink:

```bash
iga pages integration unlink supabase --product volc_supabase \
  --resource <workspace-name-or-id> --branch <branch-name-or-id> --yes
```

Key behaviors:

- **Only `supabase` / `volc_supabase`** are supported this release. `--product comm_supabase` (Supabase Community) is rejected — tell the user it's not supported yet.
- **Cross-service authorization**: before linking, the CLI checks a role; if not authorized it opens the Volcengine IAM authorization page and waits for the user to confirm. In non-TTY it errors with the auth URL. Linking can't proceed until authorized.
- **`--resource` / `--branch`** match either the display name (`WorkspaceName` / `Branch`) or the stable ID (`WorkspaceID` / `BranchID`). Ambiguous matches in non-TTY error out — pass a unique ID.
- **`--framework-prefix`** (optional) is the client-exposed env prefix (`NEXT_PUBLIC`, `VITE`, `PUBLIC`, `REACT_APP`). The CLI auto-detects the framework and uses it as the default; in TTY it prompts for confirmation, in non-TTY it uses the detected value silently. Pass `--framework-prefix` only to override the detected default.
- **`--prefix`** (custom prefix) is **optional for the first** Supabase binding but **required from the second onward**, to avoid env name collisions. Uniqueness is enforced by the backend; on a conflict the CLI surfaces the error and re-prompts.
- **Resulting var names**: client vars are `<framework-prefix>_<custom-prefix?>_SUPABASE_<KEY>`; server-only vars omit the framework prefix. The service-role key is **not** auto-synced.
- The synced vars are injected into the deployment runtime automatically — you do **not** need to run `env pull` for the deploy itself. Run `iga pages env pull` separately only when you want those vars in your local `.env.local` for local development.
- **`unlink`** removes the IGA binding and the env vars that binding created (backend-driven, by binding relationship — the CLI never deletes env by name). It does not touch anything in Supabase. Confirmation required in TTY; non-TTY needs `--yes` plus full locating flags. `--format=json` requires `--yes`.

## Deploy orchestration

The IGA Pages skill is the **orchestrator** for the deploy flow. Recommended order when a user wants to deploy a project that may use an integration:

1. Ensure logged in with `iga whoami`; only run `iga login` if `whoami` fails.
2. If the directory is not linked yet, run `iga pages link` to create/associate the Pages project (this no longer deploys). If it is already linked, continue without relinking.
3. Inspect the project for supported integrations. If Supabase usage is detected, run `iga pages integration list` first. If the required Supabase binding already exists, continue to deploy without asking again. If no matching binding exists, ask before deploying:
   > "This project appears to use Supabase, which IGA Pages can connect as an integration. Would you like to connect it before deploy?"
4. If yes (Supabase): run `iga pages integration link supabase`. The synced env vars take effect on the next deploy automatically.
5. `iga pages deploy`.

`iga pages env pull` is **not** part of this flow — it only writes vars to local `.env.local` for local development, and is unrelated to whether the deploy picks them up. Recommend it separately if the user wants to develop locally with the synced values.

## Supabase provider work → hand off to `byted-supabase`

This skill only orchestrates link / integration / env / deploy. It does **not** manage Supabase resources (creating workspaces/branches, SQL, migrations, API keys, Storage, Edge Functions). When the user wants to create or manage actual Supabase resources, hand off to the `byted-supabase` skill (`https://github.com/bytedance/agentkit-samples/blob/main/skills/byted-supabase/SKILL.md`). After it finishes, return and confirm with the user before continuing link / integration / deploy — don't auto-continue.
