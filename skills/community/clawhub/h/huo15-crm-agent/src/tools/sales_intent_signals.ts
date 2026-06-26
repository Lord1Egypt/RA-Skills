import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { NextAction } from '../shared.js';
import {
  matchSignals,
  summarizeSignals,
  FINANCE_TAX_SIGNALS,
  type SignalCategory,
} from '../domain/signal_dictionary.js';

export function registerSalesIntentSignals(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_intent_signals',
    description:
      '财税获客 / 拓客：从用户喂入的原文（招聘描述 / 招标公告 / 工商变更 / 新闻 / 风险通告等）中识别财税意向信号。基于内置《财税行业获客信号词典》（5 大类 30+ 条），命中即加权打分，输出"高 / 中 / 低 / 无"意向等级 + 命中详情 + 财税解读。本工具不联网 —— 用户需自己用其他工具（huo15-searxng / sales_company_detail / RSS / 招聘网站）抓取原文再喂入。输出可加权到 sales_lead_score 或喂给 sales_pitch 生成信号驱动话术。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        raw_texts: {
          type: 'array',
          items: { type: 'string' },
          minItems: 1,
          description: '原文数组。每条 ≤ 5000 字。可以是招聘 JD / 招标公告 / 新闻 / 工商变更条目等。',
        },
        company_hint: { type: 'string', description: '关联公司名（用于报告）' },
        signal_categories: {
          type: 'array',
          items: { type: 'string', enum: ['tender', 'recruit', 'finance', 'change', 'risk'] },
          description: '只识别这些类别的信号；不传 = 全开 5 类',
        },
      },
      required: ['raw_texts'],
    },
    async execute(
      params: {
        raw_texts: string[];
        company_hint?: string;
        signal_categories?: SignalCategory[];
      },
      _ctx: Record<string, unknown>,
    ) {
      const matches = matchSignals(params.raw_texts, params.signal_categories);
      const summary = summarizeSignals(matches);

      const nextActions: NextAction[] = [];

      if (summary.total_weight > 0) {
        // 建议把 total_weight 加到 sales_lead_score 的备注里
        nextActions.push({
          odoo_tool: 'sales_lead_score',
          reason: `已识别 ${matches.length} 条信号（${summary.inferred_intent}意向，累计权重 ${summary.total_weight}），建议把信号摘要加到 lead 的 notes 里再打分`,
          args_draft: {
            leads: [
              {
                name: params.company_hint ?? '（待填）',
                notes: matches
                  .slice(0, 8)
                  .map((m) => `[${m.category}] ${m.term}（${m.hint}）`)
                  .join('；'),
              },
            ],
          },
        });

        // 建议用强信号喂 sales_pitch 生成针对性话术
        const top = matches.slice().sort((a, b) => b.weight - a.weight)[0];
        if (top) {
          nextActions.push({
            odoo_tool: 'sales_pitch',
            reason: `最强信号"${top.term}"可直接作为话术 hook，建议 sales_pitch 用这个信号驱动`,
            args_draft: {
              scene: 'first_contact',
              client_name: params.company_hint,
              pain_point: top.hint,
              hook: `注意到贵司近期出现"${top.term}"信号 —— ${top.hint}`,
              signals: matches.slice(0, 5).map((m) => ({
                category: m.category,
                term: m.term,
                hint: m.hint,
              })),
            },
          });
        }
      }

      return {
        success: true,
        company: params.company_hint,
        summary,
        matches,
        dictionary_size: FINANCE_TAX_SIGNALS.length,
        nextActions,
        hint:
          summary.total_weight === 0
            ? '原文中未匹配到任何财税信号词条。建议：① 检查输入是否真的是招聘 / 招标 / 工商 / 新闻原文；② 若行业特殊，可能词典没覆盖 —— 反馈给绿火维护者扩充。'
            : `识别 ${matches.length} 条信号（${summary.inferred_intent}意向）。建议结合 sales_lead_score 综合打分，或用最强信号喂 sales_pitch 生成"信号驱动话术"——比模板话术转化率高一档。`,
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
