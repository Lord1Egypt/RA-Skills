# PingCode API 参考

## 认证

### 获取企业令牌

```http
GET https://open.pingcode.com/v1/auth/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}
```

响应：
```json
{
  "access_token": "e7321ca8-f724-4abd-9169-d76d095c6acf",
  "token_type": "Bearer",
  "expires_in": 1577808000
}
```

## 工作项 API

### 获取工作项列表

```http
GET https://open.pingcode.com/v1/agile/workitems?page_size=30&page_index=0
Authorization: Bearer {access_token}
```

### 创建工作项

```http
POST https://open.pingcode.com/v1/agile/workitems
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "工作项标题",
  "type": "story",
  "project_id": "项目ID",
  "assignee_id": "负责人ID"
}
```

## 项目 API

### 获取项目列表

```http
GET https://open.pingcode.com/v1/agile/projects
Authorization: Bearer {access_token}
```

## 迭代 API

### 获取迭代列表

```http
GET https://open.pingcode.com/v1/agile/iterations?project_id={project_id}
Authorization: Bearer {access_token}
```

## 更多文档

完整 API 文档：https://open.pingcode.com/
