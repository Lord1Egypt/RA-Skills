# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/cci/huawei-cloud-cci-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- Cases cover: write-intent guard (read passes / create / delete / patch /
  replace / pod exec / scale / drain / normalized variants / operation
  whitelist / resource mismatch / filter-value stripping), command construction
  (cluster-wide vs namespaced routing, region, limit, continue token, no write
  flags ever), JSON extraction, continue-token paging, failure classification
  (missing AK/SK / 403 / generic / `[USE_ERROR]` with rc=0 / hcloud not
  installed), client-side name filter, normalization (namespace / pod /
  deployment) and rendering, and all main() output modes.

## Live verification (when a KooCLI profile exists)

```bash
hcloud configure list                                                # profile check
hcloud CCI ListCoreV1Namespace --cli-region=cn-north-4 --limit=1     # API sanity
python3 scripts/list_cci.py --region cn-north-4                     # full flow (namespace)
python3 scripts/list_cci.py --resource pod --json | python3 -m json.tool >/dev/null
python3 scripts/list_cci.py --resource pod --names-only
python3 scripts/list_cci.py --resource pod --namespace default
python3 scripts/list_cci.py --resource deployment --namespace default
python3 scripts/list_cci.py --resource pod --label-selector app=web  # server-side selector
```

## API / parameter provenance

CCI exposes a **Kubernetes-style OpenAPI**; the operation ids and REST paths below
come from the official CCI API reference / API Explorer CLI examples (no path was
inferred from naming patterns):

| KooCLI operation | REST path | Source |
| ---------------- | --------- | ------ |
| `ListCoreV1Namespace` | `GET /api/v1/namespaces` | CCI API reference (Kubernetes API → Namespace, "查询所有Namespaces") |
| `ListCoreV1PodForAllNamespaces` | `GET /api/v1/pods` | CCI API reference (Kubernetes API → Pod, "查询用户所有的Pods") |
| `ListCoreV1NamespacedPod` | `GET /api/v1/namespaces/{namespace}/pods` | CCI API reference (Kubernetes API → Pod, "查询指定namespace下的Pods") |
| `ListAppsV1DeploymentForAllNamespaces` | `GET /apis/apps/v1/deployments` | CCI API reference (Kubernetes API → Deployment, "查询用户所有Deployments") |
| `ListAppsV1NamespacedDeployment` | `GET /apis/apps/v1/namespaces/{namespace}/deployments` | CCI API reference (Kubernetes API → Deployment, "查询指定Namespace下的Deployments") |

- KooCLI operation name = PascalCase of the OpenAPI operation id
  (`listCoreV1NamespacedPod` → `ListCoreV1NamespacedPod`); the API Explorer "CLI
  示例" for CCI emits the same `hcloud CCI <Operation>` shape.
- Kubernetes list query parameters forwarded by the script: `--limit`,
  `--continue` (paging), `--labelSelector`, `--fieldSelector`, and
  `--namespace` for the namespaced variants. `--name` is applied client-side
  because the list APIs expose no name query parameter.
- Response shape: a Kubernetes `{kind: <Kind>List, metadata, items:[...]}`;
  metadata carries the `continue` token when more pages exist.
- IAM actions `cci:namespace:list` / `cci:pod:list` (and a `cci:deployment:list`
  equivalent) — confirm through
  `hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=cci`
  and the official 《CCI 权限及授权项说明》 document.

## No SDK fallback (by design)

Unlike most list skills, this skill has **no SDK fallback**: the CCI Python SDK
package `huaweicloudsdkcci` is not published on PyPI
(`pip install huaweicloudsdkcci` fails, and `https://pypi.org/pypi/huaweicloudsdkcci/json`
returns 404). The script therefore routes everything through KooCLI and raises a
clear `ConfigError` when the `hcloud` binary is missing.

## Environment note

The development environment did not have the `hcloud` binary installed, so the
KooCLI path was exercised in the in-session smoke against an offline KooCLI mock
whose output matches this skill's unit-test fixtures; the real read-only call is
the QA agent's stage. Live confirmation of the operation names / parameters
should be done with `hcloud CCI <Operation> --help` against an authenticated
profile.