---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: c0953ccabbcc632b8770e0f82d375a8b
    PropagateID: c0953ccabbcc632b8770e0f82d375a8b
    ReservedCode1: 3045022100cf9c36e74f21b1821936b918b4d5237cec8b55c08f9df2343cb0fc3d42ed097602200468169f07f35adc87f3988522afca019f390b00ca78ce4affd46c31c39117a6
    ReservedCode2: 304502200eddfaacc22b74a75baa7112c0b710828ca3d7e4b93b2360ca944036eeec8695022100e676942246e55647b724f06fe07d6cbca03131cc16e1dc19a4a5763984a4ac4e
description: 【强制执行】权限控制技能。AI 在执行任何非日常对话的操作前，必须先调用此技能进行权限检查。日常对话（打招呼、闲聊、问天气时间）不需要检查。其他所有操作（执行Skill、发送邮件、创建文档、查看历史记录等）都必须先调用 permission-gate 检查权限。激活条件：用户请求执行任何非日常对话的操作时。
metadata:
    openclaw:
        always: true
name: permission-gate
---

# 权限控制技能（强制执行）

## ⚠️ 重要说明

**这是强制执行的权限检查机制！**
- AI **必须**在执行任何需要权限的操作前调用此 Skill
- **严禁**跳过权限检查直接执行操作
- 违反规则会带来安全风险

## 0. 认证 2.0 核心原则

**每次对话都要先知道对方是谁！**

```
用户发消息
    ↓
提取 open_id + platform
    ↓
调用 handle_unknown_user() 识别身份
    ↓
├── 新账号 → 创建账号 + 打招呼
├── 未绑定 → 询问名字
└── 已绑定 → 正常对话
```

## 1. 何时需要检查

### 需要检查的操作

| 操作类型 | 示例 |
|----------|------|
| 执行 Skill | "帮我创建文档"、"发送邮件" |
| 工具调用 | 调用任何 tool |
| 敏感查询 | 查询手机号、邮箱、地址等 |
| 写操作 | 创建、修改、删除文件/数据 |
| 跨渠道 | 发消息到其他平台 |

### 不需要检查的操作

| 操作类型 | 示例 |
|----------|------|
| 日常对话 | "你好"、"今天天气怎么样" |
| 闲聊 | "你好呀"、"最近怎么样" |
| 普通查询 | "现在几点了"、"今天几号" |

## 2. 检查流程（认证 2.0import sys
sys）

```python
.path.insert(0, '/workspace/skills/permission-check')
from main import handle_unknown_user, process_name_response

# 获取用户ID
open_id = "<从消息中提取的用户ID>"
platform = "<feishu/wecom/...>"

# ============ 认证 2.0：先知道对方是谁 ============

result = handle_unknown_user(open_id, platform)

# Step 1: 处理结果
if result["action"] == "greet":
    # 新账号，返回打招呼消息
    return result["response"]
    
elif result["action"] == "ask_name":
    # 未绑定用户，询问名字
    return result["response"]

elif result["action"] == "normal":
    # 已识别用户，记录用户信息
    user = result["user"]
    user_name = user.get("name") if user else None
    # 继续执行后续权限检查...

# ============ 如果用户回复了名字 ============

# 当用户告诉名字后，调用：
name = "<用户告诉的名字>"
bind_result = process_name_response(open_id, platform, name)
return bind_result["response"]
```

### 完整流程图

```
用户发消息
    ↓
提取 open_id + platform
    ↓
handle_unknown_user()
    ↓
    ├── 新账号 → create_account() + "你好呀～ 第一次见面？"
    ├── 未绑定 → "我们之前聊过，你愿意告诉我名字吗？"
    └── 已绑定 → 正常权限检查
    ↓
用户回复名字
    ↓
process_name_response()
    ↓
    ├── 名字不存在 → create_user() + 绑定 + "xxx你好！"
    └── 名字存在 → （可加验证机制）+ 绑定 + "xxx你好！"
```

## 3. 主人审批流程

当用户申请成为朋友时：

```python
from main import create_approval_request, notify_owner_approval, process_owner_reply

# 1. 用户申请成为朋友
approval = create_approval_request(
    request_type="friend_apply",
    user_id=user_id,
    open_id=open_id,
    target_identity="friend",
    code=用户提供的暗号
)

# 2. 通知主人
msg = notify_owner_approval(approval["id"])
# 发送消息给主人

# 3. 主人回复处理
# 主人说 "同意 approval_xxx" 或 "拒绝 approval_xxx"
result = process_owner_reply(主人回复)
```
```

## 4. 响应模板

### 有权限时

```
（正常执行用户请求的操作）
```

### 无权限时

```
抱歉，我没有权限执行此操作。
原因：{reason}
如需获得权限，请联系主人授权。
```

### 无法识别用户时

```
抱歉，我无法确认你的身份。
如需获得权限，请先通过身份验证。
```

## 5. 注意事项

1. **必须调用**：即使你知道用户是谁，也必须调用此 Skill
2. **不能跳过**：严禁直接执行操作而不检查权限
3. **安全优先**：不确定时，宁可拒绝也不要放行
4. **记录日志**：检查结果会自动记录

## 6. 获取用户ID

用户ID从消息元数据中获取：
- 飞书：消息的 `sender_id` 或 `open_id`
- 企微：消息的 `user_id`
- 其他渠道：类似

如果无法获取用户ID，按无权限处理。
