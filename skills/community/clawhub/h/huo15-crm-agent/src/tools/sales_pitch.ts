import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { resolveConfig, type NextAction, type Tone } from '../shared.js';
import { findScene, fillTemplate, type Scene } from '../domain/pitch_templates.js';

export function registerSalesPitch(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_pitch',
    description:
      '生成场景化的财税获客话术。支持 6 个常见场景：first_contact（首次接触）/ reengage（二次跟进）/ price_objection（价格异议）/ decision_delay（决策拖延）/ referral（转介绍邀约）/ close（促成）。每个场景默认输出 3 种语气变体（formal / warm / neutral）+ 1 条配套下一步动作建议。v0.2 起支持 signals 参数 —— 把 sales_intent_signals 抽出的具体信号传入，话术会"信号驱动"具体写出（参考 Apollo AI Research，比模板话术转化率高一档）。本工具不发消息 —— 输出的 nextActions 建议通过 huihuoyun-odoo 的 odoo_send_message / odoo_send_email 把选中变体发到 lead 沟通历史。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        scene: {
          type: 'string',
          enum: ['first_contact', 'reengage', 'price_objection', 'decision_delay', 'referral', 'close'],
          description: '话术场景',
        },
        client_name: { type: 'string', description: '客户公司名（用于占位符替换）' },
        decision_maker: { type: 'string', description: '决策人称呼，例如"王总"、"张经理"，默认"您"' },
        pain_point: { type: 'string', description: '主痛点，会嵌入话术；推荐先用 sales_lead_brief 拿到再传入' },
        hook: { type: 'string', description: '开场 hook 短句，可来自 sales_lead_brief 或 sales_intent_signals 输出' },
        service: { type: 'string', description: '主推服务，例如"代账"、"汇算清缴"' },
        tone: {
          type: 'string',
          enum: ['formal', 'warm', 'neutral', 'all'],
          description: '语气：formal 正式 / warm 朋友 / neutral 中性 / all 一次返回 3 种',
          default: 'all',
        },
        signals: {
          type: 'array',
          description: 'v0.2 新增。来自 sales_intent_signals 的命中信号；每条 { category, term, hint }。话术会基于强度最高的信号生成具体场景化措辞，而非模板填空。',
          items: {
            type: 'object',
            additionalProperties: false,
            properties: {
              category: { type: 'string', enum: ['tender', 'recruit', 'finance', 'change', 'risk'] },
              term: { type: 'string' },
              hint: { type: 'string' },
            },
            required: ['category', 'term'],
          },
        },
        odoo_lead_id: { type: 'number', description: '可选。如果话术针对 Odoo 中已有 lead，传入 crm.lead id 生成 nextAction' },
      },
      required: ['scene'],
    },
    async execute(
      params: {
        scene: Scene;
        client_name?: string;
        decision_maker?: string;
        pain_point?: string;
        hook?: string;
        service?: string;
        tone?: Tone | 'all';
        signals?: Array<{ category: string; term: string; hint?: string }>;
        odoo_lead_id?: number;
      },
      ctx: Record<string, unknown>,
    ) {
      const cfg = resolveConfig((ctx as { pluginConfig?: unknown }).pluginConfig);
      const tpl = findScene(params.scene);

      const topSignal = params.signals && params.signals.length > 0 ? params.signals[0] : undefined;
      const signalDrivenHook = topSignal
        ? `注意到贵司近期出现"${topSignal.term}"信号 —— ${topSignal.hint ?? '财税服务可介入'}`
        : undefined;
      const signalDrivenPain = topSignal?.hint;

      const slots = {
        client_name: params.client_name ?? '贵司',
        decision_maker: params.decision_maker ?? '您',
        pain_point: params.pain_point ?? signalDrivenPain ?? '日常财税合规',
        hook: params.hook ?? signalDrivenHook ?? '我们最近刚帮一家同行业公司做完类似的事',
        service: params.service ?? cfg.services[0],
        company_brand: cfg.company_brand,
        region: cfg.region,
      };

      const tone = params.tone ?? 'all';
      const variants =
        tone === 'all'
          ? {
              formal: tpl.variants.formal.map((t) => fillTemplate(t, slots)),
              warm: tpl.variants.warm.map((t) => fillTemplate(t, slots)),
              neutral: tpl.variants.neutral.map((t) => fillTemplate(t, slots)),
            }
          : { [tone]: tpl.variants[tone].map((t) => fillTemplate(t, slots)) };

      const nextActions: NextAction[] = [];
      if (params.odoo_lead_id !== undefined) {
        const sample = tone === 'all' ? variants.warm![0] : Object.values(variants)[0]![0];
        nextActions.push({
          odoo_tool: 'odoo_message_post',
          reason: '把推荐话术作为内部备注写到 lead 沟通历史，方便销售直接复制',
          args_draft: {
            res_model: 'crm.lead',
            res_id: params.odoo_lead_id,
            body: `[话术建议-${tpl.display}]\n${sample}\n\n下一步：${tpl.next_step_hint}`,
            internal: true,
          },
        });
      }

      return {
        success: true,
        scene: tpl.scene,
        scene_display: tpl.display,
        next_step_hint: tpl.next_step_hint,
        variants,
        slots_used: slots,
        nextActions,
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
