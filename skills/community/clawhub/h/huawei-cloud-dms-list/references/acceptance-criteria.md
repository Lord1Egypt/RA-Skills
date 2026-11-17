# Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Skill directory follows the repo convention `skills/database/dms/huawei-cloud-dms-list/` with `SKILL.md`, `scripts/`, `references/`, `tests/`, `templates/` | `find skills/database/dms/huawei-cloud-dms-list -type f` |
| 2 | Default output is the instance-name list | `python3 scripts/list_dms.py --region cn-north-4` |
| 3 | Empty region prints the explicit hint `当前区域（<region>）无 DMS 实例` | Empty region / empty filter result, exit 0 |
| 4 | `--table` prints 实例ID / 名称 / 引擎 / 版本 / 规格 / 状态 / 节点数 / 存储空间 / 创建时间 / VPC / 子网 / 连接地址; missing values render as `-` | `python3 scripts/list_dms.py --table` |
| 5 | `--json` prints the raw instance array | `python3 scripts/list_dms.py --json \| python3 -m json.tool` |
| 6 | Pagination passes `--limit` / `--offset` through and fetches pages automatically | `--limit 10 --offset 20`, `--single-page` |
| 7 | Filters `--name` / `--name-equal` / `--instance-id` / `--status` / `--enterprise-project-id` are forwarded as server-side query parameters | Mocked-argv unit tests + command inspection |
| 8 | Both engines are covered: Kafka (`hcloud Kafka ListInstances`) and RabbitMQ (`hcloud RabbitMQ ListInstancesDetails`); `--engine all` merges them | `--engine kafka`, `--engine rabbitmq`, default |
| 9 | Region / project override supported | `--region`, `--project-id` |
| 10 | Missing / invalid AK-SK exits non-zero with a Chinese hint that never asks for secrets in chat | Mocked failure classification |
| 11 | 403 / insufficient IAM permission exits non-zero with a Chinese DMS permission hint | Mocked 403 response |
| 12 | Missing `project_id` on the SDK fallback exits non-zero with an explicit hint | Unit test `test_sdk_missing_project_id_raises_config` |
| 13 | `hcloud` missing falls back to the official SDKs; both missing → non-zero exit with install hints | Unit test `test_hcloud_not_installed_and_sdk_missing` |
| 14 | KooCLI `[USE_ERROR]` output is treated as a hard failure with a Chinese hint and a non-zero exit, even when KooCLI returns 0 | Unit test `test_use_error_exit_code` |
| 15 | Write intents are blocked before any command runs | `--operation DeleteInstance`, `--name "restart-me"` → exit 1, no `subprocess.run` call |
| 16 | Every request issued is a GET (`/v2/{project_id}/instances`) | SDK `_http_info` + KooCLI `Method: GET` evidence in `verification-method.md` |
| 17 | SKILL.md documents prerequisites (offline AK/SK configuration) and runnable examples | SKILL.md § Prerequisites / § Core Commands |
| 18 | Offline unit tests are all green | `python3 -m unittest discover -s tests -v` |

## Scope

- In scope: read-only query of the DMS instance list (Kafka + RabbitMQ) for a
  region / project, with name / id / status / enterprise-project filters,
  limit/offset paging, and three output modes.
- Out of scope: every mutating operation (create / delete / resize / restart /
  flush / backup / restore / migrate), Topic / Queue / Vhost / user
  sub-resources, and cross-region aggregation.