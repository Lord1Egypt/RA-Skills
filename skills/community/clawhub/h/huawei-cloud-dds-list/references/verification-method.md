# Verification Method

Every external API fact used by this skill was verified by direct execution in
the development environment — nothing was inferred from training data.

## 1. KooCLI service / operation existence

```console
$ hcloud DDS --help
Available Operations:
  ... ListInstances ...
```

`DDS` is a real KooCLI service name and `ListInstances` a real operation
(KooCLI 7.2.12).

## 2. Operation signature (Method / params)

```console
$ hcloud DDS ListInstances --help
Method:
  GET

Params:
  --cli-region        required string
  --project_id        required string path
  --datastore_type    optional string query  [DDS-Community|DDS-Enhanced]
  --id                optional string query
  --limit             optional integer query (1..100, default 100)
  --mode              optional string query  [Sharding|ReplicaSet|Single]
  --name              optional string query  (leading * = fuzzy)
  --offset            optional integer query (>=0)
  --subnet_id         optional string query
  --tags              optional string query
  --vpc_id            optional string query
```

Consequences encoded in the code:

- `Method: GET` → the skill is read-only by construction.
- **No `--status` query parameter** → the script's `--status` filter is
  client-side and documented as such.
- `--limit` max is 100 (not 50 as in some other services).
- `--name` fuzzy matching uses a leading `*` (the script's `--fuzzy` flag).
- **`--mode` collides with a KooCLI system parameter** (authentication mode).
  A bare `hcloud DDS ListInstances --mode=ReplicaSet ...` prompts
  interactively and fails with `[USE_ERROR]EOF` in non-interactive runs.
  Verified resolution: pass `--cli-mode=<auth mode>` together with `--mode`;
  KooCLI then prefers `--cli-mode` for the system parameter and forwards
  `--mode` to the API. The script always emits both when the filter is used
  (auth mode defaults to `AKSK`, override via `DDS_LIST_CLI_MODE`).

## 3. Live read-only call (response shape)

```console
$ hcloud DDS ListInstances --cli-region=cn-north-4 --limit=1
{
  "instances": [],
  "total_count": 0
}
```

Response keys `instances` / `total_count` drive the script's extraction
(`extract_instances`) and automatic paging (`_total_count`).

### 3.1 Instance object fields (official response)

An instance item is `QueryInstanceResponse` (verified against the published
`huaweicloudsdkdds` v3 models, packages 3.0.45 … 3.1.220):

| Field group | Official field | Used by the table |
| ----------- | -------------- | ---------------- |
| Identity / state | `id`, `name`, `status`, `mode` | 实例ID / 名称 / 状态 / 模式 |
| Datastore | `datastore.type`, `datastore.version`, `datastore.storage_engine` | 引擎版本 |
| Timestamps | **`created`**, **`updated`** | 创建时间 |
| Network | `vpc_id`, `subnet_id` | (JSON only) |
| Flavor | **`groups[].nodes[].spec_code`** | 规格 |
| Node count | **`groups[].nodes[]` length (summed over groups)** | 节点数 |

Deliberate corrections encoded in the script (an earlier revision read
non-existent fields and always printed `-`):

- There is **no** top-level `type` — the instance type is `mode`
  (`Sharding` / `ReplicaSet` / `Single`); `type` is still tried first as a
  harmless alias.
- There is **no** `created_at` / `updated_at` — the creation and update times
  are `created` / `updated`. The script tries `created` first and keeps
  `created_at` as a legacy fallback.
- There is **no** top-level `flavor[]` — the flavor is per node group under
  `groups[].nodes[].spec_code`; the script de-duplicates the codes and joins
  them with commas (e.g. a sharded instance reports
  `...shard,...mongos`). A top-level `flavor[]` / `spec_code` is still accepted
  as a fallback for hand-built payloads.
- The node count is the number of `groups[].nodes[]` entries summed over all
  groups (shard + mongos + config …), not a top-level field; instances without
  group information render `-`. A top-level `nodes[]` is accepted as a legacy
  fallback.

The unit tests use the official shape (`created` + `groups[].nodes[].spec_code`)
so a regression to the non-existent fields fails the suite.

## 4. IAM action

```console
$ hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=dds
...
{ "name": "dds:instance:listAll", "access_level": "list",
  "aliases": ["dds:instance:list"],
  "description": {"zh_CN": "授予查询数据库实例列表的权限。"}, "resources": null }
```

See [iam-policies.md](iam-policies.md).

## 5. Write-intent guard evidence

`hcloud DDS --help` lists the mutating operations the guard blocks by
vocabulary: `CreateInstance`, `DeleteInstance`, `RestartInstance`,
`ResizeInstance`, `BatchDeleteBackup`, `CreateManualBackup`,
`BatchUpgradeDatabaseVersion`, `AddShardingNode`, `AddReadonlyNode`, etc.
Status vocabulary (CREATING / DELETING / RESIZING / FROZEN) is intentionally
NOT in the guard keyword list — those are legitimate `--status` filter values.

## 6. SDK fallback provenance

`huaweicloudsdkdds` v3 `DdsClient.list_instances` is the official SDK
counterpart of the same REST endpoint (`GET /v3/{project_id}/instances`); its
`ListInstancesRequest` model exposes `id`, `mode`, `name`, `datastore_type`,
`vpc_id`, `subnet_id`, `limit`, `offset` (limit/offset typed `int` in v3). The
published package ships a `v3` module only — 3.0.45 and 3.1.220 were inspected
and neither contains a `v2` module — so the script imports `v3` first and keeps
`v2` as a best-effort second chance. The fallback path is unit-tested with a
fake client; SDK-dependent tests auto-skip when the package is not installed
and were run for real against 3.1.220.

## 7. REST fallback provenance

The third tier issues the same `GET /v3/{project_id}/instances` directly
against `https://dds.<region>.myhuaweicloud.com` using only the standard
library. The request is signed locally with Huawei Cloud AK/SK Signature V4
(`SDK-HMAC-SHA256`): canonical URI + sorted/encoded query + canonical headers
(`host`, `x-sdk-date`, optional `x-security-token`) + empty-payload SHA-256,
then HMAC-SHA256 with the secret key. Unit tests pin the URL/query encoding,
the deterministic signature (including a security token) and the SDK→REST
hand-off.

## 8. Runtime dependency helper

`scripts/ensure_env.py` checks `huaweicloudsdkcore` + `huaweicloudsdkdds` and
installs what is missing (domestic mirrors first, official index fallback);
`--check` is read-only and `--upgrade` forces a refresh. The list script itself
needs no third-party module — the helper only enables the SDK tier.
