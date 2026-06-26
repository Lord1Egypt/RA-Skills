# 例子：长任务异步处理（播客/视频）

> 产品经理收藏了多篇行业文章，想生成一期播客给团队听，同时也要一个思维导图。

## 用户输入

```
用「行业洞察」知识库里的内容，帮我生成一期播客，顺便也做个思维导图
```

## 调用链路

```
步骤 1 — 确认知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「行业洞察」collectionId: "xxx"

步骤 2 — 确认文件状态（必须全部解析完成才能生成）
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
（参数通过 URL query string 传递）
→ 8 个文件，检查每个文件的 status 字段
→ 全部 status: "success" ✓（如果有 "processing" 的，需要先等解析完成）

步骤 3 — 并行提交两个生成任务

POST /api/v1/knowledge/creationTask
Body(JSON): {"collectionId": "xxx", "type": "PODCAST", "query": "生成播客脚本"}
→ data: "creation_pod"

POST /api/v1/knowledge/creationTask
Body(JSON): {"collectionId": "xxx", "type": "XMIND"}
→ data: "creation_map"

步骤 4 — 所有创作任务耗时较长，提交后立即告知用户，不阻塞等待
→ 思维导图预计 15-30 分钟
→ 播客预计 10-20 分钟
→ 用户稍后问"做好了吗"时查询：
GET /api/v1/knowledge/creationList?collectionId=xxx
→ 找到 contentId == "creation_map" 的记录，检查 extra.status
→ 找到 contentId == "creation_pod" 的记录，检查 extra.status
→ extra.status: "pending" → 排队中（正常，告知用户）
→ extra.status: "processing" → 生成中
→ extra.status: "success" ✓ 完成
```

## 展示给用户

**提交后立即展示：**
```
已提交 2 个生成任务：

思维导图 — 已提交（预计 15-30 分钟）
播客 — 已提交（预计 10-20 分钟）
```

**用户稍后问"做好了吗"时：**
```
思维导图 — 已完成 ✅
播客 — 生成中，请稍候
```

**全部完成时：**
```
思维导图 — 已完成 ✅
播客 — 已完成 ✅
```

## 关键规则

- **所有创作任务耗时较长**（10-30分钟），提交后立即告知用户预估时间，不要阻塞等待
- 报告类（PDF/DOCX/MARKDOWN）和播客：预计 10-20 分钟
- PPT、思维导图、视频：预计 15-30 分钟
- 两个独立的生成任务**可以并行提交**（它们不互相依赖）
- 但生成任务和文件导入之间**不能并行**（必须文件 status=success 后再生成）
- 不支持 Webhook/回调通知，需要轮询 `creationList` 检查状态
- 轮询 `creationList` 时，用 `contentId` 匹配具体任务（不要只看第一条记录）
- 状态为 `pending` 是正常排队，不是错误
