# Verification Method

## Prerequisites

```bash
hcloud version
hcloud WAF --help                 # confirm ListHost / ListCompositeHosts exist
```

## Functional verification

### 1. Cloud-mode protected-domain list

```bash
python3 scripts/list_waf_sites.py --region=cn-north-4
```

Expect: a table with 防护域名 | 防护状态 | 接入方式 | 保活方式 | 独享IP | Domain ID, and a
trailing line `共 N 个防护网站（区域: cn-north-4）`. If the account has no WAF
sites, the script prints `当前区域无 WAF 防护网站。`.

### 2. All-modes list

```bash
python3 scripts/list_waf_sites.py --all-modes --region=cn-north-4
```

Expect: composite list including `waf_type=premium` domains when present.

### 3. JSON output

```bash
python3 scripts/list_waf_sites.py --all-modes --json --region=cn-north-4
```

Expect: a JSON array/body containing `hostname`, `protect_status`, `waf_type`,
`proxy`, `exclusive_ip`, `hostid`.

### 4. Name-only output

```bash
python3 scripts/list_waf_sites.py --names-only --region=cn-north-4
```

Expect: one domain per line.

### 5. Filter by protection status

```bash
python3 scripts/list_waf_sites.py --all-modes --protect-status 1 --region=cn-north-4
```

Expect: only protected (`enabled`) domains.

## Error-path verification

| Command | Expected hint |
|---------|---------------|
| `python3 scripts/list_waf_sites.py --hostname "create x.com"` | Read-only guard: 「不支持对防护域名进行操作」 |
| Unset `hcloud`, run script | 「未找到 hcloud CLI」 |
| IAM without `waf:host:list` | 「无权限访问 WAF 防护网站列表」 |

## Acceptance signals

- All five functional checks produce the documented output, OR the account
  permission is genuinely absent (`WAF.00012006`) and the documented hint is
  printed — that confirms the skill fails gracefully, not that the interface is
  missing.
- `--json` output is valid JSON.