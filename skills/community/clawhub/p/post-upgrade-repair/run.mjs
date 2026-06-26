import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const task = process.argv.slice(2).join(' ');
if (!task) {
  console.error('用法: node run.mjs "任务描述"');
  process.exit(1);
}

// 从用户自己的 openclaw.json 读取 API 凭证
const configPath = join(homedir(), '.openclaw', 'openclaw.json');
let config;
try {
  config = JSON.parse(readFileSync(configPath, 'utf8'));
} catch (e) {
  console.error('无法读取 openclaw.json:', e.message);
  console.error('请确认 OpenClaw 已安装且配置文件存在：', configPath);
  process.exit(1);
}

// 自动从主模型配置找到对应的 provider
const primaryModel = config?.agents?.defaults?.model?.primary || '';
const providerName = primaryModel.split('/')[0];
const modelId = primaryModel.split('/').slice(1).join('/');

const provider = config?.models?.providers?.[providerName];
if (!provider) {
  console.error(`找不到主模型 "${primaryModel}" 对应的 provider "${providerName}"`);
  console.error('请检查 openclaw.json 里的 agents.defaults.model.primary 配置');
  process.exit(1);
}

const apiKey = provider.apiKey;
const baseUrl = provider.baseUrl.replace(/\/$/, '');

// 找到该 provider 下匹配的模型信息
const modelInfo = provider.models?.find(m => m.id === modelId);
const useAnthropicAPI = modelInfo?.api === 'anthropic-messages' || provider.api === 'anthropic-messages';

const response = await fetch(`${baseUrl}/messages`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': apiKey,
    'anthropic-version': '2023-06-01'
  },
  body: JSON.stringify({
    model: modelId,
    max_tokens: 8192,
    messages: [{ role: 'user', content: task }]
  })
});

const data = await response.json();
const textBlock = data.content?.find(c => c.type === 'text');
if (textBlock?.text) {
  process.stdout.write(textBlock.text);
} else {
  console.error('API 错误:', JSON.stringify(data));
  process.exit(1);
}
