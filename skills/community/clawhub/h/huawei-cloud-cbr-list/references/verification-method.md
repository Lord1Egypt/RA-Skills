# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/storage/cbr/huawei-cloud-cbr-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_backups_via_sdk` mock (no real SDK
  import, no network) plus a direct credential-resolution test that stubs the
  SDK modules in `sys.modules`.
- Cases cover: write-intent guard, command construction (limit/offset + native
  filters, no write flags), JSON extraction, failure classification,
  count-aware paging, SDK fallback, `BackupResp` attribute remapping,
  client-side filtering, rendering, and all `main()` output modes.

## Live verification (when credentials exist)

The skill's entry point is the script; each command below exercises the KooCLI
path (or the SDK fallback) end-to-end:

```bash
python3 scripts/list_cbr_backups.py --region cn-north-4
python3 scripts/list_cbr_backups.py --json
python3 scripts/list_cbr_backups.py --names-only
python3 scripts/list_cbr_backups.py --status available --names-only
python3 scripts/list_cbr_backups.py --resource_type OS::Nova::Server --names-only
python3 scripts/list_cbr_backups.py --vault_id 8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d --json
```

To check JSON validity, pipe the `--json` output to `python3 -m json.tool`
manually. The script prints to stdout only; it never writes a file.

For reference, the raw KooCLI invocations the script wraps internally
(illustrative — require KooCLI installed):

```text
hcloud configure list
hcloud CBR ListBackups --cli-region=cn-north-4 --limit=1 --offset=0
```

## API truth verified from official sources

- `huaweicloudsdkcbr` v1 `CbrClient.list_backups` →
  `GET /v3/{project_id}/backups` (`_list_backups_http_info`, read from the
  official SDK source).
- `ListBackupsRequest` carries the native query parameters: `checkpoint_id`,
  `dec`, `end_time`, `image_type`, `limit`, `marker`, `name`, `offset`,
  `resource_az`, `resource_id`, `resource_name`, `resource_type`, `sort`,
  `start_time`, `status`, `vault_id`, `enterprise_project_id`, `own_type`,
  `member_status`, `parent_id`, `used_percent`, `show_replication`,
  `incremental`.
- `ListBackupsResponse` carries `backups` (`list[BackupResp]`), `count`,
  `offset` and `limit`.
- `BackupResp` fields include: `id`, `name`, `status`, `resource_id`,
  `resource_name`, `resource_type`, `resource_size`, `resource_az`, `vault_id`,
  `image_type`, `incremental`, `created_at`, `expired_at`, `updated_at`,
  `protected_at`, `checkpoint_id`, `parent_id`, `enterprise_project_id`,
  `provider_id`, `version`.
- KooCLI operation name `ListBackups` and service `CBR` mirror the operation in
  the official CBR API reference (「查询所有备份」).

## Pass criteria

- All offline unit tests pass.
- `validate-skill.sh` reports zero Critical/High failures and SKILL.md within
  size limits.
- Error paths (missing AK/SK, hcloud missing, 403) exit non-zero with a clear
  Chinese hint on stderr; empty lists exit 0 with a friendly message.

## Offline note

This environment has neither `hcloud` nor the Huawei Cloud CBR SDK installed,
so the KooCLI/SDK command surface was verified from the official SDK source and
API reference rather than a live call. Live verification should be run by QA in
a credentialed environment.