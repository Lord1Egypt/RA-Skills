# EasyDataset 完整 API 文档

> 基于 `D:/easy-dataset/app/api/` 下全部 90 个 `route.js` 源码生成，覆盖约 130+ 个端点。
> EasyDataset 版本：1.x | 无认证中间件 | 所有 API 均可直接调用

---

## 目录

1. [通用接口](#1-通用接口)
2. [LLM 模型管理](#2-llm-模型管理)
3. [监控与日志](#3-监控与日志)
4. [项目管理](#4-项目管理)
5. [项目配置 & Prompt](#5-项目配置--prompt)
6. [标签管理](#6-标签管理)
7. [文件管理](#7-文件管理)
8. [文本分块 Chunks](#8-文本分块-chunks)
9. [问题管理](#9-问题管理)
10. [问题模板](#10-问题模板)
11. [数据集管理](#11-数据集管理)
12. [评估数据集 & 评估任务](#12-评估数据集--评估任务)
13. [盲测任务](#13-盲测任务)
14. [图片管理 & 图片数据集](#14-图片管理--图片数据集)
15. [多轮对话数据集](#15-多轮对话数据集)
16. [数据蒸馏](#16-数据蒸馏)
17. [模型配置](#17-模型配置)
18. [HuggingFace / LlamaFactory](#18-huggingface--llamafactory)
19. [Playground & 预览](#19-playground--预览)
20. [任务管理](#20-任务管理)

---

## 1. 通用接口

### GET /api/check-update
检查 GitHub Releases 是否有新版本。无参数。

**响应**: `{ hasUpdate, currentVersion, latestVersion, releaseUrl }`

### POST /api/projects/delete-directory
物理删除项目文件目录。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| projectId | string | 是 | 项目 ID |

### POST /api/projects/migrate | GET /api/projects/migrate?taskId=
启动/查询数据迁移任务。POST 无参数，返回 `{ success, taskId }`。GET 查询任务状态（`running`/`completed`/`failed`）。

---

## 2. LLM 模型管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/llm/providers` | 获取提供商列表 |
| GET | `/api/llm/model?providerId=xxx` | 获取指定提供商的模型列表 |
| POST | `/api/llm/model` | 同步模型列表 `{ newModels[], providerId }` |
| POST | `/api/llm/fetch-models` | 从提供商 API 获取模型 `{ endpoint, providerId?, apiKey? }` |
| GET | `/api/llm/ollama/models?host=127.0.0.1&port=11434` | 获取本地 Ollama 模型 |

---

## 3. 监控与日志

三个端点：`/api/monitoring/summary`、`/api/monitoring/stats`、`/api/monitoring/logs`

全部支持查询参数：`timeRange`（`24h`/`7d`/`30d`）、`projectId`、`provider`、`status`

logs 额外支持分页：`page`、`pageSize`、`search`

---

## 4. 项目管理

| 方法 | 路径 | 请求体 | 响应 |
|------|------|--------|------|
| GET | `/api/projects/{projectId}` | — | 项目详情 + taskConfig |
| PUT | `/api/projects/{projectId}` | `{ name?, defaultModelConfigId? }` | 更新后项目 |
| DELETE | `/api/projects/{projectId}` | — | `{ success: true }` |

---

## 5. 项目配置 & Prompt

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/config` | 获取完整配置 |
| PUT | `/api/projects/{projectId}/config` | 更新 Prompt 配置 `{ prompts }` |
| GET | `/api/projects/{projectId}/custom-prompts` | 获取自定义 Prompt（query: `promptType`, `language`） |
| POST | `/api/projects/{projectId}/custom-prompts` | 保存自定义 Prompt（单个: `{promptType, promptKey, language, content}` / 批量: `{prompts[]}`） |
| DELETE | `/api/projects/{projectId}/custom-prompts?promptType=&promptKey=&language=` | 删除 |
| GET | `/api/projects/{projectId}/default-prompts?promptType=&promptKey=` | 获取默认 Prompt 内容 |

---

## 6. 标签管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/tags` | 获取标签树 |
| PUT | `/api/projects/{projectId}/tags` | 创建/更新标签 `{ tags: {id?, label, parentId?} }` |
| POST | `/api/projects/{projectId}/tags` | 按标签名查问题 `{ tagName }` |
| DELETE | `/api/projects/{projectId}/tags?id=xxx` | 删除标签 |

---

## 7. 文件管理

### 文件 CRUD

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/files?page=&pageSize=&fileName=` | 分页获取文件列表 |
| POST | `/api/projects/{projectId}/files` | 上传文件（Header: `x-file-name` 编码文件名，Body: 二进制流，仅 .md/.pdf） |
| DELETE | `/api/projects/{projectId}/files?fileId=&domainTreeAction=keep` | 删除文件及关联数据 |
| POST | `/api/projects/{projectId}/batch-delete-files` | 批量删除 `{ fileIds[], domainTreeAction?, model?, language? }` |

### GA Pairs

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/files/{fileId}/ga-pairs` | 获取文件的 GA Pairs |
| POST | `/api/projects/{projectId}/files/{fileId}/ga-pairs` | 生成 GA Pairs `{ regenerate?, appendMode?, language? }` |
| PUT | `/api/projects/{projectId}/files/{fileId}/ga-pairs` | 替换全部 GA Pairs `{ updates[{genreTitle, genreDesc, audienceTitle, audienceDesc, isActive}] }` |
| PATCH | `/api/projects/{projectId}/files/{fileId}/ga-pairs` | 切换单个激活状态 `{ gaPairId, isActive }` |
| POST | `/api/projects/{projectId}/batch-generateGA` | 批量生成 `{ fileIds[], modelConfigId, language?, appendMode? }` |
| POST | `/api/projects/{projectId}/batch-add-manual-ga` | 批量手动添加 `{ fileIds[], gaPair, appendMode? }` |

---

## 8. 文本分块 Chunks

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects/{projectId}/split` | **文本分割** `{ fileNames[], model, language?, domainTreeAction? }` 返回 `{ totalChunks, chunks[], toc, tags[] }` |
| GET | `/api/projects/{projectId}/split?filter=` | 获取所有文本块 |
| POST | `/api/projects/{projectId}/chunks` | 按 ID 数组获取 `{ array: string[] }` |
| GET | `/api/projects/{projectId}/chunks/{chunkId}` | 获取单个文本块 |
| PATCH | `/api/projects/{projectId}/chunks/{chunkId}` | 编辑内容 `{ content }` |
| DELETE | `/api/projects/{projectId}/chunks/{chunkId}` | 删除文本块 |
| GET | `/api/projects/{projectId}/chunks/name?chunkName=` | 按名称查找 |
| POST | `/api/projects/{projectId}/chunks/batch-content` | 批量获取 `{ chunkNames[] }` |
| POST | `/api/projects/{projectId}/chunks/batch-edit` | 批量编辑 `{ position, content, chunkIds[] }` |
| POST | `/api/projects/{projectId}/chunks/{chunkId}/questions` | 为文本块生成问题 `{ model, language?, number?, enableGaExpansion? }` |
| GET | `/api/projects/{projectId}/chunks/{chunkId}/questions` | 获取文本块的问题列表 |
| POST | `/api/projects/{projectId}/chunks/{chunkId}/eval-questions` | 生成测评题目 `{ model, language? }` |
| POST | `/api/projects/{projectId}/chunks/{chunkId}/clean` | AI 数据清洗 `{ model, language? }` |
| POST | `/api/projects/{projectId}/custom-split` | 自定义分块 `{ fileId, fileName, content, splitPoints[] }` |

---

## 9. 问题管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/questions?page=&size=&status=&input=&chunkName=&sourceType=` | 分页获取问题列表（status: `answered`/`unanswered`） |
| POST | `/api/projects/{projectId}/questions` | 创建问题 `{ question, chunkId?, imageId?, label? }` |
| PUT | `/api/projects/{projectId}/questions` | 更新问题 |
| DELETE | `/api/projects/{projectId}/questions/{questionId}` | 删除单个 |
| DELETE | `/api/projects/{projectId}/questions/batch-delete` | 批量删除 `{ questionIds[] }` |
| POST | `/api/projects/{projectId}/questions/export` | 导出 `{ format?, selectedIds?, filters? }` |
| POST | `/api/projects/{projectId}/generate-questions` | 批量生成 `{ model, chunkIds[], language?, enableGaExpansion? }` |
| GET | `/api/projects/{projectId}/questions/tree?tag=&input=&tagsOnly=` | 问题树视图 |

---

## 10. 问题模板

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/questions/templates?sourceType=&search=` | 获取模板列表 |
| POST | `/api/projects/{projectId}/questions/templates` | 创建模板 `{ question, sourceType, answerType, description?, labels?, customFormat?, order?, autoGenerate? }` |
| GET | `/api/projects/{projectId}/questions/templates/{templateId}` | 获取单个 |
| PUT | `/api/projects/{projectId}/questions/templates/{templateId}` | 更新 |
| DELETE | `/api/projects/{projectId}/questions/templates/{templateId}` | 删除 |

---

## 11. 数据集管理

### 核心 CRUD

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/datasets?page=&size=&input=&field=&status=&hasCot=&scoreRange=&chunkName=` | 分页获取（status: `confirmed`/`unconfirmed`） |
| POST | `/api/projects/{projectId}/datasets` | 为单个问题生成答案 `{ questionId, model, language? }` |
| PATCH | `/api/projects/{projectId}/datasets?id=xxx` | 编辑数据集 `{ answer?, cot?, question?, confirmed? }` |
| DELETE | `/api/projects/{projectId}/datasets?id=xxx` | 删除数据集 |
| GET | `/api/projects/{projectId}/datasets/{datasetId}?operateType=prev` | 详情/导航 |
| PATCH | `/api/projects/{projectId}/datasets/{datasetId}` | 更新元数据 `{ score?, tags[], note? }` |

### 评估 & 优化

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects/{projectId}/datasets/{datasetId}/evaluate` | 评估质量 `{ model, language? }` |
| POST | `/api/projects/{projectId}/datasets/batch-evaluate` | 批量评估 → 返回 `{ taskId }` |
| POST | `/api/projects/{projectId}/datasets/optimize` | 优化答案 `{ datasetId, model, advice, language? }` |
| POST | `/api/projects/{projectId}/datasets/generate-eval-variant` | 生成评估变体 `{ datasetId, model, language?, questionType?, count? }` |
| GET | `/api/projects/{projectId}/datasets/{datasetId}/token-count` | Token 计数 |

### 导入/导出

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects/{projectId}/datasets/export` | 导出 `{ batchMode?, offset?, batchSize?, balanceMode?, selectedIds?, status? }` |
| POST | `/api/projects/{projectId}/datasets/import` | 导入 `{ datasets[{question, answer, chunkName?, ...}], sourceInfo? }` |
| GET | `/api/projects/{projectId}/datasets/tags` | 获取所有标签 |

---

## 12. 评估数据集 & 评估任务

### 评估数据集

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/eval-datasets?page=&pageSize=&questionType=&keyword=&tags=` | 列表 |
| POST | `/api/projects/{projectId}/eval-datasets` | 创建 `{ question, correctAnswer, questionType?, tags?, note?, chunkId?, options? }` |
| DELETE | `/api/projects/{projectId}/eval-datasets` | 批量删除 `{ ids[] }` |
| GET/PUT/DELETE | `/api/projects/{projectId}/eval-datasets/{evalId}` | 详情/更新/删除 |
| GET | `/api/projects/{projectId}/eval-datasets/count` | 统计 `{ total, byType, hasSubjective }` |
| POST | `/api/projects/{projectId}/eval-datasets/sample` | 随机采样 `{ questionType?, limit?, strategy? }` |
| POST | `/api/projects/{projectId}/eval-datasets/export` | 导出 `{ format?, questionTypes[], tags[], keyword? }` |
| POST | `/api/projects/{projectId}/eval-datasets/import` | 导入（multipart: file + questionType + tags） |

### 评估任务

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/eval-tasks` | 任务列表 |
| POST | `/api/projects/{projectId}/eval-tasks` | 创建 `{ models[{modelId, providerId}], evalDatasetIds[], judgeModelId?, judgeProviderId?, language? }` |
| GET | `/api/projects/{projectId}/eval-tasks/{taskId}?page=&type=&isCorrect=` | 任务详情+结果 |
| PUT | `/api/projects/{projectId}/eval-tasks/{taskId}` | 中断 `{ action: "interrupt" }` |
| DELETE | `/api/projects/{projectId}/eval-tasks/{taskId}` | 删除 |

---

## 13. 盲测任务

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/blind-test-tasks` | 任务列表 |
| POST | `/api/projects/{projectId}/blind-test-tasks` | 创建 `{ modelA, modelB, evalDatasetIds[] }` |
| GET | `/api/projects/{projectId}/blind-test-tasks/{taskId}` | 详情（含所有结果和评分） |
| GET | `/api/projects/{projectId}/blind-test-tasks/{taskId}/current` | 获取当前问题 + 两模型回答 |
| GET | `/api/projects/{projectId}/blind-test-tasks/{taskId}/question` | 获取当前问题信息 |
| GET | `/api/projects/{projectId}/blind-test-tasks/{taskId}/stream` | **SSE 流式**，两模型同时回答 |
| GET | `/api/projects/{projectId}/blind-test-tasks/{taskId}/stream-model?model=A` | 单模型流式 |
| POST | `/api/projects/{projectId}/blind-test-tasks/{taskId}/vote` | 提交投票 `{ vote, questionId, isSwapped, leftAnswer?, rightAnswer? }` |

---

## 14. 图片管理 & 图片数据集

### 图片管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/images?page=&pageSize=&imageName=&hasQuestions=&hasDatasets=` | 分页获取图片列表 |
| POST | `/api/projects/{projectId}/images` | 从目录导入 `{ directories[] }` |
| DELETE | `/api/projects/{projectId}/images?imageId=xxx` | 删除图片及关联数据 |
| GET | `/api/projects/{projectId}/images/{imageId}` | 图片详情（含问题+标注） |
| POST | `/api/projects/{projectId}/images/annotations` | 创建标注 `{ imageId, questionId, question, answerType, answer, note? }` |
| POST | `/api/projects/{projectId}/images/questions` | **AI 生成问题** `{ imageName, count?, model, language? }` |
| POST | `/api/projects/{projectId}/images/datasets` | **AI 生成答案** `{ imageName, question, model, language?, previewOnly? }` |
| GET | `/api/projects/{projectId}/images/next-unanswered` | 下一个待标注图片 |
| POST | `/api/projects/{projectId}/images/zip-import` | ZIP 导入（multipart: file .zip） |
| POST | `/api/projects/{projectId}/images/pdf-convert` | PDF 转图片导入（multipart: file .pdf） |

### 图片数据集

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/image-datasets?page=&pageSize=&search=&confirmed=&minScore=&maxScore=` | 列表 |
| GET/PUT/DELETE | `/api/projects/{projectId}/image-datasets/{datasetId}` | 详情/更新/删除 |
| POST | `/api/projects/{projectId}/image-datasets/export` | 导出 JSON `{ confirmedOnly? }` |
| GET | `/api/projects/{projectId}/image-datasets/export-zip?confirmedOnly=` | 导出图片 ZIP |
| GET | `/api/projects/{projectId}/image-datasets/tags` | 标签列表 |

---

## 15. 多轮对话数据集

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/dataset-conversations?page=&pageSize=&keyword=&roleA=&roleB=&scenario=&scoreMin=&scoreMax=&confirmed=` | 列表 |
| POST | `/api/projects/{projectId}/dataset-conversations` | 创建 `{ questionId, model, systemPrompt?, scenario?, rounds?, roleA?, roleB?, language? }` |
| GET/PUT/DELETE | `/api/projects/{projectId}/dataset-conversations/{conversationId}` | 详情/更新/删除 |
| GET | `/api/projects/{projectId}/dataset-conversations/export?confirmed=` | 导出 ShareGPT |

---

## 16. 数据蒸馏

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects/{projectId}/distill/questions` | 生成蒸馏问题 `{ tagPath, currentTag, tagId?, count?, model, language? }` |
| GET | `/api/projects/{projectId}/distill/questions/by-tag?tagId=` | 按标签查问题 |
| POST | `/api/projects/{projectId}/distill/tags` | 生成子标签 `{ parentTag, tagPath, count?, model, language? }` |
| GET | `/api/projects/{projectId}/distill/tags/all` | 所有蒸馏标签 |
| PUT | `/api/projects/{projectId}/distill/tags/{tagId}` | 更新标签名 `{ label }` |

---

## 17. 模型配置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/model-config` | 模型配置列表（首次自动创建默认）→ `{ data[], defaultModelConfigId }` |
| POST | `/api/projects/{projectId}/model-config` | 保存 `{ providerId, providerName, endpoint, apiKey, modelId?, modelName?, type?, temperature?, maxTokens?, topK?, topP?, status? }` |
| DELETE | `/api/projects/{projectId}/model-config/{modelConfigId}` | 删除 |

---

## 18. HuggingFace / LlamaFactory

### HuggingFace

**POST** `/api/projects/{projectId}/huggingface/upload`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| token | string | 是 | HF API Token |
| datasetName | string | 是 | username/dataset-name |
| isPrivate | boolean | 是 | |
| formatType | string | 是 | `alpaca`/`sharegpt`/`multilingualthinking`/`custom` |
| fileFormat | string | 是 | `json`/`jsonl`/`csv` |
| systemPrompt | string | 否 | |
| confirmedOnly | boolean | 否 | |
| includeCOT | boolean | 否 | |
| customFields | object | 否 | formatType=custom 时必填 |

### LlamaFactory

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/llamaFactory/checkConfig` | 检查配置 `{ exists, configPath }` |
| POST | `/api/projects/{projectId}/llamaFactory/generate` | 生成配置 `{ formatType, systemPrompt?, confirmedOnly?, includeCOT? }` |

---

## 19. Playground & 预览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/projects/{projectId}/playground/chat` | 非流式聊天 `{ model, messages[] }` → `{ response }` |
| POST | `/api/projects/{projectId}/playground/chat/stream` | 流式聊天（SSE），参数相同 |
| GET | `/api/projects/{projectId}/preview/{fileId}` | 文件内容预览 |

---

## 20. 任务管理

### 异步任务类型（taskType）

| 类型 | 说明 |
|------|------|
| `file-processing` | 文件处理（文本分割+领域树） |
| `question-generation` | 批量生成问题 |
| `answer-generation` | 批量生成答案 |
| `image-question-generation` | 批量生成图片问题 |
| `image-dataset-generation` | 批量生成图片数据集 |
| `data-cleaning` | 数据清洗 |

### 任务状态码

| 值 | 含义 |
|----|------|
| 0 | 处理中 |
| 1 | 已完成 |
| 2 | 失败 |
| 3 | 已中断 |

### API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/projects/{projectId}/tasks` | 获取任务配置 |
| PUT | `/api/projects/{projectId}/tasks` | 更新任务配置 |
| POST | `/api/projects/{projectId}/tasks` | **创建任务** `{ taskType, modelInfo?, language?, detail?, totalCount?, note? }` → `{ code:0, data:{ id, status, ... } }` |
| GET | `/api/projects/{projectId}/tasks/{taskId}` | 获取任务详情 **注意：响应为 `{ code:0, data:{ id, status, completedCount, totalCount, ... } }`** |
| PATCH | `/api/projects/{projectId}/tasks/{taskId}` | 更新任务 `{ status?, completedCount?, totalCount?, detail?, note? }` |
| DELETE | `/api/projects/{projectId}/tasks/{taskId}` | 删除 |
| GET | `/api/projects/{projectId}/tasks/list?taskType=&status=&page=&limit=` | 任务列表 |

---

## 通用响应格式

**成功**: `{ code: 0, data: {...}, message: "..." }` 或直接返回对象/数组

**错误**:
| 状态码 | 含义 |
|--------|------|
| 400 | 参数错误 / 缺少必填字段 |
| 401 | 认证失败（API 密钥无效） |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

**注意**: EasyDataset 本身无认证中间件，所有 API 直接可调用。认证仅在调用外部 LLM API 时需要。

---

*本文档共覆盖 90 个 route.js 文件，约 130+ 个端点。*
*EasyDataset: 文本/图片数据集均可完全通过 REST API 驱动，无需 Web UI。*
