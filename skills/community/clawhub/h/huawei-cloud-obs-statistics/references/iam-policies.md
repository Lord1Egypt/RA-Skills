# IAM Policies

## Least-Privilege Policy for OBS Aggregated Statistics

This skill is read-only: it lists buckets and objects only to aggregate summary
metrics. The minimal IAM actions are:

- `obs:bucket:ListBucket` — list the account's buckets and the objects in a bucket
- `obs:object:List` — list objects (with prefix) in a bucket

### Policy JSON

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "obs:bucket:ListBucket",
        "obs:object:List"
      ],
      "Resource": [
        "OBS:*:*:bucket:*",
        "OBS:*:*:object:*"
      ]
    }
  ]
}
```

### Alternative: Predefined Role

Huawei Cloud provides the `OBS ReadOnlyAccess` role which grants read-only
access to OBS buckets and objects, including bucket/object listing. Use it when
fine-grained policy management is not required.

### Notes

- No `obs:bucket:CreateBucket`, `obs:bucket:DeleteBucket`,
  `obs:object:PutObject`, `obs:object:DeleteObject`, or any other write/delete
  action is included — this skill never modifies resources.
- The `obsutil` tool is configured with AK/SK/endpoint via `~/.obsutilconfig`;
  the IAM policy above governs what those credentials are allowed to do.