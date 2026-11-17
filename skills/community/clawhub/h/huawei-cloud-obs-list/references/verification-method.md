# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/storage/obs/huawei-cloud-obs-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_buckets_via_sdk` mock (no real SDK
  import, no network) plus a direct credential-resolution test.
- Cases cover: write-intent guard, command construction (endpoint/limit, no
  write flags), obsutil output parsing (names / columns / dedupe / empty),
  failure classification (missing AK/SK / InvalidAccessKeyId / 403 / generic /
  `[USE_ERROR]` with rc=0), SDK fallback (missing env credentials / success /
  unavailable / normalization), rendering, and all `main()` output modes.

## Live verification (when obsutil credentials exist)

```bash
hcloud version                                                       # CLI present
hcloud OBS ls -limit=1                                               # obsutil credentials sanity
python3 scripts/list_obs_buckets.py --region cn-north-4              # full flow
python3 scripts/list_obs_buckets.py --json | python3 -m json.tool    # JSON validity
python3 scripts/list_obs_buckets.py --names-only                     # compact list
```

## CLI truth verified locally (KooCLI 7.3.12)

- `hcloud OBS` is **obsutil-backed**: `hcloud OBS` prints the obsutil command
  list (lowercase commands such as `ls`, `cp`, `rm`, ...).
- There is **no** `hcloud OBS ListBuckets` command — `hcloud OBS ListBuckets`
  fails with `Error: No such command: "ListBuckets"`.
- Listing the account's buckets is `hcloud OBS ls` (no `cloud_url`).
  Without credentials it prints
  `Warn: Please set ak, sk and endpoint in the configuration file!` (exit 3) —
  the exact string the script maps to `ConfigError` (missing AK/SK).
- The OBS module does **not** accept `--cli-region`; the region is expressed via
  `-e=obs.<region>.myhuaweicloud.com` (the script derives it from `--region`).

## SDK fallback provenance

`huaweicloudsdkobs` v1 `ObsClient.list_buckets(ListBucketsRequest())` returns a
response whose `buckets.bucket` list carries `name` / `creation_date` /
`location`. The script normalizes those into the same record shape used by the
CLI parser (`name`, `creation_date`, `location`, `storage_class`). This matches
the OBS ListBuckets SDK surface used elsewhere in this repository — no endpoint
was inferred from naming patterns.

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical failures and SKILL.md within size
  limits.
- Error paths (missing AK/SK, hcloud missing, 403) exit non-zero with a clear
  Chinese hint on stderr; empty lists exit 0 with a friendly message.