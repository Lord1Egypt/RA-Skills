import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { resolveConfig, type NextAction } from '../shared.js';
import { scoreLead, type LeadInput } from '../domain/lead_scoring.js';
import { pickPersona } from '../domain/personas.js';

export function registerSalesLeadBrief(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_lead_brief',
    description:
      '生成单条财税线索的全景简报。输入一条 lead 信息（可来自人工录入，或由 huihuoyun-odoo 的 odoo_crm_pipeline / odoo_search 拉到 crm.lead 后传入），输出该客户的 5 维画像：公司画像（persona）、推断痛点、推荐服务方向、决策人优先级、切入话术 hook。同时附带 1 条建议首次接触话术草稿。本工具不写 Odoo —— 后续动作（写入 description 字段、创建活动、转给销售）通过 huihuoyun-odoo 工具完成。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        lead: {
          type: 'object',
          additionalProperties: false,
          properties: {
            name: { type: 'string' },
            industry: { type: 'string' },
            region: { type: 'string' },
            employees: { type: 'number' },
            revenue_wan: { type: 'number' },
            decision_maker_role: { type: 'string' },
            notes: { type: 'string' },
            stage: { type: 'string' },
            last_contact: { type: 'string' },
          },
          required: ['name'],
        },
        odoo_lead_id: {
          type: 'number',
          description: '可选。如果 lead 来自 Odoo CRM，传入 crm.lead 的 id，brief 会附带"把 brief 写回 lead.description"的 nextAction。',
        },
      },
      required: ['lead'],
    },
    async execute(
      params: { lead: LeadInput; odoo_lead_id?: number },
      ctx: Record<string, unknown>,
    ) {
      const cfg = resolveConfig((ctx as { pluginConfig?: unknown }).pluginConfig);
      const lead = params.lead;
      const scored = scoreLead(lead, cfg);
      const persona = pickPersona({
        employees: lead.employees,
        revenue_wan: lead.revenue_wan,
        industry: lead.industry,
        stage: lead.stage,
        notes: lead.notes,
      });

      const decision_makers_with_priority = persona.decision_makers.map((role, idx) => ({
        role,
        priority: idx === 0 ? '首选' : idx === 1 ? '次选' : '备选',
      }));

      const first_message_draft = `${persona.decision_makers[0]}您好，我是${cfg.company_brand}的财税顾问。注意到贵司可能涉及"${persona.pain_points[0]}"——${persona.hooks[0]}。能否方便沟通 3 分钟？`;

      const brief = {
        company: lead.name,
        score: scored.score,
        priority: scored.priority,
        persona: {
          id: persona.id,
          display: persona.display,
          pain_points: persona.pain_points,
          recommended_services: persona.recommended_services.filter((s) => cfg.services.includes(s)),
        },
        decision_makers_with_priority,
        hooks: persona.hooks,
        score_reasons: scored.reasons,
        first_message_draft,
      };

      const nextActions: NextAction[] = [];
      if (params.odoo_lead_id !== undefined) {
        const summaryText = [
          `[财税画像] ${persona.display}（评分 ${scored.score}, ${scored.priority}）`,
          `推荐服务：${brief.persona.recommended_services.join('、')}`,
          `主痛点：${persona.pain_points.slice(0, 3).join('；')}`,
          `决策人优先级：${decision_makers_with_priority.map((d) => `${d.role}(${d.priority})`).join('；')}`,
          `切入 hook：${persona.hooks[0]}`,
        ].join('\n');

        nextActions.push({
          odoo_tool: 'odoo_crm_update',
          reason: '把 brief 摘要写到 lead.description，便于销售后续打开 Odoo 直接看到画像',
          args_draft: {
            lead_id: params.odoo_lead_id,
            description_append: summaryText,
          },
        });
        nextActions.push({
          odoo_tool: 'odoo_create_activity',
          reason: '为该 lead 创建首次接触电话活动（5 天内）',
          args_draft: {
            res_model: 'crm.lead',
            res_id: params.odoo_lead_id,
            activity_type: 'call',
            summary: `首次接触：${persona.hooks[0]}`,
            note: first_message_draft,
            date_deadline: new Date(Date.now() + 5 * 86400000).toISOString().slice(0, 10),
          },
        });
      }

      return {
        success: true,
        brief,
        nextActions,
        hint:
          nextActions.length > 0
            ? '请确认 nextActions 后，依次调用 huihuoyun-odoo 的对应工具。'
            : '若该 lead 已在 Odoo CRM 中，传入 odoo_lead_id 可生成"写回 lead.description"和"创建首次接触活动"两条建议。',
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
