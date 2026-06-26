# 全网热点 Top10 输出模板

## 目标

输出默认 Top10 全网热点排行，强调客观、去噪、去偏见，不额外生成内容脚本。

## 人读版模板

```markdown
# 全网热点 Top10

> 默认参数：全平台 / 最近24小时 / 去噪后排序 / 中性呈现

## 总览

| 排名 | 话题 | 综合热点分 | 讨论度 | 传播度 | 转发度 | 情绪强度 | 对立程度 | 平台数 |
|------|------|------------|--------|--------|--------|----------|----------|--------|
| 1 | {neutral_topic} | 91 | 88 | 93 | 84 | 76 | 68 | 6 |
| 2 | {neutral_topic} | 89 | 90 | 88 | 80 | 73 | 71 | 5 |

---

## No.1 {neutral_topic}

- 综合热点分：{overall_score}
- 讨论度：{discussion_score}
- 传播度：{propagation_score}
- 转发度：{forwarding_score}
- 情绪强度：{emotion_score}
- 对立程度：{opposition_score}
- 时效性：{freshness_score}
- 平台覆盖：{platform_count}
- 噪音惩罚：{noise_penalty}
- 置信度：{confidence}

热门原因：
{why_hot}

去噪说明：
{noise_note}

客观说明：
{neutrality_note}

代表性来源：
- {platform_1}: {title_1}
- {platform_2}: {title_2}
- {platform_3}: {title_3}

---
```

## JSON 模板

```json
{
  "run_meta": {
    "ts": "2026-03-29 10:30",
    "window": "24h",
    "top_n_requested": 10,
    "top_n_returned": 10,
    "mode": "objective-hot-topic-scan",
    "platforms_covered": ["weibo", "xhs", "dy", "wx", "zhihu", "bilibili"],
    "query": null
  },
  "ranking_basis": {
    "discussion_weight": 0.26,
    "propagation_weight": 0.24,
    "forwarding_weight": 0.18,
    "freshness_weight": 0.12,
    "emotion_weight": 0.10,
    "opposition_weight": 0.10,
    "noise_penalty_applied": true,
    "bias_guard_applied": true
  },
  "top_topics": [
    {
      "rank": 1,
      "topic_id": "topic_001",
      "neutral_topic": "某品牌新品发布",
      "representative_titles": [
        "标题A",
        "标题B",
        "标题C"
      ],
      "overall_score": 91.4,
      "discussion_score": 88.2,
      "propagation_score": 93.1,
      "forwarding_score": 84.3,
      "emotion_score": 76.0,
      "opposition_score": 68.5,
      "conflict_score": 68.5,
      "freshness_score": 82.7,
      "noise_penalty": 0.18,
      "bias_guard_score": 0.86,
      "confidence": 0.88,
      "platform_count": 6,
      "item_count": 14,
      "platforms": ["weibo", "xhs", "dy", "wx", "zhihu", "bilibili"],
      "why_hot": "多平台同步上升，评论和转发都高，近3小时仍在放大。",
      "noise_note": "存在部分标题党搬运，已做降权。",
      "neutrality_note": "结果仅表示热度，不表示立场正确性。",
      "evidence": [
        {
          "platform": "weibo",
          "title": "标题A",
          "url": "https://example.com/a",
          "publish_time": "2026-03-29T09:00:00+08:00"
        }
      ]
    }
  ],
  "filtered_noise": [
    {
      "title": "某抽奖引流帖",
      "platform": "xhs",
      "noise_penalty": 0.82,
      "noise_flags": ["promo", "lead_gen", "low_information"]
    }
  ]
}
```
