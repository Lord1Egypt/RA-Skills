# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/storage/sfs/huawei-cloud-sfs-export-markdown
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_shares_via_sdk` mock plus a live
  regression test that constructs the real `ListSharesRequest` / `SFSTurboRegion`
  when `huaweicloudsdksfsturbo` is installed (skipped otherwise).
- Markdown rendering and file writing run against a temporary directory.

Coverage: write-intent guard (read passes / create / delete / expand / shrink /
resize / mount / unmount / attach / detach / restore / normalized separators /
operation whitelist / read-only value scrubbing incl. `--flag=value`), page size
clamping, command construction (including "no filter/write flags are ever sent
to the server"), JSON extraction, failure classification (missing AK/SK / 403 /
generic / `[USE_ERROR]` with rc=0), client-side name / status filtering, paging
(count / full-page / empty), SDK fallback (success / unavailable / env
credentials), normalization, Markdown rendering (title / header / rows /
empty-result note / pipe & newline escaping), atomic file writing (missing dirs
/ bad path), and all `main()` output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                   # profile check
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=1            # API sanity
python3 scripts/list_sfs_export_markdown.py --region cn-north-4         # full flow
cat sfs_share_list.md                                                   # inspect the table
python3 scripts/list_sfs_export_markdown.py --region cn-north-4 --output /tmp/sfs.md --stdout
python3 scripts/list_sfs_export_markdown.py --status available          # client-side filter
```

## Endpoint provenance

`GET /v1/{project_id}/sfs-turbo/shares/detail` comes from the official
`huaweicloudsdksfsturbo` v1 client `_list_shares_http_info` `resource_path`
metadata (the same path the SDK fallback invokes through
`SFSTurboClient.list_shares`). No endpoint was inferred from naming patterns.

- `ListSharesRequest` real kwargs are `limit / offset` only — there is **no
  `name` / `status`** attribute and **no `project_id`** attribute (project id is
  a path parameter resolved by the client).
- Therefore filtering by name / status is applied client-side after the full
  paged list is fetched; the request itself carries only limit / offset.
- `rc=0 + [USE_ERROR]` output is recognized as an explicit parameter error
  (`hcloud 参数错误 ... --help` hint) instead of a JSON-parse failure.