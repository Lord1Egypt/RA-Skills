/**
 * 用户 & 标签 agent tool：
 *  - 粉丝信息查询、关注列表
 *  - 标签 CRUD、打/取消标签
 *  - 用户备注、黑名单
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  createUserTag,
  listUserTags,
  updateUserTag,
  deleteUserTag,
  listTagUsers,
  batchTagUsers,
  batchUntagUsers,
  getUserTagIds,
  setUserRemark,
  blacklistUsers,
  unblacklistUsers,
  listBlacklist,
} from "../api/user-tag.js";
import { getUserInfo, batchGetUserInfo, listFollowers } from "../api/user.js";
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
        "get_user_info",
        "batch_get_user_info",
        "list_followers",
        "create_tag",
        "list_tags",
        "update_tag",
        "delete_tag",
        "list_tag_users",
        "batch_tag",
        "batch_untag",
        "get_user_tag_ids",
        "set_remark",
        "blacklist",
        "unblacklist",
        "list_blacklist",
      ],
      description: "粉丝信息 + 标签 + 黑名单操作。",
    },
    openid: { type: "string", description: "单个用户 openid。" },
    openids: {
      type: "array",
      items: { type: "string" },
      description: "批量操作的 openid 列表。",
    },
    lang: { type: "string", enum: ["zh_CN", "zh_TW", "en"], description: "语言，默认 zh_CN。" },
    next_openid: { type: "string", description: "list_followers / list_blacklist 翻页游标。" },
    user_list: {
      type: "array",
      description: "batch_get_user_info 用：[{openid, lang?}]，单次最多 100。",
      items: {
        type: "object",
        properties: {
          openid: { type: "string" },
          lang: { type: "string", enum: ["zh_CN", "zh_TW", "en"] },
        },
        required: ["openid"],
      },
    },
    tag_id: { type: "number", description: "标签 id。" },
    tag_name: { type: "string", description: "create_tag / update_tag 用：标签名。" },
    remark: { type: "string", description: "set_remark 用：30 字符以内。" },
  },
} as const;

export function registerUserTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_user",
      label: "WeChat Service User",
      description:
        "微信服务号粉丝与标签管理：查询用户信息、关注列表、标签 CRUD、批量打/取消标签、备注、拉黑/解除拉黑。",
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
            toolName: "wechat_service_user",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "get_user_info": {
              const openid = requireStr(params.openid, "openid");
              const result = await getUserInfo({
                account,
                tokenHandle,
                openid,
                lang: (params.lang as "zh_CN" | "zh_TW" | "en" | undefined) ?? "zh_CN",
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `用户 ${openid} 信息已获取`,
                user: result,
              });
            }
            case "batch_get_user_info": {
              const userList = params.user_list;
              if (!Array.isArray(userList) || userList.length === 0) {
                throw new Error("user_list required for action=batch_get_user_info");
              }
              const result = await batchGetUserInfo({
                account,
                tokenHandle,
                user_list: userList as Array<{ openid: string; lang?: "zh_CN" | "zh_TW" | "en" }>,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: result.length,
                users: result,
                summary: `已批量获取 ${result.length} 个用户信息`,
              });
            }
            case "list_followers": {
              const result = await listFollowers({
                account,
                tokenHandle,
                next_openid: params.next_openid as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                total: result.total,
                count: result.count,
                next_openid: result.next_openid,
                openids: result.data?.openid ?? [],
                summary: `关注列表已获取（total=${result.total ?? 0}）`,
              });
            }
            case "create_tag": {
              const name = requireStr(params.tag_name, "tag_name");
              const tag = await createUserTag({ account, tokenHandle, name });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                tag,
                summary: `标签 "${tag.name}" 已创建（id=${tag.id}）`,
              });
            }
            case "list_tags": {
              const tags = await listUserTags({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: tags.length,
                tags,
                summary: `标签列表已获取（${tags.length} 个）`,
              });
            }
            case "update_tag": {
              const id = requireNum(params.tag_id, "tag_id");
              const name = requireStr(params.tag_name, "tag_name");
              await updateUserTag({ account, tokenHandle, id, name });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `标签 ${id} 已重命名为 "${name}"`,
              });
            }
            case "delete_tag": {
              const id = requireNum(params.tag_id, "tag_id");
              await deleteUserTag({ account, tokenHandle, id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `标签 ${id} 已删除`,
              });
            }
            case "list_tag_users": {
              const id = requireNum(params.tag_id, "tag_id");
              const result = await listTagUsers({
                account,
                tokenHandle,
                tagid: id,
                next_openid: params.next_openid as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                count: result.count,
                openids: result.data?.openid ?? [],
                next_openid: result.next_openid,
                summary: `标签 ${id} 下用户已获取（${result.count ?? 0} 个）`,
              });
            }
            case "batch_tag": {
              const id = requireNum(params.tag_id, "tag_id");
              const openids = requireStrArr(params.openids, "openids");
              await batchTagUsers({ account, tokenHandle, tagid: id, openid_list: openids });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已给 ${openids.length} 个用户打上标签 ${id}`,
              });
            }
            case "batch_untag": {
              const id = requireNum(params.tag_id, "tag_id");
              const openids = requireStrArr(params.openids, "openids");
              await batchUntagUsers({ account, tokenHandle, tagid: id, openid_list: openids });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已从 ${openids.length} 个用户移除标签 ${id}`,
              });
            }
            case "get_user_tag_ids": {
              const openid = requireStr(params.openid, "openid");
              const tagIds = await getUserTagIds({ account, tokenHandle, openid });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                tagIds,
                summary: `用户 ${openid} 拥有 ${tagIds.length} 个标签`,
              });
            }
            case "set_remark": {
              const openid = requireStr(params.openid, "openid");
              const remark = requireStr(params.remark, "remark");
              await setUserRemark({ account, tokenHandle, openid, remark });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `用户 ${openid} 备注已更新为 "${remark}"`,
              });
            }
            case "blacklist": {
              const openids = requireStrArr(params.openids, "openids");
              await blacklistUsers({ account, tokenHandle, openid_list: openids });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已拉黑 ${openids.length} 个用户`,
              });
            }
            case "unblacklist": {
              const openids = requireStrArr(params.openids, "openids");
              await unblacklistUsers({ account, tokenHandle, openid_list: openids });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已取消拉黑 ${openids.length} 个用户`,
              });
            }
            case "list_blacklist": {
              const result = await listBlacklist({
                account,
                tokenHandle,
                begin_openid: params.next_openid as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                total: result.total,
                count: result.count,
                next_openid: result.next_openid,
                openids: result.data?.openid ?? [],
                summary: `黑名单列表已获取（total=${result.total ?? 0}）`,
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

function requireNum(value: unknown, name: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new Error(`${name} required (number)`);
  }
  return value;
}

function requireStrArr(value: unknown, name: string): string[] {
  if (!Array.isArray(value) || value.length === 0) {
    throw new Error(`${name} required (non-empty array)`);
  }
  return value.map((item) => {
    const str = typeof item === "string" ? item.trim() : "";
    if (!str) throw new Error(`${name} contains empty entry`);
    return str;
  });
}
