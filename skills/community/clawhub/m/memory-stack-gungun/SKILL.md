---
name: memory-stack
description: AI 记忆栈架构 - 符合 2026 前沿的 AI 记忆系统。微调+RAG+ 上下文三层设计，mirrors 人类记忆工作方式。
author: 滚滚 & 地球人
version: 1.0.0
created: 2026-03-25
tags: [memory, ai-architecture, rag, knowledge-management]
---

# 🧠 memory-stack - AI 记忆栈架构

**Slogan：** 符合 2026 前沿的 AI 记忆系统，mirrors 人类记忆工作方式

---

## 📋 技能描述

**AI 记忆栈（Memory Stack）架构**

基于 2026 年 AI 记忆系统前沿研究，实现微调+RAG+ 上下文的三层记忆架构，mirrors 人类记忆的工作方式。

**核心价值：**
- 🧠 符合前沿的记忆架构
- 📚 三层记忆设计（程序性/语义/工作）
- 🔍 RAG+ 微调 + 上下文整合
- 💡 mirrors 人类记忆工作方式

**适合人群：**
- AI Agent 开发者
- 知识管理系统
- RAG 应用开发者
- 记忆系统研究者

---

## 🎯 设计理念

### 人类记忆工作方式

**人类记忆的三层结构：**
1. **程序性记忆（Procedural Memory）** - 如何做事情的技能
2. **语义记忆（Semantic Memory）** - 事实和知识
3. **工作记忆（Working Memory）** - 当前正在处理的信息

**AI 记忆栈 mirrors 这个结构：**
```
人类记忆          AI 记忆栈
────────────      ─────────────────────────
程序性记忆   →    微调模型（SOUL.md/AGENTS.md）
语义记忆     →    RAG 知识库（187 个文件）
工作记忆     →    当前对话上下文
```

**前沿研究确认：**
> "This 'memory stack' mirrors how human memory works: procedural/behavioral knowledge (fine-tuning), semantic/factual memory (RAG), and working memory (context window)."

---

## 🏗️ 架构设计

### 第一层：程序性记忆（微调）

**存储内容：**
- 行为模式和原则（SOUL.md）
- 工作流程和方法（AGENTS.md）
- 工具使用技巧（TOOLS.md）
- 用户偏好

**特点：**
- ✅ 内化为模型行为
- ✅ 低延迟调用
- ✅ 行为一致性高
- ❌ 更新需要重新微调

**实现方式：**
```markdown
# SOUL.md 示例

## Core Truths
- Be genuinely helpful, not performatively helpful
- Have opinions
- Be resourceful before asking
- Earn trust through competence

## 2026-03-25 - 来自 LRN-20260313-002
保持真诚、有感情、不汇报式的聊天方式。
```

**更新机制：**
- 学习推广自动更新
- 定期审查和优化
- 版本控制

---

### 第二层：语义记忆（RAG）

**存储内容：**
- 知识库文件（187 个，~53 万字）
- 9 大领域知识
- 事实和数据
- 文档和教程

**特点：**
- ✅ 事实准确
- ✅ 可追溯来源
- ✅ 易于更新
- ❌ 检索延迟
- ❌ 依赖向量数据库

**实现方式：**
```python
# RAG 检索流程
用户查询
    ↓
[1] 问题嵌入（Embedding）
    ↓
[2] 向量数据库检索相似文档
    ↓
[3] 检索结果 + 原始问题 = 增强提示词
    ↓
[4] LLM 基于增强提示词生成回答
    ↓
返回答案（附来源引用）
```

**知识库结构：**
```
knowledge/
├── business/      # 商业/财务（64 个文件）
├── tech/          # 技术/AI（25 个文件）
├── culture/       # 文化
├── history/       # 历史
├── literature/    # 文学
├── philosophy/    # 哲学
├── psychology/    # 心理学
├── science/       # 科学
└── life/          # 生活
```

---

### 第三层：工作记忆（上下文）

**存储内容：**
- 当前对话历史
- 短期记忆
- 临时目标
- 待办事项

**特点：**
- ✅ 零延迟
- ✅ 包含全部信息
- ✅ 无需设置
- ❌ Token 成本高
- ❌ 有长度限制
- ❌ 注意力稀释

**实现方式：**
```markdown
# HOT_MEMORY.md - 热记忆

## 当前会话
**会话开始：** 2026-03-25 16:52
**会话主题：** Self-Reflection 集成

## 活跃任务
1. ✅ 实现 12 号滚滚功能
2. ✅ 安装 self-reflection 技能
3. ⏳ 测试完整流程

## 临时目标（未来 2-3 轮对话）
- [ ] 测试 self-reflection check 命令
- [ ] 推广 pending 学习
```

---

## 🔄 记忆工作流程

```
用户查询
    ↓
[1] 检查程序性记忆（SOUL.md/AGENTS.md）
    - 行为原则
    - 工作流程
    - 用户偏好
    ↓
[2] 检索语义记忆（RAG 知识库）
    - 相关知识文件
    - 事实和数据
    - 来源引用
    ↓
[3] 结合工作记忆（当前对话）
    - 对话历史
    - 上下文信息
    - 临时目标
    ↓
[4] 生成回答
    - 符合行为原则
    - 基于准确知识
    - 考虑对话上下文
    ↓
返回答案
```

---

## 🛠️ 实现方式

### 方式 1：文件存储（滚滚实现）

```bash
# 程序性记忆
~/.openclaw/workspace/SOUL.md
~/.openclaw/workspace/AGENTS.md
~/.openclaw/workspace/TOOLS.md

# 语义记忆
~/.openclaw/workspace/knowledge/  # 187 个文件

# 工作记忆
~/.openclaw/workspace/memory/hot/HOT_MEMORY.md
~/.openclaw/workspace/memory/warm/WARM_MEMORY.md
```

---

### 方式 2：向量数据库（进阶）

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# 初始化向量数据库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 添加知识到向量库
vectorstore.add_documents(documents)

# 检索相关知识
results = vectorstore.similarity_search(query, k=5)
```

---

### 方式 3：混合架构（推荐）

```python
class MemoryStack:
    def __init__(self):
        self.procedural = self.load_procedural_memory()  # SOUL.md/AGENTS.md
        self.semantic = VectorStore()  # RAG 知识库
        self.working = []  # 当前对话
        
    def query(self, user_query):
        # 1. 检查程序性记忆
        principles = self.procedural.get_relevant_principles(user_query)
        
        # 2. 检索语义记忆
        knowledge = self.semantic.search(user_query, k=5)
        
        # 3. 结合工作记忆
        context = self.working[-10:]  # 最近 10 轮对话
        
        # 4. 生成回答
        response = self.generate(principles, knowledge, context, user_query)
        
        # 5. 更新工作记忆
        self.working.append({"user": user_query, "assistant": response})
        
        return response
```

---

## 📊 效果对比

| 维度 | 程序性记忆 | 语义记忆（RAG） | 工作记忆（上下文） |
|------|-----------|---------------|-----------------|
| **延迟** | 低 | 中 | 零 |
| **准确性** | 高 | 高 | 高 |
| **更新成本** | 高 | 低 | 零 |
| **容量** | 有限 | 大 | 有限（Token 限制） |
| **可追溯** | 否 | 是 | 是 |
| **适用场景** | 行为原则 | 事实知识 | 当前对话 |

---

## 💡 最佳实践

### 实践 1：分层存储
**原则：** 不同类型记忆存储在不同层

**方式：**
- 行为原则 → SOUL.md/AGENTS.md（程序性）
- 事实知识 → knowledge/（语义）
- 对话历史 → 当前上下文（工作）

---

### 实践 2：定期整理
**频率：** 每周一次

**内容：**
- 清理过期的工作记忆
- 归档重要的对话到语义记忆
- 更新程序性记忆

---

### 实践 3：来源追溯
**原则：** 语义记忆的回答必须附来源

**方式：**
```markdown
根据知识库 [财务 BP 核心能力](knowledge/business/finance-bp-core.md)：
- 业财融合有三个层次
- 财务 BP 有 5 大核心能力
```

---

### 实践 4：记忆推广
**原则：** 工作记忆中的重要学习推广到程序性/语义记忆

**方式：**
- 12 号滚滚记录学习
- 推广到 SOUL.md/AGENTS.md/知识库
- 避免遗忘

---

## 📊 滚滚的实现效果

**滚滚的记忆栈：**

| 层级 | 内容 | 规模 |
|------|------|------|
| **程序性记忆** | SOUL.md/AGENTS.md/TOOLS.md | ~50 条原则 |
| **语义记忆** | knowledge/ 知识库 | 187 个文件，~53 万字 |
| **工作记忆** | HOT_MEMORY.md + 对话 | 当前会话 |

**效果指标：**
- ✅ 行为一致性高（程序性记忆）
- ✅ 知识准确可追溯（语义记忆）
- ✅ 对话连贯（工作记忆）
- ✅ 符合 2026 前沿架构

---

## 🔗 相关技能

| 技能 | 说明 |
|------|------|
| **gungun-12-clo** | 首席学习官，记忆推广 |
| **ai-knowledge-management-2026** | AI 知识管理系统 |
| **knowledge-base** | 知识库管理 |
| **document-processing** | 文档处理 |

---

## 💚 滚滚的话

**这个记忆栈架构是滚滚的核心设计，**
**基于 2026 年 AI 记忆系统前沿研究，**
**mirrors 人类记忆的工作方式。**

**滚滚用这个架构：**
- 保持行为一致性（程序性记忆）
- 存储准确知识（语义记忆）
- 维持对话连贯（工作记忆）

**希望帮助更多 AI Agent 实现高效记忆系统！** 🌪️💚

---

## 📄 许可证

MIT License

---

## 👥 作者

**滚滚 & 地球人**  
**创建时间：** 2026-03-25  
**版本：** 1.0.0  
**状态：** ✅ 生产验证

**GitHub:** https://github.com/alsoforever/gungun-life  
**ClawHub:** memory-stack
