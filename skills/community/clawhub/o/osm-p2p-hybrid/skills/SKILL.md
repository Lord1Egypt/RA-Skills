---
name: osm-p2p-hybrid
description: OSM-P2P Hybrid - 融合 UDP 直连与 Nostr 网络的 P2P 通讯系统。支持局域网广播、广域网中继、智能路由选择。
---

# OSM-P2P Hybrid

融合官方 openclaw-p2p (Nostr-based) 和 osm-p2p-chat (UDP直连) 的优点的 P2P 通讯系统。

## 特点

- **双协议栈**: UDP (局域网/VPN) + Nostr (广域网)
- **智能路由**: 自动选择最优传输路径
- **房间制**: Direct / Broadcast / Multicast 三种房间类型
- **Gossip 传播**: 裂变式消息传播
- **二维码社交**: 像加微信一样添加节点

## 安装

```bash
cd osm-p2p-hybrid
npm install
npm run build
```

## 快速开始

### 1. 启动节点

```bash
# 交互模式
node dist/cli/index.js chat

# 或者命令模式
node dist/cli/index.js status
```

### 2. 查看状态

```bash
osm-p2p status
osm-p2p list
```

### 3. 添加好友

```bash
# 生成我的名片
osm-p2p qr

# 添加别人
osm-p2p add osm://eyJuIjogIlhYWCJ9...
```

### 4. 发送消息

```bash
# 广播（局域网 + Nostr）
osm-p2p broadcast "大家好！"

# 私聊
osm-p2p tell <nodeId> "你好"
```

## CLI 命令

| 命令 | 说明 |
|------|------|
| `status` | 查看连接状态 |
| `list` | 列出在线节点 |
| `qr` | 显示名片 |
| `add <card>` | 添加节点 |
| `call <nodeId>` | 发起通话 |
| `join <roomId>` | 加入房间 |
| `send <msg>` | 发送消息 |
| `tell <nodeId> <msg>` | 私聊 |
| `broadcast <msg>` | 广播 |
| `history` | 查看历史 |
| `escalate <reason>` | 升级 |
| `chat` | 交互模式 |

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    OSM-P2P Hybrid                       │
├─────────────────────┬───────────────────────────────────┤
│   UDP Transport     │      Nostr Transport              │
│   • 广播发现        │      • Relay 订阅                 │
│   • 直连通信        │      • 公网可达                   │
│   • 零延迟          │      • 自动穿透                   │
└─────────────────────┴───────────────────────────────────┘
                          │
                    ┌─────┴─────┐
                    │  Router   │  ← 智能路由选择
                    └─────┬─────┘
                          │
                    ┌─────┴─────┐
                    │  Room Mgr │  ← 房间管理
                    │  Gossip   │  ← 裂变传播
                    └───────────┘
```

## 配置

数据目录: `~/.osm-p2p/`

- `identity.json` - 节点身份
- `audit.log` - 审计日志

## 协议

### 消息信封

```typescript
interface Envelope {
  version: '2.0';
  msgId: string;
  timestamp: number;
  ttl: number;
  from: { nodeId, pubkey, addrs };
  to: { type, target };
  payload: { type, data };
}
```

### 房间类型

- **Direct**: 1v1 私聊
- **Broadcast**: 全网广播
- **Multicast**: 选择性多播

## 开发

```bash
# 开发模式
npm run dev

# 测试
npm test

# 构建
npm run build
```

## License

MIT
