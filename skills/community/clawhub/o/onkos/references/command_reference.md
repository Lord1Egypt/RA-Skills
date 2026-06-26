# 命令参数速查

## 目录

1. [记忆引擎](#记忆引擎-memory_enginepy)
2. [事实引擎](#事实引擎-fact_enginepy)
3. [知识图谱](#知识图谱-knowledge_graphpy)
4. [伏笔追踪](#伏笔追踪-hook_trackerpy)
5. [追读力追踪](#追读力追踪-engagement_trackerpy)
6. [弧线管理](#弧线管理-arc_managerpy)
7. [角色模拟](#角色模拟-character_simulatorpy)
8. [质量审计](#质量审计-quality_auditorpy)
9. [连续性检查](#连续性检查-continuity_checkerpy)
10. [风格分析](#风格分析-style_learnerpy)
11. [实体提取](#实体提取-entity_extractorpy)
12. [情节管理](#情节管理-plot_brancherpy)
13. [上下文检索](#上下文检索-context_retrieverpy)
14. [项目管理](#项目管理-project_initializerpy)
15. [设定导入](#设定导入-settings_importerpy)
16. [内置命令](#内置命令-command_executorpy)

---

## 记忆引擎 (memory_engine.py)

所有命令需要 `--db-path` 和 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `store-chapter` | store-chapter | chapter, content/content-file | 存储章节（自动分场景） |
| `store-scene` | store-scene | chapter, content/content-file, location, characters, mood, events, tags | 存储场景 |
| `search` | search | query, top-k, chapter, chapter-range | 搜索记忆（FTS5+ONNX混合） |
| `store-summary` | store-summary | level, range_desc, content | 存储摘要（同level+range覆盖） |
| `mem-stats` | stats | | 记忆引擎统计 |
| `create-arc` | create-arc | arc_id, arc_title, start_chapter, arc_type, end_chapter, phase_id | 创建弧线 |
| `list-arcs` | list-arcs | arc_type | 列出弧线 |
| `chapter-complete` | chapter-complete | chapter, content | 章节完成批量操作(自动replace) |

### store-summary 参数详解

- `level`: `book`(全书)/`phase`(阶段)/`arc`(弧线)/`volume`(卷)/`chapter`(章节)
- `range_desc`: 摘要范围标识（如章节号"15"、弧线ID"trial"、阶段ID"rise"等）

---

## 事实引擎 (fact_engine.py)

所有命令需要 `--db-path` 和 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `set-fact` | set-fact | category, entity, attribute, value, chapter, importance, valid-from, valid-until | 设置事实（同属性自动替代） |
| `get-fact` | get-fact | entity, attribute | 获取事实当前值 |
| `get-facts` | get-facts | entity, category, limit | 获取所有活跃事实 |
| `relevant-facts` | relevant-facts | chapter(可选) | 按相关性获取事实（importance+时效性筛选） |
| `archive-facts` | archive-facts | chapter, limit | 归档旧事实 |
| `detect-contradictions` | detect-contradictions | | 检测事实矛盾 |

### set-fact 参数详解

- `category`: 事实类别（人物/world/item/event）
- `entity`: 实体名
- `attribute`: 属性名（如"境界"、"位置"）
- `value`: 属性值
- `chapter`: 事实确立的章节号
- `importance`: `permanent`(永久设定)/`arc-scoped`(弧线内)/`chapter-scoped`(近期)
- `valid-from`: 事实生效起始章节（可选）
- `valid-until`: 事实失效章节（可选）

### relevant-facts 自动推断

`--chapter` 参数可选。未提供时，自动从 scenes_content 表查询 MAX(chapter) 作为当前章节。返回结果中包含 `current_chapter` 字段标明实际使用的章节号。

---

## 知识图谱 (knowledge_graph.py)

所有命令需要 `--db-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `add-node` | add-node | node_type, node_id, name | 添加图节点 |
| `add-edge` | add-edge | source, target, relation | 添加关系 |
| `delete-edge` | delete-edge | edge_id | 按ID删除关系 |
| `find-edge-by-names` | find-edge-by-names | source, target, relation(可选) | 按端点名称查找关系边 |
| `find-node` | find-node | name | 按名称查找节点 |
| `get-neighbors` | get-neighbors | node_id | 获取邻居节点和关系 |
| `find-path` | find-path | source, target | 查找两节点间路径 |
| `list-nodes` | list-nodes | | 列出所有节点 |
| `kg-stats` | stats | | 图谱统计（节点数/边数/类型分布） |

### 节点类型

`person`(角色)/`faction`(势力)/`location`(地点)/`item`(物品)/`event`(事件)

---

## 伏笔追踪 (hook_tracker.py)

所有命令需要 `--db-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `plant-hook` | plant | desc, planted_chapter, expected_resolve, priority, hook_id, strength | 种植伏笔(strength=0-1) |
| `resolve-hook` | resolve | hook_id, resolved_chapter | 回收伏笔 |
| `partial-resolve` | partial-resolve | hook_id, hint_chapter | 部分回收(partial_count+1) |
| `hint-hook` | hint | hook_id, hint_chapter | 暗示提及(仅更新last_hint_chapter) |
| `update-hook-strength` | update-strength | hook_id, strength | 更新伏笔强度(0-1) |
| `abandon-hook` | abandon | hook_id | 放弃伏笔 |
| `abandon-chapter-hooks` | abandon-chapter | chapter | 放弃指定章节open伏笔 |
| `list-hooks` | list-open | | 列出未闭合伏笔 |
| `overdue-hooks` | overdue | current_chapter | 超期伏笔(含urgency衰减值) |
| `forgotten-hooks` | forgotten | current_chapter | 遗忘伏笔预警(含forget_risk) |
| `hook-stats` | stats | | 伏笔统计(含urgency/strength均值) |

### plant-hook 参数详解

- `desc`: 伏笔描述
- `planted_chapter`: 种埋章节
- `expected_resolve`: 预期回收章节
- `priority`: `critical`/`normal`/`minor`
- `hook_id`: 自定义ID（可选，不填自动生成）
- `strength`: 伏笔强度(0-1)，由智能体评估，默认0.5

### urgency衰减公式

- base = strength * (1 + 0.2 * partial_count)
- 超期: urgency = base * (1 + 0.5 * (elapsed - expected_window) / 10)
- 未超期: urgency = base * max(0.3, 1.0 - elapsed * 0.02)
- Clamp [0, 5.0]

---

## 追读力追踪 (engagement_tracker.py)

所有命令需要 `--db-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `score-chapter` | score | chapter, engagement_score, hook_strength, tension_level, pace_type, notes | 存储章节追读力评分 |
| `engagement-trend` | trend | from_chapter, to_chapter | 追读力趋势分析 |
| `pacing-report` | pacing | from_chapter, to_chapter | 节奏模式检测+建议 |
| `debt-report` | debt | current_chapter | 叙事债务报告(超期伏笔+紧张度累积) |

### score-chapter 参数详解

- `chapter`: 章节编号（必填）
- `engagement_score`: 读者投入度(0-10)
- `hook_strength`: 本章伏笔钩力(0-10)
- `tension_level`: 紧张度(0-10)
- `pace_type`: 节奏类型(buildup/climax/relief/transition)
- `notes`: 智能体备注

### reader_pull计算

综合读者拉力 = 0.4 * engagement + 0.35 * hook + 0.25 * tension（缺失维度以5.0填充）

### 节奏建议规则

- 连续3+章buildup → 建议climax
- 连续2+章climax → 建议relief
- 连续3+章relief → 建议buildup
- 连续2+章transition → 警告节奏拖沓

---

## 弧线管理 (arc_manager.py)

所有命令需要 `--db-path` 和 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `create-phase` | create-phase | phase_id, title, start_chapter, end_chapter | 创建阶段(100-300章粒度) |
| `create-arc-am` | create-arc | arc_id, title, start_chapter, end_chapter, phase_id | 创建弧线(30-60章粒度) |
| `complete-arc` | complete-arc | arc_id | 标记弧线完成 |
| `arc-progress` | progress | chapter(可选), arc_id | 查看弧线进度（省略chapter自动推断） |
| `suggest-next` | suggest-next | chapter(可选) | 建议下一个弧线（省略chapter自动推断） |

---

## 角色模拟 (character_simulator.py)

所有命令需要 `--characters-dir` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `create-character` | create | name, role, big-five(JSON), core-traits(JSON), forbidden-actions(JSON), speech-style, typical-behaviors(JSON) | 创建角色 |
| `check-ooc` | check-ooc | name, behavior, context | OOC检测（双层:禁止行为+Big Five分析） |
| `char-prompt` | generate-prompt | name | 生成角色提示词 |
| `list-chars` | list | | 列出所有角色 |

### create-character 参数详解

- `name`: 角色名
- `role`: `protagonist`/`antagonist`/`mentor`/`sidekick`/`npc`
- `big-five`: JSON字符串，如 `'{"openness":0.8,"conscientiousness":0.6,"extraversion":0.4,"agreeableness":0.7,"neuroticism":0.3}'`
- `core-traits`: JSON数组，如 `'["坚韧","重情义"]'`
- `forbidden-actions`: JSON数组，如 `'["背叛朋友"]'`
- `speech-style`: 说话风格描述
- `typical-behaviors`: JSON数组，如 `'["遇事先观察"]'`

---

## 质量审计 (quality_auditor.py)

需要 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `audit` | audit | chapter, content/content-file | 质量审计（返回health_score 0-100） |

---

## 连续性检查 (continuity_checker.py)

需要 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `check-continuity` | check-chapter | chapter, content | 连续性检查（OOC+位置矛盾+事实矛盾） |
| `analyze-revision` | analyze-revision | chapter, old-content, new-content | 修订影响分析 |

### analyze-revision 返回结构

```json
{
  "chapter": 15,
  "risk_level": "high",
  "entity_changes": {"added_characters": [], "removed_characters": ["青云宗"], ...},
  "affected_chapters": [...],
  "affected_facts": [...],
  "affected_hooks": [...],
  "recommendation": "高风险修订: 存在实体删除..."
}
```

风险等级: `high`(实体删除)/`medium`(存在受影响内容)/`low`(无明显连锁影响)

---

## 风格分析 (style_learner.py)

需要 `--style-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `analyze-style` | analyze | text/content-file | 分析文本风格特征 |
| `compare-style` | compare | text(待比较文本), profile(风格配置名) | 比较文本与已有风格配置 |

---

## 实体提取 (entity_extractor.py)

需要 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `extract-entities` | extract | text/content-file, chapter, genre, types | 提取实体（含置信度） |

- `genre`: `fantasy`/`urban`/`wuxia`/`scifi`（不指定时从项目配置读取，默认fantasy）
- `types`: 逗号分隔，默认 `characters,locations,items,events`

---

## 情节管理 (plot_brancher.py)

需要 `--plot-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `add-plot` | add-node | title, chapter, node_type, description, characters, causes, leads-to | 添加情节节点（title必填） |
| `create-branch` | create-branch | title, chapter, from-node, expected-convergence | 创建支线 |
| `plot-timeline` | timeline | chapter-start, chapter-end | 情节时间线 |
| `check-branches` | check-health | | 检查支线健康（超过5条活跃支线预警） |

### 情节节点类型

`event`(事件)/`decision`(决策)/`revelation`(揭示)/`climax`(高潮)/`resolution`(解决)

---

## 上下文检索 (context_retriever.py)

需要 `--db-path` 和 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `for-creation` | for-creation | chapter, query, entities | 获取6级分层创作上下文 |
| `context-hierarchy` | hierarchy | chapter | 查看摘要层级覆盖情况 |
| `budget-report` | budget-report | chapter | 上下文预算报告 |

### for-creation 返回结构

```json
{
  "book_summary": "...",
  "current_state": "...",
  "phase_summary": "...",
  "arc_summary": "...",
  "volume_summary": "...",
  "prev_chapter_summary": "...",
  "key_facts": [...],
  "recent_scenes": [...],
  "open_hooks": [...],
  "engagement": "近期节奏+债务摘要",
  "budget_used": 8500,
  "budget_total": 12000
}
```

---

## 项目管理 (project_initializer.py)

需要 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `init` | init | title, genre, author, description | 创建项目（含数据库、目录结构、配置文件） |
| `status` | status | | 查看项目状态（是否已初始化、统计信息） |

## 设定导入 (settings_importer.py)

需要 `--project-path` 公共参数。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `import-settings` | import | path, chapter(可选,默认0) | 从Markdown文件批量导入角色、实体、关系、事实、伏笔 |
| `preview-settings` | dry-run | path, chapter(可选,默认0) | 预览设定文件解析结果（不执行实际导入） |
| `update-settings` | update | path, chapter(可选,默认0) | 从Markdown文件批量更新已有设定（角色属性/实体类型/关系/事实/伏笔） |
| `delete-settings` | delete | path | 从Markdown文件批量删除设定（角色+节点/边/事实/伏笔） |

---

## 内置命令 (command_executor.py)

内置命令由 command_executor 直接处理，不调用外部脚本。

| 命令 | action | 关键参数 | 说明 |
|------|--------|----------|------|
| `help` | help | name(可选) | 显示帮助信息或查看指定指令详情 |
| `clear-chapter` | clear-chapter | chapter | 一步清理指定章节的场景+事实+伏笔 |
| `detect-fact-changes` | detect-fact-changes | content, chapter(可选), genre(可选) | 从章节内容检测事实变更 |

### detect-fact-changes 参数详解

- `content`: 章节内容（必填）
- `chapter`: 当前章节号（可选，省略时自动推断）
- `genre`: 题材类型 fantasy/urban/wuxia/scifi（可选，默认fantasy）

返回结构:
```json
{
  "chapter": 15,
  "extracted_entities": ["林风", "青云宗", "筑基丹"],
  "current_facts_by_entity": {
    "林风": [
      {"attribute": "境界", "value": "练气九层", "importance": "permanent", "chapter": 10}
    ]
  },
  "total_entities": 3,
  "total_facts": 5,
  "analysis_hint": "对比章节内容与现有事实，识别三类变更..."
}
```

智能体收到返回后，对比章节内容与 current_facts_by_entity，识别:
1. 新事实: 内容中有但事实库无记录 -> `set-fact` 录入
2. 更新事实: 同属性值已变 -> `set-fact` 更新（自动supersede旧值）
3. 冲突事实: 内容与已有事实矛盾 -> 判断是情节需要还是写作错误
