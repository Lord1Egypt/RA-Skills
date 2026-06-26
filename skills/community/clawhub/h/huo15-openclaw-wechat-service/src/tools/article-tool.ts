/**
 * 图文草稿 + 发布 agent tool：
 *  - 草稿箱：addDraft / getDraft / updateDraft / deleteDraft / listDrafts / countDrafts
 *  - 发布：publishDraft / getPublishStatus / getPublishedArticle / listPublished / deletePublished
 *
 * 推荐流程：
 *  1. material 工具上传图文 thumb（或 inline images）
 *  2. article 工具 add 草稿（带 thumb_media_id + content）
 *  3. article 工具 publish 草稿
 *  4. article 工具 get_publish_status 轮询 publish_id，直到 publish_status=0
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  addDraft,
  getDraft,
  deleteDraft,
  updateDraft,
  listDrafts,
  getDraftCount,
  publishDraft,
  getPublishStatus,
  getPublishedArticle,
  listPublished,
  deletePublished,
  type WechatDraftArticle,
} from "../api/draft.js";
import {
  ACCOUNT_ID_SCHEMA_PROPERTY,
  asErrorMessage,
  buildErrorResult,
  buildToolResult,
  assertAuthorized,
  resolveToolAccount,
  type ToolContext,
} from "./shared.js";

const articleItemSchema = {
  type: "object",
  properties: {
    title: { type: "string" },
    author: { type: "string" },
    digest: { type: "string" },
    content: { type: "string", description: "图文正文 HTML。" },
    content_source_url: { type: "string" },
    thumb_media_id: { type: "string", description: "封面图的永久 media_id。" },
    need_open_comment: { type: "number", enum: [0, 1] },
    only_fans_can_comment: { type: "number", enum: [0, 1] },
    show_cover_pic: { type: "number", enum: [0, 1] },
  },
  required: ["title", "content", "thumb_media_id"],
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
        "add_draft",
        "get_draft",
        "update_draft",
        "delete_draft",
        "list_drafts",
        "count_drafts",
        "publish",
        "get_publish_status",
        "get_published",
        "list_published",
        "delete_published",
      ],
      description: "草稿箱 & 发布流水线操作。",
    },
    articles: {
      type: "array",
      description: "add_draft 用：图文条目数组，每条独立正文。",
      items: articleItemSchema,
    },
    article: {
      ...articleItemSchema,
      description: "update_draft 用：单个图文条目（替换该 index 位置）。",
    },
    media_id: { type: "string", description: "get/update/delete_draft 用的 media_id（草稿）。" },
    index: { type: "number", description: "update_draft 用：要替换的图文 index（0-based）。" },
    publish_id: { type: "string", description: "get_publish_status 用。" },
    article_id: { type: "string", description: "get_published / delete_published 用。" },
    offset: { type: "number", description: "list_* 用分页偏移，默认 0。" },
    count: { type: "number", description: "list_* 每页条数，默认 20（最大 20）。" },
    no_content: {
      type: "number",
      enum: [0, 1],
      description: "list_* 用：1=不返回 content 省流量，0=返回（默认 0）。",
    },
    published_index: { type: "number", description: "delete_published 用：要删的图文 index，默认 0。" },
  },
} as const;

export function registerArticleTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_article",
      label: "WeChat Service Article",
      description:
        "微信服务号图文草稿 + 发布流水线：添加草稿、更新草稿、发布、轮询发布状态、查询已发布图文。支持多图文条目，封面必须先用 material 工具上传为永久素材。",
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
            toolName: "wechat_service_article",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "add_draft": {
              const articles = params.articles;
              if (!Array.isArray(articles) || articles.length === 0) {
                throw new Error("articles required for action=add_draft");
              }
              const result = await addDraft({
                account,
                tokenHandle,
                articles: articles as WechatDraftArticle[],
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                media_id: result.media_id,
                summary: `草稿已添加（media_id: ${result.media_id}，${articles.length} 个图文）`,
              });
            }
            case "get_draft": {
              const media_id = requireStr(params.media_id, "media_id");
              const result = await getDraft({ account, tokenHandle, media_id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `草稿 ${media_id} 已获取`,
                raw: result,
              });
            }
            case "update_draft": {
              const media_id = requireStr(params.media_id, "media_id");
              const article = params.article as WechatDraftArticle | undefined;
              if (!article) throw new Error("article required for action=update_draft");
              const index =
                typeof params.index === "number" && params.index >= 0 ? params.index : 0;
              await updateDraft({
                account,
                tokenHandle,
                media_id,
                index,
                articles: article,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `草稿 ${media_id} 第 ${index} 项已更新`,
              });
            }
            case "delete_draft": {
              const media_id = requireStr(params.media_id, "media_id");
              await deleteDraft({ account, tokenHandle, media_id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `草稿 ${media_id} 已删除`,
              });
            }
            case "list_drafts": {
              const result = await listDrafts({
                account,
                tokenHandle,
                offset: params.offset as number | undefined,
                count: params.count as number | undefined,
                no_content: params.no_content as 0 | 1 | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "草稿列表已获取",
                raw: result,
              });
            }
            case "count_drafts": {
              const result = await getDraftCount({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                total_count: result.total_count,
                summary: `草稿总数 ${result.total_count ?? 0}`,
              });
            }
            case "publish": {
              const media_id = requireStr(params.media_id, "media_id");
              const result = await publishDraft({ account, tokenHandle, media_id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                publish_id: result.publish_id,
                msg_data_id: result.msg_data_id,
                summary: `发布已提交（publish_id: ${result.publish_id}）。使用 get_publish_status 轮询。`,
              });
            }
            case "get_publish_status": {
              const publish_id = requireStr(params.publish_id, "publish_id");
              const result = await getPublishStatus({ account, tokenHandle, publish_id });
              const statusLabel = describePublishStatus(result.publish_status);
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                publish_id: result.publish_id,
                publish_status: result.publish_status,
                article_id: result.article_id,
                article_detail: result.article_detail,
                fail_idx: result.fail_idx,
                summary: `发布状态：${statusLabel}（publish_status=${result.publish_status}）`,
              });
            }
            case "get_published": {
              const article_id = requireStr(params.article_id, "article_id");
              const result = await getPublishedArticle({ account, tokenHandle, article_id });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已发布图文 ${article_id} 详情已获取`,
                raw: result,
              });
            }
            case "list_published": {
              const result = await listPublished({
                account,
                tokenHandle,
                offset: params.offset as number | undefined,
                count: params.count as number | undefined,
                no_content: params.no_content as 0 | 1 | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "已发布图文列表已获取",
                raw: result,
              });
            }
            case "delete_published": {
              const article_id = requireStr(params.article_id, "article_id");
              await deletePublished({
                account,
                tokenHandle,
                article_id,
                index: params.published_index as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `已发布图文 ${article_id} 已删除`,
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

function describePublishStatus(status: number): string {
  switch (status) {
    case 0:
      return "发布成功";
    case 1:
      return "发布中";
    case 2:
      return "原创失败";
    case 3:
      return "常规失败";
    case 4:
      return "平台审核不通过";
    case 5:
      return "成功后用户删除所有文章";
    case 6:
      return "成功后系统封禁所有文章";
    default:
      return `未知(${status})`;
  }
}

function requireStr(value: unknown, name: string): string {
  const str = typeof value === "string" ? value.trim() : "";
  if (!str) throw new Error(`${name} required`);
  return str;
}
