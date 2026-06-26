/**
 * @huo15/wechat-service — OpenClaw 微信服务号（公众号）插件入口。
 *
 * 负责：
 *  1. 暴露 runtime 给插件内部模块（access token manager、outbound 等）
 *  2. 注册 ChannelPlugin（渠道声明：chatTypes/outbound/gateway/...）
 *  3. 注册 webhook HTTP 路由（主路径 /plugins/wechat-service/{accountId}，兼容 /wechat-service/{accountId}）
 *  4. 注册 agent tools（菜单、模板消息、素材、草稿/发布、用户标签、二维码、JS-SDK 等）
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import { wechatServicePlugin } from "./src/channel.js";
import { handleWechatServiceWebhookRequest } from "./src/monitor.js";
import { setWechatServiceRuntime } from "./src/runtime.js";
import { registerWechatServiceTools } from "./src/tools/index.js";

const wechatServicePluginConfigSchema = {
  type: "object" as const,
  properties: {},
};

const plugin = {
  id: "wechat-service",
  name: "微信服务号（公众号）",
  description:
    "OpenClaw 微信服务号插件：接入公众号消息收发、菜单管理、客服/模板/订阅消息、素材/图文发布、标签群发、JS-SDK 等能力，支持多账号多 Agent 隔离与知识库双写。",
  configSchema: wechatServicePluginConfigSchema,

  register(api: OpenClawPluginApi) {
    setWechatServiceRuntime(api.runtime);

    api.registerChannel({ plugin: wechatServicePlugin });

    // 主路径 /plugins/wechat-service + 兼容 /wechat-service
    const routes = ["/plugins/wechat-service", "/wechat-service"];
    for (const path of routes) {
      api.registerHttpRoute({
        path,
        handler: handleWechatServiceWebhookRequest,
        auth: "plugin",
        match: "prefix",
      });
    }

    // Agent tools（菜单/模板消息/素材/草稿发布/标签/二维码/JS-SDK）
    registerWechatServiceTools(api);
  },
};

export default plugin;
