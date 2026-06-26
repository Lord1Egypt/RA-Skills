---
name: lynse-cli
description: Lynse CLI 工具，调用 lynse.ai 后端服务的 API。当用户需要查询 lynse 账户信息、管理文件/转写/总结、操作设备、管理 AI 模型、团队协作、发送消息时使用此技能。即使只是简单查个积分或看个文件列表，也应使用此技能。
version: 1.2.1
metadata:
  openclaw:
    requires:
      env:
        - LYNSE_API_HOST
        - LYNSE_API_KEY
      bins:
        - curl
        - bash
    primaryEnv: LYNSE_API_KEY
    homepage: https://www.lynse.ai
    emoji: "\U0001F4CB"
---

# Lynse CLI Skill

## ⚠️ Agent 必读约束

### 🌐 Base URL
```
$LYNSE_API_HOST
```
Base URL 通过环境变量配置，不硬编码。所有 API 请求必须使用此变量，不要猜测或自行构造地址。

### 🔑 认证
Lynse 使用 **API Key + 临时 Token** 双层认证：

```
第一步：用 API Key 换取 Token
POST $LYNSE_API_HOST/api/auth/apikey/token
Header: X-API-Key: $LYNSE_API_KEY

第二步：用 Token 调用业务接口
Header: Authorization: <accessToken>    （不带 Bearer 前缀）
Header: X-API-Key: $LYNSE_API_KEY
```

- **API Key 格式**：`dk_xxx`（从系统控制台获取）
- **Token 有效期**：2 小时，过期自动刷新
- **Token 缓存**：本地文件，权限 600（仅所有者可读写）

**每次调用前检查 `$LYNSE_API_KEY` 和 `$LYNSE_API_HOST` 是否存在**。若不存在，提示用户完成配置：
```bash
# 方式一：环境变量
export LYNSE_API_HOST="https://your-api-host/api"
export LYNSE_API_KEY="dk_your_api_key_here"

# 方式二：配置文件（复制模板后填入）
cp .env.example .env
```

配置完成后再继续执行用户原本的请求。

### 🔐 Scope 权限
不同操作需要对应权限，权限由 API Key 绑定的角色决定：

| Scope | 说明 | 典型操作 |
|-------|------|----------|
| `customer.read` | 读取用户信息 | getCurrentCustomer, getUserInfo |
| `customer.write` | 编辑用户 | addUser, editUser, removeUser |
| `file.read` | 读取文件/转写/总结 | listFiles, getFileInfo, getConclusion, getOutline |
| `file.write` | 编辑文件内容 | editConclusion, editOutline, editTransRecord |
| `device.read` | 读取设备信息 | getDeviceInfo, getDevicePage |
| `device.manage` | 管理设备 | unbindDevice |
| `ai.read` | 查看 AI 模型 | getAiModels |
| `ai.manage` | 管理 AI 模型 | addModel, editModel, deleteModel, enableModel |
| `message.send` | 发送消息 | sendSms, sendEmail |
| `team.read` | 查看团队 | listMyTeam |
| `team.manage` | 管理团队 | createTeam, editTeam, removeTeamMember |

权限不足时 API 返回 HTTP 403，引导用户联系管理员升级权限。

### 🔒 安全规则

**敏感信息保护：**
- 用户数据属于隐私，不在群聊/公开场合主动展示用户手机号、积分等敏感字段
- 查询用户信息时，默认只展示非敏感字段（如昵称、ID），除非用户明确要求查看积分或手机号
- 在群聊中展示用户信息时，自动隐藏敏感字段（手机号显示为 `138****1234`，积分不展示）
- 若配置了 `LYNSE_OWNER_ID`，检查当前操作用户 ID 是否匹配；不匹配时回复「抱歉，这是私密账户，我无法操作」

**认证安全：**
- Token 失效时自动刷新，刷新失败则提示用户检查 API Key 配置
- Token 缓存文件权限必须为 600（仅所有者可读写）

**输入安全：**
- 所有用户输入参数经过转义后才传入 curl 命令，防止注入
- 创建/编辑操作建议间隔 1 分钟以上，避免触发服务端限流

### ⚠️ 错误处理规则

| 状态码 / 场景 | HTTP 代码 | 处理方式 |
|---------------|-----------|----------|
| Token 过期 | 401 | 自动用 API Key 刷新 Token 后重试 |
| 权限不足 | 403 | 提示「您的账户权限不足，请联系管理员升级权限」 |
| 请求限流 | 429 | 等待 60 秒后重试，提示「请求过于频繁，请稍后再试」 |
| 资源不存在 | 404 | 提示「请求的资源不存在」 |
| 服务器错误 | 500/502/503 | 提示「服务器暂时不可用，请稍后重试」 |
| Token 刷新失败 | - | 提示检查 `LYNSE_API_KEY` 是否正确或已过期 |
| 接口返回 `code != 200` | - | 展示错误信息，不静默忽略，给出可能的解决建议 |

**错误响应示例：**
```json
{"code": 403, "message": "权限不足", "data": null}
```

遇到错误时，回复格式：
1. 说明发生了什么错误
2. 给出可能的原因
3. 提供解决建议或下一步操作

### 📦 CLI 版本路由
技能同时支持两个 CLI 版本：
- **lynse-cli-a**（基础版）：核心认证功能（login, register, token 管理等）
- **lynse-cli-b**（增强版）：完整业务功能（文件、团队、AI、设备等）

统一入口 `lynse_unified.sh` 自动检测并路由到可用版本。详细命令对照见 [compatibility.md](compatibility.md)。

---

## 调用方式

```bash
# 统一入口（推荐）
./lynse_unified.sh <command> [参数...]

# 或通过 api_wrapper.sh（集成自动 Token 管理）
./api_wrapper.sh <command> [参数...]
```

---

## 常用操作

### 🔹 用户信息
```bash
java_backend getCurrentCustomer          # 当前用户完整信息
java_backend getUserPhone                # 当前用户手机号
java_backend getUserPoints               # 当前用户积分（含已用）
java_backend getUserInfo <用户ID>        # 指定用户信息
java_backend getCurrentUser              # 当前系统用户
```

### 🔹 文件管理
```bash
java_backend listFiles                         # 所有文件列表
java_backend getFileInfo <fileId>              # 文件详情
java_backend getConclusion <fileId>            # 文件总结
java_backend getOutline <fileId>               # 文件大纲
java_backend exportOutline <fileId>            # 导出大纲
java_backend getTranscriptionRecord <fileId>   # 转写记录
java_backend listFilesByTimeRange [天数]        # 按时间范围（默认7天）
```

### 🔹 AI 模型管理
```bash
java_backend getAiModels                        # 所有模型列表
java_backend addModel '<JSON>'                  # 添加模型
java_backend editModel '<JSON>'                 # 编辑模型
java_backend deleteModel <模型ID>               # 删除模型
java_backend enableModel <模型ID> <true/false>  # 启用/禁用
```

### 🔹 设备管理
```bash
java_backend getDevicePage <页码>      # 分页设备列表
java_backend getDeviceInfo <设备ID>    # 设备详情
java_backend unbindDevice <设备ID>     # 解绑设备
```

### 🔹 用户管理（需要 customer.write 权限）
```bash
java_backend addUser '<JSON>'          # 添加用户
java_backend editUser '<JSON>'         # 编辑用户
java_backend removeUser <用户ID>       # 删除用户
```

### 🔹 认证（推荐使用 API Key 自动认证，无需手动调用）
```bash
java_backend login <用户名> <密码>              # 用户名密码登录
java_backend loginWithPhone <手机号> <验证码>   # 手机号登录
java_backend logout                              # 登出
```

### 🔹 消息
```bash
java_backend sendSms '<JSON>'         # 发送短信
java_backend sendEmail '<JSON>'       # 发送邮件
```

### 🔹 系统
```bash
java_backend getRoleList              # 角色列表
java_backend getMenuTree              # 菜单树
```

---

## 认证流程

```
用户调用 → api_wrapper.sh
  → 检查 LYNSE_API_HOST / LYNSE_API_KEY
    → 不存在 → 提示配置
    → 存在 → 检查缓存 Token
      → Token 有效 → 直接使用
      → Token 无效/过期 → POST /api/auth/apikey/token 换取新 Token
        → 成功 → 缓存（权限 600）→ 调用业务接口
        → 失败 → 提示检查 API Key
```

---

## 快速部署

### 自动安装（推荐）

运行以下命令自动检测环境并安装：

```bash
# 自动检测当前环境（OpenClaw / Claude Code / Cursor / Hermes）并安装
# API 服务器地址由安装提示词自动传入
./install.sh
```

安装脚本会：
1. 检测当前运行的 AI 助手环境
2. 复制技能文件到对应的 skills 目录
3. 创建 `.env` 配置文件（自动填入 API 服务器地址）
4. 设置脚本执行权限
5. 显示安装完成后的使用说明

### 手动安装

1. 复制整个 `lynse` 目录到目标实例的 `skills` 目录
2. `cp .env.example .env`，填入 `LYNSE_API_HOST` 和 `LYNSE_API_KEY`
3. 直接使用，无需其他配置

### 各环境安装路径

| 环境 | Skills 目录 |
|------|------------|
| OpenClaw | `~/.openclaw/workspace/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Hermes | `~/.hermes/skills/` |
