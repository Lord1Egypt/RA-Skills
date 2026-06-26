/**
 * 订阅通知 API 端点 + payload 形态回归测试。
 *
 * 通过 `vi.mock("../http-client.js")` 拦截 `jsonRequest`，验证 API 包装器：
 *   1. 调用了正确的端点（避免与"模板消息"端点混淆）
 *   2. 把 access_token 放在 query
 *   3. POST body 形态符合官方文档
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

vi.mock("../http-client.js", () => ({
  jsonRequest: vi.fn(),
}));

import { jsonRequest } from "../http-client.js";
import {
  addSubscribeTemplate,
  deleteSubscribeTemplate,
  getSubscribeCategory,
  getSubscribePubTemplateKeywords,
  getSubscribePubTemplateTitles,
  listSubscribeTemplates,
  sendSubscribeMessage,
} from "./subscribe-message.js";
import {
  addTemplate,
  getTemplateLibraryList,
  getTemplateLibraryById,
} from "./template-message.js";

const mockedJsonRequest = jsonRequest as unknown as ReturnType<typeof vi.fn>;

const fakeAccount = { accountId: "default" } as unknown as ResolvedWechatServiceAccount;
const fakeTokenHandle = {
  getAccessToken: vi.fn(async () => "TEST_ACCESS_TOKEN"),
} as unknown as AccessTokenHandle;

describe("subscribe-message API endpoints + payloads", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
    (fakeTokenHandle.getAccessToken as ReturnType<typeof vi.fn>).mockClear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("getSubscribeCategory hits wxaapi/newtmpl/getcategory with GET", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ data: [{ id: 1, name: "教育" }] });
    const result = await getSubscribeCategory({ account: fakeAccount, tokenHandle: fakeTokenHandle });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("wxaapi/newtmpl/getcategory");
    expect(args.method).toBe("GET");
    expect(args.query.access_token).toBe("TEST_ACCESS_TOKEN");
    expect(result.list).toEqual([{ id: 1, name: "教育" }]);
  });

  it("getSubscribePubTemplateTitles caps limit at 30", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ count: 0, data: [] });
    await getSubscribePubTemplateTitles({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      ids: "1,2,3",
      start: 5,
      limit: 100,
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("wxaapi/newtmpl/getpubtemplatetitles");
    expect(args.query.ids).toBe("1,2,3");
    expect(args.query.start).toBe(5);
    expect(args.query.limit).toBe(30);
  });

  it("getSubscribePubTemplateKeywords passes tid in query", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ count: 2, data: [] });
    await getSubscribePubTemplateKeywords({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      tid: "TID_001",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("wxaapi/newtmpl/getpubtemplatekeywords");
    expect(args.query.tid).toBe("TID_001");
  });

  it("addSubscribeTemplate POSTs tid + kidList + sceneDesc", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ priTmplId: "PRI_001" });
    const result = await addSubscribeTemplate({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      tid: "TID_001",
      kidList: [1, 2, 3],
      sceneDesc: "订单提醒",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("wxaapi/newtmpl/addtemplate");
    expect(args.method).toBe("POST");
    expect(args.body).toEqual({ tid: "TID_001", kidList: [1, 2, 3], sceneDesc: "订单提醒" });
    expect(result.priTmplId).toBe("PRI_001");
  });

  it("addSubscribeTemplate omits sceneDesc when not provided", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ priTmplId: "X" });
    await addSubscribeTemplate({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      tid: "TID",
      kidList: [1],
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.body).toEqual({ tid: "TID", kidList: [1] });
    expect(args.body).not.toHaveProperty("sceneDesc");
  });

  it("deleteSubscribeTemplate POSTs priTmplId", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    await deleteSubscribeTemplate({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      priTmplId: "PRI_X",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("wxaapi/newtmpl/deltemplate");
    expect(args.method).toBe("POST");
    expect(args.body).toEqual({ priTmplId: "PRI_X" });
  });

  it("listSubscribeTemplates returns data array", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ data: [{ priTmplId: "A" }, { priTmplId: "B" }] });
    const list = await listSubscribeTemplates({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
    });
    expect(list).toHaveLength(2);
    expect(mockedJsonRequest.mock.calls[0][0].endpoint).toBe("wxaapi/newtmpl/gettemplate");
  });

  it("sendSubscribeMessage uses cgi-bin/message/subscribe/bizsend (not template/subscribe)", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ msgid: 12345 });
    await sendSubscribeMessage({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      touser: "oABC",
      templateId: "PRI_001",
      page: "pages/order/123",
      miniprogram: { appid: "wxAPP", pagepath: "pages/x" },
      data: { thing1: { value: "测试" } },
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    // 关键：不要混到模板消息端点 cgi-bin/message/template/send
    expect(args.endpoint).toBe("cgi-bin/message/subscribe/bizsend");
    expect(args.body.touser).toBe("oABC");
    expect(args.body.template_id).toBe("PRI_001");
    expect(args.body.page).toBe("pages/order/123");
    expect(args.body.miniprogram).toEqual({ appid: "wxAPP", pagepath: "pages/x" });
    expect(args.body.data).toEqual({ thing1: { value: "测试" } });
  });

  it("sendSubscribeMessage omits page/miniprogram when not provided", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    await sendSubscribeMessage({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      touser: "oABC",
      templateId: "PRI_001",
      data: { thing1: { value: "测试" } },
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.body).not.toHaveProperty("page");
    expect(args.body).not.toHaveProperty("miniprogram");
  });
});

describe("template-message new APIs (Phase 1 additions)", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
  });

  it("addTemplate POSTs api_add_template with template_id_short", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ template_id: "TPL_001" });
    const result = await addTemplate({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      templateIdShort: "TM00015",
      keywordIdList: [1, 2],
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("cgi-bin/template/api_add_template");
    expect(args.method).toBe("POST");
    expect(args.body).toEqual({ template_id_short: "TM00015", keyword_id_list: [1, 2] });
    expect(result.templateId).toBe("TPL_001");
  });

  it("addTemplate omits keyword_id_list when not provided", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ template_id: "X" });
    await addTemplate({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      templateIdShort: "TM00001",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.body).toEqual({ template_id_short: "TM00001" });
    expect(args.body).not.toHaveProperty("keyword_id_list");
  });

  it("getTemplateLibraryList caps count at 20", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ total_count: 100, list: [] });
    await getTemplateLibraryList({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      offset: 5,
      count: 50,
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("cgi-bin/template/get_template_library_list");
    expect(args.body).toEqual({ offset: 5, count: 20 });
  });

  it("getTemplateLibraryById POSTs id", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ id: "TM00015", title: "订单提醒" });
    const result = await getTemplateLibraryById({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      id: "TM00015",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("cgi-bin/template/get_template_library_by_id");
    expect(args.body).toEqual({ id: "TM00015" });
    expect(result.title).toBe("订单提醒");
  });
});
