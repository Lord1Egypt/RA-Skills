# Image Compressor Reference

这个 skill 封装的是已发布的 `rv-image-optimize` 包，内容尽量与项目 README 和 CLI 实际行为保持一致。当前既覆盖压缩，也覆盖 `upload` / `pipeline` 两个面向 Agent 的上传入口。  
This skill wraps the published `rv-image-optimize` package and stays aligned with the project README and CLI behavior. It now covers both compression and the Agent-facing `upload` / `pipeline` entry points.

## 安装方式 / Install options

### 安装 npm 包 / Install the package

```bash
npm install rv-image-optimize
```

### 无全局安装时运行 / Run without global install

```bash
npx rv-image-optimize ./images --output-dir ./compressed --format webp --quality 82 --json
```

### 上传已有文件 / Upload existing files

```bash
npx rv-image-optimize upload ./dist/demo.webp --config ./upload.config.json --json
```

### 大文件分片上传 / 断点续传 / Chunked resumable upload

```bash
npx rv-image-optimize upload ./large-assets --config ./upload.chunk.config.json --timeout-ms 10000 --json
```

### 一体化压缩后上传 / Compress then upload

```bash
npx rv-image-optimize pipeline ./images --format webp --quality 82 --config ./upload.config.json --json
```

## 推荐默认值 / Recommended defaults

- 输出格式 / Format: `webp`
- 压缩质量 / Quality: `82`
- 输出模式 / Output mode: `--output-dir`
- 结构化结果 / Structured result: `--json`
- 高风险参数 / Destructive flags: 默认关闭 / off by default
- 上传配置 / Upload config: 优先使用 `--config`
- 大文件上传 / Large file uploads: 优先把 `chunkUpload` 写进 `--config`
- 请求体方式 / Request body: 仅保留 `FormData`

## 支持的输出格式 / Supported output formats

- `jpeg`
- `png`
- `webp`
- `avif`

## 常用 CLI 参数 / Useful CLI flags

- `--output <file>`: 单文件精确输出路径 / exact output path for a single file
- `--output-dir <dir>`: 输出到目标目录 / write results to a target directory
- `--format <fmt>`: 指定输出格式 / choose output format
- `--quality <1-100>`: 指定压缩质量 / set compression quality
- `--max-width <number>`: 限制最大宽度 / constrain width
- `--max-height <number>`: 限制最大高度 / constrain height
- `--suffix <text>`: 自定义输出后缀 / change output suffix
- `--overwrite`: 允许覆盖已存在文件 / allow overwriting existing output
- `--delete-original`: 成功后删除原图 / remove originals after successful output
- `--replace-original`: 成功后直接替换原图 / replace originals after successful output
- `--flatten`: 平铺目录输出 / flatten folder output
- `--no-recursive`: 关闭递归处理 / disable recursive folder traversal
- `--concurrency <number>`: 控制批量并发数 / control batch concurrency
- `--json`: 输出结构化摘要 / emit structured summary

## Upload / Pipeline 参数 / Upload and pipeline flags

- `upload <input>`: 直接上传已有文件或目录 / upload existing files or directories
- `pipeline <input>`: 先压缩，再上传 / compress first, then upload
- `--config <file>`: 上传配置文件 / upload config file
- `--url <url>`: 上传接口地址 / upload endpoint
- `--method <method>`: 请求方法 / HTTP method
- `--authorization <value>`: Authorization 值 / Authorization header value
- `--cookie <value>`: Cookie 请求头值 / Cookie header value
- `--content-type <value>`: 显式 Content-Type / explicit Content-Type
- `--header <key=value>`: 额外请求头 / extra headers
- `--form-field <spec>`: 表单字段映射 / form field mapping
- `--preview-only`: 仅预览压缩与上传请求 / preview compression and upload requests only

推荐把复杂接口定义放到 `upload.config.json` 中，而不是把长 JSON 直接写进提示词。  
Prefer placing complex API definitions in `upload.config.json` instead of embedding long JSON directly in prompts.

### 推荐配置文件结构 / Recommended config shape

```json
{
  "uploadConfig": {
    "url": "https://example.com/admin/upload",
    "method": "POST",
    "authorization": "Bearer your-token",
    "cookie": "sid=abc123; theme=dark",
    "contentType": "",
    "dataMode": "formFields",
    "formFields": [
      { "key": "file", "valueType": "file" },
      { "key": "fileName", "valueType": "fileName" },
      { "key": "savedPercentage", "valueType": "savedPercentage" }
    ]
  }
}
```

### 分片上传配置结构 / Chunk upload config shape

```json
{
  "uploadConfig": {
    "url": "https://example.com/admin/upload/chunk",
    "method": "POST",
    "fileFieldKey": "chunkFile",
    "formFields": [
      { "key": "chunkFile", "valueType": "file" },
      { "key": "sessionId", "valueType": "sessionId" },
      { "key": "chunkIndex", "valueType": "chunkIndex" },
      { "key": "totalChunks", "valueType": "totalChunks" }
    ],
    "chunkUpload": {
      "enabled": true,
      "chunkSize": 5242880,
      "concurrency": 2,
      "resume": true
    }
  }
}
```

说明：

- 当前只保留 `FormData` 请求方式
- `contentType` 在 `FormData` 模式下通常建议留空，让运行时自动生成 multipart boundary
- 若接口文档明确要求手动设置 `Content-Type`，再显式传入
- 若需要分片上传 / 断点续传，优先把 `chunkUpload` 放进配置文件，而不是把长 JSON 直接写进提示词

## 选择建议 / Decision guide

### 保留原图 / Keep original files

推荐默认使用：

```bash
rv-image-optimize "{input}" --output-dir "{outputDir}" --format webp --quality 82 --json
```

### 原地替换 / Replace files in place

只有在用户明确同意时才使用：

```bash
rv-image-optimize "{input}" --format webp --quality 82 --replace-original --json
```

### 输出新文件后删除原图 / Delete originals after writing new files

只有在用户明确同意时才使用：

```bash
rv-image-optimize "{input}" --output-dir "{outputDir}" --format webp --quality 82 --delete-original --json
```

### 已有文件直接上传 / Upload existing files

```bash
rv-image-optimize upload "{input}" --config "{configPath}" --json
```

### 大文件分片上传 / Chunked upload for large files

```bash
rv-image-optimize upload "{input}" --config "{chunkConfigPath}" --timeout-ms 10000 --json
```

### 压缩后直传接口 / Compress and upload in one step

```bash
rv-image-optimize pipeline "{input}" --format webp --quality 82 --config "{configPath}" --json
```

## Agent 汇总模板 / Agent summary template

向用户汇报时可使用以下结构：

```text
Processed: {total}
Succeeded: {success}
Failed: {failed}
Output: {outputDir or replaced originals}
Failed files:
- ...
```

如果是上传 / pipeline 任务，额外建议汇报：

```text
HTTP status: {status}
Preview fields: {entries.length}
Upload mode: FormData
```

## 相关文档 / Source docs

- 主说明 / Main package overview: `README.md`
- Agent 集成 / Agent guidance: `AGENT_INTEGRATION.md`
- CLI 细节 / CLI details: `NODE_CLI_COMPRESS.md`
- 上传链路 / Upload pipeline: `UPLOAD_PIPELINE.md`
