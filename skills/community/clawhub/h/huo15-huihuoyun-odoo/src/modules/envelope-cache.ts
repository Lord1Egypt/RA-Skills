/**
 * 信封溯源缓存 —— envelope.id → { agentId, model, resId }
 *
 * 入站回复流程：渠道回发一个 InboundReply{envelopeId, body}，
 * Odoo 插件要据此定位到原 Odoo 记录（model + res_id），写 chatter。
 * 信封体积大，不想每条都全量留存；只缓存路由所需的最小元信息。
 *
 * 策略：Map 的插入顺序天然 FIFO；超过 maxSize 时淘汰最旧的条目，
 * 同时按 TTL 过期失效。对实施经理场景足够（通常用户在几分钟内回复）。
 */

export interface EnvelopeOrigin {
  agentId: string;
  model?: string;
  resId?: number;
  cachedAt: number;
}

export class EnvelopeCache {
  private map = new Map<string, EnvelopeOrigin>();
  private readonly maxSize: number;
  private readonly ttlMs: number;

  constructor(maxSize: number = 500, ttlMs: number = 24 * 60 * 60 * 1000) {
    this.maxSize = maxSize;
    this.ttlMs = ttlMs;
  }

  set(envelopeId: string, origin: Omit<EnvelopeOrigin, 'cachedAt'>): void {
    if (this.map.has(envelopeId)) this.map.delete(envelopeId);
    this.map.set(envelopeId, { ...origin, cachedAt: Date.now() });
    while (this.map.size > this.maxSize) {
      const first = this.map.keys().next();
      if (first.done) break;
      this.map.delete(first.value);
    }
  }

  get(envelopeId: string): EnvelopeOrigin | undefined {
    const hit = this.map.get(envelopeId);
    if (!hit) return undefined;
    if (Date.now() - hit.cachedAt > this.ttlMs) {
      this.map.delete(envelopeId);
      return undefined;
    }
    return hit;
  }

  size(): number {
    return this.map.size;
  }

  clear(): void {
    this.map.clear();
  }
}
