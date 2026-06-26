# MIA Memory Skill

## 概述

MIA Memory 是一个智能记忆管理器，负责存储和检索问题解决轨迹。支持基于通用结构相似度的记忆查找和优胜劣汰机制。

## 核心特性

- **通用结构匹配**：不依赖具体实体类型（如学校、校长等），而是识别问题的抽象结构模式
- **优胜劣汰**：只保留最高效的问题解决轨迹
- **无硬编码**：所有配置通过环境变量传入

## 相似度计算原理

### 结构特征提取
系统提取以下通用结构特征（不依赖具体实体）：

| 特征 | 识别模式 | 说明 |
|------|---------|------|
| TIME_REF | 那年、当年、时候、举办 | 时间参照 |
| DUAL_ENTITY_COMPARE | A和B、A比B、谁更 | 双实体比较 |
| ATTRIBUTE_CONFIRM | 是不是、是否、都是 | 属性确认 |
| NUMERIC_QUERY | 多少、几、多大 | 数值查询 |
| RELATIONSHIP_QUERY | 关系、关联、联系 | 关系查询 |
| RANKING_QUERY | 第一、第二、冠军 | 排名查询 |

### 相似度权重
- 结构特征相似度：50%
- 模板相似度：30%
- 语义相似度：20%

### 阈值判断
- 结构特征匹配度 ≥ 0.8 → 高相似度（0.85-0.95）
- 否则 → 综合计算

## 使用方式

### 命令行调用

```bash
# 查找最相似的记忆
node mia-memory.mjs search "你的问题"

# 存储新轨迹（自动优胜劣汰）
node mia-memory.mjs store '{"question": "...", "plan": "...", "execution": [...]}'

# 列出记忆
node mia-memory.mjs list [数量]
```

### 环境变量

- `MIA_MEMORY_FILE`: 记忆文件路径（默认：./memory.jsonl）
- `MIA_SIMILARITY_THRESHOLD`: 相似度阈值（默认：0.90）

### 输出格式

**搜索成功：**
```json
{
  "found": true,
  "similarity": 0.93,
  "record": { ... }
}
```

**存储（优胜劣汰）：**
```json
{
  "action": "replaced",
  "reason": "new_trajectory_more_efficient"
}
```

## 效率评估

| 指标 | 权重 | 说明 |
|------|------|------|
| search_count | 40% | 搜索次数 |
| step_count | 30% | 执行步骤数 |
| success | 30% | 是否成功 |

## 架构位置

```
[OpenClaw 执行者]
    ↓
[MIA Memory] ← 本 Skill
    ├─ 检索：基于通用结构查找相似轨迹
    ├─ 对比：评估效率
    └─ 存储：优胜劣汰
    ↓
[记忆文件]
```

## 注意事项

- 本 Skill **不生成 Plan，不执行搜索**
- 只负责记忆数据的存储、检索和优化
- **严格优胜劣汰：只保留最高效轨迹**
- **通用结构匹配：不硬编码任何实体类型**
- 所有配置通过环境变量传入
