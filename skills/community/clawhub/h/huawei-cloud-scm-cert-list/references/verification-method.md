# Verification Method

## Prerequisites

```bash
hcloud version
hcloud SCM ListCertificates --cli-region=cn-north-4 --help   # confirm Method: GET and the params
python3 -c "import huaweicloudsdkcore"                      # SDK core (fallback path only)
```

## 1. Offline unit tests (no credentials, no network)

```bash
python3 -m unittest discover -s tests -v
```

Expect: `Ran 63 tests ... OK`. The suite mocks the hcloud subprocess (fake
runner + a real mock executable injected through
`HUAWEI_CLOUD_SCM_CERT_LIST_HCLOUD_BIN`), injects a fake SDK client for the
fallback logic, and additionally builds the **real** SDK client once
(`TestSdkClientContract`, still offline) to lock the SCM credential contract:
`ScmClient` accepts only `GlobalCredentials`.

## 2. Real read-only smoke (needs `scm:cert:list`)

```bash
python3 scripts/list_scm_certs.py --region cn-north-4; echo "rc=$?"
```

Expect one of:

- a compact table `证书名称 | 绑定域名 | 到期时间` plus
  `共 N 个证书（区域: cn-north-4，后端: cli，来源: …）`, `rc=0`;
- `未找到 SSL 证书（区域: cn-north-4）。` plus a region hint, `rc=0`.

If the calling account has no `scm:cert:list`, the script must print the 403
hint (`无权限访问 SCM 证书列表 … scm:cert:list`) with `rc=1` — that is a
permission outcome, **not** a skill failure and **not** an empty list.

## 3. Output modes

```bash
python3 scripts/list_scm_certs.py --table --region cn-north-4
python3 scripts/list_scm_certs.py --json  --region cn-north-4 | python3 -m json.tool
```

- `--table`: exactly eight columns `证书ID | 名称 | 域名 | 类型 | 状态 | 到期时间 | 剩余天数 | region`.
- `--json`: valid JSON with `certificates`, `total_count`, `region`.

## 4. Filters

```bash
python3 scripts/list_scm_certs.py --content <name-or-domain> --region cn-north-4
python3 scripts/list_scm_certs.py --expiring 30 --region cn-north-4
python3 scripts/list_scm_certs.py --region ap-southeast-1
```

- `--content` must be sent to the API (`--content=...`) and re-applied
  client-side on name / domain / SAN.
- `--expiring N` only keeps certificates whose `剩余天数 <= N` (expired ones,
  i.e. negative days, are included); the footer count reflects the filtered set.
- `--region` must appear in both the output footer/region column and the
  `--cli-region=` argument.

## 5. Pagination

With more than one page of certificates:

```bash
python3 scripts/list_scm_certs.py --limit 10 --region cn-north-4
```

Expect the script to call `--offset=0`, `--offset=10`, … until a short page or
`total_count` is reached; the footer `共 N 个证书` equals the deduplicated total.
`--max-pages` caps the loop (useful when checking a huge account).

## 6. Read-only guard

```bash
python3 scripts/list_scm_certs.py --action delete; echo "rc=$?"
python3 scripts/list_scm_certs.py --action import; echo "rc=$?"
python3 scripts/list_scm_certs.py --content push;  echo "rc=$?"
```

Expect `rc=1` and a `只读` rejection message; no hcloud / SDK call is made.

## 7. Error paths

| Invocation | Expected |
| ---------- | -------- |
| `--backend cli` without hcloud on PATH | `未找到 hcloud（KooCLI）…`, `rc=1` |
| `--backend sdk` without AK/SK env | `缺少华为云凭据（AK/SK）…`, `rc=1` |
| `--backend sdk` without `huaweicloudsdkscm` | `pip install huaweicloudsdkcore huaweicloudsdkscm` hint, `rc=1` |
| Unauthorized account | `scm:cert:list` hint, `rc=1` |
| `--limit 30` | `--limit 仅支持 10 / 20 / 50`, `rc=1` |

Every failure prints a single actionable message plus an optional `详情:` line —
never a Python traceback.

## 8. Syntax checks

```bash
bash -n scripts/ensure_cli.sh scripts/install_cli.sh
python3 -m py_compile scripts/list_scm_certs.py tests/test_list_scm_certs.py
python3 -m json.tool templates/test-vars.json > /dev/null
```