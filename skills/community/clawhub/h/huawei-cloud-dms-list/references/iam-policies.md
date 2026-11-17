# IAM Policies (least privilege, read-only)

The skill invokes exactly one Huawei Cloud OpenAPI, with two engine services
(both execution paths):

| Engine | KooCLI | SDK fallback | REST |
|--------|--------|--------------|------|
| Kafka | `hcloud Kafka ListInstances` | `huaweicloudsdkkafka` v2 `KafkaClient.list_instances` | `GET /v2/{project_id}/instances` |
| RabbitMQ | `hcloud RabbitMQ ListInstancesDetails` | `huaweicloudsdkrabbitmq` v2 `RabbitMQClient.list_instances_details` | `GET /v2/{project_id}/instances` |

## Required IAM action

| Action | Access level | API | Purpose |
| -------- | ----- | ------- | ------- |
| `dms:instance:list` | list | GET /v2/{project_id}/instances | List DMS (Kafka / RabbitMQ) instances |

`dms:instance:list` was verified against the official IAM authorization schema
(`hcloud IAM GetAuthorizationSchemaV5 --cli-region=cn-north-4 --service_code=dms`
→ action `dms:instance:list`, `access_level: list`, 中文描述
「授予查看实例列表的权限。」, no resource-scope constraint). It is the single
read-only action this skill needs: no `dms:topic:list`, `dms:user:list`,
`dms:vhost:list` or `dms:broker:list` permission is required by the instance
list call.

## Custom least-privilege policy (IAM 5.0)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dms:instance:list"
      ],
      "Resource": "*"
    }
  ]
}
```

If your account already has a Huawei Cloud DMS read-only system policy assigned
to the identity, that policy also covers this call — confirm the exact policy
name in the IAM console before relying on it (system policy names were not
verified in this environment; only the action name above was).

## 403 troubleshooting

If the script reports `无权限访问分布式消息服务（DMS），请检查 IAM 权限（403）`:

1. Confirm the AK/SK belongs to a user / agency in the target region's project.
2. Grant `dms:instance:list` (custom policy above) or the account's DMS
   read-only system policy.
3. Re-run `python3 scripts/list_dms.py`.

401 means the AK/SK itself is invalid or expired — refresh the credential
profile out-of-band; do not retry with a different identity.