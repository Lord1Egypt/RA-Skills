---
name: md-img-r2
description: Upload local images in Markdown directly to Cloudflare R2 and replace paths with public URLs.
---

# md-img-r2

将 Markdown 文件中的本地图片直接上传到 Cloudflare R2，并把本地路径替换为公开 URL。

## 适用场景
- 你已经有 Cloudflare R2 桶和可公开访问域名
- 你不想依赖 PicList Desktop
- 你希望把这个能力作为可分发 skill 交给别人使用

## 前置条件
1. 已有可写入的 Cloudflare R2 凭证
2. 已有桶名和公开访问域名或 CDN 域名
3. 运行环境有 `python3`

## 推荐配置
优先用环境变量或项目根目录的 `.env` 提供配置：

- `CF_R2_ACCOUNT_ID`
- `CF_R2_ACCESS_KEY_ID`
- `CF_R2_SECRET_ACCESS_KEY`
- `CF_R2_BUCKET`
- `CF_R2_PUBLIC_BASE_URL`
- `CF_R2_REGION`，默认 `auto`
- `CF_R2_ENDPOINT`，默认 `https://<account_id>.r2.cloudflarestorage.com`
- `CF_R2_KEY_PREFIX`，默认 `md-assets`
- `--env-file` 可显式指定 `.env` 路径；不传时会优先读取 skill 目录下的 `.env`，再从目标目录向上查找

## 用法
### 单文件
bash run.sh path/to/article.md

### 目录批处理
bash run.sh path/to/dir --recursive

### Dry run
bash run.sh path/to/article.md --dry-run

### 临时覆盖 key 前缀
bash run.sh path/to/article.md --key-prefix posts/2026-04

## 输出
- 默认原地修改，并生成备份：`xxx.md.bak`
- 生成报告：`xxx.md.replace-report.json`
