import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { NextAction } from '../shared.js';
import { QccClient, resolveQccConfig } from '../clients/qichacha.js';

export function registerSalesCompanySearch(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_company_search',
    description:
      '财税获客 / 拓客：通过企查查 OpenAPI 搜索潜在客户企业（按行业 / 区域 / 关键词）。返回候选企业列表，可直接喂给 sales_lead_score 批量打分 + huihuoyun-odoo 写入 Odoo CRM。需要在插件 config 中配置 qichacha_api_key / qichacha_secret_key；未配置时返回引导信息让用户去 openapi.qcc.com 申请。本工具按调用付费（用户的企查查账户买单），绿火只做瘦客户端，不缓存数据。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        keyword: { type: 'string', description: '关键词（公司名 / 业务关键词），可选但建议传' },
        province: { type: 'string', description: '省份，例如"山东"' },
        city: { type: 'string', description: '城市，例如"青岛"' },
        industry_code: { type: 'string', description: '国民经济行业代码（GB/T 4754），例如"7233"= 会计审计税务服务' },
        page: { type: 'number', minimum: 1, description: '分页页码，默认 1' },
        page_size: { type: 'number', minimum: 1, maximum: 50, description: '每页条数，默认 20' },
      },
    },
    async execute(
      params: {
        keyword?: string;
        province?: string;
        city?: string;
        industry_code?: string;
        page?: number;
        page_size?: number;
      },
      ctx: Record<string, unknown>,
    ) {
      const pluginConfig = (ctx as { pluginConfig?: unknown }).pluginConfig;
      const qccConfig = resolveQccConfig(pluginConfig);

      if (!qccConfig) {
        return {
          success: false,
          fallback: 'no_qichacha_credentials',
          message:
            '企查查 API 未配置。绿火无法直接搜企业。请到 https://openapi.qcc.com/ 申请 key/secret 后写到 OpenClaw 插件配置：plugins.entries["crm-agent"].config.qichacha_api_key + qichacha_secret_key。配置完无需重启绿火，下次调用就会生效。',
          alternative_workflow: [
            '不接入企查查的临时方案：',
            '1. 让用户用其他工具（huo15-searxng / WebFetch）拉取目标行业 + 区域的公开企业名单',
            '2. 把 raw 文本喂给 sales_intent_signals 提取信号',
            '3. 把识别出的企业名单 + 备注交给 sales_lead_score 打分',
            '4. 高优先级线索由 huihuoyun-odoo 的 odoo_crm_create 写入 Odoo',
          ],
          nextActions: [],
        };
      }

      const client = new QccClient(qccConfig);
      const result = await client.search({
        keyword: params.keyword,
        province: params.province,
        city: params.city,
        industry_code: params.industry_code,
        page: params.page,
        page_size: params.page_size,
      });

      if (!result.ok) {
        return {
          success: false,
          fallback: 'qichacha_api_error',
          message: result.reason,
          hint:
            'API 调用失败可能原因：1) Key/Secret 错误；2) QPS 超限；3) 套餐余额不足；4) 接口路径与企查查文档不一致——可在 plugin config 里覆盖 paths。',
          nextActions: [],
        };
      }

      const items = result.data.items ?? [];
      const summary = {
        total: result.data.total ?? items.length,
        returned: items.length,
        keyword: params.keyword,
        region: [params.province, params.city].filter(Boolean).join(' / ') || undefined,
        industry_code: params.industry_code,
      };

      const nextActions: NextAction[] = [];
      if (items.length > 0) {
        nextActions.push({
          odoo_tool: 'sales_lead_score',
          reason: '把搜到的候选企业批量喂给绿火的打分工具，按财税获客优先级排序',
          args_draft: {
            leads: items.slice(0, 50).map((c) => ({
              name: c.name,
              industry: c.industry,
              region: c.region,
              notes: `企查查返回：注册资本 ${c.reg_capital ?? '-'}，状态 ${c.status ?? '-'}，法人 ${c.legal_person ?? '-'}`,
            })),
          },
        });
      }

      return {
        success: true,
        summary,
        companies: items,
        nextActions,
        hint:
          items.length > 0
            ? `已搜到 ${items.length} 家候选。建议先用 sales_lead_score 批量打分，再让用户挑选高优先级的入 Odoo CRM。如要看单家详情，调 sales_company_detail。`
            : '0 条命中。建议放宽关键词 / 区域 / 行业代码，或换 huo15-searxng 做兜底搜索。',
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
