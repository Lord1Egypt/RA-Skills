# Read-only Guard

`huawei-cloud-dcs-list` is intentionally a read-only skill. The guard is a
defense-in-depth check that rejects mutating intent before any `hcloud` call is
executed.

## Allowed operation

Only one DCS API operation is allowed:

| Operation | REST | Mode |
| --- | --- | --- |
| `ListInstances` | `GET /v2/{project_id}/instances` | read-only |

`--operation` only accepts `ListInstances`; any other operation raises a
`GuardError`.

## Three guard layers

1. **Raw argv scan** — all user arguments are normalized (case, spaces,
   `_`/`-` separators) and scanned for mutating keywords such as `create`,
   `delete`, `update`, `resize`, `restart`, `flush`, `release`.
2. **Operation whitelist** — `guard_operation()` rejects every operation other
   than `ListInstances`.
3. **Filter values** — `--name`, `--instance-id`, `--ip`, `--status` and
   `--tags` values are scanned too, so a value that looks like a mutating
   operation is rejected before it can be forwarded to the server.

## Exemptions

Local-only values are not DCS operations and are exempt from the raw argv scan:

- `--md-output <path>` / `--md-output=<path>`
- `--csv-output [<path>]` / `--csv-output=<path>`
- `--sort-by name|created` / `--sort-by=<value>`

Repository file paths and sort choices therefore do not trip the write-intent
guard.

## Error behavior

A blocked request raises `GuardError`, is printed to `stderr` with the matched
keyword, and exits with status `1`. No `hcloud` subprocess is started. The guard
does not attempt to translate a mutating request into a read-only one.

## Examples

```bash
# allowed
python3 scripts/list_dcs.py --region cn-north-4 --status RUNNING
python3 scripts/list_dcs.py --name cache --format md --md-output /tmp/dcs.md

# rejected before execution
python3 scripts/list_dcs.py --operation DeleteInstance
python3 scripts/list_dcs.py --name create-instance
```
