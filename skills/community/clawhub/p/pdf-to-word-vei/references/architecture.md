# 系统架构

## 技术栈

**前端**
- React 18 + TypeScript
- Vite（构建工具）
- React Router（路由）
- Zustand（状态管理）
- react-dropzone（文件上传）
- Tailwind CSS

**后端**
- Node.js + TypeScript
- Fastify（Web 框架）
- Prisma（ORM）
- PostgreSQL（数据库）
- BullMQ + Redis（任务队列）
- JWT（认证）

**存储**
- Local 文件系统（默认）
- 可配置 S3/OSS 等

**转换引擎**
- `pdf2docx`：PDF → DOCX（唯一可靠方案）
- `LibreOffice`：Office 格式互转、Office → PDF
- `pdftoppm`：PDF → 图片
- `ImageMagick/gs`：图片 → PDF

## 目录结构

```
doc-converter/
├── backend/
│   ├── src/
│   │   ├── index.ts              # Fastify 入口
│   │   ├── config/env.ts         # 环境变量
│   │   ├── jobs/converter.ts     # 转换 Worker（核心）
│   │   ├── routes/
│   │   │   ├── auth.ts           # 认证路由
│   │   │   ├── convert.ts         # 转换路由
│   │   │   ├── file.ts           # 文件路由
│   │   │   └── format.ts         # 格式路由
│   │   ├── services/
│   │   │   └── storage.ts        # 存储服务
│   │   └── plugins/
│   └── prisma/schema.prisma      # 数据库 Schema
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # React 入口
│   │   ├── pages/
│   │   │   ├── HomePage.tsx      # 主页面
│   │   │   ├── HistoryPage.tsx   # 历史记录
│   │   │   ├── LoginPage.tsx     # 登录
│   │   │   └── RegisterPage.tsx  # 注册
│   │   ├── api/client.ts         # API 客户端
│   │   └── stores/convertStore.ts # 状态管理
│   └── vite.config.ts
└── docker-compose.yml
```

## 数据模型

### User
| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 唯一ID |
| email | string | 邮箱（唯一） |
| passwordHash | string | 密码哈希 |
| name | string | 显示名称 |
| tier | enum | FREE/PRO/PRO_PLUS/ENTERPRISE |
| createdAt | DateTime | 创建时间 |

### File
| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 唯一ID |
| userId | string? | 所属用户 |
| originalName | string | 原始文件名 |
| format | string | 格式（pdf/docx等） |
| size | number | 文件大小（字节） |
| pages | int? | 页数（PDF） |
| storagePath | string | 存储路径 |
| expiresAt | DateTime | 过期时间 |

### ConvertTask
| 字段 | 类型 | 说明 |
|---|---|---|
| taskId | string | 任务ID（唯一） |
| userId | string? | 所属用户 |
| inputFileId | string | 输入文件ID |
| outputFileId | string? | 输出文件ID |
| conversionType | string | 转换类型 |
| status | enum | PENDING/PROCESSING/COMPLETED/FAILED |
| progress | int | 进度 0-100 |
| errorMessage | string? | 错误信息 |

## 转换流程（PDF → Word）

```
1. 用户上传 PDF 文件
   → POST /api/v1/file/upload
   → File 记录创建，文件存储到 storage

2. 用户创建转换任务
   → POST /api/v1/convert/ { fileId, conversionType: "pdf_to_word" }
   → ConvertTask 记录创建，状态 PENDING
   → 任务加入 BullMQ 队列

3. Worker 处理任务（converter.ts）
   → 状态更新为 PROCESSING (progress: 10)
   → 下载输入文件到 /tmp/doc-converter-{taskId}/
   → 执行 pdf2docx 转换 (progress: 40 → 70)
   → 上传输出文件到 storage (progress: 85 → 95)
   → 更新任务状态为 COMPLETED (progress: 100)

4. 用户轮询任务状态
   → GET /api/v1/convert/{taskId}
   → 返回当前状态和进度

5. 用户下载结果
   → GET /api/v1/convert/{taskId}/download
   → 返回 .docx 文件流
```

## 前端状态管理（Zustand）

```typescript
interface UploadedFile {
  id: string
  name: string
  size: number
  format: string
  status: 'uploading' | 'done' | 'error'
  pages?: number
}

interface ConvertTask {
  taskId: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  inputFormat: string
  outputFormat: string
  fileName: string
  downloadUrl?: string
  errorMessage?: string
}
```

## 环境变量

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/doc_converter
JWT_SECRET=your-secret-key
CORS_ORIGIN=http://localhost:5173
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=/tmp/doc-converter-files
REDIS_URL=redis://localhost:6379
MAX_FILE_SIZE_MB=50
LIBREOFFICE_PATH=/usr/bin/soffice
CONVERSION_TIMEOUT_SEC=120
PORT=3000
```
