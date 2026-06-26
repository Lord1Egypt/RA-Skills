/**
 * OSM-P2P Hybrid - 主应用类
 * 整合所有组件的入口
 */

import { EventEmitter } from 'events';
import { join } from 'path';
import { homedir } from 'os';

import { IdentityManager } from './crypto/IdentityManager.js';
import { TransportManager } from './core/TransportManager.js';
import { RoomManager } from './core/RoomManager.js';
import { DiscoveryService } from './core/DiscoveryService.js';
import { GossipEngine } from './core/GossipEngine.js';
import { AuditLogger } from './core/AuditLogger.js';

import type {
  AppConfig,
  Envelope,
  Room,
  RoomType,
  RoomMessage,
  PeerInfo,
  NodeCard,
} from './types.js';

export class OSMP2P extends EventEmitter {
  public identity: IdentityManager;
  public transport: TransportManager;
  public rooms: RoomManager;
  public discovery: DiscoveryService;
  public gossip: GossipEngine;
  public audit: AuditLogger;

  private config: AppConfig;
  private dataDir: string;
  private started: boolean = false;

  constructor(config?: Partial<AppConfig>) {
    super();

    // 默认配置
    this.dataDir = config?.node?.dataDir || join(homedir(), '.osm-p2p');
    
    this.config = {
      node: {
        id: config?.node?.id || '',
        name: config?.node?.name || '',
        capabilities: config?.node?.capabilities || ['chat', 'file', 'gossip'],
        dataDir: this.dataDir,
      },
      transport: {
        udp: {
          enabled: true,
          port: 37291,
          broadcast: true,
          ...config?.transport?.udp,
        },
        nostr: {
          enabled: true,
          relays: [
            'wss://relay.damus.io',
            'wss://nos.lol',
            'wss://relay.nostr.band',
          ],
          announceInterval: 120000,
          ...config?.transport?.nostr,
        },
      },
      discovery: {
        udpBroadcast: true,
        udpBroadcastInterval: 5000,
        nostrAnnounce: true,
        nostrAnnounceInterval: 120000,
        holePunch: true,
        stunServers: ['stun.l.google.com:19302'],
        ...config?.discovery,
      },
      gossip: {
        enabled: true,
        maxNeighbors: 10,
        defaultTTL: 5,
        strategy: 'smart',
        rateLimitPerPeer: 10,
        rateLimitWindow: 60000,
        ...config?.gossip,
      },
      audit: {
        enabled: true,
        logPath: join(this.dataDir, 'audit.log'),
        ...config?.audit,
      },
      escalation: {
        ownerChannel: config?.escalation?.ownerChannel,
        autoEscalateOnError: false,
        ...config?.escalation,
      },
    };

    // 初始化组件
    this.identity = new IdentityManager(this.dataDir);
    this.transport = new TransportManager(this.config.transport);
    this.rooms = new RoomManager();
    this.discovery = new DiscoveryService(this.config.discovery);
    this.gossip = new GossipEngine(this.config.gossip);
    this.audit = new AuditLogger(this.config.audit.logPath, this.config.audit.enabled);

    // 绑定事件
    this.setupEventHandlers();
  }

  /**
   * 启动服务
   */
  async start(): Promise<void> {
    if (this.started) return;

    console.log('🚀 启动 OSM-P2P Hybrid...\n');

    // 1. 初始化身份
    const id = await this.identity.init(
      this.config.node.id,
      this.config.node.name
    );
    
    this.config.node.id = id.nodeId;
    this.config.node.name = id.name;

    // 2. 启动传输层
    await this.transport.start({
      nodeId: id.nodeId,
      name: id.name,
      privateKey: id.nostr!.privateKey,
      addrs: id.addrs,
    });

    // 3. 设置房间管理器身份
    this.rooms = new RoomManager({
      nodeId: id.nodeId,
      name: id.name,
    });

    // 4. 记录启动
    this.audit.logSystem('osm-p2p-started', {
      nodeId: id.nodeId,
      version: '1.0.0',
    });

    this.started = true;
    this.emit('ready');
    
    console.log('\n✅ OSM-P2P Hybrid 启动完成!');
    console.log(`   节点: ${id.name} (${id.nodeId})`);
    console.log(`   地址: ${id.addrs.map(a => `${a.ip}:${a.port}`).join(', ')}`);
    if (id.nostr) {
      console.log(`   Nostr: ${id.nostr.pubkey.substring(0, 16)}...`);
    }
  }

  /**
   * 停止服务
   */
  async stop(): Promise<void> {
    if (!this.started) return;

    this.audit.logSystem('osm-p2p-stopping');
    
    this.transport.stop();
    this.gossip.stop();
    await this.audit.stop();

    this.started = false;
    this.emit('stopped');
    
    console.log('\n✅ OSM-P2P Hybrid 已停止');
  }

  /**
   * 设置事件处理器
   */
  private setupEventHandlers(): void {
    // 传输层消息 -> 房间管理器
    this.transport.on('message', (envelope: Envelope) => {
      this.rooms.handleEnvelope(envelope);
      this.audit.logIncoming(envelope, JSON.stringify(envelope).length);
    });

    // 传输层发现 -> 发现服务
    this.transport.on('peer:update', (peer: PeerInfo) => {
      // 通知 Gossip 引擎
      this.gossip.addNeighbor(peer.nodeId);
    });

    // 房间事件 -> 上层
    this.rooms.on('message:received', (msg: RoomMessage, room: Room) => {
      this.emit('message', msg, room);
    });

    this.rooms.on('call:incoming', (call) => {
      this.emit('call:incoming', call);
    });
  }

  /**
   * 创建房间
   */
  createRoom(type: RoomType, topic?: string): Room {
    return this.rooms.createRoom(type, topic);
  }

  /**
   * 加入房间
   */
  joinRoom(roomId: string): boolean {
    return this.rooms.joinRoom(roomId);
  }

  /**
   * 发送消息
   */
  async sendMessage(content: string, target?: string): Promise<boolean> {
    const room = this.rooms.getCurrentRoom();
    if (!room) {
      console.log('❌ 没有活跃的聊天室');
      return false;
    }

    const msg = this.rooms.sendMessage(room.id, content, 'text');
    if (!msg) return false;

    // 广播给房间成员
    const envelope: Envelope = {
      version: '2.0',
      msgId: msg.id,
      timestamp: msg.timestamp,
      ttl: this.config.gossip.defaultTTL,
      from: {
        nodeId: this.config.node.id,
        pubkey: this.identity.getPubkey(),
        addrs: this.identity.getIdentity().addrs,
      },
      to: {
        type: room.type === 'broadcast' ? 'broadcast' : 'room',
        target: room.id,
      },
      payload: {
        type: 'room_message',
        data: {
          roomId: room.id,
          message: msg,
        },
      },
    };

    if (room.type === 'broadcast') {
      await this.transport.broadcast(envelope, true);
    } else {
      // 发送给每个成员
      for (const [peerId] of room.peers) {
        if (peerId !== this.config.node.id) {
          await this.transport.send(envelope, peerId);
        }
      }
    }

    this.audit.logOutgoing(envelope, room.id, JSON.stringify(envelope).length);
    return true;
  }

  /**
   * 广播消息
   */
  async broadcast(content: string, useNostr: boolean = true): Promise<void> {
    const envelope: Envelope = {
      version: '2.0',
      msgId: `broadcast-${Date.now()}`,
      timestamp: Date.now(),
      ttl: this.config.gossip.defaultTTL,
      from: {
        nodeId: this.config.node.id,
        pubkey: this.identity.getPubkey(),
        addrs: this.identity.getIdentity().addrs,
      },
      to: {
        type: 'broadcast',
      },
      payload: {
        type: 'room_message',
        data: {
          content,
          sender: this.config.node.name,
        },
      },
    };

    await this.transport.broadcast(envelope, useNostr);
    
    // Gossip 传播
    const peers = this.transport.getPeers();
    const targets = this.gossip.gossip(envelope, peers);
    
    this.audit.logSystem('broadcast', { content, targets: targets.length });
  }

  /**
   * 获取在线节点列表
   */
  getPeers(): PeerInfo[] {
    return this.transport.getPeers();
  }

  /**
   * 生成名片
   */
  generateCard(vipPort?: number): string {
    return this.identity.generateCard(vipPort);
  }

  /**
   * 解析名片
   */
  static parseCard(url: string): NodeCard | null {
    return IdentityManager.parseCard(url);
  }

  /**
   * 获取状态
   */
  getStatus(): {
    started: boolean;
    nodeId: string;
    name: string;
    peers: number;
    rooms: number;
    stats: ReturnType<TransportManager['getStats']>;
  } {
    return {
      started: this.started,
      nodeId: this.config.node.id,
      name: this.config.node.name,
      peers: this.transport.getPeers().length,
      rooms: this.rooms.getAllRooms().length,
      stats: this.transport.getStats(),
    };
  }
}

export default OSMP2P;
