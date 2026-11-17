# IAM 权限策略

## 该 Skill 需要的华为云权限

| 操作 | IAM 权限 | 说明 |
|------|---------|------|
| 查询监控指标列表 | `CES:ces:metrics:list` | 调用 ListMetrics 接口 |
| 查询监控指标数据 | `CES:ces:metrics:get` | 调用 ShowMetricData 接口 |

## 最小权限策略

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "CES:ces:metrics:list",
        "CES:ces:metrics:get"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## 权限说明

- 该 skill 只需要上述列出的只读权限（最小权限原则）
- 不需要管理员权限
- 不需要写权限（ListMetrics/ShowMetricData 均为只读查询操作）
- AK/SK 对应的 IAM 用户需具备上述权限，否则 API 返回 403
