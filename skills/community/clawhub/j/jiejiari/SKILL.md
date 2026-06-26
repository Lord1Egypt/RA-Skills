---
name: jiejiari
description: "Look up official Mainland China public holiday schedules and make-up workdays from bundled annual reference data. Use when the user asks about 法定节假日, 放假安排, 调休, 补班, 国务院办公厅 holiday notices, or whether a specific 2026 date is a holiday/workday around 元旦, 春节, 清明节, 劳动节, 端午节, 中秋节, and 国庆节. Distinguish official holiday arrangements from lunar festival date lookup. NOT for calendar event CRUD, reminders, or non-China holiday calendars."
metadata: { "openclaw": { "emoji": "🎏" } }
---

# Jiejiari Skill

用这个技能回答中国法定节假日放假安排与调休问题。

## 范围

- 只根据本技能内置的年度参考数据回答。
- 当前已内置 2026 年安排，数据文件在 `references/cn-holidays-2026.json`。
- “节日日期”与“放假安排”分开处理：
  - 问农历节日本身是几月几号，可改用 `rili`。
  - 问春节/中秋/国庆具体放几天、哪天补班，优先用本技能。

## 回答规则

- 优先给出精确日期，不要只说“本周日”“下周六”。
- 明确区分：
  - `holiday_days`: 连休天数
  - `start_date` 到 `end_date`: 放假区间
  - `work_days`: 调休上班日期
- 如果用户问“某天放不放假/要不要上班”，先在年度数据里定位该日期，再明确回答属于：
  - 放假日
  - 调休日
  - 普通周末或普通工作日
- 如果用户把农历节日日期和官方调休混在一起问，先拆开回答，避免混淆。
- 数据里没有的年份或地区性安排，不要猜。明确说明当前技能只内置了哪些年份。

## 使用方式

- 先读取对应年份的参考文件。
- 按 `festival`、日期区间、`work_days` 回答。
- 用户要完整清单时，按节日顺序列出每个节日的放假区间、总天数、调休日。

## 命令

### 查某天状态

```bash
node {baseDir}/scripts/jiejiari.js date 2026-02-14
node {baseDir}/scripts/jiejiari.js date 2026-02-17 --json
```

输出会明确标注该日属于：

- 节假日
- 调休上班
- 普通周末
- 普通工作日

### 查某个节日安排

```bash
node {baseDir}/scripts/jiejiari.js festival 春节
node {baseDir}/scripts/jiejiari.js festival 国庆节 --json
```

### 列出全年安排

```bash
node {baseDir}/scripts/jiejiari.js list
node {baseDir}/scripts/jiejiari.js list --json
```

## 2026 节日列表

当前参考数据覆盖：

- 元旦
- 春节
- 清明节
- 劳动节
- 端午节
- 中秋节
- 国庆节

## 注意事项

- 这是“官方放假安排”技能，不是世界各国节假日百科。
- 不要把周末天然休息日误写成法定节假日。
- 不要自行推断“可能会调休”；只引用参考数据中的明确日期。
- 当前脚本只内置 2026 年数据；问到其他年份时要明确说明未内置。
