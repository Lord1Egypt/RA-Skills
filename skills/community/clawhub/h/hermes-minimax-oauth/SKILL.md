# Hermes MiniMax OAuth Skill

为 Hermes Agent 添加 MiniMax OAuth 登录支持。

## 功能

通过 `hermes auth add minimax-oauth` 命令实现 MiniMax 全球版或中国区 OAuth 登录。

## 工作原理

### OAuth 流程（user_code + PKCE）

MiniMax 使用非标准的 user_code OAuth 流程，区别于常见的 device_code 流程：

```
1. POST /oauth/code          → 获取 user_code + verification_uri
2. 用户在浏览器打开 verification_uri，输入 user_code
3. POST /oauth/token         → 用 user_code + PKCE verifier 兑换 access_token
4. access_token 保存到 ~/.hermes/auth.json
```

**关键差异：**
- 端点：`/oauth/code` 和 `/oauth/token`（不是 `/v1/oauth/*`）
- grant_type：`urn:ietf:params:oauth:grant-type:user_code`
- 需要 PKCE（S256 code_challenge）
- scope：`group_id profile model.completion`

## 修改的文件

### `hermes_cli/auth.py`

- **新增常量**：`DEFAULT_MINIMAX_OAUTH_*`（portal URL、端点、client_id、scope）
- **新增函数**：
  - `_generate_pkce_pair()` — 生成 PKCE verifier/challenge
  - `_minimax_device_code_login()` — 完整 OAuth 流程
  - `resolve_minimax_oauth_runtime_credentials()` — 运行时凭证解析
  - `get_minimax_oauth_auth_status()` — 登录状态查询
  - `_refresh_minimax_access_token()` — access_token 刷新
  - `_is_minimax_token_expiring()` — 过期检查
- **新增 ProviderRegistry 条目**：`minimax-oauth`、`minimax-cn-oauth`

### `hermes_cli/runtime_provider.py`

- `_resolve_explicit_runtime()` 中添加 `minimax-oauth` / `minimax-cn-oauth` 处理块

### `agent/auxiliary_client.py`

- OAuth provider 路由中添加 MiniMax 处理路径

### `hermes_cli/auth_commands.py`

- `auth_add_command` 支持 `hermes auth add minimax-oauth` 和 `hermes auth add minimax-cn-oauth`

## 使用方法

```bash
# 全球版
hermes auth add minimax-oauth

# 中国版
hermes auth add minimax-cn-oauth

# 查看状态
hermes auth list
```

## 端点信息

| 区域 | Portal Base | Code Endpoint | Token Endpoint |
|---|---|---|---|
| Global | `https://api.minimax.io` | `/oauth/code` | `/oauth/token` |
| China | `https://api.minimaxi.com` | `/oauth/code` | `/oauth/token` |

- Client ID: `78257093-7e40-4613-99e0-527b14b39113`
- Scope: `group_id profile model.completion`
- Inference URL: `https://api.minimax.io/v1` (global) / `https://api.minimaxi.com/v1` (CN)

## 注意事项

- MiniMax **没有**标准的 device_code OAuth（`/v1/oauth/*` 是错的）
- 必须使用 PKCE S256，user_code 需配合 code_verifier 使用
- 登录后 token 通过 refresh_token 刷新，无需每次重新授权
