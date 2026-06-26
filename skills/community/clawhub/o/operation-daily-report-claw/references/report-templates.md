# 日报模板库

## 简洁版（Quick Summary）

适合：快速浏览，移动端查看

```markdown
# 运营日报 · {date}

## 核心指标

| 平台 | 播放量 | 涨粉 | 互动率 |
|------|--------|------|--------|
| 抖音 | 12,345 | +89  | 3.2%   |
| 小红书 | 8,901 | +45 | 5.1%   |
| 视频号 | 3,456 | +12 | 2.8%   |

**合计播放量**：24,702  **合计涨粉**：+146

{anomaly_section}
```

---

## 详细版（Full Report）

适合：周会汇报，深度分析

```markdown
# 运营数据日报 · {date}

> 生成时间：{generated_at} | 数据来源：各平台 API

---

## 📊 数据概览

### 抖音
- 播放量：{douyin.views}（环比 {douyin.views_change}）
- 点赞数：{douyin.likes}
- 评论数：{douyin.comments}
- 转发数：{douyin.shares}
- 涨粉：{douyin.new_followers}（总粉丝：{douyin.total_followers}）
- 互动率：{douyin.engagement_rate}
- 完播率：{douyin.completion_rate}

### 小红书
- 阅读量：{xhs.views}（环比 {xhs.views_change}）
- 点赞数：{xhs.likes}
- 收藏数：{xhs.favorites}
- 评论数：{xhs.comments}
- 涨粉：{xhs.new_followers}
- 互动率：{xhs.engagement_rate}

### 视频号
（同上格式）

---

## 📈 近 7 日趋势

| 日期 | 抖音播放 | 小红书阅读 | 视频号播放 | 合计涨粉 |
|------|---------|-----------|-----------|---------|
| {d-6} | ... | ... | ... | ... |
| {d-5} | ... | ... | ... | ... |
| ...  | ... | ... | ... | ... |
| 昨日 | ... | ... | ... | ... |

---

## 🏆 优质内容 TOP 3

1. **{top1.title}**（{top1.platform}）— 播放 {top1.views}，互动率 {top1.engagement_rate}
2. **{top2.title}**（{top2.platform}）— 播放 {top2.views}，互动率 {top2.engagement_rate}
3. **{top3.title}**（{top3.platform}）— 播放 {top3.views}，互动率 {top3.engagement_rate}

---

{anomaly_section}
```

---

## 对比版（Cross-Platform Comparison）

适合：多平台运营，横向对比

```markdown
# 多平台数据对比 · {date}

## 播放量对比

| 平台 | 昨日 | 前日 | 环比 | 上周同日 | 同比 |
|------|------|------|------|---------|------|
| 抖音 | ... | ... | ▲5% | ... | ▲12% |
| 小红书 | ... | ... | ▼2% | ... | ▲8% |
| 视频号 | ... | ... | ▲1% | ... | ▲3% |

## 涨粉对比

（同上格式）

## 互动率对比

（同上格式）

## 综合评分

根据播放量、涨粉、互动率加权计算：
- 🥇 抖音：92分
- 🥈 小红书：87分
- 🥉 视频号：74分
```

---

## 异常版（Anomaly Report）

适合：问题排查，仅展示异常数据

```markdown
# ⚠️ 数据异常预警 · {date}

以下指标出现异常，请关注：

{anomaly_list}

## 异常详情

### {platform} · {metric}
- 当前值：{current_value}
- 正常范围：{normal_range}
- 异常程度：{severity}（{change_pct}）
- 建议：{suggestion}
```

---

## anomaly_section 模板

无异常时：
```markdown
✅ 今日数据无异常
```

有异常时：
```markdown
## ⚠️ 异常提醒

{anomaly_list}
```
