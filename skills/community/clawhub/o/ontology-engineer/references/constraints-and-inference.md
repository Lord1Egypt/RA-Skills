# Constraints and Inference

约束防止脏数据进入图谱，推理从已有事实中推导新知识。两者配合让知识图谱从"数据仓库"升级为"推理引擎"。

## 1. 类型约束

### 1.1 必需属性

每个 core type 的最低数据要求。缺少必需属性的实体不应写入 graph.jsonl。

| Type | 必需属性 | 说明 |
|------|----------|------|
| Person | `name` | 至少有姓名。无名人物用"某星辰集团员工"等占位，标 confidence=low |
| Organization | `name` | 至少有组织名 |
| Project | `name`, `status` | 项目必须有名称和状态（planning/active/paused/completed/archived） |
| Task | `title`, `status` | 任务必须有标题和状态（open/in_progress/blocked/done/cancelled） |
| Document | `title` | 至少有标题。path 可选（口述提到的文档可能无路径） |
| Event | `title`, `date` | 事件必须有日期，没有日期的归 Note 而非 Event |
| Note | `content` | 笔记的本体就是内容 |
| Goal | `description`, `status` | 目标必须有描述和状态（proposed/active/achieved/abandoned） |

### 1.2 属性值域约束

| Type.属性 | 允许值 | 违规处理 |
|-----------|--------|----------|
| Organization.type | company, department, team, institution, government, ngo, startup, other | 不在列表中 → 用 other + labels 补充 |
| Project.status | planning, active, paused, completed, archived | 不合法值 → review_flag |
| Task.status | open, in_progress, blocked, done, cancelled | 同上 |
| Task.priority | low, medium, high, critical | 同上 |
| Goal.status | proposed, active, achieved, abandoned | 同上 |
| Document.format | md, docx, pdf, xlsx, pptx, html, txt, sql, yaml, json, csv, doc, xls, ppt, other | 未知格式 → other |
| *.confidence | high, medium, low | 只有这三档 |

### 1.3 ID 格式约束

正则：`^[a-z][a-z0-9_]+-[0-9]{3,}$`

| Type | 前缀 | 示例 |
|------|------|------|
| Person | per- | per-00001（张三） |
| Organization | org- | org-00002（蓝天信息） |
| Project | project- | project-001 |
| Task | task- | task-00005 |
| Document | doc- | doc-00033 |
| Event | evt- | evt-00001 |
| Note | note- | note-00002 |
| Goal | goal- | goal-00006 |

ID 一旦分配不可回收。deprecated 实体的 ID 永久保留。

## 2. 关系约束

### 2.1 合法关系矩阵

标记哪些 source_type → target_type 的关系是合法的。未在矩阵中的关系写入时触发 review_flag。

| Source \ Target | Person | Org | Project | Task | Doc | Event | Note | Goal |
|-----------------|--------|-----|---------|------|-----|-------|------|------|
| **Person** | knows | works_at, leads, member_of | participates_in, manages | assigned_to(reverse) | authored(reverse) | has_participant(reverse) | authored_by(reverse) | owned_by(reverse) |
| **Org** | employs | subsidiary_of, partner_of, competitor_of, customer_of | contracted_by(reverse) | - | - | related_to(reverse) | about(reverse) | set_by(reverse) |
| **Project** | has_owner | contracted_by, delivered_to | - | has_task | has_document | - | - | - |
| **Task** | assigned_to | - | belongs_to | depends_on, blocks | produces | - | - | measured_by(reverse) |
| **Doc** | authored_by | - | belongs_to | - | references | - | extracted_from(reverse) | - |
| **Event** | has_participant | related_to | belongs_to | produces | - | - | - | - |
| **Note** | authored_by | about | about | about | extracted_from | about | - | - |
| **Goal** | owned_by | set_by | belongs_to | measured_by | - | driven_by | driven_by | - |

`-` 表示这对组合没有常见关系。如果扫描中发现了，生成 review_flag 让用户判断是否需要新增关系类型。

### 2.2 基数约束

| 关系 | 硬约束 | 理由 |
|------|--------|------|
| Person.works_at → Organization | 最多 3 个（end=null 的） | 兼职上限。超过 3 个当前有效的雇佣关系，大概率有脏数据 |
| Task.belongs_to → Project | 恰好 1 个 | 每个 Task 必须归属且只归属一个 Project |
| Document.authored_by → Person | 最多 5 个 | 联合作者上限。超过 5 个更可能是组织署名 → 建 Organization |
| Organization.subsidiary_of → Organization | 最多 1 个 | 一个组织只有一个直接上级。间接上级用推理得出 |
| Goal.measured_by → Task | 至少 1 个 | 没有 Task 衡量的 Goal 是空谈。标 review_flag |

### 2.3 自引用与循环约束

| 约束 | 检查方式 | 示例 |
|------|----------|------|
| 禁止自引用 | target_id != source_id | Organization 不能 subsidiary_of 自己 |
| subsidiary_of 无环 | 沿 subsidiary_of 追溯不能回到起点 | 蓝天信息 → 星辰集团国际 → 星辰集团 → ... 不能回到蓝天信息 |
| depends_on 无环 | Task 依赖链不能成环 | A depends_on B, B depends_on A → 检测到循环，review_flag |
| blocks 无环 | 同上 | 阻塞关系也不能成环 |
| references 允许环 | Document 可以互相引用 | 07号文档 references 技术底座方案，反过来也可以 |

## 3. 推理规则

从已有事实推导新知识。推理产出的关系标记 `source.type = "inferred"`，与扫描/手动数据区分。

### 规则 1: 传递性 — subsidiary_of

```
A subsidiary_of B, B subsidiary_of C
→ A indirectly_affiliated_with C
```

示例：蓝天信息 subsidiary_of 星辰集团国际, 星辰集团国际 subsidiary_of 星辰集团 → 蓝天信息 indirectly_affiliated_with 星辰集团

### 规则 2: 对称性 — partner_of / competitor_of / knows

```
A partner_of B → B partner_of A
A competitor_of B → B competitor_of A
A knows B → B knows A
```

写入时只存一条（direction=bidirectional），查询时双向返回。

### 规则 3: 逆关系 — works_at / employs

```
A works_at B → B employs A
A authored_by B → B authored A
A assigned_to B → B has_assignee A
```

不需要重复存储。query_graph.py 在查询 Organization 的关系时，自动反向查 Person.works_at。

### 规则 4: 继承推理 — 组织归属传递

```
A works_at B, B subsidiary_of C
→ A affiliated_with C
```

示例：张三 works_at 蓝天信息, 蓝天信息 subsidiary_of 星辰集团 → 张三 affiliated_with 星辰集团

注意：affiliated_with 比 works_at 弱——张三不直接为星辰集团工作，但属于星辰集团体系。

### 规则 5: 冲突检测 — 角色不一致

```
A works_at B (role=X) in doc-001
A works_at B (role=Y) in doc-002, where X != Y
→ review_flag: role_conflict
```

示例：某文档说李四是"总经理"，另一文档说是"法定代表人"。两个都可能对（一人多职），但需要人工确认，不自动合并。

### 规则 6: 时间推理 — 跳槽检测

```
A works_at B (end: 2023-06)
A works_at C (start: 2023-09)
→ infer: A 从 B 跳槽到 C (gap: 3个月)
```

如果 gap < 6 个月，高置信度。gap > 12 个月，可能中间还有其他经历，标 confidence=low。

### 规则 7: 项目归属推理

```
A authored doc-X, doc-X belongs_to Project-Y
→ A participates_in Project-Y (confidence=medium)
```

写了项目文档的人大概率参与了该项目。但不绝对——可能是外部审稿人。

### 规则 8: 孤立实体预警

```
Entity E has zero relations (no incoming, no outgoing)
→ review_flag: isolated_entity
```

孤立实体要么是数据不完整（缺少关系提取），要么是垃圾数据。定期检查清理。

## 4. 不一致检测清单

query_graph.py 应支持 `--check-consistency` 模式，检查以下项目：

| 检查项 | 检测方法 | 严重程度 |
|--------|----------|----------|
| 同名不同 ID | 按 name 分组，找 count > 1 的 | 高 — 可能是重复实体 |
| 同 ID 不同属性值 | 同一 ID 出现在多条 create/update 记录中，属性值矛盾 | 中 — 可能是正常更新 |
| 循环依赖 | 沿 subsidiary_of / depends_on / blocks 做 DFS 检测环 | 高 — 违反约束 |
| 孤立实体 | relations 为空且不被任何其他实体引用 | 低 — 可能只是数据不全 |
| 过期关系未标记 | temporal.end 日期已过但未标记 deprecated | 中 — 关系可能已失效 |
| ID 格式违规 | 不匹配 `^[a-z][a-z0-9_]+-[0-9]{3,}$` | 高 — 违反格式约束 |
| 基数超限 | Person.works_at(end=null) > 3 个 | 中 — 可能有脏数据 |
| 必需属性缺失 | Event 没有 date, Task 没有 status | 高 — 违反类型约束 |

**执行方式**：

```bash
python query_graph.py --check-consistency
# 输出: consistency_report.md，按严重程度排序
```

建议在每次 Step 2 完成后运行一次，在 graph.jsonl 追加 100+ 实体后再运行一次。
