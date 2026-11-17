# Environment Variables (`iga pages env`)

All `env` commands require the directory to be linked to a Pages project (`iga pages link` writes `.iga/project.json`). If not linked, the CLI tells the user to run `iga pages link` first.

Changes to `add`/`update`/`remove` edit **remote project config**, not local files, and only take effect on the **next deployment** — the CLI says so after each write.

```bash
iga pages env list                 # or: env ls — shows KEY names only, never values
iga pages env list --format=json   # as JSON
iga pages env add <NAME>           # prompts for value (hidden input)
iga pages env add <NAME> --value <v> --yes   # non-interactive / CI
iga pages env update <NAME>        # change an existing variable's value
iga pages env update <NAME> --value <v> --yes
iga pages env remove <NAME>        # or: env rm — asks for confirmation
iga pages env remove <NAME> --yes  # skip confirmation (required when no TTY)
iga pages env pull                 # write all project env to local .env.local
```

Notes:

- `list` / `pull` merge plain project env with integration-managed vars (e.g. Supabase). `list` shows keys only — values are never printed.
- Integration-managed vars are read-only; manage them via `integration link`/`unlink`.
- `pull` writes project env vars, including integration-managed vars, to local `.env.local` for local development. Treat the file as sensitive and do not commit it; deployment does not require `env pull`.
