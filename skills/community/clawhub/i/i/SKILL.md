---
name: 记事本
description: 这个技能应在用户需要记录工作事项、查询历史记录、生成工作统计报告或管理待办事项时使用。支持口语化输入，数据持久化存储在本地 JSON 文件中，实现长期记忆。
version: 2.0.1
author: JIAHUI
contact: jiahui@china.com.cn
updated: 2026-05-27
---

## 技能概述

本技能是一个工作记录私人助理，核心职责包括：
- 将口语化工作描述解析并写入本地 `records.json` 数据库
- 按时间段读取记录，生成结构化统计报告
- 管理待办事项的创建与完结状态

数据文件路径：`{WorkBuddy配置目录}/skills/Memo/records.json`（本地单文件，PC端与微信端统一写入此文件）
> - Windows 默认：`C:/Users/{用户名}/.workbuddy/skills/Memo/records.json`

---

## 意图识别

收到用户输入后，先判断意图，再执行对应流程：

| 意图 | 触发特征 | 处理方式 |
|------|----------|----------|
| 添加记录 | 描述工作事件、"帮我记"、"记一下" | 解析字段 → 写入 JSON → **回复必须展示具体内容+事件ID** |
| 统计报告 | "统计"、"汇总"、"本周/上周/本月" | 读取 JSON → 生成报告 |
| 查看待办 | "待办"、"还有什么没做" | 筛选 is_todo=true 且 todo_done=false |
| 搜索记录 | "找找XX的记录"、"有没有关于XX" | 按关键词匹配 content |
| 导出文件 | "导出"、"生成文件" | 调用 main.py export_report() |
| 标记完成 | "XX已完成"、"XX搞定了" | 调用 mark_todo_done() 标记完成 → 调用 get_automation_action_after_complete() 获取自动化操作 → **执行 automation_update** |
| 修改记录 | "把XX改成YY"、"XX应该是YY"、"更新XX"、"XX写错了" | 定位记录 → 调用 update_record() 更新字段 → **智能同步**：若修改了 work_date/reminder_time/content，自动同步对应自动化提醒 |
| 删除记录 | "删掉XX那条"、"撤销XX"、"把XX记录删除" | 定位记录 → 调用 delete_record() → 确认后删除 → **智能同步**：若该记录是待办，自动删除/更新对应提醒 |

---

## 添加记录流程

1. 从用户输入自动识别以下字段（详细规则见 `references/field-rules.md`）：
   - `work_date`：工作发生日期（优先提取内容中的日期，无则用今天）
   - `work_type`：工作类型（沟通/会议/文档/设计/测试/编程/调研/其他）
   - `planning`：计划内 / 临时（默认临时）
   - `importance`：重要 / 不重要 / 未标注
   - `urgency`：紧急 / 不紧急 / 未标注
   - `quality`：高质量 / 中等 / 待改进 / 未标注
   - `contacts`：从内容中识别的人名或角色列表
   - `is_todo`：含"下周/明天/待处理/上班后"等且未完成时为 true
   - `reminder_time`：提醒时间，格式 "HH:MM"（如 "16:00"），用户未指定时为 null，提醒触发时间默认为 08:00
   - `is_single_reminder`：是否为单次提醒。用户说"明天下午3点提醒"时为 true（只在指定日期触发一次）；用户说"每周三提醒"时为 false（重复任务）。此字段影响 validFrom/validUntil 参数的自动设置

2. 统一调用 `MemoSkill().add_record()` 写入记录。**禁止直接读写 records.json**——去重检查和自动化同步逻辑都依赖实例方法，绕过会导致重复记录和提醒失效。

3. 写入前检查 content + work_date 是否重复，避免重复写入。

4. **智能同步提醒**（v1.6.0+）：
   - 若写入的记录 `is_todo=true` 且有明确 `work_date`：
     - 调用 `s.get_automation_action_after_add(record_id)` 获取自动化操作参数
     - 先用 `automation_update(mode="view")` 检查是否已存在同名自动化
     - 根据返回的 action 执行 `automation_update` 的 create 或 update
     - **重要**：若返回的 `is_single_reminder=true`（用户明确指定某一天提醒，非重复任务），必须设置 `validFrom` 和 `validUntil` 参数：
       ```python
       automation_update(
         mode="suggested create",
         name=返回的automation_name,
         prompt="待办提醒：\n" + "\n".join([f"{i+1}. {t}" for i,t in enumerate(返回的all_todos)]),
         rrule=构建的rrule,
         validFrom=返回的validFrom,   # 如 "2026-03-31T00:00:00"
         validUntil=返回的validUntil, # 如 "2026-03-31T23:59:59"
         ...
       )
       ```
     - 这样可实现"单次提醒"功能：即使 rrule 是每周重复，配合 validFrom/validUntil 也只在指定日期触发一次

5. **回复格式（v2.0.0 强化 — 必须展示具体内容+事件ID）**：
   ```
   ✅ 记录已保存
   📝 内容：{content 原文}
   🆔 事件ID：{record_id}
   📅 工作日期：{work_date}
   🏷️ 类型：{work_type} | {planning}
   👤 涉及人员：{contacts，无则省略此行}
   ```

   > ⚠️ **关键规则**：每次添加记录后，回复中**必须**包含 📝具体内容和 🆔事件ID，让用户能确认记录已准确入库。缺少这两项会导致用户无法核实记录是否成功写入。

---

## 统计报告流程

1. 解析用户输入的时间段（本周/上周/本月/上月/自定义日期范围）。
2. **优先使用 `filter_by_date(start_date, end_date)` 读取记录**（比 search() 更完整、更可靠）。
3. 读取 `records.json`，按 `work_date` 筛选记录。
4. 按 `references/report-format.md` 中定义的格式生成报告。
5. 生成报告时，`importance`/`urgency`/`quality` 为"未标注"的字段**不显示**。

---

## 查询记录流程

1. 用户询问"记录到哪里了"、"帮我看看X月的记录"等查询意图时：
2. **优先使用 `filter_by_date(start_date, end_date)`**，而非 `search()`，因为：
   - `filter_by_date()` 按日期范围精确筛选，结果更完整
   - `search()` 仅按关键词匹配，可能遗漏不包含关键词的记录
3. 回复时**每条记录都必须展示具体内容和事件ID**，格式：
   ```
   📅 {work_date}  🆔 {record_id}
   📝 {content}
   ```

---

## 数据操作工具

`main.py` 提供以下函数，可直接调用：

```python
from main import MemoSkill
s = MemoSkill()

s.add_record(content, work_date=None, extra_fields=None)  # 添加记录（含 reminder_time 字段）
s.load_records()                                           # 读取全部记录
s.filter_by_date(start_date, end_date)                    # 按日期筛选（推荐，查询首选）
s.get_todos()                                              # 获取未完成待办
s.mark_todo_done(record_id)                               # 标记待办完成
s.search(keyword)                                          # 关键词搜索（精确查询时使用）
s.update_record(record_id=None, keyword=None, updates={}) # 更新记录字段
s.delete_record(record_id=None, keyword=None)             # 删除记录

# v1.5.0 智能同步辅助方法
s.get_automation_name(work_date)                          # 返回自动化任务名称
s.build_reminder_rrule(work_date, reminder_time=None)     # 生成 rrule 字符串（支持任意时间）
s.get_pending_todos_for_date(work_date)                   # 获取某日期所有未完成待办
s.export_report(start_date, end_date, output_path=None)   # 导出 Markdown 文件
```

## 修改记录流程

1. 从用户描述中提取**定位信息**（关键词或日期）和**修改内容**（哪个字段改成什么）。
2. 调用 `s.update_record(keyword=..., updates={...})` 定位并更新。
3. 若返回 `_ambiguous: True`，向用户展示匹配列表，请其确认是哪一条。
4. 若只有 content 变化，其他字段（work_type 等）视情况同步重新推断，或保留原值。
5. **智能同步提醒**（v1.5.0）：若修改的记录 `is_todo=true`，根据修改内容自动同步自动化任务：
   - 修改了 `work_date`：删除旧日期对应的提醒（检查旧日期是否还有其他待办，无则删除）→ 为新日期创建/合并提醒
   - 修改了 `reminder_time`：删除当前提醒 → 以新时间重建（调用 `build_reminder_rrule(work_date, new_reminder_time)`）
   - 修改了 `content`：更新对应自动化任务的 prompt，将旧内容替换为新内容
   - 上述操作合并执行，**用户只需说一次，系统自动完成所有关联操作**。
6. 回复格式：
   ```
   ✅ 记录已更新
   📝 修改内容：{改动描述}
   🆔 事件ID：{record_id}
   📅 工作日期：{work_date}
   🔔 提醒已同步：{同步操作描述，无提醒变动则省略}
   ```

---

## 删除记录流程

1. 从用户描述中提取定位关键词。
2. 调用 `s.delete_record(keyword=...)` 定位记录。
3. **删除前必须向用户确认**，展示将要删除的记录内容，等待用户回复"确认"/"是"后再执行。
4. 若返回 `_ambiguous: True`，先让用户确认是哪一条，再删除。
5. **智能同步提醒**（v1.6.0）：
   - 删除前先检查记录是否是待办且未完成
   - 删除后调用 `s.get_automation_action_after_complete(record_id)` 获取自动化操作（复用删除前的检查逻辑）
   - 根据返回的 action 执行 `automation_update` 的 delete 或 update
6. 回复格式：
   ```
   🗑️ 记录已删除：{content 前30字}
   🆔 事件ID：{record_id}
   🔔 提醒已同步：{同步操作描述，无提醒则省略}
   ```

---

## 行为准则

- 回答历史记录相关问题前，必须先读取 `records.json` 获取真实数据，不得凭记忆回答。
- 用户可一次性输入多条记录（换行分隔），逐条解析写入。
- 模糊时间如"下周上班"：记录为待办，`work_date` 设为下周一。
- **每条记录的回复都必须展示 📝具体内容 + 🆔事件ID**，这是确保用户能核实记录准确入库的关键。
- **查询记录时优先使用 `filter_by_date()`**，而非 `search()`，确保结果完整。

---

## 并发写入处理（v2.0.0）

当快速连续添加多条记录时，可能出现 `PermissionError`（文件被另一个进程占用）。v2.0.0 的 `save_records()` 已内置重试机制（3次，间隔0.3秒），AI无需额外处理。若重试3次仍失败，会抛出异常，此时：
1. 等待2秒后重试整个操作
2. 若仍失败，告知用户稍后再试

---

## 自动化提醒管理

### 创建提醒（添加记录时触发）

当新增记录满足以下条件时，自动创建或更新对应日期的自动化提醒：
- `is_todo = true`
- `work_date` 为明确的未来日期（非模糊时间如"下周"、"以后"）

**提醒时间**（v1.4.0）：
- 若用户指定了时间（如"下午4点提醒我"），将 `reminder_time` 设为 `"16:00"`
- 若用户未指定时间，`reminder_time` 为 `null`，提醒默认在 `08:00` 触发
- 调用 `s.build_reminder_rrule(work_date, reminder_time)` 生成 rrule

**合并策略**：同一 `work_date` 的所有待办合并到一个自动化任务中，命名格式为 `{work_date} 工作提醒`（如 `2026-03-18 工作提醒`）。

> ⚠️ 合并时若各待办的 `reminder_time` 不同，以**最早的时间**为准，并在 prompt 中标注各条待办的预期时间。

**操作步骤**：
1. 检查是否已存在名为 `{work_date} 工作提醒` 的自动化任务
2. 若不存在：创建新自动化，触发时间按 `reminder_time`（或默认 08:00），prompt 列出当天所有未完成待办内容
3. 若已存在：更新该自动化的 prompt，将新待办追加进去
4. rrule 格式由 `s.build_reminder_rrule(work_date, reminder_time)` 生成，例如：
   - 默认：`FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0`
   - 下午4点：`FREQ=WEEKLY;BYDAY=MO;BYHOUR=16;BYMINUTE=0`
5. cwds 固定设为 `C:\Users\X`

**回复中告知用户**：已自动为该待办创建提醒（注明触发时间）。

---

### 删除提醒（标记完成时触发）

当用户以口语化表述（如"XX已完成"、"XX搞定了"、"XX处理好了"）标记某待办完成后：

**操作步骤**：
1. 在 `records.json` 中将对应记录的 `todo_done` 更新为 `true`
2. 取出该记录的 `work_date`，查找名为 `{work_date} 工作提醒` 的自动化任务
3. 若该自动化存在：
   - 检查该日期是否还有其他未完成待办（`is_todo=true` 且 `todo_done=false`）
   - 若**无其他未完成待办**：删除该自动化任务
   - 若**仍有其他未完成待办**：更新该自动化的 prompt，移除已完成事项，保留其余待办
4. 若该自动化不存在：无需操作

---

## automation_update 工具调用格式

当 SKILL.md 流程要求执行自动化操作时，使用以下格式调用 WorkBuddy 的 `automation_update` 工具。

### 优先方案：直接操作数据库（推荐）

由于 `automation_update` 工具在某些情况下无法正确找到任务（如 ID 格式问题、任务名称不匹配等），**推荐直接操作 SQLite 数据库**：

**数据库路径**：`{WorkBuddy数据目录}/automations/automations.db`
> - Windows 默认：`%APPDATA%/WorkBuddy/automations/automations.db`
> - 替换 `{WorkBuddy数据目录}` 为实际路径

**暂停自动化**：
```python
import sqlite3
import os
db_path = os.path.join(os.getenv('APPDATA'), 'WorkBuddy', 'automations', 'automations.db')
conn = sqlite3.connect(db_path)
conn.execute('UPDATE automations SET status=? WHERE id=?', ('PAUSED', '{automation_id}'))
conn.commit()
```

**查询自动化列表**：
```python
import sqlite3
import os
db_path = os.path.join(os.getenv('APPDATA'), 'WorkBuddy', 'automations', 'automations.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT id, name, status FROM automations')
# 返回格式：(id, name, status)
```

> ⚠️ **重要**：当 `automation_update` 工具调用失败或无法找到任务时，必须使用此数据库方案作为备用。

### 备选方案：automation_update 工具

当数据库方案不可用时，使用以下格式：

#### 删除自动化
```
automation_update(
  mode="suggested update",
  id="{automation_name}",  # 如 "2026-03-28 工作提醒"
  status="PAUSED"           # 暂停自动化即达到删除效果
)
```

### 创建/更新自动化
```
automation_update(
  mode="suggested create",
  name="{automation_name}",    # 如 "2026-04-01 工作提醒"
  prompt="待办提醒：\n1. xxx\n2. yyy",
  rrule="FREQ=WEEKLY;BYDAY=WE;BYHOUR=9;BYMINUTE=0",  # 调度规则
  cwds="{用户工作目录}",       # 如 Windows: "C:\\Users\\用户名"
  scheduleType="recurring",
  validFrom="2026-03-31",      # 生效开始日期（可选）
  validUntil="2026-04-01"       # 生效结束日期（可选）
)
```

**生效日期区间参数（重要）**：
- `validFrom`：任务生效的开始日期（ISO 8601 格式，如 "2026-03-31" 或 "2026-03-31T16:00:00.000Z"）
- `validUntil`：任务生效的结束日期
- **用途**：可以将每周重复的任务变成"单次提醒"——只在指定日期区间内执行一次
- **示例**：设置 `rrule="FREQ=WEEKLY;BYDAY=WE;BYHOUR=9"` + `validFrom="2026-03-31"` + `validUntil="2026-04-01"`，实现"仅4月1日周三早上9点提醒"

> 注意：删除没有专门的 delete 操作，通过将 status 设为 "PAUSED" 来暂停自动化。

---

## 智能同步（v1.6.0）

**核心理念**：用户只需说一次"改成XX"，系统自动完成所有关联的提醒操作，无需多次交互。

| 用户操作 | 自动同步行为 |
|----------|-------------|
| 修改待办的 `work_date` | 删除旧日期提醒（若无其他待办则完全删除，否则更新 prompt）→ 在新日期创建/合并提醒 |
| 修改待办的 `reminder_time` | 删除当前提醒 → 以新时间重建（调用 `build_reminder_rrule` 生成新 rrule） |
| 修改待办的 `content` | 更新对应自动化任务的 prompt，将旧内容替换为新内容 |
| 删除待办记录 | 同"标记完成时触发"的删除逻辑 |

> 非待办记录（`is_todo=false`）的修改/删除**不触发**提醒同步。

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0.1 | 2026-05-27 | **Bug修复**：ID生成增加毫秒精度，修复同秒内多次添加导致记录ID重复的问题（历史29条重复ID已修复）；timestamp字段统一使用ID生成时的时间变量 |
| v2.0.0 | 2026-05-10 | **体验优化**：1) 回复必须展示📝具体内容+🆔事件ID，确保用户可核实记录入库；2) save_records() 增加重试机制（3次/0.3s间隔），解决并发写入 PermissionError；3) 查询优先推荐 filter_by_date()；4) _extract_contacts() 扩展人名识别规则 |
| v1.13.0 | 2026-04-24 | **数据安全防护**：save_records() 增加三层防护（写入前自动备份 + 记录数对比警告 + AUTO-MERGE自动合并）；移除未实现的图标安装功能 |
| v1.12.0 | 2026-04-10 | **智能搜索**：search() 方法支持分词匹配和多关键词OR匹配 |
| v1.11.0 | 2026-04-03 | **安全修复**：移除"直接操作 records.json"选项，统一走 MemoSkill 实例方法 |
| v1.10.0 | 2026-04-02 | 新增口语日期智能解析：_parse_date() 自动识别"今天/明天/下周/X月X日"等表达 |
| v1.9.0 | 2026-04-01 | 新增：内置完整 CLI 入口；修复：export_report 方法定义行残缺 |
| v1.8.1 | 2026-03-30 | 修复：添加待办时自动判断是否设置单次提醒参数 |
| v1.8.0 | 2026-03-30 | 新增生效日期区间参数（validFrom/validUntil） |
| v1.7.0 | 2026-03-30 | 自动化管理增强：新增直接操作 SQLite 数据库方案 |
| v1.6.0 | 2026-03-28 | 数据存储方案调整：改为本地单文件存储 |
| v1.5.0 | 2026-03-26 | 新增智能同步：修改待办时自动同步对应自动化提醒 |
| v1.4.0 | 2026-03-26 | 提醒时间支持任意时间 |
| v1.3.0 | 2026-03-16 | 新增修改/删除记录功能 |
| v1.2.0 | 2026-03-15 | 新增多设备支持 |
| v1.1.0 | 2026-03-01 | 新增自动化提醒管理 |
| v1.0.0 | 2026-02-28 | 初始版本 |
