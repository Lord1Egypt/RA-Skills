# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/storage/obs/huawei-cloud-obs-list-excel
python3 -m unittest discover -s tests -v
bash scripts/validate-skill.sh .
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is exercised via a `list_buckets_via_sdk` mock (no real SDK
  import, no network) plus a direct credential-resolution test.
- The xlsx export is verified against a **real openpyxl install**: the test
  loads the produced workbook with `openpyxl.load_workbook` and asserts the
  sheet title, header row, data rows, summary row and cell fallbacks. The
  missing-openpyxl branch is covered by mocking the `_require_openpyxl` import
  path.
- Cases cover: write-intent guard (including `--output` path value exclusion),
  command construction (endpoint/limit, no write flags), obsutil output parsing
  (names / columns / storage class / policy / dedupe / empty), failure
  classification (missing AK/SK / InvalidAccessKeyId / 403 / generic /
  `[USE_ERROR]` with rc=0), SDK fallback (missing env credentials / success /
  unavailable / normalization), xlsx export (header / rows / summary / fallback
  cells / openpyxl missing / bad path), rendering, and all `main()` output modes
  (xlsx writes file + prints path; table / json / empty / error paths).

## Live verification (when obsutil credentials exist)

```bash
python3 scripts/ensure_env.py                       # openpyxl + SDK ready
hcloud version                                      # CLI present
hcloud OBS ls -limit=1                              # obsutil credentials sanity
python3 scripts/list_obs_buckets_excel.py --format table              # full flow
python3 scripts/list_obs_buckets_excel.py --format json | python3 -m json.tool
python3 scripts/list_obs_buckets_excel.py --output /tmp/obs.xlsx --summary
python3 -c "from openpyxl import load_workbook; wb=load_workbook('/tmp/obs.xlsx'); print(wb.sheetnames)"
```

## CLI truth verified locally (KooCLI-style)

- `hcloud OBS` is **obsutil-backed**: listing the account's buckets is
  `hcloud OBS ls` (no `cloud_url`), and there is **no** PascalCase
  `hcloud OBS ListBuckets` command.
- The OBS module does **not** accept `--cli-region`; the region is expressed via
  `-e=obs.<region>.myhuaweicloud.com` (the script derives it from `--region`).
- Without credentials it prints
  `Warn: Please set ak, sk and endpoint in the configuration file!` (exit 3) —
  the exact string the script maps to `ConfigError` (missing AK/SK).

## SDK fallback provenance

`huaweicloudsdkobs` v1 `ObsClient.list_buckets(ListBucketsRequest())` returns a
response whose `buckets.bucket` list carries `name` / `creation_date` /
`location` (with `storage_class` / `policy` when present). The script normalizes
those into the same record shape used by the CLI parser (`name`, `creation_date`,
`location`, `storage_class`, `policy`).

## Excel correctness

- Sheet title fixed to `OBS 桶列表`; header row fixed to
  `桶名称 / 创建时间 / 区域 / 存储类别 / 桶策略`.
- Every bucket becomes exactly one data row; missing fields render as `-`.
- `--summary` appends a bolded `桶数量 | <N> | Region <region>` footer row.
- The workbook is saved through a temp file + atomic rename, then re-loaded with
  `openpyxl.load_workbook` in tests to confirm structural validity.

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical failures and SKILL.md within size
  limits.
- Error paths (missing AK/SK, hcloud missing, 403, openpyxl missing) exit
  non-zero with a clear Chinese hint on stderr; empty lists exit 0 with a
  friendly message and no .xlsx file.