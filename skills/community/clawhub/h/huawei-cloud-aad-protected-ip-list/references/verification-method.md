# Verification Method

## Prerequisites

```bash
hcloud version
hcloud AAD --help                       # AAD service available
hcloud AAD ListProtectedIp --help       # operation + parameters available
hcloud configure list                   # valid credential profile (read-only)
```

## Functional verification

### 1. Default concise list

```bash
python3 scripts/list_aad_protected_ip.py --region=cn-north-4
```

Expect either:

- a table with `防护 IP | 封堵状态` and a trailing line
  `共 N 个防护 IP（区域: cn-north-4，数据来源: KooCLI）`; or
- `未找到 Anti-DDoS 防护 IP。` when the account has no protected IPs.

Both outcomes return exit code 0.

### 2. Detail table

```bash
python3 scripts/list_aad_protected_ip.py --table --region=cn-north-4
```

Expect columns `防护 IP | 状态 | 绑定策略 | 套餐 | region`. Status is mapped as
`0 正常 / 1 清洗中 / 2 黑洞中（封堵中）`.

### 3. JSON output

```bash
python3 scripts/list_aad_protected_ip.py --json --region=cn-north-4
```

Expect valid JSON `{"total": N, "items": [...]}`. Each item includes `ip`,
`status`, `policy_name`, `package_name`, `region` and related fields.

### 4. Filters

```bash
python3 scripts/list_aad_protected_ip.py --ip 192.0.2.10 --region=cn-north-4
python3 scripts/list_aad_protected_ip.py --policy-id <policy-id> --region=cn-north-4
python3 scripts/list_aad_protected_ip.py --package-id <package-id> --region=cn-north-4
python3 scripts/list_aad_protected_ip.py --tag web --region=cn-north-4
```

Expect only matching IPs, or `未找到匹配的 Anti-DDoS 防护 IP。`.

`package_id` is validated by the service: it must be 32~64 characters. For a
match test pass a real package (instance) ID from the account; a 32-character
sample such as `0123456789abcdef0123456789abcdef` is format-valid and normally
returns an empty list (HTTP 200), which is the expected result for
`templates/test-vars.json` TC-03.

### 5. Paging

```bash
python3 scripts/list_aad_protected_ip.py --limit 50 --offset 0 --region=cn-north-4
```

Expect the wrapper to keep fetching pages (offsets 0, 50, 100, …) until the full
`total` is collected. `--limit` is a page size, not a total cap.

### 6. SDK fallback (offline simulation in unit tests; live requires the SDK)

When `hcloud` is absent or cannot serve `AAD ListProtectedIp`, the wrapper uses
`huaweicloudsdkaad`. A hint `[提示] KooCLI 不可用，已回退 SDK：...` is printed to
stderr.

### 7. Offline unit tests

```bash
python3 -m unittest discover -s tests -v
```

Expect all cases to pass (mocked KooCLI + mocked SDK, no network).

## Error-path verification

| Command | Expected hint |
|---------|---------------|
| `python3 scripts/list_aad_protected_ip.py --action unblock` | Read-only guard: `此技能为只读查询...` exit 1 |
| `python3 scripts/list_aad_protected_ip.py --tag "delete-this"` | Read-only guard, exit 1 |
| Run with an IAM identity lacking `aad:protectedIp:list` | `无权限访问 Anti-DDoS 防护 IP 列表...` |
| Run without credentials (CLI and SDK) | `未找到可用的华为云凭据...` |
| Simulate a network failure | `访问 Anti-DDoS 接口失败（网络超时或不可达）...` |
| Run without `hcloud` and without the SDK | `未找到 hcloud CLI，且未安装 huaweicloudsdkaad SDK...` |

## Acceptance signals

- All functional checks produce the documented output, OR the account genuinely
  has no protected IPs and the documented empty hint is printed — that confirms
  a graceful result, not a missing interface.
- `--json` output is valid JSON.
- No command produces a Python traceback.