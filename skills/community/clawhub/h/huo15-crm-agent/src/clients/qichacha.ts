/**
 * 企查查 OpenAPI 客户端（瘦客户端，仅 fetch + HMAC 签名）。
 *
 * 设计原则（按 v0.2 调研报告 takeaway #1）：
 * - 不缓存大量数据 —— 绿火只做"瘦客户端 + 提示词增强"，按调用付费让用户的
 *   企查查账户承担成本，绿火不持有数据资产。
 * - 不引入新 npm 依赖 —— 用 Node 25 内置 fetch + 内置 crypto 做 HMAC。
 * - 不引入 child_process（CLAUDE.md §6.2 红线）。
 * - graceful fallback —— 未配置 API key / 网络失败时返回 `{ ok: false, reason }`，
 *   工具层会把失败原因翻译成 hint 让 LLM 引导用户配置或自带数据。
 *
 * 注意：企查查 API 的具体接口路径与签名规则以企查查商务给出的合同 / 文档为准；
 * 此处实现按公开材料（openapi.qcc.com）合理猜测，用户首次接入需根据实际签名
 * 规则微调 `signHeaders` 方法。配置可覆盖 baseUrl / 接口路径。
 */

import { createHash } from 'node:crypto';

export interface QccConfig {
  apiKey: string;
  secretKey: string;
  /** 默认 https://api.qichacha.net。企查查不同套餐 / 私有部署可配不同 base。 */
  baseUrl?: string;
  /** 默认 8000ms。 */
  timeoutMs?: number;
  /**
   * 接口路径覆盖。企查查 API 版本变动频繁（V3/V4），实际路径以企查查文档为准。
   * 默认值为常见 V4 路径，如不一致用户在 plugin config 里覆盖即可。
   */
  paths?: {
    search?: string;     // 默认 /ECIV4/Search
    detail?: string;     // 默认 /ECIV4/GetDetailsByName
  };
}

export interface QccCompanyBrief {
  name: string;
  unique_id?: string;
  credit_code?: string;
  legal_person?: string;
  reg_capital?: string;       // 原始字符串，含币种（万元 / Million USD）
  reg_date?: string;
  industry?: string;
  region?: string;
  status?: string;
  source_url?: string;
}

export interface QccCompanyDetail extends QccCompanyBrief {
  business_scope?: string;
  employees_estimate?: string;     // 社保人数区间或精确值
  registered_address?: string;
  contact_phone?: string;
  contact_email?: string;
  website?: string;
  related_companies?: Array<{ name: string; relation?: string }>;
  recent_changes?: Array<{ date: string; field: string; before?: string; after?: string }>;
  risk_signals?: Array<{ type: string; date?: string; summary?: string }>;
}

export type QccResult<T> =
  | { ok: true; data: T }
  | { ok: false; reason: string; status?: number };

/** 企查查公开签名规则（commonly cited）：MD5(key + timestamp + secretKey).toUpperCase()。
 *  实际以合同为准。如签名规则不同，覆盖 `signHeaders` 方法即可。 */
function defaultSign(apiKey: string, secretKey: string, timestamp: string): string {
  return createHash('md5')
    .update(apiKey + timestamp + secretKey)
    .digest('hex')
    .toUpperCase();
}

export class QccClient {
  private apiKey: string;
  private secretKey: string;
  private baseUrl: string;
  private timeoutMs: number;
  private searchPath: string;
  private detailPath: string;

  constructor(config: QccConfig) {
    if (!config.apiKey || !config.secretKey) {
      throw new Error('QccClient: apiKey 和 secretKey 必填');
    }
    this.apiKey = config.apiKey;
    this.secretKey = config.secretKey;
    this.baseUrl = (config.baseUrl ?? 'https://api.qichacha.net').replace(/\/+$/, '');
    this.timeoutMs = config.timeoutMs ?? 8000;
    this.searchPath = config.paths?.search ?? '/ECIV4/Search';
    this.detailPath = config.paths?.detail ?? '/ECIV4/GetDetailsByName';
  }

  private signHeaders(): Record<string, string> {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const token = defaultSign(this.apiKey, this.secretKey, timestamp);
    return { Token: token, Timespan: timestamp };
  }

  private async call<T>(path: string, query: Record<string, string | number | undefined>): Promise<QccResult<T>> {
    const url = new URL(this.baseUrl + path);
    url.searchParams.set('key', this.apiKey);
    for (const [k, v] of Object.entries(query)) {
      if (v !== undefined && v !== '') url.searchParams.set(k, String(v));
    }
    try {
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: this.signHeaders(),
        signal: AbortSignal.timeout(this.timeoutMs),
      });
      if (!response.ok) {
        return { ok: false, reason: `企查查 API HTTP ${response.status}`, status: response.status };
      }
      const json = (await response.json()) as { Status?: string; Message?: string; Result?: T };
      if (json.Status && json.Status !== '200') {
        return { ok: false, reason: `企查查 API 业务错误 ${json.Status}: ${json.Message ?? '未知'}` };
      }
      return { ok: true, data: (json.Result ?? json) as T };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      return { ok: false, reason: `企查查 API 网络异常: ${msg}` };
    }
  }

  /** 关键词搜索企业（行业 / 区域 / 关键词）。 */
  async search(params: {
    keyword?: string;
    province?: string;
    city?: string;
    industry_code?: string;
    page?: number;
    page_size?: number;
  }): Promise<QccResult<{ total: number; items: QccCompanyBrief[] }>> {
    return this.call<{ total: number; items: QccCompanyBrief[] }>(this.searchPath, {
      keyWord: params.keyword,
      province: params.province,
      city: params.city,
      industryCode: params.industry_code,
      pageIndex: params.page ?? 1,
      pageSize: params.page_size ?? 20,
    });
  }

  /** 单企业详情。优先用 unique_id；退化用 name。 */
  async detail(params: {
    unique_id?: string;
    name?: string;
    credit_code?: string;
  }): Promise<QccResult<QccCompanyDetail>> {
    if (!params.unique_id && !params.name && !params.credit_code) {
      return { ok: false, reason: '需要 unique_id / name / credit_code 至少一个' };
    }
    return this.call<QccCompanyDetail>(this.detailPath, {
      keyWord: params.name ?? params.credit_code ?? params.unique_id,
      uniqueID: params.unique_id,
    });
  }
}

/** 从 PluginConfig 解析企查查配置。未配置返回 null。 */
export function resolveQccConfig(raw: unknown): QccConfig | null {
  if (!raw || typeof raw !== 'object') return null;
  const cfg = raw as Record<string, unknown>;
  const apiKey = typeof cfg.qichacha_api_key === 'string' ? cfg.qichacha_api_key : '';
  const secretKey = typeof cfg.qichacha_secret_key === 'string' ? cfg.qichacha_secret_key : '';
  if (!apiKey || !secretKey) return null;
  const baseUrl = typeof cfg.qichacha_base_url === 'string' ? cfg.qichacha_base_url : undefined;
  return { apiKey, secretKey, baseUrl };
}
