---
name: list
description: 智能表单 - 通用记账本与信息汇总工具。支持支出账单、出货台账、运行日志等结构化数据记录，可附加图片/文档做存档，支持自动归类、周期报表、定时提醒。用户说「记一下 xxx」即可自动触发，支持记账、备忘、出货、日志等多种记录类型。Smart form, notes, bookkeeping, records, document archive.
---

# 📋 智能表单 · list

## 📋 功能概览

List 是一款 **智能记账与信息汇总工具**，支持多种类型记录，自动归类、定期报表、定时提醒。

**核心功能：**
- **📝 随手记** — 说「记一下 xxx」即可快速记录支出、备忘、出货等
- **📊 自动归类** — 根据内容智能识别类型，自动分类归档
- **📈 周期报表** — 日/周/月报表自动生成，支出趋势一目了然
- **🔔 定时提醒** — 设置周期性提醒，不漏掉重要事项
- **📎 附件存档** — 支持图片/文档附加，方便溯源

## 核心理念

**说"记一下"就完事了**。用户不需要选类型、填字段——说了就自动归类存好。
- 零门槛：`记一下 xxx` 即可
- 自动分类：根据内容判断是支出/出货/日志/其他
- 图片也可：发张收据说"记一下"，自动识别并保存

## 行为规则

**命令式触发（直接执行）**：用户说「记一下 + 内容」这种明确命令句式时，直接识别并保存，无需确认。
**模糊触发（先确认）**：用户只说了单个词（如 "记账"、"记录一下"、"日志"、"list"）时，先问「要记一笔吗？」得到肯定答复后再执行。

## 数据存储

`workspace/memory/list-data/` 目录，每种记录类型独立 JSON：

```
memory/list-data/
├── expenses.json      # 支出
├── shipments.json     # 出货  
├── logs.json          # 运行日志
├── photos.json        # 图片归档（自动识别类型时用）
└── ...                # 自动创建的新类型
```

**记录格式**：
```json
{
  "config": {"fields": {"category":"text","amount":"number","note":"text"}},
  "records": [
    {
      "id": "uuid",
      "timestamp": "2026-05-19T19:00:00+08:00",
      "data": {"category":"餐饮","amount":200,"note":"晚饭"},
      "tags": [],
      "attachments": []
    }
  ]
}
```

## 脚本工具

所有数据操作通过 `scripts/list.py`，模型不直接改 JSON：

| 操作 | 命令 |
|------|------|
| 新增记录 | `python3 scripts/list.py add <type> --data '{"k":"v"}' [--image <path>]` |
| 查询记录 | `python3 scripts/list.py query <type> [--from DATE] [--to DATE] [--filter JSON]` |
| 周期汇总 | `python3 scripts/list.py summary <type> [--from DATE] [--to DATE] [--by category]` |
| 列出类型 | `python3 scripts/list.py types` |
| 新增类型 | `python3 scripts/list.py new-type <type> --fields '{"字段":"类型"}'` |
| 删除记录 | `python3 scripts/list.py delete <type> <id>` |

## 核心工作流程

### 1. 自动分类录入（最常用）

用户说「记一下 XXX」，自动判断类型并保存：

**判断逻辑**（由上到下匹配）：
1. 含金额数字 → **expenses**（支出），如"记一下今天吃饭200"
2. 含出货/发货/件数 → **shipments**（出货），如"记一下发了50件到广州"  
3. 含日志/运行/状态 → **logs**（运行日志），如"记一下服务器正常"
4. 含图片附件 → **photos**（图片归档），无文本时用"图片归档"类型
5. 其他 → 问用户确认类型，或创建新类型

**操作步骤**：
1. 判断属于哪个类型
2. 提取关键字段（金额/分类/数量/目的地等）
3. 如该类型 JSON 不存在 → `new-type` 自动创建，按内容推断字段
4. `python3 scripts/list.py add <type> --data 'JSON' [--image <path>]`
5. 回复确认"已记录"

**判断示例**：

| 用户说 | 自动识别 | 存入 |
|--------|---------|------|
| "记一下今天吃饭200" | expenses | `{category:"餐饮",amount:200,note:"今天吃饭"}` |
| "记一下发了50件到广州" | shipments | `{product:"未指定",quantity:50,destination:"广州"}` |
| "记一下服务器宕机了" | logs | `{system:"服务器",status:"异常",detail:"宕机"}` |
| 拍收据说"记一下" | expenses | 存图片，自动尝试读取金额 |

### 2. 查询/筛选

用户问"查一下 x月花了多少" → `query` + 模型加工输出趋势。

### 3. 周期汇总

用户说"月底总结/本月花了多少" → `summary`，按分类聚合。

### 4. 图片/文档归档

用户发图片说"记一下"：

1. 保存图片到 `memory/list-data/attachments/`
2. 如果模型支持图片识别 → 分析图片内容，提取关键信息
3. 用提取的信息填充字段（收据金额/合同日期等）
4. 保存记录 + 关联图片

> ⚠️ **注意**：图片自动识别需要大模型支持图片识别能力（如 GPT-4o、Claude 3.5 Sonnet 等）。如当前模型不支持，仅做图片存档，需用户手动补充描述。

### 5. 定时提醒

Cron 定时问用户要不要记一笔：

```
openclaw cron add \
  --name list-remind-expense \
  --cron "0 21 * * *" \
  --tz "Asia/Shanghai" \
  --message "list-remind: 睡前记账时间到~ 今天花了多少？" \
  --channel feishu --to <目标> \
  --session isolated --no-deliver
```

## 内置类型模板

模型在自动创建类型时参考以下模板结构：

**expenses（支出）** — 字段：category(text), amount(number), note(text)
- 分类：餐饮/交通/购物/娱乐/医疗/学习/生活/其他

**shipments（出货）** — 字段：product(text), quantity(number), destination(text), note(text)

**logs（运行日志）** — 字段：system(text), status(text), detail(text)
- 状态：正常/异常/维护

**photos（图片归档）** — 字段：description(text), tags(text), date(text)

不在模板中的类型由模型推断字段并 `new-type` 创建。

## 用户引导

### 首次使用

用户第一次触发 skill（或说「怎么用」）时，在回复末尾附上简短功能指引：

> 📋 智能表单已激活！试试：
> • **记一下** — "记一下今天吃饭200"（自动分类支出）
> • **查一下** — "查一下五月花了多少"
> • **月底总结** — "本月花了多少"
> • **拍照** — 发收据说"记一下"，自动识别
> • 还能记录出货、运行日志等

### 每次回复后末尾提示

成功记录、查询、汇总后，末尾加一句简短引导：

| 场景 | 末尾提示 |
|------|---------|
| 记录成功 | ✅ 已记录 💬 回复「查一下」查看记录 |
| 查询完成 | 💬 回复「记一下」继续记录，或「月底总结」看汇总 |
| 汇总报表 | 📊 本月已汇总 💬 回复「流水」查看完整清单 |

### 不确定时主动问

用户说得太模糊时，先问清楚再操作：

> 你是想记一笔支出、出货，还是其他？或者直接说「记一下 xxx」我自己判断
