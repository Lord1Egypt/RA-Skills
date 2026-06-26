# lotto-agent

私人自用的彩票 Agent Skill，运行在 OpenClaw / 自定义宿主 / 命令行下。支持 8 个彩种的 Crypto 级随机选号、规则兑奖、定时任务、报表。

> **触发**：消息含彩票相关词时宿主必须立即调用本 Skill。
>
> **未来时间词铁律**：含"明天 / 后天 / 周X / X月X日 / 早上 / 下午 / 晚上 / X点"等任意未来时间表达 → 必须 `create_task`，不允许 `generate` 立即出号；只有"现在 / 立刻 / 马上"等立即字样才能 `generate`。Python 入口会做二次校验。
>
> **反问优先于猜**：日期或时段缺一半时，先 `parse --text "<原文>"` 让规则给出反问，禁止默认填值。

## 支持彩种

双色球 / 大乐透 / 七星彩 / 七乐彩 / 福彩3D / 排列三 / 排列五 / 快乐8

## 项目结构

```
lotto-agent/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── cli.py        # CLI 入口 + 13 个 action
│   ├── lotto.py      # 选号 + 兑奖 + 报表 + 录入
│   ├── fetch.py      # GitHub 抓取 + 开奖日历
│   ├── nl.py         # NL 解析 + 反问 + guard
│   ├── schedule.py   # 自动任务 + cron + 推送
│   └── store.py      # SQLite schema + CRUD
└── config/
    ├── rules.json    # 8 彩种生成 + 兑奖规则
    └── config.json   # 推送目标 + API URL + 默认偏好
```

## 部署

```bash
pip install -r requirements.txt
python scripts/cli.py status
```

数据库默认在 `~/.openclaw/workspace/lotto-agent-data/lottery.db`，可用 `LOTTO_AGENT_DATA_DIR` 环境变量覆盖。

公共开奖数据源默认指向 `lottery-data-repo`，可用 `LOTTERY_PUBLIC_DATA_BASE_URL` 覆盖。

## 常用命令

```bash
python scripts/cli.py generate --lottery dlt --count 5 --multiple 2 --text "给我5注大乐透2倍"
python scripts/cli.py fetch_draw --lottery all --message-text
python scripts/cli.py check_prize --message-text
python scripts/cli.py report --since 7 --message-text         # 周报
python scripts/cli.py report --since 30 --message-text        # 月报
python scripts/cli.py cancel --limit 5
python scripts/cli.py record --lottery dlt --text "01 05 12 18 30 + 02 09" --multiple 2 --additional
python scripts/cli.py parse --text "明天早上给我5注双色球"
python scripts/cli.py create_task --task-action generate --schedule-kind once --schedule-spec 2026-05-15 --time-start 07:00 --time-end 12:00 --random-window --params '{"lottery":"ssq","count":5}'
python scripts/cli.py list_tasks --message-text
python scripts/cli.py disable_task --task-id 3
python scripts/cli.py setup_notify --channel openclaw-weixin --chat-id <chat> --account-id <acc> --confirm
python scripts/cli.py cron_run --push
```

## 自动化 cron

服务器加一条：

```bash
*/30 * * * * cd /root/.openclaw/workspace/skills/lotto-agent && python3 scripts/cli.py cron_run --push
```

`tasks` 表里的所有 enabled 任务到点都会自动跑。一次性任务支持"补跑"（cron 错过精确时间也能在当天剩余时间触发）。

## 选号绑定逻辑

1. 先看本地 `draws` 表里最近一期的 `next_issue` + `next_buy_end_time`
2. 如果当前时间 ≤ `next_buy_end_time`：绑定到 `next_issue`
3. 否则：丢弃 latest 的下期信息，按周历回退到下一次开奖日，期号留空，按开奖日匹配兑奖

公共仓库可能在开奖前 1-2 小时推占位/重复数据，凌晨重抓才完整 —— 所以 `next_buy_end_time` 比 `next_issue` 更可信。

兑奖类任务判断"今天是不是开奖日"时直接看 `draws` 表里有没有当天的记录，没有再用周历兜底。不能用 `next_fallback`（它会因为 now > buy_end 跳过今天）。

## 推送

只支持 OpenClaw CLI。配置 + 启用一步：

```bash
python scripts/cli.py setup_notify --channel <宿主> --chat-id <chat> [--account-id <acc>] --confirm
```

配置存在 `config/config.json` 的 `notify` 段。固定调用 PATH 里的 `openclaw`，不允许自定义命令路径。

## 数据库 schema

3 张表：

- `tickets`：每注一行；`status` 三态 `active / cancelled / matched`
- `draws`：每期一行；主键 `(lottery, issue)`
- `tasks`：自动任务

## 设计原则

- 大模型只做意图理解 + 调用 + 组织回复
- 选号 / 抓取 / 解析 / 兑奖 / 存储 全部由 Python 规则代码完成
- 随机源使用 `secrets.SystemRandom()`
- 不跨注去重，不做冷热号干预，不做概率优化
- 不承诺中奖、不暗示提高中奖率
