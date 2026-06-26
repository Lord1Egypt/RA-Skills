# 例子：向已有知识库追加文件再生成（易混淆场景）

> 用户已有知识库「竞品分析」，里面有 3 个旧文件。现在想加一篇新的公众号文章，然后用新旧文章一起生成内容。

## 用户输入

```
把这个链接加到竞品分析的知识库里 https://mp.weixin.qq.com/s/xxx，然后帮我做个总结
```

## 错误链路（跳过解析等待）

```
POST /api/v1/knowledge/upload
[multipart: content=https://mp.weixin.qq.com/s/xxx, collectionId=xxx, type=HTML]
→ data.contentId: "content_new"

# ❌ 文件还在 parsing，直接提交创作任务
POST /api/v1/knowledge/creationTask
Body(JSON): {"collectionId": "xxx", "type": "PDF"}
→ 错误码 40004: "文件解析中，暂不可用"
   或者：创作只包含旧的 3 个文件内容，新文章没被用上
```

**错误原因：** 新文件还在 parsing，索引尚未建立。创作内容要么报错，要么漏掉新文章。

## 正确链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「竞品分析」collectionId: "xxx"

步骤 2 — 导入新文章
POST /api/v1/knowledge/upload
[multipart: content=https://mp.weixin.qq.com/s/xxx, collectionId=xxx, type=HTML]
→ data.contentId: "content_new"

步骤 3a — 查询文件列表获取 contentType 和 fileId
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
（参数通过 URL query string 传递）
→ 找到 contentId="content_new" 的文件，读取 contentType（如 "UPLOADV2"）和 extra.fileId

步骤 3b — 轮询直到 success
POST /api/v1/knowledge/parseStatusThenCallBack
Body(JSON): {"reqItems": [{"contentType": "UPLOADV2", "contentId": "content_new", "fileId": "file_new"}]}
→ {"file_new": "processing"}
→ {"file_new": "processing"}
→ {"file_new": "success"} ✓

也可以简化：直接反复调用 pageQueryContents，检查该文件的 status 字段是否变为 "success"

⏸️ 确认 status=success 后才继续

步骤 4 — 提交创作任务（不传 files = 使用全部 4 个文件）
POST /api/v1/knowledge/creationTask
Body(JSON): {"collectionId": "xxx", "type": "PDF", "query": "请总结分析所有参考资料"}
→ data: "creation_id"

步骤 5 — 轮询创作状态
GET /api/v1/knowledge/creationList?collectionId=xxx
→ 找到 contentId == "creation_id" 的记录，检查 extra.status: "success"
```

## 展示给用户

```
正在导入公众号文章到知识库「竞品分析」…
公众号文章已导入，解析完成（知识库现有 4 个文件）

正在生成内容…

内容已生成。
```

## 关键规则

- **导入和生成不能并行提交**，必须等文件 `status=success` 后再生成
- 不传 `files` 时使用知识库全部文件，不需要额外查询文件列表
