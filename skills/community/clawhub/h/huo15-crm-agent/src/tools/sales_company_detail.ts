import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { NextAction } from '../shared.js';
import { QccClient, resolveQccConfig } from '../clients/qichacha.js';

export function registerSalesCompanyDetail(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_company_detail',
    description:
      '财税获客 / 拓客：通过企查查 OpenAPI 拉单家企业的工商详情（注册资本 / 法人 / 经营范围 / 关联企业 / 近期变更 / 风险信号）。输出可直接喂给 sales_lead_brief 做画像，或喂给 sales_intent_signals 做意向打分。需要 qichacha_api_key / qichacha_secret_key 配置；未配置时返回引导信息。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        name: { type: 'string', description: '公司名（精确匹配优先）' },
        unique_id: { type: 'string', description: '企查查内部 unique_id（如已知，最稳）' },
        credit_code: { type: 'string', description: '统一社会信用代码（18 位）' },
      },
    },
    async execute(
      params: { name?: string; unique_id?: string; credit_code?: string },
      ctx: Record<string, unknown>,
    ) {
      const pluginConfig = (ctx as { pluginConfig?: unknown }).pluginConfig;
      const qccConfig = resolveQccConfig(pluginConfig);

      if (!qccConfig) {
        return {
          success: false,
          fallback: 'no_qichacha_credentials',
          message:
            '企查查 API 未配置。无法拉企业详情。请在 OpenClaw 插件 config 中配置 qichacha_api_key + qichacha_secret_key（申请地址 https://openapi.qcc.com/）。',
          nextActions: [],
        };
      }

      if (!params.name && !params.unique_id && !params.credit_code) {
        return {
          success: false,
          message: '需要 name / unique_id / credit_code 至少一个',
          nextActions: [],
        };
      }

      const client = new QccClient(qccConfig);
      const result = await client.detail(params);

      if (!result.ok) {
        return {
          success: false,
          fallback: 'qichacha_api_error',
          message: result.reason,
          nextActions: [],
        };
      }

      const c = result.data;
      const nextActions: NextAction[] = [];

      // 建议 1：把详情喂给 sales_lead_brief 做画像
      nextActions.push({
        odoo_tool: 'sales_lead_brief',
        reason: '把工商详情喂给绿火 brief 工具，自动匹配 5 类财税画像 + 推断主痛点',
        args_draft: {
          lead: {
            name: c.name,
            industry: c.industry,
            region: c.region,
            notes: [
              c.business_scope ? `经营范围：${c.business_scope.slice(0, 200)}` : '',
              c.employees_estimate ? `员工规模：${c.employees_estimate}` : '',
              c.recent_changes && c.recent_changes.length > 0
                ? `近期变更：${c.recent_changes.slice(0, 3).map((r) => `${r.date} ${r.field}`).join('；')}`
                : '',
            ].filter(Boolean).join('\n'),
          },
        },
      });

      // 建议 2：风险信号喂给 sales_intent_signals 抽取财税意向
      if (c.risk_signals && c.risk_signals.length > 0) {
        nextActions.push({
          odoo_tool: 'sales_intent_signals',
          reason: '该企业有风险事件（处罚 / 异常 / 欠税等），用信号词典提取财税意向',
          args_draft: {
            company_hint: c.name,
            raw_texts: c.risk_signals.map((r) => `${r.date ?? ''} ${r.type}: ${r.summary ?? ''}`),
            signal_categories: ['risk'],
          },
        });
      }

      // 建议 3：如有近期变更，提示触发跟进
      if (c.recent_changes && c.recent_changes.length > 0) {
        const changeText = c.recent_changes.map((r) => `${r.date} ${r.field}`).join('；');
        nextActions.push({
          odoo_tool: 'sales_intent_signals',
          reason: '近期工商变更触发，可能有财税重组需求',
          args_draft: {
            company_hint: c.name,
            raw_texts: [changeText],
            signal_categories: ['change'],
          },
        });
      }

      return {
        success: true,
        company: c,
        nextActions,
        hint:
          '详情已取回。建议链路：① sales_lead_brief 出画像 → ② sales_intent_signals 出意向（如有变更/风险）→ ③ sales_lead_score 综合打分 → ④ huihuoyun-odoo 的 odoo_crm_create 入库。',
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
