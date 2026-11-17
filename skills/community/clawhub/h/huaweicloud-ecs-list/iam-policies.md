# IAM 权限声明

本 Skill 通过华为云 AK/SK 签名调用两个只读接口，所需最小权限如下。

## 所需权限

| 服务 | 权限（Action） | 说明 | 资源 |
|------|----------------|------|------|
| 弹性云服务器 ECS | `ecs:cloudServers:list` | 查询云服务器列表（ListServersDetails，只读） | `*`（或限定 `cloudServers` 资源类型） |
| 统一身份认证 IAM | `iam:projects:listProjects` | 查询项目列表（ListProjects），用于按 Region 自动解析 project_id | `*` |

## 说明

- 仅需**只读**权限，不涉及 ECS 的创建 / 启停 / 删除等写操作。
- 若在配置中显式提供 `project_id`，则不会调用 IAM ListProjects，只需授予 `ecs:cloudServers:list`。
- 若配置未提供 `project_id`，需要额外授予 `iam:projects:listProjects`。
- 建议通过自定义策略按最小授权原则配置，示例：

```json
{
  "Version": "1.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:cloudServers:list",
        "iam:projects:listProjects"
      ],
      "Resource": ["*"]
    }
  ]
}
```

## 风险提示

- 请勿将 AK/SK 写入仓库或任何共享配置，仅保存在本地 `config.json`（已 gitignore）。
- 建议定期轮换 AK/SK，并仅为该账号授予上述只读权限。
