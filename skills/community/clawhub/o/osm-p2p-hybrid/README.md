# OSM-P2P Hybrid

> 融合 UDP 直连与 Nostr 网络的 P2P 通讯系统

## 核心特性

| 特性 | 说明 |
|------|------|
| **双协议栈** | UDP (局域网/VPN) + Nostr (广域网) |
| **智能路由** | 自动选择最优传输路径 |
| **三层发现** | UDP广播 + 打洞 + Nostr Relay |
| **房间制** | Direct / Broadcast / Multicast |
| **Gossip** | 裂变传播，限频去重 |

## 快速开始

```bash
# 安装依赖
npm install

# 构建
npm run build

# 启动交互模式
npm start chat
```

## 目录结构

```
osm-p2p-hybrid/
├── src/
│   ├── core/
│   │   ├── TransportManager.ts    # 传输管理器
│   │   ├── RoomManager.ts         # 房间管理
│   │   ├── DiscoveryService.ts    # 发现服务
│   │   ├── GossipEngine.ts        # Gossip 传播
│   │   └── AuditLogger.ts         # 审计日志
│   ├── transport/
│   │   ├── UDPTransport.ts        # UDP 传输
│   │   └── NostrTransport.ts      # Nostr 传输
│   ├── crypto/
│   │   └── IdentityManager.ts     # 身份管理
│   ├── utils/
│   │   └── network.ts             # 网络工具
│   ├── cli/
│   │   └── index.ts               # CLI 入口
│   ├── types.ts                   # 类型定义
│   └── index.ts                   # 主应用类
├── skills/SKILL.md                # OpenClaw Skill 文档
├── package.json
├── tsconfig.json
└── README.md
```

## 架构对比

```
原 osm-p2p-chat          官方 openclaw-p2p          OSM-P2P Hybrid
├─ UDP 广播               ├─ Nostr Relay            ├─ UDP + Nostr 双轨
├─ 直连 P2P               ├─ 房间制                 ├─ 智能路由选择
├─ Gossip 传播            ├─ 端到端加密             ├─ 三层发现
├─ 二维码社交             ├─ 审计日志               ├─ 保留所有优点
└─ VIP 加密               └─ 升级机制               └─ 无缝融合
```

## CLI 使用

```bash
# 基础
osm-p2p status              # 查看状态
osm-p2p list                # 列出节点
osm-p2p qr                  # 显示名片

# 发现
osm-p2p add <名片>          # 添加节点

# 通讯
osm-p2p call <nodeId>       # 发起通话
osm-p2p send <msg>          # 发送消息
osm-p2p broadcast <msg>     # 广播
osm-p2p tell <nodeId> <msg> # 私聊

# 交互
osm-p2p chat                # 交互模式
```

## API 使用

```typescript
import { OSMP2P } from './src/index.js';

const app = new OSMP2P({
  node: {
    name: '我的节点',
    capabilities: ['chat', 'file'],
  },
});

await app.start();

// 创建房间
const room = app.createRoom('broadcast', '聊天室');

// 发送消息
await app.sendMessage('大家好！');

// 广播
await app.broadcast('全网广播');
```

## 融合设计亮点

### 1. 智能路由
```typescript
// 自动选择传输层
if (目标在局域网)  → UDP (零延迟)
if (目标在广域网)  → Nostr (稳定)
if (不确定)        → 两者都试
```

### 2. 保留广播
```typescript
// 广播房间类型
app.createRoom('broadcast');
app.broadcast('消息', { useNostr: true });  // UDP + Nostr
```

### 3. 三层发现
```
Layer 1: UDP 广播 (局域网 < 1ms)
Layer 2: UDP 打洞 (跨网络 ~50ms)  
Layer 3: Nostr Relay (全球 ~200ms)
```

### 4. Gossip 优化
```typescript
// 智能传播策略
strategy: 'smart'  // 优先邻居 + 信誉排序
maxNeighbors: 10     // 限制传播范围
defaultTTL: 5       // 限制跳数
```

## 技术栈

- **TypeScript** - 类型安全
- **Nostr Tools** - Nostr 协议
- **dgram** - UDP 通信
- **EventEmitter** - 事件驱动

## 待办

- [ ] STUN/TURN 打洞完整实现
- [ ] 文件传输 (分片 + 断点续传)
- [ ] WebRTC 音视频通话
- [ ] VIP 加密模式 (AES-256)
- [ ] 群组治理 (投票、仲裁)

## License

MIT
