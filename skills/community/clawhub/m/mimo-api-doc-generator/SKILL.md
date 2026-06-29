---
name: api-doc-generator
version: 1.5.0
description: |
  后端写完接口最烦的就是写文档。丢代码或接口定义进来，自动生成OpenAPI 3.0/Swagger标准文档，附带SDK示例代码和Mock配置。再也不是「接口文档在老王的脑子里」这种状态了。
  触发词：API文档、接口文档、生成API文档、Swagger文档、OpenAPI文档、REST API文档、GraphQL文档、WebSocket文档、接口规范、API规范、生成接口文档、接口说明、endpoints文档、API reference、SDK文档
  排除：产品需求文档(用prd-generator)、技术架构文档(用technical-solution)、用户使用手册、数据库设计文档(用database-schema-designer)
  上下文条件：用户提供代码/URL/OpenAPI文件/接口描述
---

# API文档生成器 📋 v1.4.0

## 核心流程（8 Steps）

### Step 1: API信息解析 🔍 输入识别

**支持的输入格式**：
| 格式 | 识别方式 | 优先级 |
|------|----------|--------|
| OpenAPI YAML/JSON | 文件后缀/.yaml/.json | ★★★★★ |
| 代码 | 框架特征关键词 | ★★★★☆ |
| URL链接 | HTTP/HTTPS前缀 | ★★★☆☆ |
| 手动描述 | 自然语言接口说明 | ★★☆☆☆ |

**代码框架识别**：
```
Python:
- Flask: @app.route, @app.endpoint
- FastAPI: @app.get, @router
- Django: path(), urlpatterns
- Tornado: @route, RequestHandler

JavaScript:
- Express: app.get/post/put/delete
- Koa: router.get/post
- NestJS: @Controller, @Get

Go:
- Gin: router.GET/POST
- Echo: e.GET/e.POST
- Fiber: app.Get/app.Post

Java:
- Spring: @RequestMapping, @GetMapping
- Spring Boot: @RestController
```

**解析检查清单**：
- [ ] 路由定义完整（URL路径）
- [ ] HTTP方法正确（GET/POST/PUT/DELETE/PATCH）
- [ ] 参数定义（路径/查询/请求体）
- [ ] 响应格式定义
- [ ] 认证方式识别

---

### Step 2: 接口详情提取 📦 字段定义

**参数分类**：
```
Path参数: /users/{id} → id为路径参数
Query参数: /users?page=1&size=10 → page,size为查询参数
Header参数: Authorization: Bearer xxx → 认证header
Body参数: POST请求体 → JSON Schema定义
Cookie参数: session_id=xxx → Cookie参数
```

**数据类型规范**：
| JSON Type | 格式约束 | 示例 |
|-----------|----------|------|
| string | - | "hello" |
| string | email | "user@example.com" |
| string | date | "2024-01-01" |
| string | date-time | "2024-01-01T12:00:00Z" |
| string | uri | "https://api.example.com" |
| string | uuid | "550e8400-e29b..." |
| integer | int32/int64 | 123 |
| number | float/double | 12.34 |
| boolean | - | true/false |
| array | - | [1,2,3] |
| object | - | {"key":"value"} |

**必填vs可选**：
- required: 必填字段
- nullable: 可为null
- default: 默认值

---

### Step 3: 响应模式定义 📤 状态码体系

**HTTP状态码规范**：
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | 成功响应 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功（无body） |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突 |
| 422 | Unprocessable Entity | 验证失败 |
| 429 | Too Many Requests | 请求过于频繁 |
| 500 | Internal Server Error | 服务器错误 |
| 503 | Service Unavailable | 服务不可用 |

**响应体结构**：
```json
// 成功响应
{
  "code": 0,
  "message": "success",
  "data": { ... }
}

// 错误响应
{
  "code": 40001,
  "message": "参数错误",
  "data": null
}
```

---

### Step 4: 认证与安全配置 🔐 安全规范

**认证方式**：
| 方式 | 适用场景 | Header格式 |
|------|----------|------------|
| Bearer Token | API Key / JWT | Authorization: Bearer xxx |
| Basic Auth | 用户名密码 | Authorization: Basic base64 |
| API Key | 静态密钥 | X-API-Key: xxx |
| OAuth 2.0 | 第三方授权 | - |

**安全扫描清单**：
- [ ] 敏感参数脱敏（password/secret/token）
- [ ] 脱敏字段不能出现在日志中
- [ ] 请求体大小限制
- [ ] 速率限制说明（Rate Limit）
- [ ] CORS配置说明

**安全Headers**：
```
X-Request-ID: 请求追踪ID
X-Rate-Limit-Limit: 请求限额
X-Rate-Limit-Remaining: 剩余请求数
X-Rate-Limit-Reset: 重置时间戳
```

---

### Step 5: OpenAPI 3.0规范生成 📄 标准输出

**文件结构**：
```yaml
openapi: 3.0.3
info:
  title: API名称
  version: 版本号
  description: API描述
servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://api-staging.example.com/v1
    description: 测试环境
paths:
  /users:
    get:
      summary: 获取用户列表
      operationId: getUsers
      tags:
        - 用户管理
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
components:
  schemas:
    UserList:
      type: object
      properties:
        users:
          type: array
          items:
            $ref: '#/components/schemas/User'
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
```

---

### Step 6: SDK示例生成 💻 多语言示例

**Python SDK示例**：
```python
import requests

class ExampleAPI:
    BASE_URL = "https://api.example.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def get_users(self, page: int = 1, size: int = 20) -> dict:
        """获取用户列表"""
        response = self.session.get(
            f"{self.BASE_URL}/users",
            params={"page": page, "size": size}
        )
        response.raise_for_status()
        return response.json()
    
    def create_user(self, name: str, email: str) -> dict:
        """创建用户"""
        response = self.session.post(
            f"{self.BASE_URL}/users",
            json={"name": name, "email": email}
        )
        response.raise_for_status()
        return response.json()

# 使用示例
api = ExampleAPI(api_key="your_api_key")
users = api.get_users(page=1, size=10)
```

**JavaScript SDK示例**：
```javascript
class ExampleAPI {
  constructor(apiKey) {
    this.baseURL = 'https://api.example.com/v1';
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }

  async getUsers(page = 1, size = 20) {
    const response = await fetch(
      `${this.baseURL}/users?page=${page}&size=${size}`,
      { headers: this.headers }
    );
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  }

  async createUser(name, email) {
    const response = await fetch(`${this.baseURL}/users`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ name, email })
    });
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  }
}

// 使用示例
const api = new ExampleAPI('your_api_key');
const users = await api.getUsers(1, 10);
```

**cURL示例**：
```bash
# 获取用户列表
curl -X GET "https://api.example.com/v1/users?page=1&size=10" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"

# 创建用户
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com"}'
```

---

### Step 7: Mock服务器配置 🎭 测试配置

**Mock配置模板**：
```javascript
// mock-server.js
const express = require('express');
const app = express();
app.use(express.json());

// 用户列表Mock
app.get('/v1/users', (req, res) => {
  res.json({
    code: 0,
    message: 'success',
    data: {
      users: [
        { id: 1, name: '张三', email: 'zhangsan@example.com' },
        { id: 2, name: '李四', email: 'lisi@example.com' }
      ],
      pagination: {
        page: 1,
        size: 20,
        total: 100
      }
    }
  });
});

// 创建用户Mock
app.post('/v1/users', (req, res) => {
  const { name, email } = req.body;
  res.status(201).json({
    code: 0,
    message: 'success',
    data: { id: Math.floor(Math.random() * 1000), name, email }
  });
});

app.listen(3000, () => console.log('Mock server running on :3000'));
```

**Mock响应规则**：
- [ ] 正常场景：返回模拟数据
- [ ] 错误场景：返回错误码和消息
- [ ] 延迟模拟：可配置网络延迟（ms）
- [ ] 随机失败：可模拟5xx错误

---

### Step 8: 集成测试用例生成 🧪 测试覆盖

**测试用例模板**：
```javascript
// api.test.js
const axios = require('axios');

describe('用户管理API测试', () => {
  const api = axios.create({
    baseURL: 'https://api.example.com/v1',
    headers: { Authorization: 'Bearer test_token' }
  });

  describe('GET /users', () => {
    test('正常获取用户列表', async () => {
      const res = await api.get('/users', {
        params: { page: 1, size: 10 }
      });
      expect(res.status).toBe(200);
      expect(res.data.code).toBe(0);
      expect(res.data.data.users).toBeInstanceOf(Array);
    });

    test('分页参数验证', async () => {
      const res = await api.get('/users', {
        params: { page: 999, size: 0 }
      });
      expect(res.data.code).toBe(400);
    });
  });

  describe('POST /users', () => {
    test('正常创建用户', async () => {
      const res = await api.post('/users', {
        name: '测试用户',
        email: 'test@example.com'
      });
      expect(res.status).toBe(201);
      expect(res.data.data.id).toBeDefined();
    });

    test('邮箱格式错误', async () => {
      try {
        await api.post('/users', {
          name: '测试',
          email: 'invalid-email'
        });
      } catch (e) {
        expect(e.response.status).toBe(400);
      }
    });
  });
});
```

---

## 输出模板

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 API文档 | {API名称} | v{版本}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 概述
| 属性 | 值 |
|------|-----|
| API名称 | {name} |
| 版本 | v{version} |
| Base URL | {base_url} |
| 认证方式 | {Bearer Token/API Key/...} |
| 数据格式 | JSON |
| 字符编码 | UTF-8 |

## 快速开始

### 1. 获取API Key
[申请流程说明]

### 2. 安装SDK
```bash
pip install example-api-sdk    # Python
npm install example-api-sdk   # JavaScript
```

### 3. 首次调用
```python
from example_api import Client
client = Client(api_key="YOUR_API_KEY")
result = client.get_users()
```

## 认证说明
[认证方式详细说明]
[Token获取/刷新流程]

## 接口文档

### GET /users
获取用户列表

**请求参数**
| 参数名 | 类型 | 位置 | 必填 | 说明 |
|--------|------|------|------|------|
| page | int | query | 否 | 页码，默认1 |
| size | int | query | 否 | 每页数量，默认20 |

**响应示例**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "users": [...],
    "pagination": {...}
  }
}
```

### POST /users
创建用户

**请求参数**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 用户名 |
| email | string | 是 | 邮箱 |

**请求示例**
```json
{
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

## 错误码
| 错误码 | HTTP状态码 | 说明 | 解决方案 |
|--------|------------|------|----------|
| 0 | 200 | 成功 | - |
| 40001 | 400 | 参数错误 | 检查请求参数 |
| 40101 | 401 | 认证失败 | 检查API Key |
| 40301 | 403 | 无权限 | 申请权限 |
| 40401 | 404 | 资源不存在 | 检查ID |
| 42901 | 429 | 请求过于频繁 | 降低频率 |

## SDK示例

### Python
```python
[完整SDK代码]
```

### JavaScript
```javascript
[完整SDK代码]
```

### cURL
```bash
[完整cURL命令]
```

## Mock服务
```bash
npm install -g mock-server
mock-server start --port 3000 --spec ./api_doc.yaml
```

## 集成测试
```bash
npm test
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 输出文件：
- api_doc.md        # Markdown格式文档
- api_doc.yaml      # OpenAPI 3.0规范
- api_doc.html      # HTML可阅读文档
- sdk_python.py     # Python SDK
- sdk_javascript.js # JavaScript SDK
- sdk_examples.sh   # cURL示例
- mock_server.js    # Mock服务
- api_tests.js      # 测试用例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 正向示例 ✅

### 示例1：FastAPI代码生成完整文档
```
**输入**：
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**输出**：完整OpenAPI YAML + Markdown文档 + Python SDK
```

### 示例2：URL链接解析生成文档
```
**输入**：https://api.github.com/users/{username}

**输出**：
- GitHub用户API完整文档
- 自动识别认证方式（Bearer Token）
- 生成响应字段说明
- 错误码映射（404/403等）
```

---

## 反向示例 ❌

### 示例3：遗漏认证信息
```
**问题**：只生成接口，遗漏认证header

**正确做法**：
- 每个接口自动添加认证参数
- 敏感字段自动标记
- 提供测试Token说明
```

### 示例4：状态码不完整
```
**问题**：只有200成功响应

**正确做法**：
- 覆盖所有常见状态码
- 每种错误提供code和message
- 错误场景给出解决方案
```

---

## 边界场景 🌐

### 边界1：分页参数处理
```
场景：大量数据分页查询
文档需包含：
- 页码分页：page/size
- 游标分页：cursor/limit
- 偏移分页：offset/limit
- 分页响应结构
```

### 边界2：文件上传接口
```
特殊处理：
- Content-Type: multipart/form-data
- 文件大小限制
- 支持格式列表
- 上传进度说明
```

### 边界3：WebSocket接口
```
文档需包含：
- 连接建立：wss://...
- 心跳机制
- 消息格式
- 断线重连策略
- 错误码体系
```

### 边界4：超时时重试策略
```
重试规范：
- 超时时间：默认30s
- 最大重试：3次
- 指数退避：1s → 2s → 4s
- 重试头：X-Retry-Count
```

### 边界5：版本迁移指南
```
v1 → v2迁移：
- 废弃时间线
- breaking changes清单
- 迁移步骤
- 兼容模式说明
```

---

## GraphQL支持 📊

**输出扩展**：
```graphql
# GraphQL Schema

type Query {
  users(page: Int, size: Int): UserConnection!
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

type User {
  id: ID!
  name: String!
  email: String!
}

input CreateUserInput {
  name: String!
  email: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}
```

---

## 质量检查清单 ✅

**文档发布前检查**：
- [ ] 所有接口都有完整参数说明
- [ ] 响应格式示例可运行
- [ ] 错误码覆盖完整
- [ ] SDK代码无语法错误
- [ ] 认证方式清晰可操作
- [ ] Mock服务可用
- [ ] 测试用例覆盖主流程
- [ ] 版本号正确

---

## Output Language
中文文档，代码示例英文注释

## Anti-rationalization

| 借口 | 正确做法 |
|------|----------|
| "认证方式代码里没写，跳过不标了" | 必须显式标注认证方式（Bearer/Basic/API Key/OAuth），无认证也要注明"该接口无需认证" |
| "响应只写200成功的格式就行" | 必须覆盖至少4种HTTP状态码（200/400/401/404），每种错误附带错误码code和message |
| "SDK示例写一个语言就够了" | 必须提供至少3种语言示例（Python/JavaScript/cURL），每段代码必须可直接运行 |
| "参数类型写string或int就行了" | 每个参数必须标注完整类型信息：类型+格式+约束（如string/email/maxLength），必填/可选必须明确 |
| "Mock服务用户自己搭就行，不用提供" | 必须提供可运行的Mock服务代码，覆盖正常和异常场景 |
| "错误码在业务层定义，不用列全" | 必须提供完整错误码映射表，每个错误码附带HTTP状态码、含义和解决方案 |
| "分页/限流这些边界场景不用写" | 分页参数、速率限制、超时重试策略必须在文档中显式说明，即使是默认值也要标注 |
