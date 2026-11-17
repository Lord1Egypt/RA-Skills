# IAM 权限策略

## 该 Skill 需要的华为云权限

| 操作 | IAM 权限 | 说明 |
|------|---------|------|
| 列出/查询命名空间 | `cci:namespaces:get` / `cci:namespaces:list` | 查询 CCI 命名空间 |
| 列出/查询 Pod | `cci:pods:get` / `cci:pods:list` | 查询 CCI Pod（容器实例） |
| 列出/查询 Deployment | `cci:deployments:get` / `cci:deployments:list` | 查询工作负载 |
| 列出/查询 Service | `cci:services:get` / `cci:services:list` | 查询 Service |
| 列出/查询 Network | `cci:networks:get` / `cci:networks:list` | 查询 CCI 网络 |
| 列出/查询 ConfigMap/Secret/PVC/Event | `cci:configmaps:*` / `cci:secrets:*` / `cci:persistentvolumeclaims:*` / `cci:events:*`（只读） | 查询其他资源 |

## 最小权限策略

推荐使用华为云系统策略 `CCI:ReadOnlyAccess`（只读访问 CCI 全部资源）。

如需自定义最小权限策略，可参考以下 JSON（按实际需要的资源裁剪）：

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cci:namespaces:get",
        "cci:namespaces:list",
        "cci:pods:get",
        "cci:pods:list",
        "cci:deployments:get",
        "cci:deployments:list",
        "cci:statefulsets:get",
        "cci:statefulsets:list",
        "cci:jobs:get",
        "cci:jobs:list",
        "cci:services:get",
        "cci:services:list",
        "cci:networks:get",
        "cci:networks:list",
        "cci:configmaps:get",
        "cci:configmaps:list",
        "cci:secrets:get",
        "cci:secrets:list",
        "cci:persistentvolumeclaims:get",
        "cci:persistentvolumeclaims:list",
        "cci:events:get",
        "cci:events:list"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## 权限说明

- 该 Skill 只需要上述列出的只读权限（最小权限原则）
- 不需要管理员权限
- 不需要写权限（Create/Delete/Update/Patch/Replace 均不在本 Skill 范围）
- 部分区域首次使用需在 CCI 控制台完成「服务授权」委托（agency），否则返回 `403 CCI.01.403122`

## CCI 服务授权委托

部分区域（如 `cn-east-3`）在首次查询时会返回：

```
403 CCI.01.403122 — user has no agency to cci, please apply a agency to cci
```

处理方式：登录华为云 CCI 控制台 → 选择对应区域 → 在「服务授权」页点击「同意」完成 agency 授权。授权后即可正常查询。
