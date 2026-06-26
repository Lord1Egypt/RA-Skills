# API 参考

## 基础信息

- **Base URL**: `http://localhost:3000/api/v1`
- **认证**: 无
- **文件限制**: 最大 50MB

## 认证

无需认证，所有接口均可直接调用。

## 文件操作

### 上传文件
```
POST /api/v1/file/upload
Content-Type: multipart/form-data
Body: file (文件字段)

Response: {
  fileId: string,
  originalName: string,
  format: string,
  size: number,
  pages: number | null
}
```

### 获取文件信息
```
GET /api/v1/file/:fileId
Response: {
  id, originalName, format, size, pages, createdAt
}
```

### 删除文件
```
DELETE /api/v1/file/:fileId
Response: { success: true }
```

## 转换操作

### 创建转换任务
```
POST /api/v1/convert/
Content-Type: application/json

Body: {
  fileId: string,          // 必需，上传后的文件ID
  conversionType: string   // 必需，如 "pdf_to_word"
}

Response: {
  taskId: string,
  status: "PENDING",
  conversionType: string,
  createdAt: string (ISO),
  expiresAt: string (ISO)
}
```

### 查询任务状态
```
GET /api/v1/convert/:taskId

Response: {
  taskId: string,
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED",
  progress: number (0-100),
  errorMessage: string | null,
  input: {
    fileId: string,
    format: string,
    originalName: string
  } | null,
  output: {
    fileId: string,
    originalName: string,
    format: string,
    size: number,
    downloadUrl: string
  } | null,
  createdAt: string,
  completedAt: string | null,
  expiresAt: string
}
```

### 下载转换结果
```
GET /api/v1/convert/:taskId/download

Conditions: status 必须为 "COMPLETED"

Response: 文件二进制流
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="output.docx"
```

### 转换历史
```
GET /api/v1/convert/history

Response: {
  total: number,
  tasks: [{
    taskId: string,
    conversionType: string,
    status: string,
    createdAt: string,
    completedAt: string | null,
    input: { originalName: string, format: string } | null,
    output: { originalName: string, format: string, size: number } | null
  }]
}
```

## 转换类型 (conversionType)

| 值 | 源格式 | 目标格式 | 需要会员 |
|---|---|---|---|
| `pdf_to_word` | PDF | DOCX | 否 |
| `word_to_pdf` | DOCX | PDF | 否 |
| `pdf_to_images` | PDF | JPG | 否 |
| `images_to_pdf` | JPG/PNG | PDF | 否 |
| `word_to_image` | DOCX | JPG | 否 |
| `excel_to_pdf` | XLSX | PDF | 否 |
| `ppt_to_pdf` | PPTX | PDF | 否 |

## 错误处理

```json
{
  "error": "错误描述"
}
```

常见错误：
- `404`: 文件或任务不存在
- `400`: 不支持的转换类型
- `403`: 需要 Pro 会员
