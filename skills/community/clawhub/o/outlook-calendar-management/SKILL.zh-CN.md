---
name: outlook-calendar-management
description: "View, find, add, update, move, and delete Outlook / Microsoft calendar events, including recurring events and free-time queries. Use when the user names Outlook calendar or the conversation already establishes it as the calendar to manage. Does not handle email or other calendar products."
license: "MIT"
metadata:
  version: 3.0.0
---

# Outlook 日历助手

管理已连接账户的默认 Outlook 日历。由模型结合用户语言和上下文理解意图，再向附带的 Python CLI 传入明确参数。后端负责日期与重复规则校验、时区转换和 Microsoft Graph 调用，不解析自然语言日期或重复规则。

## 运行入口

相对于本 skill 目录解析路径。使用可用的 Python 3.10+ 解释器（`python` 或 `python3`）：

```bash
python "<skill目录>/scripts/outlook_cal.py" context --json --lang zh
```

下文省略此前缀。优先使用 `--json`，JSON 字段名不随语言变化。中文对话加 `--lang zh`，其他语言加 `--lang en`；回复沿用用户语言。`--json`、`--lang`、`--timezone` 可放在任意子命令前或后。

首次连接或切换账户时读取 [configuration.zh-CN.md](references/configuration.zh-CN.md)，通过 `scripts/outlook_setup.py` 认证。需要隔离测试登录时，按配置文档设置独立的 `OCAL_TOKEN_PATH`，写入前核对目标账户。登录及日历命令会自动安装缺失的 requests/msal/tzdata。`context` 和 `date` 不访问日历、不登录、不安装依赖；地区时区需要系统时区数据或 tzdata。

## 执行前理解意图

- 解析相对日期时，若没有新鲜的当前时间与有效时区，先调用 `context --json`。返回 `now`、`today`、`timezone`、`utc_offset`、英文小写的 `weekday` 和本周一的 `week_start`。用户指定时区时使用 `context --timezone "Area/City" --json`。后续日历命令显式复用该时区名称；仅有 UTC 偏移无法描述夏令时规则。
- 用 `date --base YYYY-MM-DD --days N --json` 或 Python `datetime`/`calendar` 运算得到具体日期。日期工具按有符号天数计算，不读取时钟。本周五是 `context.week_start` 加 4 天，下周一加 7 天。结合上下文消除歧义，只询问影响本次操作的缺失信息。
- 日历输入只接受补零的 `YYYY-MM-DD`、`YYYY-MM-DD HH:MM`、`YYYY-MM-DDTHH:MM`；纯日期参数不接受时刻，时区单独传入。创建时段日程必须给出开始和结束；全天日程必须指定 `--all-day`。不要擅自填充时长，也不要把缺少时刻解释成全天。
- 写入前保留解析后的目标、绝对日期时间、时区和待修改字段。验证及重试复用这些明确值，即使跨过午夜也不重新解释原始相对表达。

## 选择并执行操作

| 任务 | 命令 |
|---|---|
| 某天或某段日期的日程 | `list --from YYYY-MM-DD --days N --json` |
| 在上述范围筛选 | 加 `--search "词"`、`--category "类别"` 或 `--reminders` |
| 某段日期内创建的日程 | `list --created-after YYYY-MM-DD --created-before YYYY-MM-DD --json` |
| 详情 / 定期日程下次出现 | `read <ID>` / `next <ID>` |
| 创建 / 修改 / 移动 / 删除 | `add` / `update` / `move` / `delete` |
| 空闲时段 / 连接状态 | `free YYYY-MM-DD --from HH:MM --to HH:MM` / `status` |

`list` 必须明确给出 `--from` 或 `--created-after`。`--days N` 覆盖 N 个自然日，在最后一天的次日零点结束且不包含该边界。创建时间筛选独立于日程发生日期，`--created-before` 为不包含的上界。查询安排未指定范围时，可先从 `context.today` 起查七天，汇报时说明范围。`--summary` 只有每天数量，需要标题和时间时使用普通 JSON 列表。

ID 使用返回的 `id` 和 `seriesMasterId`。修改、删除前用 `read` 获取相关现有字段，或复用新鲜完整的结果。多匹配时消除歧义，区分定期日程单次与整系列。已对明确对象与范围给出的授权继续有效，`--json`/`-y` 仅跳过 CLI 交互。识别对象后优先使用明确 ID；`--search` 只是带固定搜索范围的便利功能。

写入后回读一次，核对用户要求改变的字段；删除后查询相关范围确认目标已不存在。按实际结果汇报前后值。写入结果不明时先检查服务端状态，再决定是否重发已固定的请求；验证失败不等于写入失败。临时只读故障可重试一次；认证或权限问题用 `status` 和 [troubleshooting.zh-CN.md](references/troubleshooting.zh-CN.md) 排查。恢复失败时说明尚未解决的部分。

## 规范化示例

以下日期是假设值：`context` 返回 **2026-09-09、Asia/Shanghai**，`week_start` 为 **2026-09-07**。实际操作从当前上下文计算，不能照抄示例日期。

- **“我昨天加的那件事，改到今天。”** 用 `date --base 2026-09-09 --days -1 --json` 计算昨天。通过 `list --created-after 2026-09-08 --created-before 2026-09-09 --timezone Asia/Shanghai --json` 找候选，识别目标后执行 `move <ID> --to 2026-09-09 --timezone Asia/Shanghai --json`。原定发生日期可能在未来，不能按创建日期推断移动天数。
- **“加一个本周五 15:00 的半小时会议，提前十分钟提醒。”** 用 `date --base 2026-09-07 --days 4 --json` 算出周五，再执行 `add "会议" "2026-09-11 15:00" "2026-09-11 15:30" --remind 10 --timezone Asia/Shanghai --json`。
- **“本周五 14:00 到 17:00 有空吗？”** 同样计算周五后执行 `free 2026-09-11 --from 14:00 --to 17:00 --timezone Asia/Shanghai --json`。
- **“把每周例会改成周三。”** 先明确单次或系列范围。修改系列规则时读取 [recurring-events.zh-CN.md](references/recurring-events.zh-CN.md)，构造 Graph pattern JSON 文件，再执行 `update <seriesMasterId> --repeat-file <规则文件> --timezone <已确定时区> --json`。保留或按用户意图改变原有结束条件；执行已授权的系列变更前说明对例外日程的影响。

## 输出与参考

JSON 操作模式下，stdout 只有一个 JSON 值，诊断信息走 stderr。检查退出码：错误为 `{"error": ..., "exit": 1}`；`status` 未连接时返回含 `connected: false` 的连接状态对象。`--help` 仍为文本。解析 JSON 后使用字段，包括已还原的 Unicode 字符。空闲查询使用 JSON，因为人类输出没有时段列表时，可能表示全空闲或全忙碌。

| 何时读取 | 文档 |
|---|---|
| 参数、明确时间格式、提醒、查询边界或 JSON 结构 | [commands.zh-CN.md](references/commands.zh-CN.md) |
| 重复规则字段、结束条件、单次出现或整个系列 | [recurring-events.zh-CN.md](references/recurring-events.zh-CN.md) |
| 连接、切换账户或 Azure 应用配置 | [configuration.zh-CN.md](references/configuration.zh-CN.md) |
| 认证、安装、时区错误或异常结果 | [troubleshooting.zh-CN.md](references/troubleshooting.zh-CN.md) |

时段日程使用选定的有效时区。全天日程尽量按邮箱时区写入，不可用时回退到有效时区，以保持 Outlook 中的日历日期。时区或权限不一致时先排查，再决定是否重复写入。
