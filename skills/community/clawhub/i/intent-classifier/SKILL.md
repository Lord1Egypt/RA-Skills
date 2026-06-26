---
name: intent-classifier
description: 意图分类器 - 原创技能。实时分析用户输入，识别真实意图并路由到对应处理流程。支持代码、提问、请求、闲聊等类型识别，适用于AI助手任务调度、智能路由、对话理解等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [intent, classification, routing, nlp, understanding]
version: 1.0.0
author: laosi
source: original
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 功能原创且实用
- [x] 分类体系完整
- [x] 路由逻辑明确
- [x] 无语法错误

---

# Intent Classifier - 意图分类器

> 原创技能 | 激活词: 识别意图 / 分类任务 / 智能路由

## 核心功能

实时分析用户输入，识别真实意图并路由到对应处理流程。

## 意图分类体系

### 一级分类 (4类)

| 类型 | 标识 | 特征词 |
|------|------|--------|
| **代码类** | CODE | 写代码、修复、创建、调试、测试 |
| **知识类** | KNOW | 是什么、为什么、如何、解释 |
| **任务类** | TASK | 帮我、请、帮我做、执行 |
| **闲聊类** | CHAT | 随便聊聊、你好、今天天气 |

### 二级分类 (扩展)

```
CODE:
├── 编写 (write) → 新建文件/功能
├── 修复 (fix) → Bug修复
├── 审查 (review) → 代码审查
├── 测试 (test) → 编写测试
└── 重构 (refactor) → 重构代码

KNOW:
├── 定义 (define) → 解释概念
├── 教程 (tutorial) → 学习路径
├── 对比 (compare) → 比较差异
└── 建议 (advice) → 给出建议

TASK:
├── 文件操作 → 读取/写入/删除
├── 命令执行 → 运行脚本/命令
├── 搜索查询 → 搜索信息
└── 流程编排 → 多步骤任务

CHAT:
├── 问候 (greeting) → 打招呼
├── 反馈 (feedback) → 表达情绪
├── 澄清 (clarify) → 追问细节
└── 结束 (close) → 结束对话
```

## 识别算法

### 关键词匹配

```python
def classify_intent(text: str) -> Intent:
    text_lower = text.lower()
    
    # 代码类关键词
    code_keywords = ['写', '代码', 'function', 'class', 'def', 'fix', 'bug', 'test']
    if any(kw in text_lower for kw in code_keywords):
        return Intent(type='CODE', sub='write' if '写' in text else 'fix')
    
    # 知识类关键词
    know_keywords = ['是什么', '为什么', '如何', '解释', '什么']
    if any(kw in text_lower for kw in know_keywords):
        return Intent(type='KNOW', sub='define')
    
    # 任务类关键词
    task_keywords = ['帮我', '请', '执行', '做']
    if any(kw in text_lower for kw in task_keywords):
        return Intent(type='TASK', sub='general')
    
    # 默认闲聊类
    return Intent(type='CHAT', sub='general')
```

### 模式识别

```python
# 复杂模式
patterns = [
    (r'^写一个.*', 'CODE:write'),
    (r'^修复.*bug', 'CODE:fix'),
    (r'^.*是什么', 'KNOW:define'),
    (r'^帮我.*', 'TASK:general'),
    (r'^(hi|你好|hey)', 'CHAT:greeting'),
]
```

## 置信度计算

```python
class IntentResult:
    type: str        # 一级分类
    sub: str         # 二级分类
    confidence: float  # 置信度 0-1
    features: list   # 触发特征
    alternative: list # 备选分类
```

### 置信度规则

| 条件 | 置信度调整 |
|------|-----------|
| 明确关键词 | +0.3 |
| 完整句子结构 | +0.2 |
| 无歧义 | +0.2 |
| 短文本 (<10字) | -0.2 |
| 多关键词冲突 | -0.3 |

## 路由策略

### 直接路由

```python
def route(intent: IntentResult) -> Skill:
    if intent.type == 'CODE':
        if intent.sub == 'write':
            return 'karpathy-principles'  # Karpathy法则
        elif intent.sub == 'fix':
            return 'workflow-verifier'     # 工作流验证
    elif intent.type == 'TASK':
        return 'auto-learn-skill'          # 自动学习
    elif intent.type == 'KNOW':
        return 'mempalace-assistant'       # 记忆搜索
    else:
        return 'general-chat'              # 闲聊模式
```

### 技能推荐

| 意图 | 推荐技能 |
|------|---------|
| 写代码 | karpathy-principles |
| 修复Bug | workflow-verifier |
| 学习知识 | mempalace-assistant |
| 积累经验 | auto-learn-skill |
| 熵管理 | entropy-manager |
| 通用任务 | skill-creator |

## 输出格式

```markdown
## 意图识别结果

### 分类
- **一级类型**: CODE
- **二级类型**: write
- **置信度**: 0.87

### 触发特征
- "写" 关键词
- 完整需求描述
- 代码相关语境

### 路由建议
→ karpathy-principles (Karpathy编程法则)

### 备选
- workflow-verifier (置信度0.12)
```

## 应用场景

1. **智能助手调度** - 自动选择最佳处理技能
2. **多技能编排** - 复杂任务分解路由
3. **对话理解** - 深度语义分析
4. **任务分类** - 自动归类用户请求

## 集成建议

将本技能与以下技能配合使用：

```markdown
## 协作技能

- karpathy-principles: 代码生成路由
- workflow-verifier: Bug修复路由
- mempalace-assistant: 知识查询路由
- auto-learn-skill: 经验积累路由
- entropy-manager: 会话熵管理
```

## 原创性声明

本技能为原创，融合了：
- 自然语言处理意图识别
- 技能路由系统设计
- AI Agent任务调度
- 模式匹配算法

---

**作者**: laosi
**创建日期**: 2026-04-28