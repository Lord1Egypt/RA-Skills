# IAM 只读策略（AS 伸缩组列表）

本 skill 只调用两个只读接口，因此只需要最小只读权限。请 **不要** 授予
`as:scalingGroup:create` / `as:scalingGroup:delete` / `as:scalingGroup:update`
/ `as:scalingGroup:enable` / `as:scalingGroup:disable` / `as:scalingPolicy:execute`
/ `as:scalingGroup:batchAddInstances` / `as:scalingGroup:batchRemoveInstances`
等写权限——脚本本身也会在执行前拦截写意图。

> 授权项名称已按华为云《弹性伸缩 AS API 参考》核对：
> - `ListScalingGroups` → `as:scalingGroup:list`（别名 `as:groups:list`，资源类型 `-`）
> - `ListScalingInstances` → `as:scalingGroup:listInstances`（别名 `as:instances:list`，资源类型 `scalingGroup*`）
>
> 控制台里如果只看到别名（`as:groups:list` / `as:instances:list`），两者等价。

## 授权项对照

| 能力 | 需要的授权项（主名） | 别名 | 访问级别 | 说明 |
|------|--------------------|------|----------|------|
| 查询伸缩组列表（`ListScalingGroups`） | `as:scalingGroup:list` | `as:groups:list` | List | 名称 / ID / 状态 / 期望与当前实例数 / 最小-最大 / VPC / 子网 / ELB / 创建时间 |
| 查询组内实例列表（`ListScalingInstances`） | `as:scalingGroup:listInstances` | `as:instances:list` | List | 实例 ID / 名称 / 生命周期状态 / 健康状态 / 加入时间 |

## 最小权限策略（角色与策略授权 / 自定义策略）

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "as:scalingGroup:list",
        "as:scalingGroup:listInstances"
      ]
    }
  ]
}
```

## 身份策略（新版 IAM 身份策略授权）

`ListScalingGroups` 在官方文档中的资源类型为 `-`（不支持资源级授权），使用 `"*"`；
`ListScalingInstances` 支持资源级授权，限定到 `scalingGroup` 资源：

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "as:scalingGroup:list"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "as:scalingGroup:listInstances"
      ],
      "Resource": [
        "AS:*:*:scalingGroup:*"
      ]
    }
  ]
}
```

## 授权步骤（管理员侧，一次性）

1. 登录华为云控制台 →「统一身份认证服务 IAM」→「用户组」→ 新建/选择给运维人员的用户组。
2. 「权限配置」→「创建自定义策略」→ 选 JSON 方式 → 粘贴上面的最小权限策略。
3. 把该自定义策略授权给用户组，并将执行本 skill 的 IAM 用户加入该用户组。
4. 若账号使用企业项目，注意策略作用范围：`ListScalingGroups` 支持
   `g:EnterpriseProjectId` 条件；跨企业项目盘点需在策略里放开该条件。

## 权限不足时的表现

- 脚本输出：`无权限访问 AS 伸缩组/实例（403），请检查 IAM 权限 …`
- 常见原因：未授权 / 策略未生效（IAM 授权有分钟级延迟）/ 伸缩组在另一个
  region / 使用了只有部分企业项目权限的账号。
- 处置：按上表补授权后重试；**不要** 通过换账号或绕行方式规避权限。

## 只读保证

- 脚本只会构造 `ListScalingGroups` / `ListScalingInstances` 两个 GET 请求。
- 写意图守卫在 argparse 与网络调用之前检查原始命令行；命中即退出码 1。
- 建/改/删伸缩组、启停、批量加入/移出实例、执行伸缩策略均不在本 skill 范围，
  需要独立的可写 skill 并显式用户确认。