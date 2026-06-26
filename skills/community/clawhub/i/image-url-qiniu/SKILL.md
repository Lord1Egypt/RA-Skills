---
name: image-url-qiniu
description: Download an image from a user-supplied HTTP(S) URL and upload it to Qiniu cloud. Use when the user gives an image link and wants it stored on Qiniu (backup, CDN, stable link, or Feishu-friendly delivery).
homepage: https://www.qiniu.com/
metadata: {"openclaw":{"emoji":"📦","requires":{"bins":["uv"]}}}
---

# Image URL → Qiniu

将**公网可访问**的图片 URL 拉取到本地内存并上传到七牛对象存储，标准输出末尾会打印 **`MEDIA_URL:`** 行（七牛公网地址），与览客/飞书交付约定一致。

## 前置条件（运维）

在运行环境的进程环境中配置（**勿**写入对话或用户资料）：

| 变量 | 说明 |
|------|------|
| `QINIU_ACCESS_KEY` | 七牛 AccessKey |
| `QINIU_SECRET_KEY` | 七牛 SecretKey |
| `QINIU_BUCKET` | 存储空间名 |
| `QINIU_PUBLIC_BASE_URL` | HTTPS 访问基址，如 `https://cdn.example.com`，**不要**末尾 `/` |
| `QINIU_KEY_PREFIX` | 可选，对象名前缀，默认 `openclaw/url-import` |

目标 Bucket 需**公开读**（或你方自行改用私有空间 + 下载凭证，本脚本仅输出直链）。

## 用法

```bash
uv run {baseDir}/scripts/url_image_to_qiniu.py --url "https://example.com/path/to/image.png"
```

可选参数：

- `--max-mb N`：单图最大体积（默认 `25`），超限则失败，防止误抓大文件。
- `--no-verify-ssl`：下载时关闭 SSL 校验（仅在内网/代理异常时慎用）。
- `--timeout SEC`：下载超时秒数（默认 `60`）。

## Agent 工作流

1. 从用户消息中取得**完整图片地址**（`http://` 或 `https://`）。
2. 在技能目录下执行：  
   `uv run {baseDir}/scripts/url_image_to_qiniu.py --url "<URL>"`
3. 在输出中查找 **`MEDIA_URL:`** 行，将其后 URL 交给用户；若渠道为飞书，须**另起一行输出完整 URL 纯文本**（与览客规则一致）。
4. 若失败：根据脚本 stderr 提示检查 URL 是否可直连、是否为图片、七牛配置与 Bucket 域名。

## 合规与安全

- 仅处理用户明确提供且有权使用的链接；不要对未授权版权素材主动批量镜像。
- 脚本会校验响应 `Content-Type` 为 `image/*` 或部分源站使用的 `application/octet-stream`；后者会按文件头魔数识别 PNG/JPEG/GIF/WebP/BMP。

## 输出约定

- 成功：打印一行 `MEDIA_URL: https://...`（七牛上的新地址）。
- 失败：非零退出码，错误信息在 stderr。
