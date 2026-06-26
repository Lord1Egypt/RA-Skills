---
name: gi-error-handling
description: Handle errors and logging following project conventions. Use when implementing exception handling, adding logs, or when the user asks for error handling patterns with ApiException.
tags: ["error", "exception", "logging", "tkms", "api-exception"]
---

# Error Handling 错误处理与日志

按项目规范实现错误处理与日志记录。适用于 API 异常、业务错误、日志打点，便于排查问题。

## 何时使用

- 用户请求「加错误处理」「加日志」「异常处理」
- 实现 API 的异常返回
- 排查问题时需要定位错误来源

## 异常处理

### 1. 业务异常

```python
from tkms.exception.api import ApiException

# 抛出业务异常，会返回给前端
raise ApiException(code=400, message="用户不存在")
raise ApiException(code=401, message="未登录")
raise ApiException(code=403, message="无权限")
raise ApiException(code=404, message="资源不存在")
raise ApiException(code=500, message="服务器内部错误")
```

- `code`：HTTP 状态码或业务错误码
- `message`：返回给前端的错误信息，避免暴露内部细节

### 2. 参数校验

```python
if not user_id:
    raise ApiException(code=400, message="用户ID不能为空")

if page < 1:
    raise ApiException(code=400, message="页码必须大于0")
```

### 3. 资源不存在

```python
user = await self.user_dao.get_by_id(user_id)
if not user:
    raise ApiException(code=404, message="用户不存在")
```

### 4. 捕获并转换

```python
try:
    result = await external_api.call()
except ConnectionError as e:
    raise ApiException(code=502, message="服务暂时不可用")
except Exception as e:
    # 记录详细日志，对外返回通用信息
    logger.exception("调用外部服务失败")
    raise ApiException(code=500, message="操作失败，请稍后重试")
```

## 日志规范

### 1. 打点位置

- 接口入口：`logger.info("接口名 入参")`
- 关键业务节点：`logger.info("步骤 结果")`
- 异常：`logger.exception("异常描述")` 或 `logger.error("...")`

### 2. 日志内容

- 不输出密码、Token、完整卡号等敏感信息
- 包含关键上下文：user_id、request_id、操作类型
- 异常时记录堆栈便于排查

### 3. 示例

```python
import logging
logger = logging.getLogger(__name__)

# 入口
logger.info("get_user_list", extra={"user_id": user_id, "page": page})

# 业务节点
logger.info("查询完成", extra={"count": len(rows)})

# 异常
logger.exception("数据库查询失败", extra={"sql": sql_safe})
```

## 统一响应格式

成功：
```json
{"code": 0, "message": "success", "data": {...}}
```

失败（由 ApiException 触发）：
```json
{"code": 400, "message": "用户不存在"}
```

## 前端错误处理

- 根据 `code` 区分：401 跳登录、403 提示无权限、其他展示 `message`
- 网络错误：统一提示「网络异常，请稍后重试」
