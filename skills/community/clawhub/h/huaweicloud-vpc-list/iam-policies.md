# IAM 权限声明

本 Skill 通过华为云 AK/SK 签名调用两个只读接口，所需最小权限如下。

## 所需权限

| 服务 | 权限（Action） | 说明 | 资源 |
|------|----------------|------|------|
| 虚拟私有云 VPC | `vpc:vpcs:list` | 查询 VPC 列表（ListVpcs，只读） | `*`（或限定 `vpcs` 资源类型） |
| 统一身份认证 IAM | `iam:projects:listProjects` | 查询项目列表（ListProjects），用于按 Region 自动解析 project_id | `*` |

## 说明

- 仅需**只读**权限，不涉及 VPC 的创建 / 修改 / 删除等写操作。
- 若在配置中显式提供 `project_id`，则不会调用 IAM ListProjects，只需授予 `vpc:vpcs:list`。
- 若配置未提供 `project_id`，需要额外授予 `iam:projects:listProjects`。
- 建议通过自定义策略按最小授权原则配置，示例：

```json
{
  "Version": "1.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "vpc:vpcs:list",
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
