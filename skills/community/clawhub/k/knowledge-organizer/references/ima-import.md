# Tencent IMA Import (OpenAPI)

适用：将文章链接、Markdown 草稿或文件夹扫描结果导入腾讯 IMA 笔记（知识库）。

## 标准流程

1. **先统一输入**
   - 先把外部内容整理成共享的 `ImportDraft`
   - 不要把来源解析逻辑直接写进目标端适配器

2. **再构造 IMA OpenAPI 负载**
   - 目标端只负责把 `ImportDraft` 转成 IMA `import_doc` 可接受的结构
   - 第一版只使用官方文档字段：`content_format`、`content`、可选 `folder_id`
   - 图片/附件等媒体信息会被写入 Markdown 内容里，避免依赖未公开的上传字段

3. **最后做一次同步记录**
   - 成功后记录 `source_id`、`content_hash`、`remote_id`（doc_id）
   - 这样一次性导入和增量同步都能复用同一套状态

## 推荐环境变量

- `IMA_OPENAPI_CLIENTID`
  - IMA OpenAPI Client ID
- `IMA_OPENAPI_APIKEY`
  - IMA OpenAPI Api Key
- `IMA_OPENAPI_BASE_URL` (可选)
  - 默认：`https://ima.qq.com/openapi/note/v1`
- `IMA_OPENAPI_FOLDER_ID` (可选)
  - 目标笔记本 folder_id

## 备注

- 目前适配器直接对齐 OpenClaw 的 IMA OpenAPI 用法：`POST /import_doc` 写入 Markdown
- 如果 API 返回业务错误码（例如 `100001` 参数错误），适配器会直接报错，不会把这次导入记成成功同步
- 若后续需要增量同步更新，可以在已保存的 `doc_id` 上使用 `append_doc` 追加一条“同步更新”段落
