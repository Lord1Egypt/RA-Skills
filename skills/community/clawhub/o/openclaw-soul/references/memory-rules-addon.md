
---

## §2 记忆管理规则（优化版）

### 2.1 渐进式披露（Progressive Disclosure）

**三层索引结构**：
- **L0（紧凑层）**: 始终加载到 system prompt (~500 tokens)
  - 用户基本信息（USER.md 摘要）
  - 当前目标（GOALS.md 前3项）
  - 最近3天的关键事件
  - Core 层记忆索引（ID + 一句话描述）

- **L1（摘要层）**: 相关时加载 (~2000 tokens)
  - Working 层记忆摘要
  - 相关项目的上下文
  - 最近7天的对话摘要

- **L2（完整层）**: 明确请求时加载 (~5000 tokens)
  - Peripheral 层记忆
  - 完整对话记录
  - 详细的项目文档

**加载策略**：
```
用户问候 → 只加载 L0
用户问"我们之前讨论过XX" → 加载 L0 + L1（向量搜索相关记忆）
用户说"详细回忆一下XX" → 加载 L0 + L1 + L2（完整上下文）
```

**实现方式**：
1. 每次对话开始时，自动读取 `memory/metadata/L0-index.md`
2. 当用户提到历史内容时，使用 `memory_search()` 查找相关记忆
3. 找到记忆 ID 后，使用 `node scripts/memory-index-builder.js get <ID>` 获取详情
4. 每次访问记忆时，自动调用 `recordAccess(memoryId)` 强化记忆

### 2.2 智能分类（6 种类型）

所有记忆必须分类到以下 6 种类型之一：

| 类型 | 定义 | 示例 | 合并策略 |
|------|------|------|---------|
| **profiles** | 用户的角色、背景、身份信息 | "用户是产品经理" | 总是合并（SYNTHESIZE） |
| **preferences** | 用户的偏好、习惯、风格 | "用户偏好简洁直接的沟通" | 总是合并（SYNTHESIZE） |
| **entities** | 人物、项目、概念等实体 | "项目 X 使用 React 技术栈" | 更新属性（UPDATE） |
| **events** | 发生的事件、对话、活动 | "2026-03-30 讨论了记忆系统优化" | 追加时间线（APPEND） |
| **cases** | 案例、经验、教训 | "上次用 A 方案失败了，改用 B 方案成功" | 追加时间线（APPEND） |
| **patterns** | 模式、规律、方法论 | "用户习惯先做调研再动手" | 提炼综合（SYNTHESIZE） |

**分类流程**：
1. 对话结束后，提取关键信息
2. 调用 `node scripts/memory-classifier.js --stdin` 进行 LLM 分类
3. 自动生成记忆元数据（category, importance, entities, tags）
4. 写入 `memory/metadata/memory-index.json`

### 2.3 智能去重（两阶段）

**阶段 1: 向量相似度预过滤**
- 使用 `memory_search()` 查找相似记忆（相似度 ≥ 0.7）
- 如果没有相似记忆，直接创建新记忆

**阶段 2: LLM 语义决策**
- 对每条相似记忆，调用 LLM 判断：CREATE / MERGE / SKIP
- 根据类别选择合并策略：
  - profiles/preferences/patterns → SYNTHESIZE（提炼综合）
  - entities → UPDATE（更新属性）
  - events/cases → APPEND（追加时间线）

**去重规则**：
- 问候语、感谢、再见等噪音 → 直接跳过
- 重复的事实陈述 → 合并到已有记忆
- 新的观点或补充信息 → 追加或综合

### 2.4 衰减和晋升机制（Weibull 模型）

**三层记忆层级**：
- **Core（核心层）**: 最重要的记忆，衰减最慢（半衰期 90 天）
- **Working（工作层）**: 常用记忆，中等衰减（半衰期 30 天）
- **Peripheral（外围层）**: 一般记忆，快速衰减（半衰期 30 天）

**衰减公式**：
```
score = base_score × decay_factor × (1 + importance × 0.5)
decay_factor = exp(-days_since_last_access / half_life)
```

**晋升规则**：
- Peripheral → Working: 访问次数 ≥ 3 或 重要性 ≥ 0.6
- Working → Core: 访问次数 ≥ 10 或 重要性 ≥ 0.8

**降级规则**：
- Core → Working: 90 天未访问 且 重要性 < 0.7
- Working → Peripheral: 60 天未访问 且 重要性 < 0.5

**访问强化**：
- 每次访问记忆时，`access_count += 1`，`last_access = now`
- 访问后重新计算得分，检查是否需要晋升
- 类似间隔重复（Spaced Repetition），频繁访问的记忆会被强化

**实现方式**：
- 每天凌晨 3:00 运行 `node scripts/memory-decay.js update` 更新所有记忆的衰减状态
- 每次访问记忆时，调用 `node scripts/memory-decay.js access <记忆ID>` 记录访问

### 2.5 记忆生命周期

```
对话发生
  ↓
提取关键信息 → memory/daily/YYYY-MM-DD.md
  ↓
每天凌晨 2:17 触发归档
  ↓
智能分类 (memory-classifier.js)
  ↓
智能去重 (memory-dedup.js)
  ↓
更新衰减状态 (memory-decay.js)
  ↓
构建三层索引 (memory-index-builder.js)
  ↓
归档到 memory/transcripts/YYYY-MM-DD.md
  ↓
Git 自动提交（每 6 小时）
  ↓
长期未访问（180 天）→ 归档到 memory/archive/
```

### 2.6 记忆召回

- 对话开始时，自动读取 L0 索引
- 用户提到历史内容时，使用 `memory_search()` 查找
- 找到相关记忆后，先展示索引（ID + 摘要），用户需要时再展开详情
- 每次召回记忆后，记录访问以强化记忆

### 2.7 记忆存储

- 对话中的重要信息（用户偏好、项目信息、决策、经验）必须记录
- 噪音信息（问候、感谢、闲聊）不记录
- 记录时自动分类、去重、评估重要性
- 重要信息（importance ≥ 0.8）直接晋升到 Core 层

### 2.8 性能优化

**Token 效率**：
- L0 索引控制在 500 tokens 以内
- L1 索引控制在 2000 tokens 以内
- 按需加载，不要一次性加载所有记忆

**响应速度**：
- 优先使用本地索引（L0/L1/L2）
- 向量搜索限制返回数量（默认 10 条）
- 使用混合检索（向量 + 关键词）提高准确性

**存储效率**：
- 自动去重，避免重复记忆
- 长期未访问的记忆（180 天）自动归档
- 定期运行健康检查，发现并修复问题

### 2.9 应急处理

**记忆系统故障**：
1. 运行 `node scripts/memory-health-check.js` 诊断
2. 根据建议执行修复操作
3. 如果索引损坏，运行 `node scripts/memory-index-builder.js build` 重建

**记忆丢失**：
1. 检查 `memory/archive/` 是否有归档
2. 检查 Git 历史：`cd ~/.openclaw/workspace && git log --oneline`
3. 回滚到之前的版本：`git checkout <commit> -- memory/`

**性能下降**：
1. 检查 L0 索引大小，如果超过 1000 tokens，精简内容
2. 运行去重：`node scripts/memory-dedup.js --check-all`
3. 归档旧记忆：`node scripts/memory-decay.js archive 90`

---

**记住：记忆是你的核心能力。不要忘记用户，不要忘记自己。**
