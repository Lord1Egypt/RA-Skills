# 金山开放平台 API 参考

> 本文档定义 KingDoc 与金山开放平台 API 的对接方式，包括鉴权、请求格式、错误处理和核心接口。

---

## 1. 鉴权概述

### 1.1 获取 AppID / AppSecret

1. 访问 [金山开放平台](https://developer.kdocs.cn)
2. 创建一个新应用
3. 获取 `App ID` 和 `App Secret`
4. 在本地配置：`config.json`

### 1.2 OAuth 2.0 Client Credentials

```
POST https://open.kdocs.cn/oauth/token

Body:
  grant_type    = client_credentials
  client_id     = <APP_ID>
  client_secret = <APP_SECRET>
  scope         = user:file:write user:file:read team:file:write team:file:read
```

**响应**：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 7200,
  "scope": "user:file:write user:file:read"
}
```

### 1.3 使用 Token

在请求 Header 中传递：

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 2. 基础 URL

| 环境 | 基础 URL |
|------|---------|
| 生产环境 | `https://developer.kdocs.cn/api/v1/openapi` |
| 沙箱环境 | `https://sandbox.kdocs.cn/api/v1/openapi` |

---

## 3. 统一响应格式

所有 API 返回：

```json
{
  "code": 0,
  "message": "OK",
  "data": { ... },
  "trace_id": "trace_abc123"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 0 = 成功，非 0 = 错误 |
| message | string | 状态信息 |
| data | object | 业务数据（仅成功时存在） |
| trace_id | string | 追踪 ID，排查问题用 |

---

## 4. 个人文档 API

### 4.1 创建文档

```
POST /personal/files

Body:
{
  "name": "文档标题",
  "type": "doc",
  "folder_id": "可选，父文件夹 ID",
  "content": "可选，初始内容"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 文档标题 |
| type | string | ✅ | 文档类型：doc / sheet / ppt / dbt / form |
| folder_id | string | ❌ | 父文件夹 ID（不填为根目录） |
| content | string | ❌ | 初始内容（Markdown） |

**成功响应**：

```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "file_id": "file_abc123",
    "name": "文档标题",
    "type": "doc",
    "url": "https://docs.wps.cn/doc/file_abc123",
    "created_at": 1719849600
  }
}
```

### 4.2 获取文档内容

```
GET /personal/files/:file_id/content
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "file_id": "file_abc123",
    "content": "文档正文...",
    "version": 3
  }
}
```

### 4.3 更新文档内容

```
PUT /personal/files/:file_id/content

Body:
{
  "content": "更新的内容",
  "version": 3
}
```

> ⚠️ `version` 必须与当前版本一致，否则返回版本冲突错误。

### 4.4 删除文档（软删除）

```
DELETE /personal/files/:file_id
```

> ⚠️ 删除后文档进入回收站，可恢复。

### 4.5 彻底删除

```
DELETE /personal/files/:file_id/permanent
```

---

## 5. 空间/文件夹 API

### 5.1 创建文件夹

```
POST /personal/folders

Body:
{
  "name": "文件夹名称",
  "parent_id": "可选，父文件夹 ID"
}
```

### 5.2 查询目录树

```
GET /personal/folders/children?folder_id=:id
```

### 5.3 查询面包屑路径

```
GET /personal/folders/breadcrumb?folder_id=:id
```

---

## 6. 回收站 API

### 6.1 查询回收站

```
GET /personal/trash/list?offset=0&limit=20
```

### 6.2 恢复文件

```
POST /personal/trash/recover

Body:
{
  "file_id": "file_abc123"
}
```

### 6.3 彻底删除

```
POST /personal/trash/destroy

Body:
{
  "file_id": "file_abc123"
}
```

---

## 7. 版本历史 API

### 7.1 查询版本

```
GET /appspace/versions?file_id=:file_id
```

### 7.2 回滚到某版本

```
POST /appspace/versions/:version_id/restore

Body:
{
  "file_id": "file_abc123"
}
```

---

## 8. 批量操作 API

### 8.1 创建批量任务

```
POST /personal/tasks

Body:
{
  "operation": "move",
  "file_ids": ["file_1", "file_2"],
  "target_folder_id": "folder_xxx"
}
```

### 8.2 查询任务结果

```
GET /personal/tasks/:task_id
```

---

## 9. 电子表格精细编辑 API

```
POST /et/cells/update        # 更新单元格内容
GET /et/cells/:sheet_id       # 读取单元格
GET /et/ranges/:sheet_id      # 读取区域
PUT /et/ranges/:sheet_id      # 写入区域（批量）
POST /et/formula/set          # 设置公式
POST /et/sheets               # 添加工作表
PUT /et/sheets/:sheet_id      # 重命名工作表
DELETE /et/sheets/:sheet_id   # 删除工作表
```

---

## 10. 多维表格（轻维表）API

```
POST /dbt/tables              # 创建多维表格
GET /dbt/tables/:table_id     # 获取表格结构
POST /dbt/fields              # 添加字段
PUT /dbt/fields/:field_id     # 修改字段
DELETE /dbt/fields/:field_id  # 删除字段
GET /dbt/views/:table_id      # 列出视图
POST /dbt/views               # 添加视图
POST /dbt/records             # 添加记录
PUT /dbt/records/:record_id   # 更新记录
DELETE /dbt/records/:record_id# 删除记录
GET /dbt/records/:table_id    # 查询记录
POST /dbt/webhooks            # 设置 Webhook
```

---

## 11. 收集表 API

```
POST /personal/forms           # 创建收集表
GET /personal/forms/:form_id   # 获取收集表
PUT /personal/forms/:form_id   # 修改收集表
DELETE /personal/forms/:form_id# 删除收集表
GET /personal/forms/:form_id/answers?offset=0&limit=50  # 查询答卷
POST /personal/forms/:form_id/submit   # 提交答卷
```

---

## 12. 格式转换 API

```
POST /office/convert

Body:
{
  "file_id": "file_abc123",
  "target_format": "pdf"
}
```

---

## 13. 文档纯文本提取 API

```
POST /office/extract

Body:
{
  "file_id": "file_abc123"
}

Response:
{
  "code": 0,
  "data": {
    "text": "文档中的全部文字...",
    "file_id": "file_abc123"
  }
}
```

---

## 14. 错误码

| HTTP 状态码 | 错误码 | 含义 |
|------------|--------|------|
| 401 | KD001 | Token 无效或过期 |
| 403 | KD002 | 权限不足 |
| 404 | KD005 | 文档不存在 |
| 409 | KD007 | 文档版本冲突 |
| 413 | KD008 | 文件过大 |
| 429 | KD006 | 请求限流 |
| 500 | KD010 | 服务器内部错误 |

---

## 15. 限流策略

| 应用类型 | 每日限额 |
|---------|---------|
| 测试应用（创建/修改/查询） | 500 次 |
| 测试应用（权限/文件/用户） | 500 次 |
| 测试应用（批量下载/上传/提取） | 500 次 |
| 测试应用（内容编撰类） | 10000 次 |
| 测试应用（批量任务） | 50-100 次 |
| 正式应用（创建/修改/查询） | 100,000 次 |
| 正式应用（批量下载/上传） | 100,000 次 |
| 正式应用（内容编撰） | 10,000,000 次 |

建议：尽早申请正式应用以获得充足限额。

---

*最后更新：2026-07-02*
