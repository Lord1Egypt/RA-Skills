---
name: media-news-summary
description: 汇总和分析世界主要媒体对重大新闻事件的报道和观点。当用户想要了解不同国家/地区媒体对同一事件的看法、立场差异或详细报道内容时使用，例如："查看XX事件的国际媒体反应"、"世界媒体怎么看这件事"、"各国媒体头条"等。
---

# Media News Summary

将本技能用于汇总世界主要媒体对重大新闻事件的报道和观点。

## 工作流程

### 1. 确定新闻事件主题
理解用户想了解的新闻事件，确定关键词。

### 2. 收集主要媒体来源

**美国媒体：**
- 纽约时报 (NYT) - 偏自由派，深度分析
- 华尔街日报 (WSJ) - 商业/保守派视角
- 华盛顿邮报 (Washington Post)
- 福克斯新闻 (Fox News) - 保守派

**英国媒体：**
- BBC - 相对中立，事实为主
- 卫报 (The Guardian) - 偏自由派
- 金融时报 (FT) - 商业/财经视角

**欧洲媒体：**
- 法国24小时 (France 24)
- 德国之声 (DW)
- 欧盟媒体

**中东媒体：**
- 半岛电视台 (Al Jazeera)
- Al Arabiya

**亚太媒体：**
- 日本放送协会 (NHK)
- 澳大利亚广播公司 (ABC)
- 新加坡联合早报

### 3. 获取新闻内容

使用浏览器工具访问主要媒体网站获取头条新闻：

```bash
# 打开媒体网站
browser action=open targetUrl="https://www.nytimes.com/"
browser action=open targetUrl="https://www.bbc.com/news"
browser action=open targetUrl="https://www.theguardian.com/world"
browser action=open targetUrl="https://www.aljazeera.com/news/live/"
```

### 4. 分析和汇总

从收集的信息中提取：
- 事件概述
- 各国媒体关注点差异
- 社论/评论观点
- 媒体立场倾向

### 5. 输出格式

按照以下结构组织信息：

```
## 🌍 世界主要媒体观点汇总

### 📰 [国家/地区] 媒体

| 媒体 | 立场/观点 |
|------|-----------|
| 媒体名 | 具体报道或观点 |

### 🔑 媒体关注焦点

- 焦点1
- 焦点2

### 🗣️ 社论/评论标题精选

- 媒体名：「标题」（观点倾向）
```

## 输出要求

- 保持客观，呈现不同立场
- 标注信息来源
- 突出各媒体的关注点差异
- 对于争议性事件，平衡呈现多方观点
