import { definePluginEntry } from '/usr/lib/node_modules/openclaw/dist/plugin-sdk/plugin-entry.js';
import { registerFeishuBaseTool } from './src/tool-feishu-base.js';

export default definePluginEntry({
  id: 'openclaw-feishu-base',
  name: 'Feishu Base',
  description: 'Feishu Base/Bitable tool plugin for OpenClaw.',
  register(api) {
    try {
      console.log('[openclaw-feishu-base] plugin register() called');
    } catch {}
    registerFeishuBaseTool(api);
  },
});
