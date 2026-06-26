# 认证说明

- 认证接口：`POST /oauth/token`
- 认证模式：`client_credentials`
- 请求参数：`client_id`、`client_secret`、`grant_type=client_credentials`、`scope=app`
- 业务接口请求头：`Authorization: Bearer <access_token>`
- access token 失效后，业务接口通常返回 HTTP `401`
- 本技能脚本会优先复用显式 token、环境变量或缓存中的 token；如果都没有，则自动使用 `HIK_OPEN_CLIENT_ID` 和 `HIK_OPEN_CLIENT_SECRET` 重新获取
- 缓存 token 若接近过期，会自动重新拉取
