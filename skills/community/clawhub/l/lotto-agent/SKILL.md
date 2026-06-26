# lotto-agent 彩票 Agent Skill

**优先级最高**：消息里出现 彩票 / 双色球 / 大乐透 / 七星彩 / 七乐彩 / 福彩3D / 排列三 / 排列五 / 快乐8 / 选号 / 开奖 / 兑奖 / 中奖 / 期号 / 奖池 / 奖金 / 报表 / 盈亏 / 推荐号码 / 买彩票 / 给我X注 等任意词汇时，立即调用本 Skill，不要让通用聊天回答。

**未来时间词铁律**：消息里只要出现 今晚 / 明天 / 后天 / 周X / X月X日 / 早上 / 上午 / 下午 / 晚上 / X点 等任意未来时间表达，必须走 `create_task`，**不允许** `generate` 立即出号。唯一例外：用户**显式**说"现在 / 立刻 / 马上 / 立即 / 直接给"等立即字样。

**反问优先于猜**：日期或时段缺一半时（"明天给我5注"、"早上给我5注"、"周三给我5注"等），先调 `parse --text "<原文>"`，按返回的 `needs_clarification=true` 反问用户补全，**禁止**默认填 09:00 / 今天 / 这周等任何值。

调 `generate` 时**必须**把用户原话作为 `--text` 传入，Python 入口会做二次校验，原话含未来时间词且无立即字样时直接返回反问 payload。

本 Skill 是私人自用彩票 Agent。不承诺中奖、不做预测、不使用"必中 / 稳赚"等表达。大模型只负责理解意图、调用脚本、组织输出；选号 / 开奖抓取 / 兑奖判断 / 数据存储全部由 Python 规则代码完成。

## 入口

```bash
python scripts/cli.py <action> [options]
```

支持 13 个 action：

| action | 说明 |
|---|---|
| `status` | 健康检查 + 数据库路径 |
| `generate` | 选号入库（自动绑定下一期） |
| `check_prize` | 兑奖（按已 fetch 的开奖匹配） |
| `fetch_draw` | 抓取公共开奖数据（all / 指定彩种 / 指定期） |
| `report` | 报表 `--since N` 默认 30 天 |
| `cancel` | 取消最近 N 注（不计成本、不参与兑奖） |
| `record` | 手动录入号码（格式 `01 05 12 18 25 31 + 09`） |
| `create_task` | 创建自动任务 |
| `list_tasks` | 列出自动任务 |
| `disable_task` | 停用任务 |
| `cron_run` | cron 入口（每 30 分钟调一次） |
| `setup_notify` | 配置并开启 OpenClaw 推送 |
| `parse` | NL 解析 → action+params |

## 自然语言意图映射

**强烈推荐**：所有彩票相关的中文自然语句都先 `parse --text "<原文>"` 让规则识别 action 再分派，避免大模型自己挑错 action。

```bash
python scripts/cli.py parse --text "明天早上给我5注双色球"
# -> {action: create_task, params: {schedule_kind: once, schedule_spec: <tomorrow>, ...}}

python scripts/cli.py parse --text "明天给我5注大乐透"
# -> {needs_clarification: true, message_text: "那一天什么时候给你？早上、上午、中午、下午还是晚上？..."}

python scripts/cli.py parse --text "现在给我5注双色球"
# -> {action: generate, params: {...}}
```

`needs_clarification=true` 时，**不要**自己补默认值后继续；把 `message_text` 抛给用户、等回复、再重跑 `parse`。

常见映射示例：

- "给我5注大乐透 2倍 追加" → `generate --lottery dlt --count 5 --multiple 2 --additional --text "<原文>"`
- "现在给我5注双色球" → `generate --lottery ssq --count 5 --text "<原文>"`（含立即字样豁免）
- "今天下午给我5注大乐透" → `create_task --task-action generate --schedule-kind once --schedule-spec <today> --time-start 12:00 --time-end 18:00 --random-window`
- "今晚给我5注双色球" → `create_task --task-action generate --schedule-kind once --schedule-spec <today> --time-start 18:00 --time-end 23:30 --random-window`
- "明天早上给我5注双色球" → 同上，`schedule-spec <tomorrow>`，时段 07:00-12:00
- "明天上午10点给我5注快乐8选十" → `create_task --task-action generate --schedule-kind once --schedule-spec <tomorrow> --time-start 10:00 --time-end 10:00`（fixed）
- "5月15日上午给我5注大乐透" → `create_task --schedule-kind once --schedule-spec 2026-05-15 --time-start 07:00 --time-end 12:00 --random-window`
- "以后每天早上9点给我大乐透5注" → `create_task --task-action generate --schedule-kind daily --time-start 09:00`
- "每周二四六晚上8点给我双色球3注" → `create_task --schedule-kind weekly --schedule-spec 2,4,6 --time-start 20:00`
- "大乐透开奖那天早上给我5注" → `create_task --schedule-kind draw_day --schedule-spec dlt:0 --time-start 07:00 --time-end 12:00 --random-window`
- "双色球开奖前一天晚上给我3注" → `create_task --schedule-kind draw_day --schedule-spec ssq:-1 --time-start 18:00 --time-end 23:30 --random-window`
- "每期开奖后自动兑奖并告诉我" → `create_task --task-action draw_check_prize --schedule-kind draw_day --schedule-spec all:0 --time-start 21:35 --time-end 23:55`
- "今天中了没 / 帮我查一下今天中了没有" → `create_task` 否；直接 `fetch_draw` + `check_prize` 同时跑（或调 `cron_run` 走 `draw_check_prize` 路径）
- "本周/周报盈亏" → `report --since 7`，"本月/月报" → `report --since 30`
- "查看自动任务" → `list_tasks`
- "停用 #3 任务" → `disable_task --task-id 3`
- "我买了大乐透 01 05 12 18 30 + 02 09" → `record --lottery dlt --text "<原文>"`
- "取消刚才的5注" → `cancel --limit 5`
- "绑定通知 / 以后发到这里" → `setup_notify --channel <宿主> --chat-id <chat> [--account-id <acc>] --confirm`

## 消息输出要求

`generate` / `record` 必须返回**两条独立的聊天气泡**：

1. **第一条**只放号码块（`numbers_message` / `message_text` 都是这块），不能掺杂任何免责、跟踪、自动化、寒暄、推送状态。
2. **第二条**才发送 `followup_messages` 里的轻提示（顺延、推送未开启等）。

号码消息的标准格式：

```
彩种｜N注｜M倍｜追加（仅 dlt 追加）｜开奖 YYYY-MM-DD
投入：X元

号码1
号码2
...
```

数字之间两个空格，分区用 ` + `。每注号码前不显示序号。

## 选号绑定 / 开奖窗口

`generate` 自动绑定下一期：先看本地 `draws` 表里最近一期的 `next_issue` / `next_buy_end_time`；如果当前时间已过 `next_buy_end_time`，回退到周历的下一次开奖日，期号留空，按开奖日匹配兑奖。

公共仓库（`lottery-data-repo`）可能在开奖前 1-2 小时就推占位/重复数据，凌晨重抓才完整 —— 所以 `next_buy_end_time` 比 `next_issue` 更可信。

兑奖类任务（`check_prize` / `draw_check_prize`）判断"今天是不是开奖日"时直接看公共开奖日历（本地 `draws` 表里有当天 draw_date 即开奖日），不能用 `next_fallback`（它会因为 now > buy_end 跳过今天）。

默认配置开启 21:35-23:55 的开奖检测窗口：建一个 `create_task --task-action draw_check_prize --schedule-kind daily --time-start 21:35 --time-end 23:55` 即可，cron 每 30 分钟检查一次直到抓到当期开奖。

## 自动化规则

业务任务写入 SQLite `tasks`；服务器只需一条统一 cron 唤醒：

```bash
*/30 * * * * cd /root/.openclaw/workspace/skills/lotto-agent && python3 scripts/cli.py cron_run --push
```

时间窗口三档（自然语言映射时用）：

- 早上/上午 → 07:00-12:00 random
- 中午 → 11:00-13:00 random
- 下午 → 12:00-18:00 random
- 晚上/今晚/明晚 → 18:00-23:30 random
- 用户明确说"X点几分" → fixed

模糊表达（"有空的时候、看情况、差不多的时候、晚点"）必须反问，不允许默认。

`schedule_kind` 4 种：`once` / `daily` / `weekly` / `draw_day`。`schedule_spec` 含义：
- `once`：`YYYY-MM-DD`
- `weekly`：逗号分隔的 ISO 周几号 `1,3,5`
- `draw_day`：`<lottery>:<offset>`，offset=0 当天，-1 前一天

一次性任务允许"补跑"：cron 30 分钟粒度可能错过精确时间，只要 `last_run_key` 没设置、当前已过 `time_start`（或随机窗口的 `planned_run_time`），当天剩余时间里下一次 cron 会触发，避免错过即失效。

## 推送

仅支持 OpenClaw CLI（`openclaw message send`）。配置在 `config/config.json` 的 `notify` 段。`setup_notify --channel X --chat-id Y --confirm` 一步配完。

固定调用 PATH 里解析到的 `openclaw` 可执行文件，不允许自定义命令路径，避免命令注入。

## 数据 / 配置位置

- 数据库：默认 `~/.openclaw/workspace/lotto-agent-data/lottery.db`，可用 `LOTTO_AGENT_DATA_DIR` 环境变量覆盖。
- 公共开奖源：默认 `https://raw.githubusercontent.com/wenjinliuu/lottery-data-repo/main/public_data`，可用 `LOTTERY_PUBLIC_DATA_BASE_URL` 覆盖。
- 配置：`config/rules.json`（彩种规则，不要手改）+ `config/config.json`（推送 + 默认偏好）。
