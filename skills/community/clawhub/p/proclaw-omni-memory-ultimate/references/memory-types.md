# Memory Types - 4类型分类标准

## 概述

Omni-Memory采用四种记忆类型分类，基于信息用途而非时间维度，实现精准存储和高效检索。

## 类型定义

| 类型 | 目录 | 内容 | 示例 |
|------|------|------|------|
| **user** | memory/user/ | 用户画像、偏好、角色 | "用户是数据分析师，偏好简洁回复" |
| **feedback** | memory/feedback/ | 纠正、确认、风格指导 | "不要用Markdown表格，用列表" |
| **project** | memory/project/ | 项目状态、决策、推理 | "项目采用React因为降低学习成本" |
| **reference** | memory/reference/ | 外部资源、工具、位置 | "项目文档在 /docs/api/" |

---

## Type 1: User Memory

### 定义
关于用户本身的永久性信息，描述"用户是谁"和"用户喜欢什么"。

### 包含内容

#### 用户画像
- 姓名/称呼
- 职业角色
- 技术背景
- 知识领域

#### 用户偏好
- 沟通风格（简洁/详细）
- 输出格式（列表/表格/代码）
- 工作习惯
- 时区

#### 用户目标
- 长期目标
- 当前任务
- 期望结果

### 存储示例

```markdown
---
name: user-profile
description: 用户角色和核心偏好
type: user
created: 2026-04-06
---

## 用户画像
- 角色: 数据分析师
- 技术栈: Python, SQL, Tableau
- 背景: 3年数据分析经验

## 沟通偏好
- 风格: 简洁直接
- 格式: 优先代码示例，避免长篇解释
- 语言: 中文技术术语保留英文

## 工作习惯
- 时区: UTC+8
- 工作时间: 9:00-18:00

## 应用方式
当回复时，保持简洁，提供代码示例，使用中文混合英文术语。
```

### 触发条件

```
用户说: "我是..."
用户说: "我喜欢..."
用户说: "我的工作是..."
用户说: "我习惯..."
用户说: "请记住我是..."
```

---

## Type 2: Feedback Memory

### 定义
用户对Agent行为的反馈，包括纠正和确认，用于优化未来交互。

### 包含内容

#### 纠正 (Correction)
- 错误的理解
- 错误的方法
- 错误的格式

#### 确认 (Confirmation)
- 正确的行为
- 有效的风格
- 有用的输出

#### 风格指导 (Style Guide)
- 输出格式偏好
- 语言风格
- 细节程度

### 存储示例

```markdown
---
name: no-tables
description: 偏好列表而非Markdown表格
type: feedback
created: 2026-04-06
---

## 纠正内容
用户纠正: 不要用Markdown表格，用列表展示信息。

## 原因
表格在移动端显示不佳，列表更易阅读。

## 应用方式
当需要展示结构化信息时，使用列表格式而非表格。
避免: | 列1 | 列2 |
使用: - 项目1: 描述
```

```markdown
---
name: concise-style
description: 确认简洁回复风格有效
type: feedback
created: 2026-04-06
---

## 确认内容
用户确认: "是的，这正是我想要的，保持简洁"

## 原因
简洁的代码示例比长篇解释更符合用户需求。

## 应用方式
继续使用简洁的回复风格，代码优先，解释精简。
```

### 触发条件

```
用户说: "不对，应该是..."
用户说: "不是这样的..."
用户说: "不要..."
用户说: "是的，就是这样"
用户说: "很好，保持这样"
用户说: "下次请..."
```

### 重要原则

> **记录成功也记录失败**
> 
> 只保存纠正会让Agent过于谨慎，也要保存确认以强化正确行为。

---

## Type 3: Project Memory

### 定义
关于项目/任务的信息，包括决策、状态和推理过程。

### 包含内容

#### 决策 (Decision)
- 技术选型
- 架构设计
- 方案选择
- **决策原因**（关键）

#### 状态 (Status)
- 当前进度
- 已完成事项
- 待办事项
- 阻塞问题

#### 推理 (Reasoning)
- 为什么选择A而非B
- 权衡考量
- 假设前提

### 存储示例

```markdown
---
name: react-decision
description: 项目选择React作为前端框架
type: project
created: 2026-04-06
---

## 决策内容
项目采用React作为前端框架，不使用Vue。

## 原因
1. 用户熟悉React生态
2. 团队有React开发经验
3. 项目需要的组件库React版本更成熟

## 权衡
- Vue: 学习曲线更平缓，但团队经验不足
- React: 生态更丰富，团队熟悉度高

## 应用方式
当讨论前端架构、组件设计时，默认使用React方案。
相关工具: React DevTools, Redux, React Router
```

```markdown
---
name: api-design
description: API采用RESTful风格
type: project
created: 2026-04-06
---

## 决策内容
后端API采用RESTful风格设计，不使用GraphQL。

## 原因
1. 项目是标准CRUD场景
2. 团队对REST更熟悉
3. 无复杂查询需求

## 应用方式
设计API时遵循RESTful原则，使用标准HTTP方法。
URL格式: /api/v1/resource/{id}
```

### 触发条件

```
用户说: "我们用...吧"
用户说: "决定用..."
用户说: "选择..."
用户说: "项目需要..."
用户说: "因为..."
```

### 重要原则

> **记录推理过程**
> 
> 项目记忆衰减快，记录"为什么"帮助未来判断记忆是否仍然有效。

---

## Type 4: Reference Memory

### 定义
指向外部资源的引用，包括文件位置、工具、链接等。

### 包含内容

#### 文件位置
- 项目文档路径
- 配置文件位置
- 数据存储位置

#### 工具资源
- 使用的工具
- API端点
- 服务地址

#### 外部链接
- 参考文档
- 相关资源
- 代码仓库

### 存储示例

```markdown
---
name: project-docs
description: 项目文档位置
type: reference
created: 2026-04-06
---

## 文档位置
- API文档: /docs/api/
- 设计文档: /docs/design/
- 配置文件: /config/

## 重要文件
- 主配置: /config/app.yaml
- 数据库配置: /config/database.yaml

## 应用方式
当用户询问文档位置或需要查阅配置时，指向以上路径。
```

```markdown
---
name: external-services
description: 项目使用的第三方服务
type: reference
created: 2026-04-06
---

## 服务列表
- 数据库: PostgreSQL (localhost:5432)
- 缓存: Redis (localhost:6379)
- 消息队列: RabbitMQ (localhost:5672)

## API Keys位置
- 存储在: ~/.env
- 格式: SERVICE_NAME_API_KEY=xxx

## 应用方式
当配置或调试时，参考以上服务信息。
```

### 触发条件

```
用户说: "文档在..."
用户说: "配置文件是..."
用户说: "我们用的是..."
用户说: "服务地址是..."
```

---

## 分类判断流程

```python
def classify_memory(content, context):
    """
    判断记忆类型
    """
    
    # 1. 检查是否关于用户本身
    if is_about_user(content):
        return "user"
    
    # 2. 检查是否是纠正或确认
    if is_correction(content) or is_confirmation(content):
        return "feedback"
    
    # 3. 检查是否是项目决策
    if is_decision(content) or is_project_state(content):
        return "project"
    
    # 4. 检查是否是外部引用
    if is_reference(content):
        return "reference"
    
    # 5. 默认类型
    return "other"
```

### 判断关键词

| 类型 | 关键词 |
|------|--------|
| user | 我、我的、我是、我喜欢、我习惯 |
| feedback | 不对、不是、应该是、不要、很好、保持 |
| project | 决定、选择、采用、项目、方案、因为 |
| reference | 在、位置、路径、地址、链接、文档 |

---

## 与时间维度配合

四种类型与时间维度（Sensory/STM/WM/LTM）正交：

```
         ┌──────────────────────────────────────┐
         │           Temporal Dimension          │
         │                                      │
    ┌────┴────┬─────────┬──────────┬───────────┐
    │Sensory  │Short-Term│Working  │Long-Term  │
    │(0.25s)  │(10 turns)│(7 days) │(Permanent)│
    ├─────────┼─────────┼──────────┼───────────┤
    │ user    │    -    │  daily/  │ memory/   │
    │         │         │          │  user/    │
    ├─────────┼─────────┼──────────┼───────────┤
    │feedback │    -    │  daily/  │ memory/   │
    │         │         │          │  feedback/│
    ├─────────┼─────────┼──────────┼───────────┤
    │ project │    -    │  daily/  │ memory/   │
    │         │         │          │  project/ │
    ├─────────┼─────────┼──────────┼───────────┤
    │reference│    -    │  daily/  │ memory/   │
    │         │         │          │  reference│
    └─────────┴─────────┴──────────┴───────────┘
              Content Dimension (4 Types)
```

---

## 检索策略

### 按类型检索

```bash
# 只检索用户相关
python memory_core.py recall --query "用户偏好" --type user

# 只检索项目决策
python memory_core.py recall --query "前端框架" --type project

# 只检索纠正
python memory_core.py recall --query "格式" --type feedback
```

### 混合检索

```python
def smart_recall(query):
    """
    智能检索：根据查询自动判断类型
    """
    # 用户相关查询 → 优先user类型
    if "我" in query or "用户" in query:
        return recall(query, type="user")
    
    # 历史查询 → 优先project类型
    if "之前" in query or "决定" in query:
        return recall(query, type="project")
    
    # 位置查询 → 优先reference类型
    if "在哪" in query or "位置" in query:
        return recall(query, type="reference")
    
    # 默认全局搜索
    return recall(query)
```

---

*Memory Types Version: 1.0*
*Based on: Claude Code Memory Architecture + Atkinson-Shiffrin Model*
