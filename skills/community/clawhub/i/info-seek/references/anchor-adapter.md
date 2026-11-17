# Infoseek Anchor Adapter 适配层说明

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐全：`scripts/anchor_adapter.py`

## 1. 职责

锚点（信息源候选）→ 意图卡片的转换层。核心能力：

| 函数 | 职责 |
|------|------|
| `compute_anchor_score` / `compute_anchor_score_v15` | 四维/五维评分 |
| `calculate_score` | 统一评分入口（v1.5.0/v1.6.0/v1.7.0/v1.8.1 演进） |
| `compute_semantic_similarity` | 语义相似度（jaccard / summa / string 多算法） |
| `_jaccard_similarity` | 关键词集合 Jaccard（三跑择优 + 自适应加权） |
| `_string_containment_similarity` | 主题词包含比例（中文友好） |
| `_extract_keywords_three_run` | 三跑关键词提取（summa + jieba + regex + 零依赖兜底） |
| `compute_cross_platform_score` | 跨平台分布度（第 6 维） |
| `cross_subject_analysis` | 跨主题相关性分析 |
| `apply_resurrection_batch` | 白名单复活批量 |

## 2. 意图卡片结构

锚点经 `infos_to_seek()` 转换为标准意图卡片：

```json
{
  "title": "标题",
  "url": "https://...",
  "platform": "平台名（可选）",
  "score": 0-100,
  "snippet": "摘要（可选）",
  "interaction": 0-100,   // 互动深度维度
  "topic_match": 0-100,   // 主题一致性维度
  "credibility": 0-100    // 来源可信度维度
}
```

## 3. 语义相似度算法对比

| 算法 | 场景 | 中文表现 |
|------|------|----------|
| `jaccard`（默认） | 通用 | 关键词命中敏感，短主题偏严 |
| `summa` | 英文长文 | 中文关键词为空时自动降级 jaccard |
| `string`（containment） | 中文兜底 | 主题词包含比例，宽松 |
| `tfidf` | 已废弃 | v1.7.4 起重定向 jaccard |

## 4. v1.0.1 集成点

- `infoseek_core_v2.score_source()` 缺三字段时调用 `compute_semantic_similarity` + `_string_containment_similarity` 兜底
- `infoseek_pipeline._filter_relevant()` 调用 `compute_semantic_similarity` 做搜索结果相关性过滤

## 5. 兼容性

- v1 API 全部保留（deprecation shim 见 `calculate_score` 重载）
- `method='tfidf'` 触发 DeprecationWarning 但可运行
