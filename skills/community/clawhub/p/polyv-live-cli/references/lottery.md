# 抽奖管理

## 概述

抽奖命令用于在直播过程中创建和管理抽奖活动，包括创建、查询、更新、删除抽奖活动，以及查询中奖用户和抽奖记录。

## 创建抽奖

```bash
# 创建无条件抽奖（默认）
<CLI> lottery create -c <频道ID> --name "幸运抽奖" --type none --amount 3 --prize-name "神秘礼品" --force

# 创建邀请抽奖（观众邀请3人参与）
<CLI> lottery create -c <频道ID> --name "邀请抽奖" --type invite --amount 5 --prize-name "优惠券" --duration 30 --invite-num 3 --force

# 创建观看时长抽奖（观看10秒后可参与）
<CLI> lottery create -c <频道ID> --name "时长抽奖" --type duration --amount 2 --prize-name "红包" --duration 10 --force

# 创建评论抽奖（发送指定评论后可参与）
<CLI> lottery create -c <频道ID> --name "评论抽奖" --type comment --amount 3 --prize-name "积分" --duration 60 --comment "参与抽奖" --force

# 创建答题抽奖（回答问题后可参与）
<CLI> lottery create -c <频道ID> --name "答题抽奖" --type question --amount 1 --prize-name "大奖" --duration 30 --force

# JSON输出
<CLI> lottery create -c <频道ID> --name "测试抽奖" --type none --amount 3 --prize-name "奖品" --force -o json
```

## 查询抽奖列表

```bash
# 查询频道所有抽奖活动
<CLI> lottery list -c <频道ID>

# 分页查询
<CLI> lottery list -c <频道ID> --page 1 --size 20

# JSON输出
<CLI> lottery list -c <频道ID> -o json
```

## 查询抽奖详情

```bash
# 获取指定抽奖活动详情
<CLI> lottery get -c <频道ID> --id 20521

# JSON输出
<CLI> lottery get -c <频道ID> --id 20521 -o json
```

## 更新抽奖

```bash
# 更新抽奖活动配置
<CLI> lottery update -c <频道ID> --id 20521 --name "更新后的抽奖" --amount 5 --prize-name "新奖品" --force

# JSON输出
<CLI> lottery update -c <频道ID> --id 20521 --amount 10 --force -o json
```

## 删除抽奖

```bash
# 删除指定抽奖活动
<CLI> lottery delete -c <频道ID> --id 20521 --force
```

## 查询中奖用户

```bash
# 查询中奖用户列表
<CLI> lottery winners -c <频道ID> --lottery-id fv3mao43u6

# 分页查询
<CLI> lottery winners -c <频道ID> --lottery-id fv3mao43u6 --page 1 --limit 20

# 查询指定观众中奖记录
<CLI> lottery winners -c <频道ID> --lottery-id fv3mao43u6 --viewer-id viewer-1

# JSON输出
<CLI> lottery winners -c <频道ID> --lottery-id fv3mao43u6 -o json
```

## 查询抽奖记录

```bash
# 查询频道抽奖记录
<CLI> lottery records -c <频道ID>

# 按场次筛选
<CLI> lottery records -c <频道ID> --session-id fwly13xczv

# 按时间范围筛选
<CLI> lottery records -c <频道ID> --start-time 1615772426000 --end-time 1615773566000

# 分页查询
<CLI> lottery records -c <频道ID> --page 1 --limit 20

# JSON输出
<CLI> lottery records -c <频道ID> -o json
```

## 查询旧版 V3 抽奖记录

```bash
# 查询单频道旧版抽奖记录，必须传时间范围
<CLI> lottery legacy-records -c <频道ID> --start-time 1615772426000 --end-time 1615773566000

# 按场次筛选
<CLI> lottery legacy-records -c <频道ID> --start-time 1615772426000 --end-time 1615773566000 --session-id fwly13xczv

# 分页和 JSON 输出
<CLI> lottery legacy-records -c <频道ID> --start-time 1615772426000 --end-time 1615773566000 --page 1 --limit 20 -o json
```

## 命令选项

### lottery create

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--name` | 抽奖活动名称（必填） | - |
| `--type` | 抽奖条件类型（必填） | none/invite/duration/comment/question |
| `--amount` | 中奖人数（必填） | 数字 |
| `--prize-name` | 奖品名称（必填） | - |
| `--duration` | 抽奖时长（秒） | 数字 |
| `--invite-num` | 邀请人数（仅invite类型） | 数字 |
| `--comment` | 评论内容（仅comment类型必填） | 字符串 |
| `--receive-info` | 中奖者信息收集配置 | JSON字符串 |
| `-f, --force` | 跳过确认提示 | - |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery list

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--page` | 页码 | 数字，默认1 |
| `--size` | 每页数量 | 数字，默认10 |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery get

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--id` | 抽奖活动ID（必填） | - |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery update

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--id` | 抽奖活动ID（必填） | - |
| `--name` | 新的抽奖活动名称 | - |
| `--amount` | 新的中奖人数 | 数字 |
| `--prize-name` | 新的奖品名称 | - |
| `-f, --force` | 跳过确认提示 | - |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery delete

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--id` | 抽奖活动ID（必填） | - |
| `-f, --force` | 跳过确认提示 | - |

### lottery winners

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--lottery-id` | 抽奖ID（必填） | - |
| `--viewer-id` | 指定观众ID；传入后查询该观众中奖记录 | - |
| `--page` | 页码 | 数字，默认1 |
| `--limit` | 每页数量 | 数字，默认20 |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery records

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--session-id` | 场次ID | - |
| `--start-time` | 开始时间（毫秒时间戳） | 数字 |
| `--end-time` | 结束时间（毫秒时间戳） | 数字 |
| `--page` | 页码 | 数字，默认1 |
| `--limit` | 每页数量 | 数字，默认20 |
| `-o, --output` | 输出格式 | table（默认）/ json |

### lottery legacy-records

| 选项 | 说明 | 格式 |
|------|------|------|
| `-c, --channel-id` | 频道ID（必填） | - |
| `--start-time` | 开始时间（毫秒时间戳，必填） | 数字 |
| `--end-time` | 结束时间（毫秒时间戳，必填） | 数字 |
| `--session-id` | 场次ID | - |
| `--page` | 页码 | 数字，默认1 |
| `--limit` | 每页数量 | 数字，默认20 |
| `-o, --output` | 输出格式 | table（默认）/ json |

## 抽奖条件类型说明

| 类型 | 说明 | 必需参数 |
|------|------|----------|
| `none` | 无条件抽奖（默认） | - |
| `invite` | 邀请好友参与 | `--invite-num`（邀请人数） |
| `duration` | 观看时长抽奖 | `--duration`（观看秒数） |
| `comment` | 发送指定评论参与抽奖 | `--duration`（活动秒数）、`--comment`（评论内容） |
| `question` | 回答问题抽奖 | `--duration`（答题秒数） |

## 输出格式

### Table 格式（默认）

抽奖列表示例：
```
┌──────────┬─────────────────────┬──────────┬────────┬────────┬───────────────────┐
│ ID       │ Name                │ Type     │ Status │ Amount │ Prize             │
├──────────┼─────────────────────┼──────────┼────────┼────────┼───────────────────┤
│ 20521    │ 幸运抽奖            │ none     │ ended  │ 3      │ 神秘礼品          │
│ 20522    │ 邀请抽奖            │ invite   │ active │ 5      │ 优惠券            │
└──────────┴─────────────────────┴──────────┴────────┴────────┴───────────────────┘
```

中奖用户示例：
```
┌────────────┬────────────┬─────────────┬─────────────────────┐
│ Viewer ID  │ Nickname   │ Winner Code │ Win Time            │
├────────────┼────────────┼─────────────┼─────────────────────┤
│ viewer123  │ Winner1    │ ABC123      │ 2024-03-19 10:00:00 │
└────────────┴────────────┴─────────────┴─────────────────────┘
```

### JSON 格式

使用 `-o json` 选项输出结构化JSON数据，便于脚本处理。

## 相关文档

- [频道管理](./channel-management.md) - 频道基础操作
- [签到管理](./checkin.md) - 签到互动功能
- [聊天管理](./chat-management.md) - 聊天消息管理
