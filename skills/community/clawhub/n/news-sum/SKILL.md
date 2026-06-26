---
name: news-sum
description: 新闻汇总与邮件投递技能。当用户要求"生成今日新闻汇总"、"把新闻发给邮箱"时触发。支持：(1) 接收用户指定主题，搜索生成新闻汇总；(2) 按用户要求投递到指定邮箱。
---

# News Sum

新闻搜索生成与邮件投递。

## 默认参数
汇总文件路径：`workspace/archive/news/news-{yyyymmdd}.md`
JSON文件路径：`workspace/archive/news/json/json-{yyyymmdd}-{topic}.json`
draf文件路径：`workspace/archive/news/draf/draft-{yyyymmdd}.md`
默认检索主题：topics = `国际局势 经济金融 科技AI`

## 整体流程：主编 → 编辑 → 记者三层架构

```
主agent（主编）
    │
    ├─ Step 1: 读取昨日新闻，识别持续事件
    │
    ├─ Step 2: 并行启动记者subagent（每个topic一个）
    │           记者生成 json-{yyyymmdd}-topic.json
    │
    ├─ Step 3: 等待所有记者完成
    │
    ├─ Step 4: 启动编辑subagent
    │           编辑整合所有json → 生成 draft-{yyyymmdd}.md
    │
    └─ Step 5: 主agent读取draft.md
                添加【综合分析】【预测】
                生成最终文件 {yyyymmdd}.md + recent-brief.md
```

---

## Step 1 读取历史，追踪持续事件

1. 读取近期新闻brief文件 `archive/news/recent-brief.md`
2. 识别各topic中的持续性事件，提取1-2个关键词/topic 辅助记者agent追踪
3. 如无则略过

---

## Step 2 并行启动记者Subagent
**执行方式：**
- 使用 `sessions_spawn` 并行启动每个topic的记者subagent
- runtime = `subagent`，mode = `run`
- 所有topic同时启动，不串行等待
- 等待所有 childSessionKey 的 completion 事件返回

**记者prompt模板：** `references/journalist.md`

---

## Step 3 等待记者完成

收集所有记者返回的json文件路径，校验是否完整。如有失败，记录该topic，主agent可选择补做或标注"数据获取失败"。

---

## Step 4 启动编辑Subagent

记者全部完成后，启动编辑subagent同时告知对应json文件路径：

**编辑prompt模板：** `references/editor.md`

- 读取所有 json-{yyyymmdd}-*.json 文件
- 识别热点事件，建立专题
- 补搜非热点新闻（如某topic下非热点新闻不足3条）
- 生成 `draft-{yyyymmdd}.md`

---

## Step 5 主编生成最终文件

主agent读取 `draft-{yyyymmdd}.md`，以资深总编身份：

1. 补充【综合分析】【预测】章节
2. 按 `references/format.md` 格式写入最终文件 `news-{yyyymmdd}.md`
3. 更新近期新闻brief文件 `archive/news/recent-brief.md` -每个topic总结几个近期热点，滚动更新，整个文件控制在500字内。

---

## 核心原则

- **并行**：所有记者subagent同时启动
- **记者独立性**：每个记者只管自己topic，不参考其他topic的json
- **编辑整合**：编辑层负责跨topic的热点专题化和去重
- **主编把关**：最终文件由主agent亲自执笔总结分析
- 总字数  7000字 - 10000字

---

## 功能2：新闻邮件投递

当用户要求投递到邮箱时：

1. 读取今日新闻汇总，如无则退出
2. 将 markdown 转换为 HTML（直接在内存中转换，不生成临时文件）
3. 发送邮件：
   ```bash
   gog gmail send --to="{EmailTarget}" --subject="NewsToday {yyyy-mm-dd}" --attach="{dir}/news-yyyymmdd.md" --body-html="$(printf '%s' '{HTML内容}')"
   ```
4. **注意**：`--body-html` 使用 `$(printf '%s' ...)` 避免回车丢失
