---
name: long-term-task-memory
description: 按需调用火山引擎 Milvus 向量数据库进行长期记忆存储与检索，支持灵活的数据格式区分角色、事件、项目等维度；当用户明确要求保存、查询、更新或删除长期记忆时使用
dependency:
  python:
    - pymilvus==2.3.0
---

# 长期任务记忆管理

## 功能说明

本 Skill 提供火山引擎 Milvus 向量数据库的操作能力，用于长期记忆的存储与检索。

**核心能力**：
- 建立连接：连接到 Milvus 数据库实例
- 存储记忆：保存任务、事件、项目等信息到向量数据库
- 查询搜索：按条件检索历史记忆
- 更新记录：修改已存储的记忆信息
- 删除记录：清理不需要的记忆

**使用方式**：当用户明确要求"保存到长期记忆"、"查询历史任务"、"更新记忆状态"、"删除记录"等操作时调用。

## 前置准备

### 环境配置

编辑 `.env` 文件，填写 Milvus 连接信息：
```bash
# Milvus 实例访问地址
MILVUS_URI=http://your-instance.milvus.ivolces.com:19530

# Milvus 认证令牌（格式：Username:Password）
MILVUS_TOKEN=root:yourpassword
```

`.env` 文件加载优先级：
1. 脚本所在目录（`scripts/.env`）
2. 当前工作目录（`./.env`）
3. Skill 根目录（`long-term-task-memory/.env`）

**获取配置信息**：
1. 登录火山引擎控制台
2. 进入向量数据库 Milvus 服务
3. 创建或选择实例
4. 在实例详情页获取访问地址（URI）
5. 使用实例的用户名和密码组成 Token

## 数据格式

### 灵活的数据结构

支持多维度区分的灵活数据格式：

```json
{
  "memory_id": "唯一标识（可选，自动生成）",
  "content": "记忆内容描述",
  "category": "分类（task/event/project/note等）",
  "role": "角色标识（如：pm/dev/manager等）",
  "project": "项目名称",
  "event": "事件名称",
  "status": "状态（pending/in_progress/completed等）",
  "priority": "优先级（high/medium/low）",
  "tags": ["标签1", "标签2"],
  "context": {
    "自定义上下文信息": "支持任意JSON结构"
  },
  "metadata": {
    "自定义元数据": "支持任意JSON结构"
  }
}
```

### 维度说明

| 维度 | 字段 | 说明 | 示例值 |
|------|------|------|--------|
| 分类 | category | 记忆类型 | task、event、project、note、decision |
| 角色 | role | 相关角色 | pm、dev、manager、designer |
| 项目 | project | 所属项目 | website-redesign、app-v2 |
| 事件 | event | 相关事件 | sprint-2024-q1、release-2.0 |
| 状态 | status | 当前状态 | pending、in_progress、completed、archived |
| 优先级 | priority | 重要程度 | high、medium、low |
| 标签 | tags | 自定义标签 | ["urgent", "backend", "api"] |
| 上下文 | context | 背景信息 | 任意 JSON 结构 |
| 元数据 | metadata | 额外信息 | 任意 JSON 结构 |

## 操作手册

### 1. 建立连接

**功能**：初始化数据库连接并创建集合（如不存在）

**命令**：
```bash
python scripts/milvus_manager.py --action init
```

**参数**：
- `--action init`：执行初始化操作
- `--collection`：集合名称（可选，默认：task_memory）
- `--recreate`：是否重建集合（可选，会删除现有数据）

**示例**：
```bash
# 初始化默认集合
python scripts/milvus_manager.py --action init

# 初始化指定集合
python scripts/milvus_manager.py --action init --collection project_memory

# 重建集合（清空数据）
python scripts/milvus_manager.py --action init --recreate
```

**输出**：
```
✓ 已加载环境配置文件：/path/to/.env
✓ 成功连接到 Milvus 实例：http://your-instance.milvus.ivolces.com:19530
✓ 成功创建集合：task_memory
```

---

### 2. 存储记忆

**功能**：将记忆信息保存到数据库

**命令**：
```bash
python scripts/milvus_manager.py --action save --memory-file <文件路径>
```

**参数**：
- `--action save`：执行保存操作
- `--memory-file`：记忆信息文件路径（JSON 格式）
- `--collection`：集合名称（可选）

**准备记忆文件**：

创建 `memory.json` 文件：
```json
{
  "content": "完成用户认证模块的重构，采用 JWT 令牌方案",
  "category": "task",
  "role": "dev",
  "project": "website-redesign",
  "event": "sprint-2024-q1",
  "status": "completed",
  "priority": "high",
  "tags": ["backend", "auth", "jwt"],
  "context": {
    "tech_stack": ["Python", "FastAPI"],
    "estimated_hours": 16,
    "completed_date": "2024-03-15"
  },
  "metadata": {
    "assignee": "张三",
    "reviewer": "李四",
    "related_docs": ["api-docs.md", "auth-guide.md"]
  }
}
```

**示例**：
```bash
# 保存记忆
python scripts/milvus_manager.py --action save --memory-file ./memory.json

# 保存到指定集合
python scripts/milvus_manager.py --action save --memory-file ./memory.json --collection project_memory
```

**输出**：
```
✓ 已加载环境配置文件：/path/to/.env
✓ 成功连接到 Milvus 实例：http://your-instance.milvus.ivolces.com:19530
✓ 任务已保存，ID：550e8400-e29b-41d4-a716-446655440000
```

**更多示例**：

```json
// 项目记忆
{
  "content": "Website 重构项目，目标是在 Q2 完成前端升级",
  "category": "project",
  "project": "website-redesign",
  "status": "in_progress",
  "priority": "high",
  "tags": ["frontend", "react", "typescript"],
  "context": {
    "start_date": "2024-01-01",
    "target_date": "2024-06-30",
    "budget": "500k"
  }
}

// 事件记忆
{
  "content": "2024 Q1 冲刺计划会议，确定优先级排序",
  "category": "event",
  "event": "sprint-2024-q1",
  "project": "website-redesign",
  "tags": ["meeting", "planning"],
  "context": {
    "date": "2024-01-05",
    "participants": ["PM", "Tech Lead", "Devs"],
    "decisions": ["优先完成用户认证", "推迟支付模块"]
  }
}

// 决策记忆
{
  "content": "决定采用微服务架构重构后端系统",
  "category": "decision",
  "role": "manager",
  "project": "backend-refactor",
  "tags": ["architecture", "critical"],
  "context": {
    "date": "2024-02-20",
    "reason": "现有单体架构无法支撑业务增长",
    "alternatives": ["继续单体架构", "SOA架构"]
  }
}
```

---

### 3. 查询搜索

**功能**：按条件检索历史记忆

**命令**：
```bash
python scripts/milvus_manager.py --action query [过滤参数]
```

**参数**：
- `--action query`：执行查询操作
- `--category`：按分类过滤
- `--role`：按角色过滤
- `--project`：按项目过滤
- `--event`：按事件过滤
- `--status`：按状态过滤
- `--priority`：按优先级过滤
- `--limit`：返回数量限制（默认：10）
- `--collection`：集合名称（可选）

**示例**：

```bash
# 查询所有待处理的任务
python scripts/milvus_manager.py --action query --status pending

# 查询特定项目的所有记忆
python scripts/milvus_manager.py --action query --project website-redesign

# 查询开发角色的任务
python scripts/milvus_manager.py --action query --role dev --category task

# 查询特定事件的相关记忆
python scripts/milvus_manager.py --action query --event sprint-2024-q1

# 组合查询：高优先级的进行中任务
python scripts/milvus_manager.py --action query --status in_progress --priority high

# 查询最近 20 条记录
python scripts/milvus_manager.py --action query --limit 20
```

**输出**：
```
✓ 已加载环境配置文件：/path/to/.env
✓ 成功连接到 Milvus 实例：http://your-instance.milvus.ivolces.com:19530
✓ 查询到 3 个任务

查询结果：
[
  {
    "memory_id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "完成用户认证模块的重构",
    "category": "task",
    "role": "dev",
    "project": "website-redesign",
    "status": "completed",
    "priority": "high",
    "created_at": "2024-03-15T10:30:00",
    "tags": ["backend", "auth"]
  },
  ...
]
```

**获取单条记忆详情**：
```bash
python scripts/milvus_manager.py --action get --memory-id <记忆ID>
```

---

### 4. 更新记录

**功能**：修改已存储记忆的状态或内容

**命令**：
```bash
python scripts/milvus_manager.py --action update --memory-id <ID> --status <新状态>
```

**参数**：
- `--action update`：执行更新操作
- `--memory-id`：记忆唯一标识
- `--status`：新状态值
- `--collection`：集合名称（可选）

**示例**：

```bash
# 更新任务状态为完成
python scripts/milvus_manager.py --action update \
  --memory-id 550e8400-e29b-41d4-a716-446655440000 \
  --status completed

# 更新任务状态为进行中
python scripts/milvus_manager.py --action update \
  --memory-id 550e8400-e29b-41d4-a716-446655440000 \
  --status in_progress
```

**输出**：
```
✓ 已加载环境配置文件：/path/to/.env
✓ 成功连接到 Milvus 实例：http://your-instance.milvus.ivolces.com:19530
✓ 找到任务：550e8400-e29b-41d4-a716-446655440000
✓ 任务已保存，ID：550e8400-e29b-41d4-a716-446655440000
✓ 任务状态已更新：550e8400-e29b-41d4-a716-446655440000 -> completed
```

---

### 5. 删除记录

**功能**：从数据库中移除记忆

**命令**：
```bash
python scripts/milvus_manager.py --action delete --memory-id <ID>
```

**参数**：
- `--action delete`：执行删除操作
- `--memory-id`：记忆唯一标识
- `--collection`：集合名称（可选）

**示例**：
```bash
# 删除指定记忆
python scripts/milvus_manager.py --action delete \
  --memory-id 550e8400-e29b-41d4-a716-446655440000
```

**输出**：
```
✓ 已加载环境配置文件：/path/to/.env
✓ 成功连接到 Milvus 实例：http://your-instance.milvus.ivolces.com:19530
✓ 任务已删除：550e8400-e29b-41d4-a716-446655440000
```

---

## 使用场景

### 场景 1：项目任务管理

**用户**："把网站重构项目的任务保存到长期记忆"

**执行**：
1. 提取任务信息
2. 创建记忆文件（category=task, project=website-redesign）
3. 调用存储命令

### 场景 2：按项目查询历史

**用户**："查询 website-redesign 项目的所有记忆"

**执行**：
```bash
python scripts/milvus_manager.py --action query --project website-redesign --limit 50
```

### 场景 3：按角色查询任务

**用户**："查看开发人员（dev）的所有待处理任务"

**执行**：
```bash
python scripts/milvus_manager.py --action query --role dev --status pending
```

### 场景 4：更新任务进度

**用户**："将任务 xxx 标记为完成"

**执行**：
```bash
python scripts/milvus_manager.py --action update --memory-id xxx --status completed
```

### 场景 5：记录决策

**用户**："记录这次架构决策到长期记忆"

**执行**：
1. 提取决策内容
2. 创建记忆文件（category=decision）
3. 调用存储命令

---

## 资源索引

- **环境配置文件**：[.env](.env)
- **操作脚本**：[scripts/milvus_manager.py](scripts/milvus_manager.py)
- **格式参考**：[references/memory-format.md](references/memory-format.md)

## 注意事项

### 配置要求
- 使用前必须配置 `.env` 文件
- 如果配置不完整，脚本会提示缺少的配置项
- `.env` 文件支持多个位置自动加载

### 数据管理
- 合理使用分类、角色、项目等维度便于检索
- 使用标签增加灵活性
- 定期清理不需要的记忆
- 重要数据建议备份

### 性能优化
- 查询时使用合理的过滤条件
- 避免返回过多结果（合理设置 limit）
- 为常用查询维度建立索引
