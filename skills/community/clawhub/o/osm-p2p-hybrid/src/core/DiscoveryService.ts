/**
 * DiscoveryService - 发现服务
 * 三层发现：UDP广播 + 打洞 + Nostr
 */

import { EventEmitter } from 'events';
import type { DiscoveryConfig, PeerInfo, NodeAddress, Envelope } from '../types.js';

interface HolePunchSession {
  targetId: string;
  startedAt: number;
  attempts: number;
  resolved: boolean;
}

export class DiscoveryService extends EventEmitter {
  private config: DiscoveryConfig;
  private peers: Map<string, PeerInfo> = new Map();
  private holePunchSessions: Map<string, HolePunchSession> = new Map();
  private stunServers: string[];
  private discoveryTimer: NodeJS.Timeout | null = null;

  constructor(config?: Partial<DiscoveryConfig>) {
    super();
    
    this.config = {
      udpBroadcast: true,
      udpBroadcastInterval: 5000,
      nostrAnnounce: true,
      nostrAnnounceInterval: 120000,
      holePunch: true,
      stunServers: [
        'stun.l.google.com:19302',
        'stun1.l.google.com:19302',
      ],
      ...config,
    };

    this.stunServers = this.config.stunServers;
  }

  /**
   * 处理 UDP 发现
   */
  handleUDPDiscovery(envelope: Envelope, rinfo: { address: string; port: number }): void {
    const data = envelope.payload.data as {
      nodeId: string;
      name: string;
      addrs: NodeAddress[];
      capabilities: string[];
    };

    if (!data || !data.nodeId) return;

    const existing = this.peers.get(data.nodeId);
    
    if (existing) {
      // 更新现有节点
      existing.udpReachable = true;
      existing.lastSeen = Date.now();
      
      // 合并地址
      const newAddrs = data.addrs.filter(a => 
        !existing.addrs.some(ea => ea.ip === a.ip && ea.port === a.port)
      );
      existing.addrs.push(...newAddrs);
      
      // 合并能力
      data.capabilities.forEach(cap => {
        if (!existing.capabilities.includes(cap)) {
          existing.capabilities.push(cap);
        }
      });
    } else {
      // 添加新节点
      const peer: PeerInfo = {
        nodeId: data.nodeId,
        name: data.name,
        addrs: [
          ...data.addrs,
          { ip: rinfo.address, port: rinfo.port, type: 'local' },
        ],
        capabilities: data.capabilities,
        udpReachable: true,
        nostrReachable: false,
        source: 'udp_broadcast',
        lastSeen: Date.now(),
        firstSeen: Date.now(),
        reputation: 0,
      };

      this.peers.set(data.nodeId, peer);
      this.emit('peer:discovered', peer);
    }
  }

  /**
   * 处理 Nostr 发现
   */
  handleNostrDiscovery(event: { pubkey: string; content: string }): void {
    try {
      const data = JSON.parse(event.content);
      
      if (!data || !data.nodeId) return;

      const existing = this.peers.get(data.nodeId);
      
      if (existing) {
        existing.nostrReachable = true;
        existing.lastSeen = Date.now();
        if (data.pubkey) {
          existing.pubkey = data.pubkey;
        }
      } else {
        const peer: PeerInfo = {
          nodeId: data.nodeId,
          name: data.name,
          pubkey: data.pubkey || event.pubkey,
          addrs: data.addrs || [],
          capabilities: data.capabilities || [],
          udpReachable: false,
          nostrReachable: true,
          source: 'nostr',
          lastSeen: Date.now(),
          firstSeen: Date.now(),
          reputation: 0,
        };

        this.peers.set(data.nodeId, peer);
        this.emit('peer:discovered', peer);

        // 尝试打洞（如果启用了）
        if (this.config.holePunch && data.addrs?.length > 0) {
          this.attemptHolePunch(peer);
        }
      }
    } catch (e) {
      // 解析错误，忽略
    }
  }

  /**
   * 尝试 UDP 打洞
   */
  private async attemptHolePunch(peer: PeerInfo): Promise<void> {
    // 简单打洞实现
    // 实际实现需要 STUN/TURN 服务器协调
    
    const session: HolePunchSession = {
      targetId: peer.nodeId,
      startedAt: Date.now(),
      attempts: 0,
      resolved: false,
    };

    this.holePunchSessions.set(peer.nodeId, session);

    // 发送打洞探测包
    // 这里简化实现，实际需要更复杂的协调
    this.emit('holepunch:attempt', peer);
  }

  /**
   * 获取公网 IP（通过 STUN）
   */
  async getPublicIP(): Promise<string | null> {
    // 简化实现，实际需要 STUN 客户端
    // 可以使用 stun 包：https://www.npmjs.com/package/stun
    
    // 暂时返回 null，表示需要手动配置
    return null;
  }

  /**
   * 手动添加节点（通过名片）
   */
  addPeerFromCard(card: { n: string; i: string[]; p: number; pub?: string; pubp?: number }): PeerInfo | null {
    const addrs: NodeAddress[] = card.i.map(ip => ({
      ip,
      port: card.p,
      type: ip.startsWith('100.') || ip.startsWith('10.') || ip.startsWith('192.168.') 
        ? 'local' 
        : 'vpn',
    }));

    const peer: PeerInfo = {
      nodeId: card.n,
      name: card.n,
      pubkey: card.pub,
      addrs,
      capabilities: ['chat', 'file'],
      udpReachable: true,
      nostrReachable: !!card.pub,
      source: 'manual',
      lastSeen: Date.now(),
      firstSeen: Date.now(),
      reputation: 10, // 手动添加的节点初始信誉较高
    };

    this.peers.set(card.n, peer);
    this.emit('peer:added', peer);
    
    return peer;
  }

  /**
   * 获取对等节点
   */
  getPeer(nodeId: string): PeerInfo | undefined {
    return this.peers.get(nodeId);
  }

  /**
   * 获取所有对等节点
   */
  getAllPeers(): PeerInfo[] {
    return Array.from(this.peers.values());
  }

  /**
   * 按来源获取对等节点
   */
  getPeersBySource(source: PeerInfo['source']): PeerInfo[] {
    return Array.from(this.peers.values()).filter(p => p.source === source);
  }

  /**
   * 清理过期节点
   */
  cleanup(maxAge: number = 300000): void {
    const now = Date.now();
    
    for (const [nodeId, peer] of this.peers.entries()) {
      if (now - peer.lastSeen > maxAge) {
        // UDP 节点过期较快
        if (peer.source === 'udp_broadcast' && !peer.nostrReachable) {
          this.peers.delete(nodeId);
          this.emit('peer:expired', peer);
        }
      }
    }
  }

  /**
   * 获取网络拓扑统计
   */
  getTopologyStats(): {
    total: number;
    udpOnly: number;
    nostrOnly: number;
    both: number;
    bySource: Record<string, number>;
  } {
    const peers = Array.from(this.peers.values());
    
    return {
      total: peers.length,
      udpOnly: peers.filter(p => p.udpReachable && !p.nostrReachable).length,
      nostrOnly: peers.filter(p => !p.udpReachable && p.nostrReachable).length,
      both: peers.filter(p => p.udpReachable && p.nostrReachable).length,
      bySource: {
        udp_broadcast: peers.filter(p => p.source === 'udp_broadcast').length,
        nostr: peers.filter(p => p.source === 'nostr').length,
        manual: peers.filter(p => p.source === 'manual').length,
        gossip: peers.filter(p => p.source === 'gossip').length,
      },
    };
  }
}
