import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { resolveConfig, type NextAction } from '../shared.js';
import { scoreLead, type LeadInput, type ScoredLead } from '../domain/lead_scoring.js';

export function registerSalesLeadScore(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_lead_score',
    description:
      '财税获客线索批量打分。输入一组 lead 基础信息（公司名/行业/规模/区域/痛点备注/决策人角色），返回每条 lead 的 0-100 分、优先级（高/中/低）、推荐服务方向（代账/审计/筹划/IPO 等）、得分理由分解、切入 hook。本工具不写 Odoo —— 输出 nextActions 数组建议把高优先级线索通过 huihuoyun-odoo 的 odoo_crm_create 工具写入 Odoo CRM。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        leads: {
          type: 'array',
          minItems: 1,
          items: {
            type: 'object',
            additionalProperties: false,
            properties: {
              name: { type: 'string', description: '公司名称（必填）' },
              industry: { type: 'string', description: '行业，例如"软件"、"医疗器械"、"外贸"' },
              region: { type: 'string', description: '所在区域，例如"青岛"、"济南"、"上海"' },
              employees: { type: 'number', description: '员工数估计' },
              revenue_wan: { type: 'number', description: '年营收（万元）估计' },
              decision_maker_role: { type: 'string', description: '决策人角色，例如"老板"、"CFO"、"财务总监"、"会计"' },
              notes: { type: 'string', description: '业务员的备注，越具体越准 ——"老板说被税务通知补税"、"想做高新认定"等关键词会显著影响打分' },
              stage: { type: 'string', description: '客户当前状态描述，例如"已联系两次"、"在比价"、"拟上市"' },
              last_contact: { type: 'string', description: '上次接触日期 yyyy-mm-dd（不参与打分，便于后续 followup）' },
            },
            required: ['name'],
          },
        },
        write_back_to_odoo: {
          type: 'boolean',
          description: '是否在 nextActions 中给出"写入 Odoo CRM"的建议（默认 true，仅产生建议不直接执行）。',
          default: true,
        },
      },
      required: ['leads'],
    },
    async execute(
      params: { leads: LeadInput[]; write_back_to_odoo?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const cfg = resolveConfig((ctx as { pluginConfig?: unknown }).pluginConfig);
      const writeBack = params.write_back_to_odoo ?? true;

      const scored: ScoredLead[] = params.leads.map((l) => scoreLead(l, cfg));
      scored.sort((a, b) => b.score - a.score);

      const summary = {
        total: scored.length,
        high: scored.filter((s) => s.priority === '高').length,
        medium: scored.filter((s) => s.priority === '中').length,
        low: scored.filter((s) => s.priority === '低').length,
        avg_score: Math.round(scored.reduce((acc, s) => acc + s.score, 0) / Math.max(scored.length, 1)),
      };

      const nextActions: NextAction[] = writeBack
        ? scored
            .filter((s) => s.priority !== '低')
            .slice(0, 10)
            .map((s) => ({
              odoo_tool: 'odoo_crm_create',
              reason: `${s.priority}优先级线索（评分 ${s.score}）—— ${s.persona} —— 建议立即创建 CRM 线索并指派`,
              args_draft: {
                name: `[${s.persona}] ${s.name}`,
                description: `自动打分 ${s.score} 分。\n推荐服务：${s.recommended_services.join('、')}\n切入 hook：${s.hook}\n得分理由：\n  - ${s.reasons.join('\n  - ')}`,
                priority: s.priority === '高' ? '3' : '2',
                team_hint: cfg.odoo_team_hint,
                tag_ids: ['财税获客', s.persona, ...s.recommended_services],
              },
            }))
        : [];

      return {
        success: true,
        summary,
        scored,
        nextActions,
        hint:
          nextActions.length > 0
            ? '请确认前 ' +
              nextActions.length +
              ' 条建议后，调用 huihuoyun-odoo 的 odoo_crm_create 工具批量写入。注意每条 args_draft 的 team_hint 字段是字符串提示，需要先用 odoo_search 查到对应 team_id 再传 team_id。'
            : '已生成打分结果，未生成 Odoo 写入建议（write_back_to_odoo=false）。',
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
