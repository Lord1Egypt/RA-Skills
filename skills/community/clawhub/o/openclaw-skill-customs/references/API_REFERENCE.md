# Leap Customs API Reference

## Base URL

```
https://platform.daofeiai.com
```

## Authentication

All requests require the `Authorization` header:

```
Authorization: Bearer $LEAP_API_KEY
```

---

## Endpoints

### 1. File Upload

**POST** `/api/v1/files/upload`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | binary (multipart) | ✅ | 支持 PDF, Excel (.xlsx/.xls), 图片 (.jpg/.png/.tiff) |

**Response:**
```json
{
  "file_id": "string (UUID)",
  "original_name": "string",
  "file_size": "integer (bytes)",
  "mime_type": "string",
  "content_hash": "string",
  "is_duplicate": "boolean",
  "created_at": "string (ISO 8601)",
  "download_url": "string"
}
```

---

### 2. Submit Process Task

**POST** `/api/v1/process`

#### 2a. Fast Classification

| Parameter | Type | Required | Description |
|---|---|---|---|
| `output` | string | ✅ | 固定值 `"classify_fast"` |
| `params.files` | array | ✅ | 文件列表 |
| `params.files[].file_id` | string | ✅ | 文件ID |
| `force_reprocess` | boolean | ❌ | 是否强制重新处理（忽略缓存），默认 `false` |

**Request Example:**
```json
{
  "params": {
    "files": [
      { "file_id": "<id_1>" },
      { "file_id": "<id_2>" }
    ]
  },
  "output": "classify_fast",
  "force_reprocess": true
}
```

#### 2b. Customs Declaration

| Parameter | Type | Required | Description |
|---|---|---|---|
| `output` | string | ✅ | 固定值 `"customs"` |
| `params.files` | array | ✅ | 文件列表，包含 file_id 和 segments |
| `params.files[].file_id` | string | ✅ | 文件ID |
| `params.files[].file_name` | string | ❌ | 原始文件名 |
| `params.files[].segments` | array | ✅ | 分类结果中的 segments |
| `params.files[].metadata` | object | ❌ | 文件元信息（total_segments, file_format 等） |
| `force_reprocess` | boolean | ❌ | 是否强制重新处理（忽略缓存），默认 `false` |

**Request Example:**
```json
{
  "params": {
    "files": [
      {
        "file_id": "<id>",
        "file_name": "invoice.pdf",
        "segments": [
          {
            "type": "page",
            "file_type": "invoice",
            "confidence": 0.95,
            "pages": [1, 2, 3]
          }
        ],
        "metadata": {
          "total_segments": 1,
          "file_format": "pdf"
        }
      }
    ]
  },
  "output": "customs",
  "force_reprocess": true
}
```

#### 2c. Shared Response (classify_fast / customs)

**Response:**
```json
{
  "result_id": "string (UUID)",
  "file_id": "string",
  "file_ids": "string[] | null",
  "document_type": "string (e.g. \"universal\")",
  "status": "pending | processing | completed | failed",
  "message": "string",
  "cache_hit": "boolean",
  "task_id": "string (UUID)",
  "processing_time": "integer (ms) | null",
  "download_url": "string | null",
  "created_at": "string (ISO 8601)"
}
```

---

### 3. Query Task Status

**GET** `/api/v1/process/tasks/{result_id}`

**Response (completed):**
```json
{
  "result_id": "string",
  "status": "completed",
  "progress": 100,
  "processing_time": "integer (ms)",
  "result_data": { ... }
}
```

---

### 4. List Tasks

**GET** `/api/v1/process/tasks`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `status` | string | ❌ | 过滤状态: pending/processing/completed/failed |
| `limit` | integer | ❌ | 返回数量 (默认 20) |
| `offset` | integer | ❌ | 偏移量 (默认 0) |

---

### 5. Download Result File

**GET** `/api/v1/results/{result_id}/files/{filename}`

Returns the binary file content (e.g., Excel).

---

### 6. Cancel Task

**DELETE** `/api/v1/process/tasks/{result_id}`

Only works for `pending` or `processing` tasks.

---

### 7. Retry Failed Task

**POST** `/api/v1/process/tasks/{result_id}/retry`

Only works for `failed` tasks.

---

## File Type Enum & Segment Type Enum

→ 完整的文件类型枚举、分片类型枚举、合并漏斗规则和置信度解读，请参见 [FILE_TYPES.md](FILE_TYPES.md)。
