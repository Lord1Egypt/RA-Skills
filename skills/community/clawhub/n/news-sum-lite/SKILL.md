---
name: news-sum-lite
description: 轻量新闻日报 skill。触发条件：用户说"今日新闻"、"新闻日报"、"生成今日新闻"。主打快速、轻量、一气呵成。
---

# News Sum Lite
轻量快速新闻日报，一次性生成，不起并发。

## 默认设置
- 文件路径：`archive/news/brief/brief-yyyymmdd.md`
- 默认主题：国际局势，经济金融，科技AI

## 整体流程概述：
- 搜索-延伸话题再搜索-整理-保存-发送

## 详细流程

### Step 1 搜索
- 并行搜索用户所给主题， 
注意
1. **中英文query**都要使用，时间为**当日**
2. `web_search` `tavily_search` 均衡使用
3. 最终新闻源**中外来源比例保持1:1**
4. 必须有新闻源，**禁止幻想**

### Step 2 延伸
- 根据已搜索内容，主动探索出**一个相关的topic**进行**再搜索**

### Step 3 整理

- 每条新闻生成中文摘要（**300字**）
- 提取 标题，时间，新闻源，新闻链接

### Step 4 保存

- 严格按照**模版格式**，写入 `archive/news/brief/brief-yyyymmdd.md`
- 主动探索的 **New Topic** 也要写入

### Step 5 发送邮件
严格调用以下命令发送邮件，确保格式正确，md文件作为附件，html格式内容作为邮件正文：
```bash
HTML=$(npx marked {todays-brief.md} --breaks)
HTML="<div style='font-family:Arial, sans-serif; line-height:1.6;'>$HTML</div>"
gog gmail send --to={aim-email} --subject="今日简报 yyyy-mm-dd" --attach={todays-brief.md} --body-html "$HTML"
```

## 格式
# 日报格式模板

```markdown
## 📋 今日新闻日报 {日期}
---
### [emoji] {topic}
- **标题**
**摘要**：
**时间**：yyyy-mm-dd ｜ [新闻源](新闻链接)
- **标题**
**摘要**：
**时间**：yyyy-mm-dd ｜ [新闻源](新闻链接)
...
### [emoji] {topic}
...
### [emoji] {New topic}
...
---
## 💡 今日要点
- 简要总结今日最重要2-3件事
---
## 🔮 简单预测
---
生成时间：{时间}
```
