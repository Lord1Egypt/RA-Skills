/**
 * 火一五·辉火云企业套件插件 — 类型定义
 */

/** Odoo 连接配置 */
export interface OdooConfig {
  url: string;
  db: string;
  username: string;
  password: string;
}

/** Odoo 会话信息 */
export interface OdooSession {
  uid: number;
  session_id: string;
  user_context: Record<string, unknown>;
  company_id: number;
  partner_id: number;
  name: string;
  login: string;
}

/** Odoo API 错误 */
export interface OdooError {
  code: number;
  message: string;
  data?: {
    name: string;
    debug: string;
    message: string;
    arguments: unknown[];
  };
}

/** Odoo 记录（通用） */
export interface OdooRecord {
  id: number;
  [key: string]: unknown;
}

/** 同步更新 — 判别联合，用于 exhaustive switch */
export type SyncUpdate =
  | { type: 'todo';     action: 'create' | 'update' | 'delete'; id: number; data: OdooRecord; timestamp: number }
  | { type: 'activity'; action: 'due';                           id: number; data: OdooRecord; timestamp: number }
  | { type: 'message';  action: 'create';                        id: number; data: OdooRecord; timestamp: number }
  | { type: 'email';    action: 'create';                        id: number; data: OdooRecord; timestamp: number }
  | { type: 'calendar'; action: 'create' | 'update';             id: number; data: OdooRecord; timestamp: number };

/* ═══════════════════════════════════════════════════════════════════════════
 * 通知总线契约（跨插件）
 *
 * 本插件不关心消息最终走哪个渠道（企微 / 钉钉 / 飞书 / webhook …），
 * 只把 Odoo 事件封装成 NotificationEnvelope 并通过全局 bus 发布。
 * 其他插件（@huo15/wecom、@huo15/dingtalk 等）注册为订阅者或 transport 即可。
 *
 * 单一事实：`globalThis[Symbol.for('openclaw.huo15.notification-bus.v1')]`
 * ═══════════════════════════════════════════════════════════════════════════ */

export type NotificationKind = 'todo' | 'activity' | 'message' | 'email' | 'calendar';
export type NotificationPriority = 'low' | 'normal' | 'high' | 'urgent';

/** 跨渠道统一通知信封 */
export interface NotificationEnvelope {
  /** 稳定唯一 id，格式 `odoo:{agentId}:{kind}:{recordId}`，下游可据此去重 */
  id: string;
  /** 来源插件 id */
  source: 'odoo';
  /** 所属 OpenClaw agent（通常对应一位最终用户） */
  agentId: string;
  /** 通知种类 */
  kind: NotificationKind;
  /** 动作：create / update / due / … */
  action: string;
  /** 优先级 */
  priority: NotificationPriority;
  /** 一行标题 */
  title: string;
  /** 一句话摘要，纯文本 */
  summary: string;
  /** 可选的较长纯文本正文 */
  body?: string;
  /** 可选的 markdown 正文，渠道如支持优先使用 */
  markdown?: string;
  /** 深链（回到 Odoo 原记录） */
  link?: { url: string; label?: string };
  /** 用于路由/过滤的标签 */
  tags?: string[];
  /** 生成时间戳（ms） */
  createdAt: number;
  /** 源记录元信息，渠道可用来构造自己的 deep-link */
  origin?: {
    url?: string;
    model?: string;
    resId?: number;
  };
  /** 原始 Odoo 字段，供渠道自定义渲染 */
  raw?: Record<string, unknown>;
}

/** 渠道投递目标（通用包），字段含义由各渠道 transport 自己解释 */
export interface ChannelTarget {
  channel: string;
  userId?: string;
  chatId?: string;
  extra?: Record<string, unknown>;
}

/** 渠道投递结果 */
export interface DeliveryResult {
  ok: boolean;
  channel: string;
  messageId?: string;
  error?: string;
}

/**
 * 渠道 transport 契约 —— 由渠道插件（企微、钉钉…）向总线注册。
 * 本插件只调用 deliver()，不关心内部实现。
 */
export interface ChannelTransport {
  /** 渠道标识：'wecom' | 'dingtalk' | 'feishu' | 'webhook' | … */
  name: string;
  /** UI 描述（可选） */
  description?: string;
  /** 把 envelope 投递给具体 target */
  deliver(envelope: NotificationEnvelope, target: ChannelTarget): Promise<DeliveryResult>;
  /** 把 target 描述为人类可读字符串（可选，用于 UI） */
  describeTarget?(target: ChannelTarget): string;
}

/**
 * 入站回复载荷（从渠道回到源系统）
 *
 * 典型场景：用户在企微/钉钉里对某条 Odoo 通知直接回复一句话，
 * 渠道插件把这段文字打包成 InboundReply 发回总线，
 * Odoo 插件收到后在对应记录的 chatter 里写一条 mail.message。
 */
export interface InboundReply {
  /** 被回复的 envelope id */
  envelopeId: string;
  /** 回复来自哪个渠道 */
  channel: string;
  /** 渠道里回复的人（渠道自己解释） */
  fromUser?: string;
  /** 纯文本正文 */
  body: string;
  /** 可选的 HTML / Markdown 渲染 */
  html?: string;
  /** 附件 URL（若渠道支持） */
  attachments?: Array<{ url: string; name?: string; mime?: string }>;
  /** 渠道原始事件，供调试/审计 */
  raw?: Record<string, unknown>;
}

/** 回复处理结果 */
export interface ReplyResult {
  ok: boolean;
  handled: number;
  errors?: string[];
}

/**
 * 每 agent 的通知偏好 —— 让用户能说"别发待办通知"/"夜里静音"
 *
 * 过滤发生在生产者一侧（Odoo 插件）；bus 依然是无感知的纯广播。
 */
export interface NotificationPreferences {
  /** 主开关；false 时 Odoo 插件不再发布任何 envelope */
  enabled: boolean;
  /** 允许发布的 kind 列表；空数组视为全放行 */
  kinds: NotificationKind[];
  /** 低于此优先级的不发 */
  minPriority: NotificationPriority;
  /** 静音时段（24h 制，HH:MM，按服务器本地时区） */
  quietHours?: { start: string; end: string };
  /** 更新时间戳 */
  updatedAt: number;
}

/** 意图解析结果 */
export interface IntentResult {
  intent: string;
  confidence: number;
  entities: Record<string, unknown>;
  model?: string;
  method?: string;
}

/** 自定义意图模式 */
export interface IntentPattern {
  pattern: string;
  intent: string;
  model?: string;
  method?: string;
}

/** 插件配置（对应 openclaw.plugin.json configSchema） */
export interface OdooPluginConfig {
  odoo?: OdooConfig;
  sync?: {
    enabled: boolean;
    intervalSeconds: number;
    channels: string[];
  };
}
