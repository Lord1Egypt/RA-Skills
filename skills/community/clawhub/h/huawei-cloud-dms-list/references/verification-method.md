# Verification Method

## 1. Service-name provenance (no guessing)

KooCLI has **no `DMS` service**. A live probe on KooCLI 7.3.12:

```text
$ hcloud DMS ListInstances --cli-region=cn-north-4
[USE_ERROR]Unsupported service: DMS
```

The two real services were confirmed with `--help` (live runs, 2026-11-04):

| Source | Evidence |
| -------- | --------- |
| KooCLI catalog (authoritative) | `hcloud Kafka ListInstances --help`: `Service: Kafka`, `Method: GET`, params `--cli-region` (required), `--project_id` (required, path), `--engine` (required, query, range `kafka`), `--enterprise_project_id`, `--exact_match_name` (`true`/`false`, default `false`), `--include_failure`, `--instance_id`, `--limit` (1~50, default 10), `--name`, `--offset` (≥ 0), `--status` |
| KooCLI catalog (authoritative) | `hcloud RabbitMQ ListInstancesDetails --help`: `Service: RabbitMQ`, `Method: GET`, same parameter set with `--engine` range `rabbitmq` |
| SDK `_http_info` (authoritative) | `huaweicloudsdkkafka` v2 `KafkaClient._list_instances_http_info` → `"method": "GET"`, `"resource_path": "/v2/{project_id}/instances"`; `huaweicloudsdkrabbitmq` v2 `RabbitMQClient._list_instances_details_http_info` → same path/method |
| SDK request models | `ListInstancesRequest` / `ListInstancesDetailsRequest` kwargs: `engine / name / instance_id / status / include_failure / exact_match_name / enterprise_project_id / offset / limit` (all `str`; unknown kwargs raise `TypeError`) |
| SDK response models | `ListInstancesResponse` / `ListInstancesDetailsResponse` → `instances: list[ShowInstanceResp]`, `instance_num: int` (drives the paging stop condition) |
| SDK region catalogs | `KafkaRegion.value_of("cn-north-4")` and `RabbitMQRegion.value_of("cn-north-4")` both resolve to `https://dms.cn-north-4.myhuaweicloud.com` |

Live read-only smoke (real credentials, region cn-north-4) returned
`{"instances": [], "instance_num": 0}` for both services — the account currently
has no DMS instances in that region, which also exercises the empty-list hint.

### SDK package selection

`huaweicloudsdkdms` v2 was inspected: its `DmsClient` exposes only queue /
consumer-group / tag operations (`list_queues`, `show_queues`,
`list_consumer_groups`, …) and **no** list-instances method, and none of its
`_http_info` metadata references `/v2/{project_id}/instances` for instances.
The instance-list SDKs are the per-engine packages
`huaweicloudsdkkafka` and `huaweicloudsdkrabbitmq`, which is what the fallback
path imports. Using `huaweicloudsdkdms` would have produced a fabricated call.

Consequences encoded in the script:

- `build_command()` emits only `--cli-region`, `--engine`, `--limit`,
  `--offset`, `--project_id` (when given) and the real server-side filters
  `--name` / `--exact_match_name=true` / `--instance_id` / `--status` /
  `--enterprise_project_id`; it never emits a parameter the API does not have.
- Paging uses `--limit` (validated 1~50, default 50) + `--offset`, and stops
  when `instance_num` is reached (or a short/empty page arrives).
- The SDK fallback constructs the request with exactly those fields, passing
  `limit`/`offset` as strings (the generated models declare them `str`).
- Credentials for the SDK fallback are read from a fixed whitelist of env names
  via `os.environ.get(name)` — `os.environ` is never enumerated (skillspector
  E2 hard-fails on bulk env access).

## 2. Structure / specification validation

```bash
bash <skills-dir>/huawei-cloud-skill-creator/scripts/validate-skill.sh -s <skill-path>
```

Checks: SKILL.md + frontmatter (name matches directory, description with
triggers, no `version`), required sections, Reference Documents section, no
hardcoded AK/SK (SEC-001/SEC-002), no cross-Skill references, one-PR-one-skill,
file count / SKILL.md line / extension allowlist.

## 3. Offline unit tests (mocked hcloud + fake SDK clients)

```bash
python3 -m unittest discover -s tests -v
```

63 cases. Every branch of `list_dms.py` is exercised with a mocked
`subprocess.run`: write-intent guard, command construction for both engine
services, JSON extraction, failure classification (`[USE_ERROR]` treated as a
hard failure even at rc=0), offset paging (`instance_num`-driven / short-page
stop / empty / max-pages guard), SDK fallback (env credentials, missing
credentials, missing project id, pagination, filters, real request signature,
endpoint resolution), table / JSON / names rendering, and all `main()` output
and error paths.

The 8 SDK-specific tests require `huaweicloudsdkcore` + `huaweicloudsdkkafka` +
`huaweicloudsdkrabbitmq` and skip when they are absent; both runs were done
(with and without the SDKs installed) and are green.

## 4. Functional smoke (read-only)

With a working hcloud profile:

```bash
hcloud configure list
python3 scripts/list_dms.py --region cn-north-4
python3 scripts/list_dms.py --table
python3 scripts/list_dms.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_dms.py --engine kafka --name dms --status RUNNING
```

Expected: an instance-name list (or table / JSON); an explicit
`当前区域（cn-north-4）无 DMS 实例` message on an empty region; an explicit
IAM hint on 403; exit 1 with no command executed for a write intent.