/**
 * UDPTransport - UDP 传输层
 * 局域网发现、直连、广播
 */

import { createSocket, Socket, RemoteInfo } from 'dgram';
import { EventEmitter } from 'events';
import type { Envelope, NodeAddress, TransportStats } from '../types.js';

interface UDPPeer {
  nodeId: string;
  addr: NodeAddress;
  lastSeen: number;
}

export class UDPTransport extends EventEmitter {
  private socket: Socket | null = null;
  private port: number;
  private broadcast: boolean;
  private peers: Map<string, UDPPeer> = new Map();
  private stats: TransportStats;
  private announceTimer: NodeJS.Timeout | null = null;
  private identity: { nodeId: string; name: string; addrs: NodeAddress[] } | null = null;

  constructor(port: number = 37291, broadcast: boolean = true) {
    super();
    this.port = port;
    this.broadcast = broadcast;
    this.stats = {
      type: 'udp',
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
   * 启动 UDP 服务
   */
  async start(identity: { nodeId: string; name: string; addrs: NodeAddress[] }): Promise<void> {
    this.identity = identity;

    return new Promise((resolve, reject) => {
      this.socket = createSocket('udp4');

      // 错误处理
      this.socket.on('error', (err) => {
        console.error('UDP Error:', err);
        this.emit('error', err);
        reject(err);
      });

      // 消息处理
      this.socket.on('message', (msg, rinfo) => {
        this.handleMessage(msg, rinfo);
      });

      // 绑定端口
      this.socket.bind(this.port, () => {
        if (this.socket) {
          // 启用广播
          if (this.broadcast) {
            this.socket.setBroadcast(true);
          }
          
          this.stats.connected = true;
          console.log(`✓ UDP 服务启动: 0.0.0.0:${this.port}`);
          
          // 开始定期宣告
          this.startAnnouncing();
          
          resolve();
        }
      });
    });
  }

  /**
   * 停止 UDP 服务
   */
  stop(): void {
    if (this.announceTimer) {
      clearInterval(this.announceTimer);
      this.announceTimer = null;
    }

    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.stats.connected = false;
      console.log('✓ UDP 服务已停止');
    }
  }

  /**
   * 发送消息到指定地址
   */
  async send(msg: Envelope, addr: NodeAddress): Promise<void> {
    if (!this.socket) return;

    const data = Buffer.from(JSON.stringify(msg));
    
    return new Promise((resolve, reject) => {
      this.socket!.send(data, addr.port, addr.ip, (err) => {
        if (err) {
          reject(err);
        } else {
          this.stats.bytesSent += data.length;
          this.stats.messagesSent++;
          this.stats.lastActivity = Date.now();
          resolve();
        }
      });
    });
  }

  /**
   * 广播消息到局域网
   */
  async broadcast(msg: Envelope): Promise<void> {
    if (!this.socket || !this.broadcast) return;

    const data = Buffer.from(JSON.stringify(msg));
    
    return new Promise((resolve, reject) => {
      this.socket!.send(data, this.port, '255.255.255.255', (err) => {
        if (err) {
          reject(err);
        } else {
          this.stats.bytesSent += data.length;
          this.stats.messagesSent++;
          this.stats.lastActivity = Date.now();
          resolve();
        }
      });
    });
  }

  /**
   * 处理收到的消息
   */
  private handleMessage(msg: Buffer, rinfo: RemoteInfo): void {
    this.stats.bytesReceived += msg.length;
    this.stats.messagesReceived++;
    this.stats.lastActivity = Date.now();

    try {
      const envelope: Envelope = JSON.parse(msg.toString());
      
      // 标记为 UDP 传输
      envelope._transport = 'udp';
      envelope._receivedAt = Date.now();

      // 更新对等节点信息
      if (envelope.from.nodeId) {
        this.updatePeer(envelope.from.nodeId, {
          ip: rinfo.address,
          port: rinfo.port,
          type: 'local',
        });
      }

      // 处理发现消息
      if (envelope.payload.type === 'announce') {
        this.handleAnnounce(envelope);
      }

      // 转发给上层
      this.emit('message', envelope);
    } catch (e) {
      // 解析错误，忽略
    }
  }

  /**
   * 处理宣告消息
   */
  private handleAnnounce(envelope: Envelope): void {
    const data = envelope.payload.data as {
      nodeId: string;
      name: string;
      addrs: NodeAddress[];
      capabilities: string[];
    };

    if (data && data.nodeId !== this.identity?.nodeId) {
      // 更新对等节点
      data.addrs.forEach(addr => {
        this.updatePeer(data.nodeId, addr);
      });

      // 触发发现事件
      this.emit('peer:discover', {
        nodeId: data.nodeId,
        name: data.name,
        addrs: data.addrs,
        capabilities: data.capabilities,
        source: 'udp_broadcast',
      });
    }
  }

  /**
   * 开始定期宣告
   */
  private startAnnouncing(interval: number = 5000): void {
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
    if (!this.socket || !this.identity) return;

    const envelope: Envelope = {
      version: '2.0',
      msgId: `announce-${Date.now()}`,
      timestamp: Date.now(),
      ttl: 1,
      from: {
        nodeId: this.identity.nodeId,
        addrs: this.identity.addrs,
      },
      to: {
        type: 'broadcast',
      },
      payload: {
        type: 'announce',
        data: {
          nodeId: this.identity.nodeId,
          name: this.identity.name,
          addrs: this.identity.addrs,
          capabilities: ['chat', 'file', 'gossip'],
        },
      },
    };

    try {
      await this.broadcast(envelope);
    } catch (e) {
      // 忽略广播错误
    }
  }

  /**
   * 更新对等节点
   */
  private updatePeer(nodeId: string, addr: NodeAddress): void {
    this.peers.set(nodeId, {
      nodeId,
      addr,
      lastSeen: Date.now(),
    });
    this.stats.peers = this.peers.size;
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
  getPeers(): UDPPeer[] {
    return Array.from(this.peers.values());
  }

  /**
   * 清理过期节点
   */
  cleanupPeers(maxAge: number = 60000): void {
    const now = Date.now();
    for (const [nodeId, peer] of this.peers.entries()) {
      if (now - peer.lastSeen > maxAge) {
        this.peers.delete(nodeId);
      }
    }
    this.stats.peers = this.peers.size;
  }
}
