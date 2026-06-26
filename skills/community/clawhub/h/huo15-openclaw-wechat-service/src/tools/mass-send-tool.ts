/**
 * 群发 agent tool：按标签 / 按 openid 列表 / 预览 / 删除 / 查询状态 / 速度控制。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  massSendByTag,
  massSendByOpenids,
  massSendPreview,
  massSendDelete,
  massSendStatus,
  setMassSendSpeed,
  getMassSendSpeed,
  type MassSendContent,
} from "../api/mass-send.js";
import {
  ACCOUNT_ID_SCHEMA_PROPERTY,
  asErrorMessage,
  buildErrorResult,
  buildToolResult,
  assertAuthorized,
  resolveToolAccount,
  type ToolContext,
} from "./shared.js";

const contentSchema = {
  type: "object",
  description:
    "群发内容：type=text|image|voice|mpnews|mpvideo|wxcard。text 用 content；image 用 media_ids（数组或对象）；其他类型用 media_id。",
  properties: {
    type: {
      type: "string",
      enum: ["text", "image", "voice", "mpnews", "mpvideo", "wxcard"],
    },
    content: { type: "string" },
    media_id: { type: "string" },
    media_ids: {
      description: "type=image 用：string[] 或 {media_ids, recommend?, need_open_comment?, only_fans_can_comment?}",
    },
    card_id: { type: "string", description: "type=wxcard 用" },
  },
  required: ["type"],
} as const;

const parameters = {
  type: "object",
  additionalProperties: false,
  required: ["action"],
  properties: {
    accountId: ACCOUNT_ID_SCHEMA_PROPERTY,
    action: {
      type: "string",
      enum: [
        "send_by_tag",
        "send_by_openids",
        "preview",
        "delete",
        "status",
        "set_speed",
        "get_speed",
      ],
      description:
        "群发动作。send_by_tag / send_by_openids 触发正式群发；preview 用于 1 人预览；delete 用 msg_id 撤回；status 查看群发状态；set_speed 调整发送速度。",
    },
    is_to_all: { type: "boolean", description: "send_by_tag 用：是否全量发送。" },
    tag_id: { type: "number", description: "send_by_tag 用：标签 id（is_to_all=false 时必填）。" },
    touser: {
      type: "array",
      items: { type: "string" },
      description: "send_by_openids 用：openid 列表（至少 2 人）。",
    },
    preview_openid: { type: "string", description: "preview 用：openid。" },
    preview_wxname: { type: "string", description: "preview 用：微信号。" },
    content: contentSchema,
    msg_id: { type: "string", description: "delete / status 用：群发 msg_id。" },
    article_idx: { type: "number", description: "delete 用：要删的图文 index，默认 0 删全部。" },
    send_ignore_reprint: { type: "number", enum: [0, 1], description: "mpnews 被判定转载时是否继续发，默认 0。" },
    speed: {
      type: "number",
      enum: [0, 1, 2, 3, 4],
      description: "set_speed 用：0=80w/min, 1=60w/min, 2=45w/min, 3=30w/min, 4=10w/min。",
    },
  },
} as const;

export function registerMassSendTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_mass_send",
      label: "WeChat Service Mass Send",
      description:
        "微信服务号群发：按标签全量/按 openid 列表群发文本/图片/语音/视频/图文/卡券，支持 1 人预览、撤回、状态查询、速度控制。",
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
            toolName: "wechat_service_mass_send",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "send_by_tag": {
              const content = params.content as MassSendContent | undefined;
              if (!content) throw new Error("content required for action=send_by_tag");
              const result = await massSendByTag({
                account,
                tokenHandle,
                is_to_all: params.is_to_all as boolean | undefined,
                tag_id: params.tag_id as number | undefined,
                content,
                send_ignore_reprint: params.send_ignore_reprint as 0 | 1 | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                msg_id: result.msg_id,
                msg_data_id: result.msg_data_id,
                summary: `按标签群发已提交（msg_id: ${result.msg_id ?? "-"}）`,
              });
            }
            case "send_by_openids": {
              const content = params.content as MassSendContent | undefined;
              if (!content) throw new Error("content required for action=send_by_openids");
              const touser = params.touser;
              if (!Array.isArray(touser) || touser.length < 2) {
                throw new Error("touser required (>= 2 openids)");
              }
              const result = await massSendByOpenids({
                account,
                tokenHandle,
                touser: touser as string[],
                content,
                send_ignore_reprint: params.send_ignore_reprint as 0 | 1 | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                msg_id: result.msg_id,
                msg_data_id: result.msg_data_id,
                summary: `按 openid 群发已提交（${touser.length} 人，msg_id: ${result.msg_id ?? "-"}）`,
              });
            }
            case "preview": {
              const content = params.content as MassSendContent | undefined;
              if (!content) throw new Error("content required for action=preview");
              const result = await massSendPreview({
                account,
                tokenHandle,
                touser: params.preview_openid as string | undefined,
                towxname: params.preview_wxname as string | undefined,
                content,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                msg_id: result.msg_id,
                summary: "预览消息已提交",
              });
            }
            case "delete": {
              const msgId = requireStr(params.msg_id, "msg_id");
              await massSendDelete({
                account,
                tokenHandle,
                msg_id: Number(msgId),
                article_idx: params.article_idx as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `群发 ${msgId} 已撤回`,
              });
            }
            case "status": {
              const msgId = requireStr(params.msg_id, "msg_id");
              const result = await massSendStatus({ account, tokenHandle, msg_id: msgId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `群发 ${msgId} 状态已获取`,
                raw: result,
              });
            }
            case "set_speed": {
              const speed = params.speed;
              if (typeof speed !== "number") throw new Error("speed required");
              await setMassSendSpeed({ account, tokenHandle, speed: speed as 0 | 1 | 2 | 3 | 4 });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `群发速度已设为 ${speed}`,
              });
            }
            case "get_speed": {
              const result = await getMassSendSpeed({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `当前速度：speed=${result.speed} realspeed=${result.realspeed}`,
                raw: result,
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
