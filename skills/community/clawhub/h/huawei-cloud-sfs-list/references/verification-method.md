# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/storage/sfs/huawei-cloud-sfs-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_shares_via_sdk` mock (no real SDK
  import, no network) plus a direct credential-resolution test that stubs the
  SDK modules in `sys.modules`.
- Cases cover: write-intent guard, command construction (limit/offset, no write
  flags), JSON extraction, failure classification, count-aware paging, SDK
  fallback, `ShareInfo` attribute remapping, client-side filtering (incl. AZ),
  rendering, and all `main()` output modes (table / json / names / count-only).

## Live verification (when credentials exist)

```bash
hcloud configure list                                                # profile present
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=1 --offset=0   # raw API sanity
python3 scripts/list_sfs.py --region cn-north-4                      # full flow
python3 scripts/list_sfs.py --json | python3 -m json.tool            # JSON validity
python3 scripts/list_sfs.py --names-only                             # compact list
python3 scripts/list_sfs.py --count-only                              # count only
python3 scripts/list_sfs.py --share-proto NFS --names-only           # client-side filter
python3 scripts/list_sfs.py --az cn-north-4a --names-only            # AZ filter
```

## API truth verified from official sources

- `huaweicloudsdksfsturbo` v1 `SFSTurboClient.list_shares` →
  `GET /v1/{project_id}/sfs-turbo/shares/detail`
  (`_list_shares_http_info`, read from the official SDK source).
- `ListSharesRequest` carries only `limit` / `offset` (no server-side name / ID
  / status filter) — hence client-side filtering.
- `ListSharesResponse` carries `shares` (`list[ShareInfo]`) and `count`.
- `ShareInfo` fields include: `id`, `name`, `status`, `region`,
  `availability_zone` / `az_name`, `share_proto`, `share_type`, `size`,
  `created_at`, `export_location`, `enterprise_project_id`, `vpc_id`,
  `subnet_id`, `security_group_id`, `metadata`.
- KooCLI operation name `ListShares` and service `SFSTurbo` mirror the operation
  in the official SFS Turbo API reference (「获取文件系统列表」); `SFSTurbo` is
  the registered KooCLI service (`SFS` is not a KooCLI service in 7.3.x).

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical/High failures and SKILL.md within
  size limits.
- Error paths (missing AK/SK, hcloud missing, 403) exit non-zero with a clear
  Chinese hint on stderr; empty lists exit 0 with a friendly message.

## Offline note

This environment has neither `hcloud` nor the Huawei Cloud SDKs installed, so
the KooCLI/SDK command surface was verified from the official SDK source and
API reference rather than a live call. Live verification should be run by QA in
a credentialed environment.