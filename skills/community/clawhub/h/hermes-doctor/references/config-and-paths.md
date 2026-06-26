# HERMES_HOME 路径解析与文件清单

## HERMES_HOME 解析逻辑

源码:`hermes_constants.py:get_hermes_home()`。

优先级:
1. **环境变量 `HERMES_HOME`**(shell 当前进程或 HKCU 持久化都算)
2. fallback:`~/.hermes`(Mac/Linux)或 `%USERPROFILE%\.hermes`(Windows)
3. **profile 模式**:如果 `HERMES_HOME` 指向 `<root>/profiles/<name>`,则 `<root>` 是真正的 home,profile 只是子目录

**Windows 验证三步**:
```bash
echo "$HERMES_HOME"                                    # 当前进程
reg query "HKCU\Environment" /v HERMES_HOME             # 持久化(注销重登才生效)
hermes dump --redact 2>&1 | grep -i "hermes.home\|home_dir"   # 运行时识别
```

不一致就以 `hermes dump` 输出为准 — 那是 hermes 自己实际在用的。

## `<HERMES_HOME>/` 文件清单(关键)

| 文件/目录 | 作用 | 修复时优先级 |
|---|---|---|
| `.env` | 环境变量,主要是各 provider 的 API key | 高 |
| `.env.bak` | 上次 setup 前的 .env 备份(自动) | 参考 |
| `auth.json` | **凭证池主存储** — `credential_pool.<provider>[]` | **最高** |
| `auth.lock` | 跨进程文件锁,误删无害 | — |
| `config.yaml` | 主配置:model/provider/profiles/agent/skills/streaming 等 | 高 |
| `config.yaml.bak` | 上次 setup 前备份 | 参考 |
| `models_dev_cache.json` | provider 模型列表缓存(从 models.dev 同步) | 误删自动重建 |
| `state.db` + `-shm` + `-wal` | 跨会话状态(SQLite) | 低,WAL 大时 doctor --fix |
| `response_store.db` + `-shm` + `-wal` | 响应缓存(SQLite) | 同上 |
| `sessions/` | 每次会话的 JSON + request_dump | **诊断关键**,看实际请求 |
| `memories/` | 长期记忆(每个用户/topic 一个文件) | 跨机迁移要保留 |
| `skills/` | 用户安装/创建的 skill 目录 | 跨机迁移要保留 |
| `profiles/` | 多 profile 模式下的子家(各自 .env/config.yaml/auth.json) | 高级用法 |
| `cron/` | 定时任务定义 | 中 |
| `logs/` | 进程日志 | 诊断用 |
| `bin/` | hermes 命令入口的 symlink(Linux/Mac) | 中 |
| `hooks/` | 用户自定义钩子 | 高级用法 |
| `pairing/` | 跨设备配对状态 | 极少触碰 |
| `webui/` `hermes-webui/` `hermes-cs/` `hermes-agent/` | 子组件源码/资源(取决于安装方式,U-Hermes 打包版会有) | 不动 |
| `gateway_state.json` | gateway 服务状态 | 中,gateway 异常时看 |
| `interrupt_debug.log` | 中断调试日志 | 诊断用 |
| `SOUL.md` | 全局人设/系统提示词 | 中 |
| `USER.md` | 用户档案 | 中 |
| `.skills_prompt_snapshot.json` | skill 系统提示词缓存 | 误删自动重建 |
| `.update_check` | 上次检查更新的时间戳 | — |
| `.hermes_history` | CLI 输入历史 | — |
| `.tirith-install-failed` | 命令扫描器装失败标记 | 删了重试或忽略 |

## profile 模式

如果同一台机要切多个 hermes 用户/工作空间:

```bash
HERMES_HOME=~/.hermes/profiles/work hermes        # 公司
HERMES_HOME=~/.hermes/profiles/personal hermes    # 个人
```

每个 profile 子目录下完整复用上表结构。`hermes_constants.py` 会识别 `<root>/profiles/<name>` 模式,把 root 当 base,profile 当当前。

迁移 profile 时整个子目录复制即可。

## config.yaml 重点字段(2026-04 现役)

```yaml
model:
  active_profile: <name>            # 选哪个 model_profile,空=用顶层字段
  provider: <provider-name>         # 顶层 provider(active_profile 为空时生效)
  base_url: <url>                   # 顶层 base_url
  default: <model-id>               # 默认模型 id
  api_key: <key>                    # 顶层 api_key(优先级低于 credential_pool)
  auth_mode: api_key | oauth_device_code
  auth_header: Authorization
  auth_scheme: Bearer
  temperature: 0.7
  max_tokens: 4096

model_profiles:                     # 多 profile 切换
  <profile-name>:
    provider: ...
    base_url: ...
    default: ...
    api_key: ...
    # 完整字段同上 model.*
```

**坑**:active_profile 切换时,`config.yaml` 的 root `model.*` 不会自动同步成 profile 的值,但运行时 hermes 应该用 profile 字段。如果发请求到错的 base_url,看 issue #3685 — `api_mode` 残留。

## 修改 config.yaml 的安全做法

```bash
HOME_DIR="$(hermes dump --redact 2>&1 | awk -F': ' '/HERMES_HOME/{print $2; exit}')"
TS=$(date +%Y%m%d-%H%M%S)
cp "$HOME_DIR/config.yaml" "$HOME_DIR/config.yaml.broken-$TS"
# 直接编辑 config.yaml(yaml 语法,缩进敏感)
hermes doctor               # 验证语法和迁移
```

**永远不直接 truncate config.yaml** — 哪怕 setup 重写,部分字段(personalities / platform_toolsets)是 setup 不会回填的。
