---
name: wechat-article-publisher
description: 从 Markdown 或 HTML 文件发布图文到微信公众号。支持本地图片自动上传、封面尺寸自动处理（2.35:1）、内容图片 CDN 替换、重试机制与草稿创建。适用场景：文章发布、批量图文生产、内容运营工作流。
version: 2.1.0
metadata:
  homepage: https://github.com/victor-skills/wechat-article-publisher
  tags: [wechat, articles, publishing, mp, gzh]
  requirements:
    bins: ["python"]
    python_pkgs: ["markdown", "requests", "Pillow", "beautifulsoup4", "pyyaml"]
---

# WeChat Article Publisher v2

从 Markdown 或 HTML 文件发布图文到微信公众号，支持**本地图片自动上传**、**封面尺寸自动处理**、**内容图片 CDN 替换**、**网络重试机制**。

## 核心功能

1. **多格式输入**：Markdown 文件（带 frontmatter）或 HTML 文件
2. **本地图片处理**：相对路径图片自动上传替换为微信 CDN URL
3. **封面尺寸强制**：自动将封面 resize 为 **900×383**（2.35:1），不符合则报错 53401
4. **网络容错**：上传失败自动重试 3 次，30s 超时升级到 120s
5. **Token 缓存**：避免频繁刷新，缓存至 `.token_cache.json`
6. **干运行模式**：`--dry-run` 仅渲染预览，不调用微信 API

## 快速开始

```bash
# 安装依赖
python scripts/publish_wechat.py --install

# 干运行（只预览，不发布）
python scripts/publish_wechat.py article.md --dry-run

# 发布草稿
python scripts/publish_wechat.py article.html

# 指定封面图
python scripts/publish_wechat.py article.md --cover-image cover.png
```

## 输入格式

### Markdown（推荐）

```markdown
---
title: 文章标题
author: 作者名
---

正文内容，支持 Markdown 语法。

![图片描述](local/images/cover.png)
```

### HTML（已有渲染内容时）

直接传入 HTML 文件路径，脚本自动提取 `<body>` 内容，并处理其中的 `<img src="">`。

## 封面图规范（关键）

| 参数 | 要求 |
|------|------|
| 宽高比 | **2.35:1**（如 900×383、940×400） |
| 最小宽度 | 900px |
| 格式 | PNG/JPEG/JPG |
| 错误码 | 53401 = 尺寸不合规 |

**自动处理**：若传入的封面图比例不符，脚本会自动裁切至 900×383 存为 `cover_2_35_1.png`，再上传。

**手动处理**（PIL 示例）：

```python
from PIL import Image
img = Image.open("cover.png")
resized = img.resize((900, 383), Image.LANCZOS)
resized.save("cover_2_35_1.png", "PNG")
```

## 微信公众号 API 关键约束

| 接口 | 限制 |
|------|------|
| `access_token` | 有效期 7200s，不失效时重复使用缓存 |
| 临时素材上传 | `media/upload`，返回 `url`（CDN 地址） |
| 永久素材上传 | `material/add_material`，返回 `media_id` + `url` |
| 草稿创建 | 需 `thumb_media_id`（永久素材），否则 40007 |
| 封面图尺寸 | 2.35:1，不足则 53401 |
| 封面图大小 | 限制 2MB，超出会提示 |

## 常见错误排查

| 错误码 | 含义 | 解决方案 |
|--------|------|------|
| 40001 | access_token 无效 | 重新获取 token（强制刷新） |
| 40007 | thumb_media_id 无效 | 用永久素材接口上传封面，获取 media_id |
| 41005 | media data missing | 检查图片文件是否存在、路径是否正确 |
| 53401 | 封面图尺寸不合规 | resize 为 900×383 |
| 48001 | 没有发布权限 | 在微信后台手动发布，或确认账号类型 |

## 工作流设计（发布前必读）

```
[Markdown/HTML]
       ↓
[提取标题/作者/正文]
       ↓
[识别本地图片 src]
       ↓
[每张图：上传至微信 CDN] ← 重试 3 次，120s 超时
       ↓
[替换 src 为 CDN URL]
       ↓
[封面图：resize → 900×383 → 永久素材上传]
       ↓
[草稿创建 API → draft_media_id]
       ↓
[微信后台手动发布 或 API freepublish/submit]
```

## 脚本参数

| 参数 | 说明 |
|------|------|
| `input` | Markdown 或 HTML 文件路径 |
| `--config` | 配置文件路径，默认 `config.json` |
| `--cover-image` | 本地封面图路径（优先使用） |
| `--template` | 排版模板，`standard` 或 `viral` |
| `--author` | 覆盖作者名 |
| `--source-url` | 原文链接 |
| `--timeout` | HTTP 超时秒数（默认 30s，上传时自动升级 120s） |
| `--dry-run` | 仅渲染不调用 API |
| `--publish` | 草稿创建后立即提交发布 |
| `--status` | 查询发布状态 |
| `--install` | 安装 Python 依赖 |

## 配置（config.json）

```json
{
  "wechat": {
    "app_id": "你的AppID",
    "app_secret": "你的AppSecret",
    "author": "默认作者名"
  }
}
```

## 发布清单

发布前逐项确认：

- [ ] config.json 中 app_id / app_secret 正确
- [ ] IP 已加入微信白名单（后台 → 设置 → 基本配置 → IP白名单）
- [ ] 封面图比例 = 2.35:1，宽度 ≥ 900px
- [ ] 文章正文中的本地图片已准备好（相对路径可解析）
- [ ] `--dry-run` 渲染正常，无报错
- [ ] 草稿创建成功，获得 `media_id`

## 输出结果

成功时输出 JSON：

```json
{
  "success": true,
  "title": "文章标题",
  "draft_media_id": "W_q164cVIGUec8YcY5YyW...",
  "preview_html": "/path/to/preview.html"
}
```

失败时输出：

```json
{
  "success": false,
  "error": "错误描述",
  "type": "WeChatPublishError"
}
```

---

*🦞 v2.0.0 - 基于两篇图文发布实战经验优化（2026-05-30）*