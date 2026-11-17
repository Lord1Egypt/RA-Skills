# Acceptance Criteria — huawei-cloud-cdm-list

Mapped to Issue #134 (Spec comment 198477809).

- [x] `python3 scripts/list_cdm_clusters.py --help` exits 0 with complete
      parameter documentation (covered by an offline unit test).
- [x] Default table output includes the key cluster fields `id` / `name` /
      `status` / `status_detail` / `status_meaning` / `version`
      (datastore.version) / `instance_count` / `instances` / `flavor_name` /
      `az_name` / `public_endpoint` / `is_frozen` / `created` / `updated`;
      `--json` / `--markdown` / `--csv` all available.
- [x] `--name` (case-insensitive substring) and repeatable `--status` (code or
      Chinese meaning, union) filters work client-side; empty results print an
      explicit friendly message (and still write a header-only export file).
- [x] `--cluster-id` switches to the cluster-detail API (ShowClusterDetail,
      `GET /v1.1/{project_id}/clusters/{cluster_id}`) and renders the details
      incl. per-instance status/IPs.
- [x] Write-intent guard: create / delete / update / restart / resize / start /
      stop / expand intents (and CDM write operation names) are rejected with
      exit 1 before any command runs; only the two read-only GET operations are
      ever constructed.
- [x] hcloud missing → transparent fallback to `huaweicloudsdkcdm`
      (BasicCredentials with automatic project-id resolution); credentials
      missing → explicit out-of-band configuration hint (AK/SK are never
      requested, echoed or stored).
- [x] `python3 -m unittest discover -s tests -v` — 68 tests OK, offline
      (mocked hcloud subprocess / fake binary, no credentials, no network);
      incl. per-column Markdown assertions (节点数 = real count), CSV-detail
      rejection on the `_render` dispatch path, no duplicate rows with
      `--max-calls > 1`, and no raw `datastore` column in the flat views.
- [x] Changes limited to the skill directory
      (`skills/bigdata/cdm/huawei-cloud-cdm-list/`); no existing files touched.

## Deviations from the original Spec (documented, verified against official sources)

- The Spec's `ShowCluster` is actually named **`ShowClusterDetail`** in KooCLI
  and the SDK (the Spec's `GET /v1.1/{project_id}/clusters/{cluster_id}` is
  correct; the operation name was normalized to the real one).
- The Spec's “pagesize/startpage 自动分页” does not exist: the official
  ListClusters API takes no query parameters at all, so the implementation
  fetches the full list in one call (`--max-calls` is a defensive ceiling only,
  never sent to the API) and applies name/status filtering client-side, as the
  Spec itself chose for the filters.

## Out of scope

- Creating / deleting / restarting / resizing CDM clusters.
- CDM job / link (作业/连接) query and management.
- Writing anything back to any cloud service.
