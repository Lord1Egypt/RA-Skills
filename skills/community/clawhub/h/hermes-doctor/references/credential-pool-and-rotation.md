# Credential Pool 与 Auto-Rotation(`hermes auth` 子命令族)

`hermes auth` 是 v2026.4.3 起引入的 **凭证池管理子命令族**,比直接编辑 `auth.json` 安全很多。优先用这个,改不动了再回退到手工 edit。

## 子命令速查

| 命令 | 作用 |
|---|---|
| `hermes auth` | 交互式管理向导(列池、加/删/重置都能选) |
| `hermes auth list` | 列所有 provider 的凭证池(脱敏) |
| `hermes auth add <provider>` | 加凭证(交互问 type/key/base_url) |
| `hermes auth add <provider> --type api-key --api-key <key>` | 非交互直加(脚本/skill 用) |
| `hermes auth remove <provider> <index>` | 按索引删(`hermes auth list` 看索引) |
| `hermes auth reset <provider>` | 清 cooldown / exhaustion 标记(401/429 后自动标的"暂时跳过"也清掉) |

**典型修复一行流**(用 hermes-doctor skill 时优先尝试):
```bash
hermes auth add deepseek --type api-key --api-key sk-xxxxxxxx
hermes auth list                                          # 验证
# 重启 hermes,发 ping
```

注意:旧版本 / 部分打包发行版(如 U-Hermes 0.10.x)可能**没有** `hermes auth` 子命令,fallback 到手工 edit `auth.json`(参 auth-troubleshooting.md)。先 `hermes auth --help` 试一下。

## 4 种 rotation 策略

`config.yaml` 顶层(不是 model.* 下):
```yaml
credential_pool_strategies:
  deepseek: least_used
  openrouter: round_robin
  anthropic: fill_first
  zai: random
```

| 策略 | 行为 | 适用场景 |
|---|---|---|
| `fill_first`(默认) | 用第一把健康 key 直到耗尽 | 单 key 用户、廉价 key 优先 |
| `round_robin` | 每次选下一把,均匀分散 | 多 key 配额对称,要均摊 |
| `least_used` | 选 `request_count` 最低的 | 多 key 配额不对称、做负载均衡 |
| `random` | 健康 key 里随机 | 简单,避开持续打同一把 key |

**v2026.4.3 改进**:401 失败现在**自动旋转**到下一把 key(以前会一直 retry 同一把)。耗尽 TTL 从 24h 降到 1h(v2026.4.13)。

## 凭证池工作流

启动时:
1. hermes 加载 `auth.json.credential_pool`
2. 对每个 provider,**自动从环境变量补种**(api_key_env_vars 中找到的有效 key 会被加进池,标记 `source: env:<VAR_NAME>`)
3. 自动从 `.env` 同步(等价于 env 变量来源)
4. **手动用 `hermes auth add` 添加的标记 `source: manual`**,**永不自动清理**;`source: env:*` 的会在下次发现 env 变量消失时自动剪除

每次发请求:
1. 按策略选一把 key
2. 失败 → 标记 `last_status` / `last_error_code` / `last_error_reset_at`
3. 401/403 → 标 exhausted,1h cooldown,旋转下一把
4. 429 → 标 cooldown 到 retry-after,旋转下一把

## 已知 credential_pool 相关坑(2026 春)

### #15914:env 变量缺失时不读 credential_pool(0.10.x 实测)
`hermes_cli/auth.py` 的 `_resolve_api_key_provider_secret()` **只**读 `os.getenv(env_var)`,**不**读 `credential_pool`。意味着:
- 你只用 `hermes auth add` 加凭证、`.env` 里没该 KEY → **启动后 hermes 还是拿不到 key**,fallback 到 `Bearer no-key-required`
- **解法**:同时在 `.env` 加 `<PROVIDER>_API_KEY=<key>` 一行,启动后 hermes 自然把它写回 pool

升级到修复版本后这个限制可能解除,但 0.10.x 及之前的版本仍存在。**所以本 skill 的标准修法是 .env + auth.json 双写**。

### #14218:custom provider 删除后池里残留
从 config 里删自定义 provider 后,`auth.json.credential_pool.<provider>` 数组还在,但 `hermes auth` 看不到(因为 `_get_custom_provider_names` 从 config 读)。**手工删 auth.json 那段** 或 `hermes auth remove <provider> <index>` 强制按名删。

### #6907:并发覆盖
两个 hermes 进程并发跑(比如 CLI + Telegram bot)各自修改 `auth.json` 时,后落盘的会覆盖先落盘的。表现为加了凭证一会儿又消失。**解法**:操作 auth.json 前先停其他 hermes 进程。

### #5561 / #5908:kimi-coding base_url 写错
`sk-kimi-` 前缀的 key 应路由到 `https://api.kimi.com/coding/v1`,但池里被写成默认 `https://api.moonshot.ai/v1`,首次调用 401。**解法**:`hermes auth remove kimi-coding <index>` 然后 `hermes auth add kimi-coding --type api-key --api-key sk-kimi-...`(新版会按 prefix 重新路由),或直接 edit auth.json 把 base_url 改对。

### #7863:`suppressed_sources` 是死代码
`auth.json.suppressed_sources` 字段写了不读,无法用它压制自动发现的 OAuth(比如 `~/.claude/.credentials.json` 的 claude_code token)。**解法**:在 .env 里把对应 env 变量(`ANTHROPIC_API_KEY` 等)显式置空,或删 `~/.claude/.credentials.json` 那把 OAuth。

### #5807:hermes doctor 看不到 pool 里的 Nous Portal token
`get_nous_auth_status()` 只查 `auth.json.providers`,不查 `auth.json.credential_pool`。`hermes auth add nous` 加进去的会被 doctor 误报"未登录"。无视即可,实际能用。

## fallback_providers vs credential_pool 区别

很多人混淆:

| | fallback_providers | credential_pool |
|---|---|---|
| 切什么 | provider(deepseek → openrouter) | 同 provider 的不同 key |
| 配置位置 | `config.yaml` model.fallback_providers | `auth.json` + `config.yaml` credential_pool_strategies |
| 用途 | 主 provider 全挂时切到备份 | 同 provider 多 key 做负载均衡 + 401/429 自动旋转 |
| v2026.4.23 改 | fallback 切换时保留 pool 状态 | — |

实际 ops 推荐:**两层都配**。同 provider 多 key 做日常 rotation,挂了再切 fallback provider。

## 一行 cheat sheet:401 紧急加 key

```bash
# 优先(版本支持时):
hermes auth add deepseek --type api-key --api-key sk-NEWKEY && hermes auth list

# fallback(0.10.x 及之前的版本必须 .env + auth.json 双写):
HOME_DIR="$(reg query 'HKCU\Environment' /v HERMES_HOME 2>/dev/null | awk '/HERMES_HOME/{print $NF}')"
[ -z "$HOME_DIR" ] && HOME_DIR="$HOME/.hermes"
TS=$(date +%Y%m%d-%H%M%S)
cp "$HOME_DIR/.env" "$HOME_DIR/.env.broken-$TS"
cp "$HOME_DIR/auth.json" "$HOME_DIR/auth.json.broken-$TS"
echo 'DEEPSEEK_API_KEY=sk-NEWKEY' >> "$HOME_DIR/.env"
# 然后用 Edit/jq 给 auth.json.credential_pool.deepseek 加一条(参 auth-troubleshooting.md 模板)
# 重启 hermes
```
