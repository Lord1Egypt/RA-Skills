/**
 * 通知总线（基座） —— 跨插件 pub/sub
 *
 * 设计目标：
 *  - 本插件（欧度）只负责把 Odoo 事件打包成 NotificationEnvelope 并 publish
 *  - 渠道插件（企微 / 钉钉 / 飞书 / webhook 等）以两种方式之一接收：
 *      1) subscribe(handler) —— 收到全部 envelope，自己决定投递策略
 *      2) registerTransport({ name, deliver }) —— 由本插件或其他协调方显式
 *         调用 bus.deliver(envelope, { channel: name, ... }) 时才触发
 *  - 基座不感知任何具体渠道；新增渠道无需改动本插件
 *
 * 单例通过 `globalThis[Symbol.for('openclaw.huo15.notification-bus.v1')]` 共享，
 * 即便多个插件被分别打包成独立 ESM，只要运行在同一 Node 进程就能对接。
 */

import type {
  NotificationEnvelope,
  ChannelTransport,
  ChannelTarget,
  DeliveryResult,
  InboundReply,
  ReplyResult,
} from '../types/index.js';

const BUS_KEY = Symbol.for('openclaw.huo15.notification-bus.v1');

export type EnvelopeHandler = (envelope: NotificationEnvelope) => void | Promise<void>;
export type ReplyHandler = (reply: InboundReply) => void | Promise<void>;

export class NotificationBus {
  private handlers = new Set<EnvelopeHandler>();
  private replyHandlers = new Set<ReplyHandler>();
  private transports = new Map<string, ChannelTransport>();

  /** 订阅所有 envelope —— 返回取消订阅函数 */
  subscribe(handler: EnvelopeHandler): () => void {
    this.handlers.add(handler);
    return () => {
      this.handlers.delete(handler);
    };
  }

  /** 当前订阅者数量 */
  subscriberCount(): number {
    return this.handlers.size;
  }

  /** 注册渠道 transport —— 返回注销函数 */
  registerTransport(transport: ChannelTransport): () => void {
    this.transports.set(transport.name, transport);
    return () => {
      const current = this.transports.get(transport.name);
      if (current === transport) this.transports.delete(transport.name);
    };
  }

  /** 已注册的渠道列表 */
  listTransports(): Array<{ name: string; description?: string }> {
    return [...this.transports.values()].map(t => ({
      name: t.name,
      description: t.description,
    }));
  }

  hasTransport(name: string): boolean {
    return this.transports.has(name);
  }

  /**
   * 发布 envelope —— 并行通知所有订阅者
   *
   * 单个订阅者抛错不影响其他订阅者；本方法不抛错。
   */
  async publish(envelope: NotificationEnvelope): Promise<void> {
    if (this.handlers.size === 0) return;
    const results = await Promise.allSettled(
      [...this.handlers].map(h => Promise.resolve().then(() => h(envelope))),
    );
    for (const r of results) {
      if (r.status === 'rejected') {
        const reason = r.reason instanceof Error ? r.reason.message : String(r.reason);
        // 只在 stderr 留痕，避免影响主流程；真正的错误处理由订阅者自己负责
        // eslint-disable-next-line no-console
        console.warn('[notification-bus] subscriber failed:', reason);
      }
    }
  }

  /**
   * 显式调用某个 transport 投递 envelope 到具体 target。
   * 注意：publish() 已经把消息广播给所有 subscriber，大多数渠道直接 subscribe 即可；
   * 只有当你需要「本插件知道该发给谁、但具体怎么发由渠道实现」时才用 deliver。
   */
  async deliver(envelope: NotificationEnvelope, target: ChannelTarget): Promise<DeliveryResult> {
    const transport = this.transports.get(target.channel);
    if (!transport) {
      return {
        ok: false,
        channel: target.channel,
        error: `transport "${target.channel}" not registered`,
      };
    }
    try {
      return await transport.deliver(envelope, target);
    } catch (e) {
      return {
        ok: false,
        channel: target.channel,
        error: e instanceof Error ? e.message : String(e),
      };
    }
  }

  /* ═════════════════════════ 入站回复（渠道 → 源系统） ═════════════════════════ */

  /**
   * 订阅入站回复 —— 返回取消订阅函数。
   * 通常由源系统（Odoo）插件订阅；渠道插件不需要订阅自己发的回复。
   */
  onReply(handler: ReplyHandler): () => void {
    this.replyHandlers.add(handler);
    return () => {
      this.replyHandlers.delete(handler);
    };
  }

  replySubscriberCount(): number {
    return this.replyHandlers.size;
  }

  /**
   * 渠道插件收到用户回复时调用此方法。
   * 总线把 reply 并行发给所有 onReply 订阅者（通常只有 Odoo 插件一个）。
   */
  async reply(reply: InboundReply): Promise<ReplyResult> {
    if (this.replyHandlers.size === 0) {
      return { ok: false, handled: 0, errors: ['no reply handler registered'] };
    }
    const errors: string[] = [];
    let handled = 0;
    const results = await Promise.allSettled(
      [...this.replyHandlers].map(h => Promise.resolve().then(() => h(reply))),
    );
    for (const r of results) {
      if (r.status === 'fulfilled') {
        handled += 1;
      } else {
        errors.push(r.reason instanceof Error ? r.reason.message : String(r.reason));
      }
    }
    return { ok: errors.length === 0, handled, errors: errors.length ? errors : undefined };
  }
}

function resolveBus(): NotificationBus {
  const g = globalThis as Record<symbol, unknown>;
  let bus = g[BUS_KEY] as NotificationBus | undefined;
  if (!bus) {
    bus = new NotificationBus();
    g[BUS_KEY] = bus;
  }
  return bus;
}

/** 全局单例 —— 所有 openclaw 插件共享同一个总线 */
export const notificationBus: NotificationBus = resolveBus();
