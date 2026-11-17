# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI (both execution paths):

- KooCLI: `GET /v3/{project_id}/elb/loadbalancers` — `hcloud ELB ListLoadbalancers`
- SDK fallback: `huaweicloudsdkelb` v3 `ElbClient.list_load_balancers` (same REST path)

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | -------- | ----- | ------- |
| `elb:loadbalancers:list` | list | GET /v3/{project_id}/elb/loadbalancers | Query the ELB load balancer list |

The action above is the least-privilege read-only permission for this single
call. Because the request is authenticated with a project-scoped token and the
REST path contains `{project_id}`, the permission must be granted within the
target project (or the enterprise project when `enterprise_project_id` is used).

If you prefer a system policy, assign **ELB ReadOnlyAccess** instead of the
custom policy below.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elb:loadbalancers:list"
      ],
      "Resource": "*"
    }
  ]
}
```

## 403 troubleshooting

If the script reports `无权限访问弹性负载均衡（ELB），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target project.
2. Grant `elb:loadbalancers:list` (custom policy above) or the `ELB
   ReadOnlyAccess` system policy.
3. Re-run `python3 scripts/list_elb.py`.