/**
 * 常量定义
 * 集中管理所有配置参数
 */

// WebSocket 配置
export const WS_CONFIG = {
  DEFAULT_URL: 'wss://global.powpow.online:8080',
  RECONNECT_INTERVAL: 3000, // 3秒
  MAX_RECONNECT_ATTEMPTS: 10,
  HEARTBEAT_INTERVAL: 30000, // 30秒心跳
  CONNECTION_TIMEOUT: 10000, // 10秒连接超时
} as const;

// 消息配置
export const MESSAGE_CONFIG = {
  MAX_LENGTH: 2000, // 最大消息长度
  QUEUE_SIZE: 100, // 消息队列最大长度
  BATCH_SIZE: 10, // 批量发送大小
} as const;

// 验证配置
export const VALIDATION_CONFIG = {
  DIGITAL_HUMAN_ID_MIN: 1,
  DIGITAL_HUMAN_ID_MAX: 100,
  USER_ID_MIN: 1,
  USER_ID_MAX: 100,
} as const;

// 内容类型
export const CONTENT_TYPES = {
  TEXT: 'text',
  VOICE: 'voice',
  IMAGE: 'image',
} as const;

// 发送者类型
export const SENDER_TYPES = {
  USER: 'user',
  OPENCLAW: 'openclaw',
} as const;

// WebSocket 消息类型
export const WS_MESSAGE_TYPES = {
  CHAT_MESSAGE: 'chat_message',
  CHAT_MESSAGE_ACK: 'chat_message_ack',
  CONNECTED: 'connected',
  ERROR: 'error',
  PING: 'ping',
  PONG: 'pong',
} as const;
