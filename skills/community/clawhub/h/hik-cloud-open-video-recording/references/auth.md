# 认证说明

本技能内部使用海康云眸开放平台 OAuth token：

- 地址：`https://api2.hik-cloud.com/oauth/token`
- 方法：`POST application/x-www-form-urlencoded`
- 参数：`client_id`、`client_secret`、`grant_type=client_credentials`、`scope=app`

Skill 约束：

- 不对用户暴露“先获取 access_token 再调用”的显式工作流
- 脚本优先自动处理 token 获取、缓存、续期
- 业务接口统一注入 `Authorization: Bearer <access_token>`
- 401 时自动刷新 token 并重试一次
- 认证接口与业务接口统一跟随当前 base URL

环境变量：

- `HIK_OPEN_CLIENT_ID`
- `HIK_OPEN_CLIENT_SECRET`
- `HIK_OPEN_ACCESS_TOKEN`（可选覆盖）
- `HIK_OPEN_BASE_URL`（可选，用于指定自定义环境域名）
