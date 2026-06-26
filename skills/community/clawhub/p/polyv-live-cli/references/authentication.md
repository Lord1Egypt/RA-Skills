# 身份认证配置

保利威直播 CLI 支持命令行凭证、账号配置和环境变量。客户环境优先使用账号配置或环境变量，避免把密钥写入脚本和文档。

## 常用认证方式

### 账号配置

```bash
<CLI> account add production \
  --app-id your-app-id \
  --app-secret your-app-secret \
  --user-id your-user-id

<CLI> account set-default production
<CLI> account current
<CLI> account list
```

移除账号：

```bash
<CLI> account remove old-account
<CLI> account remove old-account --force
```

### 环境变量

```bash
export POLYV_APP_ID="your-app-id"
export POLYV_APP_SECRET="your-app-secret"
export POLYV_USER_ID="your-user-id"

<CLI> channel list
```

### 单次命令指定账号或凭证

```bash
<CLI> channel list -a production
<CLI> channel list --appId <id> --appSecret <secret> --userId <userId>
```

## 推荐流程

1. 使用 `account add` 添加客户账号。
2. 使用 `account set-default` 设置默认账号。
3. 使用 `account current` 或 `account list` 确认当前账号。
4. 再执行频道、商品、统计等业务命令。

```bash
<CLI> account add customer-prod \
  --app-id "$POLYV_APP_ID" \
  --app-secret "$POLYV_APP_SECRET" \
  --user-id "$POLYV_USER_ID"

<CLI> account set-default customer-prod
<CLI> account current
<CLI> channel list -o json
```

## CI/CD 示例

```yaml
env:
  POLYV_APP_ID: ${{ secrets.POLYV_APP_ID }}
  POLYV_APP_SECRET: ${{ secrets.POLYV_APP_SECRET }}
  POLYV_USER_ID: ${{ secrets.POLYV_USER_ID }}

steps:
  - name: 列出频道
    run: <CLI> channel list -o json
```

## 安全建议

- 不要把 AppID、AppSecret、UserID 提交到 Git。
- 给不同客户、环境分别配置账号名称，避免误操作生产资源。
- 客户交付文档中使用占位符，不写真实凭证。
- 执行删除、初始化、推送等高风险命令前，先用 `account current` 确认当前账号。

## 故障排除

### 认证配置不完整

```bash
<CLI> account current
<CLI> account list
```

如果没有默认账号，执行：

```bash
<CLI> account set-default <账号名称>
```

也可以在单次命令中用 `-a <账号名称>` 指定账号。

### 凭证无效

- 确认 AppID、AppSecret、UserID 是否来自同一保利威账号。
- 确认客户账号具备对应 API 权限。
- 如密钥已轮换，重新执行 `account add` 或更新环境变量。
