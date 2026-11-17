# olvm-aiops — CLI reference

Every engine command takes `--target/-t <name>` (default: the first target in `config.yaml`);
`init`, `doctor`, `secret` and `mcp` do not. Lists and diagnoses take `--json` for the full
payload. Each engine command calls the MCP tool of the same name, so it is audited like an MCP
call. Errors print one line and exit 1; an invalid option value exits 2, as does `undo apply`
when an outcome is undetermined.

## Setup & health

```bash
olvm-aiops init                      # wizard: URL, username with profile, CA file, TLS, password
olvm-aiops doctor                    # config, encrypted store, login, engine product version
olvm-aiops doctor --skip-auth        # offline checks only
olvm-aiops mcp                       # run the MCP server over stdio
```

## Diagnosis

```bash
olvm-aiops engine health [--events-window-hours 24] [--events-limit 200] [--json]
olvm-aiops host health [--events-window-hours 24] [--events-limit 200] [--json]
olvm-aiops storage capacity [--events-window-hours 24] [--events-limit 200] [--json]
olvm-aiops vm health [--events-window-hours 24] [--events-limit 200] [--json]
```

## Inventory

```bash
olvm-aiops datacenter list [--limit 100] [--json]
olvm-aiops cluster list [--limit 100] [--json]
olvm-aiops host list [--search 'status!=up'] [--limit 100] [--json]
olvm-aiops host get <host-id>
olvm-aiops storage list [--limit 100] [--json]
olvm-aiops storage get <domain-id>
olvm-aiops vm list [--search 'status=up'] [--limit 100] [--page 1] [--json]
olvm-aiops vm capacity [--page-size 100] [--max-pages 100] [--json]
olvm-aiops vm get <vm-id>
olvm-aiops vm stats <vm-id>
```

`--search` accepts engine criteria (`status=up`, `cluster=Default`, `name=web*`)
and an optional `sortby` clause. Use `--page` for VM pagination instead of
putting `page N` inside `--search`. Keep the same limit and search for each
page, and follow the JSON `nextPage` until null. The engine has no atomic total
count and may change between pages.
For agent-facing VM lists, use `--limit 20`. `vm capacity` aggregates inside the
server and reports `complete: false` with an `incompleteReason` when a full
count or ratio cannot be supported. It does not produce an atomic snapshot.

## Activity

```bash
olvm-aiops event list [--min-severity warning] [--limit 100] [--json]
olvm-aiops event list --page 2                    # older events
olvm-aiops event list --after-index 1234          # events after index 1234, oldest first (not with --page)
olvm-aiops event list --since-minutes 60          # last hour (client-side on event time)
olvm-aiops job list [--status failed] [--limit 100] [--json]
```

## Undo log

```bash
olvm-aiops undo list
olvm-aiops undo apply <undo-id>      # nothing to undo in this read-only release
```

## Secrets (encrypted store)

```bash
olvm-aiops secret set <target>       # hidden prompt for the engine account password
olvm-aiops secret list               # names only
olvm-aiops secret rm <target>
olvm-aiops secret rotate-password    # re-encrypt under a new master password
olvm-aiops secret migrate            # import a legacy plaintext .env
```

## Environment variables

| Variable | Purpose |
|---|---|
| `OLVM_AIOPS_MASTER_PASSWORD` | Unlocks `secrets.enc` without a prompt (MCP, CI, cron) |
| `OLVM_AIOPS_HOME` | Relocates config, secrets, audit and undo databases (default `~/.olvm-aiops`) |
| `OLVM_AIOPS_CONFIG` | Path to a config file for the MCP server |
| `OLVM_<TARGET>_PASSWORD` | Legacy plaintext password fallback (warns; migrate it) |
| `OLVM_MAX_TOOL_CALLS` / `OLVM_MAX_TOOL_SECONDS` | Budget ceilings |
| `OLVM_RUNAWAY_MAX` / `OLVM_RUNAWAY_WINDOW_SEC` | Tight-loop breaker (`OLVM_RUNAWAY_MAX=0` disables) |
| `OLVM_AUDIT_APPROVED_BY` / `OLVM_AUDIT_RATIONALE` | Optional who/why annotations on audit rows |

## Truncation

Tables print a yellow line when more rows exist than `--limit` showed; diagnoses print
`PARTIAL` when their host, VM, storage-domain or event scan was cut short. In `--json`, read
`truncated`, `scanTruncated`, `hostsTruncated`, `vmsTruncated`, `domainsTruncated` and
`eventsTruncated` (true only when the event window itself was cut).
