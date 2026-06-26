/**
 * 智能开放接口（OCR + 图像处理）agent tool。
 *
 * 单一 action：通过 `vision` 参数选 11 个操作之一。所有操作都接受公网 imgUrl。
 * 与 analytics-tool 同样的设计哲学：避免炸 actions 让 LLM 选错。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  VISION_ACTIONS,
  VISION_REGISTRY,
  type VisionAction,
} from "../api/intelligent.js";
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
      enum: ["list_visions", "run"],
      description: "list_visions 看支持的能力清单；run 执行具体能力。",
    },
    vision: {
      type: "string",
      enum: VISION_ACTIONS,
      description:
        "run 用：选择 OCR / 图像处理能力。OCR：ocr_idcard_front / ocr_idcard_back（身份证两面）/ ocr_bankcard / ocr_driving / ocr_driving_license / ocr_business_license / ocr_plate_number / ocr_common（通用印刷体）。图像：image_ai_crop（智能裁剪）/ image_scan_qrcode（二维码识别）/ image_super_resolution（图片高清化）。",
    },
    imgUrl: {
      type: "string",
      description: "run 用：图片公网 URL（HTTP/HTTPS，需可被微信侧服务器抓取）。",
    },
  },
} as const;

export function registerIntelligentTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_intelligent",
      label: "WeChat Service Intelligent",
      description:
        "微信公众号智能开放接口：OCR（身份证/银行卡/驾驶证/行驶证/营业执照/车牌/通用印刷体）+ 图像处理（AI 智能裁剪 / 二维码识别 / 图片高清化）。所有能力都通过公网 imgUrl 调用。先 list_visions 看清单，再 run vision:<name> imgUrl:<url>。",
      parameters,
      async execute(_toolCallId: string, params: Record<string, unknown>) {
        try {
          const action = String(params.action ?? "");

          if (action === "list_visions") {
            return buildToolResult({
              ok: true,
              action,
              count: VISION_ACTIONS.length,
              visions: VISION_ACTIONS,
              summary: `${VISION_ACTIONS.length} 项视觉能力可用`,
            });
          }

          if (action !== "run") {
            throw new Error(`Unsupported action: ${action}`);
          }

          const { account, tokenHandle } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId as string | undefined,
          });
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_intelligent",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          const vision = String(params.vision ?? "") as VisionAction;
          if (!VISION_ACTIONS.includes(vision)) {
            throw new Error(
              `vision 必填，且必须是以下之一：${VISION_ACTIONS.join(", ")}`,
            );
          }
          const imgUrl = requireStr(params.imgUrl, "imgUrl");
          if (!/^https?:\/\//i.test(imgUrl)) {
            throw new Error("imgUrl must be a public http(s) URL");
          }

          const fn = VISION_REGISTRY[vision];
          const raw = await fn({ account, tokenHandle, imgUrl });

          return buildToolResult({
            ok: true,
            action,
            accountId: account.accountId,
            vision,
            imgUrl,
            summary: `${vision} 已识别`,
            raw,
          });
        } catch (err) {
          return buildErrorResult({
            action: String(params?.action),
            error: asErrorMessage(err),
          });
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
