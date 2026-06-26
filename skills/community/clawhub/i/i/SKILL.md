---
name: Memo
description: 这个技能应在用户需要记录工作事项、查询历史记录、生成工作统计报告或管理待办事项时使用。支持口语化输入，数据持久化存储在本地 JSON 文件中，实现长期记忆。
version: 1.2.0
author: 贾辉
contact: 13581935893
updated: 2026-03-15
---

## 技能概述

本技能是一个工作记录私人助理，核心职责包括：
- 将口语化工作描述解析并写入本地 `records.json` 数据库
- 按时间段读取记录，生成结构化统计报告
- 管理待办事项的创建与完结状态

数据文件路径：`D:/华为云盘/records.json`

---

## 意图识别

收到用户输入后，先判断意图，再执行对应流程：

| 意图 | 触发特征 | 处理方式 |
|------|----------|----------|
| 添加记录 | 描述工作事件、"帮我记"、"记一下" | 解析字段 → 写入 JSON → 若含明确日期的待办则自动创建/合并提醒 |
| 统计报告 | "统计"、"汇总"、"本周/上周/本月" | 读取 JSON → 生成报告 |
| 查看待办 | "待办"、"还有什么没做" | 筛选 is_todo=true 且 todo_done=false |
| 搜索记录 | "找找XX的记录"、"有没有关于XX" | 按关键词匹配 content |
| 导出文件 | "导出"、"生成文件" | 调用 main.py export_report() |
| 标记完成 | "XX已完成"、"XX搞定了" | 更新对应记录 todo_done=true → 检查并删除对应日期的自动化提醒 |

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

2. 调用 `main.py` 中的 `MemoSkill().add_record()` 写入记录，或直接操作 `records.json`。

3. 写入前检查 content + work_date 是否重复，避免重复写入。

4. 回复格式：
   ```
   ✅ 记录已保存
   📅 工作日期：{work_date}
   🏷️ 类型：{work_type} | {planning}
   👤 涉及人员：{contacts，无则省略此行}
   ```

---

## 统计报告流程

1. 解析用户输入的时间段（本周/上周/本月/上月/自定义日期范围）。
2. 读取 `records.json`，按 `work_date` 筛选记录。
3. 按 `references/report-format.md` 中定义的格式生成报告。
4. 生成报告时，`importance`/`urgency`/`quality` 为"未标注"的字段**不显示**。

---

## 数据操作工具

`main.py` 提供以下函数，可直接调用：

```python
from main import MemoSkill
s = MemoSkill()

s.add_record(content, work_date=None, extra_fields=None)  # 添加记录
s.load_records()                                           # 读取全部记录
s.filter_by_date(start_date, end_date)                    # 按日期筛选
s.get_todos()                                              # 获取未完成待办
s.mark_todo_done(record_id)                               # 标记待办完成
s.search(keyword)                                          # 关键词搜索
s.export_report(start_date, end_date, output_path=None)   # 导出 Markdown 文件
```

---

## 行为准则

- 回答历史记录相关问题前，必须先读取 `records.json` 获取真实数据，不得凭记忆回答。
- 用户可一次性输入多条记录（换行分隔），逐条解析写入。
- 模糊时间如"下周上班"：记录为待办，`work_date` 设为下周一。

---

## 自动化提醒管理

### 创建提醒（添加记录时触发）

当新增记录满足以下条件时，自动创建或更新对应日期的自动化提醒：
- `is_todo = true`
- `work_date` 为明确的未来日期（非模糊时间如"下周"、"以后"）

**合并策略**：同一 `work_date` 的所有待办合并到一个自动化任务中，命名格式为 `{work_date} 工作提醒`（如 `2026-03-18 工作提醒`）。

**操作步骤**：
1. 检查是否已存在名为 `{work_date} 工作提醒` 的自动化任务
2. 若不存在：创建新自动化，触发时间为该日期对应星期几的 08:00，prompt 列出当天所有未完成待办内容
3. 若已存在：更新该自动化的 prompt，将新待办追加进去
4. rrule 格式：`FREQ=WEEKLY;BYDAY={星期缩写};BYHOUR=8;BYMINUTE=0`
   - 星期对应：周一=MO，周二=TU，周三=WE，周四=TH，周五=FR，周六=SA，周日=SU
5. cwds 固定设为 `D:\华为云盘`

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

