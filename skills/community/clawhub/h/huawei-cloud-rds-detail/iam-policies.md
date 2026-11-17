# IAM 权限策略

## 最小权限原则

本 Skill 仅执行只读操作，遵循最小权限原则，只需以下 IAM 权限：

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:instance:list",
        "ces:metrics:list",
        "ces:metricData:list"
      ]
    }
  ]
}
```

## 权限说明

| 权限 | 关联 API | 说明 |
|------|----------|------|
| `rds:instance:list` | ListInstances | 查询 RDS 实例列表和详情 |
| `ces:metrics:list` | ListMetrics | 查询监控指标列表 |
| `ces:metricData:list` | BatchListMetricData | 批量查询监控指标数据 |

## 配置方式

### 华为云控制台

1. 登录 [IAM 控制台](https://console.huaweicloud.com/iam/)
2. 创建自定义策略，粘贴以上 JSON
3. 将策略授权给使用 AK/SK 的 IAM 用户
4. 授权范围选择「全局服务资源」

### 注意事项

- `rds:instance:list` 覆盖所有 RDS 实例的只读查询权限
- `ces:metrics:list` 和 `ces:metricData:list` 用于查询监控指标
- 本 Skill 不执行任何写操作，不需要 `rds:instance:create`、`rds:instance:delete` 等写权限
- 如需查询更多区域的 RDS 资源，无需额外权限配置，只需在调用时指定不同的 region 即可