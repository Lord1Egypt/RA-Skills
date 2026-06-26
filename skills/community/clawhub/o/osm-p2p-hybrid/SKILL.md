---
name: osm-p2p-hybrid
description: OSM-P2P Hybrid - 融合 UDP 直连与 Nostr 网络的 P2P 通讯系统
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
npm install
npm run build
```

## 快速开始

### 启动节点

```bash
# 交互模式
node dist/cli/index.js chat

# 或者命令模式
node dist/cli/index.js status
```

### 查看状态

```bash
osm-p2p status
osm-p2p list
```

### 添加好友

```bash
# 生成我的名片
osm-p2p qr

# 添加别人
osm-p2p add osm://...
```

### 发送消息

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
| `broadcast <msg>` | 广播 |
| `chat` | 交互模式 |

## License

MIT
