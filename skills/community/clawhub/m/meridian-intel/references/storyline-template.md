# Storyline Template

每条故事线（`intel/storylines/storyline_{NNN}.md`）使用此模板。

```markdown
---
id: {NNN}
title: "{一句话标题，不超过 20 字}"
category: "{tools|models|business|voices|technical|policy}"
impact: "{high|medium|low}"
date_range: "{YYYY-MM-DD} → {YYYY-MM-DD}"
source_count: {N}
---

# {标题}

## Timeline

### {YYYY-MM-DD}：{事件节点标题}

{2-3 句事实描述，不掺入观点}

- 来源：[{来源标题}]({URL})

### {YYYY-MM-DD}：{事件节点标题}

{2-3 句事实描述}

- 来源：[{来源标题}]({URL})
- 关联：[{关联内容标题}]({URL})

### {YYYY-MM-DD}：{最新进展}

{描述}

- 来源：[{来源标题}]({URL})

## Why It Matters

{2-3 句话，站在产品经理角度回答 "so what"}

- 如果你在做 {X}，需要关注 {Y}
- 这可能影响 {Z} 方向的技术选型

## Highlight Links

| 类型 | 标题 | 链接 | 为什么值得看 |
|------|------|------|-------------|
| 🎥 视频 | {title} | {url} | {一句话理由} |
| 🐦 X/Twitter | {title} | {url} | {一句话理由} |
| 📰 文章 | {title} | {url} | {一句话理由} |
| 🔧 工具/项目 | {title} | {url} | {一句话理由} |
```

## 故事线质量 Checklist

写完后自检：

- [ ] 时间节点 ≥ 2 个
- [ ] 来源 ≥ 2 个不同来源（交叉验证）
- [ ] 所有事实都附可点击链接
- [ ] 日期从来源中提取（非推测）
- [ ] 包含 "Why It Matters" 段落
- [ ] 包含 Highlight Links 表格（≥ 1 条）
- [ ] 不含模型知识补充的事实断言

**达不到以上任意一条 → 降级为 Quick Hit，不包装成故事线。**
