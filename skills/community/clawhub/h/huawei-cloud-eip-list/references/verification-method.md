# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/eip/huawei-cloud-eip-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_publicips_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ListPublicipsRequest` and `EipRegion` when `huaweicloudsdkeip` is installed
  (skipped otherwise).
- Cases cover: write-intent guard, command construction (filters forwarded
  server-side), JSON extraction, failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
  empty), SDK fallback (success / missing credentials / missing project id /
  unavailable), rendering, and all main() output modes.
- Markdown export cases (`TestRenderMarkdown` / `TestExportMarkdown` /
  `TestMarkdownMain` / `TestGuardTextFromArgv`): full title + metadata +
  twelve-column header, row values from flattened `bandwidth`/`vnic` fields,
  `-` fallback for missing fields, empty-result 「无数据」 with exit 0, default
  `eip_list_<region>_<timestamp>.md` filename, explicit `-o` path, automatic
  parent-directory creation, atomic write (no leftover temp files), overwrite
  of an existing report, unusable path raising `ExportError`, export precedence
  over `--json`/`--names-only`, and the write-intent guard still firing when
  export flags are combined with a mutating operation.

## Live verification (when credentials exist)

```bash
hcloud configure list                                              # profile check
hcloud EIP ListPublicips --cli-region=cn-north-4 --limit=1         # API sanity
python3 scripts/list_eip.py --region cn-north-4                    # full flow
python3 scripts/list_eip.py --json | python3 -m json.tool >/dev/null  # JSON validity
python3 scripts/list_eip.py --names-only
python3 scripts/list_eip.py --status ACTIVE                        # server-side filter
python3 scripts/list_eip.py --id eip-0001
python3 scripts/list_eip.py --public-ip 1.2.3.4

# Markdown export (default filename + explicit path)
python3 scripts/list_eip.py --region cn-north-4 --markdown
python3 scripts/list_eip.py --region cn-north-4 -o /tmp/eip_list.md
cat /tmp/eip_list.md | head -5                                  # title + metadata + header
python3 scripts/list_eip.py --status ACTIVE --markdown -o /tmp/eip_active.md
```

Markdown export checks performed offline (mocked hcloud, no credentials):

- The report starts with `# 华为云 EIP 列表`, carries
  `查询区域 / 生成时间 / 记录数`, and a table with the fixed twelve headers.
- Missing fields render as `-`; nested `bandwidth`/`vnic` data appears in the
  flat columns.
- An empty query still writes the file with the 「无数据」 note and exits 0.
- `-o` creates missing parent directories; writing is atomic (temp file +
  rename) and leaves no `.tmp` residue.
- Export flags override `--json` / `--names-only`; without them, outputs are
  unchanged.

## API / parameter provenance

Verified against the installed official SDK `huaweicloudsdkeip`, no endpoint or
parameter was inferred from naming patterns:

- `huaweicloudsdkeip` v3 `eip_client._list_publicips_http_info` declares
  `method = GET`, `resource_path = /v3/{project_id}/eip/publicips`.
- `ListPublicipsRequest` real query parameters include: `limit`, `marker`,
  `offset`, `id`, `status`, `public_ip_address`, `public_ipv6_address`,
  `type`, `ip_version`, `enterprise_project_id`, `vnic.*`, `bandwidth.*`
  (`id` / `status` / `public_ip_address` are list / csv values; `limit` range
  0–2000).
- Paging is `limit` + `marker`; the next page marker is the response
  `page_info.next_marker`, and `page_info.current_count` reports the page size.
- `PublicipSingleShowResp` fields: `id`, `project_id`, `ip_version`,
  `public_ip_address`, `public_ipv6_address`, `status`, `description`,
  `created_at`, `updated_at`, `type`, `vnic`, `bandwidth`,
  `enterprise_project_id`, `billing_info`, `lock_status`,
  `associate_instance_type`, `associate_instance_id`, `publicip_pool_id`,
  `publicip_pool_name`, `alias`, `public_border_group`.
- Nested `BandwidthResp` (`id`, `size`, `share_type`, `charge_mode`, `name`,
  `billing_info`) and `VnicResp` (`private_ip_address`, `device_id`,
  `device_owner`, `vpc_id`, `port_id`, `instance_id`, `instance_type`) are
  expanded into flat table columns.
- Region catalog `huaweicloudsdkeip.v3.region.eip_region.EipRegion` maps
  `cn-north-4 → https://vpc.cn-north-4.myhuaweicloud.com`.
- IAM action `vpc:publicIps:list` (VPC service, EIP `publicIps` resource) is the
  least-privilege read-only permission for this call.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path could not be executed live; its command/parameter shape is derived
from the official SDK request model and the KooCLI
`hcloud <Service> <Operation> --cli-region=<region>` format standard. The SDK
fallback path was import-verified against the installed `huaweicloudsdkeip`.