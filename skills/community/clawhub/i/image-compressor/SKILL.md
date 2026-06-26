---
name: image-compressor
description: 基于 `rv-image-optimize` 的图片压缩、上传与一体化压缩后上传 skill，支持 JPEG/PNG/WebP/AVIF、批量目录处理、FormData 接口配置与 JSON 结果汇总。Use when the user asks to compress images, upload optimized files, convert to WebP or AVIF, batch-process image folders, resize images, or run image optimization/upload from an agent workflow.
version: 3.0.30
metadata:
  openclaw:
    emoji: "\U0001F5BC\uFE0F"
    homepage: https://github.com/ziji1224054593/Rv-image-optimize
    requires:
      anyBins:
        - rv-image-optimize
        - npx
    install:
      - kind: node
        package: rv-image-optimize
        bins:
          - rv-image-optimize
---

# Image Compressor

基于 `rv-image-optimize` 的图片压缩、上传与格式转换 skill。  
An image compression, upload, and format-conversion skill powered by `rv-image-optimize`.

## 核心功能 / Features

- 压缩单张或批量图片 / Compress single images or whole folders
- 转换 `jpeg`、`png`、`webp`、`avif` / Convert between `jpeg`, `png`, `webp`, and `avif`
- 压缩时限制尺寸 / Resize while compressing with max width and height
- 通过 `upload` 子命令按 `FormData` 配置上传文件 / Upload files through the `upload` subcommand with `FormData` config
- 通过 `pipeline` 子命令一条命令完成“压缩 + 上传” / Complete "compress + upload" in one command with the `pipeline` subcommand
- 通过 `chunkUpload` 配置执行分片上传 / 断点续传 / Run chunked and resumable uploads through `chunkUpload` config
- 输出结构化 JSON 结果 / Return structured JSON summaries for agents
- 默认安全输出到新目录 / Default to safe output in a new directory

## 何时使用 / When to use

当用户提到以下需求时使用：

- “压缩图片”
- “图片太大”
- “减小文件大小”
- “转成 WebP / AVIF”
- “批量处理整个图片目录”
- “压缩时顺便缩小尺寸”
- “让 Agent / CLI 自动处理图片”
- “压缩后上传到接口”
- “按接口配置上传文件”
- “大文件分片上传”
- “断点续传”

Use this skill when the user asks to:

- compress one or more images
- reduce image file size
- convert images to `webp` or `avif`
- batch-process an image folder
- resize images while compressing
- run image optimization from an agent or CLI workflow
- upload files to an API through CLI
- compress files and immediately upload them
- perform chunked uploads for large files
- resume interrupted uploads

## 默认策略 / Default behavior

除非用户明确要求修改原图，否则优先使用安全模式：

- 使用 `--output-dir` 输出到新目录
- 使用 `--json` 方便 Agent 汇总结果
- 默认不删除原图
- 默认不替换原图
- 大文件上传优先把 `chunkUpload` 写进 `--config`

Preferred command:

```bash
rv-image-optimize "{input}" --output-dir "{outputDir}" --format webp --quality 82 --json
```

如果全局命令不可用，可回退到：

```bash
npx rv-image-optimize "{input}" --output-dir "{outputDir}" --format webp --quality 82 --json
```

如果任务是“压缩后上传接口”，优先使用：

```bash
rv-image-optimize pipeline "{input}" --format webp --quality 82 --config "{configPath}" --json
```

如果任务是“已有文件直接上传接口”，优先使用：

```bash
rv-image-optimize upload "{input}" --config "{configPath}" --json
```

## 安全规则 / Safety rules

以下选项只有在用户明确要求时才允许使用：

- `--delete-original`
- `--replace-original`

`--replace-original` 不能和以下参数一起使用：

- `--output`
- `--output-dir`
- `--suffix`

If the user wants to preserve source files, always choose `--output-dir`.

上传相关安全约定：

- 当前只保留 `FormData` 请求方式
- 复杂上传字段优先写进 `--config` JSON 文件
- 大文件 / 可恢复上传优先使用 `chunkUpload` 配置块
- `Authorization`、`Cookie`、`Content-Type` 优先用配置文件显式字段表达
- `Content-Type` 在 `FormData` 模式下通常建议留空，让运行时自动生成 boundary

## 常用命令 / Common recipes

### 单张图片压缩 / Compress a single image

```bash
rv-image-optimize "./photo.jpg" --output-dir "./compressed" --format webp --quality 82 --json
```

### 批量压缩目录 / Compress a folder

```bash
rv-image-optimize "./images" --output-dir "./images-compressed" --format webp --quality 82 --json
```

### 调整尺寸并压缩 / Resize and compress

```bash
rv-image-optimize "./images" --output-dir "./images-compressed" --format webp --quality 82 --max-width 1920 --max-height 1080 --json
```

### 压缩成功后删除原图 / Delete originals after success

```bash
rv-image-optimize "./images" --output-dir "./images-compressed" --format webp --quality 82 --delete-original --json
```

### 直接替换原图 / Replace originals in place

```bash
rv-image-optimize "./images" --format webp --quality 82 --replace-original --json
```

### 直接上传已有文件 / Upload existing files

```bash
rv-image-optimize upload "./dist/demo.webp" --config "./upload.config.json" --json
```

### 分片上传 / 断点续传 / Chunked resumable upload

```bash
rv-image-optimize upload "./large-assets" --config "./upload.chunk.config.json" --timeout-ms 10000 --json
```

### 压缩后直接上传 / Compress then upload

```bash
rv-image-optimize pipeline "./images" --format webp --quality 82 --config "./upload.config.json" --json
```

### 仅预览上传字段 / Preview upload fields only

```bash
rv-image-optimize upload "./dist/demo.webp" --config "./upload.config.json" --preview-only --json
```

## 汇报结果 / Reporting results

使用 `--json` 时，建议汇总：

- `total`
- `success`
- `failed`
- 输出目录或是否替换了原图
- 失败文件列表
- 上传模式下的 HTTP 状态码或预览字段

## 推荐参数 / Recommended defaults

- 默认格式：`webp`
- 默认质量：`82`
- 更小体积优先且接受更慢编码时：`avif`
- 上传任务默认优先使用 `--config`
- 大文件上传默认优先使用 `chunkUpload`
- 压缩后上传默认优先使用 `pipeline`
- 如需更多示例和参数说明，见 [reference.md](reference.md)
