/**
 * 自定义菜单 agent tool：创建/查询/删除 基础菜单 + 个性化菜单。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  createCustomMenu,
  getCustomMenu,
  deleteCustomMenu,
  createConditionalMenu,
  deleteConditionalMenu,
  tryMatchConditionalMenu,
  type WechatMenuButton,
  type ConditionalMatchRule,
} from "../api/menu.js";
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
      enum: ["create", "get", "delete", "create_conditional", "delete_conditional", "try_match"],
      description:
        "menu 操作：create=创建基础菜单，get=查询当前菜单，delete=删除所有菜单（含个性化），create_conditional=创建个性化菜单，delete_conditional=删除指定个性化菜单，try_match=测试某个 openid 命中哪个个性化菜单。",
    },
    buttons: {
      type: "array",
      description:
        "菜单按钮数组（最多 3 个一级按钮，每个一级按钮可含 5 个子按钮）。create / create_conditional 必填。",
      items: { type: "object" },
    },
    matchrule: {
      type: "object",
      description: "create_conditional 用：tag_id / sex / country / province / city / client_platform_type / language。",
      additionalProperties: true,
    },
    menuid: {
      type: "string",
      description: "delete_conditional 用：个性化菜单 menuid。",
    },
    user_id: {
      type: "string",
      description: "try_match 用：openid 或 微信号。",
    },
  },
} as const;

export function registerMenuTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_menu",
      label: "WeChat Service Menu",
      description:
        "微信服务号自定义菜单管理：创建/查询/删除基础菜单与个性化菜单；个性化菜单可按标签、性别、地域、客户端平台、语言匹配展示。",
      parameters,
      async execute(_toolCallId: string, params: {
        accountId?: string;
        action: string;
        buttons?: WechatMenuButton[];
        matchrule?: ConditionalMatchRule;
        menuid?: string;
        user_id?: string;
      }) {
        try {
          const { account, tokenHandle } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId,
          });
          const action = String(params.action ?? "");
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_menu",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (params.action) {
            case "create": {
              if (!Array.isArray(params.buttons)) {
                throw new Error("buttons required for action=create");
              }
              await createCustomMenu({ account, tokenHandle, buttons: params.buttons });
              return buildToolResult({
                ok: true,
                action: "create",
                accountId: account.accountId,
                summary: `已创建公众号菜单（${params.buttons.length} 个一级按钮）`,
              });
            }
            case "get": {
              const result = await getCustomMenu({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action: "get",
                accountId: account.accountId,
                summary: "当前菜单已获取",
                raw: result,
              });
            }
            case "delete": {
              await deleteCustomMenu({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action: "delete",
                accountId: account.accountId,
                summary: "所有菜单（含个性化）已删除",
              });
            }
            case "create_conditional": {
              if (!Array.isArray(params.buttons) || !params.matchrule) {
                throw new Error("buttons and matchrule required for action=create_conditional");
              }
              const result = await createConditionalMenu({
                account,
                tokenHandle,
                buttons: params.buttons,
                matchrule: params.matchrule,
              });
              return buildToolResult({
                ok: true,
                action: "create_conditional",
                accountId: account.accountId,
                menuid: result.menuid,
                summary: `已创建个性化菜单（menuid: ${result.menuid}）`,
              });
            }
            case "delete_conditional": {
              if (!params.menuid) throw new Error("menuid required for action=delete_conditional");
              await deleteConditionalMenu({ account, tokenHandle, menuid: params.menuid });
              return buildToolResult({
                ok: true,
                action: "delete_conditional",
                accountId: account.accountId,
                summary: `个性化菜单 ${params.menuid} 已删除`,
              });
            }
            case "try_match": {
              if (!params.user_id) throw new Error("user_id required for action=try_match");
              const result = await tryMatchConditionalMenu({
                account,
                tokenHandle,
                user_id: params.user_id,
              });
              return buildToolResult({
                ok: true,
                action: "try_match",
                accountId: account.accountId,
                summary: "已返回该用户命中的菜单",
                raw: result,
              });
            }
            default:
              throw new Error(`Unsupported action: ${params.action}`);
          }
        } catch (err) {
          return buildErrorResult({ action: params?.action, error: asErrorMessage(err) });
        }
      },
    };
  });
}
