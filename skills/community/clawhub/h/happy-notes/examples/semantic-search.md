# 例子：语义检索知识库内容

> 用户想在知识库中查找与某个话题相关的具体内容片段，而不是整个文件。

## 用户输入

```
在「天文论文集」里搜一下关于宇宙演化巡天的内容
```

## 调用链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「天文论文集」collectionId: "f61124bf-ec22-44ea-93cc-36cd4a35a568"

步骤 2 — 语义检索（提示用户可能需要等待）
POST /api/v1/knowledge/searchChunk
Body(JSON): {
  "query": "宇宙演化巡天",
  "collectionId": "f61124bf-ec22-44ea-93cc-36cd4a35a568"
}
⚠️ 同步接口，可能需要几秒到几十秒

→ 返回 nodes 数组，包含匹配的文本片段和图片片段
```

## 展示给用户

```
正在检索「天文论文集」中与"宇宙演化巡天"相关的内容，请稍候…

找到 2 个相关内容片段：

1. **[文本 · 来自 cosmos-survey.pdf]**（匹配度：高）
   天文学的重要目标是测绘和理解宇宙内容。宇宙演化巡天（COSMOS）填补了浅场
   宽面积巡天和深场点束太空巡天之间的空白，覆盖2平方度的连续区域…

2. **[图片 · 来自 cosmos-survey.pdf]**（匹配度：高）
   这是一张双纵轴的天文观测数据图，横轴为波长（μm），显示在不同波长下
   各仪器的灵敏度水平。
   ![Figure 1](https://files.iflow.cn/knowledge_index/10006179002/xxx/2.png)
```

## 变体：限定文件检索

用户说"在那篇 COSMOS 论文里找一下关于 JWST 的内容"时：

```
步骤 1 — 先通过文件列表找到目标文件
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
→ 找到 cosmos-survey.pdf 的 contentId: "8232544f-..."

步骤 2 — 限定文件范围检索
POST /api/v1/knowledge/searchChunk
Body(JSON): {
  "query": "JWST 观测",
  "collectionId": "xxx",
  "contentIds": ["8232544f-..."]
}
→ 只在该文件内检索，速度更快
```

## 变体：检索后生成报告

用户说"找一下关于宇宙演化的内容，然后生成一份总结"时：

```
步骤 1 — 语义检索
POST /api/v1/knowledge/searchChunk
→ 返回匹配片段，记录片段来源的 contentId 列表

步骤 2 — 展示检索结果，确认生成
→ "找到 3 个相关片段，来自 2 个文件。用这些文件生成总结，确认吗？"

步骤 3 — 用检索结果中的文件提交创作任务
POST /api/v1/knowledge/creationTask
Body(JSON): {
  "collectionId": "xxx",
  "type": "PDF",
  "query": "总结宇宙演化巡天的研究进展",
  "files": [
    {"contentId": "contentId1"},
    {"contentId": "contentId2"}
  ]
}
```

## 关键规则

- `searchChunk` 是**同步接口**，可能很慢（几秒到几十秒），调用前必须提示用户等待
- 使用 curl 直接调用时需加 `--max-time 120` 设置超时
- 返回的片段可能是文本（`type=text`）或图片（`type=image`），展示时需区分处理
- 图片片段的 `text` 字段是 Markdown 格式的图片链接，可直接渲染
- `contentIds` 不传则检索全部文件，传了则只在指定文件内检索（更快）
- 返回的 `contentId` 可直接用于 `creationTask` 的 `files` 参数
