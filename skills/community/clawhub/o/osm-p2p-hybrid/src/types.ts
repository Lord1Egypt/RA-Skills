/**
 * OSM-P2P Hybrid - 类型定义
 * 融合 UDP 直连与 Nostr 网络的统一类型系统
 */

// ============================================
// 基础类型
// ============================================

export interface NodeAddress {
  ip: string;
  port: number;
  type: 'local' | 'vpn' | 'public';
}

export interface NodeIdentity {
  nodeId: string;
  name: string;
  avatar?: string;
  
  // Nostr 身份
  nostr?: {
    pubkey: string;
    privateKey: Uint8Array;
  };
  
  // UDP 身份（VIP 加密用）
  udp?: {
    key: Uint8Array;
  };
  
  // 地址列表
  addrs: NodeAddress[];
  
  // 能力声明
  capabilities: string[];
  
  // 元数据
  version: string;
  lastSeen: number;
}

// ============================================
// 信封与消息
// ============================================

export interface Envelope {
  version: '2.0';
  msgId: string;
  timestamp: number;
  ttl: number;
  
  from: {
    nodeId: string;
    pubkey?: string;
    addrs: NodeAddress[];
  };
  
  to: {
    type: 'direct' | 'broadcast' | 'room' | 'multicast';
    target?: string;
    targets?: string[];
  };
  
  payload: Payload;
  
  // 传输层信息（内部使用）
  _transport?: 'udp' | 'nostr';
  _receivedAt?: number;
}

export interface Payload {
  type: MessageType;
  data: unknown;
}

export type MessageType =
  // 发现层
  | 'announce'
  | 'discover'
  | 'discover_resp'
  
  // 房间层
  | 'call_request'
  | 'call_accept'
  | 'call_reject'
  | 'call_end'
  | 'room_join'
  | 'room_leave'
  | 'room_message'
  | 'room_file'
  
  // 升级层
  | 'escalate'
  
  // Gossip 层
  | 'gossip_announce'
  | 'gossip_message';

// ============================================
// 房间系统
// ============================================

export type RoomType = 'direct' | 'broadcast' | 'multicast';

export interface Room {
  id: string;
  type: RoomType;
  topic?: string;
  
  // 参与者
  peers: Map<string, RoomPeer>;
  
  // 创建者
  creator: string;
  
  // 传输配置
  transport: RoomTransport;
  
  // 消息历史
  messages: RoomMessage[];
  
  // 元数据
  createdAt: number;
  updatedAt: number;
  expiresAt?: number;
}

export interface RoomPeer {
  nodeId: string;
  pubkey?: string;
  role: 'creator' | 'admin' | 'member';
  joinedAt: number;
  lastActivity: number;
}

export interface RoomTransport {
  primary: 'udp' | 'nostr';
  fallback: 'nostr' | null;
  allowRelay: boolean;
}

export interface RoomMessage {
  id: string;
  roomId: string;
  sender: string;
  type: 'text' | 'file' | 'system';
  content: string;
  meta?: {
    filename?: string;
    size?: number;
    mimeType?: string;
  };
  timestamp: number;
  transport: 'udp' | 'nostr';
}

// ============================================
// 传输层
// ============================================

export interface TransportConfig {
  // UDP 配置
  udp: {
    enabled: boolean;
    port: number;
    broadcast: boolean;
    multicastAddr?: string;
  };
  
  // Nostr 配置
  nostr: {
    enabled: boolean;
    relays: string[];
    announceInterval: number;
  };
  
  // VIP 配置
  vip?: {
    enabled: boolean;
    key: string;
    port: number;
  };
}

export interface TransportStats {
  type: 'udp' | 'nostr';
  connected: boolean;
  peers: number;
  bytesSent: number;
  bytesReceived: number;
  messagesSent: number;
  messagesReceived: number;
  lastActivity: number;
}

// ============================================
// 发现层
// ============================================

export interface PeerInfo {
  nodeId: string;
  name: string;
  pubkey?: string;
  addrs: NodeAddress[];
  capabilities: string[];
  
  // 可达性
  udpReachable: boolean;
  nostrReachable: boolean;
  
  // 发现来源
  source: 'udp_broadcast' | 'udp_punch' | 'nostr' | 'manual' | 'gossip';
  
  // 元数据
  lastSeen: number;
  firstSeen: number;
  rtt?: number;
  
  // 信誉
  reputation: number;
}

export interface DiscoveryConfig {
  // UDP 发现
  udpBroadcast: boolean;
  udpBroadcastInterval: number;
  
  // Nostr 发现
  nostrAnnounce: boolean;
  nostrAnnounceInterval: number;
  
  // 打洞
  holePunch: boolean;
  stunServers: string[];
}

// ============================================
// Gossip 层
// ============================================

export interface GossipConfig {
  enabled: boolean;
  maxNeighbors: number;
  defaultTTL: number;
  
  // 传播策略
  strategy: 'flood' | 'random' | 'smart';
  
  // 限频
  rateLimitPerPeer: number;
  rateLimitWindow: number;
}

// ============================================
// 审计日志
// ============================================

export interface AuditLogEntry {
  ts: number;
  dir: 'in' | 'out';
  peer: string;
  room?: string;
  type: MessageType;
  content: string;
  transport: 'udp' | 'nostr';
  size: number;
}

// ============================================
// 应用配置
// ============================================

export interface AppConfig {
  node: {
    id: string;
    name: string;
    capabilities: string[];
    dataDir: string;
  };
  
  transport: TransportConfig;
  discovery: DiscoveryConfig;
  gossip: GossipConfig;
  
  // 审计
  audit: {
    enabled: boolean;
    logPath: string;
  };
  
  // 升级
  escalation: {
    ownerChannel?: string;
    autoEscalateOnError: boolean;
  };
}

// ============================================
// CLI 类型
// ============================================

export interface CLICommand {
  name: string;
  description: string;
  args: { name: string; required: boolean; description: string }[];
  options: { flag: string; description: string; default?: string }[];
  handler: (args: string[], opts: Record<string, string>) => Promise<void>;
}

// ============================================
// 名片格式 (osm:// URL)
// ============================================

export interface NodeCard {
  n: string;        // name
  i: string[];      // ips
  p: number;        // port
  pub?: string;     // nostr pubkey
  pubp?: number;    // vip port
}
