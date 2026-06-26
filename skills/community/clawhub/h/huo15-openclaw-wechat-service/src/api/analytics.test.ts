/**
 * 数据统计（datacube）API 回归测试。
 *
 * 关键不变量：
 *  1. 每个 metric 命中正确的 datacube/<endpoint>，避免错位（曾经的 bug：getuserread vs getuserreadhour）
 *  2. body 形态是 {begin_date, end_date}（snake_case，跟官方文档对齐）
 *  3. METRIC_REGISTRY 完整覆盖 17 个指标
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

vi.mock("../http-client.js", () => ({
  jsonRequest: vi.fn(),
}));

import { jsonRequest } from "../http-client.js";
import {
  ANALYTICS_METRICS,
  METRIC_REGISTRY,
  type AnalyticsMetric,
  type DateRange,
} from "./analytics.js";

const mockedJsonRequest = jsonRequest as unknown as ReturnType<typeof vi.fn>;

const fakeAccount = { accountId: "default" } as unknown as ResolvedWechatServiceAccount;
const fakeTokenHandle = {
  getAccessToken: vi.fn(async () => "TEST_TOKEN"),
} as unknown as AccessTokenHandle;

const range: DateRange = { beginDate: "2026-04-21", endDate: "2026-04-28" };

const EXPECTED_ENDPOINT: Record<AnalyticsMetric, string> = {
  user_summary: "datacube/getusersummary",
  user_cumulate: "datacube/getusercumulate",
  article_summary: "datacube/getarticlesummary",
  article_total: "datacube/getarticletotal",
  user_read: "datacube/getuserread",
  user_read_hour: "datacube/getuserreadhour",
  user_share: "datacube/getusershare",
  user_share_hour: "datacube/getusersharehour",
  upstream_msg: "datacube/getupstreammsg",
  upstream_msg_hour: "datacube/getupstreammsghour",
  upstream_msg_week: "datacube/getupstreammsgweek",
  upstream_msg_month: "datacube/getupstreammsgmonth",
  upstream_msg_dist: "datacube/getupstreammsgdist",
  upstream_msg_dist_week: "datacube/getupstreammsgdistweek",
  upstream_msg_dist_month: "datacube/getupstreammsgdistmonth",
  interface_summary: "datacube/getinterfacesummary",
  interface_summary_hour: "datacube/getinterfacesummaryhour",
};

describe("analytics METRIC_REGISTRY 完整性", () => {
  it("覆盖 17 项指标", () => {
    expect(ANALYTICS_METRICS.length).toBe(17);
  });

  it("ANALYTICS_METRICS 与 EXPECTED_ENDPOINT 一一对应", () => {
    expect(new Set(ANALYTICS_METRICS)).toEqual(new Set(Object.keys(EXPECTED_ENDPOINT)));
  });
});

describe("每个 metric 命中正确的 datacube/<endpoint>", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
    mockedJsonRequest.mockResolvedValue({ list: [] });
    (fakeTokenHandle.getAccessToken as ReturnType<typeof vi.fn>).mockClear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  for (const metric of ANALYTICS_METRICS) {
    const expectedEndpoint = EXPECTED_ENDPOINT[metric];
    it(`${metric} → ${expectedEndpoint}`, async () => {
      const fn = METRIC_REGISTRY[metric];
      await fn({ account: fakeAccount, tokenHandle: fakeTokenHandle, range });
      const args = mockedJsonRequest.mock.calls[0][0];
      expect(args.endpoint).toBe(expectedEndpoint);
      expect(args.method).toBe("POST");
      expect(args.query.access_token).toBe("TEST_TOKEN");
      expect(args.body).toEqual({
        begin_date: "2026-04-21",
        end_date: "2026-04-28",
      });
    });
  }
});

describe("空 list 安全降级", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
  });

  it("当微信返回 {} 时返回 list:[]", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    const fn = METRIC_REGISTRY.user_summary;
    const result = await fn({ account: fakeAccount, tokenHandle: fakeTokenHandle, range });
    expect(result.list).toEqual([]);
  });

  it("当微信返回 {list: undefined} 时返回 list:[]", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ list: undefined });
    const fn = METRIC_REGISTRY.user_summary;
    const result = await fn({ account: fakeAccount, tokenHandle: fakeTokenHandle, range });
    expect(result.list).toEqual([]);
  });
});
