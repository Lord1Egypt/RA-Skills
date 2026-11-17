# IAM Policies (least privilege, read-only)

The skill invokes exactly two Huawei Cloud OpenAPI operations (both execution
paths):

| Execution path | Call | REST path |
| --- | --- | --- |
| KooCLI | `hcloud VPN ListVgws` | `GET /v5/{project_id}/vpn-gateways` |
| KooCLI | `hcloud VPN ListVpnConnections` | `GET /v5/{project_id}/vpn-connection` |
| SDK fallback | `huaweicloudsdkvpn` v5 `VpnClient.list_vgws` | `GET /v5/{project_id}/vpn-gateways` |
| SDK fallback | `huaweicloudsdkvpn` v5 `VpnClient.list_vpn_connections` | `GET /v5/{project_id}/vpn-connection` |

## Required IAM actions

| Action | Access level | Resource type | Purpose |
| -------- | -------- | ----- | ------- |
| `vpn:vpnGateways:list` | list | `vpnGateways` | Query the VPN gateway list |
| `vpn:vpnConnections:list` | list | `vpnConnections` | Query the IPSec connection list |

Both action names are observable verbatim from the live API: when the caller
lacks the permission, the VPN service returns

```json
{"error_code": "VPN.0007",
 "error_msg": "User: ... is not authorized to perform: vpn:vpnGateways:list
               on resource: vpn:cn-north-4:<project>:vpnGateways:* because no
               identity-based policy allows the vpn:vpnGateways:list action."}
```

and the same envelope names `vpn:vpnConnections:list` for the connection call.
No action name in this file is inferred from naming patterns — they are copied
from that response, which is also what the IAM authorization schema
(`hcloud IAM GetAuthorizationSchemaV5 --service_code=vpn`) reports for these
operations.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "vpn:vpnGateways:list",
        "vpn:vpnConnections:list"
      ],
      "Resource": "*"
    }
  ]
}
```

`Resource: "*"` is required because the list operations enumerate every
gateway / connection of the project; no resource-level scoping is available for
a list.

## System policy alternative

If your organization prefers a managed policy, attach the read-only VPN system
policy offered in the IAM console (search "VPN" + read-only in
**策略 → 系统策略**) instead of the custom statement above. The skill does not
hard-code a system-policy name because Huawei Cloud maintains several VPN
policy revisions; pick the current one in the console and verify it grants both
actions above.

## 403 troubleshooting

If the script reports `无权限访问 VPN 网关 / IPSec 连接，请检查 IAM 权限（403）`:

1. Confirm both actions are granted — a policy that only allows
   `vpn:vpnGateways:list` still fails on the connection query.
2. Confirm the project / region of the credential matches `--region`
   (`cn-north-4` by default); a profile bound to another region can produce the
   same envelope.
3. Re-run `hcloud configure list` (read-only, no secrets echoed) to confirm the
   active profile.

Do not work around a 403 by using another credential or by widening the policy
to write actions — the skill never needs them.