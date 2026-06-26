/**
 * 公共模块入口：对外暴露 webhook 处理函数 + 常量。
 * 把内部 `transport/webhook/*` 的实现细节隔开，让 `index.ts` 看起来干净。
 */

export {
  handleWechatServiceHttpRequest,
  handleWechatServiceHttpRequest as handleWechatServiceWebhookRequest,
} from "./transport/webhook/handler.js";
export {
  WECHAT_SERVICE_ROUTE_PREFIX,
  WECHAT_SERVICE_LEGACY_PREFIX,
  resolveWebhookPath,
  resolveDerivedPathSummary,
} from "./config/derived-paths.js";
