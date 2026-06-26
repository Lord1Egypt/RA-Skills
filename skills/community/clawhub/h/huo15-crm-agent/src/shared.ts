/**
 * 公共类型与辅助函数。
 *
 * 设计原则：
 * - 不直连 Odoo —— 所有 CRM 写入由 @huo15/huo15-huihuoyun-odoo 执行
 * - v0.2 起接入企查查 API 做工商底座（绿火只做瘦客户端，不缓存数据）
 *
 * 因此本插件返回的 payload 都附带 `nextActions[]`，每条 nextAction 给出一条建议
 * 由 OpenClaw 在用户允许后调用 huihuoyun-odoo / 绿火其他工具的"下一步建议"。
 */

export type Tone = 'formal' | 'warm' | 'neutral';

export type ServiceLine =
  | '代账'
  | '审计'
  | '税务筹划'
  | 'IPO辅导'
  | '财税顾问'
  | '高新申报'
  | '汇算清缴'
  | '股权架构';

export type Priority = '高' | '中' | '低';

export interface PluginConfig {
  services?: ServiceLine[];
  region?: string;
  tone?: Tone;
  company_brand?: string;
  odoo_team_hint?: string;
  /** 企查查 OpenAPI key（v0.2 起，sales_company_search / sales_company_detail 使用）。 */
  qichacha_api_key?: string;
  qichacha_secret_key?: string;
  /** 默认 https://api.qichacha.net；私有部署 / 不同套餐可覆盖。 */
  qichacha_base_url?: string;
}

export interface NextAction {
  /** 建议调用的工具名（huihuoyun-odoo 的 odoo_*，或绿火自家的 sales_*）。 */
  odoo_tool: string;
  /** 自然语言描述：为什么建议这步、做什么。 */
  reason: string;
  /** 调用时建议的参数草稿（不直接执行，由 OpenClaw 让用户确认）。 */
  args_draft: Record<string, unknown>;
}

export const DEFAULT_CONFIG = {
  services: ['代账', '审计', '税务筹划', '财税顾问'] as ServiceLine[],
  region: '青岛',
  tone: 'warm' as Tone,
  company_brand: '青岛火一五信息科技有限公司',
};

export interface ResolvedConfig {
  services: ServiceLine[];
  region: string;
  tone: Tone;
  company_brand: string;
  odoo_team_hint?: string;
  qichacha_api_key?: string;
  qichacha_secret_key?: string;
  qichacha_base_url?: string;
}

export function resolveConfig(raw: unknown): ResolvedConfig {
  const cfg = (raw && typeof raw === 'object' ? raw : {}) as PluginConfig;
  return {
    services: cfg.services && cfg.services.length > 0 ? cfg.services : DEFAULT_CONFIG.services,
    region: cfg.region ?? DEFAULT_CONFIG.region,
    tone: cfg.tone ?? DEFAULT_CONFIG.tone,
    company_brand: cfg.company_brand ?? DEFAULT_CONFIG.company_brand,
    odoo_team_hint: cfg.odoo_team_hint,
    qichacha_api_key: cfg.qichacha_api_key,
    qichacha_secret_key: cfg.qichacha_secret_key,
    qichacha_base_url: cfg.qichacha_base_url,
  };
}

export function clamp(n: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, n));
}

export function priorityFromScore(score: number): Priority {
  if (score >= 75) return '高';
  if (score >= 50) return '中';
  return '低';
}

/** 返回 yyyy-mm-dd 格式的相对偏移日期（基于今天）。 */
export function offsetDate(daysFromToday: number, base = new Date()): string {
  const d = new Date(base);
  d.setDate(d.getDate() + daysFromToday);
  return d.toISOString().slice(0, 10);
}
