# 记忆提取 Skill

自动从对话中提取 Entity/Relation/Observation 并更新知识图谱。

## 功能

1. **实体提取** - 从对话中识别用户、项目、技能、偏好等实体
2. **关系提取** - 识别实体之间的关系
3. **观察提取** - 提取原子化事实作为观察
4. **自动更新** - 写入知识图谱存储

## 使用方法

### 手动调用

```python
from scripts.knowledge_graph_manager import KnowledgeGraphManager

manager = KnowledgeGraphManager()

# 创建实体
manager.create_entities([
    {'name': '新项目', 'entityType': 'project', 'observations': ['描述']}
])

# 创建关系
manager.create_relations([
    {'from': '用户', 'to': '新项目', 'relationType': 'owns'}
])

# 添加观察
manager.add_observations([
    {'entityName': '用户', 'contents': ['新偏好']}
])
```

### 自动提取规则

Agent 在对话中应主动识别以下信息并写入记忆：

#### 实体类型

| entityType | 识别信号 | 示例 |
|------------|----------|------|
| `user` | "我是"、"我的" | "我叫张三" → 创建用户实体 |
| `project` | "项目"、"做个"、"创建" | "做个看板" → 创建项目实体 |
| `skill` | "技能"、"能力" | "我有飞书技能" → 创建技能实体 |
| `tool` | "用"、"使用" | "用 yfinance" → 创建工具实体 |
| `preference` | "喜欢"、"偏好"、"想" | "喜欢深色风格" → 创建偏好实体 |
| `location` | "在"、"位于" | "在北京" → 创建地点实体 |
| `event` | "今天"、"时间点" | "2026-03-06 初次对话" → 创建事件实体 |

#### 关系类型

| relationType | 识别信号 | 示例 |
|--------------|----------|------|
| `owns` | "我的"、"我做的" | 用户 owns 项目 |
| `uses` | "用"、"使用" | 项目 uses 工具 |
| `prefers` | "喜欢"、"偏好" | 用户 prefers 偏好 |
| `located_at` | "在"、"位于" | 用户 located_at 地点 |
| `named` | "叫"、"命名" | 用户 named Agent |
| `created_on` | "创建时间" | 项目 created_on 时间 |
| `deployed_to` | "部署到" | 项目 deployed_to 平台 |

#### 观察提取

观察应该是**原子化事实**：
- 一条观察 = 一个事实
- 简洁、具体、可验证

**示例**：
- ✅ "时区：Asia/Shanghai"
- ✅ "邮箱：user@example.com"
- ❌ "用户信息包括时区和邮箱"（不是原子化）

## 记忆更新流程

```
对话开始
    ↓
读取知识图谱 (search_nodes / read_graph)
    ↓
对话进行中
    ↓
识别新信息 → 提取 Entity/Relation/Observation
    ↓
写入知识图谱 (create_entities / create_relations / add_observations)
    ↓
对话结束
    ↓
导出 Markdown 视图
```

## System Prompt 集成

在 Agent 的 System Prompt 中添加：

```
## 记忆管理

每次对话开始时：
1. 说 "正在回忆..." 并从知识图谱检索相关信息
2. 将知识图谱称为 "记忆"

对话过程中：
主动识别并记录以下类型的信息：
- Basic Identity: 年龄、性别、位置、职业、教育
- Behaviors: 兴趣、习惯
- Preferences: 交流风格、语言偏好
- Goals: 目标、期望
- Relationships: 人际关系（3 度以内）

发现新信息时：
1. 创建实体（用户、项目、技能、工具、偏好、地点、事件）
2. 创建关系（owns, uses, prefers, located_at, named 等）
3. 添加观察（原子化事实）
```

## 文件位置

- 管理器: `scripts/knowledge_graph_manager.py`
- 存储: `memory/knowledge-graph.jsonl`
- 视图: `memory/KNOWLEDGE_GRAPH.md`

---

*基于 MCP Memory Server 设计*