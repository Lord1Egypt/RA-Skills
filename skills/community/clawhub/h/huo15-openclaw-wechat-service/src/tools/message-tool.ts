/**
 * 消息下发 agent tool：客服消息 + 模板消息 + 一次性订阅消息 + 输入状态。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  sendCustomerServiceMessage,
  sendCustomerServiceTyping,
  type CustomerServiceMessage,
} from "../api/customer-service.js";
import {
  sendTemplateMessage,
  listTemplates,
  deleteTemplate,
  setIndustry,
  getIndustry,
  sendSubscribeOnceMessage,
  addTemplate,
  getTemplateLibraryList,
  getTemplateLibraryById,
  type TemplateDataEntry,
} from "../api/template-message.js";
import {
  getSubscribeCategory,
  getSubscribePubTemplateTitles,
  getSubscribePubTemplateKeywords,
  addSubscribeTemplate,
  deleteSubscribeTemplate,
  listSubscribeTemplates,
  sendSubscribeMessage,
} from "../api/subscribe-message.js";
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
      enum: [
        "send_text",
        "send_image",
        "send_voice",
        "send_video",
        "send_news",
        "send_mpnews",
        "send_menu",
        "send_miniprogram",
        "typing",
        "send_template",
        "list_templates",
        "delete_template",
        "set_industry",
        "get_industry",
        "send_subscribe_once",
        "add_template",
        "list_template_library",
        "get_template_library_item",
        "subscribe_get_category",
        "subscribe_pub_titles",
        "subscribe_pub_keywords",
        "subscribe_add_template",
        "subscribe_delete_template",
        "subscribe_list_templates",
        "send_subscribe",
      ],
      description: "消息下发动作。send_* 为客服消息（需 48h 窗口内）；模板消息: send_template / list_templates / add_template / delete_template / set_industry / get_industry / list_template_library / get_template_library_item；一次性订阅: send_subscribe_once；长期订阅通知（subscribe notification）: subscribe_get_category / subscribe_pub_titles / subscribe_pub_keywords / subscribe_add_template / subscribe_delete_template / subscribe_list_templates / send_subscribe。",
    },
    touser: { type: "string", description: "接收者 openid（必填，大多数 action 需要）" },
    content: { type: "string", description: "send_text：文本内容；typing 不使用。" },
    mediaId: { type: "string", description: "send_image/voice/video/mpnews 用：media_id。" },
    thumbMediaId: { type: "string", description: "send_video 用：封面 thumb_media_id。" },
    title: { type: "string", description: "send_video/send_miniprogram 用：标题。" },
    description: { type: "string", description: "send_video 用：描述。" },
    articles: {
      type: "array",
      description: "send_news 用：图文列表，每项 {title, description?, url, picurl?}。最多 8 条。",
      items: {
        type: "object",
        properties: {
          title: { type: "string" },
          description: { type: "string" },
          url: { type: "string" },
          picurl: { type: "string" },
        },
        required: ["title", "url"],
      },
    },
    menu: {
      type: "object",
      description: "send_menu 用：{head_content, list:[{id,content}], tail_content?}",
      properties: {
        head_content: { type: "string" },
        tail_content: { type: "string" },
        list: {
          type: "array",
          items: {
            type: "object",
            properties: { id: { type: "string" }, content: { type: "string" } },
            required: ["id", "content"],
          },
        },
      },
      required: ["head_content", "list"],
    },
    miniprogram: {
      type: "object",
      description: "send_miniprogram 用：{appid, pagepath, thumb_media_id}",
      properties: {
        appid: { type: "string" },
        pagepath: { type: "string" },
        thumb_media_id: { type: "string" },
      },
      required: ["appid", "pagepath", "thumb_media_id"],
    },
    typingCommand: {
      type: "string",
      enum: ["Typing", "CancelTyping"],
      description: "typing 用。",
    },
    kfAccount: { type: "string", description: "send_text 可选：以某个客服帐号下发。" },
    templateId: { type: "string", description: "send_template / delete_template / send_subscribe_once 用。" },
    url: { type: "string", description: "send_template / send_subscribe_once 用：跳转链接。" },
    templateData: {
      type: "object",
      description: "send_template / send_subscribe_once 用：{key: {value, color?}} 映射。",
      additionalProperties: true,
    },
    clientMsgId: { type: "string", description: "send_template 用：去重 id。" },
    templateMiniprogram: {
      type: "object",
      description: "send_template 用：跳转小程序 {appid, pagepath}。",
      properties: {
        appid: { type: "string" },
        pagepath: { type: "string" },
      },
      required: ["appid", "pagepath"],
    },
    industryId1: { type: "string", description: "set_industry 用：主营行业 id（字符串）。" },
    industryId2: { type: "string", description: "set_industry 用：副营行业 id（字符串）。" },
    subscribeScene: { type: "string", description: "send_subscribe_once 用：订阅场景值。" },
    subscribeTitle: { type: "string", description: "send_subscribe_once 用：消息主标题。" },
    templateIdShort: {
      type: "string",
      description: "add_template / get_template_library_item 用：公模板库编号（如 TM00015）。",
    },
    keywordIdList: {
      type: "array",
      description: "add_template 可选：模板库 v2 起允许指定关键词 id 列表。",
      items: { type: "number" },
    },
    libraryOffset: { type: "number", description: "list_template_library 用：起始位置 0-based。" },
    libraryCount: { type: "number", description: "list_template_library 用：拉取数量，最大 20。" },
    categoryIds: {
      type: "string",
      description: "subscribe_pub_titles 用：类目 id 列表（逗号分隔字符串），从 subscribe_get_category 获取。",
    },
    pubTemplateStart: { type: "number", description: "subscribe_pub_titles 用：起始位置 0-based。" },
    pubTemplateLimit: { type: "number", description: "subscribe_pub_titles 用：拉取数量，最大 30。" },
    tid: {
      type: "string",
      description: "subscribe_pub_keywords / subscribe_add_template 用：公模板库 tid。",
    },
    kidList: {
      type: "array",
      description: "subscribe_add_template 用：选用的关键词 id 列表，来自 subscribe_pub_keywords。",
      items: { type: "number" },
    },
    sceneDesc: {
      type: "string",
      description: "subscribe_add_template 用：业务场景描述（≤15 字）。",
    },
    priTmplId: {
      type: "string",
      description: "subscribe_delete_template / send_subscribe 用：个人订阅模板 id。",
    },
    page: {
      type: "string",
      description: "send_subscribe 可选：跳转页面 path。",
    },
    subscribeMiniprogram: {
      type: "object",
      description: "send_subscribe 可选：跳转小程序 {appid, pagepath}。",
      properties: {
        appid: { type: "string" },
        pagepath: { type: "string" },
      },
      required: ["appid", "pagepath"],
    },
  },
} as const;

export function registerMessageTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_message",
      label: "WeChat Service Message",
      description:
        "微信服务号消息下发：客服消息（文本/图片/语音/视频/图文/小程序卡片/菜单消息）、模板消息、一次性订阅消息、输入状态指示。客服消息需用户在过去 48 小时内与公众号有交互。",
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
            toolName: "wechat_service_message",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "send_text": {
              const touser = requireStr(params.touser, "touser");
              const content = requireStr(params.content, "content");
              const msg: CustomerServiceMessage = {
                touser,
                msgtype: "text",
                text: { content },
                ...(params.kfAccount
                  ? { customservice: { kf_account: String(params.kfAccount) } }
                  : {}),
              };
              await sendCustomerServiceMessage({ account, tokenHandle, message: msg });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `文本消息已下发（${touser}，${content.length} chars）`,
              });
            }
            case "send_image": {
              const touser = requireStr(params.touser, "touser");
              const mediaId = requireStr(params.mediaId, "mediaId");
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: { touser, msgtype: "image", image: { media_id: mediaId } },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `图片消息已下发（${touser}）`,
              });
            }
            case "send_voice": {
              const touser = requireStr(params.touser, "touser");
              const mediaId = requireStr(params.mediaId, "mediaId");
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: { touser, msgtype: "voice", voice: { media_id: mediaId } },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `语音消息已下发（${touser}）`,
              });
            }
            case "send_video": {
              const touser = requireStr(params.touser, "touser");
              const mediaId = requireStr(params.mediaId, "mediaId");
              const thumbMediaId = requireStr(params.thumbMediaId, "thumbMediaId");
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: {
                  touser,
                  msgtype: "video",
                  video: {
                    media_id: mediaId,
                    thumb_media_id: thumbMediaId,
                    title: params.title as string | undefined,
                    description: params.description as string | undefined,
                  },
                },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `视频消息已下发（${touser}）`,
              });
            }
            case "send_news": {
              const touser = requireStr(params.touser, "touser");
              const articles = params.articles;
              if (!Array.isArray(articles) || articles.length === 0) {
                throw new Error("articles required for action=send_news");
              }
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: {
                  touser,
                  msgtype: "news",
                  news: { articles: articles as Array<{ title: string; url: string }> },
                },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `图文消息已下发（${touser}，${articles.length} 条）`,
              });
            }
            case "send_mpnews": {
              const touser = requireStr(params.touser, "touser");
              const mediaId = requireStr(params.mediaId, "mediaId");
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: { touser, msgtype: "mpnews", mpnews: { media_id: mediaId } },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `图文消息（mpnews）已下发（${touser}）`,
              });
            }
            case "send_menu": {
              const touser = requireStr(params.touser, "touser");
              const menu = params.menu;
              if (!menu || typeof menu !== "object") {
                throw new Error("menu required for action=send_menu");
              }
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: {
                  touser,
                  msgtype: "msgmenu",
                  msgmenu: menu as CustomerServiceMessage extends infer T
                    ? T extends { msgtype: "msgmenu"; msgmenu: infer M }
                      ? M
                      : never
                    : never,
                },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `菜单消息已下发（${touser}）`,
              });
            }
            case "send_miniprogram": {
              const touser = requireStr(params.touser, "touser");
              const title = requireStr(params.title, "title");
              const mini = params.miniprogram as {
                appid?: string;
                pagepath?: string;
                thumb_media_id?: string;
              };
              if (!mini?.appid || !mini?.pagepath || !mini?.thumb_media_id) {
                throw new Error("miniprogram.{appid,pagepath,thumb_media_id} required");
              }
              await sendCustomerServiceMessage({
                account,
                tokenHandle,
                message: {
                  touser,
                  msgtype: "miniprogrampage",
                  miniprogrampage: {
                    title,
                    appid: mini.appid,
                    pagepath: mini.pagepath,
                    thumb_media_id: mini.thumb_media_id,
                  },
                },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `小程序卡片已下发（${touser}）`,
              });
            }
            case "typing": {
              const touser = requireStr(params.touser, "touser");
              await sendCustomerServiceTyping({
                account,
                tokenHandle,
                touser,
                command: (params.typingCommand as "Typing" | "CancelTyping" | undefined) ?? "Typing",
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已下发输入状态：${touser}`,
              });
            }
            case "send_template": {
              const touser = requireStr(params.touser, "touser");
              const templateId = requireStr(params.templateId, "templateId");
              const data = params.templateData;
              if (!data || typeof data !== "object") {
                throw new Error("templateData required for action=send_template");
              }
              const result = await sendTemplateMessage({
                account,
                tokenHandle,
                message: {
                  touser,
                  template_id: templateId,
                  url: params.url as string | undefined,
                  miniprogram: params.templateMiniprogram as
                    | { appid: string; pagepath: string }
                    | undefined,
                  data: data as Record<string, TemplateDataEntry>,
                  client_msg_id: params.clientMsgId as string | undefined,
                },
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                msgid: result.msgid,
                summary: `模板消息已下发（${touser}，msgid: ${result.msgid}）`,
              });
            }
            case "list_templates": {
              const templates = await listTemplates({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: templates.length,
                templates,
                summary: `已获取模板列表（${templates.length} 条）`,
              });
            }
            case "delete_template": {
              const templateId = requireStr(params.templateId, "templateId");
              await deleteTemplate({ account, tokenHandle, templateId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `模板 ${templateId} 已删除`,
              });
            }
            case "set_industry": {
              const industryId1 = requireStr(params.industryId1, "industryId1");
              await setIndustry({
                account,
                tokenHandle,
                industry_id1: industryId1,
                industry_id2: params.industryId2 as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "行业设置已更新（年度 2 次上限）",
              });
            }
            case "get_industry": {
              const result = await getIndustry({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "当前行业配置已获取",
                raw: result,
              });
            }
            case "send_subscribe_once": {
              const touser = requireStr(params.touser, "touser");
              const templateId = requireStr(params.templateId, "templateId");
              const scene = requireStr(params.subscribeScene, "subscribeScene");
              const title = requireStr(params.subscribeTitle, "subscribeTitle");
              const data = params.templateData;
              if (!data || typeof data !== "object") {
                throw new Error("templateData required for action=send_subscribe_once");
              }
              await sendSubscribeOnceMessage({
                account,
                tokenHandle,
                touser,
                template_id: templateId,
                scene,
                title,
                url: params.url as string | undefined,
                data: data as Record<string, { value: string; color?: string }>,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `一次性订阅消息已下发（${touser}）`,
              });
            }
            case "add_template": {
              const templateIdShort = requireStr(params.templateIdShort, "templateIdShort");
              const result = await addTemplate({
                account,
                tokenHandle,
                templateIdShort,
                keywordIdList: params.keywordIdList as number[] | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                templateId: result.templateId,
                summary: `已选用模板 ${templateIdShort} → ${result.templateId}`,
              });
            }
            case "list_template_library": {
              const result = await getTemplateLibraryList({
                account,
                tokenHandle,
                offset: params.libraryOffset as number | undefined,
                count: params.libraryCount as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                totalCount: result.totalCount,
                count: result.list.length,
                templates: result.list,
                summary: `公模板库（${result.list.length}/${result.totalCount}）`,
              });
            }
            case "get_template_library_item": {
              const id = requireStr(params.templateIdShort, "templateIdShort");
              const raw = await getTemplateLibraryById({ account, tokenHandle, id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `公模板 ${id} 详情已获取`,
                raw,
              });
            }
            case "subscribe_get_category": {
              const result = await getSubscribeCategory({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: result.list.length,
                categories: result.list,
                summary: `订阅通知类目（${result.list.length} 项）`,
              });
            }
            case "subscribe_pub_titles": {
              const ids = requireStr(params.categoryIds, "categoryIds");
              const result = await getSubscribePubTemplateTitles({
                account,
                tokenHandle,
                ids,
                start: params.pubTemplateStart as number | undefined,
                limit: params.pubTemplateLimit as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: result.list.length,
                totalCount: result.count,
                templates: result.list,
                summary: `公模板标题（${result.list.length}/${result.count}）`,
              });
            }
            case "subscribe_pub_keywords": {
              const tid = requireStr(params.tid, "tid");
              const result = await getSubscribePubTemplateKeywords({
                account,
                tokenHandle,
                tid,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: result.count,
                keywords: result.list,
                summary: `tid=${tid} 关键词（${result.count} 项）`,
              });
            }
            case "subscribe_add_template": {
              const tid = requireStr(params.tid, "tid");
              const kidList = params.kidList;
              if (!Array.isArray(kidList) || kidList.length === 0) {
                throw new Error("kidList required (number[]) for action=subscribe_add_template");
              }
              const result = await addSubscribeTemplate({
                account,
                tokenHandle,
                tid,
                kidList: kidList as number[],
                sceneDesc: params.sceneDesc as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                priTmplId: result.priTmplId,
                summary: `订阅模板已选用：tid=${tid} → priTmplId=${result.priTmplId}`,
              });
            }
            case "subscribe_delete_template": {
              const priTmplId = requireStr(params.priTmplId, "priTmplId");
              await deleteSubscribeTemplate({ account, tokenHandle, priTmplId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `订阅模板 ${priTmplId} 已删除`,
              });
            }
            case "subscribe_list_templates": {
              const list = await listSubscribeTemplates({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: list.length,
                templates: list,
                summary: `已选用订阅模板（${list.length} 条）`,
              });
            }
            case "send_subscribe": {
              const touser = requireStr(params.touser, "touser");
              const priTmplId = requireStr(params.priTmplId, "priTmplId");
              const data = params.templateData;
              if (!data || typeof data !== "object") {
                throw new Error("templateData required for action=send_subscribe");
              }
              const result = await sendSubscribeMessage({
                account,
                tokenHandle,
                touser,
                templateId: priTmplId,
                page: params.page as string | undefined,
                miniprogram: params.subscribeMiniprogram as
                  | { appid: string; pagepath: string }
                  | undefined,
                data: data as Record<string, { value: string; color?: string }>,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                msgid: result.msgid,
                summary: `订阅通知已下发（${touser}${result.msgid != null ? `，msgid=${result.msgid}` : ""}）`,
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
