# Verification Method

## Live API verification (2026-11-12, region cn-north-4, KooCLI 7.3.12)

All CLI calls below were executed through the mandated wrapper
`skill-quality-cli run --skill-name huawei-cloud-eip-bandwidth-list -- hcloud ...`
(read-only, no resources created).

### Operation names and parameters (`--help`)

`hcloud EIP ListBandwidths --help` — `Method: GET`, params:

| Param | Required | Type | Location |
| ----- | -------- | ---- | -------- |
| `--cli-region` | yes | string | — |
| `--project_id` | yes | string | path |
| `--enterprise_project_id` | no | string | query |
| `--limit` | no | integer | query (`0..intmax`) |
| `--marker` | no | string | query |
| `--share_type` | no | string | query (`WHOLE` / `PER`) |

`hcloud EIP ShowBandwidth --help` — `Method: GET`, params:

| Param | Required | Type | Location |
| ----- | -------- | ---- | -------- |
| `--cli-region` | yes | string | — |
| `--bandwidth_id` | yes | string | path |
| `--project_id` | yes | string | path |

No parameter was inferred from naming patterns; every name above appears in
the real KooCLI parameter list.

### ListBandwidths live result

- `--limit=10` returned 10 records; a second call with
  `--marker=<last-id>` returned 6 records; total 16 (account inventory).
- The real response body contains only `{"bandwidths": [...]}` — **no
  `page_info`**. Paging is therefore count-based: when a page is full
  (`len(batch) == limit`), the next request uses the last record `id` as
  `marker`; an empty or partial page ends the loop. A `page_info.next_marker`,
  if a future API version returns one, is used first.
- `--share_type=WHOLE` returned 0 records (the server-side filter is effective;
  the account currently has no shared bandwidth). This is the verified
  zero-result branch.
- Observed record keys: `id` / `name` / `size` / `share_type` /
  `publicip_info[].publicip_id|publicip_address|ip_version|publicip_type` /
  `tenant_id` / `bandwidth_type` / `charge_mode` / `billing_info` /
  `enterprise_project_id` / `status` / `created_at` / `updated_at` /
  `enable_bandwidth_rules` / `rule_quota` / `bandwidth_rules` /
  `public_border_group`.
- All 16 records were `share_type=PER` at verification time; the `WHOLE` path
  is covered by the empty-filter branch and offline unit tests.

### ShowBandwidth live result

- `--bandwidth_id=<id from the list>` returned
  `{"bandwidth": { ...same record shape... }}` with one `publicip_info` entry
  and `bandwidth_rules: []`, `rule_quota: 0`.

### Script live runs (same wrapper, `EIP_BANDWIDTH_HCLOUD_BIN`)

```bash
python3 scripts/list_bandwidths.py --region cn-north-4 --limit 10   # 16 rows, table
python3 scripts/list_bandwidths.py --json --limit 10               # JSON array, 16 rows
python3 scripts/list_bandwidths.py --share-type WHOLE --format md -o /tmp/bw-whole.md
python3 scripts/list_bandwidths.py --share-type PER   --format md -o /tmp/bw-per.md
python3 scripts/list_bandwidths.py --bandwidth-id <id>             # detail + public IP table
```

Results: list table rendered the nine required columns; `--json` parsed back
(16 objects); `--format md` wrote a report with the fixed header
`| 带宽名称 | 带宽 ID | 大小(Mbit/s) | 共享类型 | 计费方式 | 关联公网 IP 数 | 状态 |
企业项目 ID | 创建时间 |`; the `WHOLE` empty report contained the header plus
`无数据`; the detail view listed `publicip_address` / `publicip_type` /
`ip_version` and `rule_quota` / `bandwidth_rules`.

### ShowBandwidth non-existent ID (exit-code-0 error body)

```bash
python3 scripts/list_bandwidths.py --bandwidth-id 00000000-0000-4000-8000-000000000000
```

KooCLI printed `{"code": "VPC.0305", "message": "{\"NeutronError\":{...No Eip
bandwidth exist...}}"}` on stdout **with exit code 0**. The script now parses
the body and exits 1 with: `带宽不存在或已删除（接口返回 VPC.0305）：请先不带
--bandwidth-id 运行 ListBandwidths 核对当前 Region 的带宽 ID，再用正确的
--bandwidth-id 重试。` Previously it fell through to a generic
「响应为空」 hint. Documentation IDs are illustrative; always take real IDs from
the list output of the target account/region.

## Offline unit tests (primary, CI-safe)

```bash
cd skills/network/eip/huawei-cloud-eip-bandwidth-list
python3 scripts/run_tests.py
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no
  credentials, no network, deterministic.
- 78 tests cover: write-intent guard (read passes; create / delete / update /
  change / bind / unbind / release / normalized variants; operation
  allowlist), command construction (filters + marker), JSON extraction,
  failure classification (missing AK/SK / 403 list vs detail / 404 detail /
  `[USE_ERROR]` with rc=0), API error bodies printed with exit code 0
  (`VPC.0305` not-found, `APIGW.0301` auth, generic codes, success payload
  not misclassified), marker paging (full page → next page, partial,
  empty, explicit `next_marker`), SDK fallback (hcloud missing → SDK, SDK
  unavailable, request construction / pagination with a mocked
  `huaweicloudsdkeip.v3` module), rendering (list table / detail text /
  Markdown list / Markdown detail / `-` fallback / empty 「无数据」),
  Markdown export (parent creation, atomic write, detail), and all `main()`
  output/error paths.

## SDK fallback note

`huaweicloudsdkeip` was not installed in the development environment, so the
SDK path could not be executed against the real API here. It is covered by
offline tests with a mocked `huaweicloudsdkeip.v3` module (request fields
`limit` / `marker` / `share_type` / `enterprise_project_id`, response
`bandwidths` / `bandwidth`, no-network). Real-environment SDK verification
belongs to the QA stage.

## Provenance

- CLI operation names and parameters: live `--help` output (KooCLI 7.3.12), as
  tabulated above.
- REST paths: EIP bandwidth resources under `/v3/{project_id}/eip/bandwidths`
  and `/v3/{project_id}/eip/bandwidths/{bandwidth_id}` (the same v3 EIP
  endpoint family used by the verified KooCLI calls).
- IAM actions `eip:bandwidths:list` / `eip:bandwidths:get` follow the Spec in
  Issue #195; see `references/iam-policies.md`.