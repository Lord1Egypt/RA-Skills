# GMNCODE Usage API 参考

## 凭据存储

把账号密码放在 `~/.openclaw/.env`，不要硬编码进脚本。

```bash
GMNCODE_EMAIL=your_email@example.com
GMNCODE_PASSWORD=your_password
```

建议权限：

```bash
chmod 600 ~/.openclaw/.env
```

脚本读取顺序：
1. 当前进程环境变量
2. `~/.openclaw/.env`

`GMNCODE_BASE_URL` 在 skill 里固定为 `https://gmncode.cn`，不需要额外配置。

Token 缓存路径：
- `~/.cache/openclaw/gmncode-usage/token.json`
- 脚本会用仅当前用户可读写的权限写入缓存。
- 遇到 `401` / `INVALID_TOKEN` 时，脚本会删除缓存、重新登录并自动重试一次。

## 登录接口

`POST /api/v1/auth/login`

请求体：

```json
{
  "email": "...",
  "password": "..."
}
```

关键返回字段：
- `data.access_token`
- `data.refresh_token`
- `data.expires_in`

## 可用的接口

### 0. 活跃订阅 / 额度口径

`GET /api/v1/subscriptions?status=active`

常用字段：
- `daily_usage_usd`
- `weekly_usage_usd`
- `monthly_usage_usd`
- `group.daily_limit_usd`
- `group.weekly_limit_usd`
- `group.monthly_limit_usd`

推荐口径：
- 账户**每日使用额度** = 所有活跃订阅的 `group.daily_limit_usd` 求和
- 账户**今日已用** = 所有活跃订阅的 `daily_usage_usd` 求和
- 账户**今日剩余** = 每日使用额度 - 今日已用

### 1. 汇总统计

`GET /api/v1/usage/dashboard/stats?timezone=Asia/Shanghai`

常用字段：
- `today_requests`
- `today_tokens`
- `today_cost`
- `total_requests`
- `total_tokens`
- `total_cost`
- `total_actual_cost`

### 2. 每日趋势

`GET /api/v1/usage/dashboard/trend?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&timezone=Asia/Shanghai`

返回 `data.trend[]`，字段包括：
- `date`
- `requests`
- `total_tokens`
- `cost`
- `actual_cost`

### 3. 按模型拆分

`GET /api/v1/usage/dashboard/models?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&timezone=Asia/Shanghai`

返回 `data.models[]`，字段包括：
- `model`
- `requests`
- `input_tokens`
- `output_tokens`
- `cache_read_tokens`
- `total_tokens`
- `cost`
- `actual_cost`

## 备注

- 旧的 `/api/v1/usage/stats` 不适合这里的按日期 dashboard 统计。
- 上面这组 dashboard 接口使用普通用户 Bearer token 即可，不需要 admin 权限。
- `/api/v1/admin/dashboard/*` 这类 admin 路由对普通用户 token 会返回 `403 FORBIDDEN`，不要在这个技能里使用。
