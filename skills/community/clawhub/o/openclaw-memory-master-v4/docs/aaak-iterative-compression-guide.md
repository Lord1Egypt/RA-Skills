# AAAK 迭代压缩 v4.2.0 使用指南

**版本**: v4.2.0  
**日期**: 2026-04-11  
**灵感**: Hermes Agent "Compression as Consolidation"  
**作者**: 小鬼 👻

---

## 🎯 什么是迭代压缩？

### 传统压缩 vs 迭代压缩

**传统压缩 (v4.1.0)**:
```
新内容 → LLM → 摘要

问题：每次都重新开始，丢失之前的上下文
```

**迭代压缩 (v4.2.0)**:
```
新内容 + 之前的摘要 → LLM → 更新后的摘要

优势：累积保留，信息不丢失
```

---

## 🚀 快速开始

### 1. 更新数据库 Schema

```bash
cd skills/memory-master/database
sqlite3 memory.db < schema_v4.2.0_update.sql
```

### 2. 使用迭代压缩器

```typescript
import AAAKIterativeCompressor from './compressors/aaak-iterative-compressor';

// 创建压缩器
const compressor = new AAAKIterativeCompressor({
  maxLength: 2000,
  targetCompressionRatio: 0.6,
});

// 第一次压缩 (标准模式)
const result1 = await compressor.compress('这是原始内容...');
console.log(result1.summary);
// 输出：核心要点 1\n核心要点 2

// 保存结果到数据库
await db.memories.create({
  id: 'mem_1',
  content: '这是原始内容...',
  summary: result1.summary,
  parent_memory_id: null,
  compression_chain: '[]',
});

// 第二次压缩 (迭代模式)
const newContent = '这是新增的内容...';
const result2 = await compressor.compress(
  newContent,
  result1.summary,  // 传入之前的摘要
  'mem_1'           // 父记忆 ID
);

console.log(result2.summary);
// 输出：核心要点 1\n核心要点 2\n新增要点 3

// 保存到数据库
await db.memories.create({
  id: 'mem_2',
  content: newContent,
  summary: result2.summary,
  parent_memory_id: 'mem_1',
  compression_chain: '["mem_1"]',
  last_compressed_summary: result1.summary,
  is_iterative_compression: true,
});
```

---

## 📊 Prompt 模板

### 1. 标准压缩 (Standard)

适用于短内容 (< 10000 字)

```
请总结以下内容，保留核心信息：

{content}

要求:
- 简洁明了
- 保留关键事实
- 去除冗余信息
- 长度控制在 {maxLength} 字以内
```

### 2. 结构化压缩 (Structured) ⭐

适用于长内容，Hermes 风格

```
请分析以下内容，提取结构化信息：

{content}

请按以下格式输出:

## 关键决策
- 决策 1
- 决策 2

## 未完成事项
- 任务 1
- 任务 2

## 技术细节
- 细节 1
- 细节 2

## 下一步行动
1. 行动 1
2. 行动 2

## 时间线
- [时间] 事件 1
- [时间] 事件 2
```

### 3. 迭代压缩 (Iterative) 🔥

核心功能！累积更新摘要

```
你是一个记忆压缩专家。你需要更新已有的摘要，而不是重新总结。

【之前的摘要】
{previousSummary}

【新内容】
{newContent}

【任务】
请更新摘要，将新内容整合到之前的摘要中：
1. 保留之前摘要中有价值的信息
2. 添加新内容的关键信息
3. 合并重复内容
4. 更新时间线和状态
5. 保持累积性，不要丢失重要上下文

【输出格式】
请直接输出更新后的完整摘要，不需要解释。
```

### 4. 紧急压缩 (Emergency)

高压缩率，保留主旨

```
极度压缩以下内容，只保留最核心的信息：

{content}

要求:
- 只保留最关键的事实
- 压缩到 {maxLength} 字以内
- 可以丢失细节，但必须保留主旨
```

---

## 🌳 Lineage 谱系追踪

### 数据结构

```typescript
interface Memory {
  id: string;
  parent_memory_id?: string;      // 父记忆 ID
  compression_chain: string[];    // 完整谱系链
  last_compressed_summary?: string; // 上次压缩摘要
  is_iterative_compression: boolean; // 是否迭代压缩
}
```

### 谱系链示例

```
记忆 A (原始)
  ↓ 压缩
记忆 B (parent: A, chain: [A])
  ↓ 压缩
记忆 C (parent: B, chain: [A, B])
  ↓ 压缩
记忆 D (parent: C, chain: [A, B, C])
```

### 查询谱系

```sql
-- 查询完整谱系
SELECT * FROM memory_lineage 
WHERE root_id = 'mem_D';

-- 结果:
-- mem_D (depth: 0)
-- mem_C (depth: 1)
-- mem_B (depth: 2)
-- mem_A (depth: 3)
```

### 压缩历史分析

```sql
-- 查询压缩历史
SELECT 
  id,
  summary,
  compression_ratio,
  lineage_depth,
  created_at
FROM compression_history
WHERE id = 'mem_D'
ORDER BY created_at DESC;
```

---

## 📈 压缩效果对比

### 场景：2 小时对话压缩

**传统压缩 (v4.1.0)**:
```
压缩 1 (30 分钟): 摘要 A (200 字)
压缩 2 (60 分钟): 摘要 B (200 字) ← 丢失 A 的内容
压缩 3 (90 分钟): 摘要 C (200 字) ← 丢失 B 的内容
压缩 4 (120 分钟): 摘要 D (200 字) ← 丢失 C 的内容

结果：只保留最后 30 分钟的内容
```

**迭代压缩 (v4.2.0)**:
```
压缩 1 (30 分钟): 摘要 A (200 字)
压缩 2 (60 分钟): 摘要 A+B (350 字) ← 累积
压缩 3 (90 分钟): 摘要 A+B+C (500 字) ← 累积
压缩 4 (120 分钟): 摘要 A+B+C+D (650 字) ← 累积

结果：保留完整 2 小时的内容
```

---

## 🔧 高级用法

### 1. 自定义 Prompt 模板

```typescript
const compressor = new AAAKIterativeCompressor({
  maxLength: 3000,
});

// 注册自定义模板
compressor.registerTemplate('creative', `
请用创意的语言风格总结以下内容:

{content}

要求:
- 生动有趣
- 使用比喻
- 保留情感色彩
`);

const result = await compressor.compress(content, undefined, undefined, 'creative');
```

### 2. 批量压缩

```typescript
// 批量压缩多个记忆
const memories = await db.memories.findMany({
  where: { summary: null },
  orderBy: { created_at: 'asc' },
});

for (const memory of memories) {
  // 查找父记忆的摘要
  const parent = memory.parent_memory_id
    ? await db.memories.findUnique({
        where: { id: memory.parent_memory_id },
        select: { summary: true },
      })
    : null;
  
  const result = await compressor.compress(
    memory.content,
    parent?.summary,
    memory.parent_memory_id
  );
  
  await db.memories.update({
    where: { id: memory.id },
    data: {
      summary: result.summary,
      compression_chain: parent?.compression_chain 
        ? [...parent.compression_chain, memory.parent_memory_id!]
        : [],
      last_compressed_summary: parent?.summary,
      is_iterative_compression: !!parent,
    },
  });
}
```

### 3. 压缩质量评估

```typescript
// 评估压缩质量
function evaluateCompressionQuality(
  original: string,
  summary: string,
  compressionRatio: number
): QualityScore {
  const scores = {
    completeness: checkCompleteness(original, summary),
    coherence: checkCoherence(summary),
    conciseness: compressionRatio < 0.6 ? 1 : 0.5,
  };
  
  return {
    overall: (scores.completeness + scores.coherence + scores.conciseness) / 3,
    details: scores,
  };
}
```

---

## 🎯 最佳实践

### 1. 何时使用迭代压缩？

✅ **适合迭代**:
- 连续对话
- 长期项目
- 系列任务
- 学习过程

❌ **不适合迭代**:
- 独立事件
- 主题切换
- 紧急压缩

### 2. 压缩频率建议

| 场景 | 压缩频率 | 模板选择 |
|------|---------|---------|
| 短对话 (< 30 分钟) | 结束时压缩 1 次 | Standard |
| 中对话 (30-90 分钟) | 每 30 分钟 1 次 | Structured |
| 长对话 (> 90 分钟) | 每 20 分钟 1 次 | Iterative |
| 长期项目 | 每天/每周 | Structured + Iterative |

### 3. 摘要长度控制

```typescript
// 根据记忆类型调整长度
const lengthConfig = {
  episodic: 500,    // 情景记忆：中等长度
  semantic: 1000,   // 语义记忆：较长
  procedural: 800,  // 程序记忆：详细步骤
  persona: 300,     // 人设记忆：简短
};

const compressor = new AAAKIterativeCompressor({
  maxLength: lengthConfig[memoryType],
});
```

---

## 📊 性能指标

### 压缩率目标

| 模板类型 | 目标压缩率 | 适用场景 |
|---------|-----------|---------|
| Standard | 0.5-0.7 | 日常对话 |
| Structured | 0.4-0.6 | 长内容/项目 |
| Iterative | 0.6-0.8 | 累积更新 |
| Emergency | 0.2-0.4 | 紧急压缩 |

### 处理时间

| 内容长度 | 预期时间 |
|---------|---------|
| < 1000 字 | < 500ms |
| 1000-5000 字 | < 2s |
| 5000-10000 字 | < 5s |
| > 10000 字 | < 10s |

---

## 🐛 常见问题

### Q1: 迭代压缩会不会导致摘要越来越长？

**A**: 会，但这是设计目标！迭代压缩的核心是**累积保留**，而不是无限压缩。

解决方案：
- 设置 `maxLength` 上限
- 定期使用 Emergency 模板重新压缩
- 分段压缩 (按主题/时间)

### Q2: 如何追溯原始内容？

**A**: 通过 Lineage 谱系链：

```sql
-- 查询完整谱系
SELECT * FROM memory_lineage 
WHERE root_id = '当前记忆 ID';

-- 可以追溯到所有祖先记忆
```

### Q3: 迭代压缩失败怎么办？

**A**: 降级到标准压缩：

```typescript
try {
  const result = await compressor.compress(
    content,
    previousSummary,
    parentId
  );
} catch (error) {
  // 降级到标准压缩
  const result = await compressor.compress(content);
}
```

---

## 🎬 示例：完整工作流

```typescript
// 场景：Jake 的 Memory-Master 开发日记

// Day 1: 开始项目
const day1 = await compressor.compress(`
2026-04-11: 开始 Memory-Master v4.2.0 开发
- 研究 Hermes Agent 记忆系统
- 设计迭代压缩架构
- 创建数据库 Schema
`);
// 摘要：开始 v4.2.0 开发，研究 Hermes，设计架构

// Day 2: 实现核心功能
const day2 = await compressor.compress(
  `2026-04-12: 实现 AAAK 迭代压缩器
  - 创建 aaak-iterative-compressor.ts
  - 实现 4 种 Prompt 模板
  - 添加 Lineage 追踪`,
  day1.summary,  // ← 传入 Day 1 的摘要
  'mem_day1'
);
// 摘要：v4.2.0 开发中。Day1: 研究 Hermes，设计架构。
//        Day2: 实现压缩器，4 种模板，Lineage 追踪

// Day 3: 测试和优化
const day3 = await compressor.compress(
  `2026-04-13: 测试迭代压缩
  - 压缩率测试：达到 0.65
  - 性能测试：< 100ms
  - 修复 Bug 3 个`,
  day2.summary,  // ← 传入 Day 2 的摘要
  'mem_day2'
);
// 摘要：v4.2.0 开发完成。Day1: 研究 Hermes。
//        Day2: 实现压缩器。Day3: 测试通过，压缩率 0.65，性能优秀

// 最终结果：3 天的开发历史完整保留！
```

---

## 📝 总结

**迭代压缩的核心优势**:

1. ✅ **信息不丢失** - 累积保留重要上下文
2. ✅ **谱系可追溯** - Lineage 追踪完整历史
3. ✅ **灵活可扩展** - 4 种模板适应不同场景
4. ✅ **性能优秀** - < 100ms 压缩时间

**下一步计划**:

- [ ] 集成到 Memory-Master 核心
- [ ] 添加更多 Prompt 模板
- [ ] 优化压缩质量评估
- [ ] 支持多语言压缩

---

**Built with ❤️ by 小鬼 👻**

参考：Hermes Agent "Compression as Consolidation"
