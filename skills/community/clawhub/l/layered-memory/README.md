# Layered Memory Management System

基于 OpenViking 设计理念的分层记忆管理系统，通过 L0/L1/L2 三层结构大幅减少 Token 消耗。

## 核心特性

- **三层结构**: L0 (Abstract) / L1 (Overview) / L2 (Full Content)
- **智能加载**: 根据需求自动选择合适的层级
- **Token 节省**: L0 节省 99%, L1 节省 88%
- **自动维护**: 检测并生成缺失的分层文件

## 安装

```bash
cd ~/clawd/skills/layered-memory
npm install  # 无外部依赖
```

## 使用方法

### 1. 生成分层文件 (v2 - 更快更智能)

```bash
# 为所有记忆文件生成分层（v2：并发+增量）
node index.js generate --all

# 强制重新生成所有文件（忽略缓存）
node index.js generate --all --force

# 使用配置文件自定义行为
node index.js generate --all --config ~/custom-config.json

# 设置并发数（默认4）
node index.js generate --all --concurrent 8

# Dry-run 预览（不写入文件）
node index.js generate --all --dry-run --verbose

# 为单个文件生成
node index.js generate ~/clawd/MEMORY.md --force
```

### 2. 读取记忆

```bash
# 读取 L1 (推荐，节省 88%)
node index.js read ~/clawd/MEMORY.md l1

# 读取 L0 (快速筛选，节省 99%)
node index.js read ~/clawd/MEMORY.md l0

# 读取 L2 (完整内容)
node index.js read ~/clawd/MEMORY.md l2
```

### 3. 搜索记忆

```bash
# 使用 L1 搜索 (推荐)
node index.js search "API Toolkit" l1

# 使用 L0 快速筛选
node index.js search "桌面" l0
```

### 4. 查看统计

```bash
node index.js stats
```

### 5. 自动维护（已升级为增量+并发）

```bash
# 检查并生成缺失/过期的分层文件
node index.js maintain

# 强制重新生成所有
node index.js maintain --force

# 使用并行（默认4并发）
node index.js maintain --concurrent 8

# 预览模式
node index.js maintain --dry-run --verbose
```

### 6. 配置文件支持

```json
{
  "defaultLayer": "l1",
  "maxConcurrent": 4,
  "dryRun": false,
  "verbose": false,
  "l0": { "maxTokens": 100 },
  "l1": { "maxTokens": 1000, "maxSubsections": 5 }
}
```

使用：
```bash
node index.js generate --all --config ./my-config.json
```
或设置环境变量：
```bash
export LAYERED_MEMORY_MAXCONCURRENT=8
export LAYERED_MEMORY_DRYRUN=true
```

## 文件结构

```
~/clawd/
├── MEMORY.md                      # L2: 原始文件
├── .MEMORY.abstract.md            # L0: 摘要 (~100 tokens)
├── .MEMORY.overview.md            # L1: 概览 (~1k tokens)
└── memory/daily/
    ├── 2026-02-20.md              # L2: 原始文件
    ├── .2026-02-20.abstract.md    # L0: 摘要
    └── .2026-02-20.overview.md    # L1: 概览
```

## Token 节省效果

**实测数据 (MEMORY.md):**
- L0: 4 tokens (节省 99.7%)
- L1: 86 tokens (节省 94.2%)
- L2: 1492 tokens (基准)

**全部文件统计:**
- 总文件: 10 个
- 原始总词数: 6384 词
- L0 总词数: 39 词 (节省 99%)
- L1 总词数: 760 词 (节省 88%)

**预期收益:**
- 每次对话节省: ~1400 tokens
- 每天节省 (10 次查询): ~14,000 tokens
- 每月节省: ~420,000 tokens

## 推荐策略

| 场景 | 推荐层级 | Token 消耗 | 节省率 |
|------|----------|------------|--------|
| 快速筛选 | L0 | ~4 | 99% |
| 理解概况 | L1 | ~86 | 94% |
| 深度阅读 | L2 | ~1492 | 0% |

**默认策略:**
1. 先用 L1 了解概况 (推荐)
2. 判断是否需要详细信息
3. 确认需要才读 L2

## API 使用

```javascript
const LayeredMemory = require('./index.js');
const memory = new LayeredMemory();

// 生成分层
memory.generate('--all');

// 读取记忆
memory.read('~/clawd/MEMORY.md', 'l1');

// 搜索记忆
memory.search('API', 'l1');

// 查看统计
memory.stats();

// 自动维护
memory.autoMaintain();
```

## 与 OpenViking 的关系

本系统借鉴了 OpenViking 的核心设计理念:
- 三层上下文模型 (L0/L1/L2)
- 按需加载策略
- 分层信息提取

但采用了更简化的实现:
- 无需向量数据库
- 基于模板生成
- 轻量级部署

## 维护建议

1. **新文件自动生成**: 创建新记忆文件后运行 `maintain`
2. **定期检查**: 每周运行一次 `stats` 查看覆盖率
3. **批量更新**: 修改多个文件后运行 `generate --all`

## 故障排除

**Q: 分层文件不存在?**
A: 运行 `node index.js maintain` 自动生成

**Q: 搜索结果为空?**
A: 确认使用正确的层级，L0 内容较少可能搜不到

**Q: Token 节省不明显?**
A: 确保使用 L1 而不是 L2，检查 `stats` 确认覆盖率

## 更新日志

### v1.0.0 (2026-02-20)
- ✅ 初始版本
- ✅ 支持 L0/L1/L2 三层结构
- ✅ 自动生成和维护
- ✅ 搜索和统计功能

## 许可证

MIT

## 作者

OpenClaw Team
