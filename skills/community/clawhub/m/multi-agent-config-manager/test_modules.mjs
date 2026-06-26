import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const mods = [
  './lib/modelSelector.js',
  './lib/retryManager.js',
  './lib/thinkingCapabilities.js',
  './lib/modelAdaptation.js',
  './lib/executor.js',
  './index.js'
];

let ok = 0, fail = 0;

for (const mPath of mods) {
  try {
    await import(mPath);
    console.log('✅ ' + mPath);
    ok++;
  } catch (e) {
    console.error('❌ ' + mPath + ': ' + e.message);
    fail++;
    // 在报错时提供详细堆栈
    console.error(e.stack.split('\n').slice(1, 3).join('\n'));
  }
}

console.log('\n' + (ok === mods.length ? '✅ ALL' : `⚠️ ${ok}/${mods.length}`) + ' modules loaded');

// 测试 thinkingCapabilities 核心功能
try {
  const { checkModelThinking, selectThinkingLevel, formatCapabilitiesTable } = await import('./lib/thinkingCapabilities.js');
  
  const caps = checkModelThinking('openrouter/qwen/qwen3.6-plus:free');
  console.log('\n🧪 checkModelThinking: qwen3.6-plus:free');
  console.log('   supportsThinking:', caps.supportsThinking);
  console.log('   modes:', caps.thinkingModes);
  
  const thinking = selectThinkingLevel('openrouter/qwen/qwen3.6-plus:free', 'complex');
  console.log('   selectThinkingLevel(complex):', thinking);
  
} catch (e) {
  console.error('❌ 功能测试失败:', e.message);
}

// 测试 modelAdaptation 核心功能
try {
  const { recommendRoleConfig } = await import('./lib/modelAdaptation.js');
  const rec = recommendRoleConfig();
  console.log('\n🧪 recommendRoleConfig:');
  console.log('   available models:', rec.available);
  if (rec.coordinator) {
    console.log('   coordinator:', rec.coordinator.shortId, '(thinking:', rec.coordinator.thinking + ')');
  }
  if (rec.critic) {
    console.log('   critic:', rec.critic.shortId, '(thinking:', rec.critic.thinking + ')');
  }
  if (rec.worker) {
    console.log('   worker:', rec.worker.shortId, '(thinking:', rec.worker.thinking + ')');
  }
} catch (e) {
  console.error('❌ 功能测试失败:', e.message);
}

// 测试 thinkling fallback
try {
  const { batchDegradeThinking } = await import('./lib/thinkingCapabilities.js');
  const testSpawns = [
    { model: 'openrouter/free', thinking: 'high', label: 'test-coordinator' },
    { model: 'custom-api-inference-modelscope-cn/deepseek-ai/DeepSeek-V3.2', thinking: 'high', label: 'test-critic' },
    { model: 'custom-open-bigmodel-cn/GLM-4.7-Flash', thinking: 'low', label: 'test-worker' },
  ];
  const result = batchDegradeThinking(testSpawns);
  console.log('\n🧪 batchDegradeThinking:');
  for (const s of result.spawns) {
    console.log('   ' + (s.label || 'N/A') + ': ' + s.model + ' thinking=' + (s.thinking || 'off'));
  }
  if (result.log.length > 0) {
    console.log('   降级日志:');
    for (const l of result.log) {
      console.log('     ' + l.reason);
    }
  }
} catch (e) {
  console.error('❌ batchDegradeThinking 测试失败:', e.message);
}
