# Feishu Import (OpenClaw Plugin)

适用：将文章链接、Markdown 草稿或文件夹扫描结果导入飞书文档/知识库（通过 OpenClaw 官方 `openclaw-lark` 插件）。

## 标准流程

1. **先统一输入**
   - 先把外部内容整理成共享的 `ImportDraft`
   - 不要把来源解析逻辑直接写进目标端适配器

2. **再构造飞书负载**
   - 目标端只负责把 `ImportDraft` 转成 `openclaw-lark` 插件可接受的结构
   - 使用 `title` + `markdown`，并通过 `wiki_node` / `wiki_space` / `folder_token` 选择落点
   - 标题通过 `title` 参数传入，markdown 正文不要再重复写一级标题
   - 图片和文件使用飞书插件支持的 Lark 标签：
     - 图片：`<image url="..."/>`
     - 文件：`<file url="..." name="..."/>`
   - 本地图片/文件需要走插件的媒体工具追加（如 `feishu_doc_media`）；本仓库适配器只会保留引用提示

3. **最后做一次同步记录**
   - 成功后记录 `source_id`、`content_hash`、`remote_id`、`remote_url`
   - 这样一次性导入和增量同步都能复用同一套状态

## 推荐环境变量

- `FEISHU_FOLDER_TOKEN`
  - 飞书文件夹 token
- `FEISHU_WIKI_NODE`
  - 飞书知识库节点 token
- `FEISHU_WIKI_SPACE`
  - 飞书知识空间 ID

## 备注

- 第一版优先对齐 `openclaw-lark` 的 `feishu-create-doc` / `feishu-update-doc` 插件形状，不再依赖自定义 HTTP import endpoint
- 插件支持自动下载并上传公开 URL 的图片和文件，因此 markdown 中尽量保留可访问的 URL
- 若后续要支持增量更新，可以把已有 `doc_id` 交给 `feishu-update-doc` 的 append / replace 模式
