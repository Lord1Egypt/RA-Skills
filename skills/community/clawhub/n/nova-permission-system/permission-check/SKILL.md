---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 4b4723df785e2644b131adffbf816f0d
    PropagateID: 4b4723df785e2644b131adffbf816f0d
    ReservedCode1: 3045022100c542d2d5e8948f46c5f8688daeaad98a9e8056385a38b1e857673bd38165138d02204e98e5388d3f5cd4a06c64956d6b23449f8164bb838520f8ba54588212bbb04f
    ReservedCode2: 304402204e98734a5e62d730928648596a04e491ac332304888e8c443862d95968bb760702207c9552c37c725ddb9dc08cf9fc1403708e176022b0f5a47fd61fd9cbea8c34f3
---

# permission-check 技能

## 功能概述

拦截消息并检查用户权限，是权限系统的核心鉴权模块。

## 模块说明

- **main.py** - 核心鉴权模块，提供用户识别、权限检查
- **middleware.py** - 权限检查中间件，用于消息入口处的权限检查

---

## 模块一：main.py 核心鉴权

### 1. identify_user(open_id, platform)

根据平台账号 ID 查找对应的用户信息。

**参数：**
- `open_id` (str): 平台账号 ID（如飞书的 open_id）
- `platform` (str): 平台名称（如 "feishu"）

**返回：**
- 用户对象（含 user_id, name, role）或 `None`（未找到）

### 2. check_permission(user, permission)

检查用户是否拥有指定权限。

**参数：**
- `user` (dict): 用户对象（需包含 role 字段）
- `permission` (str): 权限名称（read/write/admin/execute）

**返回：**
- `True` 允许，`False` 拒绝

**权限逻辑：**
| 角色 | read | write | admin | execute |
|------|------|-------|-------|---------|
| owner | ✅ | ✅ | ✅ | ✅ |
| friend | ✅ | ❌ | ❌ | ✅ |
| stranger | ❌ | ❌ | ❌ | ❌ |

### 3. authenticate(request)

统一鉴权入口，拦截并验证请求。

**参数：**
- `request` (dict): 请求对象，需包含 open_id, platform, permission

**返回：**
- `{"allowed": True/False, "user": user对象, "reason": "..."}`

## 数据文件

技能依赖以下数据文件（位于 /workspace/data/）：
- `users.json` - 用户列表
- `accounts.json` - 账号绑定关系
- `permissions.json` - 角色权限配置

## 使用示例

```python
from skills.permission_check.main import identify_user, check_permission, authenticate

# 根据 open_id 查找用户
user = identify_user("ou_xxx", "feishu")

# 检查权限
if user:
    can_write = check_permission(user, "write")

# 统一鉴权
result = authenticate({
    "open_id": "ou_xxx",
    "platform": "feishu",
    "permission": "read"
})
```

---

## 模块二：middleware.py 权限检查中间件

中间件用于在消息入口处检查权限，支持配置开关和熔断机制。

### 1. check_request(request)

检查请求权限的主入口。

**参数：**
- `request` (dict): 请求对象，需包含：
  - `open_id` (str): 平台账号 ID
  - `platform` (str): 平台名称
  - `action/command/type` (str): 操作类型（可选）

**返回：**
- `{"allowed": True/False, "user": user对象, "reason": "...", "skipped": True/False}`

**特性：**
- 只对需要 execute 权限的操作进行检查
- 日常对话类操作（chat, message, ask 等）自动跳过
- 配置 `enabled=false` 时跳过所有检查
- 缺少用户标识时放行
- 检查异常时熔断放行并记录日志

### 2. check_permission(request, permission)

检查特定权限的中间件。

**参数：**
- `request` (dict): 请求对象
- `permission` (str): 权限名称（read/write/admin/execute）

**返回：**
- 同 check_request

### 使用示例

```python
from skills.permission_check.middleware import check_request

# 在消息入口处调用
result = check_request({
    "open_id": "ou_xxx",
    "platform": "feishu",
    "action": "skill",
    "text": "执行某个技能"
})

if not result["allowed"]:
    return "权限不足，无法执行此操作"

# 继续处理请求...
```

### 配置开关

编辑 `/workspace/config/permission.json`：

```json
{
  "enabled": true
}
```

- `enabled: true` - 启用权限检查
- `enabled: false` - 禁用权限检查（放行所有请求）
