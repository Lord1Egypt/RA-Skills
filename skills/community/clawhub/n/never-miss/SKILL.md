---
name: never-miss
display_name: 不错过
display_name_en: Never Miss
version: "1.0.0"
description: 把一句话、截图或邮件中的日程与截止事项写入 macOS 系统日历并设置提醒，支持多邮箱定时扫描与跨账户去重。当用户说"提醒我/帮我记一下/安排一下"、提到会议或截止时间（deadline/DDL/截止）、要配置邮箱日程提醒、查询最近建的提醒或运行状态时使用。
description_zh: 把一句话、截图或邮件中的日程与截止事项，写入 macOS 系统日历并自动设置提醒；支持多邮箱定时扫描、跨账户去重与 .ics 会议邀请解析。
description_en: Turn schedules and deadlines from chat, screenshots, or email into macOS Calendar events with reminders; supports multi-account IMAP scanning, cross-account deduplication, and .ics invitation parsing.
compatibility: macOS with Calendar.app and AppleScript (osascript); Python 3.9+ stdlib only; IMAPS-capable mail accounts; host scheduler required for daily auto-scan. Non-macOS degrades to .ics file output only.
metadata:
  data-dir: ~/.workbuddy/never-miss
  keychain-service: never-miss-imap
---

# never-miss（不错过）

把散落在口述、截图、邮件里的日程与截止事项，变成 macOS 系统日历里**带提醒的事件**；提醒由操作系统负责，写入后不再依赖本 Skill 是否在线。

## 1. 模式判定（先判断当前属于哪种模式）

| 模式 | 判定信号 | 下一步 |
|---|---|---|
| ①交互建提醒 | 用户消息含日程意图（提醒我/记一下/安排/会议/截止…），含口述或截图 | 走 §3 |
| ②自动扫描 | 宿主注入哨兵提示 `【never-miss:auto-run】` | 读 `references/runbook-auto.md` |
| ③查询 | "建了哪些提醒/今天有什么/本周日程/运行状态" | 走 §6 |
| ④配置维护 | "配置日程提醒/再配一个邮箱/删账户/停用账户" | 走 §7 |

## 2. 铁律（不可妥协）

1. 相对时间换算前**必须先执行 `now`** 取锚点；换算结果必须写进回复明示（NFR-01）
2. 缺字段如实标"未提供"，**禁止编造**时间与参与者（FR-13）
3. 缺开始时间 / 时间歧义：交互模式**追问**，自动模式**跳过**（FR-21/22/24/25）
4. 创建成功**必须复述完整详情**，时间用绝对日期时间（如"9月5日（周六）15:00"）
5. 任何失败不静默；按错误码给修复指引或上报（FR-30）
6. 密码只经 stdin 入 Keychain，任何输出打码；配置与日志不留明文（FR-03）

## 3. 交互建提醒流程

1. `now` 取时间锚点
2. 提取字段并换算（规则见 `references/extraction-rules.md`，含 deadline 识别与全天判定）
3. 缺开始时间 / 时间歧义 → 追问；低置信度 → 追问
4. 冲突检查：`check-conflict --start <ISO> --end <ISO>`；有冲突则告知用户决定（改期/照建/放弃）
5. 构建 Event JSON（见 §5）→ 经 stdin 传给 `create`
6. 按输出复述详情；`status:"ics_fallback"` 时提示用户双击导入 `.ics`；`duplicate` 时说明已存在

## 4. 命令速查

数据目录：`NEVER_MISS_DATA` 环境变量 > 默认 `~/.workbuddy/never-miss`。所有命令用 `python3 scripts/never_miss.py <cmd>`，输出结构化 JSON。

| 命令 | 用途 |
|---|---|
| `now` | 时间锚点（换算前置） |
| `init` | 生成 config.yaml 与 state.json |
| `secret set/check/delete <邮箱>` | Keychain 读写删（set 的密码经 stdin） |
| `doctor [--write-test]` | 逐账户自检（配置/时区/Keychain/IMAP/日历） |
| `create [--journal]` | 建日历事件（Event JSON 经 stdin；自动模式加 --journal） |
| `check-conflict --start --end` | 查时间冲突 |
| `mail list/read` | 交互式看/读邮件（FR-09） |
| `scan fetch/commit` | 自动扫描：取信（游标不动）/ 推进游标 |
| `journal skip/error` | 补记跳过/失败（自动模式） |
| `query events/status` | 只读查询（最近 N 天 / 时间范围 / 运行状态） |

错误码：`E_ARGS` `E_CONFIG` `E_KEYCHAIN` `E_IMAP` `E_CALENDAR` `E_AUTH` `E_UNSUPPORTED` `E_STATE` `E_INTERNAL`。对照处置见 `references/troubleshooting.md`。

## 5. Event JSON 契约（create 的 stdin）

```json
{
  "title": "项目评审",
  "start": "2026-09-12T10:00:00+08:00",
  "end": "2026-09-12T11:00:00+08:00",
  "all_day": false,
  "location": "会议室A",
  "attendees": ["张三"],
  "reminder_lead_minutes": 60,
  "source": {"account": "me@example.com", "mail_subject": "评审通知", "mail_uid": 48213}
}
```

- `title`、`start` 必需；`end` 可省略（普通事件默认 +1h，全天事件默认单日）
- 全天事件：`all_day:true` 且 `start` 用 `YYYY-MM-DD`
- `source`：邮件来源必填（account/mail_subject/mail_uid）；对话来源可省略

`create` 返回：`status` ∈ `created|duplicate|ics_fallback`，另有 `uid`、`conflicts`、`ics_path`、`event`（回显）。

## 6. 查询（只读）

- 最近 N 天建的提醒：`query events --created-days N`（默认 7）→ 倒序表格（主题/时间/来源账户/来源邮件主题）
- 某时间段日程：`query events --from YYYY-MM-DD --to YYYY-MM-DD`
- 运行状态：`query status`（上次运行、各账户游标、新建/跳过/失败、待汇报标记）
- 空结果明确回复"没有"

## 7. 配置维护

1. 对话式收集账户必填项（host/username/label）；各家"专用密码"获取见 `references/mail-setup.md`
2. 写 config.yaml（不含密码）+ `secret set <邮箱>`（stdin 传密码）
3. `doctor --write-test` 逐项汇报；提示宿主注册每天 `schedule.time` 定时任务
4. 追加/停用/删除账户 = 改 YAML；删除时提示是否清理 Keychain

## 8. 引用（按需加载）

- 提取规则（字段/时间换算/置信度/deadline）：`references/extraction-rules.md`
- 自动模式完整流程：`references/runbook-auto.md`
- 邮箱专用密码指引：`references/mail-setup.md`
- 错误码处置：`references/troubleshooting.md`
