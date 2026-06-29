# api-doc-generator 详细参考

## 支持的框架与代码示例

### Python - Flask
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息
    ---
    tags:
      - 用户
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: 用户ID
    responses:
      200:
        description: 成功
      404:
        description: 用户不存在
    """
    user = {'id': user_id, 'name': '张三', 'email': 'zhang@example.com'}
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户
    ---
    tags:
      - 用户
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: 张三
            email:
              type: string
              format: email
              example: zhang@example.com
    responses:
      201:
        description: 创建成功
    """
    data = request.json
    return jsonify({'id': 1001, **data}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

### Python - FastAPI
```python
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="用户API", version="1.0.0")

class UserCreate(BaseModel):
    """创建用户请求体"""
    name: str
    email: EmailStr
    age: Optional[int] = None

class User(BaseModel):
    """用户响应体"""
    id: int
    name: str
    email: str

users_db = {}

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int = Path(..., description="用户ID")):
    """获取用户详情"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="用户不存在")
    return users_db[user_id]

@app.post("/api/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """创建新用户"""
    user_id = len(users_db) + 1
    new_user = User(id=user_id, name=user.name, email=user.email)
    users_db[user_id] = new_user
    return new_user
```

### JavaScript - Express
```javascript
const express = require('express');
const app = express();
app.use(express.json());

// 获取用户 GET /api/users/:id
app.get('/api/users/:id', (req, res) => {
  const userId = parseInt(req.params.id);
  const user = { id: userId, name: '张三', email: 'zhang@example.com' };
  res.json(user);
});

// 创建用户 POST /api/users
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  const newUser = { id: Date.now(), name, email };
  res.status(201).json(newUser);
});

// 更新用户 PUT /api/users/:id
app.put('/api/users/:id', (req, res) => {
  const userId = parseInt(req.params.id);
  const { name, email } = req.body;
  res.json({ id: userId, name, email, updated: true });
});

// 删除用户 DELETE /api/users/:id
app.delete('/api/users/:id', (req, res) => {
  const userId = parseInt(req.params.id);
  res.json({ id: userId, deleted: true });
});

app.listen(3000);
```

### Go - Gin
```go
package main

import (
    "net/http"
    "strconv"
    "github.com/gin-gonic/gin"
)

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

var users = map[int]User{
    1: {ID: 1, Name: "张三", Email: "zhang@example.com"},
}

// GET /api/users/:id
func GetUser(c *gin.Context) {
    id, _ := strconv.Atoi(c.Param("id"))
    if user, ok := users[id]; ok {
        c.JSON(http.StatusOK, user)
    } else {
        c.JSON(http.StatusNotFound, gin.H{"error": "用户不存在"})
    }
}

// POST /api/users
func CreateUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    user.ID = len(users) + 1
    users[user.ID] = user
    c.JSON(http.StatusCreated, user)
}

func main() {
    r := gin.Default()
    r.GET("/api/users/:id", GetUser)
    r.POST("/api/users", CreateUser)
    r.Run(":8080")
}
```

### Java - Spring Boot
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return new User(id, "张三", "zhang@example.com");
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User createUser(@RequestBody @Valid UserRequest request) {
        return new User(1001L, request.getName(), request.getEmail());
    }

    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody UserRequest request) {
        return new User(id, request.getName(), request.getEmail());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteUser(@PathVariable Long id) {
        return ResponseEntity.ok().body(Map.of("deleted", true));
    }
}

public record User(Long id, String name, String email) {}
public record UserRequest(String name, String email) {}
```

---

## OpenAPI 3.0 规范结构

```yaml
openapi: 3.0.3
info:
  title: 用户管理API
  description: 用户CRUD操作接口
  version: 1.0.0
  contact:
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://staging-api.example.com/v1
    description: 测试环境

paths:
  /users/{id}:
    get:
      summary: 获取用户详情
      operationId: getUserById
      tags: [用户管理]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
            format: int64
          example: 123
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    User:
      type: object
      required: [id, name, email]
      properties:
        id:
          type: integer
          format: int64
          example: 123
        name:
          type: string
          minLength: 1
          maxLength: 50
          example: 张三
        email:
          type: string
          format: email
          example: zhang@example.com
        created_at:
          type: string
          format: date-time
    
    Error:
      type: object
      properties:
        code:
          type: integer
          example: 400
        message:
          type: string
          example: 参数错误
  
  responses:
    NotFound:
      description: 资源不存在
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: 未授权
      headers:
        WWW_Authenticate:
          schema:
            type: string
            example: Bearer realm="api"
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## SDK示例代码

### Python SDK
```python
import requests

class UserAPIClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_user(self, user_id: int) -> dict:
        """获取用户详情"""
        response = requests.get(
            f'{self.base_url}/api/users/{user_id}',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_user(self, name: str, email: str) -> dict:
        """创建用户"""
        response = requests.post(
            f'{self.base_url}/api/users',
            headers=self.headers,
            json={'name': name, 'email': email}
        )
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, **kwargs) -> dict:
        """更新用户"""
        response = requests.put(
            f'{self.base_url}/api/users/{user_id}',
            headers=self.headers,
            json=kwargs
        )
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        response = requests.delete(
            f'{self.base_url}/api/users/{user_id}',
            headers=self.headers
        )
        return response.status_code == 200

# 使用示例
client = UserAPIClient('https://api.example.com', 'your-token-here')
user = client.get_user(123)
print(f'用户名: {user["name"]}')
```

### JavaScript/TypeScript SDK
```typescript
class UserAPIClient {
  private baseURL: string;
  private token: string;

  constructor(baseURL: string, token: string) {
    this.baseURL = baseURL.replace(/\/$/, '');
    this.token = token;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    body?: object
  ): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async getUser(id: number): Promise<User> {
    return this.request<User>('GET', `/api/users/${id}`);
  }

  async createUser(data: CreateUserInput): Promise<User> {
    return this.request<User>('POST', '/api/users', data);
  }

  async updateUser(id: number, data: Partial<User>): Promise<User> {
    return this.request<User>('PUT', `/api/users/${id}`, data);
  }

  async deleteUser(id: number): Promise<void> {
    await this.request<void>('DELETE', `/api/users/${id}`);
  }
}

// 使用示例
const client = new UserAPIClient('https://api.example.com', 'token');
const user = await client.getUser(123);
console.log(`用户名: ${user.name}`);
```

### cURL 示例
```bash
# 获取用户
curl -X GET "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer your-token-here"

# 创建用户
curl -X POST "https://api.example.com/api/users" \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhang@example.com"}'

# 更新用户
curl -X PUT "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "email": "li@example.com"}'

# 删除用户
curl -X DELETE "https://api.example.com/api/users/123" \
  -H "Authorization: Bearer your-token-here"
```

---

## 错误码设计规范

| 错误码 | HTTP状态码 | 说明 | 处理建议 |
|--------|------------|------|----------|
| 0 | 200 | 成功 | - |
| 1001 | 400 | 参数错误 | 检查请求参数 |
| 1002 | 400 | 参数缺失 | 补充必填参数 |
| 1003 | 422 | 参数格式错误 | 校验格式(email/date等) |
| 2001 | 401 | Token无效 | 重新登录获取Token |
| 2002 | 401 | Token过期 | 刷新Token |
| 2003 | 403 | 权限不足 | 申请更高权限 |
| 3001 | 404 | 资源不存在 | 检查ID是否正确 |
| 3002 | 404 | 接口不存在 | 检查请求路径 |
| 4001 | 429 | 请求过于频繁 | 降低请求频率 |
| 5001 | 500 | 服务器内部错误 | 联系技术支持 |
| 5002 | 503 | 服务暂时不可用 | 稍后重试 |

---

## 最佳实践

### 1. RESTful URL 设计
```
✅ GET /api/users          # 获取用户列表
✅ GET /api/users/123      # 获取指定用户
✅ POST /api/users         # 创建用户
✅ PUT /api/users/123      # 更新用户
✅ DELETE /api/users/123   # 删除用户

❌ GET /api/getUser?id=123
❌ POST /api/user/create
```

### 2. 版本控制
```
Base URL: https://api.example.com/v1
下一版本: https://api.example.com/v2
```

### 3. 分页规范
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### 4. 认证方式选择
| 方式 | 适用场景 | 安全性 |
|------|----------|--------|
| Bearer Token (JWT) | Web/移动App | ⭐⭐⭐⭐⭐ |
| API Key | 服务端对服务端 | ⭐⭐⭐⭐ |
| OAuth 2.0 | 第三方授权 | ⭐⭐⭐⭐⭐ |

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 401 Unauthorized | Token缺失/无效 | 检查Authorization头 |
| 404 Not Found | 路径错误/资源不存在 | 核对API路径 |
| 422 Validation Error | 参数校验失败 | 检查参数格式和必填 |
| 429 Rate Limited | 请求超限 | 添加重试间隔 |
| 500 Server Error | 服务端异常 | 联系后端开发 |
