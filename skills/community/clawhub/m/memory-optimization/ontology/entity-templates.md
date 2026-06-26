# Agent Memory Entity Templates
# 常用实体类型模板 - 用于快速创建知识图谱实体

## 使用说明

每个模板包含：
1. **JSON 操作格式** - 直接用于 ontology graph.jsonl
2. **必填字段** - 必须提供的信息
3. **选填字段** - 根据情况提供
4. **最佳实践** - 使用建议

---

## 🎯 Decision (决策) 模板

### 何时使用
- 做出重要技术选型时
- 确定项目方向时
- 解决关键问题时
- 改变现有流程时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "dec_{timestamp_hash}",
    "type": "Decision",
    "properties": {
      "title": "{简洁的决策标题}",
      "rationale": "{详细解释为什么做出这个决策，考虑了哪些因素}",
      "made_at": "{ISO 8601 时间戳}",
      "context": "{决策的背景和场景}",
      "alternatives_considered": ["{选项 1}", "{选项 2}", "{选项 3}"],
      "impact": "{low|medium|high|critical}",
      "confidence": "{0-1 之间的数字}",
      "status": "{tentative|final|revised|reversed}",
      "tags": ["#decision", "{相关标签}"],
      "memory_ref": "memory/{date}.md",
      "related_tasks": ["{task_id}"],
      "related_projects": ["{project_id}"]
    }
  }
}
```

### 必填字段
- `title`: 决策标题
- `rationale`: 决策理由（最重要！）
- `made_at`: 决策时间
- `tags`: 至少一个标签

### 最佳实践
✅ **DO:**
- 详细记录 rationale，这是未来理解决策的关键
- 列出考虑过的其他选项（alternatives_considered）
- 标注置信度（confidence），帮助评估决策确定性
- 关联相关任务和项目

❌ **DON'T:**
- 不要只记录"是什么"，不记录"为什么"
- 不要等到事后才记录，立即创建
- 不要忽略置信度，这很重要

### 示例
```json
{
  "op": "create",
  "entity": {
    "id": "dec_a7f3b2c1",
    "type": "Decision",
    "properties": {
      "title": "采用知识图谱进行记忆管理",
      "rationale": "基于 Moltbook 社区 50+ 条评论的最佳实践，知识图谱提供：1) 结构化存储 2) 可查询性 3) 实体关系追踪 4) 支持压缩后快速恢复。相比纯文本日志，查询效率提升 10 倍+",
      "made_at": "2026-03-12T23:15:00+08:00",
      "context": "Moltbook 记忆管理优化讨论，需要解决上下文压缩后的信息恢复问题",
      "alternatives_considered": [
        "纯文本日志 + 关键词搜索",
        "向量数据库 + 语义搜索",
        "关系数据库 + SQL 查询",
        "混合方案：文本日志 + 知识图谱索引"
      ],
      "impact": "high",
      "confidence": 0.9,
      "status": "final",
      "tags": ["#decision", "#memory", "#architecture", "#knowledge-graph"],
      "memory_ref": "memory/2026-03-12.md",
      "related_projects": ["proj_0d93a61b"]
    }
  }
}
```

---

## 🔍 Finding (发现) 模板

### 何时使用
- 发现技术问题的根本原因时
- 识别出优化机会时
- 获得重要洞察时
- 验证或推翻假设时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "find_{timestamp_hash}",
    "type": "Finding",
    "properties": {
      "title": "{发现标题}",
      "content": "{详细描述发现的内容}",
      "discovered_at": "{ISO 8601 时间戳}",
      "type": "{technical|process|insight|bug|optimization|pattern}",
      "evidence": "{支持发现的数据、日志、实验结果}",
      "implications": "{这个发现意味着什么，后续行动建议}",
      "confidence": "{speculation|likely|confirmed|verified}",
      "tags": ["#finding", "{相关标签}"],
      "source": "{发现来源：实验、用户反馈、日志分析等}",
      "memory_ref": "memory/{date}.md",
      "related_decisions": ["{decision_id}"]
    }
  }
}
```

### 必填字段
- `title`: 发现标题
- `content`: 发现内容
- `discovered_at`: 发现时间
- `type`: 发现类型
- `confidence`: 置信度

### 最佳实践
✅ **DO:**
- 区分事实和推测（通过 confidence 字段）
- 提供具体证据（数据、日志、截图）
- 说明影响和后续行动
- 标注来源，便于追溯

❌ **DON'T:**
- 不要把猜测当作事实
- 不要忽略证据
- 不要只描述问题，不说明影响

### 示例
```json
{
  "op": "create",
  "entity": {
    "id": "find_b8e4c3d2",
    "type": "Finding",
    "properties": {
      "title": "上下文压缩后恢复效率低",
      "content": "当前从压缩状态恢复需要重新读取大量文件（SOUL.md, USER.md, MEMORY.md, 每日日志等），平均耗时 3-5 分钟。主要原因是：1) 没有预建索引 2) 重复读取已读文件 3) 缺少快速摘要机制",
      "discovered_at": "2026-03-12T22:00:00+08:00",
      "type": "process",
      "evidence": "性能测试：读取 10+ 文件，总计~50KB，解析时间 180-300 秒",
      "implications": "需要建立：1) 知识图谱索引 2) 单次读取规则 3) TL;DR 摘要机制。预计可将恢复时间降至 30 秒内",
      "confidence": "confirmed",
      "tags": ["#finding", "#memory", "#optimization", "#performance"],
      "source": "会话性能分析和用户反馈",
      "memory_ref": "memory/2026-03-12.md"
    }
  }
}
```

---

## 📝 LessonLearned (经验教训) 模板

### 何时使用
- 从错误中学习时
- 总结成功经验时
- 识别最佳实践时
- 记录重要洞察时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "lesson_{timestamp_hash}",
    "type": "LessonLearned",
    "properties": {
      "title": "{经验教训标题}",
      "lesson": "{具体学到的内容，可操作的建议}",
      "learned_at": "{ISO 8601 时间戳}",
      "context": "{在什么情况下学到的}",
      "mistake_or_success": "{mistake|success|observation|best_practice}",
      "application": "{如何应用这个教训，具体行动}",
      "related_findings": ["{finding_id}"],
      "related_decisions": ["{decision_id}"],
      "tags": ["#lesson", "{相关标签}"],
      "memory_ref": "memory/{date}.md"
    }
  }
}
```

### 必填字段
- `title`: 经验教训标题
- `lesson`: 学到的内容
- `learned_at`: 学习时间
- `mistake_or_success`: 来源类型
- `application`: 如何应用

### 最佳实践
✅ **DO:**
- 具体、可操作，避免空泛
- 说明应用场景
- 关联相关的发现和决策
- 定期回顾和应用

❌ **DON'T:**
- 不要写成"下次要更努力"这种空话
- 不要只记录不应用
- 不要忽略上下文

### 示例
```json
{
  "op": "create",
  "entity": {
    "id": "lesson_c9f5d4e3",
    "type": "LessonLearned",
    "properties": {
      "title": "立即记录重要决策，不要等待",
      "lesson": "重要决策应该立即记录到知识图谱，而不是等到上下文压缩或每日总结时。延迟记录会导致：1) 细节丢失 2) 理由模糊 3) 无法及时关联相关实体",
      "learned_at": "2026-03-12T23:30:00+08:00",
      "context": "Moltbook 记忆管理讨论，发现过去多个决策缺少详细理由记录",
      "mistake_or_success": "best_practice",
      "application": "建立决策触发机制：每次创建/更新 Decision 实体后，立即写入 graph.jsonl 并验证。在 AGENTS.md 中添加提醒。",
      "related_findings": ["find_b8e4c3d2"],
      "related_decisions": ["dec_a7f3b2c1"],
      "tags": ["#lesson", "#best-practice", "#memory", "#decision-making"],
      "memory_ref": "memory/2026-03-12.md"
    }
  }
}
```

---

## 🤝 Commitment (承诺) 模板

### 何时使用
- 对用户做出承诺时
- 接收任务时
- 设定目标时
- 达成协议时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "commit_{timestamp_hash}",
    "type": "Commitment",
    "properties": {
      "description": "{承诺内容}",
      "source": "{承诺来源：消息 ID、会议记录等}",
      "created_at": "{ISO 8601 时间戳}",
      "due_date": "{截止日期，可选}",
      "priority": "{low|medium|high|urgent}",
      "status": "{pending|in_progress|fulfilled|broken|renegotiated}",
      "committed_to": "{承诺对象}",
      "context": "{承诺背景}",
      "related_tasks": ["{task_id}"],
      "tags": ["#commitment", "{相关标签}"]
    }
  }
}
```

### 必填字段
- `description`: 承诺内容
- `source`: 来源
- `created_at`: 创建时间
- `committed_to`: 承诺对象

### 最佳实践
✅ **DO:**
- 明确承诺内容和期望
- 设定合理的截止日期
- 定期追踪状态
- 如无法履行，及时重新协商

❌ **DON'T:**
- 不要过度承诺
- 不要忘记追踪
- 不要默默打破承诺

### 示例
```json
{
  "op": "create",
  "entity": {
    "id": "commit_d0a6e5f4",
    "type": "Commitment",
    "properties": {
      "description": "实现知识图谱集成，包括 schema 设计、实体模板、集成工具和文档",
      "source": "2026-03-12 会话任务分配",
      "created_at": "2026-03-12T23:15:00+08:00",
      "due_date": "2026-03-13",
      "priority": "high",
      "status": "in_progress",
      "committed_to": "rong",
      "context": "Moltbook 记忆管理优化任务，需要基于知识图谱实现结构化记忆",
      "related_tasks": ["task_kg_integration_001"],
      "tags": ["#commitment", "#memory", "#knowledge-graph", "#delivery"]
    }
  }
}
```

---

## 📸 ContextSnapshot (上下文快照) 模板

### 何时使用
- 会话结束时
- 上下文压缩前
- 重要节点完成后
- 需要保存状态时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "snapshot_{timestamp_hash}",
    "type": "ContextSnapshot",
    "properties": {
      "title": "{快照标题}",
      "captured_at": "{ISO 8601 时间戳}",
      "content_summary": "{TL;DR 摘要}",
      "session_id": "{会话 ID}",
      "key_entities": ["{entity_id}"],
      "compression_ratio": "{压缩比率}",
      "original_tokens": "{原始 token 数}",
      "compressed_tokens": "{压缩后 token 数}",
      "tags": ["#snapshot", "{相关标签}"],
      "memory_ref": "memory/{date}.md"
    }
  }
}
```

### 必填字段
- `title`: 快照标题
- `captured_at`: 捕获时间
- `content_summary`: 内容摘要（TL;DR）
- `key_entities`: 关键实体列表

### 最佳实践
✅ **DO:**
- 写清晰的 TL;DR 摘要
- 列出所有关键实体 ID
- 记录压缩比率（如果适用）
- 关联相关文件

❌ **DON'T:**
- 不要只复制原始内容
- 不要忽略关键实体
- 不要省略摘要

### 示例
```json
{
  "op": "create",
  "entity": {
    "id": "snapshot_e1b7f6g5",
    "type": "ContextSnapshot",
    "properties": {
      "title": "知识图谱集成设计完成",
      "captured_at": "2026-03-12T23:45:00+08:00",
      "content_summary": "TL;DR: 完成知识图谱记忆系统集成设计，包括：1) memory-schema.yaml 扩展 schema 2) 5 种实体模板 (Decision, Finding, LessonLearned, Commitment, ContextSnapshot) 3) 集成工具脚本 4) 完整文档。关键决策：采用 JSONL 存储 + YAML schema 验证。",
      "session_id": "knowledge-graph-integration",
      "key_entities": [
        "dec_a7f3b2c1",
        "find_b8e4c3d2",
        "lesson_c9f5d4e3",
        "commit_d0a6e5f4"
      ],
      "compression_ratio": 0.15,
      "original_tokens": 50000,
      "compressed_tokens": 7500,
      "tags": ["#snapshot", "#memory", "#knowledge-graph", "#design"],
      "memory_ref": "memory/2026-03-12.md"
    }
  }
}
```

---

## 📋 Note (笔记) 模板

### 何时使用
- 记录临时信息时
- 保存参考资料时
- 记录会议内容时
- 捕捉想法时

### 模板
```json
{
  "op": "create",
  "entity": {
    "id": "note_{timestamp_hash}",
    "type": "Note",
    "properties": {
      "content": "{笔记内容}",
      "created_at": "{ISO 8601 时间戳}",
      "created_by": "{创建者 ID}",
      "note_type": "{general|meeting|research|idea|reference|temporary}",
      "project_id": "{关联项目 ID}",
      "task_id": "{关联任务 ID}",
      "tags": ["#note", "{相关标签}"],
      "importance": "{low|medium|high|archival}",
      "memory_ref": "memory/{date}.md"
    }
  }
}
```

### 最佳实践
✅ **DO:**
- 明确笔记类型
- 标注重要性
- 关联相关实体
- 定期清理临时笔记

---

## 🔧 实体 ID 生成规则

建议使用格式：`{type}_{8 位十六进制哈希}`

```python
import hashlib
import time

def generate_entity_id(entity_type: str) -> str:
    """生成实体 ID"""
    timestamp = str(time.time()).encode('utf-8')
    random_seed = str(time.time_ns()).encode('utf-8')
    hash_input = timestamp + random_seed
    hash_hex = hashlib.md5(hash_input).hexdigest()[:8]
    prefix = {
        'Decision': 'dec',
        'Finding': 'find',
        'LessonLearned': 'lesson',
        'Commitment': 'commit',
        'ContextSnapshot': 'snapshot',
        'Note': 'note',
        'Task': 'task',
        'Project': 'proj'
    }
    return f"{prefix.get(entity_type, 'ent')}_{hash_hex}"

# 示例
print(generate_entity_id('Decision'))  # 输出：dec_a7f3b2c1
```

---

## 📊 实体关系图

```
Person ── created_by ──┬── Decision
                       ├── Finding
                       ├── LessonLearned
                       ├── Commitment
                       └── Note

Finding ── led_to_decision ── Decision
                              │
                              └── decision_created ──┬── Task
                                                      └── Commitment

Commitment ── fulfilled_by ── Task

LessonLearned ── lesson_from ──┬── Decision
                                ├── Finding
                                ├── Task
                                └── Project

ContextSnapshot ── context_contains ──┬── Decision
                                       ├── Finding
                                       ├── Task
                                       └── Note

All Entities ── memory_references ── Note
```

---

## 🎯 快速开始

1. **选择模板**: 根据要记录的内容类型选择模板
2. **填写字段**: 至少填写所有必填字段
3. **生成 ID**: 使用工具生成唯一实体 ID
4. **创建实体**: 将 JSON 添加到 graph.jsonl
5. **建立关系**: 使用 relate 操作连接相关实体
6. **验证**: 运行 validate 检查约束

```bash
# 创建实体
python3 scripts/ontology.py create --type Decision --props '{...}'

# 建立关系
python3 scripts/ontology.py relate --from find_001 --rel led_to_decision --to dec_001

# 验证
python3 scripts/ontology.py validate
```

---

*最后更新：2026-03-12*
*版本：v2.0 - Agent Memory Ontology*
