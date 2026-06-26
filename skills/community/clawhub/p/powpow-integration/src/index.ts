/**
 * OpenClaw POWPOW Integration Skill v2.1.10
 * 
 * WebSocket-based real-time bidirectional chat with POWPOW digital humans
 */

import { EventEmitter } from 'events';
import WebSocket from 'ws';
import { logger } from './utils/logger';
import {
  validateDigitalHumanId,
  validateUserId,
  validateMessage,
  validateContentType,
  validateWebSocketUrl,
  validateMediaUrl,
  validateDuration,
  sanitizeString,
} from './utils/validator';
import {
  WS_CONFIG,
  MESSAGE_CONFIG,
  CONTENT_TYPES,
  SENDER_TYPES,
  WS_MESSAGE_TYPES,
} from './utils/constants';

// ============================================================================
// Types
// ============================================================================

interface PowPowConfig {
  wsUrl: string;
  digitalHumanId: string;
  openclawUserId: string;
  autoReconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

interface ChatMessage {
  id?: string;
  digitalHumanId: string;
  senderType: 'user' | 'openclaw';
  senderId: string;
  senderName?: string;
  content: string;
  contentType?: 'text' | 'voice' | 'image';
  mediaUrl?: string;
  duration?: number;
  timestamp?: string;
  isRead?: boolean;
}

interface WebSocketMessage {
  type: string;
  data: any;
}

// ============================================================================
// PowPowSkill Class
// ============================================================================

class PowPowSkill extends EventEmitter {
  private ws: WebSocket | null = null;
  private config: PowPowConfig;
  private isConnected = false;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private messageQueue: ChatMessage[] = [];
  private connectionStartTime: Date | null = null;
  private reconnectAttempts = 0;
  private connectionTimeout: NodeJS.Timeout | null = null;

  constructor(config: PowPowConfig) {
    super();
    
    // 验证必要参数
    const dhValidation = validateDigitalHumanId(config.digitalHumanId);
    if (!dhValidation.valid) {
      throw new Error(`Invalid digitalHumanId: ${dhValidation.error}`);
    }

    const userValidation = validateUserId(config.openclawUserId);
    if (!userValidation.valid) {
      throw new Error(`Invalid openclawUserId: ${userValidation.error}`);
    }

    const urlValidation = validateWebSocketUrl(config.wsUrl);
    if (!urlValidation.valid) {
      throw new Error(`Invalid wsUrl: ${urlValidation.error}`);
    }

    this.config = {
      autoReconnect: true,
      reconnectInterval: WS_CONFIG.RECONNECT_INTERVAL,
      maxReconnectAttempts: WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
      ...config,
    };

    logger.info('PowPowSkill initialized', {
      digitalHumanId: config.digitalHumanId,
      wsUrl: config.wsUrl,
    });
  }

  /**
   * Connect to POWPOW WebSocket server
   */
  public connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.isConnected) {
        logger.warn('Already connected');
        resolve();
        return;
      }

      try {
        const wsUrl = `${this.config.wsUrl}?client=openclaw&digitalHumanId=${this.config.digitalHumanId}&userId=${this.config.openclawUserId}`;
        
        logger.info('Connecting to WebSocket:', wsUrl);
        
        this.ws = new WebSocket(wsUrl);

        // 设置连接超时
        this.connectionTimeout = setTimeout(() => {
          if (!this.isConnected) {
            logger.error('Connection timeout');
            this.ws?.terminate();
            reject(new Error('Connection timeout'));
          }
        }, WS_CONFIG.CONNECTION_TIMEOUT);

        this.ws.on('open', () => {
          logger.info('WebSocket connected');
          this.isConnected = true;
          this.connectionStartTime = new Date();
          this.reconnectAttempts = 0;
          
          if (this.connectionTimeout) {
            clearTimeout(this.connectionTimeout);
            this.connectionTimeout = null;
          }

          this.startHeartbeat();
          this.emit('connected');
          this.flushMessageQueue();
          resolve();
        });

        this.ws.on('message', (data: WebSocket.RawData) => {
          try {
            const message: WebSocketMessage = JSON.parse(data.toString());
            this.handleMessage(message);
          } catch (error) {
            logger.error('Failed to parse message:', error);
            this.emit('error', new Error('Failed to parse message'));
          }
        });

        this.ws.on('close', (code: number, reason: Buffer) => {
          logger.info('WebSocket closed:', { code, reason: reason.toString() });
          this.cleanup();
          this.emit('disconnected', { code, reason: reason.toString() });
          
          if (this.config.autoReconnect && this.reconnectAttempts < (this.config.maxReconnectAttempts || WS_CONFIG.MAX_RECONNECT_ATTEMPTS)) {
            this.scheduleReconnect();
          }
        });

        this.ws.on('error', (error) => {
          logger.error('WebSocket error:', error);
          this.emit('error', error);
          reject(error);
        });

        this.ws.on('ping', () => {
          logger.debug('Received ping');
          this.ws?.pong();
        });

        this.ws.on('pong', () => {
          logger.debug('Received pong');
        });

      } catch (error) {
        logger.error('Failed to create connection:', error);
        reject(error);
      }
    });
  }

  /**
   * Disconnect from WebSocket server
   */
  public disconnect(): void {
    logger.info('Disconnecting...');
    this.cleanup();
    this.reconnectAttempts = this.config.maxReconnectAttempts || WS_CONFIG.MAX_RECONNECT_ATTEMPTS; // 阻止自动重连
  }

  /**
   * Cleanup resources
   */
  private cleanup(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }

    if (this.connectionTimeout) {
      clearTimeout(this.connectionTimeout);
      this.connectionTimeout = null;
    }

    if (this.ws) {
      try {
        this.ws.close();
      } catch (error) {
        logger.error('Error closing WebSocket:', error);
      }
      this.ws = null;
    }

    this.isConnected = false;
    this.connectionStartTime = null;
  }

  /**
   * Start heartbeat
   */
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        logger.debug('Sending ping');
        this.ws.ping();
      }
    }, WS_CONFIG.HEARTBEAT_INTERVAL);
  }

  /**
   * Send chat message
   */
  public sendMessage(content: string, contentType: 'text' | 'voice' | 'image' = 'text', options?: {
    mediaUrl?: string;
    duration?: number;
  }): boolean {
    // 验证输入
    const contentValidation = validateMessage(content);
    if (!contentValidation.valid) {
      logger.error('Invalid message content:', contentValidation.error);
      throw new Error(contentValidation.error);
    }

    const typeValidation = validateContentType(contentType);
    if (!typeValidation.valid) {
      logger.error('Invalid content type:', typeValidation.error);
      throw new Error(typeValidation.error);
    }

    // 验证多媒体参数
    if (contentType === 'voice' || contentType === 'image') {
      if (!options?.mediaUrl) {
        throw new Error('mediaUrl is required for voice/image messages');
      }
      const urlValidation = validateMediaUrl(options.mediaUrl);
      if (!urlValidation.valid) {
        throw new Error(urlValidation.error);
      }
    }

    if (contentType === 'voice' && options?.duration !== undefined) {
      const durationValidation = validateDuration(options.duration);
      if (!durationValidation.valid) {
        throw new Error(durationValidation.error);
      }
    }

    // 清理内容防止 XSS
    const sanitizedContent = sanitizeString(content);

    const message: ChatMessage = {
      digitalHumanId: this.config.digitalHumanId,
      senderType: SENDER_TYPES.OPENCLAW as 'openclaw',
      senderId: this.config.openclawUserId,
      content: sanitizedContent,
      contentType,
      ...options,
      timestamp: new Date().toISOString(),
    };

    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify({
          type: WS_MESSAGE_TYPES.CHAT_MESSAGE,
          data: message,
        }));
        logger.info('Message sent');
        return true;
      } catch (error) {
        logger.error('Failed to send message:', error);
        this.messageQueue.push(message);
        return false;
      }
    } else {
      // 检查队列是否已满
      if (this.messageQueue.length >= MESSAGE_CONFIG.QUEUE_SIZE) {
        logger.error('Message queue is full');
        throw new Error('Message queue is full');
      }
      
      this.messageQueue.push(message);
      logger.info('Message queued for later delivery');
      return false;
    }
  }

  /**
   * Quick reply
   */
  public reply(content: string): boolean {
    return this.sendMessage(content, CONTENT_TYPES.TEXT as 'text');
  }

  /**
   * Send voice message
   */
  public sendVoice(content: string, mediaUrl: string, duration: number): boolean {
    return this.sendMessage(content, CONTENT_TYPES.VOICE as 'voice', { mediaUrl, duration });
  }

  /**
   * Send image message
   */
  public sendImage(content: string, mediaUrl: string): boolean {
    return this.sendMessage(content, CONTENT_TYPES.IMAGE as 'image', { mediaUrl });
  }

  /**
   * Get connection status
   */
  public getConnectionStatus(): { connected: boolean; digitalHumanId: string; duration?: number; reconnectAttempts: number } {
    let duration: number | undefined;
    if (this.connectionStartTime) {
      duration = Date.now() - this.connectionStartTime.getTime();
    }

    return {
      connected: this.isConnected,
      digitalHumanId: this.config.digitalHumanId,
      duration,
      reconnectAttempts: this.reconnectAttempts,
    };
  }

  /**
   * Handle incoming messages
   */
  private handleMessage(message: WebSocketMessage): void {
    logger.debug('Received message:', message.type);

    switch (message.type) {
      case WS_MESSAGE_TYPES.CONNECTED:
        logger.info('Connection confirmed:', message.data);
        this.emit('connectionConfirmed', message.data);
        break;

      case WS_MESSAGE_TYPES.CHAT_MESSAGE:
        this.emit('message', message.data);
        break;

      case WS_MESSAGE_TYPES.CHAT_MESSAGE_ACK:
        logger.info('Message delivered:', message.data);
        this.emit('messageAck', message.data);
        break;

      case WS_MESSAGE_TYPES.ERROR:
        logger.error('Server error:', message.data);
        this.emit('serverError', message.data);
        break;

      case WS_MESSAGE_TYPES.PING:
        logger.debug('Received ping from server');
        break;

      case WS_MESSAGE_TYPES.PONG:
        logger.debug('Received pong from server');
        break;

      default:
        logger.warn('Unknown message type:', message.type);
    }
  }

  /**
   * Flush queued messages
   */
  private flushMessageQueue(): void {
    if (this.messageQueue.length === 0) return;

    logger.info(`Flushing ${this.messageQueue.length} queued messages`);

    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message && this.ws?.readyState === WebSocket.OPEN) {
        try {
          this.ws.send(JSON.stringify({
            type: WS_MESSAGE_TYPES.CHAT_MESSAGE,
            data: message,
          }));
        } catch (error) {
          logger.error('Failed to send queued message:', error);
          // 放回队列开头
          this.messageQueue.unshift(message);
          break;
        }
      }
    }
  }

  /**
   * Schedule reconnection
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectAttempts++;
    const delay = Math.min(
      this.config.reconnectInterval! * Math.pow(2, this.reconnectAttempts - 1),
      30000 // 最大30秒
    );

    logger.info(`Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts})`);
    this.emit('reconnecting', { attempt: this.reconnectAttempts, delay });

    this.reconnectTimer = setTimeout(() => {
      this.connect().catch((error) => {
        logger.error('Reconnection failed:', error);
      });
    }, delay);
  }
}

// ============================================================================
// OpenClaw Skill Plugin
// ============================================================================

interface OpenClawContext {
  userId: string;
  config: any;
  powpowSkill?: PowPowSkill;
  emit: (event: string, data: any) => void;
}

const powpowSkillPlugin = {
  name: 'powpow-integration',
  version: '2.1.10',
  description: 'POWPOW WebSocket Integration - Real-time bidirectional chat with POWPOW digital humans',

  init(context: any): void {
    logger.info('Plugin initialized');
    context.powpowConfig = {
      defaultWsUrl: WS_CONFIG.DEFAULT_URL,
      autoReconnect: true,
      reconnectInterval: WS_CONFIG.RECONNECT_INTERVAL,
      maxReconnectAttempts: WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
    };
  },

  destroy(): void {
    logger.info('Plugin destroyed');
  },

  commands: {
    /**
     * Connect to POWPOW
     */
    async connect(params: { digitalHumanId: string; wsUrl?: string }, context: OpenClawContext) {
      try {
        const wsUrl = params.wsUrl || context.config?.wsUrl || WS_CONFIG.DEFAULT_URL;

        // 验证参数
        const dhValidation = validateDigitalHumanId(params.digitalHumanId);
        if (!dhValidation.valid) {
          return { success: false, error: dhValidation.error };
        }

        const skill = new PowPowSkill({
          wsUrl,
          digitalHumanId: params.digitalHumanId,
          openclawUserId: context.userId,
          autoReconnect: true,
          reconnectInterval: WS_CONFIG.RECONNECT_INTERVAL,
          maxReconnectAttempts: WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
        });

        skill.on('message', (message: ChatMessage) => {
          context.emit('powpow.message.received', message);
        });

        skill.on('error', (error: Error) => {
          context.emit('powpow.error', error);
        });

        skill.on('reconnecting', (data: any) => {
          context.emit('powpow.reconnecting', data);
        });

        await skill.connect();
        context.powpowSkill = skill;

        return {
          success: true,
          message: 'Connected to POWPOW',
          digitalHumanId: params.digitalHumanId,
        };
      } catch (error) {
        logger.error('Connect command failed:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },

    /**
     * Disconnect from POWPOW
     */
    disconnect(params: {}, context: OpenClawContext) {
      const skill = context.powpowSkill;
      if (skill) {
        skill.disconnect();
        delete context.powpowSkill;
        return { success: true, message: 'Disconnected from POWPOW' };
      }
      return { success: false, error: 'Not connected' };
    },

    /**
     * Get connection status
     */
    status(params: {}, context: OpenClawContext) {
      const skill = context.powpowSkill;
      if (!skill) {
        return { success: false, status: 'disconnected', message: 'Not connected' };
      }

      const status = skill.getConnectionStatus();
      return {
        success: true,
        status: status.connected ? 'connected' : 'disconnected',
        digitalHumanId: status.digitalHumanId,
        duration: status.duration,
        reconnectAttempts: status.reconnectAttempts,
        message: status.connected ? 'Connected' : 'Disconnected',
      };
    },

    /**
     * Send message
     */
    send(params: { message: string; contentType?: string }, context: OpenClawContext) {
      try {
        const skill = context.powpowSkill;
        if (!skill) {
          return { success: false, error: 'Not connected to POWPOW' };
        }

        const contentType = (params.contentType || 'text') as 'text' | 'voice' | 'image';
        const sent = skill.sendMessage(params.message, contentType);
        return {
          success: sent,
          message: sent ? 'Message sent' : 'Message queued for delivery',
        };
      } catch (error) {
        logger.error('Send command failed:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },

    /**
     * Quick reply
     */
    reply(params: { message: string }, context: OpenClawContext) {
      try {
        const skill = context.powpowSkill;
        if (!skill) {
          return { success: false, error: 'Not connected to POWPOW' };
        }

        const sent = skill.reply(params.message);
        return {
          success: sent,
          message: sent ? 'Reply sent' : 'Reply queued for delivery',
        };
      } catch (error) {
        logger.error('Reply command failed:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },

    /**
     * Send voice message
     */
    sendVoice(params: { content: string; mediaUrl: string; duration: number }, context: OpenClawContext) {
      try {
        const skill = context.powpowSkill;
        if (!skill) {
          return { success: false, error: 'Not connected to POWPOW' };
        }

        const sent = skill.sendVoice(params.content, params.mediaUrl, params.duration);
        return {
          success: sent,
          message: sent ? 'Voice message sent' : 'Voice message queued',
        };
      } catch (error) {
        logger.error('SendVoice command failed:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },

    /**
     * Send image message
     */
    sendImage(params: { content: string; mediaUrl: string }, context: OpenClawContext) {
      try {
        const skill = context.powpowSkill;
        if (!skill) {
          return { success: false, error: 'Not connected to POWPOW' };
        }

        const sent = skill.sendImage(params.content, params.mediaUrl);
        return {
          success: sent,
          message: sent ? 'Image sent' : 'Image queued',
        };
      } catch (error) {
        logger.error('SendImage command failed:', error);
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },

    /**
     * Start listening for messages
     */
    listen(params: { autoReply?: boolean }, context: OpenClawContext) {
      const skill = context.powpowSkill;
      if (!skill) {
        return { success: false, error: 'Not connected to POWPOW' };
      }

      skill.on('message', (message: ChatMessage) => {
        logger.info('Received message:', message);
        context.emit('powpow.message.received', message);

        if (params.autoReply) {
          const reply = generateAutoReply(message.content);
          skill.reply(reply);
        }
      });

      return { success: true, message: 'Started listening for messages' };
    },

    /**
     * Stop listening for messages
     */
    stopListen(params: {}, context: OpenClawContext) {
      const skill = context.powpowSkill;
      if (skill) {
        skill.removeAllListeners('message');
        return { success: true, message: 'Stopped listening for messages' };
      }
      return { success: false, error: 'Not connected' };
    },
  },
};

/**
 * Auto-reply generator
 */
function generateAutoReply(content: string): string {
  const replies: Record<string, string> = {
    '你好': '你好！很高兴为你服务 😊',
    '嗨': '嗨！有什么可以帮助你的吗？',
    '帮助': '我可以帮你：\n1. 回答问题\n2. 提供信息\n3. 协助完成任务',
    '谢谢': '不客气！随时为你服务。',
    '再见': '再见！期待下次交流 👋',
  };

  for (const [keyword, reply] of Object.entries(replies)) {
    if (content.includes(keyword)) {
      return reply;
    }
  }

  return '收到你的消息了！我会尽快处理。';
}

// ============================================================================
// Exports
// ============================================================================

export { PowPowSkill, powpowSkillPlugin, logger };
export default powpowSkillPlugin;
