/**
 * **数据统计（datacube）API**
 *
 * 服务号"数据统计"提供用户、图文、消息、接口四大维度的指标。
 * 所有端点统一在 `https://api.weixin.qq.com/datacube/<metric>` 下，
 * 用普通 access_token（cgi-bin/token）做认证，body 是 `{ begin_date, end_date }`。
 *
 * 区间限制（来自官方文档）：
 *  - getusersummary / getusercumulate: 最大跨度 7 天
 *  - getarticlesummary 等图文类: 最大跨度 1 天（必须 begin_date == end_date）
 *  - getarticletotal: 最大跨度 7 天
 *  - getuserread / getusershare 等: 最大跨度 30 天
 *  - getupstreammsg* (按日): 最大跨度 7 天
 *  - getupstreammsg*week: 最大跨度 30 天
 *  - getupstreammsg*month: 最大跨度 30 天
 *  - getinterfacesummary*: 最大跨度 30 天
 *
 * 调用方应自行约束区间，本模块不做客户端校验（避免和官方文档错位）。
 *
 * 官方文档：
 *   https://developers.weixin.qq.com/doc/offiaccount/Analytics/User_Analysis_Data_Interface.html
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type DateRange = {
  /** YYYY-MM-DD 格式 */
  beginDate: string;
  /** YYYY-MM-DD 格式 */
  endDate: string;
};

export type DatacubeRows<T extends Record<string, unknown> = Record<string, unknown>> = {
  list: T[];
};

/**
 * 内部统一调用：所有 datacube 端点都是同一形态。
 */
async function datacubeQuery(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  endpoint: string;
  range: DateRange;
}): Promise<DatacubeRows> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ list?: Array<Record<string, unknown>> }>({
    method: "POST",
    endpoint: params.endpoint,
    query: { access_token: accessToken },
    body: {
      begin_date: params.range.beginDate,
      end_date: params.range.endDate,
    },
    network: params.account.network,
  });
  return { list: data.list ?? [] };
}

// ---- 用户分析 ----

/** 获取用户增减数据（最大跨度 7 天） */
export async function getUserSummary(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getusersummary" });
}

/** 获取累计用户数据（最大跨度 7 天） */
export async function getUserCumulate(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getusercumulate" });
}

// ---- 图文分析 ----

/** 图文群发每日数据（必须 begin_date == end_date） */
export async function getArticleSummary(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getarticlesummary" });
}

/** 图文群发总数据（最大 7 天） */
export async function getArticleTotal(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getarticletotal" });
}

/** 图文阅读概况（最大 30 天） */
export async function getUserRead(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getuserread" });
}

/** 图文阅读分时数据（必须 begin_date == end_date） */
export async function getUserReadHour(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getuserreadhour" });
}

/** 图文分享转发概况（最大 30 天） */
export async function getUserShare(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getusershare" });
}

/** 图文分享分时数据（必须 begin_date == end_date） */
export async function getUserShareHour(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getusersharehour" });
}

// ---- 消息分析（上行消息） ----

/** 消息分析数据（最大 7 天） */
export async function getUpstreamMsg(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsg" });
}

/** 消息分时数据（必须 begin_date == end_date） */
export async function getUpstreamMsgHour(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsghour" });
}

/** 消息周数据（最大 30 天） */
export async function getUpstreamMsgWeek(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsgweek" });
}

/** 消息月数据（最大 30 天） */
export async function getUpstreamMsgMonth(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsgmonth" });
}

/** 消息发送分布数据（最大 7 天） */
export async function getUpstreamMsgDist(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsgdist" });
}

/** 消息发送分布周数据（最大 30 天） */
export async function getUpstreamMsgDistWeek(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsgdistweek" });
}

/** 消息发送分布月数据（最大 30 天） */
export async function getUpstreamMsgDistMonth(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getupstreammsgdistmonth" });
}

// ---- 接口分析 ----

/** 接口调用概况（最大 30 天） */
export async function getInterfaceSummary(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getinterfacesummary" });
}

/** 接口调用分时数据（必须 begin_date == end_date） */
export async function getInterfaceSummaryHour(params: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; range: DateRange }): Promise<DatacubeRows> {
  return datacubeQuery({ ...params, endpoint: "datacube/getinterfacesummaryhour" });
}

/**
 * **METRIC_REGISTRY**
 *
 * agent tool 把 metric 字符串映射到具体函数；这是同一份 metadata 的真理来源。
 * 同时也用作 `wechat_service_analytics` 的 `metric` enum 来源。
 */
export const METRIC_REGISTRY = {
  user_summary: getUserSummary,
  user_cumulate: getUserCumulate,
  article_summary: getArticleSummary,
  article_total: getArticleTotal,
  user_read: getUserRead,
  user_read_hour: getUserReadHour,
  user_share: getUserShare,
  user_share_hour: getUserShareHour,
  upstream_msg: getUpstreamMsg,
  upstream_msg_hour: getUpstreamMsgHour,
  upstream_msg_week: getUpstreamMsgWeek,
  upstream_msg_month: getUpstreamMsgMonth,
  upstream_msg_dist: getUpstreamMsgDist,
  upstream_msg_dist_week: getUpstreamMsgDistWeek,
  upstream_msg_dist_month: getUpstreamMsgDistMonth,
  interface_summary: getInterfaceSummary,
  interface_summary_hour: getInterfaceSummaryHour,
} as const;

export type AnalyticsMetric = keyof typeof METRIC_REGISTRY;

export const ANALYTICS_METRICS: AnalyticsMetric[] = Object.keys(METRIC_REGISTRY) as AnalyticsMetric[];
