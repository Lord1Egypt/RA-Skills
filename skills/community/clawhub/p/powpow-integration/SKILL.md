# POWPOW Integration Skill v2.1.10

## 基本信息

- **Name**: powpow-integration
- **Version**: 2.1.10
- **Description**: POWPOW WebSocket Integration - Real-time bidirectional chat with POWPOW digital humans using WebSocket
- **Author**: durenzidu
- **License**: MIT

## 功能

此 Skill 允许 OpenClaw 用户通过 **WebSocket** 与 POWPOW 数字人进行**实时双向通信**：

1. **实时消息收发** - WebSocket 连接，低延迟
2. **自动重连** - 连接断开后自动恢复
3. **消息队列** - 离线消息自动排队发送
4. **多媒体支持** - 文本、语音、图片消息
5. **连接状态监控** - 实时显示连接状态

## 命令

### 连接管理

#### `connect`
连接到 POWPOW WebSocket 服务器

**参数**:
- `digitalHumanId` (string, required): 数字人 ID
- `wsUrl` (string, optional): WebSocket 地址，默认 `wss://global.powpow.online:8080`

**示例**:
```
connect digitalHumanId=abc123
connect digitalHumanId=abc123 wsUrl=wss://global.powpow.online:8080
```

**返回**:
- 连接状态
- 客户端 ID

#### `disconnect`
断开 WebSocket 连接

**参数**: 无

**示例**:
```
disconnect
```

#### `status`
查看连接状态

**参数**: 无

**示例**:
```
status
```

**返回**:
- 连接状态 (connected/disconnected)
- 数字人 ID
- 连接时长

### 消息发送

#### `send`
发送消息到 POWPOW

**参数**:
- `message` (string, required): 消息内容
- `contentType` (string, optional): 消息类型 (text/voice/image)，默认 text

**示例**:
```
send message="你好，PowPow！"
send message="语音消息" contentType=voice
```

#### `reply`
快捷回复

**参数**:
- `message` (string, required): 回复内容

**示例**:
```
reply message="收到你的消息了！"
```

#### `sendVoice`
发送语音消息

**参数**:
- `content` (string, required): 语音转文字内容
- `mediaUrl` (string, required): 语音文件 URL
- `duration` (number, required): 语音时长（秒）

**示例**:
```
sendVoice content="你好" mediaUrl="https://example.com/voice.mp3" duration=5
```

#### `sendImage`
发送图片消息

**参数**:
- `content` (string, required): 图片描述
- `mediaUrl` (string, required): 图片文件 URL

**示例**:
```
sendImage content="风景照" mediaUrl="https://example.com/image.jpg"
```

### 消息监听

#### `listen`
开始监听 POWPOW 消息

**参数**:
- `autoReply` (boolean, optional): 是否启用自动回复，默认 false

**示例**:
```
listen
listen autoReply=true
```

**说明**:
- 启动后，收到消息会触发 OpenClaw 事件
- 可以配合 `autoReply` 自动回复

#### `stopListen`
停止监听消息

**参数**: 无

**示例**:
```
stopListen
```

## 配置

### 配置文件

```json
{
  "skills": {
    "powpow-integration": {
      "powpowBaseUrl": "https://global.powpow.online",
      "wsUrl": "wss://global.powpow.online:8080",
      "autoReconnect": true,
      "reconnectInterval": 3000
    }
  }
}
```

### 配置项说明

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `powpowBaseUrl` | string | 否 | https://global.powpow.online | POWPOW API 基础 URL |
| `wsUrl` | string | 否 | wss://global.powpow.online:8080 | WebSocket 服务器地址 |
| `autoReconnect` | boolean | 否 | true | 是否自动重连 |
| `reconnectInterval` | number | 否 | 3000 | 重连间隔（毫秒） |

## 依赖

```json
{
  "@openclaw/core": ">=1.0.0",
  "ws": "^8.16.0"
}
```

## 使用示例

### 完整流程示例

```
# 1. 连接到数字人
connect digitalHumanId=your-dh-id

# 2. 开始监听消息
listen autoReply=true

# 3. 发送消息
send message="你好，我是 OpenClaw！"

# 4. 收到消息后会自动触发回复（如果 autoReply=true）

# 5. 停止监听
stopListen

# 6. 断开连接
disconnect
```

### 手动回复示例

```
# 连接并监听（不自动回复）
connect digitalHumanId=your-dh-id
listen

# 当收到消息时，手动回复
reply message="这是手动回复的内容"
```

## 技术细节

### 架构

```
OpenClaw Agent
    │
    ├── Skill 接收命令
    │
    └── WebSocket 连接
            │
            ▼
    POWPOW WebSocket Server (wss://global.powpow.online:8080)
            │
    POWPOW 用户（浏览器/APP）
```

### 特点

- **WebSocket 实时通信**: 比轮询更低延迟
- **自动重连**: 网络不稳定时自动恢复连接
- **消息队列**: 离线时消息不丢失
- **双向通信**: OpenClaw ↔ POWPOW 双向实时

### WebSocket 消息类型

| 类型 | 说明 |
|------|------|
| `chat_message` | 聊天消息 |
| `chat_message_ack` | 消息确认 |
| `connected` | 连接成功 |
| `error` | 错误信息 |

### 数据库存储

消息存储在 POWPOW 的 `openclaw_messages` 表中：

```sql
- digital_human_id: 数字人ID
- sender_type: 'user' | 'openclaw'
- sender_id: 发送者ID
- content: 消息内容
- content_type: 'text' | 'voice' | 'image'
- created_at: 创建时间
```

## 故障排除

### 连接失败

**Q: 无法连接 WebSocket**
A: 
1. 检查 `wsUrl` 配置是否正确
2. 确认网络可以访问 `wss://global.powpow.online:8080`
3. 检查防火墙设置

### 消息发送失败

**Q: 发送消息失败**
A:
1. 确认已执行 `connect` 命令
2. 检查 `status` 确认连接状态
3. 查看错误日志

### 收不到消息

**Q: 发送成功但收不到回复**
A:
1. 确认已执行 `listen` 命令
2. 检查 POWPOW 前端是否在线
3. 查看 WebSocket 网络面板

### 自动重连问题

**Q: 连接频繁断开**
A:
1. 检查网络稳定性
2. 调整 `reconnectInterval` 配置
3. 查看服务器日志

## 更新日志

### v2.1.10 (2026-04-05)

- ✅ **WebSocket 支持**: 全新 WebSocket 实时通信
- ✅ **自动重连**: 智能重连机制
- ✅ **消息队列**: 离线消息不丢失
- ✅ **多媒体消息**: 支持语音、图片
- ✅ **连接状态**: 实时监控连接状态
- ✅ **双向通信**: OpenClaw ↔ POWPOW 实时双向

### v2.1.0 (2026-03-27)

- 轮询机制实现
- 密码认证支持
- AI 自动回复

### v1.0.0 (2024-03-16)

- 初始版本
- 基础 API 集成
