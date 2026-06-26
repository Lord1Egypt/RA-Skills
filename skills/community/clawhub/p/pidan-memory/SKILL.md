# Pidan Memory Skill

本地持久化向量记忆系统，为 AI Assistant 提供长期记忆能力。支持多用户/共享模式。

## 概述

基于 **LanceDB + Ollama** 实现的本地向量记忆系统，支持语义搜索和多用户隔离。

## 架构

```
用户输入 → Ollama (向量化) → LanceDB (存储/搜索)
                    ↑
              nomic-embed-text (768维向量)
```

## 功能

### 1. 自动记忆（推荐）

**安装 Hook 后自动生效，无需手动调用！**

每次对话后自动评估并存储重要信息，覆盖 16 大类场景。

**安装方式：**
```bash
# 1. 复制文件
mkdir -p ~/.openclaw/hooks/pidan-memory
cp HOOK.md handler.ts ~/.openclaw/hooks/pidan-memory/
cp auto_memory.py ~/.openclaw/workspace/memory/

# 2. 启用
openclaw hooks enable pidan-memory
openclaw gateway restart
```

### 2. 记住信息 (remember)

手动存储重要信息到向量数据库

**参数:**
- `content`: 记忆内容 (必填)
- `summary`: 摘要 (可选)
- `importance`: 重要程度 1-5 (默认 3)
- `user_id`: 用户 ID (默认 default)

**示例:**
```json
{
  "command": "remember",
  "parameters": {
    "content": "用户最喜欢吃火锅",
    "summary": "饮食偏好",
    "importance": 4,
    "user_id": "default"
  }
}
```

### 3. 搜索记忆 (recall)

语义向量搜索

**参数:**
- `query`: 搜索关键词
- `limit`: 返回数量 (默认 5)
- `user_id`: 用户 ID

### 4. 获取最近记忆 (recent_memories)

获取用户的有权限访问的记忆

### 5. 模式管理

#### 获取当前模式 (get_mode)
```json
{
  "command": "get_mode",
  "parameters": {}
}
```

#### 设置模式 (set_mode)
```json
{
  "command": "set_mode",
  "parameters": {
    "mode": "private"  // 或 "shared"
  }
}
```

**模式说明：**
- `private`: 多用户模式（默认），每个用户记忆独立隔离
- `shared`: 共享模式，所有用户可互相查询共享记忆

### 6. 删除记忆 (delete_memory)

删除记忆（需二次确认，只有创建人可删除）

**参数:**
- `memory_id`: 记忆 ID (必填)
- `confirm`: 是否确认删除 (默认 false)

**首次请求（获取确认）：**
```json
{
  "command": "delete_memory",
  "parameters": {
    "memory_id": "uuid-xxx",
    "confirm": false
  }
}
```

**确认删除：**
```json
{
  "command": "delete_memory",
  "parameters": {
    "memory_id": "uuid-xxx",
    "confirm": true
  }
}
```

**权限规则：**
- ✅ 创建人本人可以删除
- ❌ 非创建人无法删除
- ⚠️ 删除前必须二次确认

### 7. 共享记忆 (share_memory)

将记忆共享给指定用户（只有创建人可以共享）

**参数:**
- `memory_id`: 记忆 ID (必填)
- `visible_to`: 可见用户列表 (默认 []) - 空=私有
- `user_id`: 请求者 ID (用于权限校验)

**示例 - 共享给指定用户：**
```json
{
  "command": "share_memory",
  "parameters": {
    "memory_id": "uuid-xxx",
    "visible_to": ["user_a", "user_b"],
    "user_id": "default"
  }
}
```

**示例 - 取消共享（设为私有）：**
```json
{
  "command": "share_memory",
  "parameters": {
    "memory_id": "uuid-xxx",
    "visible_to": [],
    "user_id": "default"
  }
}
```

**权限规则：**
- ✅ 创建人本人可以共享
- ❌ 非创建人无法共享
- ⚠️ visible_to 为空时 = 私有模式

### 8. 列表记忆 (list_memories)

列出用户有权限访问的所有记忆

### 8. 手动去重 (deduplicate)

手动触发去重（每 20 条自动触发）

### 9. 统计 (stats)

获取记忆统计信息

## 配置

配置文件：`~/.openclaw/workspace/memory/config.yaml`

```yaml
memory:
  mode: private              # private | shared
  deduplicate_after: 20      # 每N条自动去重
```

或通过环境变量：
```bash
MEMORY_MODE=private
MEMORY_DEDUP_AFTER=20
```

## 存储位置

```
~/.openclaw/workspace/memory/lance/  # LanceDB 数据
```

## 技术栈

| 组件 | 作用 |
|------|------|
| LanceDB | 向量存储/搜索 |
| Ollama | 本地 embedding 模型 |
| nomic-embed-text | 768维向量 |

## CLI 测试

```bash
# 添加记忆
echo '{"command": "remember", "parameters": {"content": "测试"}}' | python3 run.py

# 搜索
echo '{"command": "recall", "parameters": {"query": "测试"}}' | python3 run.py

# 获取模式
echo '{"command": "get_mode", "parameters": {}}' | python3 run.py

# 设置模式
echo '{"command": "set_mode", "parameters": {"mode": "shared"}}' | python3 run.py

# 删除记忆（首次）
echo '{"command": "delete_memory", "parameters": {"memory_id": "xxx"}}' | python3 run.py
```

## 安全说明

### 用户身份验证

所有命令通过 **环境变量 `OPENCLAW_USER_ID`** 获取真实用户ID，防止伪造：

```bash
# 设置用户ID
export OPENCLAW_USER_ID=your_user_id
python3 run.py ...
```

### 权限控制

- **删除/共享记忆**：只有创建人可以操作
- **查询记忆**：根据模式(private/shared)决定访问权限
- **参数中的 user_id**：无效，必须通过环境变量

### Hook 模式

通过 Hook 自动触发时，用户ID由平台传递（ DingTalk openid 等），自动注入环境变量。
```
