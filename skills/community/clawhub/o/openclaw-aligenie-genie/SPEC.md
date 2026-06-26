# Aligenie Cloud Platform — 技术规格文档

**版本**: v1.0
**日期**: 2026-03-30
**状态**: 设计中

---

## 一、设计目标

为 OpenClaw 与天猫精灵的双向通信提供一个**安全、可扩展、云端管理**的基础设施。

核心原则：
- **安全第一**：账户隔离、API Key 分级、密码不可逆哈希
- **零信任架构**：默认不信任任何请求，所有调用需验证
- **用户透明**：绑定流程对用户无感知，无需复杂操作
- **可演进**：CLI 管理，自用期间积累运营经验，未来可开放给外部用户

---

## 二、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                   腾讯云 AligenieServer                      │
│                    (Java Socket Server)                     │
├─────────────────────────────────────────────────────────────┤
│  HTTP Server (端口 58472)                                   │
│  ├── /health              公开                               │
│  ├── /api/v1/account/*   账户管理（注册/登录）              │
│  ├── /api/v1/key/*       API Key 管理                      │
│  ├── /api/v1/device/*     设备管理                          │
│  ├── /api/v1/agent/*     Agent 管理                        │
│  ├── /push                Agent 推送（API Key + 权限校验）  │
│  ├── /genie/webhook       阿里云回调（自动绑定设备）        │
│  ├── /genie/poll          Agent 长轮询                      │
│  ├── /genie/result        Agent 提交结果                    │
│  └── /genie/verify        验证码绑定                        │
├─────────────────────────────────────────────────────────────┤
│  SQLite Database (aligenie.db)                            │
│  ├── users            账户表                                │
│  ├── api_keys         API Key 表                           │
│  ├── devices           设备表（openId 绑定）                │
│  ├── agents           Agent 表                              │
│  ├── bindings         设备-Agent 绑定表                     │
│  └── verify_codes    验证码表                              │
└─────────────────────────────────────────────────────────────┘
                            ↑
              OpenClaw Agent (麻辣龙虾)
              ├── 注册 agent
              ├── poll 请求
              └── 推送消息
```

---

## 三、数据库设计

### 3.1 表结构

```sql
-- 账户表
CREATE TABLE users (
    id              TEXT PRIMARY KEY,           -- UUID
    username        TEXT UNIQUE NOT NULL,       -- 登录用户名
    password_hash   TEXT NOT NULL,              -- PBKDF2-SHA256 哈希
    salt            TEXT NOT NULL,              -- 盐值
    iterations      INTEGER NOT NULL DEFAULT 100000,
    created_at      TEXT NOT NULL,             -- ISO 8601
    updated_at      TEXT NOT NULL,
    last_login_at   TEXT
);

-- API Key 表
CREATE TABLE api_keys (
    id              TEXT PRIMARY KEY,           -- UUID
    user_id         TEXT NOT NULL REFERENCES users(id),
    key_hash        TEXT NOT NULL,              -- SHA-256 哈希（存根）
    key_prefix      TEXT NOT NULL,              -- 前4位（用于显示）
    name            TEXT NOT NULL,               -- Key 名称
    permissions     TEXT NOT NULL,              -- JSON: ["push", "poll", "admin"]
    enabled         INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL,
    last_used_at    TEXT,
    expires_at      TEXT                        -- 可选过期时间
);

-- 设备表（天猫精灵设备）
CREATE TABLE devices (
    id              TEXT PRIMARY KEY,           -- UUID
    user_id         TEXT NOT NULL REFERENCES users(id),
    open_id         TEXT UNIQUE NOT NULL,        -- 阿里云的 openId
    device_type     TEXT,                        -- speaker / display / etc
    device_name     TEXT,                        -- 用户自定义名称
    bound_at        TEXT NOT NULL,               -- 绑定时间
    last_seen_at   TEXT,                        -- 最后活跃时间
    enabled         INTEGER NOT NULL DEFAULT 1
);

-- Agent 表
CREATE TABLE agents (
    id              TEXT PRIMARY KEY,           -- UUID
    user_id         TEXT NOT NULL REFERENCES users(id),
    agent_id        TEXT UNIQUE NOT NULL,        -- 业务 ID（如 "lobster"）
    push_key_hash  TEXT NOT NULL,              -- 推送密钥哈希
    push_key_salt  TEXT NOT NULL,              -- 推送密钥盐
    enabled         INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL,
    last_poll_at   TEXT
);

-- 设备-Agent 绑定表
CREATE TABLE bindings (
    id              TEXT PRIMARY KEY,
    device_id       TEXT NOT NULL REFERENCES devices(id),
    agent_id        TEXT NOT NULL REFERENCES agents(id),
    user_id         TEXT NOT NULL REFERENCES users(id),
    created_at      TEXT NOT NULL,
    UNIQUE(device_id, agent_id)
);

-- 验证码表
CREATE TABLE verify_codes (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    code            TEXT NOT NULL,              -- 6位数字验证码
    device_open_id  TEXT,                        -- 预分配的 openId（可选）
    expires_at      TEXT NOT NULL,               -- 过期时间
    used_at         TEXT,                        -- 使用时间（NULL=未使用）
    created_at      TEXT NOT NULL
);

-- 操作日志（可选，生产环境开启）
CREATE TABLE audit_log (
    id              TEXT PRIMARY KEY,
    user_id         TEXT REFERENCES users(id),
    action          TEXT NOT NULL,
    resource        TEXT,
    ip_address      TEXT,
    created_at      TEXT NOT NULL
);
```

### 3.2 索引

```sql
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_devices_user ON devices(user_id);
CREATE INDEX idx_devices_openid ON devices(open_id);
CREATE INDEX idx_agents_user ON agents(user_id);
CREATE INDEX idx_agents_agentid ON agents(agent_id);
CREATE INDEX idx_bindings_device ON bindings(device_id);
CREATE INDEX idx_bindings_agent ON bindings(agent_id);
CREATE INDEX idx_verify_codes_code ON verify_codes(code);
CREATE INDEX idx_verify_codes_expires ON verify_codes(expires_at);
```

---

## 四、API 设计

### 4.1 认证方式

| 接口类别 | 认证方式 |
|---------|---------|
| 账户注册/登录 | 用户名+密码，返回 API Key |
| 管理接口 | API Key (`X-Api-Key` header) |
| Webhook | 阿里云 Token 文件验证 |
| Push | API Key (`X-Api-Key`) + 权限校验 |

### 4.2 接口列表

#### 账户

```
POST /api/v1/account/register
  Body: {"username": "xxx", "password": "xxx"}
  Response: {"userId": "uuid", "username": "xxx"}

POST /api/v1/account/login
  Body: {"username": "xxx", "password": "xxx"}
  Response: {"apiKey": "ak_xxxx...", "userId": "uuid"}
```

#### API Key 管理

```
GET /api/v1/keys
  Header: X-Api-Key: ak_xxx
  Response: [{"id": "uuid", "name": "main", "prefix": "ak_xk", "permissions": [...], "createdAt": "..."}]

POST /api/v1/keys
  Body: {"name": "agent-key", "permissions": ["push", "poll"], "expiresAt": "2027-01-01T00:00:00Z"}
  Response: {"apiKey": "ak_xxxx_full_key", "id": "uuid", "name": "agent-key"}

DELETE /api/v1/keys/:id
  Header: X-Api-Key: ak_xxx (需要 admin 权限)
  Response: {"success": true}
```

#### 设备管理

```
GET /api/v1/devices
  Header: X-Api-Key: ak_xxx
  Response: [{"id": "uuid", "openId": "ou_xxx", "deviceType": "speaker", "boundAt": "..."}]

DELETE /api/v1/devices/:id
  Header: X-Api-Key: ak_xxx
  Response: {"success": true}
```

#### 验证码（绑定天猫精灵）

```
POST /api/v1/verifycodes
  Header: X-Api-Key: ak_xxx
  Response: {"code": "384721", "expiresAt": "2026-03-30T12:10:00Z", "expiresIn": 300}
  注意：6位数字，5分钟有效，同一用户最多3个未使用验证码

DELETE /api/v1/verifycodes/active
  Header: X-Api-Key: ak_xxx
  作废当前用户所有未使用的验证码
```

#### Agent 管理

```
GET /api/v1/agents
  Header: X-Api-Key: ak_xxx
  Response: [{"id": "uuid", "agentId": "lobster", "pushKeyPrefix": "pk_xk...", "createdAt": "..."}]

POST /api/v1/agents
  Header: X-Api-Key: ak_xxx
  Body: {"agentId": "lobster"}
  Response: {"id": "uuid", "agentId": "lobster", "pushKey": "pk_xxx_full_key"}
  注意：pushKey 只在创建时返回一次，之后不存储原文

DELETE /api/v1/agents/:id
  Header: X-Api-Key: ak_xxx
  Response: {"success": true}
```

#### Push（Agent 推送消息）

```
POST /push
  Header: X-Api-Key: ak_xxx
  Body: {"agentId": "lobster", "text": "你好，小爪子已上线"}
  权限校验：
    1. API Key 属于某用户
    2. 该用户有该 agentId 的绑定记录
    3. 绑定设备数量 > 0
  Response: {"success": true, "deviceCount": 1}
```

#### Genie2 Webhook

```
POST /genie/webhook
  阿里云回调：
  Body: {"openId": "ou_xxx", "utterance": "384721", "skillId": "xxx", ...}
  
  处理流程：
    1. 验证 skillId 是否匹配
    2. 如果 utterance 是6位数字 → 验证码绑定流程
    3. 否则 → 正常请求入队，等待 poll
```

### 4.3 错误码

```json
{
  "error": "ERROR_CODE",
  "message": "Human readable message",
  "details": {}
}
```

| 错误码 | 说明 |
|--------|------|
| `INVALID_CREDENTIALS` | 用户名密码错误 |
| `USERNAME_EXISTS` | 用户名已存在 |
| `INVALID_API_KEY` | API Key 无效或禁用 |
| `PERMISSION_DENIED` | 没有该操作的权限 |
| `DEVICE_NOT_FOUND` | 设备不存在 |
| `AGENT_NOT_FOUND` | Agent 不存在 |
| `AGENT_NOT_BOUND` | Agent 未绑定任何设备，无法推送 |
| `VERIFY_CODE_INVALID` | 验证码无效或已过期 |
| `DEVICE_ALREADY_BOUND` | 设备已被其他用户绑定 |
| `RATE_LIMITED` | 请求过于频繁 |

---

## 五、安全设计

### 5.1 密码存储

使用 **PBKDF2-SHA256**，不依赖外部库：

```java
// 存储格式：iterations$salt$hash
// 示例：100000$randomSaltBase64$20字节DerivedKeyBase64

int iterations = 100_000;
byte[] salt = new byte[32]; // 256-bit random salt
PBEKeySpec spec = new PBEKeySpec(password, salt, iterations, 256);
SecretKeyFactory f = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
byte[] hash = f.generateSecret(spec).getEncoded();
String stored = iterations + "$" + Base64.encode(salt) + "$" + Base64.encode(hash);
```

### 5.2 API Key 生成与存储

- 生成：256-bit 随机数，Base64url 编码，前缀 `ak_`
- 存储：**SHA-256 哈希**（不存明文，512-bit 输出）
- 显示：前4位明文 + `***` + 后4位（如 `ak_xk4t***9f2r`）
- 传输：创建时返回一次完整 Key，之后不再暴露

### 5.3 Push Key 生成与存储

- 同 API Key，但前缀 `pk_`
- 每个 agent 独立，用于推送验证

### 5.4 验证码安全

- 6位纯数字，有效期5分钟
- 单用户最多3个未使用验证码（超限自动拒绝生成）
- 验证成功立即失效
- 过期自动清理（每分钟清理）

### 5.5 权限模型

```json
{
  "permissions": {
    "push": "推送消息到绑定的设备",
    "poll": "长轮询获取请求",
    "device:read": "查看设备列表",
    "device:write": "添加/删除设备",
    "agent:write": "创建/删除 Agent",
    "key:write": "管理 API Key",
    "admin": "全部权限"
  }
}
```

### 5.6 Rate Limiting

| 端点 | 限制 |
|------|------|
| `/api/v1/account/*` | 10次/分钟/IP |
| `/push` | 60次/分钟/API Key |
| `/genie/webhook` | 不限制（阿里云调用）|
| `/genie/poll` | 不限制 |

### 5.7 腾讯云安全组配置（补充）

```
入站规则：
- TCP 58472 来源: 0.0.0.0/0    （HTTP 服务）
- TCP 22   来源: 用户IP           （SSH 管理）
```

---

## 六、CLI 管理工具

位置：`C:\temp\aligenie-cli.bat`（或 `.ps1`）

### 6.1 命令列表

```bash
# 账户
aligenie-cli account register <username> <password>
aligenie-cli account login <username> <password>

# API Key
aligenie-cli key list
aligenie-cli key create <name> <permissions...>
aligenie-cli key revoke <keyId>

# 设备
aligenie-cli device list
aligenie-cli device delete <deviceId>

# Agent
aligenie-cli agent list
aligenie-cli agent create <agentId>
aligenie-cli agent delete <agentId>

# 验证码
aligenie-cli verify create          # 生成验证码
aligenie-cli verify list           # 查看当前有效验证码
aligenie-cli verify revoke          # 作废所有验证码

# 服务器
aligenie-cli server status        # 查看运行状态
aligenie-cli server reload         # 重载配置（不停服）
aligenie-cli server stop
```

### 6.2 配置文件

`C:\temp\aligenie-cli-config.json`（不进入代码仓库）：

```json
{
  "server": "http://127.0.0.1:58472",
  "apiKey": "ak_xxx",
  "userId": "uuid"
}
```

---

## 七、数据迁移

**从 JSON 配置迁移到 SQLite：**

初始启动时，如果检测到旧的 JSON 配置文件，自动导入到 SQLite，并备份 JSON。

```java
// 伪代码
if (configJson.exists() && !database.exists()) {
    migrateFromJson(configJson, db);
    backup(configJson, configJson + ".bak");
}
```

---

## 八、部署步骤

### 8.1 依赖准备

需要下载到 `C:\temp\`：
1. `sqlite-jdbc-3.45.1.0.jar` — SQLite JDBC 驱动
2. `AligenieServer.java` — 服务器源码（带 SQLite 支持）
3. `aligenie-cli` — 管理工具

### 8.2 初始化

```bash
# 1. 创建管理员账户
aligenie-cli account register admin <password>

# 2. 创建 Agent
aligenie-cli agent create lobster

# 3. 获取验证码并绑定天猫精灵
aligenie-cli verify create
# → 返回验证码，告诉用户对天猫精灵说这个数字

# 4. 查看绑定状态
aligenie-cli device list

# 5. 获取 agent pushKey（创建时显示一次）
# 在 agent 配置中使用
```

---

## 九、腾讯云 Java 环境说明

| 项目 | 状态 |
|------|------|
| Java | 17.0.9（`C:\Program Files\Java\jdk-17\bin\java.exe`）|
| SQLite JDBC | 需手动下载（约 3MB jar）|
| Python | 2.7.6（Yunjing工具自带，不用于主程序）|
| 网络 | 公网 IP 101.43.110.225，端口 58472 |

---

## 十、TODO

- [ ] 调研 SQLite JDBC 是否可在 Java 17 纯 Socket 服务中使用
- [ ] 实现账户系统（注册/登录/密码哈希）
- [ ] 实现 API Key 系统（生成/存储/校验）
- [ ] 实现设备绑定系统（webhook 回调/验证码）
- [ ] 实现 Agent 系统（注册/pushKey/绑定表）
- [ ] 实现 CLI 管理工具
- [ ] 迁移现有 JSON 配置到 SQLite
- [ ] 更新 DEPLOY.md
