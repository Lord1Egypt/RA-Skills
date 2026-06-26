import fs from "node:fs";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { isWecomAgentSource } from "../../runtime/source-registry.js";
import type { ResolvedAgentAccount } from "../../types/index.js";
import { resolveAgentAccountOrUndefined } from "../bot/fallback-delivery.js";
import { WecomDocClient } from "./client.js";
import { wecomDocToolSchema } from "./schema.js";
import { UpdateRequest } from "./types.js";

function readString(value: unknown): string {
  const trimmed = String(value ?? "").trim();
  return trimmed || "";
}

function mapDocTypeLabel(docType: number): string {
  if (docType === 10) return "智能表格";
  return docType === 4 ? "表格" : "文档";
}

function summarizeDocInfo(info: any = {}) {
  const docName = readString(info.doc_name) || "未命名文档";
  const docType = mapDocTypeLabel(Number(info.doc_type));
  return `${docType}"${docName}"信息已获取`;
}

function summarizeDocAuth(result: any = {}) {
  return `权限信息已获取：通知成员 ${result.docMembers?.length ?? 0}，协作者 ${result.coAuthList?.length ?? 0}`;
}

function readBooleanFlag(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function formatDocMemberRef(value: any) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return "";
  const userid = readString(value.userid ?? value.userId);
  if (userid) return `userid:${userid}`;
  const partyid = readString(value.partyid);
  if (partyid) return `partyid:${partyid}`;
  const tagid = readString(value.tagid);
  if (tagid) return `tagid:${tagid}`;
  return "";
}

function mapDocMemberList(values: any) {
  return Array.isArray(values)
    ? values.map((item) => formatDocMemberRef(item)).filter(Boolean)
    : [];
}

function describeFlagState(
  value: boolean | null,
  enabledLabel: string,
  disabledLabel: string,
  unknownLabel = "未知",
) {
  if (value === true) return enabledLabel;
  if (value === false) return disabledLabel;
  return unknownLabel;
}

function buildDocAuthDiagnosis(result: any = {}, requesterSenderId = "") {
  const accessRule =
    result.accessRule && typeof result.accessRule === "object" ? result.accessRule : {};
  const viewers = mapDocMemberList(result.docMembers);
  const collaborators = mapDocMemberList(result.coAuthList);
  const requester = readString(requesterSenderId);
  const requesterViewerRef = requester ? `userid:${requester}` : "";
  const requesterIsViewer = requesterViewerRef ? viewers.includes(requesterViewerRef) : false;
  const requesterIsCollaborator = requesterViewerRef
    ? collaborators.includes(requesterViewerRef)
    : false;
  const internalAccessEnabled = readBooleanFlag(accessRule.enable_corp_internal);
  const externalAccessEnabled = readBooleanFlag(accessRule.enable_corp_external);
  const externalShareAllowed =
    typeof accessRule.ban_share_external === "boolean" ? !accessRule.ban_share_external : null;
  const likelyAnonymousLinkFailure =
    internalAccessEnabled === true && externalAccessEnabled === false;
  const findings = [
    `企业内访问：${describeFlagState(internalAccessEnabled, "开启", "关闭")}`,
    `企业外访问：${describeFlagState(externalAccessEnabled, "开启", "关闭")}`,
    `外部分享：${describeFlagState(externalShareAllowed, "允许", "禁止")}`,
    `查看成员：${viewers.length}`,
    `协作者：${collaborators.length}`,
  ];
  const recommendations: string[] = [];
  if (likelyAnonymousLinkFailure) {
    recommendations.push(
      '当前更像是仅企业内可访问；匿名浏览器或未登录企业微信环境通常会显示"文档不存在"。',
    );
  }
  if (requester) {
    if (requesterIsCollaborator) {
      recommendations.push(`当前请求人 ${requester} 已在协作者列表中。`);
    } else if (requesterIsViewer) {
      recommendations.push(`当前请求人 ${requester} 已在查看成员列表中，但还不是协作者。`);
    } else {
      recommendations.push(`当前请求人 ${requester} 不在查看成员或协作者列表中。`);
    }
  }
  return {
    internalAccessEnabled,
    externalAccessEnabled,
    externalShareAllowed,
    viewerCount: viewers.length,
    collaboratorCount: collaborators.length,
    viewers,
    collaborators,
    requesterSenderId: requester || undefined,
    requesterRole: requesterIsCollaborator
      ? "collaborator"
      : requesterIsViewer
        ? "viewer"
        : requester
          ? "none"
          : "unknown",
    likelyAnonymousLinkFailure,
    findings,
    recommendations,
  };
}

function summarizeDocAuthDiagnosis(diagnosis: any = {}) {
  const parts = Array.isArray(diagnosis.findings) ? diagnosis.findings : [];
  return parts.length > 0 ? `文档权限诊断：${parts.join("，")}` : "文档权限诊断已完成";
}

function buildDocIdUsageHint(docId?: string) {
  const normalizedDocId = readString(docId);
  if (!normalizedDocId) return "";
  return `后续权限、分享和诊断操作请使用真实 docId：${normalizedDocId}；不要直接使用分享链接路径中的片段。`;
}

function safeParseJson(text: string) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function extractEmbeddedJson(html: string, variableName: string) {
  const source = String(html ?? "");
  if (!source) return null;
  const marker = `window.${variableName}=`;
  const start = source.indexOf(marker);
  if (start < 0) return null;
  const valueStart = start + marker.length;
  const end = source.indexOf(";</script>", valueStart);
  if (end < 0) return null;
  return safeParseJson(source.slice(valueStart, end));
}

function buildShareLinkDiagnosis(params: {
  shareUrl: string;
  finalUrl: string;
  status: number;
  contentType: string;
  basicClientVars: any;
}) {
  const { shareUrl, finalUrl, status, contentType, basicClientVars } = params;
  const parsedUrl = new URL(finalUrl || shareUrl);
  const pathSegments = parsedUrl.pathname.split("/").filter(Boolean);
  const pathResourceType = readString(pathSegments[0]);
  const pathResourceId = readString(pathSegments[1]);
  const shareCode = readString(parsedUrl.searchParams.get("scode"));
  const userInfo =
    basicClientVars?.userInfo && typeof basicClientVars.userInfo === "object"
      ? basicClientVars.userInfo
      : {};
  const docInfo =
    basicClientVars?.docInfo && typeof basicClientVars.docInfo === "object"
      ? basicClientVars.docInfo
      : {};
  const padInfo = docInfo?.padInfo && typeof docInfo.padInfo === "object" ? docInfo.padInfo : {};
  const ownerInfo =
    docInfo?.ownerInfo && typeof docInfo.ownerInfo === "object" ? docInfo.ownerInfo : {};
  const shareInfo =
    docInfo?.shareInfo && typeof docInfo.shareInfo === "object" ? docInfo.shareInfo : {};
  const aclInfo = docInfo?.aclInfo && typeof docInfo.aclInfo === "object" ? docInfo.aclInfo : {};
  const userType = readString(userInfo.userType);
  const padType = readString(padInfo.padType);
  const padId = readString(padInfo.padId);
  const padTitle = readString(padInfo.padTitle);
  const isGuest = userType === "guest" || Number(userInfo.loginType) === 0;
  const isBlankPage = padType === "blankpage";
  const likelyUnavailableToGuest = isGuest && isBlankPage && !padTitle;
  const findings = [
    `HTTP ${String(status || "")}`.trim(),
    `内容类型：${readString(contentType) || "未知"}`,
    `访问身份：${userType || "未知"}`,
    `页面类型：${padType || "未知"}`,
    `路径资源：${pathResourceType || "未知"} / ${pathResourceId || "未知"}`,
  ];
  const recommendations: string[] = [];
  if (likelyUnavailableToGuest) {
    recommendations.push(
      '当前链接对 guest/未登录企业微信环境返回 blankpage，外部访问会表现为打不开或像"文档不存在"。',
    );
  }
  if (shareCode) {
    recommendations.push(
      `当前链接带有分享码 scode=${shareCode}。如分享码过期或未生效，外部访问会失败。`,
    );
  }
  if (pathResourceId && padId && pathResourceId !== padId) {
    recommendations.push(
      `链接路径中的资源标识与页面 padId 不一致：path=${pathResourceId}，padId=${padId}。`,
    );
  }
  if (pathResourceId && padId && pathResourceId === padId) {
    recommendations.push(
      "链接路径资源标识与页面 padId 一致，但这仍不等同于 Wedoc API 可用的真实 docId。",
    );
  }
  return {
    shareUrl,
    finalUrl,
    httpStatus: status,
    contentType: readString(contentType) || undefined,
    pathResourceType: pathResourceType || undefined,
    pathResourceId: pathResourceId || undefined,
    shareCode: shareCode || undefined,
    userType: userType || undefined,
    isGuest,
    padId: padId || undefined,
    padType: padType || undefined,
    padTitle: padTitle || undefined,
    ownerId: readString(ownerInfo.ownerId) || undefined,
    hasShareInfo: Object.keys(shareInfo).length > 0,
    hasAclInfo: Object.keys(aclInfo).length > 0,
    likelyUnavailableToGuest,
    findings,
    recommendations,
  };
}

async function inspectWecomShareLink(params: { shareUrl: string }) {
  const { shareUrl } = params;
  const normalizedUrl = readString(shareUrl);
  if (!normalizedUrl) throw new Error("shareUrl required");
  let parsed;
  try {
    parsed = new URL(normalizedUrl);
  } catch {
    throw new Error("shareUrl must be a valid URL");
  }
  // To protect URLs containing underscores from markdown italic corruption in output, we ensure we return exactly what we got or wrap it later.

  const response = await fetch(parsed.toString(), {
    headers: {
      "user-agent": "OpenClaw-Wechat/1.0",
      accept: "text/html,application/xhtml+xml",
    },
    signal: AbortSignal.timeout(10000),
  });
  const contentType = response.headers?.get("content-type") || "";
  const html = await response.text();
  const basicClientVars = extractEmbeddedJson(html, "basicClientVars");
  const diagnosis = buildShareLinkDiagnosis({
    shareUrl: normalizedUrl,
    finalUrl: response.url || parsed.toString(),
    status: response.status,
    contentType,
    basicClientVars,
  });
  return {
    raw: {
      httpStatus: response.status,
      // Markdown italic protection for URLs
      finalUrl: `\u00A0${response.url || parsed.toString()}\u00A0`.trim(),
      contentType,
      basicClientVars,
    },
    diagnosis,
  };
}

function summarizeShareLinkDiagnosis(diagnosis: any = {}) {
  const parts = Array.isArray(diagnosis.findings) ? diagnosis.findings : [];
  return parts.length > 0 ? `分享链接校验：${parts.join("，")}` : "分享链接校验已完成";
}

function summarizeSheetProperties(result: any = {}) {
  return `表格属性已获取：工作表 ${result.properties?.length ?? 0}`;
}

function summarizeDocAccess(result: any = {}) {
  const parts = [];
  if (result.addedViewerCount) parts.push(`新增查看成员 ${result.addedViewerCount}`);
  if (result.addedCollaboratorCount) parts.push(`新增协作者 ${result.addedCollaboratorCount}`);
  if (result.removedViewerCount) parts.push(`移除查看成员 ${result.removedViewerCount}`);
  if (result.removedCollaboratorCount) parts.push(`移除协作者 ${result.removedCollaboratorCount}`);
  return parts.length > 0 ? `文档权限已更新：${parts.join("，")}` : "文档权限已更新";
}

function summarizeFormInfo(result: any = {}) {
  const title = readString(result.formInfo?.form_title) || "未命名收集表";
  return `收集表"${title}"信息已获取`;
}

function summarizeFormAnswer(result: any = {}) {
  return `收集表答案已获取：字段 ${result.answerList?.length ?? 0}`;
}

function summarizeFormStatistic(result: any = {}) {
  return `收集表统计已获取：请求 ${result.items?.length ?? 0}，成功 ${result.successCount ?? 0}`;
}

function summarizeAdvancedAccount(result: any = {}, action: string) {
  if (action === "assign") return `高级功能账号分配任务已提交，jobid: ${result.jobid || "未知"}`;
  if (action === "cancel") return `高级功能账号取消任务已提交，jobid: ${result.jobid || "未知"}`;
  return `高级功能账号列表已获取：${result.userList?.length ?? 0} 个`;
}

function readMemberUserId(value: any) {
  if (typeof value === "string" || typeof value === "number") {
    return readString(value);
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) return "";
  return readString(value.userid ?? value.userId);
}

function hasMemberUserId(values: any, requesterSenderId: string) {
  const normalizedRequesterSenderId = readString(requesterSenderId);
  if (!normalizedRequesterSenderId) return false;
  return (
    Array.isArray(values) &&
    values.some((item) => readMemberUserId(item) === normalizedRequesterSenderId)
  );
}

function resolveCreateCollaborators(params: { toolContext: any; requestParams: any }) {
  const { toolContext, requestParams } = params;
  const explicitCollaborators = Array.isArray(requestParams?.collaborators)
    ? [...requestParams.collaborators]
    : [];
  const requesterSenderId = readString(toolContext?.senderId || toolContext?.requesterSenderId); // align with OpenClaw standard `senderId`
  if (!requesterSenderId) return explicitCollaborators;
  // By default, let's always auto-grant requester
  if (hasMemberUserId(explicitCollaborators, requesterSenderId)) return explicitCollaborators;
  if (hasMemberUserId(requestParams?.viewers, requesterSenderId)) return explicitCollaborators;
  explicitCollaborators.push(requesterSenderId);
  return explicitCollaborators;
}

function buildToolResult(payload: any) {
  // To avoid formatting issues with URLs having underscores rendering as markdown Italics
  if (payload.url) payload.url = `<${payload.url}>`;
  if (payload.diagnosis?.finalUrl) payload.diagnosis.finalUrl = `<${payload.diagnosis.finalUrl}>`;
  if (payload.diagnosis?.shareUrl) payload.diagnosis.shareUrl = `<${payload.diagnosis.shareUrl}>`;
  return {
    content: [{ type: "text" as const, text: JSON.stringify(payload, null, 2) }],
    details: payload,
  };
}

export function registerWecomDocTools(api: OpenClawPluginApi) {
  if (typeof api?.registerTool !== "function") return;
  const docClient = new WecomDocClient();

  api.registerTool((toolContext: any) => {
    if (
      toolContext?.messageChannel !== "wecom" ||
      !isWecomAgentSource({
        accountId: toolContext?.agentAccountId || toolContext?.accountId,
        sessionKey: toolContext?.sessionKey,
        sessionId: toolContext?.sessionId,
      })
    ) {
      return null;
    }

    return {
      name: "wecom_doc",
      label: "WeCom Doc",
      description:
        "企业微信文档工具。支持文档/表格/收集表完整CRUD操作、查看/协作者权限配置、属性查询以及分享打不开可用性诊断功能。",
      parameters: wecomDocToolSchema,
      async execute(_toolCallId, params: any) {
        try {
          let accountId =
            params.accountId || toolContext?.agentAccountId || toolContext?.accountId || "default";
          const account = resolveAgentAccountOrUndefined(api.config, accountId);
          if (!account || !account.configured) {
            throw new Error(`WeCom account ${accountId} not configured for Doc API requirements`);
          }

          const action = params.action;
          switch (action) {
            case "create": {
              const explicitCollaborators = Array.isArray(params.collaborators)
                ? [...params.collaborators]
                : [];
              const result = await docClient.createDoc({
                agent: account,
                docName: params.docName,
                docType: params.docType,
                spaceId: params.spaceId,
                fatherId: params.fatherId,
                adminUsers: params.adminUsers,
              });

              // Auto-set security rules for better default permissions (internal users can edit)
              try {
                await docClient.setDocJoinRule({
                  agent: account,
                  docId: result.docId,
                  request: {
                    enable_corp_internal: true,
                    corp_internal_auth: 2, // 2 = edit permission
                    enable_corp_external: false,
                    ban_share_external: false,
                  },
                });
              } catch (err) {
                // Non-fatal: document created, just default permissions may be read-only
              }

              // Handle initial content (title/body separation) if provided
              // Supports: string (text) or {type: "text"|"image", content/url: string}
              let contentResult: any = null;
              if (Array.isArray(params.init_content) && params.init_content.length > 0) {
                try {
                  // Helper: check if content item is an image
                  const isImageItem = (item: any): boolean => {
                    if (typeof item === "object" && item !== null) {
                      return item.type === "image" || (item.url && !item.content);
                    }
                    if (typeof item === "string") {
                      // Detect image URLs
                      return (
                        item.startsWith("http") &&
                        (item.includes(".png") ||
                          item.includes(".jpg") ||
                          item.includes(".jpeg") ||
                          item.includes(".gif") ||
                          item.includes("qpic.cn") ||
                          item.includes("weixin.qq.com"))
                      );
                    }
                    return false;
                  };

                  // Helper: get image URL from content item
                  const getImageUrl = (item: any): string => {
                    if (typeof item === "object" && item !== null) {
                      return item.url || item.content || "";
                    }
                    return String(item);
                  };

                  // Helper: get text from content item
                  const getText = (item: any): string => {
                    if (typeof item === "object" && item !== null) {
                      return item.content || item.text || "";
                    }
                    return String(item);
                  };

                  // Helper: download image from URL or read local file and convert to base64
                  const getImageAsBase64 = async (imageSource: string): Promise<string> => {
                    // Check if it's a local file path or remote URL
                    const isLocalFile =
                      !imageSource.startsWith("http") && !imageSource.startsWith("data:");

                    if (isLocalFile) {
                      // Local file path - read using Node.js fs
                      const fs = await import("fs");
                      const path = await import("path");

                      // Resolve to absolute path if relative
                      const absolutePath = path.isAbsolute(imageSource)
                        ? imageSource
                        : path.join(process.cwd(), imageSource);

                      if (!fs.existsSync(absolutePath)) {
                        throw new Error(`Local image file not found: ${absolutePath}`);
                      }

                      const fileBuffer = fs.readFileSync(absolutePath);
                      return fileBuffer.toString("base64");
                    } else if (imageSource.startsWith("data:")) {
                      // Data URL (base64 already)
                      const matches = imageSource.match(
                        /^data:image\/(?:png|jpeg|gif|webp);base64,(.*)$/,
                      );
                      if (matches && matches[1]) {
                        return matches[1];
                      }
                      throw new Error("Invalid data URL format");
                    } else {
                      // Remote URL - download first
                      console.log(
                        `[wecom-doc] Downloading remote image: ${imageSource.substring(0, 50)}...`,
                      );
                      const response = await fetch(imageSource, {
                        signal: AbortSignal.timeout(10000),
                      });
                      if (!response.ok) {
                        throw new Error(
                          `Failed to download image: ${response.status} ${response.statusText}`,
                        );
                      }
                      const arrayBuffer = await response.arrayBuffer();
                      return Buffer.from(arrayBuffer).toString("base64");
                    }
                  };

                  // Step 1: Insert first paragraph (title) at index 0
                  if (params.init_content[0]) {
                    const firstItem = params.init_content[0];
                    if (isImageItem(firstItem)) {
                      // First item is image - upload first, then insert at index 0
                      const imgUrl = getImageUrl(firstItem);

                      try {
                        // Upload image to WeCom to get proper image_id
                        const base64 = await getImageAsBase64(imgUrl);
                        const uploadResult = await docClient.uploadDocImage({
                          agent: account,
                          docId: result.docId,
                          base64_content: base64,
                        });
                        console.log(
                          `[wecom-doc] Title image uploaded: ${uploadResult.width}x${uploadResult.height}`,
                        );

                        // Insert image using uploaded URL
                        // Note: version is optional, API handles concurrency
                        await docClient.updateDocContent({
                          agent: account,
                          docId: result.docId,
                          requests: [
                            {
                              insert_image: {
                                image_id: uploadResult.url,
                                location: { index: 0 },
                                width: uploadResult.width,
                                height: uploadResult.height,
                              },
                            },
                          ],
                        });
                      } catch (uploadErr) {
                        console.error(`Failed to upload first image ${imgUrl}:`, uploadErr);
                        throw new Error(
                          `First image upload failed: ${uploadErr instanceof Error ? uploadErr.message : String(uploadErr)}`,
                        );
                      }
                    } else {
                      const titleText = getText(firstItem);
                      await docClient.updateDocContent({
                        agent: account,
                        docId: result.docId,
                        requests: [
                          {
                            insert_text: {
                              text: titleText,
                              location: { index: 0 },
                            },
                          },
                        ],
                      });

                      // Apply Title Styling (Bold)
                      if (titleText.length > 0) {
                        await docClient.updateDocContent({
                          agent: account,
                          docId: result.docId,
                          requests: [
                            {
                              update_text_property: {
                                text_property: { bold: true },
                                ranges: [{ start_index: 0, length: titleText.length }],
                              },
                            },
                          ],
                        });
                      }
                    }
                  }

                  // Step 2: For subsequent items, append with proper paragraph handling
                  // Per API spec: must get latest version and index before each batch_update
                  for (let i = 1; i < params.init_content.length; i++) {
                    const item = params.init_content[i];

                    // Refresh content to get latest document structure and version
                    // API requires: version difference ≤ 100 from latest
                    const currentContent = await docClient.getDocContent({
                      agent: account,
                      docId: result.docId,
                    });

                    // Get the end index of the document
                    const docEndIndex = currentContent.document.end;
                    const currentVersion = currentContent.version;

                    if (isImageItem(item)) {
                      // Insert image
                      const imgUrl = getImageUrl(item);

                      try {
                        // Upload image to WeCom
                        const base64 = await getImageAsBase64(imgUrl);
                        const uploadResult = await docClient.uploadDocImage({
                          agent: account,
                          docId: result.docId,
                          base64_content: base64,
                        });
                        console.log(
                          `[wecom-doc] Item ${i} image uploaded: ${uploadResult.width}x${uploadResult.height}`,
                        );

                        // Step 2: Create new paragraph and insert image in one batch (2 operations ≤ 30)
                        // Per API spec: all indices are based on the same document snapshot
                        // insert_paragraph at docEndIndex creates a new paragraph
                        // insert_image at docEndIndex + 1 inserts into the newly created paragraph
                        await docClient.updateDocContent({
                          agent: account,
                          docId: result.docId,
                          version: currentVersion, // Pass version for concurrency control
                          requests: [
                            {
                              insert_paragraph: {
                                location: { index: docEndIndex },
                              },
                            },
                            {
                              insert_image: {
                                image_id: uploadResult.url,
                                location: { index: docEndIndex + 1 },
                                width: uploadResult.width,
                                height: uploadResult.height,
                              },
                            },
                          ],
                        });
                      } catch (uploadErr) {
                        console.error(`Failed to upload image ${imgUrl}:`, uploadErr);
                        throw new Error(
                          `Image upload failed: ${uploadErr instanceof Error ? uploadErr.message : String(uploadErr)}`,
                        );
                      }
                    } else {
                      const text = getText(item);
                      if (!text) continue;

                      // Insert text: create paragraph and insert text in one batch (2 operations ≤ 30)
                      // Per API spec: all indices are based on the same document snapshot
                      // insert_paragraph at docEndIndex creates a new paragraph
                      // insert_text at docEndIndex + 1 inserts into the newly created paragraph
                      await docClient.updateDocContent({
                        agent: account,
                        docId: result.docId,
                        version: currentVersion, // Pass version for concurrency control
                        requests: [
                          {
                            insert_paragraph: {
                              location: { index: docEndIndex },
                            },
                          },
                          {
                            insert_text: {
                              text: text,
                              location: { index: docEndIndex + 1 },
                            },
                          },
                        ],
                      });
                    }
                  }
                  contentResult = "init_content_populated";
                } catch (err) {
                  contentResult = `content_failed: ${err instanceof Error ? err.message : String(err)}`;
                }
              }

              let accessResult: any = null;
              if (
                (Array.isArray(params.viewers) && params.viewers.length > 0) ||
                explicitCollaborators.length > 0
              ) {
                try {
                  accessResult = await docClient.grantDocAccess({
                    agent: account,
                    docId: result.docId,
                    viewers: params.viewers,
                    collaborators: explicitCollaborators,
                  });
                } catch (err) {
                  return buildToolResult({
                    ok: false,
                    partial: true,
                    action: "create",
                    accountId: account.accountId,
                    resourceType: result.docTypeLabel,
                    canonicalDocId: result.docId,
                    docId: result.docId,
                    title: readString(params.docName),
                    url: result.url || undefined,
                    summary: `已创建${mapDocTypeLabel(result.docType)}"${readString(params.docName)}"（docId: ${result.docId}），但权限授予失败`,
                    usageHint: buildDocIdUsageHint(result.docId) || undefined,
                    error: err instanceof Error ? err.message : String(err),
                    raw: { create: result.raw },
                  });
                }
              }
              return buildToolResult({
                ok: true,
                action: "create",
                accountId: account.accountId,
                resourceType: result.docTypeLabel,
                canonicalDocId: result.docId,
                docId: result.docId,
                title: readString(params.docName),
                url: result.url || undefined,
                summary: accessResult
                  ? `已创建${mapDocTypeLabel(result.docType)}"${readString(params.docName)}"（docId: ${result.docId}）；${summarizeDocAccess(accessResult)}` +
                    (contentResult ? `；内容填充: ${contentResult}` : "")
                  : `已创建${mapDocTypeLabel(result.docType)}"${readString(params.docName)}"（docId: ${result.docId}）` +
                    (contentResult ? `；内容填充: ${contentResult}` : ""),
                usageHint: buildDocIdUsageHint(result.docId) || undefined,
                raw: accessResult ? { create: result.raw, access: accessResult.raw } : result.raw,
              });
            }
            case "rename": {
              const result = await docClient.renameDoc({
                agent: account,
                docId: params.docId,
                newName: params.newName,
              });
              return buildToolResult({
                ok: true,
                action: "rename",
                accountId: account.accountId,
                docId: result.docId,
                title: result.newName,
                summary: `文档已重命名为"${result.newName}"`,
                raw: result.raw,
              });
            }
            case "copy": {
              const result = await docClient.copyDoc({
                agent: account,
                docId: params.docId,
                newName: params.newName,
                spaceId: params.spaceId,
                fatherId: params.fatherId,
              });
              return buildToolResult({
                ok: true,
                action: "copy",
                accountId: account.accountId,
                docId: result.docId,
                summary: `文档已成功复制，新 docId: ${result.docId}`,
                raw: result.raw,
              });
            }
            case "get_info": {
              const result = await docClient.getDocBaseInfo({
                agent: account,
                docId: params.docId,
              });
              return buildToolResult({
                ok: true,
                action: "get_info",
                accountId: account.accountId,
                docId: params.docId,
                title: readString(result.info?.doc_name) || undefined,
                resourceType:
                  Number(result.info?.doc_type) === 10
                    ? "smart_table"
                    : Number(result.info?.doc_type) === 4
                      ? "spreadsheet"
                      : "doc",
                summary: summarizeDocInfo(result.info),
                raw: result.raw,
              });
            }
            case "share": {
              const result = await docClient.shareDoc({
                agent: account,
                docId: params.docId,
              });
              return buildToolResult({
                ok: true,
                action: "share",
                accountId: account.accountId,
                canonicalDocId: params.docId,
                docId: params.docId,
                url: result.shareUrl || undefined,
                summary: result.shareUrl
                  ? `文档分享链接已获取（docId: ${params.docId}）`
                  : `文档分享接口调用成功（docId: ${params.docId}）`,
                usageHint: buildDocIdUsageHint(params.docId) || undefined,
                raw: result.raw,
              });
            }
            case "get_auth": {
              const result = await docClient.getDocAuth({
                agent: account,
                docId: params.docId,
              });
              const diagnosis = buildDocAuthDiagnosis(result, toolContext?.senderId);
              return buildToolResult({
                ok: true,
                action: "get_auth",
                accountId: account.accountId,
                canonicalDocId: params.docId,
                docId: params.docId,
                summary: summarizeDocAuth(result),
                diagnosis,
                raw: result.raw,
              });
            }
            case "diagnose_auth": {
              const result = await docClient.getDocAuth({
                agent: account,
                docId: params.docId,
              });
              const diagnosis = buildDocAuthDiagnosis(result, toolContext?.senderId);
              return buildToolResult({
                ok: true,
                action: "diagnose_auth",
                accountId: account.accountId,
                canonicalDocId: params.docId,
                docId: params.docId,
                summary: summarizeDocAuthDiagnosis(diagnosis),
                diagnosis,
                raw: result.raw,
              });
            }
            case "validate_share_link": {
              const result = await inspectWecomShareLink({
                shareUrl: params.shareUrl,
              });
              return buildToolResult({
                ok: true,
                action: "validate_share_link",
                accountId: account.accountId,
                url: result.diagnosis.finalUrl || params.shareUrl,
                summary: summarizeShareLinkDiagnosis(result.diagnosis),
                diagnosis: result.diagnosis,
                raw: result.raw,
              });
            }
            case "delete": {
              const result = await docClient.deleteDoc({
                agent: account,
                docId: params.docId,
                formId: params.formId,
              });
              return buildToolResult({
                ok: true,
                action: "delete",
                accountId: account.accountId,
                docId: result.docId || undefined,
                formId: result.formId || undefined,
                summary: result.formId ? "收集表已删除" : "文档已删除",
                raw: result.raw,
              });
            }
            case "set_join_rule": {
              const result = await docClient.setDocJoinRule({
                agent: account,
                docId: params.docId,
                request: params.request,
              });
              return buildToolResult({
                ok: true,
                action: "set_join_rule",
                accountId: account.accountId,
                docId: result.docId,
                summary: "文档查看规则已更新",
                raw: result.raw,
              });
            }
            case "set_member_auth": {
              const result = await docClient.setDocMemberAuth({
                agent: account,
                docId: params.docId,
                request: params.request,
              });
              return buildToolResult({
                ok: true,
                action: "set_member_auth",
                accountId: account.accountId,
                docId: result.docId,
                summary: "文档通知范围及成员权限已更新",
                raw: result.raw,
              });
            }
            case "grant_access": {
              const result = await docClient.grantDocAccess({
                agent: account,
                docId: params.docId,
                viewers: params.viewers,
                collaborators: params.collaborators,
                removeViewers: params.removeViewers,
                removeCollaborators: params.removeCollaborators,
                authLevel: params.auth,
              });
              return buildToolResult({
                ok: true,
                action: "grant_access",
                accountId: account.accountId,
                docId: result.docId,
                summary: summarizeDocAccess(result),
                raw: result.raw,
              });
            }
            case "add_collaborators": {
              const result = await docClient.addDocCollaborators({
                agent: account,
                docId: params.docId,
                collaborators: params.collaborators,
                auth: params.auth,
              });
              return buildToolResult({
                ok: true,
                action: "add_collaborators",
                accountId: account.accountId,
                docId: result.docId,
                summary: `协作者已添加：${result.addedCollaboratorCount ?? 0}`,
                raw: result.raw,
              });
            }
            case "get_content": {
              const result = await docClient.getDocContent({
                agent: account,
                docId: params.docId,
              });
              return buildToolResult({
                ok: true,
                action: "get_content",
                accountId: account.accountId,
                docId: params.docId,
                summary: "文档内容已获取",
                raw: result.raw,
              });
            }
            case "update_content": {
              const result = await docClient.updateDocContent({
                agent: account,
                docId: params.docId,
                requests: params.requests,
                version: params.version,
              });

              const batchCount = result.batches ?? 1;
              return buildToolResult({
                ok: true,
                action: "update_content",
                accountId: account.accountId,
                docId: params.docId,
                summary:
                  batchCount > 1
                    ? `文档内容已更新（自动分批，共${batchCount}批）`
                    : "文档内容已更新",
                batches: batchCount,
                raw: result.raw,
              });
            }
            case "set_safety_setting": {
              const result = await docClient.setDocSafetySetting({
                agent: account,
                docId: params.docId,
                request: params.request,
              });
              return buildToolResult({
                ok: true,
                action: "set_safety_setting",
                accountId: account.accountId,
                docId: result.docId,
                summary: "文档安全设置已更新",
                raw: result.raw,
              });
            }
            case "get_doc_security_setting": {
              const result = await docClient.getDocAuth({
                agent: account,
                docId: params.docId,
              });
              return buildToolResult({
                ok: true,
                action: "get_doc_security_setting",
                accountId: account.accountId,
                docId: params.docId,
                summary: "文档安全设置已获取",
                details: result.secureSetting,
                raw: result.raw,
              });
            }
            case "mod_doc_security_setting": {
              // Alias to setDocSafetySetting logic
              const result = await docClient.setDocSafetySetting({
                agent: account,
                docId: params.docId,
                request: params.setting,
              });
              return buildToolResult({
                ok: true,
                action: "mod_doc_security_setting",
                accountId: account.accountId,
                docId: result.docId,
                summary: "文档安全设置已更新",
                raw: result.raw,
              });
            }
            case "mod_doc_member_notified_scope": {
              const result = await docClient.modDocMemberNotifiedScope({
                agent: account,
                docId: params.docId,
                notified_scope_type: params.notified_scope_type,
                notified_member_list: params.notified_member_list,
              });
              return buildToolResult({
                ok: true,
                action: "mod_doc_member_notified_scope",
                accountId: account.accountId,
                docId: params.docId,
                summary: "文档成员通知范围已更新",
                raw: result,
              });
            }
            case "create_form": {
              // 创建收集表（表单）
              try {
                const result = await docClient.createCollect({
                  agent: account,
                  formInfo: params.formInfo,
                  spaceId: params.spaceId,
                  fatherId: params.fatherId,
                });
                const title = readString(result.title);
                return buildToolResult({
                  ok: true,
                  action: "create_form",
                  accountId: account.accountId,
                  formId: result.formId,
                  title: title || undefined,
                  summary: title
                    ? `已创建收集表"${title}"（formId: ${result.formId}）`
                    : `已创建收集表（formId: ${result.formId}）`,
                  raw: result.raw,
                });
              } catch (err) {
                const errorMsg = err instanceof Error ? err.message : String(err);
                return buildToolResult({
                  ok: false,
                  action: "create_form",
                  accountId: account.accountId,
                  error: errorMsg,
                  summary: "创建收集表失败",
                  raw: {},
                });
              }
            }
            case "modify_form": {
              const result = await docClient.modifyCollect({
                agent: account,
                oper: params.oper,
                formId: params.formId,
                formInfo: params.formInfo,
              });
              const title = readString(result.title);
              return buildToolResult({
                ok: true,
                action: "modify_form",
                accountId: account.accountId,
                formId: result.formId,
                title: title || undefined,
                summary: title
                  ? `收集表已更新（${result.oper}）："${title}"`
                  : `收集表已更新（${result.oper}）`,
                raw: result.raw,
              });
            }
            case "get_form_info": {
              const result = await docClient.getFormInfo({
                agent: account,
                formId: params.formId,
              });
              return buildToolResult({
                ok: true,
                action: "get_form_info",
                accountId: account.accountId,
                formId: params.formId,
                title: readString(result.formInfo?.form_title) || undefined,
                summary: summarizeFormInfo(result),
                raw: result.raw,
              });
            }
            case "get_form_answer": {
              const result = await docClient.getFormAnswer({
                agent: account,
                repeatedId: params.repeatedId,
                answerIds: params.answerIds,
              });
              return buildToolResult({
                ok: true,
                action: "get_form_answer",
                accountId: account.accountId,
                repeatedId: params.repeatedId,
                summary: summarizeFormAnswer(result),
                raw: result.raw,
              });
            }
            case "get_form_statistic": {
              const result = await docClient.getFormStatistic({
                agent: account,
                requests: params.requests,
              });
              return buildToolResult({
                ok: true,
                action: "get_form_statistic",
                accountId: account.accountId,
                summary: summarizeFormStatistic(result),
                raw: result.raw,
              });
            }
            case "get_sheet_properties": {
              const result = await docClient.getSheetProperties({
                agent: account,
                docId: params.docId,
              });
              return buildToolResult({
                ok: true,
                action: "get_sheet_properties",
                accountId: account.accountId,
                docId: params.docId,
                summary: summarizeSheetProperties(result),
                raw: result.raw,
              });
            }
            case "edit_sheet_data": {
              const result = await docClient.editSheetData({
                agent: account,
                docId: params.docId,
                sheetId: params.sheetId,
                startRow: params.startRow ?? 0,
                startColumn: params.startColumn ?? 0,
                gridData: params.gridData,
                requests: params.requests, // Support direct requests for multiple operations
              });
              const summary = result.operations
                ? `在线表格已更新（${result.operations}个操作）`
                : "在线表格数据已编辑";
              return buildToolResult({
                ok: true,
                action: "edit_sheet_data",
                accountId: account.accountId,
                docId: result.docId,
                summary: summary,
                operations: result.operations,
                updatedCells: result.updatedCells,
                raw: result.raw,
              });
            }
            case "get_sheet_data": {
              const result = await docClient.getSheetData({
                agent: account,
                docId: params.docId,
                sheetId: params.sheetId,
                range: params.range,
              });
              return buildToolResult({
                ok: true,
                action: "get_sheet_data",
                accountId: account.accountId,
                docId: params.docId,
                summary: "在线表格数据已读取",
                data: result.data,
                raw: result.raw,
              });
            }
            case "modify_sheet_properties": {
              const result = await docClient.modifySheetProperties({
                agent: account,
                docId: params.docId,
                requests: params.requests,
              });
              return buildToolResult({
                ok: true,
                action: "modify_sheet_properties",
                accountId: account.accountId,
                docId: result.docId,
                summary: "在线表格属性已修改",
                raw: result.raw,
              });
            }
            case "smartsheet_add_records": {
              const result = await docClient.smartTableAddRecords({
                agent: account,
                docId: params.docId,
                sheetId: params.sheetId,
                records: params.records,
                key_type: params.key_type,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格记录已添加",
                raw: result.raw,
              });
            }
            case "smartsheet_update_records": {
              const result = await docClient.smartTableUpdateRecords({
                agent: account,
                docId: params.docId,
                sheetId: params.sheetId,
                records: params.records,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格记录已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_del_records": {
              const result = await docClient.smartTableOperate({
                agent: account,
                docId: params.docId,
                operation: "del_records",
                bodyData: params,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格记录已删除",
                raw: result.raw,
              });
            }
            case "smartsheet_get_records": {
              const result = await docClient.smartTableGetRecords({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: result.records?.length
                  ? `智能表格记录已获取：${result.records.length} 条`
                  : "智能表格记录列表已获取",
                total: result.total,
                has_more: result.has_more,
                ver: result.ver,
                raw: result.raw,
              });
            }
            case "smartsheet_get_views": {
              const result = await docClient.smartTableGetViews({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: result.views?.length
                  ? `智能表格视图已获取：${result.views.length} 个`
                  : "智能表格视图列表已获取",
                total: result.total,
                has_more: result.has_more,
                raw: result.raw,
              });
            }
            case "smartsheet_get_sheets": {
              const result = await docClient.smartTableGetSheets({
                agent: account,
                docId: params.docId,
                sheet_id: params.sheet_id,
                need_all_type_sheet: params.need_all_type_sheet,
              });
              return buildToolResult({
                ok: true,
                action: "smartsheet_get_sheets",
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格子表列表已获取：${result.sheets.length} 个`,
                raw: result.raw,
              });
            }
            case "smartsheet_add_sheet": {
              const result = await docClient.smartTableAddSheet({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格子表已添加",
                raw: result.raw,
              });
            }
            case "smartsheet_del_sheet": {
              const result = await docClient.smartTableDelSheet({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格子表已删除",
                raw: result.raw,
              });
            }
            case "smartsheet_update_sheet": {
              const result = await docClient.smartTableUpdateSheet({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格子表已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_add_view": {
              const result = await docClient.smartTableAddView({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格视图已添加：${result.view?.view_title || "未知"}`,
                raw: result.raw,
              });
            }
            case "smartsheet_del_view": {
              const result = await docClient.smartTableDelView({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格视图已删除：${params.view_ids?.length || 0} 个`,
                raw: result.raw,
              });
            }
            case "smartsheet_update_view": {
              const result = await docClient.smartTableUpdateView({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格视图已更新：${result.view?.view_title || "未知"}`,
                raw: result.raw,
              });
            }
            case "smartsheet_add_fields": {
              const result = await docClient.smartTableAddFields({ 
                agent: account, 
                docId: params.docId, 
                sheetId: params.sheetId, 
                fields: params.fields,
                autoCleanupDefaultField: params.autoCleanupDefaultField !== false, // Default true
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格字段已添加：${result.fields?.length || 0} 个`,
                raw: result.raw,
              });
            }
            case "smartsheet_del_fields": {
              const result = await docClient.smartTableDelFields({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格字段已删除：${params.field_ids?.length || 0} 个`,
                raw: result.raw,
              });
            }
            case "smartsheet_update_fields": {
              const result = await docClient.smartTableUpdateFields({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格字段已更新：${result.fields?.length || 0} 个`,
                raw: result.raw,
              });
            }
            case "smartsheet_get_fields": {
              const result = await docClient.smartTableGetFields({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: result.fields?.length
                  ? `智能表格字段已获取：${result.fields.length} 个`
                  : "智能表格字段列表已获取",
                total: result.total,
                has_more: result.has_more,
                raw: result.raw,
              });
            }
            case "smartsheet_add_group": {
              const result = await docClient.smartTableAddGroup({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格编组已添加",
                raw: result.raw,
              });
            }
            case "smartsheet_del_group": {
              const result = await docClient.smartTableDelGroup({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格编组已删除",
                raw: result.raw,
              });
            }
            case "smartsheet_update_group": {
              const result = await docClient.smartTableUpdateGroup({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格编组已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_get_groups": {
              const result = await docClient.smartTableGetGroups({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格编组列表已获取",
                raw: result.raw,
              });
            }
            case "smartsheet_add_external_records": {
              const result = await docClient.smartTableAddExternalRecords({
                agent: account,
                ...params,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格外部记录已添加",
                raw: result.raw,
              });
            }
            case "smartsheet_update_external_records": {
              const result = await docClient.smartTableUpdateExternalRecords({
                agent: account,
                ...params,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格外部记录已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_get_sheet_priv": {
              const result = await docClient.smartTableGetSheetPriv({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格子表权限已获取",
                raw: result.raw,
              });
            }
            case "smartsheet_update_sheet_priv": {
              const result = await docClient.smartTableUpdateSheetPriv({
                agent: account,
                ...params,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格子表权限已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_create_rule": {
              const result = await docClient.smartTableCreateRule({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: `智能表格成员额外权限规则已创建 (rule_id: ${result.rule_id})`,
                raw: result.raw,
              });
            }
            case "smartsheet_mod_rule_member": {
              const result = await docClient.smartTableModRuleMember({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格成员额外权限成员已更新",
                raw: result.raw,
              });
            }
            case "smartsheet_delete_rule": {
              const result = await docClient.smartTableDeleteRule({ agent: account, ...params });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                docId: params.docId,
                summary: "智能表格成员额外权限规则已删除",
                raw: result.raw,
              });
            }
            case "doc_assign_advanced_account": {
              const result = await docClient.assignDocAdvancedAccount({
                agent: account,
                userid_list: params.userid_list,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: summarizeAdvancedAccount(result.raw, "assign"),
                raw: result.raw,
              });
            }
            case "doc_cancel_advanced_account": {
              const result = await docClient.cancelDocAdvancedAccount({
                agent: account,
                userid_list: params.userid_list,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: summarizeAdvancedAccount(result.raw, "cancel"),
                raw: result.raw,
              });
            }
            case "doc_get_advanced_account_list": {
              const result = await docClient.getDocAdvancedAccountList({
                agent: account,
                ...params,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: summarizeAdvancedAccount(result, "list"),
                raw: result.raw,
              });
            }
            case "upload_doc_image": {
              const filePath = params.file_path;
              if (!fs.existsSync(filePath)) {
                throw new Error(`File not found: ${filePath}`);
              }
              const fileContent = fs.readFileSync(filePath);
              const base64Content = fileContent.toString("base64");

              const result = await docClient.uploadDocImage({
                agent: account,
                docId: params.docId,
                base64_content: base64Content,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "图片上传成功",
                details: {
                  url: result.url,
                  width: result.width,
                  height: result.height,
                  size: result.size,
                },
                raw: result.raw,
              });
            }
            default:
              throw new Error(`Unsupported action: ${String(action)}`);
          }
        } catch (err) {
          return {
            content: [
              {
                type: "text" as const,
                text: JSON.stringify(
                  {
                    ok: false,
                    action: params?.action,
                    error: err instanceof Error ? err.message : String(err),
                  },
                  null,
                  2,
                ),
              },
            ],
            details: {},
            isError: true,
          };
        }
      },
    };
  });
}
