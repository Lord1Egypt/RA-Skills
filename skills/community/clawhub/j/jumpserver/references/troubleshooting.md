# 故障排查

## 快速概览

- 优先按“判断当前是首次全量还是后续轻量 -> 环境 -> 连通性 -> 组织 -> 对象解析 -> 能力查询”的顺序排查。
- 环境与入口问题看 [runtime.md](runtime.md)；资源与标准流程看 [assets.md](assets.md)；治理和调查能力看 [capabilities.md](capabilities.md)。
- 所有正式入口都在 `scripts/jumpserver_api/` 下，不使用 SDK 临时脚本路径。

## 报错速查

| 报错文本 | 常见原因 | 优先动作 |
|---|---|---|
| `python3: command not found` / 无可用 Python 3 | 本机未安装 Python 3，或命令名不对 | 回到 [runtime.md](runtime.md) 的 Python 3 检查 |
| `No module named requests` / `Automatic dependency installation failed.` | 当前解释器环境缺依赖、pip 不可用、无网络，或自动安装失败 | 优先查看自动安装错误明细；必要时执行 `python3 -m pip install -r requirements.txt` |
| `.env` 缺失，或 `JMS_API_URL is required.` | 本地配置未初始化，或地址变量没配置 | 先执行 `python3 scripts/jumpserver_api/jms_diagnose.py config-status --json` |
| `API credential is required.` / 认证凭据缺失 | 未提供完整的 AK/SK 或用户名密码 | 补齐 `JMS_ACCESS_KEY_ID/JMS_ACCESS_KEY_SECRET` 或 `JMS_USERNAME/JMS_PASSWORD` 中至少一组 |
| `Unable to determine the effective organization.` | 未选组织，且当前环境不能自动代选组织 | 先执行 `python3 scripts/jumpserver_api/jms_diagnose.py select-org --org-id <org-id> --confirm` |
| `Unknown capability` | `--capability` 拼写错误，或当前版本未实现 | 先执行 `... capabilities` 查看能力目录 |
| `Invalid JSON payload` / `JSON payload must be an object.` | `--filters` 不是合法 JSON 对象 | 检查引号、逗号和花括号 |
| `Asset permission API is unavailable or not yet confirmed ...` | 当前环境未开放权限接口，或权限不足 | 记录为接口待确认，先做替代性只读验证 |
| `object_does_not_exist` / `404` | ID 错误、组织错误或对象不存在 | 先重新 `list/get/resolve` |
| “帮我创建/更新/删除/解锁/授权” 被拒绝 | 本仓库不提供对象或权限写操作 | 说明边界，并回到只读查询或能力分析路径 |

## 轻量失败后的升级动作

| 轻量校验失败点 | 升级动作 |
|---|---|
| `config-status --json` 显示 `complete=false` | 回到 [runtime.md](runtime.md) 补环境 |
| `ping` 失败 | 重新执行完整预检，确认 URL、认证凭据（AK/SK 或用户名密码）、TLS、组织 |
| `select-org` 返回候选组织但未确定 | 明确组织后再继续业务命令 |
| `inspect/analyze` 返回空结果 | 先检查时间范围，再检查对象过滤条件 |

## 最小排查流程

```text
判断当前是首次全量失败还是后续轻量失败
  -> 若为轻量失败，先升级到全量校验
  -> 检查 Python 3 与自动依赖安装结果
  -> 执行 config-status --json
  -> 检查 .env / shell 环境变量
  -> jms_diagnose.py ping
  -> 选择组织 select-org
  -> 精确解析对象 resolve / list / get
  -> 再执行 inspect / analyze / list / get
```

## 常见误用

| 误用 | 正确做法 |
|---|---|
| 为标准流程写临时 SDK Python 文件 | 回到正式 `scripts/jumpserver_api/jms_*.py` |
| 用模糊名称直接推断对象 | 先解析为精确对象或 ID |
| 查调查类问题却只调用单个 `list` 接口 | 优先用 `analyze --capability ...` |
| 查治理类问题却手工拼接多个读取命令 | 优先用 `inspect --capability ...` |
| 未指定时间范围就认定“没有历史数据” | 先显式传 `date_from/date_to` |
| 想在本仓库上直接做写操作 | 先说明本仓库不提供对象或权限写操作 |
