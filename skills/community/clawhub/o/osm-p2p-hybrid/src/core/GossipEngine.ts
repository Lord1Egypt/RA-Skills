/**
 * GossipEngine - Gossip 传播引擎
 * 裂变传播，限频，去重
 */

import { EventEmitter } from 'events';
import type { Envelope, GossipConfig, PeerInfo } from '../types.js';

interface GossipMessage {
  envelope: Envelope;
  receivedAt: number;
  forwarded: boolean;
  forwardCount: number;
}

interface GossipPeer {
  nodeId: string;
  reputation: number;
  lastMessageAt: number;
  messageCount: number;
}

export class GossipEngine extends EventEmitter {
  private config: GossipConfig;
  private seenMessages: Map<string, GossipMessage> = new Map();
  private peers: Map<string, GossipPeer> = new Map();
  private neighbors: Set<string> = new Set();
  private cleanupTimer: NodeJS.Timeout | null = null;

  constructor(config?: Partial<GossipConfig>) {
    super();
    
    this.config = {
      enabled: true,
      maxNeighbors: 10,
      defaultTTL: 5,
      strategy: 'smart',
      rateLimitPerPeer: 10,
      rateLimitWindow: 60000,
      ...config,
    };

    // 启动定期清理
    this.startCleanup();
  }

  /**
   * 处理收到的消息，决定是否传播
   */
  shouldGossip(envelope: Envelope, fromPeer: string): boolean {
    if (!this.config.enabled) return false;

    // 1. 检查是否已见过（去重）
    if (this.seenMessages.has(envelope.msgId)) {
      return false;
    }

    // 2. TTL 检查
    if (envelope.ttl <= 0) {
      return false;
    }

    // 3. 限频检查
    if (this.isRateLimited(fromPeer)) {
      return false;
    }

    // 4. 信誉检查
    const peer = this.peers.get(fromPeer);
    if (peer && peer.reputation < -50) {
      return false;
    }

    return true;
  }

  /**
   * 记录消息并选择传播目标
   */
  gossip(envelope: Envelope, allPeers: PeerInfo[]): string[] {
    // 记录已见
    this.seenMessages.set(envelope.msgId, {
      envelope,
      receivedAt: Date.now(),
      forwarded: false,
      forwardCount: 0,
    });

    // 根据策略选择邻居
    const targets = this.selectTargets(envelope, allPeers);

    // 更新转发记录
    const record = this.seenMessages.get(envelope.msgId);
    if (record) {
      record.forwarded = true;
      record.forwardCount = targets.length;
    }

    return targets;
  }

  /**
   * 创建传播用的 envelope（TTL-1）
   */
  createGossipEnvelope(original: Envelope): Envelope {
    return {
      ...original,
      msgId: `${original.msgId}-gossip-${Date.now()}`,
      ttl: original.ttl - 1,
      payload: {
        type: 'gossip_message',
        data: original.payload,
      },
    };
  }

  /**
   * 添加邻居
   */
  addNeighbor(nodeId: string): void {
    if (this.neighbors.size < this.config.maxNeighbors) {
      this.neighbors.add(nodeId);
    }
  }

  /**
   * 移除邻居
   */
  removeNeighbor(nodeId: string): void {
    this.neighbors.delete(nodeId);
  }

  /**
   * 更新对等节点信誉
   */
  updateReputation(nodeId: string, delta: number): void {
    const peer = this.peers.get(nodeId);
    if (peer) {
      peer.reputation += delta;
    } else {
      this.peers.set(nodeId, {
        nodeId,
        reputation: delta,
        lastMessageAt: Date.now(),
        messageCount: 1,
      });
    }
  }

  /**
   * 记录消息接收
   */
  recordReceive(nodeId: string): void {
    const peer = this.peers.get(nodeId);
    if (peer) {
      peer.lastMessageAt = Date.now();
      peer.messageCount++;
    } else {
      this.peers.set(nodeId, {
        nodeId,
        reputation: 0,
        lastMessageAt: Date.now(),
        messageCount: 1,
      });
    }
  }

  /**
   * 选择传播目标
   */
  private selectTargets(envelope: Envelope, allPeers: PeerInfo[]): string[] {
    const strategy = this.config.strategy;
    
    switch (strategy) {
      case 'flood':
        return this.floodStrategy(allPeers);
      case 'random':
        return this.randomStrategy(allPeers);
      case 'smart':
      default:
        return this.smartStrategy(envelope, allPeers);
    }
  }

  /**
   * 泛洪策略 - 传给所有可达节点（除了来源）
   */
  private floodStrategy(allPeers: PeerInfo[]): string[] {
    return allPeers
      .filter(p => p.udpReachable || p.nostrReachable)
      .map(p => p.nodeId);
  }

  /**
   * 随机策略 - 随机选择最多 maxNeighbors 个
   */
  private randomStrategy(allPeers: PeerInfo[]): string[] {
    const candidates = allPeers.filter(p => p.udpReachable || p.nostrReachable);
    const shuffled = candidates.sort(() => Math.random() - 0.5);
    return shuffled.slice(0, this.config.maxNeighbors).map(p => p.nodeId);
  }

  /**
   * 智能策略 - 基于网络拓扑和信誉选择
   */
  private smartStrategy(envelope: Envelope, allPeers: PeerInfo[]): string[] {
    // 1. 优先选择已知邻居
    const neighborTargets = Array.from(this.neighbors)
      .filter(id => allPeers.some(p => p.nodeId === id));

    // 2. 补充随机节点到 maxNeighbors
    if (neighborTargets.length < this.config.maxNeighbors) {
      const otherPeers = allPeers
        .filter(p => !this.neighbors.has(p.nodeId))
        .filter(p => p.udpReachable || p.nostrReachable)
        .sort((a, b) => (b.reputation || 0) - (a.reputation || 0)); // 优先高信誉

      const needed = this.config.maxNeighbors - neighborTargets.length;
      const additional = otherPeers.slice(0, needed).map(p => p.nodeId);
      
      return [...neighborTargets, ...additional];
    }

    return neighborTargets;
  }

  /**
   * 检查是否限频
   */
  private isRateLimited(nodeId: string): boolean {
    const peer = this.peers.get(nodeId);
    if (!peer) return false;

    const now = Date.now();
    const window = this.config.rateLimitWindow;
    const limit = this.config.rateLimitPerPeer;

    // 如果超出时间窗口，重置计数
    if (now - peer.lastMessageAt > window) {
      peer.messageCount = 0;
      return false;
    }

    return peer.messageCount > limit;
  }

  /**
   * 启动定期清理
   */
  private startCleanup(): void {
    this.cleanupTimer = setInterval(() => {
      this.cleanup();
    }, 60000); // 每分钟清理一次
  }

  /**
   * 清理过期数据
   */
  private cleanup(): void {
    const now = Date.now();
    
    // 清理看过的消息（保留10分钟）
    for (const [msgId, msg] of this.seenMessages.entries()) {
      if (now - msg.receivedAt > 600000) {
        this.seenMessages.delete(msgId);
      }
    }

    // 清理不活跃的对等节点
    for (const [nodeId, peer] of this.peers.entries()) {
      if (now - peer.lastMessageAt > 3600000) { // 1小时
        this.peers.delete(nodeId);
        this.neighbors.delete(nodeId);
      }
    }
  }

  /**
   * 停止引擎
   */
  stop(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = null;
    }
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    seenMessages: number;
    peers: number;
    neighbors: number;
  } {
    return {
      seenMessages: this.seenMessages.size,
      peers: this.peers.size,
      neighbors: this.neighbors.size,
    };
  }
}
