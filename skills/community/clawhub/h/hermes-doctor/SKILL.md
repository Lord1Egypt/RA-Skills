---
name: hermes-doctor
description: 诊断与抢救 Hermes Agent (NousResearch) 故障 — 401/Authentication Fails、provider 切换后 key 没注入、credential_pool 缺条目、HERMES_HOME 被环境变量重定向、gateway lock、stale config、备份恢复。Windows 优先。覆盖 .env / auth.json / HKCU\Environment / config.yaml profile 四处残留点排查、hermes auth 子命令族(v2026.4.3+)、credential_pool 4 种 rotation 策略、已知 issues #16394/#15914/#3685/#16677 等的完整 workaround。
version: 1.1.0
license: MIT
homepage: https://github.com/dongsheng123132/hermes-doctor
repository: https://github.com/dongsheng123132/hermes-doctor
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [hermes, troubleshoot, auth, deepseek, ops, doctor, credential-pool]
    related_skills: []
    last_synced_with_upstream: 2026-04-30
---

# Hermes Doctor — 故障诊断与抢救流程

## 何时触发本 skill

任一信号即触发:

- `HTTP 401: Authentication Fails`(尤其是 `your api key: ****xxx is invalid`)
- `Authorization: Bearer no-key-required` 之类**字面占位符**出现在请求 header(用 request_dump 看)
- `hermes setup` 不弹 API key 输入步骤,只显示绿色 ✓
- `/model` 切换 provider 后立刻 401/404
- `hermes doctor` 报红/黄
- `gateway already running` 启动失败
- WAL 文件 > 100MB

不要等用户描述清楚 — 看到上面任一症状立即载入 references/auth-troubleshooting.md。

## 第一原则:先确认 HERMES_HOME 在哪

**Windows 上最容易踩的坑**:`HERMES_HOME` 可能被 HKCU\Environment 重定向到非默认位置(比如 `C:\Users\<u>\AppData\Local\hermes`),而不是 `~/.hermes`。诊断和修复必须先确认真路径,否则你改的是无效文件:

```bash
echo "$HERMES_HOME"                              # shell 当前值
reg query "HKCU\Environment" /v HERMES_HOME      # 持久化值
hermes dump --redact | head -20                  # hermes 自己认的路径
```

三处不一致就以 hermes dump 输出的为准。Windows 上的常见场景:U-Hermes 等打包发行版会把 HERMES_HOME 写到 `%LOCALAPPDATA%\hermes`(即 `C:\Users\<USER>\AppData\Local\hermes`),让默认的 `~/.hermes` 变成空壳。如果你只改 `~/.hermes` 下的文件而 hermes 没反应,八成就是这种情况。

## 黄金 5 步排查

详见 templates/triage-checklist.md。摘要:

1. **定位真 HERMES_HOME**(上一节)
2. **跑 `hermes dump --redact`** — 看运行时 provider/key/active_profile/请求 URL/Authorization 的真实样子。这一步常常一眼定位问题。
3. **看最新 request_dump** — `<HERMES_HOME>/sessions/request_dump_*.json` 里的 `request.headers.Authorization` 和 `request.url` 是不是符合预期。如果 Authorization 是 `Bearer no-key-required` 或 `Bearer <字面单词>`,说明 key 注入失败,不是 key 本身的问题。
4. **排查 4 处残留点**(顺序很重要,从隐蔽到显眼):
   - HKCU\Environment 的 `HERMES_HOME`、`*_API_KEY`(`reg query "HKCU\Environment"`)
   - shell 进程环境(`echo "$DEEPSEEK_API_KEY"` 等)
   - `<HERMES_HOME>/auth.json` 的 `credential_pool.<provider>` 数组(**最容易缺**)
   - `<HERMES_HOME>/.env` 和 `<HERMES_HOME>/config.yaml`(顶层 model.api_key + model_profiles.*.api_key)
5. **备份后修复**(详见 references/auth-troubleshooting.md):
   - 永远先 `cp <file> <file>.broken-$(date +%Y%m%d-%H%M%S)`
   - 修完跑 `hermes doctor` 验证,启动 hermes 发 ping

## 常见症状速查表

| 症状 | 大概率根因 | 跳到 |
|---|---|---|
| `your api key: ****ired is invalid` | key 是字面 `expired` 或 `no-key-required` 占位符,没注入到 header | references/auth-troubleshooting.md |
| `Authorization: Bearer no-key-required` | credential_pool 缺该 provider 条目 | references/auth-troubleshooting.md §"占位符注入" |
| `hermes setup` 不弹 key 输入 | issue #16394:.env 里有该 KEY 行就静默跳过 | references/auth-troubleshooting.md §"setup 静默跳过" |
| `/model` 切完 404 | issue #3685:api_mode 残留 | references/provider-switch.md |
| `gateway already running` | lock 文件残留 | references/doctor-and-dump.md §gateway |
| WAL 巨大 | response_store/state 数据库未 checkpoint | `hermes doctor --fix` |
| 跨机迁移后全报错 | API key 没在新机重新填,base_url 错 | references/backup-and-migrate.md |

## 危险动作清单(执行前必须明确得到用户授权)

只要你打算做下面任一操作,先把动作和影响告诉用户、等他点头,再做:

- 删 `<HERMES_HOME>/.env` 任一行
- 改 `<HERMES_HOME>/auth.json` 的 credential_pool(可能会让另一些 provider 失联)
- 删 HKCU\Environment 的环境变量(影响所有应用,不只 hermes)
- 跑 `hermes doctor --fix`(会自动改 config 和 symlink)
- 删 sessions/ 或 state.db(无法恢复历史)
- 重新装 hermes-agent(venv 重建)

## 何时升级到人工

`hermes dump` 显示运行时 key 与 4 处残留点都对不上 → venv 损坏的可能性 > 90%,建议:

1. 备份整个 HERMES_HOME 到 zip
2. 卸载并重装 hermes-agent (`pipx reinstall hermes-agent` 或对应安装方式)
3. 重新跑 `hermes setup`
4. 把备份的 sessions/ memories/ skills/ 复制回新 HERMES_HOME

## 排查时优先翻这些地方

- 真 HERMES_HOME(用 `hermes dump --redact` 或 `reg query "HKCU\Environment" /v HERMES_HOME` 确认)
- Hermes Python 源码 — 诊断时直接读最准:
  - 标准 pip 安装:`<venv>/Lib/site-packages/hermes_cli/`(Win)或 `<venv>/lib/python*/site-packages/hermes_cli/`
  - 打包发行版(如 U-Hermes):`<install-root>/hermes-agent/hermes_cli/`
  - 关键文件:`auth.py`(provider 解析、PROVIDER_REGISTRY、`_resolve_api_key_provider_secret`)、`doctor.py`(`run_doctor`)、`setup.py`(setup wizard)、`env_loader.py`、`runtime_provider.py`
- Hermes CLI 二进制:venv 的 `Scripts/hermes.exe`(Win)或 `bin/hermes`(Mac/Linux)

## 修复手段优先级

故障定位后,优先用安全程度高的手段:

1. **`hermes auth` 子命令**(v2026.4.3+,推荐) — `hermes auth add/remove/list/reset`,见 references/credential-pool-and-rotation.md。先 `hermes auth --help` 看你装的版本支不支持
2. **`hermes doctor --fix`** — 修 stale config / WAL / symlink,不动 key
3. **手工 edit `.env` + `auth.json`** — `hermes auth` 不可用或版本太旧时(参 references/auth-troubleshooting.md)。**关键**:目前主流版本(0.10.x 及之前)的 `_resolve_api_key_provider_secret()` 只读 env,不读 credential_pool(issue #15914),所以 .env 和 auth.json 通常需要**双写**才稳定
4. **`hermes setup`** — 重跑全量 wizard,但 issue #16394 让它在 .env 已有 KEY 行时静默跳过,所以先删 .env 那行再跑
5. **重装 venv** — 升级到人工

## 详细资料

- `references/auth-troubleshooting.md` — 401/key 注入失败/setup 静默跳过的全套排查
- `references/credential-pool-and-rotation.md` — `hermes auth` 子命令、4 种 rotation 策略、池子坑(#15914/#5561/#6907/#7863)
- `references/fallback-and-rate-limit.md` — fallback_providers 链、429 cooldown、模型路由解析链(#15914/#16677)
- `references/doctor-and-dump.md` — `hermes doctor` 检查项 + `hermes dump` 用法
- `references/config-and-paths.md` — HERMES_HOME 解析、`<home>/` 下每个文件作用
- `references/provider-switch.md` — `/model` 切换、api_mode 陷阱、profile 配置
- `references/backup-and-migrate.md` — 备份恢复 HERMES_HOME,跨机迁移
- `templates/triage-checklist.md` — 出问题时按这张表逐条排
- `assets/known-issues.json` — 16 条已知 GitHub issues 结构化清单 + 6 个相关 release 摘要
