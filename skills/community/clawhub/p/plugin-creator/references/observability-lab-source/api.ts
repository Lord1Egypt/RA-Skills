// 这个本地 barrel 只做一件事：把插件源码统一锚定到官方 SDK 表面，同时避免到处写长路径。
export { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
export type {
  AnyAgentTool,
  OpenClawConfig,
  OpenClawPluginApi,
  PluginHookAfterToolCallEvent,
  PluginHookBeforeMessageWriteEvent,
  PluginHookBeforeMessageWriteResult,
  PluginHookBeforeToolCallEvent,
  PluginHookLlmInputEvent,
  PluginHookLlmOutputEvent,
  PluginCommandContext,
  PluginCommandResult,
  PluginHookMessageContext,
  PluginHookMessageReceivedEvent,
  PluginHookSessionContext,
  PluginHookSessionEndEvent,
  PluginHookSessionStartEvent,
  PluginHookToolContext,
} from "openclaw/plugin-sdk/plugin-runtime";
