/**
 * Node Connection Doctor - 诊断脚本
 * 自动检测 OpenClaw 节点连接问题
 */

const { exec } = require('child_process');
const fs = require('fs');

// 诊断模式: 'full' | 'quick'
const mode = process.argv[2] || 'quick';

console.log(`🔍 Node Connection Doctor - 开始诊断 (${mode}模式)...\n`);

// 1. 检查网关状态
function checkGatewayStatus() {
  return new Promise((resolve) => {
    exec('openclaw gateway status', (error, stdout, stderr) => {
      if (error) {
        resolve({ ok: false, error: '网关状态检查失败', details: stderr });
      } else {
        resolve({ ok: true, output: stdout });
      }
    });
  });
}

// 2. 检查节点配置
function checkNodeConfig() {
  const configPath = './config/plugins/entries/device-pair.config.json';
  try {
    if (!fs.existsSync(configPath)) {
      return { ok: false, error: '配置文件不存在' };
    }
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return { ok: true, config };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

// 3. 测试网络连通性
function testConnectivity() {
  return new Promise((resolve) => {
    exec('ping -n 1 gateway.openclaw.ai', (error) => {
      resolve({ ok: !error, error: error ? '网络不通' : null });
    });
  });
}

// 主诊断流程
async function runDiagnosis() {
  const results = [];

  // 网关状态
  const gateway = await checkGatewayStatus();
  results.push({ step: '网关状态', ...gateway });

  // 节点配置
  if (mode === 'full') {
    const config = checkNodeConfig();
    results.push({ step: '节点配置', ...config });
  }

  // 网络测试
  if (mode === 'full') {
    const network = await testConnectivity();
    results.push({ step: '网络连通性', ...network });
  }

  // 生成报告
  console.log('\n📋 诊断报告:');
  results.forEach(r => {
    const status = r.ok ? '✅' : '❌';
    console.log(`${status} ${r.step}${r.error ? ': ' + r.error : ''}`);
  });

  // 建议
  console.log('\n💡 建议:');
  if (!results[0].ok) {
    console.log('- 重启网关: openclaw gateway restart');
    console.log('- 检查 token: openclaw config get gateway.auth.token');
  }
  if (results[1] && !results[1].ok) {
    console.log('- 重新配对: openclaw node pair --reset');
  }

  return results;
}

runDiagnosis().then(() => {
  console.log('\n✅ 诊断完成');
  process.exit(0);
}).catch(err => {
  console.error('❌ 诊断失败:', err);
  process.exit(1);
});
