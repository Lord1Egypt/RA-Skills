# Fallback Provider 链 / 速率限制 / 模型路由

## fallback_providers 是什么

主 provider 全挂(429 持续 / 401 不可恢复 / 网络断 / quota 用尽)时,hermes 切到备份 provider 继续跑。`config.yaml`:

```yaml
model:
  provider: deepseek
  default: deepseek-chat
  api_key: sk-...
  fallback_providers:
    - provider: openrouter
      default: deepseek/deepseek-chat
    - provider: gemini
      default: gemini-2.5-flash
```

链按顺序尝试,头部成功就停。

## fallback 链坍塌 — issue #15914

**症状**:主 provider rate limit 后切 fallback,fallback 也 401 跑不通,链塌方。

**根因**:`_resolve_api_key_provider_secret()` (`hermes_cli/auth.py:389-411`) 只读 `os.environ`。如果你只把 fallback provider 的 key 加到了 `auth.json.credential_pool` 而**没有同步进 .env / shell env**,fallback 启动时拿不到 key。

**解法**:
- 给 fallback 链上每一个 provider 都在 `.env` 写 KEY,**不要只放 credential_pool**
- 或升级到本 issue 已修复的版本(2026-04 时尚未确认修复)

## v2026.4.23 改进

转 4.23 起 credential_pool 在 fallback 切换时**保留状态**。意思:即便切到 fallback 又切回主 provider,旋转游标和 cooldown 都不会重置,继续从上次位置走。这本来不正常 — pool reset 会让所有曾经 401 的 key 又被试一次,被 ban 风险高。

## issue #16677:deepseek-v4-pro via OpenRouter 崩溃

**症状**(2026-04-26 起出现):
- gateway 进入 crash loop,Telegram bot 无响应
- 单独时 `deepseek/deepseek-v4-pro` 返回 401 "User not found"
- 401 被当 retryable 反复 retry,而不是立即 fallback

**workaround**:
- **不要**在 OpenRouter 走 deepseek/deepseek-v4-pro。改用 `deepseek/deepseek-chat` 或直连 deepseek
- 或换其他 router(Together / Anyscale)

## 速率限制(429)处理

`auth.json.credential_pool.<provider>[].last_status` 写成 429 时:
- 同 provider 多 key → 旋转下一把(策略决定)
- 单 key → 等 `last_error_reset_at`(从 server 的 retry-after 头取)
- v2026.4.13 起 exhaustion TTL 从 24h 降到 1h

清掉 cooldown(确认 quota 已恢复):
```bash
hermes auth reset deepseek
```

## 401 vs 403 vs 429 路由策略

| 状态 | 当前行为(2026-04) | 期望行为(issue #16677 提议) |
|---|---|---|
| 401 | 标记 key exhausted,旋转下一把(同 provider 池);链断时切 fallback provider | 401/403 立即 non-retryable 切 fallback,不在主 provider 内 retry |
| 403 | 同 401 | 同上 |
| 429 | 标记 cooldown,按 retry-after 等;旋转 | 已合理 |
| 5xx | retry 当前 key | 已合理 |

如果遇到主 key 持续 401 但你确认 key 健康(`curl` 直测能用) → 大概率是路由问题(参 #5561 kimi-coding base_url)或 provider 解析错位(参 #12146 custom 误 fallback 到 OpenRouter)。**不要**简单怪 hermes,用 hermes dump 看实际 base_url 和 source。

## 模型路由解析链(0.10.x 版本)

出请求时 hermes 按顺序解析:
1. **`config.yaml.model.active_profile`** 非空 → 用 `model_profiles.<name>` 字段
2. 否则用 `config.yaml.model.*` 顶层字段
3. **`api_key` 来源**:`_resolve_api_key_provider_secret()` 读 `os.getenv(env_var)`(参 PROVIDER_REGISTRY 的 api_key_env_vars 元组)。**注意:这一版本不读 credential_pool**(issue #15914)
4. env 没 → fallback 占位符 `no-key-required`(出 401 时就因为这个)
5. 启动时 hermes 会**反向**:把 env 里有的 key 自动写回 credential_pool(标记 source: env:*)

修复故障的关键:**让目标 KEY 出现在 hermes 启动时的 os.environ 里**。在 `<HERMES_HOME>/.env` 写就行,hermes 用 dotenv 加载。

## hermes 进程启动时加载 .env 的精确时机

源码 `hermes_cli/env_loader.py`(在 venv 或打包发行版下):
1. 读 `<HERMES_HOME>/.env`,合入 os.environ(已存在的 shell env 优先,不覆盖)
2. 读 profile 的 .env(如果 active_profile 是子目录模式)
3. 触发 PROVIDER_REGISTRY 解析

所以 shell 里 `export DEEPSEEK_API_KEY=...` **会覆盖** .env 的同名项。这在多 hermes 进程跑不同 key 时很有用(每个进程 export 自己的 key)。

排错时如果 .env 改了重启没生效,先 `env | grep <PROVIDER>_API_KEY` 看 shell 是不是还在覆盖。
