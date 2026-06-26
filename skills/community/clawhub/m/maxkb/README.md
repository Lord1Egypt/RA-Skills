# MaxKB Skill — 智能体路由与调用

> 基于 MaxKB 平台的 Skill，供宿主智能体（LLM）查询已发布智能体列表并按名称发起对话，实现多智能体路由分发。

---

## 目录

- [功能概述](#功能概述)
- [目录结构](#目录结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [环境变量](#环境变量)
- [工具函数说明](#工具函数说明)
  - [list\_agents](#list-agents)
  - [chat\_to\_agent](#chat-to-agent)
- [推荐调用流程](#推荐调用流程)
- [API 接口说明](#api-接口说明)
- [错误处理](#错误处理)

---

## 功能概述

本 Skill 提供两个工具函数，配合宿主智能体的 LLM 完成智能路由与调用：

| 函数              | 说明                                                          |
|-------------------|---------------------------------------------------------------|
| `list_agents`     | 返回当前工作空间所有**已发布**智能体的名称与描述，供 LLM 选择 |
| `chat_to_agent`   | 按 LLM 指定的智能体名称发起对话，返回该智能体的回答           |

---

## 目录结构

```
MaxKB-skills/
├── .env.example        # 环境变量示例（复制为 .env 并填写实际值）
├── .gitignore
├── SKILL.md            # Skill 快速参考文档
└── scripts/
    └── main.py         # Skill 核心实现
```

---

## 环境要求

- Python 3.7+
- 可访问的 MaxKB 实例（v2.x）
- （可选）`python-dotenv`：用于自动加载 `.env` 文件

  ```bash
  pip install python-dotenv
  ```

  若未安装，脚本内置了简单的 `.env` 解析，无需额外安装。

---

## 快速开始

### 1. 配置环境变量

复制示例文件并填写实际值：

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# ==================== 必填配置 ====================

# MaxKB 服务地址（必填）
MAXKB_DOMAIN=http://localhost:8080

# ==================== 选填配置 ====================

# MaxKB API 前缀（选填，默认 /admin）
# - 标准 MaxKB 部署：无需配置（默认 /admin）
# - 子路径部署（如 http://example.com/mk）：配置为 /mk
# - 根路径无前缀：配置为空字符串 ""
MAXKB_API_PREFIX=/admin

# MaxKB 工作空间 ID（选填，默认 default）
MAXKB_WORKSPACE_ID=default

# ==================== 认证配置（二选一）====================

# 方式 1：用户名 + 密码（优先级高）
MAXKB_USERNAME=admin
MAXKB_PASSWORD=admin123

# 方式 2：Token（如果配置了用户名密码，此项被忽略）
# MAXKB_TOKEN=your_token_here
```

> **提示**：
> - `MAXKB_API_PREFIX`：标准部署无需修改，只有非标准部署才需要配置
> - 认证方式：推荐配置用户名密码，系统会自动登录获取 Token
> - 如果同时配置了用户名密码和 Token，系统会使用用户名密码登录

### 2. 列出已发布智能体

```bash
python3 scripts/main.py
```

输出示例：

```json
[
  {"name": "客服助手", "desc": "处理用户常见问题"},
  {"name": "代码助手", "desc": "辅助编写和审查代码"}
]
```

### 3. 向指定智能体提问

```bash
python3 scripts/main.py "Python 里如何读取文件？" "代码助手"
```

输出示例：

```json
{
  "agent_name": "代码助手",
  "answer": "可以使用内置的 open() 函数来读取文件..."
}
```

---

## 环境变量

| 变量                 | 必填 | 说明                              | 默认值                    |
|----------------------|------|-----------------------------------|---------------------------|
| `MAXKB_DOMAIN`       | ✅ 是 | MaxKB 服务地址                    | `<maxkb_domain>`          | 
| `MAXKB_API_PREFIX`   | ❌ 否 | API 路径前缀，适用于子路径部署     | `/admin` |
| `MAXKB_TOKEN`        | ⚠️ 二选一 | Bearer Token（管理员 API Key）    | —                         |
| `MAXKB_USERNAME`     | ⚠️ 二选一 | 登录用户名（优先于 `MAXKB_TOKEN`）| —                         |
| `MAXKB_PASSWORD`     | ⚠️ 二选一 | 登录密码（优先于 `MAXKB_TOKEN`）  | —                         |
| `MAXKB_WORKSPACE_ID` | ❌ 否 | 工作空间 ID                       | `default`                 |

**说明**：
- `MAXKB_API_PREFIX`：标准 MaxKB 部署无需配置（默认 `/admin`），子路径部署需配置（如 `/mk`）
- 认证方式：配置 `MAXKB_USERNAME` + `MAXKB_PASSWORD` **或** `MAXKB_TOKEN`，前者优先级更高

### MAXKB_API_PREFIX 使用说明

**使用场景**：当 MaxKB 部署在子路径下时（非根路径），需要配置此项。

**默认值**：`/admin`（标准 MaxKB 部署）

**示例**：

```bash
# 场景 1：标准 MaxKB 部署（默认值）
# http://localhost:8080/admin/api/...
MAXKB_DOMAIN=http://localhost:8080
MAXKB_API_PREFIX=/admin

# 场景 2：MaxKB 部署在子路径
# http://example.com/mk/api/...
MAXKB_DOMAIN=http://example.com
MAXKB_API_PREFIX=/mk

# 场景 3：MaxKB 部署在根路径且无 /admin 前缀
# http://localhost:8080/api/...
MAXKB_DOMAIN=http://localhost:8080
MAXKB_API_PREFIX=""

# 场景 4：MaxKB 部署在多级子路径
# http://example.com/ai/maxkb/api/...
MAXKB_DOMAIN=http://example.com
MAXKB_API_PREFIX=/ai/maxkb
```

**路径处理规则**：

| API 类型 | 原始路径 | 配置 `MAXKB_API_PREFIX=/mk` 后 |
|----------|----------|-------------------------------|
| 数据 API | `/api/workspace/...` | `/mk/api/workspace/...` |
| 对话 API | `/chat/api/...` | `/chat/api/...` (不变) |

> **注意**：`/chat/` 开头的路径是 MaxKB 前端路由，不会添加 API 前缀。

**认证优先级**：若同时配置了 `MAXKB_USERNAME` + `MAXKB_PASSWORD` 和 `MAXKB_TOKEN`，系统将使用用户名/密码登录获取 Token，忽略 `MAXKB_TOKEN`。

---

## 工具函数说明

### list_agents

返回当前工作空间所有已发布智能体的列表，供 LLM 判断选择合适的智能体。

**函数签名**

```python
list_agents() -> str
```

**返回值**：JSON 字符串，数组中每个元素包含：

| 字段   | 类型   | 说明         |
|--------|--------|--------------|
| `name` | string | 智能体名称   |
| `desc` | string | 智能体描述   |

**返回示例**

```json
[
  {"name": "客服助手", "desc": "处理用户常见问题"},
  {"name": "代码助手", "desc": "辅助编写和审查代码"}
]
```

---

### chat_to_agent

向指定智能体发起一次对话，返回智能体的回答。

**函数签名**

```python
chat_to_agent(question: str, agent_name: str) -> str
```

**参数**

| 参数         | 类型   | 说明                                       |
|--------------|--------|--------------------------------------------|
| `question`   | string | 用户的问题文本                             |
| `agent_name` | string | 由 LLM 从 `list_agents` 结果中选定的名称  |

**返回值**：JSON 字符串，包含：

| 字段         | 类型   | 说明               |
|--------------|--------|--------------------|
| `agent_name` | string | 实际调用的智能体名称 |
| `answer`     | string | 智能体的回答内容   |

**返回示例**

```json
{
  "agent_name": "客服助手",
  "answer": "您好，有什么可以帮助您的？"
}
```

---

## 推荐调用流程

```
用户提问
   │
   ▼
LLM 调用 list_agents()              ← 获取已发布智能体列表
   │  返回 [{"name":..., "desc":...}, ...]
   ▼
LLM 根据问题内容选出最合适的 agent_name
   │
   ▼
LLM 调用 chat_to_agent(question, agent_name)   ← 发起对话
   │  返回 {"agent_name":..., "answer":...}
   ▼
将 answer 返回给用户
```

---

## API 接口说明

脚本内部依次调用以下 MaxKB API：

| 步骤 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 1 | POST | `/admin/api/user/login` | 用户名/密码登录，获取 Token |
| 2 | GET  | `/admin/api/workspace/{workspace_id}/application/1/100` | 获取智能体列表 |
| 3 | GET  | `/admin/api/workspace/{workspace_id}/application/{agent_id}/access_token` | 获取匿名访问 Token |
| 4 | POST | `/chat/api/auth/anonymous` | 创建匿名会话 |
| 5 | GET  | `/chat/api/open` | 初始化对话，获取 chat_id |
| 6 | POST | `/chat/api/chat_message/{chat_id}` | 发送消息（SSE 流式响应）|

---

## 错误处理

| 错误场景                   | 行为                                       |
|----------------------------|--------------------------------------------|
| 无已发布智能体             | 抛出 `RuntimeError`，提示工作空间无可用智能体 |
| 智能体名称不存在           | 抛出 `RuntimeError`，列出所有可用智能体名称 |
| HTTP 请求失败（4xx/5xx）   | 抛出 `RuntimeError`，包含状态码和响应体    |
| 网络连接失败               | 抛出 `RuntimeError`，包含连接错误信息      |
| 登录失败                   | 抛出 `RuntimeError`，包含登录响应内容      |
