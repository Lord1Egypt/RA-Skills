# 数据格式规范 v3.0

## 目标

定义全网热点客观排行所需的统一输入字段，以及脚本输出的标准字段。

## 输入根结构

支持两种输入：

1. 按平台分组的对象
2. 扁平数组，但每条记录必须带 `platform`

### 推荐格式

```json
{
  "weibo": [],
  "xhs": [],
  "dy": [],
  "wx": [],
  "zhihu": [],
  "bilibili": [],
  "kuaishou": []
}
```

## 单条记录统一字段

以下字段并不是全部强制，但越完整越能提高排序质量。

### 基础字段

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 标题或话题名 |
| url | string | 原始链接 |
| platform | string | 平台标识 |
| author | string | 作者或账号名 |
| author_id | string | 作者或账号 ID |
| followers | number | 粉丝数 |
| publish_time | string or number | 发布时间，建议 ISO 8601 |
| content | string | 摘要或正文片段 |
| event_id | string | 已知事件 ID，可选 |

### 传播字段

| 字段 | 类型 | 说明 |
|------|------|------|
| view | number | 播放量 |
| read | number | 阅读量 |
| reads | number | 阅读量别名 |
| exposure | number | 曝光量 |
| like | number | 点赞量 |
| vote | number | 赞同量 |
| watch | number | 在看量 |

### 讨论字段

| 字段 | 类型 | 说明 |
|------|------|------|
| comment | number | 评论量 |
| comment_count | number | 评论量别名 |
| reply_count | number | 回复量 |
| qa_count | number | 问答量 |

### 转发字段

| 字段 | 类型 | 说明 |
|------|------|------|
| share | number | 分享量 |
| forward | number | 转发量 |
| repost | number | 转帖量 |
| save | number | 收藏量 |
| fav | number | 收藏量别名 |
| favorite | number | 收藏量别名 |

### 时效字段

| 字段 | 类型 | 说明 |
|------|------|------|
| delta_1h | number | 近 1 小时增量 |
| delta_3h | number | 近 3 小时增量 |
| delta_6h | number | 近 6 小时增量 |
| baseline_heat | number | 基础热度 |
| topic_type | string | breaking / news / entertainment / tech / general |

### 情绪与对立字段

| 字段 | 类型 | 说明 |
|------|------|------|
| emotion_intensity | number | 0-1，已计算好的情绪强度 |
| opposition_score | number | 0-1，已计算好的对立程度 |
| controversy_score | number | 0-1，对立程度别名 |
| positive_count | number | 正向评论数 |
| negative_count | number | 负向评论数 |
| neutral_count | number | 中性评论数 |
| support_count | number | 支持观点计数 |
| oppose_count | number | 反对观点计数 |

### 合规与去噪字段

| 字段 | 类型 | 说明 |
|------|------|------|
| is_original | boolean | 是否原创 |
| is_repost | boolean | 是否转载 |
| source_attributed | boolean | 是否标注来源 |
| has_ad | boolean | 是否商业推广 |
| is_ad | boolean | 是否广告 |
| ad_marked | boolean | 是否广告标注 |
| is_aigc | boolean | 是否 AI 生成 |
| aigc_marked | boolean | 是否 AIGC 标注 |
| spam_score | number | 0-1，已知垃圾噪音分 |

## 最小可用输入

如果只能提供最少字段，至少保证：

```json
{
  "title": "话题标题",
  "url": "https://example.com",
  "platform": "weibo",
  "publish_time": "2026-03-29T09:00:00+08:00",
  "comment": 1200,
  "share": 600,
  "read": 180000
}
```

## 输出结构

脚本默认输出以下根字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| run_meta | object | 本次运行信息 |
| ranking_basis | object | 排序权重与规则 |
| top_topics | array | 默认 Top10 热点 |
| filtered_noise | array | 被过滤或强降权的话题 |
| summary | object | 汇总信息 |

## top_topics 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | int | 排名 |
| topic_id | string | 聚类后话题 ID |
| neutral_topic | string | 中性命名后的话题名 |
| representative_titles | string[] | 代表性标题 |
| overall_score | number | 综合热点分，0-100 |
| discussion_score | number | 讨论度，0-100 |
| propagation_score | number | 传播度，0-100 |
| forwarding_score | number | 转发度，0-100 |
| emotion_score | number | 情绪强度，0-100 |
| opposition_score | number | 对立程度，0-100 |
| conflict_score | number | 对立程度别名，0-100 |
| freshness_score | number | 时效性，0-100 |
| noise_penalty | number | 0-1 |
| bias_guard_score | number | 0-1 |
| confidence | number | 0-1 |
| platform_count | int | 覆盖平台数 |
| item_count | int | 聚类内条目数 |
| platforms | string[] | 涉及平台 |
| why_hot | string | 热门原因 |
| noise_note | string | 去噪说明 |
| neutrality_note | string | 客观性说明 |
| evidence | array | 代表性来源列表 |

## filtered_noise 字段

每条至少包含：

```json
{
  "title": "标题",
  "platform": "xhs",
  "noise_penalty": 0.82,
  "noise_flags": ["promo", "lead_gen", "low_information"]
}
```
