# 🧠 Memory-Master v4.2.0

**AI Agent Memory System with Iterative Compression & Lineage Tracking**

**发布**: 2026-04-20 (计划中)  
**许可**: MIT  
**状态**: ✅ 测试通过

---

## ✨ v4.2.0 核心特性

### 🆕 新增功能

| 功能 | 描述 | 优势 |
|------|------|------|
| **🔥 迭代压缩** | 新内容 + 旧摘要 → 更新摘要 | 信息不丢失，累积保留 |
| **🌳 Lineage 追踪** | 完整的记忆谱系链 | 可追溯所有历史 |
| **⚡ 性能优化** | LRU 缓存 + 并行处理 | 平均 45ms，提升 5.6 倍 |
| **📊 结构化摘要** | 决策/任务/时间线提取 | Hermes Agent 启发 |
| **💾 增量检测** | 只压缩变化的内容 | 节省 70% 计算资源 |

### 📊 性能指标

| 指标 | v4.1.0 | v4.2.0 | 提升 |
|------|--------|--------|------|
| **平均压缩时间** | 250ms | **45ms** | **5.6x** ⚡ |
| **P95 时间** | 400ms | **52ms** | **7.7x** ⚡ |
| **缓存命中率** | 0% | **72%** | **+72%** 🎯 |
| **批量处理** | 2500ms | **520ms** | **4.8x** ⚡ |

---

## 🎯 核心功能

### 1. 4 类记忆模型

- **📅 情景记忆 (Episodic)**: 事件、经历、对话
- **📚 语义记忆 (Semantic)**: 知识、事实、概念
- **🔧 程序记忆 (Procedural)**: 技能、习惯、流程
- **👤 人设记忆 (Persona)**: 身份、偏好、价值观

### 2. 时间树结构

- 📅 按时间组织记忆
- 🔍 快速定位特定时间段
- 📊 支持时间范围查询

### 3. 5 种检索类型

- **语义检索**: 基于内容相似度
- **时间检索**: 基于时间范围
- **类型检索**: 基于记忆类型
- **标签检索**: 基于标签过滤
- **混合检索**: 多条件组合

### 4. 迭代压缩 (v4.2.0 新)

```
传统压缩：新内容 → 摘要 (丢失旧上下文)
迭代压缩：新内容 + 旧摘要 → 更新摘要 (累积保留)
```

**示例**:
```javascript
// 第一次压缩
const result1 = await compressor.compress('Day1: 完成架构设计');
// 摘要：开始 v4.2.0 开发，设计架构

// 第二次压缩 (迭代)
const result2 = await compressor.compress(
  'Day2: 实现核心功能',
  result1.summary,  // ← 传入之前的摘要
  'mem_day1'
);
// 摘要：v4.2.0 开发中。Day1: 设计架构。Day2: 实现核心功能
```

### 5. Lineage 谱系追踪 (v4.2.0 新)

```typescript
interface Memory {
  id: string;
  parent_memory_id?: string;      // 父记忆
  compression_chain: string[];    // 完整谱系链
  last_compressed_summary?: string; // 上次摘要
  is_iterative_compression: boolean;
}
```

**查询谱系**:
```sql
SELECT * FROM memory_lineage WHERE root_id = 'mem_current';
-- 返回完整的记忆历史链
```

---

## 🚀 快速开始

### 安装

```bash
# 从 ClawHub 安装
clawhub install openclaw-memory-master@4.2.0

# 或从 GitHub 克隆
git clone https://github.com/cp3d1455926-svg/memory-master.git
cd memory-master
npm install
```

### 基础使用

```javascript
const { MemoryManager } = require('./src/memory-manager');

// 创建管理器
const manager = new MemoryManager({
  baseDir: './memory',
  autoIndex: true,
  compression: true,
  compressionMaxLength: 2000,
  compressionRatio: 0.6,
});

// 存储记忆
const result = manager.store('今天完成了 Memory-Master v4.2.0 开发', {
  tags: ['开发', '里程碑'],
  timestamp: Date.now(),
});

// 压缩记忆 (v4.2.0)
const compressed = await manager.compressMemory(result.memoryId);
console.log('摘要:', compressed.summary);
console.log('压缩率:', compressed.compressionRatio);
```

### 迭代压缩示例

```javascript
// Day 1: 开始项目
const day1 = await manager.compressMemory(mem1);
// 摘要：开始 v4.2.0 开发

// Day 2: 继续开发
const day2 = await manager.compressMemory(mem2, {
  parentMemoryId: mem1.id,  // ← 迭代压缩
});
// 摘要：v4.2.0 开发中。Day1: 开始开发。Day2: 实现功能
```

---

## 📊 数据库 Schema

### v4.2.0 更新

```sql
-- 添加迭代压缩字段
ALTER TABLE memories ADD COLUMN parent_memory_id TEXT;
ALTER TABLE memories ADD COLUMN compression_chain TEXT;
ALTER TABLE memories ADD COLUMN last_compressed_summary TEXT;
ALTER TABLE memories ADD COLUMN is_iterative_compression INTEGER DEFAULT 0;
ALTER TABLE memories ADD COLUMN compression_template TEXT DEFAULT 'standard';

-- 创建索引
CREATE INDEX idx_memories_parent ON memories(parent_memory_id);
CREATE INDEX idx_memories_compression_chain ON memories(compression_chain);

-- 创建谱系视图
CREATE VIEW memory_lineage AS
WITH RECURSIVE lineage AS (...)
SELECT * FROM lineage;
```

**升级方法**:
```bash
sqlite3 memory.db < database/schema_v4.2.0_update.sql
```

---

## 📁 项目结构

```
memory-master/
├── src/
│   ├── compressors/
│   │   ├── aaak-iterative-compressor.ts  # 迭代压缩器
│   │   └── performance-optimizer.ts      # 性能优化
│   ├── layers/
│   │   └── ...                           # 4 类记忆层
│   ├── memory-classifier.js              # 记忆分类器
│   ├── memory-manager.js                 # 统一管理器
│   ├── query-classifier.js               # 查询分类器
│   └── time-tree.js                      # 时间树
├── database/
│   └── schema_v4.2.0_update.sql          # Schema 更新
├── docs/
│   ├── aaak-iterative-compression-guide.md  # 压缩指南
│   ├── performance-optimization-report.md   # 性能报告
│   └── ...
├── test-full-suite.js                    # 完整测试套件
├── TEST_RESULTS.md                       # 测试结果
├── INTEGRATION_COMPLETE.md               # 集成报告
└── README.md
```

---

## 🧪 测试

### 运行测试

```bash
# 完整测试套件
node test-full-suite.js

# 迭代压缩测试
node test-iterative-compression.js
```

### 测试结果

```
🧪 Memory-Master v4.2.0 测试套件

=============================================================
📊 测试结果:
   总计：12
   ✅ 通过：12
   ❌ 失败：0
=============================================================
✅ 所有测试通过！
```

**性能指标**:
- 平均压缩时间：**45.2ms** (目标 100ms) ✅
- P95 时间：**52ms** (目标 100ms) ✅
- 缓存命中率：**72%** (目标 50%) ✅

---

## 📖 文档

| 文档 | 描述 |
|------|------|
| [迭代压缩指南](docs/aaak-iterative-compression-guide.md) | 详细使用教程 |
| [性能优化报告](docs/performance-optimization-report.md) | 性能分析和最佳实践 |
| [测试报告](TEST_REPORT.md) | 测试用例和结果 |
| [集成报告](INTEGRATION_COMPLETE.md) | 集成细节 |

---

## 🎯 使用场景

### 1. 长期项目跟踪

```javascript
// 每天记录进展，迭代压缩保留完整历史
await manager.compressMemory(todayWork, {
  parentMemoryId: yesterdayMemory.id,
});
```

### 2. 对话历史管理

```javascript
// 多轮对话，累积摘要
const summary = await manager.compressMemory(newMessage, {
  parentMemoryId: previousTurn.id,
});
```

### 3. 学习笔记系统

```javascript
// 学习新知识，结构化摘要
const result = await manager.compressMemory(notes, {
  template: 'structured',  // 提取决策/任务/时间线
});
```

---

## 🔧 配置选项

```typescript
interface MemoryManagerConfig {
  baseDir: string;                    // 基础目录
  autoIndex: boolean;                 // 自动索引
  compression: boolean;               // 启用压缩
  compressionMaxLength: number;       // 最大长度 (默认 2000)
  compressionRatio: number;           // 目标压缩率 (默认 0.6)
  cacheSize: number;                  // 缓存大小 (默认 1000)
  maxConcurrency: number;             // 最大并发 (默认 5)
}
```

---

## 📈 版本历史

| 版本 | 日期 | 主要功能 |
|------|------|---------|
| **v4.2.0** | **2026-04-11** | **迭代压缩、Lineage 追踪、性能优化** |
| v4.1.0 | 2026-04-10 | 重要性评分、情感维度 |
| v4.0.0 | 2026-04-10 | AAAK 压缩算法 |
| v3.0.0 | 2026-04-09 | 4 类记忆模型、时间树 |
| v2.6.1 | 2026-04-08 | AGENTS.md 规则分离 |

---

## 🚀 发布计划

### v4.2.0 发布

- **发布日期**: 2026-04-20
- **发布平台**:
  - ClawHub
  - GitHub
  - Gitee
- **宣传渠道**:
  - 公众号文章
  - 技术社区
  - 视频教程

---

## 🤝 贡献

欢迎贡献！请查看：

1. [贡献指南](CONTRIBUTING.md)
2. [开发文档](docs/development.md)
3. [代码规范](docs/code-style.md)

---

## 📝 许可

MIT License © 2026 Jake & 小鬼 👻

---

## 🔗 链接

- **GitHub**: https://github.com/cp3d1455926-svg/memory-master
- **Gitee**: https://gitee.com/cp3d1455926-svg/memory-master
- **ClawHub**: https://clawhub.ai/openclaw-memory-master
- **文档**: https://memory-master.pages.dev

---

**Built with ❤️ by Jake & 小鬼 👻**

**v4.2.0 - 让 AI 真正"记住"并"成长"！** 🚀
