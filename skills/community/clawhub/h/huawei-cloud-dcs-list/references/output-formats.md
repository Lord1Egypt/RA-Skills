# Output Formats

`huawei-cloud-dcs-list` supports five output modes. All modes operate on the
same fully paged, filtered and sorted instance list; only the rendering step
differs.

## Modes

| Mode | Flags | Output |
| --- | --- | --- |
| `names` | default, `--names-only`, `--format names` | One instance name per line |
| `table` | `--table`, `--format table` | Human-readable full-field table |
| `json` | `--json`, `--format json` | Raw instance objects as JSON |
| `md` | `--md`, `--format md` | GitHub-flavored Markdown table (10 columns) |
| `csv` | `--csv`, `--format csv` | RFC4180 CSV table (10 columns) |

## Precedence

When several flags are present, the effective mode is resolved in this order:

```text
--json > --names-only > --table > --md > --csv > --format <value> > default names
```

Contradictory combinations are rejected before rendering. In particular,
`--csv` cannot be combined with `--json`, `--table`, `--md`, `--names-only`, or
a non-`csv` `--format`.

## Markdown and CSV contracts

Both modes use the same ten columns, in this order:

```text
名称 / ID / 引擎 / 版本 / 容量 / 规格 / 状态 / 连接地址 / 端口 / 可用区
```

- Missing values render as `-`.
- Markdown escapes pipes and line breaks so a value cannot split a row.
- CSV uses CRLF line endings and standard CSV quoting/escaping.
- `--csv-bom` prepends the UTF-8 BOM for spreadsheet tools.
- Empty result sets print the shared empty hint and write no output file.

## Persisting output

- `--md-output <path>` atomically writes the Markdown table (temp file +
  atomic rename). It is only valid with `md`.
- `--csv-output [<path>]` atomically writes the CSV table. Omitted path or a
  directory uses a timestamped default filename. It is only valid with `csv`.
- `--sort-by name|created` is applied before every output mode, including
  `--json`.

## Examples

```bash
# default names list
python3 scripts/list_dcs.py

# Markdown table to stdout and a file
python3 scripts/list_dcs.py --format md --md-output /tmp/dcs.md

# CSV with BOM and default timestamped filename
python3 scripts/list_dcs.py --csv --csv-bom --csv-output /tmp/dcs

# JSON, sorted by creation time
python3 scripts/list_dcs.py --json --sort-by created
```
