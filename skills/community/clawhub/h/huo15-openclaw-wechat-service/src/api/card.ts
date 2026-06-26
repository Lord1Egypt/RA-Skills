/**
 * **卡券（Card）API —— 精简版**
 *
 * 微信卡券是大型业务套件（优惠券/会员卡/礼品卡/电影票/景点门票/通用卡券……）。
 * 本模块只覆盖最常用的 80% 场景：创建、详情、批量列表、删除、核销、解码。
 *
 * 没覆盖的（按需后续补）：
 *  - 修改库存 (`card/modifystock`)
 *  - 投放卡券（生成卡券二维码 `card/qrcode/create`）
 *  - 货架管理（landingpage / mpnews 集成）
 *  - 卡券扩展类型：会员卡积分 / 礼品卡兑换券 / 电影票座位 / 景点门票 ...
 *  - 第三方门店 / 微信支付商户号绑定
 *
 * 官方文档：
 *   https://developers.weixin.qq.com/doc/offiaccount/WeChat_Coupon_Vouchers/index.html
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type CardCreatePayload = {
  /** 卡券类型 */
  card_type:
    | "GROUPON"
    | "CASH"
    | "DISCOUNT"
    | "GIFT"
    | "GENERAL_COUPON"
    | "MEMBER_CARD"
    | "SCENIC_TICKET"
    | "MOVIE_TICKET"
    | "BOARDING_PASS"
    | "MEETING_TICKET";
  /** 通用 base_info + 卡券类型特定字段，由调用方按官方 schema 拼好 */
  [key: string]: unknown;
};

/**
 * 创建卡券
 *
 * 请求 body 形态由 card_type 决定（常见 base_info: title/code_type/sku/...）。
 * 调用方需对照官方文档拼好完整 payload，本函数只做透传 + access_token 注入。
 *
 * @returns 新卡券 card_id
 */
export async function createCard(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 完整 card 字段（含 card_type / base_info / 子类型 specific 字段） */
  card: CardCreatePayload;
}): Promise<{ cardId: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ card_id?: string }>({
    method: "POST",
    endpoint: "card/create",
    query: { access_token: accessToken },
    body: { card: params.card },
    network: params.account.network,
  });
  return { cardId: String(data.card_id ?? "") };
}

/**
 * 查询卡券详情
 */
export async function getCard(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  cardId: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "card/get",
    query: { access_token: accessToken },
    body: { card_id: params.cardId },
    network: params.account.network,
  });
}

/**
 * 批量查询卡券列表
 */
export async function batchGetCards(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 起始位置 0-based */
  offset?: number;
  /** 一次拉取数量，最大 50 */
  count?: number;
  /** 卡券状态过滤（可选）：CARD_STATUS_NOT_VERIFY/CARD_STATUS_VERIFY_FAIL/CARD_STATUS_VERIFY_OK/CARD_STATUS_USER_DELETE/CARD_STATUS_DISPATCH */
  statusList?: string[];
}): Promise<{ totalNum: number; cardIdList: string[] }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ total_num?: number; card_id_list?: string[] }>({
    method: "POST",
    endpoint: "card/batchget",
    query: { access_token: accessToken },
    body: {
      offset: params.offset ?? 0,
      count: Math.min(params.count ?? 50, 50),
      ...(params.statusList ? { status_list: params.statusList } : {}),
    },
    network: params.account.network,
  });
  return {
    totalNum: Number(data.total_num ?? 0),
    cardIdList: data.card_id_list ?? [],
  };
}

/**
 * 删除卡券
 */
export async function deleteCard(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  cardId: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "card/delete",
    query: { access_token: accessToken },
    body: { card_id: params.cardId },
    network: params.account.network,
  });
}

/**
 * 卡券核销（用 code 标记一次使用）
 *
 * @param code 用户出示的卡券 code
 * @param cardId 可选；非自定义 code 模式下不需要，自定义 code 模式必传
 */
export async function consumeCardCode(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  code: string;
  cardId?: string;
}): Promise<{ cardId: string; openid: string; raw: Record<string, unknown> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ card?: { card_id?: string }; openid?: string }>({
    method: "POST",
    endpoint: "card/code/consume",
    query: { access_token: accessToken },
    body: {
      code: params.code,
      ...(params.cardId ? { card_id: params.cardId } : {}),
    },
    network: params.account.network,
  });
  return {
    cardId: String(data.card?.card_id ?? ""),
    openid: String(data.openid ?? ""),
    raw: data,
  };
}

/**
 * 解码卡券 encrypt_code（扫码 / JS-API 拿到的密文 code → 明文 code）
 */
export async function decryptCardCode(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  encryptCode: string;
}): Promise<{ code: string; raw: Record<string, unknown> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ code?: string }>({
    method: "POST",
    endpoint: "card/code/decrypt",
    query: { access_token: accessToken },
    body: { encrypt_code: params.encryptCode },
    network: params.account.network,
  });
  return { code: String(data.code ?? ""), raw: data };
}
