🌐 [English](README.md) | 中文

<p align="center">
  <img src="./icon/appIcon.png" alt="App Logo" width="20%">
</p>

# Outlook 日历助手

通过与 AI 助手对话管理 Outlook 日历。模型负责理解请求，本地 Python CLI 校验明确参数并调用 Microsoft Graph。支持个人 outlook.com 和 Microsoft 365 账户、定期日程、提醒、空闲查询以及中英文输出，无需 MCP 服务或后台常驻进程。

**3.0.0** 将语言理解与执行分开：CLI 只接受绝对日期和结构化重复规则。本地 `context`、`date` 工具提供当前时钟/时区和确定的日期运算，让模型在写入前确定请求，并在重试时复用相同参数。

## 快速开始

将完整项目目录放入 Agent 的 skill 目录，或用 Python 3.10+ 直接运行。[SKILL.zh-CN.md](SKILL.zh-CN.md) 是中文 Agent 入口。

```bash
# 本地工具：不访问日历，不要求登录。
python scripts/outlook_cal.py context --timezone Asia/Shanghai --json
python scripts/outlook_cal.py date --base 2026-09-07 --days 4 --json

# 日历命令先登录，按提示完成设备码认证。
python scripts/outlook_setup.py

# 日期仅为示例，请替换为实际需要的绝对日期。
python scripts/outlook_cal.py list --from 2026-09-09 --days 7 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py add "计划讨论" "2026-09-11 15:00" "2026-09-11 15:30" --remind 10 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py free 2026-09-11 --from 14:00 --to 17:00 --timezone Asia/Shanghai --json
```

登录及日历命令会自动安装缺失的 `requests`、`msal`、`tzdata`。离线工具不安装依赖；地区时区数据不可用时，用同一解释器运行 `python -m pip install tzdata`。设备码登录将凭据存放在 `~/.outlook_cal_token.json`，工具在可能时自动续期。账户与 Azure 应用设置见[连接配置](references/configuration.zh-CN.md)。

## 分工

| 模型 | Python 后端 |
|---|---|
| 结合对话理解相对日期和自然语言 | 提供当前时钟/时区，按明确偏移计算日期 |
| 识别日程、修改字段、单次/系列范围 | 校验操作参数、日期格式、时间范围、重复结构 |
| 消除影响操作的歧义，复用已有授权 | 处理时区转换和全天日期边界 |
| 固定绝对参数并在重试时复用 | 认证、接口分页、按规则重试、返回 JSON |
| 核实用户要求的结果并准确汇报 | 返回服务端数据和结构化错误 |

例如，用户仍可说“本周五 14:00 到 17:00 有空吗”。模型读取 `context`，在周一 `week_start` 上加四天，再将计算出的日期传给 `free`；后端本身拒绝 `本周五`、`今天下午2点` 等字符串。

## 明确的命令契约

- 日期格式为 `YYYY-MM-DD`，带时刻为 `YYYY-MM-DD HH:MM` 或 `YYYY-MM-DDTHH:MM`，各字段补零。时区通过单独的 `--timezone` 指定 IANA 或 Windows 名称，不指定则自动探测。
- `list` 必须给 `--from` 或创建日期筛选，`free` 必须给日期。已移除 `today`/`tomorrow`/`week` 命令及 `--past`。
- 创建时段日程必须给开始和结束，全天日程必须加 `--all-day`。两种类型之间转换必须明确开始与结束。
- 重复规则通过 `--repeat` 或 `--repeat-file` 传 Graph pattern JSON 对象，不再解析自然语言。文件形式可避开 shell 引号转义问题。
- `--json` 使 stdout 只有一个 JSON 值，警告和诊断信息走 stderr；解析 JSON 后恢复 Unicode。`--lang zh|en` 改变人类提示，不改变字段名。
- 时段操作使用有效时区。全天日程尽量按邮箱时区写入，不可用时使用有效时区，以保留 Outlook 中的日历日期含义。

完整参数见[命令参考](references/commands.zh-CN.md)和[定期日程指南](references/recurring-events.zh-CN.md)，实现边界和离线测试见 [DEVELOPMENT.zh-CN.md](DEVELOPMENT.zh-CN.md)。
