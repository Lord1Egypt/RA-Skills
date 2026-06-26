/**
 * 卡券（精简版）API 回归测试。
 *
 * 关键不变量：
 *  1. 每个操作命中正确的 card/<endpoint>
 *  2. body 形态对齐官方文档（`{card_id}` / `{code}` / `{encrypt_code}` 等）
 *  3. batchget count 上限截断（最大 50）
 *  4. consume 解析嵌套的 card.card_id
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

vi.mock("../http-client.js", () => ({
  jsonRequest: vi.fn(),
}));

import { jsonRequest } from "../http-client.js";
import {
  batchGetCards,
  consumeCardCode,
  createCard,
  decryptCardCode,
  deleteCard,
  getCard,
} from "./card.js";

const mockedJsonRequest = jsonRequest as unknown as ReturnType<typeof vi.fn>;

const fakeAccount = { accountId: "default" } as unknown as ResolvedWechatServiceAccount;
const fakeTokenHandle = {
  getAccessToken: vi.fn(async () => "TEST_TOKEN"),
} as unknown as AccessTokenHandle;

describe("card API endpoints + body shape", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
    (fakeTokenHandle.getAccessToken as ReturnType<typeof vi.fn>).mockClear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("createCard → card/create with {card: {...}}", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ card_id: "p1pj9F..." });
    const result = await createCard({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      card: {
        card_type: "GENERAL_COUPON",
        general_coupon: { base_info: { brand_name: "辉火云", title: "测试券" } },
      },
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/create");
    expect(args.method).toBe("POST");
    expect(args.body.card.card_type).toBe("GENERAL_COUPON");
    expect(result.cardId).toBe("p1pj9F...");
  });

  it("getCard → card/get with {card_id}", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ card: { card_type: "GENERAL_COUPON" } });
    await getCard({ account: fakeAccount, tokenHandle: fakeTokenHandle, cardId: "p_ABC" });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/get");
    expect(args.body).toEqual({ card_id: "p_ABC" });
  });

  it("batchGetCards caps count at 50", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ total_num: 100, card_id_list: [] });
    await batchGetCards({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      offset: 10,
      count: 200,
      statusList: ["CARD_STATUS_VERIFY_OK"],
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/batchget");
    expect(args.body).toEqual({
      offset: 10,
      count: 50,
      status_list: ["CARD_STATUS_VERIFY_OK"],
    });
  });

  it("batchGetCards omits status_list when not provided", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    await batchGetCards({ account: fakeAccount, tokenHandle: fakeTokenHandle });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.body).toEqual({ offset: 0, count: 50 });
    expect(args.body).not.toHaveProperty("status_list");
  });

  it("deleteCard → card/delete", async () => {
    mockedJsonRequest.mockResolvedValueOnce({});
    await deleteCard({ account: fakeAccount, tokenHandle: fakeTokenHandle, cardId: "p_X" });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/delete");
    expect(args.body).toEqual({ card_id: "p_X" });
  });

  it("consumeCardCode parses nested card.card_id and openid", async () => {
    mockedJsonRequest.mockResolvedValueOnce({
      card: { card_id: "p_ABC" },
      openid: "oUSER1",
      errcode: 0,
    });
    const result = await consumeCardCode({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      code: "1234567890",
      cardId: "p_ABC",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/code/consume");
    expect(args.body).toEqual({ code: "1234567890", card_id: "p_ABC" });
    expect(result.cardId).toBe("p_ABC");
    expect(result.openid).toBe("oUSER1");
  });

  it("consumeCardCode omits card_id when not provided (非自定义 code 模式)", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ card: { card_id: "auto" }, openid: "oUSER" });
    await consumeCardCode({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      code: "1234567890",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.body).toEqual({ code: "1234567890" });
    expect(args.body).not.toHaveProperty("card_id");
  });

  it("decryptCardCode → card/code/decrypt with {encrypt_code}", async () => {
    mockedJsonRequest.mockResolvedValueOnce({ code: "1234567890" });
    const result = await decryptCardCode({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      encryptCode: "ENCRYPT_BLOB",
    });
    const args = mockedJsonRequest.mock.calls[0][0];
    expect(args.endpoint).toBe("card/code/decrypt");
    expect(args.body).toEqual({ encrypt_code: "ENCRYPT_BLOB" });
    expect(result.code).toBe("1234567890");
  });
});
