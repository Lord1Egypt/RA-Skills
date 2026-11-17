# Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Query Anti-DDoS protected IPs in a region | `python3 scripts/list_aad_protected_ip.py --region=cn-north-4` |
| 2 | Default output shows 防护 IP and 封堵状态 | Default concise list |
| 3 | Detail table shows 防护 IP / 状态 / 绑定策略 / 套餐 / region | `python3 scripts/list_aad_protected_ip.py --table --region=cn-north-4` |
| 4 | `--json` returns the raw response | `python3 scripts/list_aad_protected_ip.py --json --region=cn-north-4` |
| 5 | `--ip` / `--policy-id` / `--package-id` / `--tag` filters work | Targeted command tests |
| 6 | `--limit` 1~100 with automatic offset paging | `--limit 50 --offset 0`; verify all pages fetched |
| 7 | `--region` overrides the default region | Run in a second AAD region |
| 8 | Empty list prints an explicit hint and exits 0 | `未找到 Anti-DDoS 防护 IP。` |
| 9 | Filtered-empty list prints an explicit hint and exits 0 | `未找到匹配的 Anti-DDoS 防护 IP。` |
| 10 | IAM permission missing prints a permission hint, no traceback | 403 / `not authorized` path |
| 11 | Missing credentials prints a credential hint, no traceback | Unset profile and env credentials |
| 12 | Network failure prints a network hint, no traceback | Simulated timeout |
| 13 | `[USE_ERROR]` falls back to the SDK | Mocked/unsupported-operation path |
| 14 | Write intents rejected before execution with exit 1 | `--action unblock`, `--tag delete-this` |
| 15 | Offline unit tests pass | `python3 -m unittest discover -s tests -v` |
| 16 | Syntax checks pass | `python3 -m py_compile`, `bash -n`, `python3 -m json.tool` |
| 17 | References complete | IAM policy, CLI install, verification method, this checklist |

## Scope

- In scope: read-only query of the Anti-DDoS protected-IP list (protected IP,
  status, bound policy, package, region).
- Out of scope: create / delete / update policies, associate / disassociate IPs,
  execute unblock, modify package or tag, traffic-cleaning statistics,
  attack-event analytics and alert subscriptions.