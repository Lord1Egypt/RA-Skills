---
name: gi-api-design-fastapi
description: Design and implement RESTful API endpoints following FastAPI best practices. Use when creating new API routes, designing request/response schemas, or when the user asks for API design guidance.
tags: ["fastapi", "api", "rest", "openapi", "python", "backend"]
---

# FastAPI 接口设计规范

按照项目规范设计并实现 RESTful API，适用于 tkms + FastAPI 技术栈。

## 何时使用

- 用户请求「设计一个接口」「新增 API」「写个路由」
- 设计请求/响应结构
- 实现 app/router 下的新端点

## 项目结构

```
app/
├── router/     # 路由定义
├── service/    # 业务逻辑
├── dao/        # 数据访问
└── model/
    ├── dto/    # 入参（请求体、查询参数）
    ├── entity/ # 数据库实体
    └── vo/     # 出参（响应体）
```

## 设计原则

### 1. 路由命名

- 资源用复数名词：`/users`、`/orders`
- 嵌套资源：`/users/{user_id}/orders`
- 动作用动词：`/orders/{id}/cancel`（POST）

### 2. HTTP 方法

| 方法 | 用途 | 示例 |
|------|------|------|
| GET | 查询 | GET /users, GET /users/{id} |
| POST | 创建 | POST /users |
| PUT | 全量更新 | PUT /users/{id} |
| PATCH | 部分更新 | PATCH /users/{id} |
| DELETE | 删除 | DELETE /users/{id} |

### 3. 统一响应格式

```python
# 成功
{"code": 0, "message": "success", "data": {...}}

# 分页
{"code": 0, "data": {"list": [...], "total": 100}}

# 错误（由 ApiException 统一处理）
{"code": 400, "message": "参数错误"}
```

### 4. 错误处理

```python
from tkms.exception.api import ApiException

# 业务异常
raise ApiException(code=400, message="用户不存在")
```

### 5. 入参校验

- 使用 Pydantic 模型（dto）
- 路径参数：`user_id: int`
- 查询参数：`Query(..., description="")`
- 请求体：`Body(...)` 或直接声明

### 6. 分页规范

```python
# 入参
page: int = Query(1, ge=1)
page_size: int = Query(20, ge=1, le=100)

# 出参
{"list": [...], "total": 100}
```

## 示例模板

```python
# router/user.py
from fastapi import APIRouter, Depends
from app.model.dto.user_dto import UserCreateDto, UserUpdateDto
from app.model.vo.user_vo import UserVo
from app.service.user_service import UserService

router = APIRouter(prefix="/users", tags=["用户"])

@router.post("", response_model=UserVo)
async def create_user(dto: UserCreateDto, service: UserService = Depends()):
    return await service.create(dto)

@router.get("/{user_id}", response_model=UserVo)
async def get_user(user_id: int, service: UserService = Depends()):
    return await service.get_by_id(user_id)
```

## 安全与权限

- 需要登录：使用依赖注入的认证中间件
- 敏感操作：校验权限/角色
- 限流：按需配置
