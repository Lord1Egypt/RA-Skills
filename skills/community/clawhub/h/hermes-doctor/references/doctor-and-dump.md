# `hermes doctor` & `hermes dump` 用法

## hermes doctor

源码:`hermes_cli/doctor.py`(在 venv 的 site-packages 下,或 U-Hermes 等打包发行版的 `<install-root>/hermes-agent/hermes_cli/doctor.py`)。

**做什么**:检查 Hermes 安装、配置、依赖、服务状态。`--fix` 自动修可修项。

```bash
hermes doctor          # 只看
hermes doctor --fix    # 看 + 自动修
```

**实际检查项**(基于 `run_doctor` 函数):

| 检查 | 是什么 | --fix 能修? |
|---|---|---|
| Python 版本 | 是否 ≥ 推荐版本 | ❌ |
| 依赖包 | 必装包是否在 venv 里 | ❌ 给出 install 命令 |
| `<home>/config.yaml` 旧版字段迁移 | provider/base_url 在 root,该挪到 model.* | ✅ |
| Stale root-level provider/base_url | 同上残留 | ✅ |
| WAL 文件大小 | response_store/state 的 -wal > 阈值 | ✅ checkpoint |
| `bin/hermes` symlink | Linux/Mac:符号链是否完好 | ✅ 重建 |
| `bin/` 目录 | 是否存在 | ✅ |
| Gateway service linger(systemd) | Linux | ❌ |
| API key 是否配置 | 至少一个 provider 有可用凭证 | ❌ 跑 `hermes setup` |
| Honcho(后台进程管理器) | 是否启动 | ❌ |
| Tirith 安装失败标记 | `.tirith-install-failed` | ❌ |
| 工具可用性 | `node`/`bash`/`curl` 等 | ❌ |

**`--fix` 不能修的**:
- API key 错误/过期(必须人工填)
- credential_pool 缺失(`hermes-doctor` skill 的 auth-troubleshooting.md 处理)
- HKCU\Environment 错误(Windows 必须人工 `reg delete`)
- venv 损坏(必须重装)

**输出色码**:
- 绿 `[ ok ]` 通过
- 黄 `[warn]` 不影响功能但建议处理
- 红 `[fail]` 必须修

## hermes dump

**做什么**:输出运行时实际状态的脱敏快照,用于:
- 调试 "为啥这把 key 不生效" — 直接看 dump 里 active provider 用的是哪个 source
- 提 GitHub issue / 群里求助 — 自动 redact API key,可放心贴

```bash
hermes dump              # 完整 dump
hermes dump --redact     # 强制脱敏(默认就脱敏,显式声明更安全)
hermes dump | head -40   # 只看前面的 provider/key 部分
```

**dump 包含**:
- `HERMES_HOME`(实际路径,不是默认)
- 当前 active provider 和 model
- credential_pool 各 provider 的状态(脱敏 key + last_status + 错误)
- config.yaml 关键字段
- 依赖版本
- 平台 / 系统

**最有用的诊断信号**:
- `credential_pool.<provider>` 是空数组 → 类型 1 占位符注入(参 auth-troubleshooting.md)
- `last_status: 401` + `last_error_code: invalid_request_error` → key 真过期,去服务商续
- HERMES_HOME 与你预期不一致 → 你改的可能是错文件

## 常见 doctor 报错快速对应

| 报错关键字 | 跳到 |
|---|---|
| "Run 'hermes doctor --fix' or 'hermes setup' to migrate config" | 直接跑 `hermes doctor --fix` |
| "Stale root-level provider/base_url in config.yaml" | 同上 |
| "Large WAL file" | 同上(checkpoint) |
| "Broken symlink at .../hermes" | 同上(重建)|
| "Missing .../hermes symlink" | 同上 |
| "Gateway already running" | `rm -f $TEMP/openclaw/gateway.*.lock` 后重试 |
| "Tirith install failed" | 删 `<home>/.tirith-install-failed` 后重试,或忽略(只是命令扫描器降级) |
| "API key not configured for X" | `hermes setup` 或参 auth-troubleshooting.md 直接补 auth.json |
