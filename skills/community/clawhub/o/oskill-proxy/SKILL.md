---
name: oskill-proxy
description: Android组件调用代理。通过本地HTTP API在Android设备上启动Activity、启动Service、发送Broadcast、操作ContentProvider。当你无法直接执行Android Intent或组件调用时（例如在Termux环境中），使用此工具完成调用。
version: "1.0"
author: Raynor
category: SYSTEM_PROXY
config:
  token: "43b618ce5f3a46c78fbde7e6eb6bcac3"
  baseUrl: "http://127.0.0.1:8726"
---

# OSkillProxy — Android 组件调用代理

## 概述

OSkillProxy 是运行在 Android 设备上的代理服务。它提供本地 HTTP API，允许你以正确的 App 身份调用 Android 四大组件（Activity、Service、BroadcastReceiver、ContentProvider）。

**使用前提**：
- OSkillProxy App 已安装并且代理服务已启动
- Token 已配置（在 App 界面上查看）
- 通过 `http://127.0.0.1:8726` 访问（端口可能已修改，以实际配置为准）

## 工具列表

### start_activity
启动一个 Android Activity。
- 支持显式 Intent（指定 package + class）和隐式 Intent（指定 action）
- 这是一个 fire-and-forget 操作，不返回 Activity 结果

### start_service
启动一个 Android Service。
- 支持普通启动和前台服务启动

### send_broadcast
发送一个 Android Broadcast。
- 支持普通广播和带权限限制的广播

### query_provider
查询 ContentProvider 数据，返回结构化结果（列名 + 行数据）。

### insert_provider
向 ContentProvider 插入数据，返回新记录的 URI。

### update_provider
更新 ContentProvider 数据，返回受影响的行数。

### delete_provider
删除 ContentProvider 数据，返回受影响的行数。

### call_provider
调用 ContentProvider 的 call() 方法，返回 Bundle 结果。

## 调用方式

所有调用通过 HTTP POST 请求发起，使用 JSON 格式。

### 通用 HTTP 格式

```bash
curl -X POST http://127.0.0.1:8726/api/v1/component/<endpoint> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '<json_body>'
```

### 认证
每个请求（除 GET /api/v1/status 外）必须携带 Authorization header：
```
Authorization: Bearer <你的token>
```

### 通用响应格式
```json
{
  "success": true,
  "code": 0,
  "message": "ok",
  "data": {},
  "requestId": "abc12345"
}
```

## 各端点详细说明

### POST /component/activity/start

启动一个 Activity。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| package | string | 否 | 目标包名 |
| class | string | 否 | 目标 Activity 完整类名（需同时指定 package） |
| action | string | 否 | Intent Action |
| categories | string[] | 否 | Intent Categories |
| data | string | 否 | Intent Data URI |
| type | string | 否 | MIME Type |
| extras | object | 否 | Intent Extras，见 extras 格式 |
| flags | string[] | 否 | Intent Flags 名称列表 |

> `package`+`class`（显式）或 `action`（隐式）至少提供一种。

**支持的 Flags**:
- FLAG_ACTIVITY_NEW_TASK（自动添加）
- FLAG_ACTIVITY_CLEAR_TOP
- FLAG_ACTIVITY_SINGLE_TOP
- FLAG_ACTIVITY_CLEAR_TASK
- FLAG_ACTIVITY_NO_HISTORY
- FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS
- FLAG_ACTIVITY_NEW_DOCUMENT
- FLAG_ACTIVITY_MULTIPLE_TASK
- FLAG_INCLUDE_STOPPED_PACKAGES

---

### POST /component/service/start

启动一个 Service。

**请求参数**: 同 Activity，额外字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| foreground | boolean | 否 | 是否以前台方式启动（Android 8.0+） |

---

### POST /component/broadcast/send

发送一个 Broadcast。

**请求参数**: 同 Activity，额外字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| permission | string | 否 | 接收方需要持有的权限 |

---

### POST /component/provider/query

查询 ContentProvider。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uri | string | 是 | Content URI |
| projection | string[] | 否 | 要查询的列 |
| selection | string | 否 | WHERE 条件（使用 ? 占位符） |
| selectionArgs | string[] | 否 | WHERE 参数值 |
| sortOrder | string | 否 | 排序规则 |

**响应 data**:
```json
{
  "columns": ["_id", "title"],
  "rows": [[1, "Note 1"], [2, "Note 2"]],
  "count": 2
}
```

---

### POST /component/provider/insert

向 ContentProvider 插入数据。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uri | string | 是 | Content URI |
| values | object | 是 | 要插入的键值对，格式同 extras |

**响应 data**:
```json
{
  "uri": "content://com.example.provider/notes/3"
}
```

---

### POST /component/provider/update

更新 ContentProvider 数据。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uri | string | 是 | Content URI |
| values | object | 是 | 要更新的键值对 |
| selection | string | 否 | WHERE 条件 |
| selectionArgs | string[] | 否 | WHERE 参数值 |

**响应 data**:
```json
{
  "affectedRows": 1
}
```

---

### POST /component/provider/delete

删除 ContentProvider 数据。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uri | string | 是 | Content URI |
| selection | string | 否 | WHERE 条件 |
| selectionArgs | string[] | 否 | WHERE 参数值 |

**响应 data**:
```json
{
  "affectedRows": 1
}
```

---

### POST /component/provider/call

调用 ContentProvider 的 call() 方法。

**请求参数**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uri | string | 是 | Content URI |
| method | string | 是 | 方法名 |
| arg | string | 否 | 字符串参数 |
| extras | object | 否 | Bundle 参数（简单 key-value，自动推断类型） |

**响应 data**: ContentProvider 返回的 Bundle 内容，序列化为 JSON 对象。

---

## extras 类型说明

extras 字段支持两种格式：

**格式 1：显式类型（推荐）**
```json
{
  "key": {"type": "string", "value": "hello"},
  "count": {"type": "int", "value": 42},
  "flag": {"type": "boolean", "value": true}
}
```

支持的类型：`string`, `int`, `long`, `float`, `double`, `boolean`, `string_array`, `int_array`, `long_array`

**格式 2：自动推断**
```json
{
  "key": "hello",
  "count": 42,
  "flag": true
}
```
自动根据 JSON 值类型推断。

---

## 使用示例

### 示例 1：启动一个 Activity（显式 Intent）

场景：启动录音应用的透明 Activity 进行录音控制

```bash
curl -X POST http://127.0.0.1:8726/api/v1/component/activity/start \
  -H "Authorization: Bearer a3f8xxxxxxxxxxc9d2" \
  -H "Content-Type: application/json" \
  -d '{
    "package": "com.coloros.soundrecorder",
    "class": "oplus.multimedia.soundrecorder.slidebar.TransparentActivity",
    "action": "oplus.intent.action.START_RECORD_FROM_CUBE_BUTTON",
    "categories": ["android.intent.category.DEFAULT"]
  }'
```

### 示例 2：启动一个 Activity（隐式 Intent，带 extras）

```bash
curl -X POST http://127.0.0.1:8726/api/v1/component/activity/start \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "android.intent.action.SEND",
    "type": "text/plain",
    "extras": {
      "android.intent.extra.TEXT": {"type": "string", "value": "Hello from agent!"}
    }
  }'
```

### 示例 3：查询 ContentProvider

```bash
curl -X POST http://127.0.0.1:8726/api/v1/component/provider/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "uri": "content://com.example.provider/notes",
    "projection": ["_id", "title", "content"],
    "selection": "title LIKE ?",
    "selectionArgs": ["%meeting%"],
    "sortOrder": "created_at DESC"
  }'
```

### 示例 4：发送 Broadcast

```bash
curl -X POST http://127.0.0.1:8726/api/v1/component/broadcast/send \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "com.example.app.ACTION_REFRESH",
    "package": "com.example.app",
    "extras": {
      "force": {"type": "boolean", "value": true}
    }
  }'
```

### 示例 5：检查服务状态（无需 Token）

```bash
curl http://127.0.0.1:8726/api/v1/status
```

---

## 错误码

| 错误码 | 含义 |
|--------|------|
| 0 | 成功 |
| 400 | 请求格式错误 |
| 401 | 认证失败 |
| 404 | 端点不存在 |
| 1001 | Activity 启动失败 |
| 1002 | Service 启动失败 |
| 1003 | Broadcast 发送失败 |
| 1004 | Provider query 失败 |
| 1005 | Provider insert 失败 |
| 1006 | Provider update 失败 |
| 1007 | Provider delete 失败 |
| 1008 | Provider call 失败 |

---

## 状态检查

### GET /api/v1/status

无需认证，用于检查代理服务是否运行。

**响应**:
```json
{
  "success": true,
  "code": 0,
  "data": {
    "running": true,
    "version": "1.0.0",
    "handlers": ["component"],
    "endpoints": [
      "/api/v1/component/activity/start",
      "/api/v1/component/service/start",
      "/api/v1/component/broadcast/send",
      "/api/v1/component/provider/query",
      "/api/v1/component/provider/insert",
      "/api/v1/component/provider/update",
      "/api/v1/component/provider/delete",
      "/api/v1/component/provider/call"
    ]
  }
}
```
