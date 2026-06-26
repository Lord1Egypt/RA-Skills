/**
 * 数据统计 agent tool（datacube）。
 *
 * 单一 action 设计：通过 `metric` 参数选择 17 个指标之一，避免在 tool 级别炸出
 * 一堆 actions 让 LLM 选错。所有指标共用 `{ beginDate, endDate }` 入参。
 *
 * 使用提示：
 *  - 区间限制由调用方控制（小时类必须 begin == end，天类 7d/30d 不一）
 *  - LLM 通常先 list_metrics 一次，再选具体 metric
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  ANALYTICS_METRICS,
  METRIC_REGISTRY,
  type AnalyticsMetric,
  type DateRange,
} from "../api/analytics.js";
import {
  ACCOUNT_ID_SCHEMA_PROPERTY,
  asErrorMessage,
  buildErrorResult,
  buildToolResult,
  assertAuthorized,
  resolveToolAccount,
  type ToolContext,
} from "./shared.js";

const parameters = {
  type: "object",
  additionalProperties: false,
  required: ["action"],
  properties: {
    accountId: ACCOUNT_ID_SCHEMA_PROPERTY,
    action: {
      type: "string",
      enum: ["list_metrics", "query"],
      description: "list_metrics 列出所有可用指标；query 拉具体指标的数据。",
    },
    metric: {
      type: "string",
      enum: ANALYTICS_METRICS,
      description:
        "query 用：指标名。user_summary/user_cumulate（用户增减/累计） · article_summary/article_total/user_read/user_read_hour/user_share/user_share_hour（图文阅读分享） · upstream_msg/_hour/_week/_month/_dist/_dist_week/_dist_month（消息分析） · interface_summary/_hour（接口调用）。",
    },
    beginDate: {
      type: "string",
      description: "query 用：开始日期，YYYY-MM-DD。",
    },
    endDate: {
      type: "string",
      description: "query 用：结束日期，YYYY-MM-DD。注意官方对各指标有跨度限制（_hour 类必须 begin==end，多数 _summary 是 7 天，_share/_read 是 30 天）。",
    },
  },
} as const;

export function registerAnalyticsTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_analytics",
      label: "WeChat Service Analytics",
      description:
        "微信公众号数据统计（datacube）：用户增减、累计用户、图文阅读分享、消息上行/下行、接口调用四大维度共 17 项指标。先 list_metrics 看支持的 metric，再 query 拉数据。",
      parameters,
      async execute(_toolCallId: string, params: Record<string, unknown>) {
        try {
          const action = String(params.action ?? "");

          if (action === "list_metrics") {
            return buildToolResult({
              ok: true,
              action,
              count: ANALYTICS_METRICS.length,
              metrics: ANALYTICS_METRICS,
              summary: `${ANALYTICS_METRICS.length} 项指标可用`,
            });
          }

          if (action !== "query") {
            throw new Error(`Unsupported action: ${action}`);
          }

          const { account, tokenHandle } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId as string | undefined,
          });
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_analytics",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          const metric = String(params.metric ?? "") as AnalyticsMetric;
          if (!ANALYTICS_METRICS.includes(metric)) {
            throw new Error(
              `metric 必填，且必须是以下之一：${ANALYTICS_METRICS.join(", ")}`,
            );
          }
          const beginDate = requireStr(params.beginDate, "beginDate");
          const endDate = requireStr(params.endDate, "endDate");
          assertIsoDate(beginDate, "beginDate");
          assertIsoDate(endDate, "endDate");

          const range: DateRange = { beginDate, endDate };
          const fn = METRIC_REGISTRY[metric];
          const result = await fn({ account, tokenHandle, range });
          return buildToolResult({
            ok: true,
            action,
            accountId: account.accountId,
            metric,
            beginDate,
            endDate,
            count: result.list.length,
            list: result.list,
            summary: `${metric} ${beginDate}~${endDate}：${result.list.length} 行`,
          });
        } catch (err) {
          return buildErrorResult({ action: String(params?.action), error: asErrorMessage(err) });
        }
      },
    };
  });
}

function requireStr(value: unknown, name: string): string {
  const str = typeof value === "string" ? value.trim() : "";
  if (!str) throw new Error(`${name} required`);
  return str;
}

function assertIsoDate(value: string, name: string): void {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throw new Error(`${name} must be YYYY-MM-DD, got: ${value}`);
  }
}
