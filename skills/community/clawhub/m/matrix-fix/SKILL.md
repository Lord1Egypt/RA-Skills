---
name: matrix-fix
description: >
  修复 Matrix Channel 常见问题：加密模块安装、token 过期处理、重新登录等。
  Use when: Matrix channel 无法正常工作、加密模块报错、token 失效等问题。
metadata: { "openclaw": { "emoji": "🔧", "requires": {} } }
---

# Matrix Channel 修复指南

## 常见问题

### 1. 加密模块缺失

**症状：**
```
MatrixClientLite Failed to initialize crypto storage, E2EE disabled
Cannot find module '@matrix-org/matrix-sdk-crypto-nodejs'
```

**修复：**
```bash
cd /usr/local/lib/node_modules/openclaw
pnpm add @matrix-org/matrix-sdk-crypto-nodejs
pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs
openclaw gateway restart
```

### 2. Token 失效 (M_UNKNOWN_TOKEN)

**症状：**
```
errcode: 'M_UNKNOWN_TOKEN', error: 'Invalid access token passed.'
```

**修复：**
清除旧 token 并重启：
```bash
rm -rf ~/.openclaw/matrix/accounts/*
openclaw gateway restart
```

### 3. DNS 解析失败 (ENOTFOUND)

**症状：**
```
Error: getaddrinfo ENOTFOUND YOUR_HOMESERVER
```

**检查：**
```bash
host YOUR_HOMESERVER
ping YOUR_HOMESERVER
```

### 4. 重新配置 Matrix Channel

**完整重置步骤：**

1. 移除旧配置：
```bash
openclaw config unset channels.matrix
```

2. 重新设置配置：
```bash
openclaw config set channels.matrix.homeserver "https://YOUR_HOMESERVER:PORT"
openclaw config set channels.matrix.userId "@YOUR_BOT_USER_ID"
openclaw config set channels.matrix.password "YOUR_PASSWORD"
openclaw config set channels.matrix.deviceName "YOUR_DEVICE_NAME"
openclaw config set channels.matrix.encryption true
openclaw config set channels.matrix.enabled true
```

3. 重启 Gateway：
```bash
openclaw gateway restart
```

### 5. 退出所有房间

如果需要让 bot 退出所有房间：

```bash
# 获取 access_token
TOKEN=$(curl -s -X POST "https://YOUR_HOMESERVER:PORT/_matrix/client/r0/login" \
  -H "Content-Type: application/json" \
  -d '{"type":"m.login.password","user":"YOUR_BOT_USER","password":"YOUR_PASSWORD"}' | \
  jq -r '.access_token')

# 获取房间列表
curl -s -X GET "https://YOUR_HOMESERVER:PORT/_matrix/client/r0/joined_rooms" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 逐一退出
for room in "ROOM_ID_1" "ROOM_ID_2"; do
  curl -s -X POST "https://YOUR_HOMESERVER:PORT/_matrix/client/r0/rooms/$room/leave" \
    -H "Authorization: Bearer $TOKEN"
done
```

### 6. 检查状态

```bash
openclaw channels status --probe
openclaw logs | grep -i matrix
```

## 诊断命令

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看整体状态 |
| `openclaw channels status` | 查看渠道状态 |
| `openclaw channels status --probe` | 探测渠道连通性 |
| `openclaw logs 2>&1 \| grep -i matrix` | 查看 Matrix 日志 |

## 配置示例

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://YOUR_HOMESERVER:PORT",
      "userId": "@YOUR_BOT_USER_ID",
      "password": "YOUR_PASSWORD",
      "deviceName": "YOUR_DEVICE_NAME",
      "encryption": true
    }
  }
}
```
