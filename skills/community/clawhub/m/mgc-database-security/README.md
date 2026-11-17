# Database Credential Security (Zero-Exposure Edition)

Secure database credential management, analysis-script execution and multi-step data analysis workflows using MGC Blackbox 1.5.4. Supports MySQL, PostgreSQL, SQLite, MariaDB, SQL Server and more.

## Three Capability Layers

| Layer | What it does | Core tools |
|---|---|---|
| **L1 — Credentials** | Store, rotate, revoke and delete database secrets; scripts read them at runtime over the localhost REST API | `mgc_save`, `mgc_delete`, `mgc_find` |
| **L2 — Analysis scripts** | Run one parameterised script that queries the database and writes a result file | `mgc_save`, `mgc_run` |
| **L3 — Data analysis workflows** | Run a multi-script pipeline (extract → clean → analyse) with auto-recognised cross-script call graphs | `mgc_save_file`, `mgc_run`, `mgc_seal_package` |

**AI agents never hold credential plaintext.** The AI supplies SQL, parameters and addresses; the script resolves the secret inside the MGC execution boundary and writes only the result.

## What's New in v2.0.0

Upgraded from credential-only management to the three-layer model above, based on the MGC 1.5.4 skill specification.

- **Analysis script layer** — the analysis script contract: credential indirection, literal `argparse` defaults, result-file read-back via `RESULT_FILE:<path>`, and `ext02` runtime override.
- **Data analysis workflow layer** — folder mode, the `ext08` call graph, query → clean → analyse orchestration, and the recognised vs unrecognised call-form matrix.
- **Cross-folder subprocess rules** — a literal filename must be **unique** across stored folders; zero or multiple matches fall back to an ordinary subprocess. Re-save the caller after storing the callee so the dependency graph is rebuilt.
- **Run-compatibility badge** — `ext10` reports `supported` / `unsupported`. A fatal path check (`if not Path(...).exists(): sys.exit(1)`) is the only pattern that overrides an otherwise runnable call form.
- **Receiver version floor** — a package carrying `ext08` needs MGC **1.5.2+** on the receiving node, otherwise the exporter reports `TARGET_NODE_MAY_NOT_SUPPORT_AUTO_WORKFLOW`.
- **Security Boundary chapter** — what this skill provides and what it explicitly does not provide.
- **Hands-on link authorization verification** — tamper with `ext09` by one space and the capsule fails with `UNSEAL_FAILED`.
- **Fixed a factual error** — folder import stores `diff_3` as the relative POSIX path **including the file extension** (`step1_extract.py`), not the bare file stem.
- **Fixed a factual error** — a plain script run returns the result payload including `pid`; a sealed script run returns only `{"status": "started"}`.
- **`mgc_run` forces the script type** — the server injects `info_type="script"` and `action="run"`; a client-supplied `info_type` is ignored.

## What This Skill Does

- Encrypted credential storage pattern in MGC, with a full rotate / revoke / delete lifecycle
- Parameterised analysis scripts with a result-file channel that carries data but not secrets
- Multi-step data analysis workflows stored as folders, with cross-script calls routed at runtime
- Cross-node script and workflow sealing with the 1.5.4 dual-mode model
- Runtime advisories for missing dependencies, incompatible platforms and out-of-package calls
- Anti-patterns and security guidance

Documentation-only — contains **no executable code**, safe for automatic approval.

## Prerequisites

- Python 3.10+ (macOS 14+ Apple Silicon, Windows, or Linux)
- `pip install mgc-blackbox>=1.5.4`
- MGC service running (`mgc`) — REST API at `http://127.0.0.1:57219`, WebUI at `http://127.0.0.1:57218`
- Database driver installed (`mysql-connector-python`, `psycopg2-binary`, `pymysql`, …). MGC reports missing dependencies; it never installs them.

## Quick Start

### 1. Install and start MGC

```bash
pip install mgc-blackbox>=1.5.4
mgc
```

### 2. Store the credential (L1)

WebUI → Add Entry, with `info_type="config"`, `info_owner="my_mysql_prod"`, and content as JSON with `host` / `port` / `database` / `user` / `password`.

Or AI can store it on explicit user instruction via `mgc_save`.

### 3. Reference it from the script

The script references the credential by `info_owner` only. It never embeds the password.

### 4. Read it inside the script

```python
resp = requests.post(
    "http://127.0.0.1:57219/api/mgc/sensitive/get",
    json={"info_type": "config", "info_owner": "my_mysql_prod"},
    headers={"X-MGC-Token": token, "Content-Type": "application/json"},
    timeout=10,
)
resp.raise_for_status()
creds = json.loads(resp.json()["data"])   # `data` IS the plaintext string
```

### 5. Run the analysis script (L2)

```text
Tool: mgc_run
Parameters:
  info_owner:  "mysql_query_v1"
  diff_3:      "mysql_query_v1"
  ext02:       "[\"--sql\", \"SELECT 1\"]"
```

The AI reads the result file the script writes. The password never enters AI context.

### 6. Run a pipeline (L3)

```text
# Store the folder
Tool: mgc_save_file
Parameters:
  path:        "/abs/path/db_pipeline"
  info_owner:  "db_pipeline_team"

# Run the entry script — diff_3 carries the file extension
Tool: mgc_run
Parameters:
  info_owner:  "db_pipeline_team"
  diff_2:      "db_pipeline"
  diff_3:      "step1_extract.py"
```

The three steps run as one workflow. Cross-script calls are routed through sealed execution — no source files on disk, no rewrites.

## MCP Tools

| Tool | Purpose |
|---|---|
| `mgc_save` | Store credentials and scripts |
| `mgc_save_file` | Store a workflow folder; import a sealed capsule (preferred) |
| `mgc_run` | Blackbox script execution — required: `info_owner` |
| `mgc_list` | Enumerate entries (metadata only) |
| `mgc_find` | Fuzzy search by `info_owner` / diff fields — no `info_type` filter |
| `mgc_delete` | Delete a credential or script — required: `info_type`, `info_owner`. Folder-level delete needs `confirm_folder_delete="true"` (a string) |
| `mgc_seal` | Seal a script for another node — required: `info_owner`, `output_dir` |
| `mgc_seal_package` | Seal a workflow folder — required: `info_owner`, `diff_2`, `output_dir` |
| `mgc_package` | Export a folder as a plaintext archive |
| `mgc_open_webui` | Open the WebUI for the user to store credentials |
| `mgc_get` | **Restricted** — never for credentials; only the `__NODE_PUB__` lookup |
| `mgc_skill` | Load the upstream MGC skill document |

## Locating a Script

| Field | Single script (`mgc_save`) | Folder import (`mgc_save_file`) |
|---|---|---|
| `diff_1` | Business description, defaults to the file stem | Usually empty |
| `diff_2` | Usually empty | The folder name — required in practice for folder scripts |
| `diff_3` | The file stem | The relative POSIX path **including the extension**, e.g. `step1_extract.py` |

`diff_3` is the most reliable locator — it identifies one record on its own.

## Recognised Cross-Script Call Forms

| Pattern | Runs in MGC |
|---|---|
| `from` import / `from` import with alias | Yes |
| Plain `import` | Yes |
| Relative path via `Path(__file__).parent` | Yes |
| Subprocess with a relative path | Yes |
| Subprocess with a literal filename | Yes, if the filename is unique across stored folders |
| Dynamic import (`importlib.import_module`) | No — only string literals are recognised |
| Absolute path via `open()` | No — use MGC location addressing |
| Fatal path check (`sys.exit` on a missing path) | No — the script exits before interception |

## Sealing Modes

| Mode | How to produce it | Who can unseal |
|---|---|---|
| **p2p mode** | `mgc_seal(..., ext04=<target PEM>)` | Only the node holding the matching private key |
| **free mode** | `mgc_seal(...)` — omit `ext04` | Any MGC 1.5.4+ node |
| **chain mode** | Reserved for future multi-hop chains | Not available yet |

Omitting `ext04` does not raise an error — it silently produces a free-mode artifact. Verify `ext09` reads `p2p mode` when node binding was intended. Alias typos such as `node_pub` fail loudly with `UNKNOWN_PARAM`.

## Anti-Patterns

| Wrong | Right |
|---|---|
| `mgc_get(info_type="config", ...)` to fetch a credential | The script reads it over the REST API inside the MGC boundary |
| Password hardcoded in the script | Resolved from MGC at runtime |
| Password passed through `ext02` | Password lives in the `info_type="config"` entry |
| Password printed or logged | Log host, query and row count only |
| Credential written to a plain file | Stored in MGC only |
| Credential sealed into a capsule | Seal scripts; each node stores its own credential |
| `mgc_seal` without `output_dir` | Always pass an absolute `output_dir` |
| `diff_3="step1_extract"` for a folder script | `diff_3="step1_extract.py"` — the extension is part of the path |
| A computed `argparse` default | Literal default, or supply `ext02` at run time |
| Running a folder script without `diff_2` | Pass both `diff_2` and the extension-bearing `diff_3` |
| Expecting a `pid` from a sealed run | A sealed run returns `{"status": "started"}` only |

## Troubleshooting

| Symptom | Fix |
|---|---|
| Credential not found | Verify `info_owner` exactly; `mgc_find` with `match_mode="substring"` |
| "Entry exists" | Pass `update_if_exists=true` |
| `AMBIGUOUS_SCRIPT` | `mgc_find` first, then re-run with the exact `diff_3` |
| "Missing required param: output_dir" | Pass an absolute directory — mandatory since 1.5.4 |
| `UNKNOWN_PARAM: node_pub` | Rename to `ext04` |
| "Invalid PEM format" | `ext04` must be a real multi-line PEM with actual newlines |
| `UNSEAL_FAILED` | `ext07` or `ext09` was altered in transit — re-seal and forward untouched |
| `DEP_MISSING` | Install using the PyPI name: `pymysql` → `PyMySQL`, `yaml` → `PyYAML`, `mysql` → `mysql-connector-python` |
| `PLATFORM_INCOMPAT` | `ext06` excludes this OS — re-save on a supported platform |
| `DIFF2_MISMATCH` | The cross-script target is outside the caller's package |
| `dynamic_args_detected` | Use a literal argparse default, or supply `ext02` at run time |
| Folder script not found by `diff_3` | The extension is part of the stored path — use `mgc_find` to list the stored values |
| Cross-script call runs as an ordinary subprocess | The callee filename is ambiguous, or the caller was stored before the callee — re-save the caller |
| Badge shows `unsupported` | The script has a fatal path check — remove or soften the `Path(...).exists()` pre-check |
| Workflow does not route on the receiver | The receiver runs MGC below 1.5.2 — upgrade it |

## When to Use This Skill

- Production environments with sensitive data
- Automation tasks requiring database access
- Multi-node collaboration via `mgc_seal`
- AI needs database access but must not see passwords
- Multi-step analysis pipelines where scripts call each other

## When NOT to Use This Skill

- Public databases with no authentication
- Local development with mock data
- Interactive manual database access (DBeaver / MySQL Workbench)

## Security

- Credentials never exposed to AI
- Encrypted storage via MGC
- Local scripts retrieve credentials over the localhost REST API inside the blackbox
- No plaintext in logs
- Separate credentials per environment
- Revoked credentials removed with `mgc_delete`
- `ext07` and `ext09` forwarded verbatim when a capsule is shared
- Result files carry data only — never the credential

> **Never auto-confirm.** `mgc_delete` returns a candidate list when more than one record matches. Present it to the user, ask "Delete all N records?", and only after the user approves re-invoke with `confirm_folder_delete="true"`. The AI must never set that flag on its own.

> **Scope of the guarantee.** MGC protects content confidentiality. After unsealing, a script runs with the permissions of the user running it — which commands it invokes, which files it reads or writes and which network endpoints it reaches are outside MGC's control. Import only capsules you produced or received from a party you trust.

> **This skill does not provide** automated data access, automated cleaning or analysis, automated transport, or script generation and modification. All scripts must be user-provided and comply with organizational policy.

## License

MIT
