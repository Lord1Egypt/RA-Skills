# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/bigdata/mrs/huawei-cloud-mrs-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- 43 cases cover: write-intent guard, command construction, JSON extraction,
  failure classification (missing AK/SK / 403 / generic), paging (total,
  full-page, isFinished, empty), rendering, and all main() output modes.

## Live verification (when credentials exist)

```bash
hcloud configure list                                                  # profile check
hcloud MRS ListClusters --cli-region=cn-north-4 --pageSize=1           # API sanity
python3 scripts/list_mrs.py --region cn-north-4                        # full flow
python3 scripts/list_mrs.py --json | python3 -m json.tool >/dev/null   # JSON validity
python3 scripts/list_mrs.py --names-only
python3 scripts/list_mrs.py --cluster-state running
```

Live verification was not executed in the coding phase of this issue (no live
credentials in the offline environment); the tester agent should re-run the live
checks above.

## REST path provenance

`GET /v1.1/{project_id}/cluster_infos` comes from the official
`huaweicloudsdkmrs` v1 client `_list_clusters_http_info` `resource_path`
metadata (cross-checked against the sibling skill `huawei-cloud-mrs-manage`
Phase 2 research, where `hcloud MRS ListClusters --cli-region=cn-north-4 --help`
succeeded live). No endpoint was inferred from naming patterns.
