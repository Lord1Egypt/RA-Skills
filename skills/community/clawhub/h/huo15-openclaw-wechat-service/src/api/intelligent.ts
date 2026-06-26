/**
 * **智能开放接口（OCR + 图像处理）API**
 *
 * 微信公众号"智能开放"提供 OCR（身份证/银行卡/驾驶证/行驶证/营业执照/车牌/通用印刷体）
 * 和图像处理（AI 裁剪/二维码识别/图片高清化）能力。
 *
 * 使用模式：
 *  - 所有接口都支持 `img_url`（图片公网 URL）—— 本模块默认用这个，简洁，不依赖 multipart
 *  - OCR 还支持上传图片（multipart/form-data）—— 本模块暂不实现，等场景驱动
 *
 * ⚠️ "语义理解"（cgi-bin/semantic/semproxy/search）已被微信官方下线多年，本模块不实现。
 *
 * 官方文档：
 *   https://developers.weixin.qq.com/doc/offiaccount/Intelligent_Interface/Intelligent_Interface.html
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

/** 内部统一调用：所有 OCR / 图像 API 都是 POST + access_token + img_url 形态 */
async function visionQuery<T extends Record<string, unknown> = Record<string, unknown>>(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  endpoint: string;
  imgUrl: string;
  /** OCR 部分接口需要 type 区分前后两面（如身份证 type=front/back） */
  extraQuery?: Record<string, string | number>;
}): Promise<T> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<T>({
    method: "POST",
    endpoint: params.endpoint,
    query: {
      access_token: accessToken,
      img_url: params.imgUrl,
      ...(params.extraQuery ?? {}),
    },
    network: params.account.network,
  });
}

// ---------------- OCR ----------------

/** OCR：身份证。需指定 type='front'（人像面）或 'back'（国徽面） */
export async function ocrIdCard(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
  type: "front" | "back";
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/idcard", extraQuery: { type: params.type } });
}

/** OCR：银行卡 */
export async function ocrBankCard(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/bankcard" });
}

/** OCR：驾驶证 */
export async function ocrDriving(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/driving" });
}

/** OCR：行驶证 */
export async function ocrDrivingLicense(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/drivinglicense" });
}

/** OCR：营业执照 */
export async function ocrBusinessLicense(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/bizlicense" });
}

/** OCR：车牌号 */
export async function ocrPlateNumber(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/platenum" });
}

/** OCR：通用印刷体（任意场景文字） */
export async function ocrCommon(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/ocr/comm" });
}

// ---------------- 图像处理 ----------------

/** 图像：AI 智能裁剪（按主体识别裁剪比例） */
export async function imageAiCrop(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/img/aicrop" });
}

/** 图像：二维码 / 条码识别（含位置信息） */
export async function imageScanQrcode(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/img/qrcode" });
}

/** 图像：图片高清化（superresolution，2 倍超分辨率） */
export async function imageSuperResolution(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  imgUrl: string;
}): Promise<Record<string, unknown>> {
  return visionQuery({ ...params, endpoint: "cv/img/superresolution" });
}

// ---------------- METRIC_REGISTRY ----------------

/**
 * **VISION_REGISTRY**
 *
 * 给 agent tool 用，map 操作名 → 函数。OCR 身份证额外需要 type，分两条 entry。
 */
export const VISION_REGISTRY = {
  ocr_idcard_front: (p: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; imgUrl: string }) =>
    ocrIdCard({ ...p, type: "front" }),
  ocr_idcard_back: (p: { account: ResolvedWechatServiceAccount; tokenHandle: AccessTokenHandle; imgUrl: string }) =>
    ocrIdCard({ ...p, type: "back" }),
  ocr_bankcard: ocrBankCard,
  ocr_driving: ocrDriving,
  ocr_driving_license: ocrDrivingLicense,
  ocr_business_license: ocrBusinessLicense,
  ocr_plate_number: ocrPlateNumber,
  ocr_common: ocrCommon,
  image_ai_crop: imageAiCrop,
  image_scan_qrcode: imageScanQrcode,
  image_super_resolution: imageSuperResolution,
} as const;

export type VisionAction = keyof typeof VISION_REGISTRY;

export const VISION_ACTIONS: VisionAction[] = Object.keys(VISION_REGISTRY) as VisionAction[];
