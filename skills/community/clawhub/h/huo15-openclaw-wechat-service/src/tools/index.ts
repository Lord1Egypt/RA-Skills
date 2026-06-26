/**
 * 微信服务号 agent tools 汇总注册入口。
 *
 * 在 plugin register() 里调用 registerWechatServiceTools(api)，
 * 会把以下 tool 注册到每个会话的 tool 列表中：
 *
 *  - wechat_service_menu         自定义菜单（基础 + 个性化）
 *  - wechat_service_message      客服消息 / 模板消息 / 一次性订阅消息 / 长期订阅通知 / 模板库
 *  - wechat_service_material     临时/永久素材上传、列表、删除
 *  - wechat_service_article      图文草稿 + 发布流水线
 *  - wechat_service_user         粉丝信息 / 标签 CRUD / 黑名单 / 备注
 *  - wechat_service_qrcode       带参数二维码 + short_key 长链转换
 *  - wechat_service_mass_send    按标签/openid 列表群发 + 预览 + 撤回
 *  - wechat_service_jssdk        JS-SDK wx.config() 签名
 *  - wechat_service_oauth        网页授权 OAuth2.0（authorize url / code→token / refresh / userinfo / validate）
 *  - wechat_service_analytics    数据统计（datacube）17 项指标
 *  - wechat_service_intelligent  智能开放：OCR 7 类 + 图像处理 3 项
 *  - wechat_service_card         卡券（精简版）：create / get / batchget / delete / consume / decrypt
 *
 * 每个工具都走统一的 accountId 解析：优先 params.accountId → toolContext.agentAccountId
 * → 默认账号。未配置账号会直接返回结构化错误（isError=true）。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import { registerAnalyticsTool } from "./analytics-tool.js";
import { registerArticleTool } from "./article-tool.js";
import { registerCardTool } from "./card-tool.js";
import { registerIntelligentTool } from "./intelligent-tool.js";
import { registerJssdkTool } from "./jssdk-tool.js";
import { registerMassSendTool } from "./mass-send-tool.js";
import { registerMaterialTool } from "./material-tool.js";
import { registerMenuTool } from "./menu-tool.js";
import { registerMessageTool } from "./message-tool.js";
import { registerOAuthTool } from "./oauth-tool.js";
import { registerQrcodeTool } from "./qrcode-tool.js";
import { registerUserTool } from "./user-tool.js";

export function registerWechatServiceTools(api: OpenClawPluginApi): void {
  registerMenuTool(api);
  registerMessageTool(api);
  registerMaterialTool(api);
  registerArticleTool(api);
  registerUserTool(api);
  registerQrcodeTool(api);
  registerMassSendTool(api);
  registerJssdkTool(api);
  registerOAuthTool(api);
  registerAnalyticsTool(api);
  registerIntelligentTool(api);
  registerCardTool(api);
}
