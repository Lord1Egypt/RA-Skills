#!/usr/bin/env node

/**
 * One Calendar - 配置向导
 * 引导用户配置飞书用户 ID 并可选发送测试
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const DEFAULT_BASE_URL = 'https://img.owspace.com/Public/uploads/Download';

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((resolve) => rl.question(q, resolve));

// ── 交互：获取飞书用户 ID ───────────────────────────

async function askUserId() {
  console.log('\n📅 单向历 - 配置向导\n');
  console.log('获取飞书用户 ID 的方法：');
  console.log('  1. 运行 openclaw logs --follow');
  console.log('  2. 在飞书中给机器人发消息');
  console.log('  3. 日志中会出现 ou_xxx... 即为你的 ID\n');

  while (true) {
    const id = (await ask('请输入飞书用户 ID: ')).trim();
    if (id.startsWith('ou_')) return id;
    console.log('❌ 格式错误，ID 应以 ou_ 开头，请重试\n');
  }
}

// ── 保存配置 ────────────────────────────────────────

function saveConfig(userId) {
  const config = {
    feishu: { userId },
    settings: {
      timezone: 'Asia/Shanghai',
      baseUrl: DEFAULT_BASE_URL,
    },
  };
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
  console.log(`\n✅ 配置已保存到 ${CONFIG_PATH}`);
}

// ── 可选：发送测试 ──────────────────────────────────

async function offerTest() {
  const answer = (await ask('\n发送测试图片？(y/N) ')).trim().toLowerCase();
  if (answer !== 'y' && answer !== 'yes') {
    console.log('⏭️  跳过测试。可手动运行：node scripts/send.js\n');
    return;
  }

  console.log('正在发送...');
  try {
    execSync('node ' + path.join(__dirname, 'send.js'), { stdio: 'inherit' });
  } catch {
    console.log('❌ 测试失败，请检查用户 ID 和飞书渠道配置\n');
  }
}

// ── 主流程 ──────────────────────────────────────────

async function main() {
  const userId = await askUserId();
  saveConfig(userId);
  await offerTest();

  console.log('🎉 配置完成！\n');
  console.log('使用方法：');
  console.log('  node scripts/send.js        # 手动发送');
  console.log('  openclaw cron add \\');
  console.log('    --name "每日单向历" \\');
  console.log('    --at "0 8 * * *" \\');
  console.log('    --session isolated \\');
  console.log('    --message "node ~/.openclaw/workspace/skills/one-calendar/scripts/send.js"\n');

  rl.close();
}

main();
