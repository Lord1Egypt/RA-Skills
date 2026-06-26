/**
 * NostrTransport - Nostr 传输层
 * 基于 Nostr 协议的广域网通讯
 */

import { EventEmitter } from 'events';
import {
  SimplePool,
  type Event,
  type Filter,
  getPublicKey,
  getEventHash,
  getSignature,
  finalizeEvent,
} from 'nostr-tools';
import type { Envelope, NodeAddress, TransportStats, Payload } from '../types.js';

interface NostrPeer {
  nodeId: string;
  pubkey: string;
  name: string;
  addrs: NodeAddress[];
  capabilities: string[];
  lastSeen: number;
}

// Nostr Event Kind 定义
const KIND_AGENT_ANNOUNCE = 10002;  // 节点宣告
const KIND_AGENT_MESSAGE = 10003;   // 节点间消息

export class NostrTransport extends EventEmitter {
  private pool: SimplePool | null = null;
  private relays: string[];
  private identity: { nodeId: string; privateKey: Uint8Array; name: string } | null = null;
  private peers: Map<string, NostrPeer> = new Map();
  private stats: TransportStats;
  private announceTimer: NodeJS.Timeout | null = null;
  private subscriptions: (() => void)[] = [];

  constructor(relays: string[] = [
    'wss://relay.damus.io',
    'wss://nos.lol',
    'wss://relay.nostr.band',
  ]) {
    super();
    this.relays = relays;
    this.stats = {
      type: 'nostr',
      connected: false,
      peers: 0,
      bytesSent: 0,
      bytesReceived: 0,
      messagesSent: 0,
      messagesReceived: 0,
      lastActivity: 0,
    };
  }

  /**
   * 启动 Nostr 服务
   */
  async start(identity: { nodeId: string; privateKey: Uint8Array; name: string }): Promise<void> {
    this.identity = identity;

    // 创建连接池
    this.pool = new SimplePool();

    // 订阅消息
    await this.subscribeMessages();

    // 开始定期宣告
    this.startAnnouncing();

    this.stats.connected = true;
    console.log(`✓ Nostr 服务启动: ${this.relays.length} 个 relay`);
  }

  /**
   * 停止 Nostr 服务
   */
  stop(): void {
    if (this.announceTimer) {
      clearInterval(this.announceTimer);
      this.announceTimer = null;
    }

    // 取消订阅
    this.subscriptions.forEach(unsub => unsub());
    this.subscriptions = [];

    // 关闭连接池
    if (this.pool) {
      this.pool.close(this.relays);
      this.pool = null;
    }

    this.stats.connected = false;
    console.log('✓ Nostr 服务已停止');
  }

  /**
   * 订阅消息
   */
  private async subscribeMessages(): Promise<void> {
    if (!this.pool || !this.identity) return;

    const pubkey = getPublicKey(this.identity.privateKey);

    // 订阅宣告消息
    const announceFilter: Filter = {
      kinds: [KIND_AGENT_ANNOUNCE],
      since: Math.floor(Date.now() / 1000) - 300,
    };

    const unsubAnnounce = this.pool.subscribeMany(this.relays, [announceFilter], {
      onevent: (event) => {
        this.handleAnnounce(event);
      },
    });

    this.subscriptions.push(unsubAnnounce);

    // 订阅直接消息
    const messageFilter: Filter = {
      kinds: [KIND_AGENT_MESSAGE],
      '#p': [pubkey],  // 标记为发给我们的
      since: Math.floor(Date.now() / 1000) - 60,
    };

    const unsubMessage = this.pool.subscribeMany(this.relays, [messageFilter], {
      onevent: (event) => {
        this.handleMessage(event);
      },
    });

    this.subscriptions.push(unsubMessage);
  }

  /**
   * 发送消息到指定公钥
   */
  async send(msg: Envelope, targetPubkey: string): Promise<void> {
    if (!this.pool || !this.identity) return;

    const event = this.createEvent(
      KIND_AGENT_MESSAGE,
      JSON.stringify(msg),
      [['p', targetPubkey]]
    );

    await this.pool.publish(this.relays, event);
    
    this.stats.messagesSent++;
    this.stats.bytesSent += JSON.stringify(event).length;
    this.stats.lastActivity = Date.now();
  }

  /**
   * 发布事件到全网
   */
  async publish(msg: Envelope): Promise<void> {
    if (!this.pool || !this.identity) return;

    const event = this.createEvent(
      KIND_AGENT_MESSAGE,
      JSON.stringify(msg)
    );

    await this.pool.publish(this.relays, event);
    
    this.stats.messagesSent++;
    this.stats.bytesSent += JSON.stringify(event).length;
    this.stats.lastActivity = Date.now();
  }

  /**
   * 处理宣告消息
   */
  private handleAnnounce(event: Event): void {
    try {
      const data = JSON.parse(event.content);
      
      if (data.nodeId && data.nodeId !== this.identity?.nodeId) {
        // 更新对等节点
        this.peers.set(data.nodeId, {
          nodeId: data.nodeId,
          pubkey: event.pubkey,
          name: data.name,
          addrs: data.addrs || [],
          capabilities: data.capabilities || [],
          lastSeen: Date.now(),
        });
        
        this.stats.peers = this.peers.size;

        // 触发发现事件
        this.emit('peer:discover', {
          nodeId: data.nodeId,
          name: data.name,
          pubkey: event.pubkey,
          addrs: data.addrs,
          capabilities: data.capabilities,
          source: 'nostr',
        });
      }
    } catch (e) {
      // 解析错误，忽略
    }
  }

  /**
   * 处理消息
   */
  private handleMessage(event: Event): void {
    this.stats.messagesReceived++;
    this.stats.bytesReceived += JSON.stringify(event).length;
    this.stats.lastActivity = Date.now();

    try {
      const envelope: Envelope = JSON.parse(event.content);
      
      // 标记为 Nostr 传输
      envelope._transport = 'nostr';
      envelope._receivedAt = Date.now();

      // 转发给上层
      this.emit('message', envelope);
    } catch (e) {
      // 解析错误，忽略
    }
  }

  /**
   * 创建 Nostr 事件
   */
  private createEvent(kind: number, content: string, tags: string[][] = []): Event {
    if (!this.identity) {
      throw new Error('Identity not initialized');
    }

    const eventTemplate = {
      kind,
      created_at: Math.floor(Date.now() / 1000),
      tags,
      content,
    };

    return finalizeEvent(eventTemplate, this.identity.privateKey);
  }

  /**
   * 开始定期宣告
   */
  private startAnnouncing(interval: number = 120000): void {
    if (!this.identity) return;

    // 立即宣告一次
    this.announce();

    // 定期宣告
    this.announceTimer = setInterval(() => {
      this.announce();
    }, interval);
  }

  /**
   * 发送宣告消息
   */
  private async announce(): Promise<void> {
    if (!this.pool || !this.identity) return;

    const pubkey = getPublicKey(this.identity.privateKey);

    const data = {
      nodeId: this.identity.nodeId,
      name: this.identity.name,
      pubkey,
      capabilities: ['chat', 'file', 'gossip'],
    };

    const event = this.createEvent(
      KIND_AGENT_ANNOUNCE,
      JSON.stringify(data)
    );

    try {
      await this.pool.publish(this.relays, event);
    } catch (e) {
      // 忽略发布错误
    }
  }

  /**
   * 获取统计信息
   */
  getStats(): TransportStats {
    return { ...this.stats };
  }

  /**
   * 获取对等节点列表
   */
  getPeers(): NostrPeer[] {
    return Array.from(this.peers.values());
  }

  /**
   * 根据 nodeId 查找公钥
   */
  lookupPubkey(nodeId: string): string | undefined {
    return this.peers.get(nodeId)?.pubkey;
  }

  /**
   * 清理过期节点
   */
  cleanupPeers(maxAge: number = 300000): void {
    const now = Date.now();
    for (const [nodeId, peer] of this.peers.entries()) {
      if (now - peer.lastSeen > maxAge) {
        this.peers.delete(nodeId);
      }
    }
    this.stats.peers = this.peers.size;
  }
}
