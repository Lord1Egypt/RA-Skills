/**
 * 卡券（Card）agent tool —— 精简版。
 *
 * actions:
 *   create        创建卡券（card payload 由调用方按官方文档拼好）
 *   get           查卡券详情（by card_id）
 *   batchget      批量查列表（含状态过滤）
 *   delete        删除卡券
 *   consume       核销 code → 标记一次使用
 *   decrypt       解码 encrypt_code（扫码 / JS-API 拿到的密文）
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  batchGetCards,
  consumeCardCode,
  createCard,
  decryptCardCode,
  deleteCard,
  getCard,
  type CardCreatePayload,
} from "../api/card.js";
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
      enum: ["create", "get", "batchget", "delete", "consume", "decrypt"],
      description: "卡券动作。",
    },
    card: {
      type: "object",
      description:
        "create 用：完整 card 字段（含 card_type / base_info / 子类型 specific 字段）。" +
        "card_type 可选：GROUPON / CASH / DISCOUNT / GIFT / GENERAL_COUPON / MEMBER_CARD / SCENIC_TICKET / MOVIE_TICKET / BOARDING_PASS / MEETING_TICKET。" +
        "完整字段对照：https://developers.weixin.qq.com/doc/offiaccount/WeChat_Coupon_Vouchers/Coupon_Card_and_Coupon_Background_Interface_Documentation.html",
      additionalProperties: true,
    },
    cardId: {
      type: "string",
      description: "get / delete / consume（自定义 code 模式必传）用：card_id。",
    },
    offset: { type: "number", description: "batchget 用：起始位置 0-based。" },
    count: { type: "number", description: "batchget 用：拉取数量，最大 50。" },
    statusList: {
      type: "array",
      description:
        "batchget 可选：状态过滤。值取自 CARD_STATUS_NOT_VERIFY / CARD_STATUS_VERIFY_FAIL / CARD_STATUS_VERIFY_OK / CARD_STATUS_USER_DELETE / CARD_STATUS_DISPATCH。",
      items: { type: "string" },
    },
    code: { type: "string", description: "consume 用：用户出示的卡券 code（明文）。" },
    encryptCode: { type: "string", description: "decrypt 用：扫码 / JS-API 拿到的 encrypt_code 密文。" },
  },
} as const;

export function registerCardTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_card",
      label: "WeChat Service Card",
      description:
        "微信卡券（精简）：创建 / 详情 / 批量列表 / 删除 / 核销 / 解码 encrypt_code。覆盖 80% 场景；不含修改库存、卡券二维码生成、积分/兑换券等扩展能力（需要时再加）。",
      parameters,
      async execute(_toolCallId: string, params: Record<string, unknown>) {
        try {
          const { account, tokenHandle } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId as string | undefined,
          });
          const action = String(params.action ?? "");
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_card",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;

          switch (action) {
            case "create": {
              const card = params.card;
              if (!card || typeof card !== "object") {
                throw new Error("card object required for action=create");
              }
              const result = await createCard({
                account,
                tokenHandle,
                card: card as CardCreatePayload,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                cardId: result.cardId,
                summary: `卡券已创建：card_id=${result.cardId}`,
              });
            }
            case "get": {
              const cardId = requireStr(params.cardId, "cardId");
              const raw = await getCard({ account, tokenHandle, cardId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                cardId,
                summary: `卡券 ${cardId} 详情已获取`,
                raw,
              });
            }
            case "batchget": {
              const result = await batchGetCards({
                account,
                tokenHandle,
                offset: params.offset as number | undefined,
                count: params.count as number | undefined,
                statusList: params.statusList as string[] | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                totalNum: result.totalNum,
                count: result.cardIdList.length,
                cardIdList: result.cardIdList,
                summary: `卡券列表（${result.cardIdList.length}/${result.totalNum}）`,
              });
            }
            case "delete": {
              const cardId = requireStr(params.cardId, "cardId");
              await deleteCard({ account, tokenHandle, cardId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `卡券 ${cardId} 已删除`,
              });
            }
            case "consume": {
              const code = requireStr(params.code, "code");
              const result = await consumeCardCode({
                account,
                tokenHandle,
                code,
                cardId: params.cardId as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                cardId: result.cardId,
                openid: result.openid,
                summary: `code=${code} 已核销（card_id=${result.cardId}, openid=${result.openid}）`,
                raw: result.raw,
              });
            }
            case "decrypt": {
              const encryptCode = requireStr(params.encryptCode, "encryptCode");
              const result = await decryptCardCode({
                account,
                tokenHandle,
                encryptCode,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                code: result.code,
                summary: `encrypt_code 已解码 → ${result.code}`,
                raw: result.raw,
              });
            }
            default:
              throw new Error(`Unsupported action: ${action}`);
          }
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
