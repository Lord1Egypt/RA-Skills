/**
 * TransportManager - 传输管理器
 * 管理 UDP 和 Nostr 双协议栈，智能路由选择
 */

import { EventEmitter } from 'events';
import { UDPTransport } from './UDPTransport.js';
import { NostrTransport } from './NostrTransport.js';
import type {
  Envelope,
  NodeAddress,
  TransportConfig,
  TransportStats,
  PeerInfo,
} from '../types.js';

interface RouteInfo {
  type: 'udp' | 'nostr';
  priority: number;
  available: boolean;
}

export class TransportManager extends EventEmitter {
  private udp: UDPTransport | null = null;
  private nostr: NostrTransport | null = null;
  private config: TransportConfig;
  private identity: { nodeId: string; name: string; privateKey: Uint8Array; addrs: NodeAddress[] } | null = null;
  private peers: Map<string, PeerInfo> = new Map();

  constructor(config: TransportConfig) {
    super();
    this.config = config;
  }

  /**
   * 启动传输层
   */
  async start(identity: {
    nodeId: string;
    name: string;
    privateKey: Uint8Array;
    addrs: NodeAddress[];
  }): Promise<void> {
    this.identity = identity;

    // 启动 UDP
    if (this.config.udp.enabled) {
      this.udp = new UDPTransport(this.config.udp.port, this.config.udp.broadcast);
      
      // 监听消息
      this.udp.on('message', (envelope: Envelope) => {
        this.emit('message', envelope);
      });

      this.udp.on('peer:discover', (peer) => {
        this.addPeer({
          ...peer,
          udpReachable: true,
          nostrReachable: false,
          reputation: 0,
          firstSeen: Date.now(),
        });
      });

      await this.udp.start({
        nodeId: identity.nodeId,
        name: identity.name,
        addrs: identity.addrs,
      });
    }

    // 启动 Nostr
    if (this.config.nostr.enabled) {
      this.nostr = new NostrTransport(this.config.nostr.relays);

      // 监听消息
      this.nostr.on('message', (envelope: Envelope) => {
        this.emit('message', envelope);
      });

      this.nostr.on('peer:discover', (peer) => {
        const existing = this.peers.get(peer.nodeId);
        if (existing) {
          // 更新现有节点
          existing.nostrReachable = true;
          existing.lastSeen = Date.now();
        } else {
          this.addPeer({
            ...peer,
            udpReachable: false,
            nostrReachable: true,
            reputation: 0,
            firstSeen: Date.now(),
          });
        }
      });

      await this.nostr.start({
        nodeId: identity.nodeId,
        name: identity.name,
        privateKey: identity.privateKey,
      });
    }

    console.log('✓ 传输管理器启动完成');
  }

  /**
   * 停止传输层
   */
  stop(): void {
    if (this.udp) {
      this.udp.stop();
      this.udp = null;
    }

    if (this.nostr) {
      this.nostr.stop();
      this.nostr = null;
    }

    console.log('✓ 传输管理器已停止');
  }

  /**
   * 发送消息到指定节点
   */
  async send(envelope: Envelope, targetNodeId: string): Promise<boolean> {
    const route = this.selectRoute(targetNodeId);
    
    if (!route.available) {
      return false;
    }

    try {
      if (route.type === 'udp' && this.udp) {
        const peer = this.peers.get(targetNodeId);
        if (peer?.addrs[0]) {
          await this.udp.send(envelope, peer.addrs[0]);
          return true;
        }
      }

      if (route.type === 'nostr' && this.nostr) {
        const pubkey = this.nostr.lookupPubkey(targetNodeId);
        if (pubkey) {
          await this.nostr.send(envelope, pubkey);
          return true;
        }
      }
    } catch (e) {
      console.error(`发送失败 [${route.type}]:`, e);
    }

    return false;
  }

  /**
   * 广播消息
   */
  async broadcast(envelope: Envelope, useNostr: boolean = true): Promise<void> {
    // UDP 广播（局域网）
    if (this.udp && this.config.udp.broadcast) {
      try {
        await this.udp.broadcast(envelope);
      } catch (e) {
        // 忽略错误
      }
    }

    // Nostr 发布（广域网）
    if (useNostr && this.nostr) {
      try {
        await this.nostr.publish(envelope);
      } catch (e) {
        // 忽略错误
      }
    }
  }

  /**
   * 智能路由选择
   */
  selectRoute(targetNodeId: string): RouteInfo {
    const peer = this.peers.get(targetNodeId);

    // 1. 检查 UDP 可达性（局域网优先）
    if (peer?.udpReachable && peer.addrs.length > 0) {
      return { type: 'udp', priority: 1, available: true };
    }

    // 2. 检查 Nostr 可达性
    if (peer?.nostrReachable && this.nostr) {
      const pubkey = this.nostr.lookupPubkey(targetNodeId);
      if (pubkey) {
        return { type: 'nostr', priority: 2, available: true };
      }
    }

    // 3. 无法路由，尝试 Nostr（如果有 pubkey）
    if (this.nostr) {
      const pubkey = this.nostr.lookupPubkey(targetNodeId);
      if (pubkey) {
        return { type: 'nostr', priority: 3, available: true };
      }
    }

    // 4. 完全无法到达
    return { type: 'nostr', priority: 4, available: false };
  }

  /**
   * 添加对等节点
   */
  addPeer(peer: PeerInfo): void {
    const existing = this.peers.get(peer.nodeId);
    
    if (existing) {
      // 合并信息
      existing.udpReachable = existing.udpReachable || peer.udpReachable;
      existing.nostrReachable = existing.nostrReachable || peer.nostrReachable;
      existing.addrs = [...new Set([...existing.addrs, ...peer.addrs])];
      existing.capabilities = [...new Set([...existing.capabilities, ...peer.capabilities])];
      existing.lastSeen = Date.now();
    } else {
      this.peers.set(peer.nodeId, peer);
    }

    this.emit('peer:update', this.peers.get(peer.nodeId));
  }

  /**
   * 获取对等节点列表
   */
  getPeers(): PeerInfo[] {
    return Array.from(this.peers.values());
  }

  /**
   * 获取统计信息
   */
  getStats(): { udp?: TransportStats; nostr?: TransportStats } {
    return {
      udp: this.udp?.getStats(),
      nostr: this.nostr?.getStats(),
    };
  }

  /**
   * 清理过期节点
   */
  cleanupPeers(): void {
    this.udp?.cleanupPeers();
    this.nostr?.cleanupPeers();

    const now = Date.now();
    for (const [nodeId, peer] of this.peers.entries()) {
      // 超过 5 分钟未见的节点标记为不可达
      if (now - peer.lastSeen > 300000) {
        peer.udpReachable = false;
        
        // Nostr 节点保持更久
        if (!peer.nostrReachable || now - peer.lastSeen > 600000) {
          this.peers.delete(nodeId);
        }
      }
    }
  }
}
