# 例子：先搜索再定向生成

> 知识库里有几十篇文章，用户只想用其中和某个话题相关的几篇来生成报告。

## 用户输入

```
在「AI 论文集」里搜一下关于注意力机制的内容，然后用相关的文章生成一份对比分析
```

## 调用链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「AI 论文集」collectionId: "xxx"

步骤 2 — 获取文件列表和摘要（替代文件级搜索）
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
（参数通过 URL query string 传递）
→ 返回文件列表，每个文件含 fileName、summary、contentId、status 字段

步骤 3 — Agent 根据文件名和摘要匹配用户需求
→ 从文件列表中找到与"注意力机制"相关的文件（根据 fileName 和 summary 内容判断）：
  - contentId: "content_att", fileName: "attention.pdf", summary: "Self-attention 的计算复杂度..."
  - contentId: "content_bert", fileName: "bert.pdf", summary: "BERT uses a multi-layer bidirectional..."
  - contentId: "content_gpt", fileName: "gpt4_report.pdf", summary: "GPT-4 extends the attention..."
→ 同时确认这些文件的 status 都是 "success"（已解析完成）

步骤 4 — 展示匹配的文件，让用户确认
→ "找到 3 个与注意力机制相关的文件，用这 3 篇生成，确认吗？"

步骤 5 — 用匹配的文件提交创作任务
POST /api/v1/knowledge/creationTask
Body(JSON): {
  "collectionId": "xxx",
  "type": "PDF",
  "query": "对比分析这几篇论文中注意力机制的设计差异和演进",
  "files": [
    {"contentId": "content_att"},
    {"contentId": "content_bert"},
    {"contentId": "content_gpt"}
  ]
}
→ data: "creation_id"

步骤 6 — 轮询创作状态
GET /api/v1/knowledge/creationList?collectionId=xxx
→ 找到 contentId == "creation_id" 的记录，检查 extra.status: "success"
```

## 展示给用户

```
在「AI 论文集」中找到 3 个与"注意力机制"相关的文件：

1. **attention.pdf** — Self-attention 的计算复杂度为 O(n²·d)...
2. **bert.pdf** — BERT 使用多层双向 Transformer 编码器...
3. **gpt4_report.pdf** — GPT-4 扩展了注意力架构...

用这 3 篇生成对比分析，确认吗？
```

用户确认后：

```
正在生成对比分析…

内容已生成。
```

## 关键规则

- 后端不提供文件级语义搜索，Agent 需通过文件列表的 `fileName` 和 `summary` 字段自行匹配
- 也可使用 `fileName` 参数按文件名关键字过滤
- 搜索结果展示后，最好让用户确认再生成，而不是直接执行
