# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | Main path uses the real KooCLI operation `hcloud APIG ListInstancesV2` (GET /v2/{project_id}/apigw/instances) | ✅ `build_instance_command` |
| 3 | SDK fallback to `huaweicloudsdkapig` v2 when hcloud is missing | ✅ `list_instances_via_sdk` / `list_apis_via_sdk` |
| 4 | `--instance-id` drills down to that instance's API list (GET /v2/{project_id}/apigw/instances/{instance_id}/apis) | ✅ `list_apis` / `build_apis_command` |
| 5 | Default compact list: instance name / id / status | ✅ `compact_instance_lines` |
| 6 | `--table` renders 实例ID/名称/状态/规格/版本/可用区/EIP/VPC/创建时间 | ✅ `render_instance_table` |
| 7 | `--json` outputs the raw response records | ✅ `main` JSON modes |
| 8 | `--name` (exact) / `--fuzzy` (substring) / `--instance-id` / `--status` filters | ✅ `filter_records` |
| 9 | `--region` default `cn-north-4` and override | ✅ argparse default |
| 10 | `--limit` 1-100 with automatic offset/limit paging | ✅ `_page_size` / `_call_hcloud_page` |
| 11 | Write intents (create/delete/update/publish/offline/bind-eip/unbind-eip) rejected before execution with exit 1 | ✅ `guard_write_intent` (pre-argparse) |
| 12 | Empty list explicit hint (exit 0) | ✅ `_empty_hint` |
| 13 | 403 explicit hint with the two read-only IAM actions (exit 1), incl. KooCLI API envelopes on stdout with rc=0 | ✅ `AuthError` / `_payload_error` |
| 14 | Missing AK/SK explicit hint (exit 1); 401/`APIGW.0301` reported as invalid credentials, not 403 | ✅ `ConfigError` / `classify_hcloud_failure` |
| 15 | `[USE_ERROR]` parameter error explicit hint (exit 1) | ✅ `classify_hcloud_failure` |
| 16 | Non-existent `--instance-id` explicit hint `实例不存在` (exit 1) | ✅ `InstanceNotFoundError` |
| 17 | Offline unit tests with mocked hcloud, all passing (67 tests) | ✅ |
| 18 | `bash -n`, `py_compile`, `json.tool` all clean | ✅ |
| 19 | SKILL.md ≤ 500 lines, ≤ 30 files, ≤ 40 MB, allowed extensions only | ✅ |
| 20 | Live read-only smoke in cn-north-4: instance list rc=0, drill-down rc=0, invalid id rc=1, write intent rc=1 | ✅ |

## Notes

- The APIG `ListInstancesV2` response has no version / availability-zone / VPC
  field; those table cells show `-` rather than a fabricated value, and
  `--json` carries every field the service actually returned.
- Functional re-verification (real read-only calls) belongs to the QA stage;
  this skill performs no writes and creates no cloud resources.