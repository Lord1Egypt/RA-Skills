/**
 * RoomManager - 房间管理器
 * 管理 Direct、Broadcast、Multicast 三种房间类型
 */

import { EventEmitter } from 'events';
import { randomBytes } from 'crypto';
import type {
  Room,
  RoomType,
  RoomPeer,
  RoomMessage,
  Envelope,
  Payload,
} from '../types.js';

interface RoomConfig {
  maxPeers?: number;
  maxMessages?: number;
  autoCleanup?: boolean;
  ttl?: number;
}

export class RoomManager extends EventEmitter {
  private rooms: Map<string, Room> = new Map();
  private currentRoomId: string | null = null;
  private identity: { nodeId: string; name: string } | null = null;
  private defaultConfig: RoomConfig = {
    maxPeers: 100,
    maxMessages: 1000,
    autoCleanup: true,
    ttl: 3600000, // 1小时
  };

  constructor(identity?: { nodeId: string; name: string }) {
    super();
    this.identity = identity || null;
  }

  /**
   * 创建房间
   */
  createRoom(type: RoomType, topic?: string, config?: RoomConfig): Room {
    const roomId = this.generateRoomId();
    const now = Date.now();

    const room: Room = {
      id: roomId,
      type,
      topic,
      peers: new Map(),
      creator: this.identity?.nodeId || 'unknown',
      transport: {
        primary: type === 'broadcast' ? 'udp' : 'nostr',
        fallback: 'nostr',
        allowRelay: true,
      },
      messages: [],
      createdAt: now,
      updatedAt: now,
      expiresAt: config?.ttl ? now + config.ttl : undefined,
    };

    // 创建者自动加入
    if (this.identity) {
      this.addPeerToRoom(roomId, {
        nodeId: this.identity.nodeId,
        role: 'creator',
        joinedAt: now,
        lastActivity: now,
      });
    }

    this.rooms.set(roomId, room);
    this.currentRoomId = roomId;

    this.emit('room:created', room);
    return room;
  }

  /**
   * 加入房间
   */
  joinRoom(roomId: string, peer?: RoomPeer): boolean {
    const room = this.rooms.get(roomId);
    if (!room) {
      // 可以接收外部房间邀请时创建
      return false;
    }

    if (peer) {
      this.addPeerToRoom(roomId, peer);
    } else if (this.identity) {
      this.addPeerToRoom(roomId, {
        nodeId: this.identity.nodeId,
        role: 'member',
        joinedAt: Date.now(),
        lastActivity: Date.now(),
      });
    }

    this.currentRoomId = roomId;
    this.emit('room:joined', room);
    return true;
  }

  /**
   * 离开房间
   */
  leaveRoom(roomId?: string): boolean {
    const id = roomId || this.currentRoomId;
    if (!id) return false;

    const room = this.rooms.get(id);
    if (!room || !this.identity) return false;

    // 移除自己
    room.peers.delete(this.identity.nodeId);

    // 广播离开消息
    this.addMessage(id, {
      id: this.generateMessageId(),
      roomId: id,
      sender: 'system',
      type: 'system',
      content: `${this.identity.name} 离开了房间`,
      timestamp: Date.now(),
      transport: 'udp',
    });

    this.emit('room:left', room);

    // 如果没有参与者了，清理房间
    if (room.peers.size === 0 && this.defaultConfig.autoCleanup) {
      this.closeRoom(id);
    }

    if (this.currentRoomId === id) {
      this.currentRoomId = null;
    }

    return true;
  }

  /**
   * 关闭房间
   */
  closeRoom(roomId: string): boolean {
    const room = this.rooms.get(roomId);
    if (!room) return false;

    this.rooms.delete(roomId);
    
    if (this.currentRoomId === roomId) {
      this.currentRoomId = null;
    }

    this.emit('room:closed', room);
    return true;
  }

  /**
   * 获取房间
   */
  getRoom(roomId?: string): Room | undefined {
    return this.rooms.get(roomId || this.currentRoomId || '');
  }

  /**
   * 获取当前房间
   */
  getCurrentRoom(): Room | null {
    return this.currentRoomId ? this.rooms.get(this.currentRoomId) || null : null;
  }

  /**
   * 获取所有房间
   */
  getAllRooms(): Room[] {
    return Array.from(this.rooms.values());
  }

  /**
   * 添加消息到房间
   */
  addMessage(roomId: string, message: RoomMessage): void {
    const room = this.rooms.get(roomId);
    if (!room) return;

    room.messages.push(message);
    room.updatedAt = Date.now();

    // 限制消息数量
    if (room.messages.length > (this.defaultConfig.maxMessages || 1000)) {
      room.messages.shift();
    }

    // 更新发送者的活动时间
    const peer = room.peers.get(message.sender);
    if (peer) {
      peer.lastActivity = Date.now();
    }

    this.emit('message:received', message, room);
  }

  /**
   * 发送消息（创建 envelope）
   */
  sendMessage(roomId: string, content: string, type: 'text' | 'file' = 'text', meta?: RoomMessage['meta']): RoomMessage | null {
    if (!this.identity) return null;

    const room = this.rooms.get(roomId);
    if (!room) return null;

    const message: RoomMessage = {
      id: this.generateMessageId(),
      roomId,
      sender: this.identity.nodeId,
      type,
      content,
      meta,
      timestamp: Date.now(),
      transport: room.transport.primary,
    };

    this.addMessage(roomId, message);
    return message;
  }

  /**
   * 处理收到的 envelope
   */
  handleEnvelope(envelope: Envelope): void {
    const { payload, from, to } = envelope;

    switch (payload.type) {
      case 'call_request':
        this.handleCallRequest(envelope);
        break;
      case 'call_accept':
        this.handleCallAccept(envelope);
        break;
      case 'call_reject':
        this.handleCallReject(envelope);
        break;
      case 'room_join':
        this.handleRoomJoin(envelope);
        break;
      case 'room_message':
        this.handleRoomMessage(envelope);
        break;
      case 'room_file':
        this.handleRoomFile(envelope);
        break;
      case 'call_end':
        this.handleCallEnd(envelope);
        break;
    }
  }

  /**
   * 处理呼叫请求
   */
  private handleCallRequest(envelope: Envelope): void {
    const data = envelope.payload.data as {
      roomId: string;
      topic?: string;
    };

    // 通知上层有来电
    this.emit('call:incoming', {
      roomId: data.roomId,
      callerId: envelope.from.nodeId,
      topic: data.topic,
    });
  }

  /**
   * 处理呼叫接受
   */
  private handleCallAccept(envelope: Envelope): void {
    const data = envelope.payload.data as { roomId: string };
    this.emit('call:accepted', data.roomId);
  }

  /**
   * 处理呼叫拒绝
   */
  private handleCallReject(envelope: Envelope): void {
    const data = envelope.payload.data as { roomId: string; reason?: string };
    this.emit('call:rejected', data.roomId, data.reason);
  }

  /**
   * 处理加入房间
   */
  private handleRoomJoin(envelope: Envelope): void {
    const data = envelope.payload.data as {
      roomId: string;
      peer: RoomPeer;
    };

    this.joinRoom(data.roomId, {
      ...data.peer,
      nodeId: envelope.from.nodeId,
    });
  }

  /**
   * 处理房间消息
   */
  private handleRoomMessage(envelope: Envelope): void {
    const data = envelope.payload.data as {
      roomId: string;
      message: RoomMessage;
    };

    this.addMessage(data.roomId, {
      ...data.message,
      sender: envelope.from.nodeId,
      transport: envelope._transport || 'nostr',
    });
  }

  /**
   * 处理房间文件
   */
  private handleRoomFile(envelope: Envelope): void {
    const data = envelope.payload.data as {
      roomId: string;
      message: RoomMessage;
    };

    this.addMessage(data.roomId, {
      ...data.message,
      sender: envelope.from.nodeId,
      type: 'file',
      transport: envelope._transport || 'nostr',
    });
  }

  /**
   * 处理结束呼叫
   */
  private handleCallEnd(envelope: Envelope): void {
    const data = envelope.payload.data as { roomId: string };
    this.emit('call:ended', data.roomId);
  }

  /**
   * 添加对等节点到房间
   */
  private addPeerToRoom(roomId: string, peer: RoomPeer): void {
    const room = this.rooms.get(roomId);
    if (!room) return;

    room.peers.set(peer.nodeId, peer);
    room.updatedAt = Date.now();
  }

  /**
   * 生成房间 ID
   */
  private generateRoomId(): string {
    return `room-${randomBytes(8).toString('hex')}`;
  }

  /**
   * 生成消息 ID
   */
  private generateMessageId(): string {
    return `msg-${randomBytes(4).toString('hex')}`;
  }

  /**
   * 清理过期房间
   */
  cleanup(): void {
    const now = Date.now();
    
    for (const [roomId, room] of this.rooms.entries()) {
      // 清理过期房间
      if (room.expiresAt && now > room.expiresAt) {
        this.closeRoom(roomId);
        continue;
      }

      // 清理不活跃的对等节点
      for (const [peerId, peer] of room.peers.entries()) {
        if (now - peer.lastActivity > 300000) { // 5分钟
          room.peers.delete(peerId);
        }
      }

      // 空房间清理
      if (room.peers.size === 0 && this.defaultConfig.autoCleanup) {
        this.closeRoom(roomId);
      }
    }
  }
}
