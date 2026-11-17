# Verification Method — huawei-cloud-cdm-list

## Static / offline verification

- Offline unit tests (mocked hcloud subprocess, no credentials, no network):

  ```bash
  python3 -m unittest discover -s tests -v
  ```

  Result during development: **68 tests OK** (1 environment-dependent skip
  without the SDK installed; full pass with `huaweicloudsdkcore` +
  `huaweicloudsdkcdm` installed). Two of them are regression tests for the
  review findings below: the Markdown 节点数 column must carry the real count,
  and the CSV-detail rejection must be reachable through the render dispatch.

  Covered behaviour:
  - write-intent guard: read verbs pass; `CreateCluster`, `delete-cluster`,
    `RestartCluster`, `StartCluster`, `StopCluster`, `ModifyCluster`,
    `stop the cluster`, ... blocked; operation whitelist; value-flag exclusion
    (`--name cdm-delete-test`, `--output cdm-delete-report.json`,
    `--status stop-me` are not scanned, a following flag still is); extra
    `CDM_LIST_HCLOUD_ARGS` scanned; raw main argv intercepted before argparse.
  - operation resolution: default `ListClusters`; `--cluster-id` →
    `ShowClusterDetail`.
  - command construction: ListClusters argv contains **no** query parameters
    (official API fact), ShowClusterDetail carries `--cluster_id=`, REST paths
    under `/v1.1/{project_id}/clusters`.
  - JSON extraction (with wrapper noise) and error-envelope classification,
    including the permission envelope returned on **stdout with rc=0** and
    `[USE_ERROR]` usage errors.
  - client-side filters: name substring (case-insensitive), status code,
    status Chinese meaning, multi-status union, no-match empty.
  - normalization: camelCase→snake_case, derived `version`
    (datastore.version), `instance_count`, flattened `instances`,
    `status_meaning` fallback.
  - SDK fallback: triggered when `hcloud` is missing; missing env credentials
    raise `ConfigError`; missing package raises `ConfigError` (not a crash);
    whitelisted env credentials are picked up when the SDK is installed.
  - renderers: table / Markdown / CSV / JSON, incl. header-only empty output
    and the detail field/value views; CSV detail explicitly rejected (also on
    the real `_render` dispatch path). Markdown cells are asserted per column
    (the 节点数 column must show the real count, `1` / `0`). The raw nested
    `datastore` object is dropped from the flat table / CSV / detail views
    (its `version` / `datastore_type` derivations stay); `--format json` keeps
    the untouched API record.
  - no duplicate rows: `--max-calls > 1` re-reads the same full list (the API
    has no paging), so records are de-duplicated by cluster id and the loop
    stops when a call adds nothing new.
  - atomic export (temp file + rename, missing directory creation).
  - end-to-end through the **real subprocess path** with a fake hcloud binary
    (`CDM_LIST_HCLOUD_BIN`) asserting the exact argv forwarded.
  - `--help` exits 0 with the full parameter documentation.

## Live read-only verification (executed during development)

Not executed in the delivery environment (no hcloud binary and no AK/SK are
present there, by design). The verification steps below are exactly what QA
should run out-of-band with a configured profile:

```bash
hcloud CDM ListClusters --cli-region=cn-north-4
hcloud CDM ShowClusterDetail --cli-region=cn-north-4 --cluster_id=<uuid>
python3 scripts/list_cdm_clusters.py --region cn-north-4
python3 scripts/list_cdm_clusters.py --status 200
python3 scripts/list_cdm_clusters.py --cluster-id <uuid>
```

A `403 没有操作权限` response classifies as an explicit permission error (the
current IAM principal lacks `cdm:cluster:list` / `cdm:cluster:get`; not a skill
defect). Full end-to-end read validation requires an IAM principal holding
those permissions; it is performed out-of-band by QA.

## API facts verified (not guessed)

- REST paths and methods read from the `huaweicloudsdkcdm` v1
  `_list_clusters_http_info` / `_show_cluster_detail_http_info` metadata:
  `GET /v1.1/{project_id}/clusters` and
  `GET /v1.1/{project_id}/clusters/{cluster_id}`.
- `ListClustersRequest.attribute_map == {}` — the official ListClusters API
  takes no query parameters (no pagesize/startpage; one call returns the full
  list).
- KooCLI operation names verified against the official CDM CLI reference
  (clir-cdm): `hcloud CDM ListClusters`, `hcloud CDM ShowClusterDetail`
  (no `ShowCluster` operation exists).
- Response shapes verified against the SDK models (`Clusters`,
  `ShowClusterDetailResponse`, `ClusterDetailInstance`, `Datastore`) and the
  official API reference (status codes 100/200/300/303/500/800/900/910/920).
- `BasicCredentials` project-id auto-resolution verified in the
  `huaweicloudsdkcore` source (`Credentials.get_update_path_params` fills the
  `{project_id}` path parameter; IAM list-projects fallback).
- IAM actions `cdm:cluster:list` / `cdm:cluster:get` verified against the
  DataArts Studio permission documentation (CDM action list).
