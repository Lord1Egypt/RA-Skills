# Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Query cloud-mode WAF protected domains in a region | `python3 scripts/list_waf_sites.py --region=cn-north-4` |
| 2 | Query protected domains across all WAF instances | `python3 scripts/list_waf_sites.py --all-modes --region=cn-north-4` |
| 3 | Output includes domain, protection status, access mode, keep-alive mode, exclusive-IP flag, domain ID | Default table columns |
| 4 | `--json` raw output supported | `python3 scripts/list_waf_sites.py --json --region=cn-north-4` |
| 5 | `--names-only` compact inventory supported | `python3 scripts/list_waf_sites.py --names-only --region=cn-north-4` |
| 6 | Filter by `--hostname`, `--protect-status`, `--enterprise-project-id`, `--policyname` | Targeted command tests |
| 7 | Region override via `--region` | Run in a second region |
| 8 | Empty region prints explicit empty hint | `当前区域无 WAF 防护网站。` |
| 9 | IAM permission missing prints explicit permission hint, does not crash | `无权限访问 WAF 防护网站列表...` |
| 10 | Write intents rejected before execution | `--hostname "delete x"` guard message |
| 11 | hcloud missing prints install hint | `未找到 hcloud CLI` |

## Scope

- In scope: read-only query of WAF protected website / domain-name list.
- Out of scope: create / delete / update / migrate domains, policy and rule
  management, log / certificate / instance management, detailed per-domain
  configuration export.