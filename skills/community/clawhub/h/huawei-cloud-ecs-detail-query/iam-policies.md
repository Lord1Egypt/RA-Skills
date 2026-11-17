# IAM 权限策略

## 该 Skill 需要的华为云权限

| 操作 | IAM 权限 | 说明 |
|------|---------|------|
| 查询 ECS 实例详情 | `ecs:servers:get` | 通过 ShowServer API 查询单个 ECS 实例 |
| 查询 ECS 实例列表 | `ecs:servers:list` | 通过 ListServersDetails API 查询 ECS 列表 |

## 最小权限策略

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:servers:get",
        "ecs:servers:list"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## 权限说明

- 该 skill 只需要上述列出的权限（最小权限原则）
- 不需要管理员权限
- 不需要写权限（纯只读查询类 skill）
