# 记忆数据格式规范

## 概览

本文档定义长期记忆的数据存储格式，支持灵活的多维度分类和检索。

## 数据结构

### 完整格式

```json
{
  "memory_id": "唯一标识（可选，自动生成UUID）",
  "content": "记忆内容描述（必需）",
  "category": "分类（可选，默认：general）",
  "role": "角色标识（可选）",
  "project": "项目名称（可选）",
  "event": "事件名称（可选）",
  "status": "状态（可选，默认：pending）",
  "priority": "优先级（可选，默认：medium）",
  "tags": ["标签列表（可选）"],
  "context": {
    "自定义上下文（可选，支持任意JSON结构）": ""
  },
  "metadata": {
    "自定义元数据（可选，支持任意JSON结构）": ""
  }
}
```

### 字段说明

#### 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| content | String | 记忆的核心内容描述，最大 2000 字符 |

#### 可选字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| memory_id | String | 自动生成 | 唯一标识符，UUID v4 格式 |
| category | String | general | 分类标识 |
| role | String | 空 | 角色标识 |
| project | String | 空 | 项目名称 |
| event | String | 空 | 事件名称 |
| status | String | pending | 状态标识 |
| priority | String | medium | 优先级 |
| tags | Array | [] | 标签列表 |
| context | Object | {} | 上下文信息，任意 JSON 结构 |
| metadata | Object | {} | 元数据，任意 JSON 结构 |

## 维度定义

### 1. 分类（category）

用于区分记忆的类型。

**推荐值**：

| 值 | 说明 | 示例场景 |
|-----|------|---------|
| task | 任务 | 待办事项、开发任务、运维任务 |
| project | 项目 | 项目信息、项目计划 |
| event | 事件 | 会议、活动、里程碑 |
| decision | 决策 | 技术决策、产品决策 |
| note | 笔记 | 临时记录、想法、灵感 |
| issue | 问题 | Bug、故障、问题记录 |
| knowledge | 知识 | 技术知识、最佳实践 |
| general | 通用 | 默认分类 |

### 2. 角色（role）

用于区分不同角色的记忆。

**推荐值**：

| 值 | 说明 |
|-----|------|
| pm | 产品经理 |
| dev | 开发人员 |
| designer | 设计师 |
| manager | 管理者 |
| ops | 运维人员 |
| qa | 测试人员 |
| user | 用户 |

### 3. 项目（project）

项目名称，用于按项目组织记忆。

**命名建议**：
- 使用简洁的标识符
- 多个单词用连字符连接
- 示例：`website-redesign`、`app-v2`、`backend-refactor`

### 4. 事件（event）

事件名称，用于关联特定事件或周期。

**命名建议**：
- 冲刺周期：`sprint-2024-q1`
- 发布版本：`release-2.0`
- 会议：`meeting-20240315`
- 活动名称：`hackathon-2024`

### 5. 状态（status）

记忆项的当前状态。

**推荐值**：

| 值 | 说明 |
|-----|------|
| pending | 待处理 |
| in_progress | 进行中 |
| completed | 已完成 |
| archived | 已归档 |
| cancelled | 已取消 |
| failed | 失败 |

### 6. 优先级（priority）

重要程度标识。

**推荐值**：

| 值 | 说明 |
|-----|------|
| high | 高优先级 |
| medium | 中优先级（默认） |
| low | 低优先级 |

### 7. 标签（tags）

自定义标签列表，用于灵活分类和检索。

**示例**：
```json
["urgent", "backend", "api", "jwt", "auth"]
```

## 使用示例

### 示例 1：任务记忆

```json
{
  "content": "完成用户认证模块重构，采用 JWT 令牌方案替换原有的 Session 机制",
  "category": "task",
  "role": "dev",
  "project": "website-redesign",
  "event": "sprint-2024-q1",
  "status": "completed",
  "priority": "high",
  "tags": ["backend", "auth", "jwt", "security"],
  "context": {
    "tech_stack": ["Python", "FastAPI", "Redis"],
    "estimated_hours": 16,
    "completed_date": "2024-03-15",
    "related_tasks": ["task-001", "task-002"]
  },
  "metadata": {
    "assignee": "张三",
    "reviewer": "李四",
    "pull_request": "https://github.com/xxx/pr/123",
    "commit": "abc123def456"
  }
}
```

### 示例 2：项目记忆

```json
{
  "content": "Website 重构项目，目标是在 Q2 完成前端技术栈升级，提升用户体验和开发效率",
  "category": "project",
  "project": "website-redesign",
  "status": "in_progress",
  "priority": "high",
  "tags": ["frontend", "react", "typescript", "migration"],
  "context": {
    "start_date": "2024-01-01",
    "target_date": "2024-06-30",
    "budget": "500k",
    "team_size": 8,
    "tech_stack": {
      "frontend": ["React", "TypeScript", "TailwindCSS"],
      "backend": ["Python", "FastAPI"],
      "database": ["PostgreSQL", "Redis"]
    }
  },
  "metadata": {
    "stakeholders": ["产品部", "技术部", "运营部"],
    "project_manager": "王五",
    "tech_lead": "李四"
  }
}
```

### 示例 3：事件记忆

```json
{
  "content": "2024 Q1 冲刺计划会议，确定本季度开发优先级和资源分配",
  "category": "event",
  "event": "sprint-2024-q1",
  "project": "website-redesign",
  "status": "completed",
  "tags": ["meeting", "planning", "quarterly"],
  "context": {
    "date": "2024-01-05",
    "duration": "2h",
    "participants": ["PM", "Tech Lead", "Devs", "QA"],
    "location": "会议室A"
  },
  "metadata": {
    "decisions": [
      "优先完成用户认证模块",
      "推迟支付模块开发到 Q2",
      "新增数据分析功能"
    ],
    "action_items": [
      "张三：完成认证模块设计",
      "李四：准备技术方案文档"
    ]
  }
}
```

### 示例 4：决策记忆

```json
{
  "content": "决定采用微服务架构重构后端系统，替换现有的单体架构",
  "category": "decision",
  "role": "manager",
  "project": "backend-refactor",
  "status": "completed",
  "priority": "high",
  "tags": ["architecture", "critical", "long-term"],
  "context": {
    "date": "2024-02-20",
    "reason": "现有单体架构无法支撑业务增长，维护成本过高",
    "alternatives": [
      {
        "option": "继续单体架构",
        "pros": "改动小，风险低",
        "cons": "无法解决根本问题"
      },
      {
        "option": "SOA架构",
        "pros": "成熟方案",
        "cons": "复杂度高，不够灵活"
      }
    ],
    "selected_approach": "微服务架构",
    "rationale": "更好的扩展性、独立部署、技术栈灵活"
  },
  "metadata": {
    "decision_makers": ["CTO", "架构师", "技术负责人"],
    "approval_date": "2024-02-25",
    "implementation_start": "2024-03-01"
  }
}
```

### 示例 5：问题记忆

```json
{
  "content": "生产环境数据库连接池耗尽导致服务不可用",
  "category": "issue",
  "role": "ops",
  "project": "website-redesign",
  "status": "completed",
  "priority": "high",
  "tags": ["incident", "database", "production", "critical"],
  "context": {
    "occurred_at": "2024-03-10T14:30:00",
    "duration": "45min",
    "affected_services": ["API服务", "用户中心"],
    "root_cause": "连接池配置过小，未正确释放连接"
  },
  "metadata": {
    "severity": "P1",
    "resolved_by": "李四",
    "solution": "增加连接池大小，修复连接泄漏问题",
    "preventive_actions": [
      "添加连接池监控",
      "定期检查连接使用情况"
    ]
  }
}
```

### 示例 6：知识记忆

```json
{
  "content": "Redis 缓存穿透、击穿、雪崩的区别和解决方案",
  "category": "knowledge",
  "role": "dev",
  "tags": ["redis", "cache", "performance", "best-practice"],
  "context": {
    "cache_penetration": {
      "definition": "查询不存在的数据，缓存和数据库都没有",
      "solution": "布隆过滤器、空值缓存"
    },
    "cache_breakdown": {
      "definition": "热点数据过期，大量请求直接打到数据库",
      "solution": "热点数据永不过期、互斥锁"
    },
    "cache_avalanche": {
      "definition": "大量缓存同时过期",
      "solution": "随机过期时间、多级缓存"
    }
  },
  "metadata": {
    "source": "技术分享会",
    "author": "张三",
    "date": "2024-03-12"
  }
}
```

## 验证规则

### 必需字段检查
```python
def validate_memory(memory_info):
    if not memory_info.get("content"):
        raise ValueError("content 是必需字段")
    if len(memory_info.get("content", "")) > 2000:
        raise ValueError("content 超过最大长度 2000")
    return True
```

### 枚举值验证（可选）
```python
VALID_CATEGORIES = ["task", "project", "event", "decision", "note", "issue", "knowledge", "general"]
VALID_PRIORITIES = ["high", "medium", "low"]
VALID_STATUSES = ["pending", "in_progress", "completed", "archived", "cancelled", "failed"]

def validate_enums(memory_info):
    if "category" in memory_info and memory_info["category"] not in VALID_CATEGORIES:
        print(f"⚠ category 建议使用以下值：{VALID_CATEGORIES}")
    
    if "priority" in memory_info and memory_info["priority"] not in VALID_PRIORITIES:
        print(f"⚠ priority 建议使用以下值：{VALID_PRIORITIES}")
    
    if "status" in memory_info and memory_info["status"] not in VALID_STATUSES:
        print(f"⚠ status 建议使用以下值：{VALID_STATUSES}")
    
    return True
```

## 使用建议

### 1. 命名规范
- project 和 event 使用连字符分隔：`website-redesign`、`sprint-2024-q1`
- tags 使用小写字母：`backend`、`api`、`jwt`
- 保持命名一致性，便于检索

### 2. 上下文设计
- context 存储结构化的背景信息
- 使用合理的嵌套层次，避免过深
- 为常用字段建立约定

### 3. 元数据管理
- metadata 存储额外的补充信息
- 可包含外部链接、关联ID等
- 支持后续扩展

### 4. 标签使用
- 标签用于灵活分类
- 控制标签数量，建议 3-5 个
- 使用有意义的标签名称

## 文件保存示例

```bash
# 创建记忆文件
cat > ./memory.json << 'EOF'
{
  "content": "完成API接口开发",
  "category": "task",
  "role": "dev",
  "project": "website-redesign",
  "status": "pending",
  "priority": "high"
}
EOF

# 保存记忆
python scripts/milvus_manager.py --action save --memory-file ./memory.json
```
