# IAM 只读策略（KMS 密钥列表）

本 skill 只调用两个只读接口，因此只需要最小只读权限。请 **不要** 给本 skill 授予任何
`kms:cmk:create` / `kms:cmk:enable` / `kms:cmk:disable` / `kms:cmk:scheduleKeyDeletion`
/ `kms:cmk:rotate` / `kms:grant:create` 等写权限——脚本本身也在执行前拦截写意图。

## 授权项对照

| 能力 | 需要的授权项 | 访问级别 | 说明 |
|------|--------------|----------|------|
| 查询密钥列表（`ListKeys`） | `kms:cmk:list` | List | 列表、别名、状态、用途、类型、创建时间、轮转开关 |
| 查询密钥详情（可选） | `kms:cmk:get` | Read | 仅在需要更细字段时使用，本 skill 不依赖 |
| 查询密钥轮换状态（`ShowKeyRotationStatus`） | `kms:cmk:getRotation` | Read | 轮转周期（30~365 天）、上次轮转时间、轮转次数 |

> 历史策略里 `kms:key:list` / `kms:key:get` 是上述授权项的旧称（别名），新账号请以
> `kms:cmk:*` 为准；两者在 IAM 侧等价，按控制台实际展示的授权项勾选即可。
> 若只需要列表而暂时拿不到 `kms:cmk:getRotation`，请加 `--no-rotation-detail`，
> 表格的「轮转周期」列会退化为「开启 / 关闭」，其余字段不受影响。

## 最小权限策略（角色与策略授权 / 自定义策略）

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:cmk:list",
        "kms:cmk:getRotation"
      ]
    }
  ]
}
```

## 身份策略（新版 IAM 身份策略授权）

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:cmk:list",
        "kms:cmk:getRotation"
      ],
      "Resource": [
        "KMS:*:*:key:*"
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
   跨企业项目盘点需在策略里放开 `g:EnterpriseProjectId` 条件或授予 `all_granted_eps`。

## 权限不足时的表现

- 脚本输出：`无权限访问 KMS 密钥列表（403），请检查 IAM 权限 kms:cmk:list…`
- 常见原因：未授权 / 策略未生效（IAM 授权有分钟级延迟）/ 密钥在另一个 region /
  使用了只有部分企业项目权限的账号。
- 处置：按上表补授权后重试；**不要** 通过换账号或绕行方式规避权限。