---
name: mineru
description: 用 MinerU Agent 轻量解析 API 将 PDF/Word/PPT/Excel/图片解析为 Markdown，无需 Token，IP 限频。适用于文档解析、表格提取、OCR 识别。
---

# 📄 MinerU - 文档解析

> PDF/Word/PPT/Excel/图片 → 结构化 Markdown

## 🎯 触发条件

当用户要求解析文档、提取文档内容、OCR 识别、将文件转为 Markdown 时使用。

## 🔗 API 信息

- **Base URL:** `https://mineru.net/api/v1/agent`
- **认证方式:** 无需 Token，IP 限频
- **文档:** https://mineru.net/apiManage/docs

## 📋 支持的文件类型

| 类型 | 格式 |
|------|------|
| 📕 PDF | 论文、书籍、扫描件 |
| 📝 Word | .docx |
| 📊 PPT | .pptx |
| 📊 Excel | .xls, .xlsx |
| 🖼️ 图片 | .png, .jpg, .jpeg, .jp2, .webp, .gif, .bmp |

## ⚠️ 限制

| 限制项 | 限制值 |
|--------|--------|
| 文件大小 | 10 MB |
| 文件页数 | 20 页 |

## 🚀 使用方式

### 方式一：URL 解析（文件有公开 URL 时）

直接调用解析脚本：

```bash
python3 SKILL_DIR/scripts/mineru_parse.py --url "https://example.com/file.pdf"
```

可选参数：
- `--language ch|en` （默认 ch）
- `--page_range 1-10`（仅 PDF 有效）
- `--output /path/to/output.md`（指定输出文件）

### 方式二：文件上传解析（本地文件）

```bash
python3 SKILL_DIR/scripts/mineru_parse.py --file /path/to/document.pdf
```

### 方式三：在对话中直接使用

用户发送文件或提供文件路径/URL 时，调用脚本解析，将结果返回给用户。

## 🔄 API 流程

### URL 模式
1. `POST /parse/url` → 获取 task_id
2. `GET /parse/{task_id}` → 轮询直到 done
3. 下载 markdown_url 返回结果

### 文件上传模式
1. `POST /parse/file` → 获取 task_id + file_url
2. `PUT file_url` → 上传文件到 OSS
3. `GET /parse/{task_id}` → 轮询直到 done
4. 下载 markdown_url 返回结果

## ❌ 错误码

| 错误码 | 说明 | 应对策略 |
|--------|------|----------|
| -30001 | 文件大小超出限制（10MB） | 拆分文件或告知用户 |
| -30002 | 不支持的文件类型 | 检查文件格式 |
| -30003 | 页数超出限制 | 指定 page_range 拆分 |
| -30004 | 请求参数错误 | 检查必填参数 |

## 💡 使用技巧

1. **中文文档用 `language: ch`**
2. **大文件指定 `page_range` 分段解析**
3. **Word/PPT 用 Office 原生 API 解析，速度最快**
4. **解析结果为 Markdown 格式，可直接用于后续处理**

---

*轻量快速，无需 Token！📄*
