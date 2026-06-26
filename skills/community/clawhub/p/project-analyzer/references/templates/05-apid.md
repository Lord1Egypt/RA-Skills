# {{PROJECT_NAME}} - API 接口文档 (APID)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {{PROJECT_NAME}} |
| 版本 | {{VERSION}} |
| 日期 | {{DATE}} |

---

## 1. 接口概述

| 属性 | 值 |
|------|-----|
| Controller 数量 | {{CONTROLLER_COUNT}} |
| 接口总数 | {{API_COUNT}} |
| 认证方式 | JWT Bearer Token |
| 协议 | HTTP/HTTPS |
| 数据格式 | JSON |

---

## 2. 统一响应格式

### 2.1 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 2.2 分页响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "pageNum": 1,
    "pageSize": 20,
    "list": []
  }
}
```

### 2.3 失败响应

```json
{
  "code": 40001,
  "message": "参数校验失败",
  "data": null
}
```

---

## 3. 错误码定义

### 3.1 系统错误码

| 错误码 | 描述 | 说明 |
|--------|------|------|
| 200 | success | 成功 |
| 40001 | 参数校验失败 | 请求参数不合法 |
| 40002 | 认证失败 | Token 无效或过期 |
| 40003 | 权限不足 | 无权限访问该资源 |
| 50000 | 系统异常 | 服务器内部错误 |

### 3.2 业务错误码

{{ERROR_CODES}}

---

## 4. 接口列表

{{API_LIST}}

---

## 5. 附录

### 5.1 认证方式

```
Authorization: Bearer <JWT_TOKEN>
```

### 5.2 公共请求头

| Header | 说明 |
|--------|------|
| Content-Type | application/json |
| Authorization | Bearer Token |

---

*文档版本: {{VERSION}}*
*最后更新: {{DATE}}*
