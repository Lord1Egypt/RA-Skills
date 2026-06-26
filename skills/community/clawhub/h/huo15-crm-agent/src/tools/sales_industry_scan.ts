import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { resolveConfig } from '../shared.js';
import { thisMonth, nextMonths } from '../domain/industry_calendar.js';

export function registerSalesIndustryScan(api: OpenClawPluginApi) {
  api.registerTool({
    name: 'sales_industry_scan',
    description:
      '财税行业历法扫描。基于当前日期返回本月/未来 N 月（默认 3 月）的关键政策节点（汇算清缴、申报、高新认定窗口、研发加计、年报等）+ 配套外呼话术 hook。用于"主题化群发"前抓取一个时点 hook，让陌拜话术有具体由头。建议把扫描结果作为 hook 参数传给 sales_pitch / sales_lead_brief 工具。',
    parameters: {
      type: 'object',
      additionalProperties: false,
      properties: {
        months_ahead: {
          type: 'number',
          minimum: 1,
          maximum: 6,
          description: '向后看几个月（含当月），默认 3',
          default: 3,
        },
        services_filter: {
          type: 'array',
          items: { type: 'string' },
          description: '只返回与这些服务方向相关的 hook（命中关键词即保留）；不传则返回全部',
        },
        date: {
          type: 'string',
          description: '可选。基准日 yyyy-mm-dd，默认今天',
        },
      },
    },
    async execute(
      params: { months_ahead?: number; services_filter?: string[]; date?: string },
      ctx: Record<string, unknown>,
    ) {
      const cfg = resolveConfig((ctx as { pluginConfig?: unknown }).pluginConfig);
      const baseDate = params.date ? new Date(params.date) : new Date();
      const monthsAhead = params.months_ahead ?? 3;

      const filterByServices = params.services_filter && params.services_filter.length > 0
        ? params.services_filter.map((s) => s.toLowerCase())
        : null;

      const matchHook = (text: string): boolean => {
        if (!filterByServices) return true;
        return filterByServices.some((s) => text.toLowerCase().includes(s));
      };

      const current = thisMonth(baseDate);
      const upcoming = nextMonths(monthsAhead, baseDate);

      const result = upcoming.map((m, idx) => ({
        month: m.month,
        is_current: idx === 0,
        events: m.events,
        pitch_hooks: m.pitch_hooks.filter((h) => matchHook(h)),
      }));

      const top_hooks_now = current.pitch_hooks.filter((h) => matchHook(h));

      return {
        success: true,
        base_date: baseDate.toISOString().slice(0, 10),
        services_filter: params.services_filter ?? cfg.services,
        current_month: current.month,
        top_hooks_now,
        upcoming_months: result,
        hint:
          'top_hooks_now 是本月可立即使用的 hook，建议作为 sales_pitch 工具的 hook 参数。如要做"主题群发"，先用 huihuoyun-odoo 的 odoo_search 拉出某 stage 的 leads，再 sales_pitch 配合每条 lead 个性化生成话术。',
      };
    },
  } as unknown as Parameters<typeof api.registerTool>[0]);
}
