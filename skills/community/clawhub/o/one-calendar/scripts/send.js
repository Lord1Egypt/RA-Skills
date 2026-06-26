#!/usr/bin/env node

/**
 * One Calendar - 单向历发送脚本
 * 获取当天日期，构造图片 URL，通过飞书发送
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, '..', 'config.json');

// ── 加载并校验配置 ──────────────────────────────────

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在，请先运行：node scripts/setup.js');
    process.exit(1);
  }

  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  } catch (e) {
    console.error('❌ 配置文件格式错误:', e.message);
    process.exit(1);
  }
}

function validateUserId(id) {
  if (!id || !id.startsWith('ou_')) {
    console.error('❌ 飞书用户 ID 无效，请重新配置：node scripts/setup.js');
    process.exit(1);
  }
}

// ── 构造今日图片 URL ────────────────────────────────

function getTodayImageUrl(baseUrl) {
  const now = new Date();
  const year = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');

  return {
    label: `${year}年${+mm}月${+dd}日`,
    url: `${baseUrl}/${year}/${mm}${dd}.jpg`,
  };
}

// ── 通过 openclaw 发送图片 ──────────────────────────

function sendImage(userId, imageUrl) {
  const cmd = `openclaw message send --channel=feishu --target=${userId} --media="${imageUrl}"`;
  execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
}

// ── 主流程 ──────────────────────────────────────────

function main() {
  const config = loadConfig();
  const userId = config.feishu?.userId;
  const baseUrl = config.settings?.baseUrl || 'https://img.owspace.com/Public/uploads/Download';

  validateUserId(userId);

  const { label, url } = getTodayImageUrl(baseUrl);

  console.log(`\n📅 单向历 · ${label}`);
  console.log(`   ${url}\n`);

  try {
    sendImage(userId, url);
    console.log('✅ 发送成功！\n');
  } catch (e) {
    console.error('❌ 发送失败:', e.message, '\n');
    process.exit(1);
  }
}

main();
