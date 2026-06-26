---
name: pdf-to-word
description: |
  PDF 转 Word（docx）文档转换工具。当用户需要将 PDF 文件转换为 Word 文档（.docx）时使用此技能。
  
  触发词：PDF转Word、PDF to Word、pdf转docx、把PDF转成Word、文档转换
  
  支持的功能：
  (1) PDF → Word (.docx) 转换
  (2) 查询转换任务状态
  (3) 下载转换结果
  (4) 批量转换
  (5) 转换历史记录
---

# PDF to Word (pdf-to-word) Skill

PDF 转 Word 转换技能，基于 doc-converter 项目实现。

## 项目位置

```
/home/vei/.openclaw/workspace/doc-converter/
├── backend/          # Node.js 后端 (Fastify + Prisma)
├── frontend/         # React 前端 (Vite + TypeScript)
└── docker-compose.yml
```

## 核心转换流程

### 1. 上传 PDF 文件

**前端上传**（已实现于 HomePage.tsx）：
```
POST /api/v1/file/upload
Content-Type: multipart/form-data
Body: file (PDF文件，最大50MB)
Response: { fileId, originalName, format, size, pages }
```

**直接 API 调用**：
```bash
curl -X POST http://localhost:3000/api/v1/file/upload \
  -F "file=@your.pdf"
```

### 2. 创建 PDF→Word 转换任务

```
POST /api/v1/convert/
Content-Type: application/json
Body: { fileId: "<fileId>", conversionType: "pdf_to_word" }
Response: { taskId, status, conversionType, createdAt, expiresAt }
```

### 3. 轮询任务状态

```
GET /api/v1/convert/:taskId
Response: {
  taskId, status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED",
  progress: 0-100,
  output: { fileId, originalName, format, size, downloadUrl } | null,
  errorMessage: string | null
}
```

**状态说明**：
- `PENDING` - 排队中
- `PROCESSING` - 转换中（有 progress 进度）
- `COMPLETED` - 完成，可下载
- `FAILED` - 失败，查看 errorMessage

### 4. 下载转换结果

```
GET /api/v1/convert/:taskId/download
Response: 文件流 (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
```

### 5. 转换历史

```
GET /api/v1/convert/history
Response: { total, tasks: [{ taskId, conversionType, status, createdAt, input, output }] }
```

## 后端转换实现

**核心文件**：`backend/src/jobs/converter.ts`

PDF → Word 使用 `pdf2docx` Python库：
```python
from pdf2docx import Converter
c = Converter('input.pdf')
c.convert('output.docx')
c.close()
```

其他转换类型使用 LibreOffice：
- Word/Excel/PPT → PDF：`soffice --headless --convert-to pdf`
- PDF → 图片：`pdftoppm -jpeg -r 200`
- 图片 → PDF：`convert` 或 `gs`

## 前端组件

- **HomePage.tsx** - 主转换界面（拖拽上传、转换选项、结果展示）
- **HistoryPage.tsx** - 转换历史
- **convertStore** - Zustand 状态管理

## 支持的转换类型

| conversionType | 说明 | 引擎 |
|---|---|---|
| `pdf_to_word` | PDF → Word | pdf2docx |
| `word_to_pdf` | Word → PDF | LibreOffice |
| `pdf_to_images` | PDF → 图片 | pdftoppm |
| `images_to_pdf` | 图片 → PDF | ImageMagick/gs |
| `word_to_image` | Word → 图片 | LibreOffice + pdftoppm |
| `excel_to_pdf` | Excel → PDF | LibreOffice |
| `ppt_to_pdf` | PPT → PDF | LibreOffice |

## 快速使用流程

1. **上传 PDF**：拖拽或点击选择 PDF 文件
2. **选择转换格式**：自动显示 PDF→Word 选项
3. **开始转换**：点击转换按钮
4. **等待完成**：轮询任务状态（每1.5秒）
5. **下载结果**：点击下载按钮获取 .docx 文件

## 关键代码参考

- 转换路由：`backend/src/routes/convert.ts`
- 转换Worker：`backend/src/jobs/converter.ts`
- 前端API：`frontend/src/api/client.ts`
- 状态管理：`frontend/src/stores/convertStore.ts`

详细 API 和架构说明见 references/
