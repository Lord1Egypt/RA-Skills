import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { resolveConfig, type NextAction, offsetDate } from '../shared.js';
import { STAGES, type StageId } from '../domain/stages.js';

export function registerSalesFollowupPlan(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_followup_plan',
    description:
      '基于销售阶段生成未来 14 天的跟进动作清单。支持 5 个阶段：cold（陌拜）/ introduced（初谈）/ proposal（方案）/ negotiation（议价）/ won_or_lost（成交或失败复盘）。输出每天/每个动作的标准 SOP + 可直接喂给 huihuoyun-odoo 的 odoo_create_activity 的 args_draft。本工具不写 Odoo —— 用户确认后通过 huihuoyun-odoo 批量执行。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        stage: {
          type: 'string',
          enum: ['cold', 'introduced', 'proposal', 'negotiation', 'won_or_lost'],
        },
        odoo_lead_id: {
          type: 'number',
          description: '可选。Odoo crm.lead 的 id；提供后会为每个 action 生成 odoo_create_activity 的 args_draft',
        },
        sales_owner_uid: {
          type: 'number',
          description: '可选。Odoo res.users 的 id（销售负责人），写入 activity 的 user_id 字段',
        },
        start_date: {
          type: 'string',
          description: '可选。起算日 yyyy-mm-dd，默认今天',
        },
        skip_weekends: {
          type: 'boolean',
          description: '是否跳过周末（顺延到下一个工作日），默认 true',
          default: true,
        },
      },
      required: ['stage'],
    },
    async execute(
      params: {
        stage: StageId;
        odoo_lead_id?: number;
        sales_owner_uid?: number;
        start_date?: string;
        skip_weekends?: boolean;
      },
      ctx: Record<string, unknown>,
    ) {
      const cfg = resolveConfig((ctx as { pluginConfig?: unknown }).pluginConfig);
      const stage = STAGES[params.stage];
      const skipWeekends = params.skip_weekends ?? true;
      const baseDate = params.start_date ? new Date(params.start_date) : new Date();

      const shiftIfWeekend = (date: string): string => {
        if (!skipWeekends) return date;
        const d = new Date(date);
        const dow = d.getDay();
        if (dow === 6) return offsetDate(2, d);
        if (dow === 0) return offsetDate(1, d);
        return date;
      };

      const plan = stage.actions.map((a, idx) => {
        const rawDate = offsetDate(a.day_offset, baseDate);
        const dueDate = shiftIfWeekend(rawDate);
        return {
          step: idx + 1,
          due_date: dueDate,
          action: a.action,
          channel: a.channel,
        };
      });

      const nextActions: NextAction[] = [];
      if (params.odoo_lead_id !== undefined) {
        for (const p of plan) {
          nextActions.push({
            odoo_tool: 'odoo_create_activity',
            reason: `${stage.display} - 第 ${p.step} 步（${p.due_date}）：${p.action}`,
            args_draft: {
              res_model: 'crm.lead',
              res_id: params.odoo_lead_id,
              activity_type: stage.default_activity_type,
              summary: `[${stage.display}-${p.step}] ${p.action}`,
              date_deadline: p.due_date,
              note: `渠道：${p.channel}\n本阶段目标：${stage.goals.join('；')}\n常见异议：${stage.common_objections.join('；')}`,
              user_id: params.sales_owner_uid,
            },
          });
        }
      }

      return {
        success: true,
        stage_display: stage.display,
        goals: stage.goals,
        common_objections: stage.common_objections,
        promote_signals: stage.promote_signals,
        plan,
        nextActions,
        hint:
          nextActions.length > 0
            ? `已生成 ${nextActions.length} 条 odoo_create_activity 草稿，确认后批量调用 huihuoyun-odoo 创建活动。`
            : '未传入 odoo_lead_id，仅返回 SOP；如需写入 Odoo 创建活动，请重新调用并附带 odoo_lead_id。',
        company_brand: cfg.company_brand,
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
