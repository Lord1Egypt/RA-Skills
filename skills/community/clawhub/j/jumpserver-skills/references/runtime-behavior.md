# Runtime

## 概览

- 仓库支持环境初始化写入：`config-write --confirm` 可生成或更新 `.env.local`。
- 仓库支持组织持久化：`select-org --confirm` 可写回 `JMS_ORG_ID`。
- `ping` 仍是正式预检步骤之一，用于检查连通性和当前账号上下文。
- 资产、权限、审计相关业务命令仍是只读查询。
- 当前仓库是查询型 skill，不是通用运维执行器。

## 预检顺序

```text
config-status --json
  -> complete=false: 对话收集配置
  -> config-write --confirm
  -> ping
  -> 缺组织时 select-org --confirm
  -> 执行正式只读查询
```

## 环境变量

下表以当前实现为准，来源于 `scripts/jms_runtime.py`。

| 变量 | 是否必需 | 说明 | 示例 |
|---|---|---|---|
| `JMS_API_URL` | 必需 | JumpServer API/访问地址 | `https://jump.example.com` |
| `JMS_VERSION` | 建议配置 | JumpServer 版本，当前默认按 `4` 处理 | `4` |
| `JMS_ACCESS_KEY_ID` | 与 `JMS_ACCESS_KEY_SECRET` 成组，或改用用户名密码 | AK/SK 鉴权 ID | `your-access-key-id` |
| `JMS_ACCESS_KEY_SECRET` | 与 `JMS_ACCESS_KEY_ID` 成组，或改用用户名密码 | AK/SK 鉴权密钥 | `your-access-key-secret` |
| `JMS_USERNAME` | 与 `JMS_PASSWORD` 成组，或改用 AK/SK | 用户名密码鉴权用户名 | `ops-user` |
| `JMS_PASSWORD` | 与 `JMS_USERNAME` 成组，或改用 AK/SK | 用户名密码鉴权密码 | `your-password` |
| `JMS_ORG_ID` | 初始化时可选 | 业务执行前通过 `select-org` 或保留组织特判写入 | `00000000-0000-0000-0000-000000000000` |
| `JMS_TIMEOUT` | 可选 | SDK 请求超时秒数 | `30` |
| `JMS_SDK_MODULE` | 可选 | 自定义 SDK 模块路径，默认 `jms_client.client` | `jms_client.client` |
| `JMS_SDK_GET_CLIENT` | 可选 | 自定义 client 工厂函数名，默认 `get_client` | `get_client` |

## `.env.local` 示例

```dotenv
JMS_API_URL="https://jump.example.com"
JMS_VERSION="4"
JMS_ORG_ID=""

JMS_ACCESS_KEY_ID="your-access-key-id"
JMS_ACCESS_KEY_SECRET="your-access-key-secret"

# JMS_USERNAME="ops-user"
# JMS_PASSWORD="your-password"

# JMS_TIMEOUT="30"
# JMS_SDK_MODULE="jms_client.client"
# JMS_SDK_GET_CLIENT="get_client"
```

## 环境变量规则

- 必须提供 `JMS_API_URL`。
- 认证方式必须二选一：`AK/SK` 或 `用户名/密码`。
- `.env.local` 会被脚本自动加载。
- 首次配置缺失时，推荐先执行 `python3 scripts/jms_diagnose.py config-status --json`。
- 如果你切换了 JumpServer、账号、组织或 `.env.local` 内容，应该按首次运行重新做全量校验。

## 允许的环境写入

| 命令 | 作用 |
|---|---|
| `config-write --confirm` | 生成或更新 `.env.local` |
| `select-org --confirm` | 写回 `JMS_ORG_ID` |

## 保留组织特判

- 若可访问组织集合恰好是 `{0002}` 或 `{0002,0004}`，系统允许自动写入 `0002` 并继续。
- 这不是通用默认组织；其他环境仍需显式 `select-org --confirm`。

## 实现备注

- 当前 `scripts/jms_runtime.py` 在构造 client 时固定使用 `verify=False`。
- HTTPS 证书告警会被抑制。
- 这两个行为目前不是通过环境变量控制的。

## 常见阻塞

| 现象 | 原因 | 下一步 |
|---|---|---|
| `complete=false` | 地址或鉴权不完整 | 用用户提供的信息执行 `config-write --confirm` |
| `selection_required=true` | 当前缺少组织上下文 | 先 `select-org`，再 `select-org --confirm` |
| `selected_org_accessible=false` | 当前 `JMS_ORG_ID` 不可访问 | 重新 `select-org --confirm` |
