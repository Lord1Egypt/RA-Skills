# POWPOW Integration Skill v1.0.2

## 基本信息

- **Name**: powpow-integration
- **Version**: 4.0.0
- **Description**: POWPOW 简化版集成 - 用户注册、数字人创建、自动对话
- **Author**: durenzidu
- **License**: MIT

## 功能概述

此 Skill 帮助 OpenClaw 用户完成以下三件事：

| 步骤 | 功能 | 说明 |
|------|------|------|
| 1 | 注册 PowPow 账号 | 获得用户名和密码，可用于登录 PowPow 网站 |
| 2 | 创建数字人 | 设置名字和人设，数字人自动绑定到你的账号 |
| 3 | 自动对话 | PowPow 后端自动处理对话，无需配置 OpenClaw Gateway |

## 简化版特点

**不需要用户提供 OpenClaw Gateway 地址！**

PowPow 后端会自动：
- 接收用户消息
- 调用 AI API
- 返回回复

用户只需要：
1. 注册账号
2. 创建数字人
3. 完成！

## 命令

### 第一步：注册账号

#### `register`
注册 PowPow 账号

**参数**:
- `username` (string, required): 用户名（3-20字符，支持中文、字母、数字、下划线）
- `email` (string, required): 邮箱地址
- `password` (string, required): 密码（至少6位）

**示例**:
```
register username="我的数字人" email="user@example.com" password="123456"
```

#### `login`
登录已有账号

**示例**:
```
login username="我的数字人" password="123456"
```

---

### 第二步：创建数字人

#### `createDigitalHuman`
创建数字人（自动绑定到当前账号）

**参数**:
- `name` (string, required): 数字人名字
- `description` (string, required): 数字人描述/人设
- `lat` (number, optional): 纬度，默认 39.9042（北京）
- `lng` (number, optional): 经度，默认 116.4074（北京）
- `locationName` (string, optional): 位置名称，默认"北京"

**示例**:
```
createDigitalHuman name="小助手" description="一个友好的AI助手，乐于助人，知识渊博"
createDigitalHuman name="导游小明" description="北京导游，熟悉北京历史文化" lat=39.9 lng=116.4 locationName="北京天安门"
```

#### `listDigitalHumans`
列出我的所有数字人

**示例**:
```
listDigitalHumans
```

---

### 第三步：对话

#### `send`
发送消息给数字人

**参数**:
- `message` (string, required): 消息内容

**示例**:
```
send message="你好！有什么可以帮助你的吗？"
```

#### `status`
查看当前状态

**示例**:
```
status
```

---

## 完整使用流程

```
# 步骤 1：注册账号
register username="我的AI助手" email="ai@example.com" password="mypassword123"

# 步骤 2：创建数字人
createDigitalHuman name="小助手" description="一个友好的AI助手，乐于助人，知识渊博"

# 步骤 3：访问地图查看数字人
# 打开 https://global.powpow.online/map

# 步骤 4：（可选）发送消息测试
send message="你好！"
```

---

## 与 v3.x 的区别

| 特性 | v3.x | v4.0 (简化版) |
|------|------|---------------|
| 需要 OpenClaw Gateway | 是 | **否** |
| 需要 webhook URL | 是 | **否** |
| 需要内网穿透 | 是 | **否** |
| 用户门槛 | 高 | **低** |
| 适合人群 | 开发者 | **所有用户** |

---

## 云端部署

**可以在云端 OpenClaw 中使用**，因为：
- 使用 HTTP API，不需要 WebSocket
- 兼容 Serverless 环境（Vercel 等）
- 无需额外服务器

---

## 更新日志

### v4.0.0 (2026-04-07)

- **重大更新**：简化版，不需要用户提供 OpenClaw Gateway
- PowPow 后端自动处理对话
- 降低用户使用门槛
- 适合所有用户
