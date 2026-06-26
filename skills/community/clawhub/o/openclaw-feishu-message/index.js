import { definePluginEntry } from '/usr/lib/node_modules/openclaw/dist/plugin-sdk/plugin-entry.js';
import { registerFeishuMessageTool } from './src/tool-feishu-message.js';

export default definePluginEntry({
  id: 'openclaw-feishu-message',
  name: 'Feishu Message',
  description: 'Feishu/Lark message tool plugin for OpenClaw.',
  register(api) {
    try {
      console.log('[openclaw-feishu-message] plugin register() called');
    } catch {}
    registerFeishuMessageTool(api);
  },
});
