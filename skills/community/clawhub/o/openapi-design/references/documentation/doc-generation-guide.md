# Documentation Generation Guide

## 文档生成流程

### 1. 从 OpenAPI 规范生成

#### 使用 Redocly

```bash
# 安装
npm install -g @redocly/cli

# 生成 HTML 文档
redocly build-docs openapi.yaml

# 启动预览
redocly preview-docs openapi.yaml
```

#### 使用 Swagger UI

```bash
# 使用 swagger-ui
docker run -p 8080:80 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v $(pwd)/openapi.yaml:/spec/openapi.yaml \
  swaggerapi/swagger-ui
```

---

## 2. 文档结构

### 必需章节

```markdown
# API 名称

## 概述
[API 简介]

## 认证
[认证方式和流程]

## 基础 URL
```
https://api.example.com/v1
```

## 端点列表

### Users

#### List Users
`GET /users`

#### Get User
`GET /users/{userId}`

#### Create User
`POST /users`

[... 其他端点 ...]

## 错误码参考

| 错误码 | HTTP Status | 描述 |
|--------|-------------|------|
| AUTH_001 | 401 | 认证失败 |
| VAL_001 | 400 | 参数验证失败 |

## 速率限制
[限制说明]
```

---

## 3. 代码示例

### cURL 示例

```bash
# 获取用户列表
curl -X GET "https://api.example.com/v1/users?page=1&limit=20" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json"

# 创建用户
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secret123"
  }'
```

### JavaScript 示例

```javascript
// 获取用户列表
const response = await fetch('https://api.example.com/v1/users', {
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log(data);
```

### Python 示例

```python
import requests

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.example.com/v1/users',
    headers=headers
)

data = response.json()
print(data)
```

---

## 4. 交互式文档

### Swagger Hub

1. 访问 https://app.swaggerhub.com
2. 创建账号并登录
3. Import OpenAPI 规范
4. 自动生成交互式文档

### Postman

1. 导入 OpenAPI 规范
2. 自动生成 Collection
3. 可以直接测试 API

---

## 5. 文档维护

### 版本同步

| 变更类型 | 需要更新文档 |
|----------|--------------|
| 新增端点 | ✅ |
| 修改参数 | ✅ |
| 新增字段 | ✅ |
| Bug 修复 | ❌ |
| 性能优化 | ❌ |

### 审查流程

```
API 变更 → 更新 OpenAPI → 审查 → 发布文档
              ↓
          自动化测试（lint）
```

---

## 6. 自动化工具

### Lint 检查

```bash
# Spectral lint
npx @stoplight/spectral lint openapi.yaml

# 检查规则
spectral lint openapi.yaml \
  --ruleset https://raw.githubusercontent.com/oursky/openapi-main/master/.spectral.yaml
```

### 文档部署

```yaml
# GitHub Actions 示例
name: Deploy API Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build docs
        run: npx @redocly/cli build-docs openapi.yaml
      - name: Deploy
        run: |
          # 部署到 GitHub Pages 或其他托管服务
```
