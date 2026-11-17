# IAM 只读策略（SCM 证书列表）

本 skill 只调用一个只读接口 `SCM ListCertificates`，因此只需要最小只读权限。
请 **不要** 授予任何 `scm:cert:create` / `scm:cert:delete` / `scm:cert:import`
/ `scm:cert:push` / `scm:cert:revoke` 等写权限——脚本本身也在调用前拦截写意图。

## 授权项对照

| 能力 | 需要的授权项 | 访问级别 | 说明 |
|------|--------------|----------|------|
| 查询证书列表（`ListCertificates`） | `scm:cert:list` | List | 证书 ID、名称、绑定域名、类型、状态、到期时间 |

> `scm:cert:list` 为官方授权项名称：未授权时 SCM 接口返回
> `SCM.4002 Permission denied ... not authorized to perform: scm:cert:list`
> （资源形如 `scm:<region>:<account-id>:cert:*`）。本 skill 不需要任何其它授权项。

## 最小权限策略（新版 IAM 身份策略，推荐）

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "scm:cert:list"
      ],
      "Resource": [
        "scm:*:*:cert/*"
      ]
    }
  ]
}
```

## 兼容旧版（角色与策略授权 / 自定义策略）

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "scm:cert:list"
      ]
    }
  ]
}
```

## 授权步骤（管理员侧，一次性）

1. 登录华为云控制台 →「统一身份认证服务 IAM」→「用户组」→ 新建/选择给运维人员的用户组。
2. 「权限配置」→「创建自定义策略」→ 选 JSON 方式 → 粘贴上面的最小权限策略。
3. 把该自定义策略授权给用户组，并将执行本 skill 的 IAM 用户加入该用户组。
4. 若账号使用企业项目，注意策略作用范围：默认企业项目内不勾选企业项目即可；
   跨企业项目盘点需在策略里放开 `g:EnterpriseProjectId` 条件或授予
   `all_granted_eps`，并可用 `--enterprise-project-id` 指定项目。

## 权限不足时的表现

- 脚本输出：`无权限访问 SCM 证书列表（403），请授予 IAM 只读权限 scm:cert:list 后重试。`（退出码 1）
- 常见原因：未授权 / 策略未生效（IAM 授权有分钟级延迟）/ 证书在另一个 region /
  使用了只有部分企业项目权限的账号。
- 处置：按上表补授权后重试；**不要** 通过换账号或绕行方式规避权限。
- **禁止**把 403 当成「没有证书」：脚本对两者给出不同提示，403 恒为退出码 1。