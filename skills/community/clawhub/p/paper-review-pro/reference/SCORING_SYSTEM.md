# 综合评分系统

## 功能描述

同时考虑相关度和权威度的综合评分机制，用于 Top-K 论文筛选和排序。

## 评分公式

```
综合分数 = 相关度 × (1 - weight) + 权威度 × weight
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| **相关度** | 基于查询关键词与论文标题/摘要的匹配度 | - |
| **权威度** | 基于发表状态和 CCF 评级 | - |
| **weight** | 权威度权重（0.0-1.0） | 0.3 |

### 权威度评分标准

| CCF 评级 | 权威度分数 |
|---------|-----------|
| CCF-A | 1.0 |
| CCF-B | 0.8 |
| CCF-C | 0.6 |
| 已发表未评级 | 0.5 |
| preprint（预印本） | 0.3 |

## 模块信息

- **核心模块**: `scripts/core/similarity.py`
- **新增方法**: `compute_with_authority()`

## 使用方式

### 标准检索（启用综合评分）
```bash
python scripts/review.py --query "LLM reasoning" --retrieve_number 20 --keep_topk 5 --year 2024
```

### 仅使用相关度评分（禁用权威度）
```bash
python scripts/review.py --query "LLM reasoning" --keep_topk 5 --no-authority
```

### 调整权威度权重
```bash
python scripts/review.py --query "LLM reasoning" --keep_topk 5 --authority-weight 0.5
```

## 权重建议

| 场景 | 建议权重 | 说明 |
|------|---------|------|
| 探索性研究 | 0.2-0.3 | 相关度优先，广泛探索 |
| 系统性综述 | 0.4-0.5 | 权威度优先，确保质量 |
| 纯内容分析 | 禁用权威度 | 仅关注内容相关性 |

## 配置项

### 新增配置
- `authority_weight`: 权威度分数权重（默认 0.3）

### 快速配置
```bash
python scripts/config.py --default_n 20 --default_k 5 --authority-weight 0.4
```

## 索引文件增强

索引文件（`index.json`）包含以下评分相关字段：

| 字段 | 说明 |
|------|------|
| `similarity_base` | 原始相关度分数 |
| `authority_score` | 权威度分数 |
| `similarity` | 综合分数（相关度 + 权威度） |

## 注意事项

1. **权威度权重**建议设置在 0.2-0.4 之间。权重过高可能导致高评级但不太相关的论文排在前面。

2. **禁用权威度**时，系统仅使用相关度进行排序，适合特定场景（如新兴领域、预印本分析）。
