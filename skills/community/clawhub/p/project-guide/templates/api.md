# API 接口设计

## 1. 接口概览

### 1.1 基础信息
| 项目 | 值 |
|------|-----|
| Base URL | /api/v1 |
| 认证方式 | Bearer Token |
| 协议 | HTTPS |
| 数据格式 | JSON |

### 1.2 通用响应格式

#### 成功响应
```json
{
  "code": 0,
  "data": { ... },
  "message": "success"
}
```

#### 错误响应
```json
{
  "code": 1001,
  "data": null,
  "message": "错误描述"
}
```

### 1.3 错误码表
| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 认证失败 |
| 1003 | 权限不足 |
| 1004 | 资源不存在 |
| 1005 | 服务器内部错误 |

---

## 2. 用户模块

### 2.1 用户登录
**POST** `/auth/login`

**请求参数：**
```json
{
  "username": "string",
  "password": "string"
}
```

**响应：**
```json
{
  "code": 0,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "uuid",
      "username": "string",
      "email": "string"
    }
  },
  "message": "success"
}
```

---

### 2.2 用户注册
**POST** `/auth/register`

**请求参数：**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**响应：**
```json
{
  "code": 0,
  "data": {
    "id": "uuid",
    "username": "string",
    "email": "string"
  },
  "message": "success"
}
```

---

### 2.3 获取当前用户信息
**GET** `/users/me`

**请求头：**
```
Authorization: Bearer <token>
```

**响应：**
```json
{
  "code": 0,
  "data": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "createdAt": "2024-01-01T00:00:00Z"
  },
  "message": "success"
}
```

---

## 3. 业务模块

### 3.1 [业务接口名称]
**[METHOD]** `/resource/{id}`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 资源ID |

**请求体：**
```json
{
  "field1": "string",
  "field2": 0
}
```

**响应：**
```json
{
  "code": 0,
  "data": {
    "id": "uuid",
    "field1": "string",
    "field2": 0,
    "createdAt": "2024-01-01T00:00:00Z"
  },
  "message": "success"
}
```

---

## 4. 接口清单

### 4.1 接口列表
| 模块 | 方法 | 路径 | 说明 | 优先级 |
|------|------|------|------|--------|
| 认证 | POST | /auth/login | 用户登录 | P0 |
| 认证 | POST | /auth/register | 用户注册 | P0 |
| 认证 | POST | /auth/logout | 用户登出 | P1 |
| 用户 | GET | /users/me | 获取当前用户 | P0 |
| 用户 | PUT | /users/me | 更新用户信息 | P1 |
| 业务 | GET | /resources | 资源列表 | P0 |
| 业务 | POST | /resources | 创建资源 | P0 |
| 业务 | GET | /resources/{id} | 获取资源详情 | P0 |
| 业务 | PUT | /resources/{id} | 更新资源 | P0 |
| 业务 | DELETE | /resources/{id} | 删除资源 | P1 |

---

## 5. WebSocket 接口

### 5.1 连接信息
| 项目 | 值 |
|------|-----|
| URL | wss://domain/ws |
| 协议 | ws |

### 5.2 消息格式
```json
{
  "type": "event_type",
  "data": { ... }
}
```

---

*请根据实际业务需求补充完整的 API 设计*
