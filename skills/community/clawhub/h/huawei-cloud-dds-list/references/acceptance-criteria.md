# Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Skill directory follows the repo convention `skills/database/dds/huawei-cloud-dds-list/` with `SKILL.md`, `scripts/`, `references/`, `tests/`, `templates/` | `find skills/database/dds/huawei-cloud-dds-list -type f` |
| 2 | Default output is the instance-name list | `python3 scripts/list_dds.py --region cn-north-4` |
| 3 | Empty region prints the explicit hint `当前区域（<region>）无 DDS 实例` | Empty region / empty filter result, exit 0 |
| 4 | `--table` prints the fixed 8 columns 实例ID / 名称 / 状态 / 引擎版本 / 规格 / 节点数 / 创建时间 / 模式; 模式 mapped to 集群/副本集/单节点; 创建时间取官方 `created`、规格取 `groups[].nodes[].spec_code`、节点数取 `groups[].nodes` 数量; missing values render as `-` | `python3 scripts/list_dds.py --table` |
| 5 | `--json` prints the raw instance array | `python3 scripts/list_dds.py --json \| python3 -m json.tool` |
| 6 | Pagination passes `--limit` (1~100) / `--offset` through and fetches pages automatically until `total_count` | `--limit 10 --offset 20`, `--single-page` |
| 7 | Server-side filters `--name` (+`--fuzzy`) / `--instance-id` / `--mode` / `--datastore-type` / `--vpc-id` / `--subnet-id` are forwarded as real query parameters | Mocked-argv unit tests + `hcloud DDS ListInstances --help` evidence |
| 8 | `--status` is a client-side filter (the API has no server-side status param — verified) | Unit test `test_client_side_filter`, hint `（客户端过滤）` |
| 9 | Region / project override supported | `--region`, `--project-id` |
| 10 | Missing / invalid AK-SK exits non-zero with a Chinese hint that never asks for secrets in chat | Mocked failure classification |
| 11 | 403 / insufficient IAM permission exits non-zero with a Chinese DDS permission hint | Mocked 403 response |
| 12 | Missing `project_id` on the SDK / REST fallback exits non-zero with an explicit hint | Unit test (SDK / REST paths) |
| 13 | `hcloud` missing falls back to the official SDK, then to the locally signed REST call; all three missing → non-zero exit with install hints | Unit test |
| 14 | KooCLI `[USE_ERROR]` output is treated as a hard failure with a Chinese hint and a non-zero exit, even when KooCLI returns 0 | Unit test `test_use_error_with_rc0_is_hard_failure` |
| 15 | Write intents (create / delete / restart / resize / backup / ...) are blocked before any command runs, exit 1 | `DeleteInstance` / `--create-instance` → exit 1, no `subprocess.run` call |
| 15b | Values of read-only filter options are data, not commands: an instance named after a verb is not blocked | `--name "create-me"` / `--instance-id "create-instance-01"` → exit 0, filter forwarded |
| 16 | Every request issued is a GET (`/v3/{project_id}/instances`) | `hcloud DDS ListInstances --help` (`Method: GET`) evidence in `verification-method.md` |
| 17 | SKILL.md documents prerequisites (offline AK/SK configuration) and runnable examples | SKILL.md § Prerequisites / § Core Commands |
| 18 | `scripts/ensure_env.py` checks / installs the SDK runtime dependency (`--check` / `--upgrade`) | `python3 scripts/ensure_env.py --check` |
| 19 | REST fallback builds `GET https://dds.<region>.myhuaweicloud.com/v3/{project_id}/instances` with AK/SK Signature V4 (`SDK-HMAC-SHA256`) and optional security token | Unit tests (URL, signature, token) |
| 20 | Offline unit tests are all green | `python3 -m unittest discover -s tests -v` |

## Scope

- In scope: read-only query of the DDS instance list for a region / project,
  with name / id / mode / tags server-side filters, client-side status
  filter, limit/offset paging, three output modes, and the CLI → SDK → REST
  execution tiers.
- Out of scope: every mutating operation (create / delete / restart / resize /
  backup / restore / upgrade / node add/remove), tag-based listing
  (ListInstancesByTags), and cross-region aggregation.
