# 例子：学生写文献综述

> 大三学生要写毕业论文，收集了几篇 PDF 和网页文章，想整理成一份文献综述报告。

## 用户输入

```
帮我建一个知识库叫"毕业论文参考文献"，然后把这几篇论文传上去
[附件: attention.pdf, bert.pdf]
再把这个链接也存进去 https://arxiv.org/abs/2005.14165
最后帮我生成一份文献综述
```

## 调用链路

```
步骤 1 — 创建知识库
POST /api/v1/knowledge/saveCollection
Body(JSON): {"collectionName": "毕业论文参考文献", "description": "毕业论文相关参考文献"}
→ data: "collection_id_xxx"

步骤 2 — 上传本地文件（2 个可并行）
POST /api/v1/knowledge/upload  [multipart: file=@attention.pdf, collectionId=collection_id_xxx, type=PDF]
→ data.contentId: "content_001"

POST /api/v1/knowledge/upload  [multipart: file=@bert.pdf, collectionId=collection_id_xxx, type=PDF]
→ data.contentId: "content_002"

步骤 3 — URL 导入（与步骤 2 可并行）
POST /api/v1/knowledge/upload  [multipart: content=https://arxiv.org/abs/2005.14165, collectionId=collection_id_xxx, type=HTML]
⚠️ 导入网页 URL 时，URL 放在 content 字段（不是 fileUrl）
→ data.contentId: "content_003"

步骤 4a — 查询文件列表获取 contentType 和 fileId（⚠️ upload 响应不含这些字段）
POST /api/v1/knowledge/pageQueryContents?collectionId=collection_id_xxx&pageNum=1&pageSize=50
→ 从返回的 data 中找到每个文件的 contentType（如 "UPLOADV2"）和 extra.fileId

步骤 4b — 轮询所有文件解析状态（每 3-5 秒，直到全部 success）
POST /api/v1/knowledge/parseStatusThenCallBack
Body(JSON): {"reqItems": [
  {"contentType": "UPLOADV2", "contentId": "content_001", "fileId": "file_001"},
  {"contentType": "UPLOADV2", "contentId": "content_002", "fileId": "file_002"},
  {"contentType": "UPLOADV2", "contentId": "content_003", "fileId": "file_003"}
]}
→ {"file_001": "processing", "file_002": "success", "file_003": "processing"}
→ ... 继续轮询 ...
→ {"file_001": "success", "file_002": "success", "file_003": "success"}

⚠️ contentType 必须与步骤 4a 中查到的实际值匹配（UPLOAD 或 UPLOADV2），否则返回 500 错误

⏸️ 三个文件全部 success 后，才能进入下一步

也可以用简化方式：直接用 pageQueryContents 检查每个文件的 status 字段，
当所有文件 status 都是 "success" 时表示解析完成。

步骤 5 — 提交创作任务
POST /api/v1/knowledge/creationTask
Body(JSON): {
  "collectionId": "collection_id_xxx",
  "type": "PDF",
  "query": "请生成一份文献综述，对比分析这三篇论文的核心方法和创新点"
}
→ data: "creation_id_xxx"

步骤 6 — 轮询创作状态（每 30 秒）
GET /api/v1/knowledge/creationList?collectionId=collection_id_xxx
→ 找到 contentId == "creation_id_xxx" 的记录，检查 extra.status
→ extra.status: "processing" → 继续轮询
→ extra.status: "success" → 完成
```

## 展示给用户

```
已创建知识库「毕业论文参考文献」

正在导入 3 个文件…
  1. attention.pdf — 解析完成
  2. bert.pdf — 解析完成
  3. arxiv.org/abs/2005.14165 — 解析完成

正在生成文献综述…

文献综述已生成。
```

## 涉及的依赖链

```
创建知识库 → 上传/导入文件(可并行) → 查询文件列表获取参数 → 轮询解析状态全部success → 提交创作任务 → 轮询创作状态 → 完成
```

步骤 2、3 可以并行，但步骤 5 必须等步骤 4 全部 success。
